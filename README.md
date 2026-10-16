# Luca Atella

**Software Architect · Backend Engineer · Systems Designer**

This repository contains my technical portfolio: selected case studies, architecture notes, and profile material.

I design and build backend and platform systems with a focus on:

- modular and plugin-based architectures
- runtime validation and contract-driven design
- cloud-portable backend platforms
- reliability, observability, and clear failure semantics
- developer tooling and system foundations

My work sits at the intersection of software architecture, production backend engineering, cloud infrastructure, and system design.

---

## Areas of Focus

- Runtime contracts and validation systems
- Plugin-based and modular backends
- Declarative DSLs for system governance
- Fault isolation and fail-fast design
- Data ingestion and validation pipelines
- Distributed and cluster-ready architectures
- Unified backends for heterogeneous data sources
- Backend platforms for IoT and smart environments
- Developer tooling for reliability and safety

---

## Selected Work

### ImportSpy
A policy-as-code admission layer for Python code and dependencies.

It separates static inspection, evidence collection, and policy evaluation from explicit code execution, making admission decisions inspectable before loading a target.

Key concepts:

- static preflight without executing the inspected code
- explicit dependency identity and execution context
- evidence collection and declarative policy evaluation
- structured admission decisions and diagnostics
- explicit execution after admission

---

## Technical Profile & Case Studies

A curated, architecture-focused presentation of my work is available on my [portfolio page](https://profile.atellaluca.com).

It includes:

- deep-dive case studies
- system design and architectural rationale
- validation and contract models
- modular backend architectures
- reliability and diagnostics systems

The portfolio is bilingual:

- English is served from the root path (`/`)
- Italian is served from `/it/`
- language selection is explicit: browser preferences never redirect a visitor away from the requested URL
- Material for MkDocs supplies the language switcher with direct localized page links; the SEO hook publishes absolute, reciprocal `hreflang` alternates and an English `x-default` in `sitemap.xml`
- `hreflang` is declared in the sitemap rather than the HTML head: Material 9.7 treats head alternates as site roots, probing nonexistent page-level sitemaps and intercepting language links as version navigation
- legacy case-study `/overview/` URLs redirect to their current landing pages using immediate HTML refresh (GitHub Pages)

The services landing pages use `/services/` in English and `/it/servizi/` in Italian. The Italian URL is the business-card QR destination; the language switcher links directly between these pages.

To install the locked dependencies and validate a local build:

```bash
poetry install --no-interaction --no-root
poetry run mkdocs build --strict
poetry run python scripts/check_seo.py site
poetry run python scripts/check_site.py site
```

The deployment workflow already requires the strict build and SEO check. The additional site check covers every generated HTML file, local fragments, image alt attributes and CSS resources.

For browser verification with the existing Playwright development dependency:

```bash
# Only needed if Chromium is not installed:
poetry run playwright install chromium
poetry run python scripts/check_browser.py site
```

The browser check serves the local build through request interception; it never reads the live portfolio. It exercises both service pages at desktop, tablet and phone widths, language switching, mobile navigation, search, redirects and Mermaid rendering. Fonts and Mermaid's CDN still require network access. Add `--screenshots /tmp/portfolio-qa` to save review images.

---

## Contact

- E-mail: [info@atellaluca.com](mailto:info@atellaluca.com)
- LinkedIn: [linkedin.com/in/luca-atella](https://www.linkedin.com/in/luca-atella/)
