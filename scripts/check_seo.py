"""Validate the built bilingual portfolio before deployment (stdlib only)."""
import gzip
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from xml.etree import ElementTree as ET

SITE = Path(sys.argv[1] if len(sys.argv) > 1 else "site")
ROOT = "https://profile.atellaluca.com/"
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml"}


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.schemas = []
        self.json_text = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.json_text = ""

    def handle_data(self, data):
        if self.json_text is not None:
            self.json_text += data

    def handle_endtag(self, tag):
        if tag == "script" and self.json_text is not None:
            self.schemas.append(json.loads(self.json_text))
            self.json_text = None

    def select(self, tag, **attrs):
        return [a for t, a in self.tags if t == tag and all(a.get(k) == v for k, v in attrs.items())]


def local_file(url):
    path = unquote(urlsplit(url).path).lstrip("/")
    target = SITE / path
    return target / "index.html" if not path or path.endswith("/") else target


def check():
    xml = (SITE / "sitemap.xml").read_bytes()
    assert gzip.decompress((SITE / "sitemap.xml.gz").read_bytes()) == xml
    entries = ET.fromstring(xml).findall("s:url", NS)
    locations = [e.findtext("s:loc", namespaces=NS) for e in entries]
    assert len(locations) == len(set(locations)), "Duplicate sitemap locations"
    documents = {}
    for location in locations:
        assert location.startswith(ROOT) and "/cv-pdf/" not in location and "/overview/" not in location
        path = local_file(location)
        assert path.is_file(), location
        text = path.read_text()
        doc = Document(text)
        documents[location] = doc
        assert len(doc.select("h1")) == 1, (location, "H1")
        assert doc.select("meta", name="description")[0].get("content"), location
        assert doc.select("link", rel="canonical") == [{"rel": "canonical", "href": location}], location
        assert "noindex" not in doc.select("meta", name="robots")[0]["content"], location
        lang = "it" if urlsplit(location).path.startswith("/it/") else "en"
        assert doc.select("html")[0]["lang"] == lang, location
        assert "window.location.replace" not in text and "navigator.languages" not in text, location
        assert len(doc.schemas) == 1 and doc.schemas[0]["inLanguage"] == lang, location
        if doc.schemas[0]["@type"] == "ProfilePage":
            assert doc.schemas[0]["mainEntity"]["@id"] == ROOT + "#person"
        for tag, attrs in doc.tags:
            resource = attrs.get("src") if tag in ("img", "script") else attrs.get("href") if tag in ("a", "link") else None
            if not resource:
                continue
            absolute = urljoin(location, resource)
            if absolute.startswith(ROOT):
                assert local_file(absolute).is_file(), (location, resource, "Broken internal URL")

    for entry, location in zip(entries, locations):
        doc = documents[location]
        alternates = {a["hreflang"]: a["href"] for a in doc.select("link", rel="alternate") if "hreflang" in a}
        assert set(alternates) == {"en", "it", "x-default"}, (location, alternates)
        assert alternates["x-default"] == alternates["en"], location
        assert {a.get("hreflang"): a.get("href") for a in entry.findall("x:link", NS)} == alternates, location
        for alternate in alternates.values():
            assert alternate in documents, (location, alternate)
            reciprocal = {a["hreflang"]: a["href"] for a in documents[alternate].select("link", rel="alternate") if "hreflang" in a}
            assert reciprocal == alternates, (location, "Non-reciprocal hreflang")

    for prefix in ("", "it/"):
        doc = Document((SITE / prefix / "cv-pdf/index.html").read_text())
        assert "noindex" in doc.select("meta", name="robots")[0]["content"]
        assert doc.select("link", rel="canonical")[0]["href"] == ROOT + prefix + "cv/"
        assert not doc.select("link", rel="alternate")
    redirects = list(SITE.glob("**/case-studies/*/overview/index.html"))
    # Allow the number of legacy overview redirects to grow as case studies are added.
    assert len(redirects) >= 14, len(redirects)
    for path in redirects:
        doc = Document(path.read_text())
        target = doc.select("link", rel="canonical")[0]["href"]
        assert target in documents, (path, target)
        assert doc.select("meta", **{"http-equiv": "refresh"})[0]["content"] == "0; url=" + target
    assert "noindex" in Document((SITE / "404.html").read_text()).select("meta", name="robots")[0]["content"]
    assert "Disallow: /" not in (SITE / "robots.txt").read_text()
    print(f"PASS: {len(locations)} indexable pages; reciprocal EN/IT/x-default, canonical, JSON-LD, internal URLs, sitemap/gzip, print exclusions and {len(redirects)} legacy redirects.")


if __name__ == "__main__":
    check()
