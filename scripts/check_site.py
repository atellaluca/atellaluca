"""Check every generated HTML page and CSS asset, including non-indexed pages.

Uses only the standard library. External URLs are deliberately not requested.
"""
from __future__ import annotations

import argparse
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from xml.etree import ElementTree as ET


class Document(HTMLParser):
    def __init__(self, text: str):
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.duplicates: set[str] = set()
        self.references: list[str] = []
        self.missing_alt = 0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        identifier = attrs.get("id")
        if identifier:
            if identifier in self.ids:
                self.duplicates.add(identifier)
            self.ids.add(identifier)
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        if tag == "img" and "alt" not in attrs:
            self.missing_alt += 1
        for attr in ("href", "src", "poster"):
            if attrs.get(attr):
                self.references.append(attrs[attr])
        if tag == "object" and attrs.get("data"):
            self.references.append(attrs["data"])
        # Data URLs may contain commas; responsive local assets do not.
        if attrs.get("srcset") and "data:" not in attrs["srcset"]:
            self.references.extend(item.strip().split()[0]
                                   for item in attrs["srcset"].split(",") if item.strip())


def check(site: Path) -> None:
    site = site.resolve()
    sitemap = ET.parse(site / "sitemap.xml")
    first_url = sitemap.findtext("{*}url/{*}loc")
    if not first_url:
        raise SystemExit("FAIL: sitemap has no URLs")
    parts = urlsplit(first_url)
    origin = f"{parts.scheme}://{parts.netloc}/"
    documents = {path: Document(path.read_text(encoding="utf-8"))
                 for path in sorted(site.rglob("*.html"))}
    errors: set[str] = set()
    references = 0

    def validate(source: Path, resource: str) -> None:
        nonlocal references
        relative = source.relative_to(site).as_posix()
        # Directory URLs are how MkDocs pages are served, including relative links.
        source_url = origin + (relative[:-10] if relative.endswith("index.html") else relative)
        url = urlsplit(urljoin(source_url, resource))
        if url.scheme not in ("http", "https") or url.netloc != parts.netloc:
            return
        references += 1
        target = site / unquote(url.path).lstrip("/")
        if target.is_dir():
            target /= "index.html"
        if not target.is_file():
            errors.add(f"{relative}: missing local resource {resource}")
        elif target in documents and url.fragment and unquote(url.fragment) not in documents[target].ids:
            errors.add(f"{relative}: missing fragment in {resource}")

    for path, document in documents.items():
        relative = path.relative_to(site)
        for identifier in document.duplicates:
            errors.add(f"{relative}: duplicate id {identifier}")
        if document.missing_alt:
            errors.add(f"{relative}: {document.missing_alt} images without an alt attribute")
        for resource in document.references:
            validate(path, resource)

    css_files = sorted(site.rglob("*.css"))
    for path in css_files:
        css = re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.S)
        for match in re.finditer(r"url\(\s*(['\"]?)(.*?)\1\s*\)", css, flags=re.S):
            validate(path, match.group(2).strip())

    if errors:
        raise SystemExit("FAIL:\n" + "\n".join(sorted(errors)))
    print(f"PASS: {len(documents)} HTML files, {len(css_files)} CSS files, "
          f"{references} local references; targets, fragments, unique IDs and image alt attributes.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", nargs="?", type=Path, default=Path("site"))
    check(parser.parse_args().site)
