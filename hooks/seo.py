from __future__ import annotations

import gzip
import re
from pathlib import Path


def on_page_context(context, page, config, nav):
    if page.url == "cv-pdf/":
        page.canonical_url = f"{config.site_url.rstrip('/')}/cv/"
    elif page.url == "it/cv-pdf/":
        page.canonical_url = f"{config.site_url.rstrip('/')}/it/cv/"
    return context


def on_post_build(config):
    sitemap_path = Path(config.site_dir) / "sitemap.xml"
    if not sitemap_path.exists():
        return

    sitemap = sitemap_path.read_text(encoding="utf-8")
    sitemap = re.sub(
        r"\s*<url>\s*<loc>https://profile\.atellaluca\.com/(?:it/)?cv-pdf/</loc>.*?</url>",
        "",
        sitemap,
        flags=re.DOTALL,
    )
    sitemap = re.sub(
        r'\s*<xhtml:link rel="alternate" hreflang="[^"]+" href="https://profile\.atellaluca\.com/(?:it/)?cv-pdf/"/>',
        "",
        sitemap,
    )
    sitemap_path.write_text(sitemap, encoding="utf-8")

    gz_path = Path(config.site_dir) / "sitemap.xml.gz"
    if gz_path.exists():
        with gzip.open(gz_path, "wb") as gz_file:
            gz_file.write(sitemap.encode("utf-8"))
