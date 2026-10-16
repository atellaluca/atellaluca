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
SERVICE_URLS = {
    "/services/": "https://profile.atellaluca.com/services/",
    "/it/servizi/": "https://profile.atellaluca.com/it/servizi/",
}
SERVICE_ALIASES = {
    "servizi/": "services/",                 # default EN counterpart of servizi.it.md
    "it/services/": "it/servizi/",            # Italian counterpart of services.md
    "en/services/": "services/",            # optional explicit /en/ English URL
}


def is_services_page(url):
    return urlsplit(url).path in SERVICE_URLS


def service_alternates():
    en = SERVICE_URLS["/services/"]
    it = SERVICE_URLS["/it/servizi/"]
    return {"en": en, "it": it, "x-default": en}


def root_url(config):
    parts = urlsplit(config.site_url)
    return f"{parts.scheme}://{parts.netloc}/"


@event_priority(-110)
def on_config(config):
    # Run after i18n selects the locale, before MkDocs constructs its Page/nav
    # objects. This keeps the Italian services tab active at the printed QR URL.
    if config.theme["language"] == "it":
        def localized_nav(value):
            if isinstance(value, list):
                return [localized_nav(item) for item in value]
            if isinstance(value, dict):
                return {key: localized_nav(item) for key, item in value.items()}
            return "servizi.md" if value == "services.md" else value

        config.nav = localized_nav(config.nav)
    return config


def on_page_markdown(markdown, page, config, files):
    # Search must not advertise print-only pages or the service redirect stubs.
    if "noindex" in str(page.meta.get("robots", "")):
        page.meta["search"] = {**(page.meta.get("search") or {}), "exclude": True}
    return markdown


@event_priority(-100)
def on_page_context(context, page, config, nav):
    # i18n pairs suffixes, but these two canonical pages have translated slugs.
    # Update Material's native selector after i18n configures it for this page.
    if is_services_page(page.canonical_url):
        alternates = getattr(config.extra, "alternate", config.extra.get("alternate", []))
        for alternate in alternates:
            destination = service_alternates().get(alternate["lang"])
            if destination:
                alternate["link"] = urlsplit(destination).path.lstrip("/")
    return context


def on_env(env, config, files):
    env.globals["portfolio_root"] = root_url(config)
    return env


def on_post_page(output, page, config):
    # Material 9.7 treats every head alternate as another site's root and probes
    # <page>/sitemap.xml, then intercepts clicks as version navigation. Publish
    # reciprocal hreflang in the sitemap; keep its native, direct language menu.
    output = re.sub(r'<link\b[^>]*hreflang="[^"]+"[^>]*>', '', output)
    # Keep the Page object unchanged: MkDocs also uses it to generate sitemap loc.
    if "noindex" in str(page.meta.get("robots", "")):
        if page.url.rstrip('/').endswith('cv-pdf'):
            output = output.replace(page.canonical_url,
                                    page.canonical_url.replace('/cv-pdf/', '/cv/'))
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
        suffix = urlsplit(location).path.lstrip("/")
        if "/cv-pdf/" in location or suffix in SERVICE_ALIASES or location in seen:
            root.remove(entry)
            continue
        seen.add(location)
        if is_services_page(location):
            for alternate in list(entry.findall(f"{{{XHTML}}}link")):
                entry.remove(alternate)
            for lang, href in service_alternates().items():
                ET.SubElement(entry, f"{{{XHTML}}}link", {
                    "rel": "alternate", "hreflang": lang, "href": href})
            continue
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

    # GitHub Pages has no server-side redirects; keep the QR URL canonical while
    # routing language-switcher alternates and /en/services/ to their primary slugs.
    for old_path, new_path in SERVICE_ALIASES.items():
        old = site / old_path / "index.html"
        old.parent.mkdir(parents=True, exist_ok=True)
        destination = urljoin(config.site_url, new_path)
        target = escape(destination, quote=True)
        language = "it" if old_path.startswith("it/") else "en"
        label = "Vai ai servizi" if language == "it" else "Go to services"
        old.write_text(f'<!doctype html><html lang="{language}"><head><meta charset="utf-8">'
                       f'<meta name="robots" content="noindex,follow">'
                       f'<meta http-equiv="refresh" content="0; url={target}">'
                       f'<link rel="canonical" href="{target}"><title>{label} · Luca Atella</title>'
                       f'</head><body><h1>{label}</h1><a href="{target}">{label}</a></body></html>',
                       encoding="utf-8")

    # GitHub Pages has no configurable HTTP 301: use an immediate HTML refresh.
    for landing in site.glob("**/case-studies/*/index.html"):
        relative = landing.parent.relative_to(site).as_posix() + "/"
        destination = urljoin(config.site_url, relative)
        language = "it" if "/it/" in destination else "en"
        label = "Pagina spostata" if language == "it" else "Page moved"
        redirects = {"overview": destination}
        if landing.parent.name == "importspy":
            redirects.update({slug: urljoin(destination, "architecture/")
                              for slug in ("validation", "contracts", "violations")})
        for slug, destination in redirects.items():
            old = landing.parent / slug / "index.html"
            old.parent.mkdir(parents=True, exist_ok=True)
            target = escape(destination, quote=True)
            old.write_text(f'<!doctype html><html lang="{language}"><head><meta charset="utf-8">'
                           f'<meta name="robots" content="noindex,follow">'
                           f'<meta http-equiv="refresh" content="0; url={target}">'
                           f'<link rel="canonical" href="{target}"><title>{label} · Luca Atella</title>'
                           f'</head><body><h1>{label}</h1><a href="{target}">{label}</a></body></html>',
                           encoding="utf-8")
