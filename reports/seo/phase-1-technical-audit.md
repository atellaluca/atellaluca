# Phase 1 - Technical SEO Audit

## Scope

Initial technical SEO audit of the local `atellaluca` MkDocs portfolio repository published at `https://profile.atellaluca.com/`.

This phase inspected repository configuration, MkDocs templates, page metadata, robots directives, sitemap output, canonical output, JSON-LD generation, indexability, on-page SEO signals, and internal linking. No source files were changed.

## Repository Structure

SEO-relevant files and folders found:

- `mkdocs.yml`: site metadata, `site_url`, theme, plugins, i18n configuration, navigation.
- `overrides/main.html`: custom head metadata, robots meta fallback, Open Graph/Twitter metadata, JSON-LD generation, language redirect script.
- `overrides/404.html`: custom 404 template.
- `docs/robots.txt`: published robots rules and sitemap references.
- `docs/image-sitemap.xml`: static image sitemap copied to the build output.
- `docs/index.md`, `docs/profile.md`, `docs/about.md`, `docs/methodology.md`, `docs/contact.md`, `docs/cv.md`, `docs/cv-pdf.md`: main English pages.
- `docs/index.it.md`, `docs/profile.it.md`, `docs/about.it.md`, `docs/methodology.it.md`, `docs/contact.it.md`, `docs/cv.it.md`: Italian localized pages.
- `docs/case-studies/index.md` and `docs/case-studies/index.it.md`: case-study hub pages.
- `docs/case-studies/**`: case-study pages for cloud-portable fleet platform, ImportSpy, B3DO, unified backend, IoT data aggregation/digital twin, and fleet tracking.
- `docs/assets/**`: images, favicons, talks PDFs, and CV PDFs referenced by the site.
- `pyproject.toml` and `poetry.lock`: MkDocs dependencies and build toolchain.

Searches performed:

- Source search: `rg -n '"author"|ProfilePage|Person|WebSite|WebPage|Article|application/ld\+json|schema.org|robots|canonical|noindex|sitemap|site_url' .`
- Rendered output search: `rg -n '"author"|"@type": "ProfilePage"|noindex|canonical|application/ld\+json|schema.org' /tmp/atellaluca-site-audit --glob '*.html'`
- Sitemap/robots search: `rg -n '<loc>|sitemap|Disallow|Allow' /tmp/atellaluca-site-audit/sitemap.xml /tmp/atellaluca-site-audit/robots.txt /tmp/atellaluca-site-audit/image-sitemap.xml`

## Build Result

- Command attempted first: `mkdocs build --strict --site-dir /tmp/atellaluca-site-audit`
- Result: failed because `mkdocs` was not available on PATH.
- Error: `zsh:1: command not found: mkdocs`

- Command executed successfully: `poetry run mkdocs build --strict --site-dir /tmp/atellaluca-site-audit`
- Result: success.
- Output directory: `/tmp/atellaluca-site-audit`
- Warnings/info:
  - MkDocs reported `cv-pdf.md` exists in `docs` but is not included in `nav` for both English and Italian builds.
  - Italian documentation was generated under `/tmp/atellaluca-site-audit/it`.
  - `sitemap.xml`, `sitemap.xml.gz`, `robots.txt`, and `image-sitemap.xml` were generated/copied into the output.

Expected output files checked:

- Exists: `/tmp/atellaluca-site-audit/index.html`
- Exists: `/tmp/atellaluca-site-audit/profile/index.html`
- Exists: `/tmp/atellaluca-site-audit/cv/index.html`
- Exists: `/tmp/atellaluca-site-audit/cv-pdf/index.html`
- Exists: `/tmp/atellaluca-site-audit/contact/index.html`
- Exists: `/tmp/atellaluca-site-audit/methodology/index.html`
- Exists: `/tmp/atellaluca-site-audit/case-studies/index.html`
- Exists: `/tmp/atellaluca-site-audit/case-studies/importspy/overview/index.html`
- Exists: `/tmp/atellaluca-site-audit/case-studies/cloud-portable-fleet-platform/overview/index.html`
- Exists: `/tmp/atellaluca-site-audit/case-studies/iot-data-aggregation-digital-twin/overview/index.html`
- Missing: `/tmp/atellaluca-site-audit/case-studies/importspy/index.html`
- Missing: `/tmp/atellaluca-site-audit/case-studies/cloud-portable-fleet-platform/index.html`
- Missing: `/tmp/atellaluca-site-audit/case-studies/iot-data-aggregation-digital-twin/index.html`
- Exists: `/tmp/atellaluca-site-audit/robots.txt`
- Exists: `/tmp/atellaluca-site-audit/sitemap.xml`

