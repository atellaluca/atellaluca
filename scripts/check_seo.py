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
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml",
      "image": "http://www.google.com/schemas/sitemap-image/1.1"}


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
    for prefix in ("", "it/"):
        assert not (SITE / prefix / "build").exists(), "Internal build documentation was published"
    xml = (SITE / "sitemap.xml").read_bytes()
    assert gzip.decompress((SITE / "sitemap.xml.gz").read_bytes()) == xml
    entries = ET.fromstring(xml).findall("s:url", NS)
    locations = [e.findtext("s:loc", namespaces=NS) for e in entries]
    assert len(locations) == len(set(locations)), "Duplicate sitemap locations"
    documents = {}
    for location in locations:
        assert "/build/" not in location, (location, "Internal build documentation in sitemap")
        assert location.startswith(ROOT) and "/cv-pdf/" not in location and "/overview/" not in location
        path = local_file(location)
        assert path.is_file(), location
        text = path.read_text()
        doc = Document(text)
        documents[location] = doc
        assert len(doc.select("h1")) == 1, (location, "H1")
        descriptions = doc.select("meta", name="description")
        assert len(descriptions) == 1 and descriptions[0].get("content"), location
        assert len(doc.select("title")) == 1, (location, "Title")
        assert doc.select("link", rel="canonical") == [{"rel": "canonical", "href": location}], location
        assert "noindex" not in doc.select("meta", name="robots")[0]["content"], location
        assert not doc.select("meta", **{"http-equiv": "refresh"}), (location, "Indexable redirect")
        lang = "it" if urlsplit(location).path.startswith("/it/") else "en"
        assert doc.select("html")[0]["lang"] == lang, location
        assert "window.location.replace" not in text and "navigator.languages" not in text, location
        assert len(doc.schemas) == 1 and doc.schemas[0]["inLanguage"] == lang, location
        assert doc.schemas[0]["url"] == location, (location, "JSON-LD URL")
        for key in ("og:title", "og:description", "og:image", "og:locale", "og:url"):
            metadata = doc.select("meta", property=key)
            assert len(metadata) == 1 and metadata[0].get("content"), (location, key)
        assert doc.select("meta", property="og:url")[0]["content"] == location, location
        assert doc.select("meta", property="og:description")[0]["content"] == descriptions[0]["content"], location
        assert doc.select("meta", property="og:locale")[0]["content"] == ("it_IT" if lang == "it" else "en_US"), location
        for key in ("twitter:card", "twitter:title", "twitter:description", "twitter:image"):
            metadata = doc.select("meta", name=key)
            assert len(metadata) == 1 and metadata[0].get("content"), (location, key)
        for image_url in (doc.schemas[0]["image"], doc.select("meta", property="og:image")[0]["content"],
                          doc.select("meta", name="twitter:image")[0]["content"]):
            assert image_url.startswith("https://"), (location, image_url)
            if image_url.startswith(ROOT):
                assert local_file(image_url).is_file(), (location, image_url, "Missing social image")
        if doc.schemas[0]["@type"] == "ProfilePage":
            assert doc.schemas[0]["mainEntity"]["@id"] == ROOT + "#person"
        for tag, attrs in doc.tags:
            resource = attrs.get("src") if tag in ("img", "script") else attrs.get("href") if tag in ("a", "link") else None
            if not resource:
                continue
            absolute = urljoin(location, resource)
            if absolute.startswith(ROOT):
                assert local_file(absolute).is_file(), (location, resource, "Broken internal URL")

    sitemap_alternates = {
        location: {a.get("hreflang"): a.get("href") for a in entry.findall("x:link", NS)}
        for entry, location in zip(entries, locations)
    }
    for entry, location in zip(entries, locations):
        doc = documents[location]
        assert not any("hreflang" in a for a in doc.select("link", rel="alternate")), (
            location, "Head hreflang triggers Material's alternate-site sitemap probes")
        alternate_links = entry.findall("x:link", NS)
        assert len(alternate_links) == 3, (location, "Duplicate or missing hreflang")
        assert all(a.get("rel") == "alternate" for a in alternate_links), location
        alternates = sitemap_alternates[location]
        assert set(alternates) == {"en", "it", "x-default"}, (location, alternates)
        assert alternates["x-default"] == alternates["en"], location
        for alternate in alternates.values():
            assert alternate in documents, (location, alternate)
            assert sitemap_alternates[alternate] == alternates, (location, "Non-reciprocal sitemap hreflang")
        switcher = {a["hreflang"]: urljoin(location, a["href"]) for a in doc.select("a")
                    if "md-select__link" in a.get("class", "").split()}
        assert switcher == {lang: alternates[lang] for lang in ("en", "it")}, (location, "Language selector", switcher)

    services_en = ROOT + "services/"
    services_it = ROOT + "it/servizi/"
    assert services_en in documents and services_it in documents, "Primary service pages missing"
    for location in (services_en, services_it):
        doc = documents[location]
        assert sitemap_alternates[location] == {
            "en": services_en, "it": services_it, "x-default": services_en}, location
        assert any(urljoin(location, a["href"]) == location and "md-nav__link--active" in a.get("class", "").split()
                   for a in doc.select("a") if a.get("href")), (location, "Services navigation is not active")
    service_aliases = {
        "servizi/": services_en,
        "it/services/": services_it,
        "en/services/": services_en,
    }
    for old, target in service_aliases.items():
        old_url = ROOT + old
        assert old_url not in locations, (old_url, "Service redirect in sitemap")
        alias = Document((SITE / old / "index.html").read_text())
        assert alias.select("link", rel="canonical") == [{"rel": "canonical", "href": target}]
        assert alias.select("meta", **{"http-equiv": "refresh"})[0]["content"] == "0; url=" + target
        assert "noindex" in alias.select("meta", name="robots")[0]["content"], old_url
        assert not alias.select("link", rel="alternate"), old_url
        assert target in documents, (old_url, "Redirect chain or missing destination")
    for location, doc in documents.items():
        targets = [urljoin(location, a["href"]) for a in doc.select("a") if a.get("href")]
        assert not any(urlsplit(target).path.lstrip("/") in service_aliases for target in targets
                       if target.startswith(ROOT)), (location, "Link to a service redirect")
        services = services_it if urlsplit(location).path.startswith("/it/") else services_en
        assert services in targets, (location, "Services navigation missing")
    search_entries = json.loads((SITE / "search/search_index.json").read_text())["docs"]
    search_locations = {urljoin(ROOT, entry["location"]).split("#", 1)[0] for entry in search_entries}
    assert {services_en, services_it} <= search_locations, "Services missing from search"
    assert not ({ROOT + alias for alias in service_aliases} & search_locations), "Service redirects in search"
    assert not any("/cv-pdf/" in location for location in search_locations), "Print pages in search"

    for prefix in ("", "it/"):
        doc = Document((SITE / prefix / "cv-pdf/index.html").read_text())
        assert "noindex" in doc.select("meta", name="robots")[0]["content"]
        assert doc.select("link", rel="canonical")[0]["href"] == ROOT + prefix + "cv/"
        assert not doc.select("link", rel="alternate")
    redirects = list(SITE.glob("**/case-studies/*/overview/index.html"))
    # Allow the number of legacy overview redirects to grow as case studies are added.
    assert len(redirects) >= 14, len(redirects)
    for prefix in ("", "it/"):
        current = ROOT + prefix + "case-studies/importspy/architecture/"
        for slug in ("validation", "contracts", "violations"):
            old = ROOT + prefix + "case-studies/importspy/" + slug + "/"
            assert old not in locations, (old, "Redirect in sitemap")
            path = local_file(old)
            doc = Document(path.read_text())
            assert doc.select("link", rel="canonical") == [{"rel": "canonical", "href": current}], old
            redirects.append(path)
    for path in redirects:
        doc = Document(path.read_text())
        target = doc.select("link", rel="canonical")[0]["href"]
        assert target in documents, (path, target)
        assert "noindex" in doc.select("meta", name="robots")[0]["content"], path
        assert doc.select("meta", **{"http-equiv": "refresh"})[0]["content"] == "0; url=" + target
    assert "noindex" in Document((SITE / "404.html").read_text()).select("meta", name="robots")[0]["content"]
    robots = (SITE / "robots.txt").read_text()
    assert "Disallow: /" not in robots
    sitemap_urls = [line.split(":", 1)[1].strip() for line in robots.splitlines()
                    if line.lower().startswith("sitemap:")]
    assert ROOT + "sitemap.xml" in sitemap_urls, "Primary sitemap missing from robots.txt"
    for sitemap_url in sitemap_urls:
        assert sitemap_url.startswith(ROOT) and local_file(sitemap_url).is_file(), sitemap_url
        sitemap = ET.parse(local_file(sitemap_url)).getroot()
        for image in sitemap.findall(".//image:loc", NS):
            assert image.text.startswith(ROOT) and local_file(image.text).is_file(), image.text
    print(f"PASS: {len(locations)} indexable pages; reciprocal sitemap EN/IT/x-default, direct language selector and services navigation, canonical, social metadata, JSON-LD, internal URLs, search exclusions, robots/sitemaps/gzip, print exclusions, {len(service_aliases)} service redirects and {len(redirects)} legacy redirects.")


if __name__ == "__main__":
    check()
