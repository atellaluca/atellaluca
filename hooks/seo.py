"""Keep language signals and migration URLs consistent on GitHub Pages."""
from __future__ import annotations

import gzip
import re
from html import escape
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from xml.etree import ElementTree as ET

from mkdocs.plugins import event_priority

SM = "http://www.sitemaps.org/schemas/sitemap/0.9"
XHTML = "http://www.w3.org/1999/xhtml"


def root_url(config):
    parts = urlsplit(config.site_url)
    return f"{parts.scheme}://{parts.netloc}/"


def on_env(env, config, files):
    env.globals["portfolio_root"] = root_url(config)
    return env


def on_post_page(output, page, config):
    # Keep the Page object unchanged: MkDocs also uses it to generate sitemap loc.
    if "noindex" in str(page.meta.get("robots", "")):
        output = re.sub(r'<link\b[^>]*hreflang="[^"]+"[^>]*>', '', output)
        if page.url.rstrip('/').endswith('cv-pdf'):
            output = output.replace(page.canonical_url,
                                    page.canonical_url.replace('/cv-pdf/', '/cv/'))
        return output
    # Preserve Material's switcher, normalize only the rendered head annotations.
    def absolute_alternate(match):
        return re.sub(r'href="([^"]+)"', lambda href: 'href="' +
                      urljoin(page.canonical_url, href.group(1)) + '"', match.group(0))

    output = re.sub(r'<link\b[^>]*hreflang="[^"]+"[^>]*>', absolute_alternate, output)
    english = re.search(r'<link\b[^>]*href="([^"]+)"[^>]*hreflang="en"[^>]*>', output)
    if english and "noindex" not in str(page.meta.get("robots", "")):
        output = output.replace("</head>", '<link rel="alternate" hreflang="x-default" href="' +
                                english.group(1) + '">\n</head>', 1)
    return output


@event_priority(-200)
def on_post_build(config):
    site = Path(config.site_dir)
    sitemap_path = site / "sitemap.xml"
    if not sitemap_path.exists():
        return
    ET.register_namespace("", SM)
    ET.register_namespace("xhtml", XHTML)
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    seen = set()
    for entry in list(root):
        location = entry.findtext(f"{{{SM}}}loc", "")
        if "/cv-pdf/" in location or location in seen:
            root.remove(entry)
            continue
        seen.add(location)
        for alternate in list(entry.findall(f"{{{XHTML}}}link")):
            if "/cv-pdf/" in alternate.get("href", ""):
                entry.remove(alternate)
        english = next((a.get("href") for a in entry.findall(f"{{{XHTML}}}link")
                        if a.get("hreflang") == "en"), None)
        if english and not any(a.get("hreflang") == "x-default" for a in entry):
            ET.SubElement(entry, f"{{{XHTML}}}link", {
                "rel": "alternate", "hreflang": "x-default", "href": english})
    xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    sitemap_path.write_bytes(xml)
    with gzip.open(site / "sitemap.xml.gz", "wb") as compressed:
        compressed.write(xml)

    # GitHub Pages has no configurable HTTP 301: use an immediate HTML refresh.
    for landing in site.glob("**/case-studies/*/index.html"):
        relative = landing.parent.relative_to(site).as_posix() + "/"
        destination = urljoin(config.site_url, relative)
        old = landing.parent / "overview" / "index.html"
        old.parent.mkdir(parents=True, exist_ok=True)
        target = escape(destination, quote=True)
        language = "it" if "/it/" in destination else "en"
        label = "Pagina spostata" if language == "it" else "Page moved"
        old.write_text(f'<!doctype html><html lang="{language}"><head><meta charset="utf-8">'
                       f'<meta http-equiv="refresh" content="0; url={target}">'
                       f'<link rel="canonical" href="{target}"><title>{label} · Luca Atella</title>'
                       f'</head><body><h1>{label}</h1><a href="{target}">{label}</a></body></html>',
                       encoding="utf-8")
