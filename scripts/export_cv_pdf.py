from __future__ import annotations

import subprocess
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[1]      
PROFILE_DIR = REPO_ROOT                  
SITE_DIR = PROFILE_DIR / "site"
CV_HTML = SITE_DIR / "cv-pdf" / "index.html"
OUT_PDF = PROFILE_DIR / "docs" / "assets" / "Luca-Atella-CV.pdf"


def run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=str(cwd), check=True)


def main() -> None:
    run(["poetry", "run", "mkdocs", "build", "-f", "mkdocs.yml"], cwd=PROFILE_DIR)

    if not CV_HTML.exists():
        raise FileNotFoundError(f"CV HTML not found: {CV_HTML}")

    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto(CV_HTML.as_uri(), wait_until="networkidle")
        page.emulate_media(media="print")

        page.pdf(
            path=str(OUT_PDF),
            format="A4",
            print_background=False,
            margin={"top": "8mm", "right": "8mm", "bottom": "8mm", "left": "8mm"},
            scale=0.95,
        )


        browser.close()

    print(f"✅ CV PDF generated: {OUT_PDF}")


if __name__ == "__main__":
    main()