## JSON-LD Findings

JSON-LD is generated in `overrides/main.html` inside the `extrahead` block:

- `overrides/main.html:54`: `<script type="application/ld+json">`
- `overrides/main.html:56`: `@context` is `https://schema.org`
- `overrides/main.html:57`: `@type` comes from `page.meta.schema_type`, with fallback `WebPage`
- `overrides/main.html:62-66`: `isPartOf` is a `WebSite`
- `overrides/main.html:67-89`: `author` is emitted unconditionally as a `Person`

`ProfilePage` exists in source front matter:

- `docs/index.md:6`
- `docs/profile.md:6`
- `docs/cv.md:6`
- `docs/index.it.md:6`
- `docs/profile.it.md:6`
- `docs/cv.it.md:6`

Rendered `ProfilePage` pages include `author`:

- `/`: `@type: "ProfilePage"` at rendered `index.html`, with `author` immediately after.
- `/profile/`: `@type: "ProfilePage"` at rendered `profile/index.html`, with `author` immediately after.
- `/cv/`: `@type: "ProfilePage"` at rendered `cv/index.html`, with `author` immediately after.
- Italian equivalents `/it/`, `/it/profile/`, `/it/cv/` have the same pattern.

Finding: `author` is present inside every rendered `ProfilePage` because the template emits it for all schema types. This is a structured-data risk because `author` is not appropriate for `ProfilePage` in the same way it is for `Article` or `TechArticle`.

`mainEntity` was not found in source or rendered output. The current `Person` entity is nested under `author`, not under `mainEntity`.

The nested `Person` entity is coherent as a person profile signal: it includes name, URL, sameAs links for GitHub and LinkedIn, jobTitle, and knowsAbout topics. The placement is the issue, not the person details.

`TechArticle` pages also receive `author`. This is appropriate for article-like case-study and methodology pages, but the current template applies the same property to every page type.

Potential JSON-LD conflicts:

- No multiple JSON-LD blocks were found per normal page from the custom template.
- The conflict is semantic: the same generic JSON-LD structure is used for `ProfilePage`, `CollectionPage`, `ContactPage`, `TechArticle`, and `WebPage`, even when schema properties should differ by type.
- `/cv-pdf/` is noindex but still receives JSON-LD as `WebPage`, with `author`.

## Indexability Findings

