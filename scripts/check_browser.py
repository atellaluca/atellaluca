"""Exercise the built portfolio in Chromium without contacting the live site.

Requires the existing Playwright development dependency and its Chromium binary.
The production origin is intercepted and served directly from the local build.
External fonts and Mermaid's CDN are loaded normally so their failures are visible.
"""
from __future__ import annotations

import argparse
from mimetypes import guess_type
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET

from playwright.sync_api import expect, sync_playwright


def check(site: Path, screenshots: Path | None) -> None:
    site = site.resolve()
    locations = [entry.text for entry in ET.parse(site / "sitemap.xml").findall("{*}url/{*}loc")]
    parts = urlsplit(locations[0])
    origin = f"{parts.scheme}://{parts.netloc}"
    errors: list[str] = []
    views = 0
    diagrams = 0
    if screenshots:
        screenshots.mkdir(parents=True, exist_ok=True)

    def record_error(message: str) -> None:
        errors.append(message)
        print(message, flush=True)

    def local(route):
        path = site / unquote(urlsplit(route.request.url).path).lstrip("/")
        if path.is_dir():
            path /= "index.html"
        if path.is_file():
            route.fulfill(path=str(path), content_type=guess_type(path)[0] or "application/octet-stream")
        else:
            errors.append(f"Missing local browser resource: {route.request.url}")
            route.fulfill(status=404, body="Missing local build resource")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 1440, "height": 1000})
        context.route(origin + "/**", local)
        page = context.new_page()
        cdp = context.new_cdp_session(page)
        page.on("pageerror", lambda error: record_error(f"JavaScript: {page.url}: {error}"))
        page.on("console", lambda message: record_error(f"Console: {message.location.get('url', page.url)}: {message.text}")
                if message.type == "error" else None)
        page.on("requestfailed", lambda request: record_error(f"Request: {request.url}: {request.failure}"))

        def visit(url: str) -> None:
            nonlocal views, diagrams
            page.goto(url, wait_until="networkidle")
            views += 1
            expect(page.locator("main h1")).to_have_count(1)
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), (url, "Horizontal overflow")
            count = page.locator(".mermaid").count()
            if count:
                # Material replaces each source <pre> with a <div> containing
                # an SVG in a closed shadow root. Ordinary selectors cannot see it.
                expect(page.locator("div.mermaid"), f"{url}: Mermaid diagrams must render").to_have_count(count, timeout=15000)

                def rendered_svgs(node):
                    total = int(node.get("localName") == "svg")
                    for child in node.get("children", []) + node.get("shadowRoots", []):
                        total += rendered_svgs(child)
                    return total

                def diagram_svgs(node):
                    attributes = dict(zip(node.get("attributes", [])[::2], node.get("attributes", [])[1::2]))
                    if "mermaid" in attributes.get("class", "").split():
                        return rendered_svgs(node)
                    return sum(diagram_svgs(child) for child in node.get("children", []) + node.get("shadowRoots", []))

                document = cdp.send("DOM.getDocument", {"depth": -1, "pierce": True})["root"]
                assert diagram_svgs(document) == count, (url, "Missing Mermaid SVGs in shadow DOM")
                diagrams += count
            # Check the article's outline and accessible link names after rendering.
            problems = page.locator(".md-content").evaluate("""content => {
                const errors = [];
                let previous = 0;
                for (const heading of content.querySelectorAll('h1,h2,h3,h4,h5,h6')) {
                    if (heading.closest('svg')) continue;
                    const level = Number(heading.tagName.slice(1));
                    if (level > previous + 1) errors.push('Skipped heading: ' + heading.textContent.trim());
                    previous = level;
                }
                for (const link of content.querySelectorAll('a[href]')) {
                    const name = link.textContent.trim() || link.getAttribute('aria-label') || link.title ||
                        [...link.querySelectorAll('img')].map(image => image.alt).join('').trim();
                    if (!name) errors.push('Unnamed link: ' + link.getAttribute('href'));
                }
                return errors;
            }""")
            errors.extend(f"{url}: {problem}" for problem in problems)

        for url in locations:
            visit(url)
        print(f"Checked {len(locations)} indexable pages in Chromium.", flush=True)

        service_paths = ("/services/", "/it/servizi/")
        for width, height in ((1440, 1000), (768, 1024), (390, 844), (320, 740)):
            page.set_viewport_size({"width": width, "height": height})
            for path in service_paths:
                visit(origin + path)
                expect(page.locator(".portfolio-services .portfolio-card")).to_have_count(4)
                buttons = page.locator(".portfolio-services .md-button--primary")
                expect(buttons).to_have_count(2)
                for button in buttons.all():
                    assert button.get_attribute("href").startswith("mailto:info@atellaluca.com"), path
                    assert button.bounding_box()["height"] >= 24, (path, "Small contact target")
                if screenshots and width in (1440, 390):
                    language = "it" if path.startswith("/it/") else "en"
                    page.screenshot(path=str(screenshots / f"services-{language}-{width}.png"), full_page=True)
        print("Checked both service pages at 1440, 768, 390 and 320 px.", flush=True)

        # Use the actual mobile drawer and language menu.
        page.set_viewport_size({"width": 390, "height": 844})
        visit(origin + "/it/")
        page.locator(".md-header label[for='__drawer']").click()
        page.locator(".md-nav--primary").get_by_role("link", name="Servizi", exact=True).click()
        expect(page).to_have_url(origin + "/it/servizi/")
        page.wait_for_load_state("networkidle")
        page.locator(".md-select").hover()
        page.locator(".md-select__link", has_text="English").click()
        expect(page).to_have_url(origin + "/services/")
        page.wait_for_load_state("networkidle")
        page.locator(".md-select").hover()
        page.locator(".md-select__link", has_text="Italiano").click()
        expect(page).to_have_url(origin + "/it/servizi/")
        page.wait_for_load_state("networkidle")

        # Search is a browser worker; validate it in each language, not just its JSON.
        for prefix, term in (("", "services"), ("/it", "servizi")):
            page.goto(origin + prefix + "/", wait_until="networkidle")
            page.locator(".md-header__button[for='__search']").click()
            page.locator(".md-search__input").fill(term)
            results = page.locator(".md-search-result__link")
            expect(results.first).to_be_visible(timeout=15000)
            hrefs = results.evaluate_all("links => links.map(link => link.href)")
            expected = origin + ("/it/servizi/" if prefix else "/services/")
            # Material adds ?h=<query> when search.highlight is enabled.
            assert any(urlsplit(href).path == urlsplit(expected).path for href in hrefs), (term, hrefs)
            assert all(urlsplit(href).path not in ("/servizi/", "/it/services/", "/en/services/") for href in hrefs), hrefs

        for source, target in (("/servizi/", "/services/"), ("/it/services/", "/it/servizi/"),
                               ("/en/services/", "/services/")):
            page.goto(origin + source)
            expect(page).to_have_url(origin + target)
            page.wait_for_load_state("networkidle")

        if screenshots:
            page.set_viewport_size({"width": 1440, "height": 1000})
            visit(origin + "/it/case-studies/importspy/")
            page.screenshot(path=str(screenshots / "importspy-it-1440.png"), full_page=True)
        version = browser.version
        browser.close()

    if errors:
        raise SystemExit("FAIL:\n" + "\n".join(dict.fromkeys(errors)))
    print(f"PASS: Chromium {version}; {len(locations)} indexable pages, {views} page/viewport checks, "
          f"{diagrams} rendered diagrams; mobile menu, direct language switching, EN/IT search, "
          "service redirects, contact CTAs, heading hierarchy and accessible article links; "
          "no JavaScript, console or request errors.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", nargs="?", type=Path, default=Path("site"))
    parser.add_argument("--screenshots", type=Path)
    args = parser.parse_args()
    check(args.site, args.screenshots)
