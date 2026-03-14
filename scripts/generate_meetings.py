#!/usr/bin/env python3
"""
generate_meetings.py

Generate HTML meeting pages from gitbook/meetings Markdown source and
update meetings.html index so the site and GitBook stay in sync.

Usage:
  python scripts/generate_meetings.py

It writes HTML files into `meetings/` mirroring the `gitbook/meetings` tree.
Requires packages in `requirements.txt` (jinja2, markdown).
"""
from pathlib import Path
import markdown
from jinja2 import Template

ROOT = Path(__file__).resolve().parents[1]
GITBOOK_MEETINGS = ROOT / "gitbook" / "meetings"
SITE_MEETINGS = ROOT / "meetings"

PAGE_TEMPLATE = Template("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title }} - AID2E</title>
  <link rel="stylesheet" href="/assets/css/style.css">
  <link rel="stylesheet" href="https://www.w3schools.com/w3css/5/w3.css">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Lato">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
</head>
<body class="darker-bg">
  <div class="w3-top">
    <div class="w3-bar dark-bg w3-card w3-left-align w3-large">
      <a href="/index.html" class="w3-bar-item w3-button w3-padding-large">Home</a>
      <a href="/meetings.html" class="w3-bar-item w3-button w3-hide-small w3-padding-large accent-color">Meetings</a>
    </div>
  </div>
  <div class="page-header" style="padding-top: 6rem;">
    <h1>{{ title }}</h1>
  </div>
  <div class="w3-container dark-bg" style="padding: clamp(1.5rem, 3vw, 3rem);">
    <div class="w3-content">
      {{ content|safe }}
    </div>
  </div>
  <footer class="w3-container w3-padding-64 w3-center dark-bg">
    <p>&copy; 2025 AID2E Collaboration.</p>
  </footer>
</body>
</html>
""")


def md_to_html(md_text: str) -> str:
    return markdown.markdown(md_text, extensions=["fenced_code", "tables", "toc"])


def generate_page(src_md: Path, dest_html: Path):
    md = src_md.read_text(encoding="utf-8")
    html = md_to_html(md)
    title = src_md.stem
    rendered = PAGE_TEMPLATE.render(title=title, content=html)
    dest_html.parent.mkdir(parents=True, exist_ok=True)
    dest_html.write_text(rendered, encoding="utf-8")


def build_all():
    # Mirror gitbook/meetings/**/*.md -> meetings/**/NAME.html
    md_files = list(GITBOOK_MEETINGS.rglob("*.md"))
    for md in md_files:
        # skip SUMMARY.md and README.md at top-level when appropriate
        rel = md.relative_to(GITBOOK_MEETINGS)
        out = SITE_MEETINGS / rel
        out = out.with_suffix(".html")
        generate_page(md, out)
        print(f"Wrote {out}")


if __name__ == "__main__":
    build_all()