| Page | Expected Indexability | Actual Finding | Risk |
|---|---|---|---|
| `/` | Indexable | Rendered with `index,follow,max-image-preview:large`; canonical points to `https://profile.atellaluca.com/`; included in sitemap. | Low for indexability; structured-data risk due to `ProfilePage.author`. |
| `/profile/` | Indexable | Rendered with `index,follow,max-image-preview:large`; canonical points to `/profile/`; included in sitemap. | Low for indexability; structured-data risk due to `ProfilePage.author` and missing `mainEntity`. |
| `/case-studies/` | Indexable | Rendered with `index,follow,max-image-preview:large`; canonical points to `/case-studies/`; included in sitemap. | Low. Hub is indexable and links to case studies. |
| `/case-studies/importspy/` | Indexable if intended as canonical case-study URL | Not generated. Actual page is `/case-studies/importspy/overview/`, which is indexable and in sitemap. | Medium if external/internal expectations target the shorter URL. |
| `/case-studies/importspy/overview/` | Indexable | Rendered with `index,follow,max-image-preview:large`; canonical points to `/case-studies/importspy/overview/`; included in sitemap. | Low. |
| `/case-studies/cloud-portable-fleet-platform/` | Indexable if intended as canonical case-study URL | Not generated. Actual page is `/case-studies/cloud-portable-fleet-platform/overview/`, which is indexable and in sitemap. | Medium if the shorter URL is expected. |
| `/case-studies/cloud-portable-fleet-platform/overview/` | Indexable | Rendered with `index,follow,max-image-preview:large`; canonical points to `/case-studies/cloud-portable-fleet-platform/overview/`; included in sitemap. | Low. |
| `/case-studies/iot-data-aggregation-digital-twin/` | Indexable if intended as canonical case-study URL | Not generated. Actual page is `/case-studies/iot-data-aggregation-digital-twin/overview/`, which is indexable and in sitemap. | Medium if the shorter URL is expected. |
| `/case-studies/iot-data-aggregation-digital-twin/overview/` | Indexable | Rendered with `index,follow,max-image-preview:large`; canonical points to `/case-studies/iot-data-aggregation-digital-twin/overview/`; included in sitemap. | Low. |
| `/cv/` | Indexable | Rendered with `index,follow,max-image-preview:large`; canonical points to `/cv/`; included in sitemap. | Low for indexability; structured-data risk due to `ProfilePage.author`. |
| `/cv-pdf/` | Noindex | Rendered with template-level `noindex, nofollow`, but default head canonical points to `/cv-pdf/`; an additional body-level canonical points to `/cv/`; included in sitemap. | High. Noindex page is in sitemap and has conflicting canonical signals. |
| `/contact/` | Indexable | Rendered with `index,follow,max-image-preview:large`; canonical points to `/contact/`; included in sitemap. | Low. |
| `/methodology/` | Indexable | Rendered with `index,follow,max-image-preview:large`; canonical points to `/methodology/`; included in sitemap. | Low. |

No accidental global `noindex` was found. The default robots meta in `overrides/main.html` is `index,follow,max-image-preview:large`; only `docs/cv-pdf.md` defines `robots: noindex, nofollow`.

## Robots.txt Findings

`docs/robots.txt` exists and is copied to `/tmp/atellaluca-site-audit/robots.txt`.

Current rules:

- `Allow: /`
- `Disallow: /assets/talks/`
- `Disallow: /assets/cv/`
- `Sitemap: https://profile.atellaluca.com/sitemap.xml`
- `Sitemap: https://profile.atellaluca.com/image-sitemap.xml`

Findings:

- Does not block `/`.
- Does not block `/profile/`.
- Does not block `/case-studies/`.
- Does not block `/cv/`.
- Does not block `/contact/`.
- Does not block `/methodology/`.
- Does not block `/assets/` globally.
- Blocks `/assets/talks/`, which prevents crawling talk PDFs.
- Blocks `/assets/cv/`, which prevents crawling the CV PDF asset referenced from `/cv/`.
- Includes both the standard sitemap and image sitemap.

Risk: blocking `/assets/cv/` is probably intentional for duplicate CV PDF control, but it should be reviewed together with `/cv-pdf/` noindex and sitemap inclusion. Blocking PDFs can prevent crawlers from seeing assets that are linked from indexable pages.

## Sitemap Findings

`sitemap.xml` is generated by MkDocs because `site_url` is configured. `sitemap.xml.gz` is also present.

The sitemap includes:

- `https://profile.atellaluca.com/`
- `/about/`
- `/contact/`
- `/cv-pdf/`
- `/cv/`
- `/methodology/`
- `/profile/`
- `/case-studies/`
- `/case-studies/b3do/overview/`
- `/case-studies/cloud-portable-fleet-platform/overview/`
- `/case-studies/fleet-tracking/architecture/`
- `/case-studies/fleet-tracking/overview/`
- `/case-studies/importspy/architecture/`
- `/case-studies/importspy/contracts/`
- `/case-studies/importspy/overview/`
- `/case-studies/importspy/validation/`
- `/case-studies/importspy/violations/`
- `/case-studies/iot-data-aggregation-digital-twin/overview/`
- `/case-studies/unified-backend/architecture/`
- `/case-studies/unified-backend/operations/`
- `/case-studies/unified-backend/overview/`
- `/case-studies/unified-backend/plugin-system/`
- `/case-studies/unified-backend/ui-schema/`
- Italian equivalents under `/it/`

Findings:

- Homepage is included.
- `/profile/` is included.
- `/case-studies/` is included.
- Main case studies are included at their `/overview/` URLs.
- `/cv/`, `/contact/`, and `/methodology/` are included.
- `/cv-pdf/` and `/it/cv-pdf/` are included even though they are noindex.
- The shorter URLs `/case-studies/importspy/`, `/case-studies/cloud-portable-fleet-platform/`, and `/case-studies/iot-data-aggregation-digital-twin/` are not included because those pages are not generated.

`image-sitemap.xml` exists as a static file and includes image sitemap entries for:

- `/`
- `/case-studies/cloud-portable-fleet-platform/overview/`
- `/it/case-studies/cloud-portable-fleet-platform/overview/`
- `/case-studies/iot-data-aggregation-digital-twin/overview/`
- `/it/case-studies/iot-data-aggregation-digital-twin/overview/`

## Canonical Findings

Main rendered pages have self-referencing canonical tags:

- `/`: `https://profile.atellaluca.com/`
- `/profile/`: `https://profile.atellaluca.com/profile/`
- `/case-studies/`: `https://profile.atellaluca.com/case-studies/`
- `/case-studies/importspy/overview/`: `https://profile.atellaluca.com/case-studies/importspy/overview/`
- `/case-studies/cloud-portable-fleet-platform/overview/`: `https://profile.atellaluca.com/case-studies/cloud-portable-fleet-platform/overview/`
- `/case-studies/iot-data-aggregation-digital-twin/overview/`: `https://profile.atellaluca.com/case-studies/iot-data-aggregation-digital-twin/overview/`
- `/cv/`: `https://profile.atellaluca.com/cv/`
- `/contact/`: `https://profile.atellaluca.com/contact/`
- `/methodology/`: `https://profile.atellaluca.com/methodology/`

No main page was found canonicalizing incorrectly to `/`, `/cv-pdf/`, or another unrelated page.

`/cv-pdf/` has conflicting canonical output:

- Head canonical generated by MkDocs/Material: `https://profile.atellaluca.com/cv-pdf/`
- Body-level Markdown-rendered canonical from `docs/cv-pdf.md`: `https://profile.atellaluca.com/cv/`

Finding: `/cv-pdf/` does not cleanly canonicalize to `/cv/` in the document head. The intended canonical is present only as body content after Markdown rendering, which search engines may ignore or treat as invalid.

Italian `/it/cv-pdf/` has the same issue: the head canonical points to `/it/cv-pdf/`, while the body contains a canonical pointing to the English `/cv/`.

## On-page SEO Findings

Home:

- Clear H1: `Luca Atella`.
- Clear subtitle: `Software Architect - Backend & Platform Engineering`.
- Strong meta title and description aligned with software architecture, backend platforms, AWS, FastAPI, runtime contracts, IoT, and Digital Twin systems.
- Links to major case studies, profile, case-studies hub, CV, methodology, contact, LinkedIn.
- Does not visibly link to GitHub from the main content, although GitHub is present in theme social links and JSON-LD.

Profile:

- Clear H1 and description.
- Good topical coverage for architecture, platform engineering, AWS, runtime validation, IoT, edge/cloud, and geospatial work.
- Links to LinkedIn, GitHub, email, and selected case studies.
- Structured-data placement should be improved by using `mainEntity` with `Person`.

Case Studies:

- Hub page is clear and links all main case studies: cloud-portable fleet platform, ImportSpy, B3DO, unified backend, IoT data aggregation/digital twin, and fleet tracking.
- Individual overview pages have strong titles, descriptions, H1s, and topical focus.
- Some deep-dive case-study pages are indexable and included in sitemap, which may be fine, but should be intentional.
- URL shape uses `/overview/` for canonical case-study landing pages rather than shorter project root URLs.

CV:

- Strong title, description, H1, and content structure.
- Links to email, GitHub, LinkedIn, and PDF download.
- Uses `ProfilePage`, but receives `author` instead of a person-focused `mainEntity`.
- PDF asset is linked from an indexable page but `/assets/cv/` is disallowed in robots.

Contact:

- Clear title, description, H1, contact methods, and fit criteria.
- Links to GitHub and LinkedIn are present.
- Page type is `ContactPage`; generic JSON-LD template still emits `author`.

Methodology:

- Clear title, description, H1, and article-like topical structure.
- Uses `TechArticle`; `author` is appropriate here.

## Internal Linking Findings

Homepage links:

- `/profile/`: yes, via `profile.md`.
- `/case-studies/`: yes, via `case-studies/index.md`.
- `/case-studies/cloud-portable-fleet-platform/overview/`: yes.
- `/case-studies/importspy/overview/`: yes.
- `/case-studies/iot-data-aggregation-digital-twin/overview/`: yes.
- `/cv/`: yes, via `cv.md`.
- `/contact/`: yes, via `contact.md`.
- GitHub: not in the main homepage content; available via theme social configuration and JSON-LD.
- ImportSpy: yes, linked as a case study.

Case studies index:

- Links all main case studies found in nav: cloud-portable fleet platform, ImportSpy, B3DO, unified backend, IoT data aggregation/digital twin, and fleet tracking.

CV and Contact:

- CV links GitHub, LinkedIn, email, PDF download, and discusses selected projects, but the checked excerpt does not show prominent internal links back to portfolio case-study URLs.
- Contact links GitHub, LinkedIn, and email, but does not link back to case studies or CV.

Finding: internal linking is sufficient from the home and case-study hub, but CV and Contact could better reinforce portfolio navigation with contextual links to case studies and the case-study hub.

## Risks

1. `ProfilePage` JSON-LD contains `author` because `overrides/main.html` emits `author` globally. This affects `/`, `/profile/`, `/cv/`, and Italian equivalents.
2. `ProfilePage` JSON-LD lacks `mainEntity`, so the person profile entity is not modeled in the strongest expected shape.
3. `/cv-pdf/` and `/it/cv-pdf/` are noindex but still included in `sitemap.xml`.
4. `/cv-pdf/` has conflicting canonical signals: head canonical points to `/cv-pdf/`, while a body-rendered canonical points to `/cv/`.
5. Italian `/it/cv-pdf/` body canonical points to English `/cv/`, not `/it/cv/`, while the head canonical points to `/it/cv-pdf/`.
6. Robots blocks `/assets/cv/`, including the linked CV PDF asset, which may be intentional but should be coordinated with the noindex/canonical strategy.
7. Expected short case-study root URLs are not generated; actual canonical pages are under `/overview/`.
8. CV and Contact pages have weaker internal links back to case studies compared with the homepage and case-study hub.

## Recommended Next Commits

1. `fix(schema): correct ProfilePage structured data`
2. `fix(seo): align cv pdf noindex sitemap and canonical metadata`
3. `fix(seo): clarify case study canonical url strategy`
4. `docs(content): strengthen cv contact and case study internal links`
5. `docs(case-studies): review indexability of deep dive case study pages`

## Phase 1 Summary

The site builds successfully with Poetry and has a generally solid technical SEO baseline: correct `site_url`, generated sitemap, published robots file, indexable core pages, self-canonical main pages, coherent titles/descriptions, and good home-to-case-study linking.

The main issues are concentrated in structured data and CV PDF handling. The next highest-value change is to make JSON-LD schema-type-aware: `ProfilePage` should use a coherent `mainEntity` `Person` and should not receive the generic `author` property. After that, `/cv-pdf/` should be removed from the sitemap or otherwise excluded from sitemap generation, and its canonical/noindex signals should be made consistent in the document head.
