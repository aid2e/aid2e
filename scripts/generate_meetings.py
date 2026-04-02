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
import markdown, re, os
from jinja2 import Template,  Environment, FileSystemLoader
from datetime import datetime

BASE_URL = os.getenv("BASE_URL", "/").strip()
if BASE_URL:
    if not BASE_URL.startswith("/"):
        BASE_URL = "/" + BASE_URL
    if not BASE_URL.endswith("/"):
        BASE_URL = BASE_URL + "/"
ROOT = Path(__file__).resolve().parents[1]
env = Environment(loader=FileSystemLoader(ROOT / "templates"))

GITBOOK_MEETINGS = ROOT / "gitbook" / "meetings"
SITE_MEETINGS = ROOT / "meetings"

PAGE_TEMPLATE = Template("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title }} - AID2E</title>
  <link rel="stylesheet" href="{{ base_url }}assets/css/style.css">
  <link rel="stylesheet" href="https://www.w3schools.com/w3css/5/w3.css">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Lato">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
</head>
<body class="darker-bg">
  <div class="w3-top">
    <div class="w3-bar dark-bg w3-card w3-left-align w3-large">
      <a class="w3-bar-item w3-button w3-hide-medium w3-hide-large w3-right w3-padding-large w3-hover-opacity w3-large" href="javascript:void(0);" onclick="myFunction()" title="Toggle Navigation Menu"><i class="fa fa-bars"></i></a>
      <a href="{{ base_url }}index.html" class="w3-bar-item w3-button w3-padding-large accent-hover">Home</a>
      <a href="{{ base_url }}collaboration.html" class="w3-bar-item w3-button w3-hide-small w3-padding-large accent-hover">Collaboration</a>
      <a href="{{ base_url }}projects.html" class="w3-bar-item w3-button w3-hide-small w3-padding-large accent-hover">Projects</a>
      <a href="{{ base_url }}publications.html" class="w3-bar-item w3-button w3-hide-small w3-padding-large accent-hover">Publications</a>
      <a href="{{ base_url }}meetings.html" class="w3-bar-item w3-button w3-hide-small w3-padding-large accent-color">Meetings</a>
      <a href="{{ base_url }}other-activities.html" class="w3-bar-item w3-button w3-hide-small w3-padding-large accent-hover">Other Activities</a>
    </div>
  </div>

  <!-- Navbar on small screens -->
  <div id="navDemo" class="w3-bar-block dark-bg w3-hide w3-hide-large w3-hide-medium w3-large">
    <a href="{{ base_url }}index.html" class="w3-bar-item w3-button w3-padding-large">Home</a>
    <a href="{{ base_url }}collaboration.html" class="w3-bar-item w3-button w3-padding-large">Collaboration</a>
    <a href="{{ base_url }}projects.html" class="w3-bar-item w3-button w3-padding-large">Projects</a>
    <a href="{{ base_url }}publications.html" class="w3-bar-item w3-button w3-padding-large">Publications</a>
    <a href="{{ base_url }}meetings.html" class="w3-bar-item w3-button w3-padding-large">Meetings</a>
    <a href="{{ base_url }}other-activities.html" class="w3-bar-item w3-button w3-padding-large">Other Activities</a>
  </div>
  
  <div class="page-header" style="padding-top: 6rem;">
    <h1>{{ title }}</h1>
  </div>
  <div class="w3-container dark-bg" style="padding: clamp(1.5rem, 3vw, 3rem);">
    <div class="w3-content markdown-content">
      {{ content|safe }}
    </div>
  </div>
  <div class="w3-container dark-bg" style="padding: 1rem 2rem;">
    <div class="w3-content" style="display:flex; justify-content:space-between; gap:1rem;">
      <div>
        {% if prev_href %}
        <a class="nav-link nav-prev" href="{{ prev_href }}"><i class="fa fa-arrow-left" aria-hidden="true"></i> Previous: {{ prev_text }}</a>
        {% endif %}
      </div>
      <div style="margin-left:auto;">
        {% if next_href %}
        <a class="nav-link nav-next" href="{{ next_href }}">Next: {{ next_text }} <i class="fa fa-arrow-right" aria-hidden="true"></i></a>
        {% endif %}
      </div>
    </div>
  </div>
  <footer class="w3-container w3-padding-64 w3-center dark-bg">
    <p>&copy; 2025 AID2E Collaboration.</p>
  </footer>
<script>
function myFunction() {
  var x = document.getElementById("navDemo");
  if (x.className.indexOf("w3-show") == -1) {
    x.className += " w3-show";
  } else {
    x.className = x.className.replace(" w3-show", "");
  }
}
</script>
</body>
</html>
""")


def md_to_html(md_text: str) -> str:
  # Use extensions that improve list handling and GitHub-style features
  # Pre-process common two-space nested-list markers into four-space
  # so python-markdown treats them as sublists (preserve original content otherwise).
  md_text = md_text.replace('\n  * ', '\n    * ').replace('\n  - ', '\n    - ')
  # Unescape backslash-escaped ampersands (users sometimes write "W\&M").
  md_text = md_text.replace('\\&', '&')
  return markdown.markdown(
    md_text,
    extensions=["fenced_code", "tables", "toc", "sane_lists"],
  )


def postprocess_html(html: str) -> str:
  # Wrap Attendees paragraph in a styled div to mimic markdown preview
  # Handle both '<p><strong>Attendees:</strong> ...</p>' and '<p>Attendees: ...</p>'
  def repl_strong(m):
    inner = m.group(1).strip()
    return f'<div class="attendees"><strong>Attendees:</strong> {inner}</div>'

  html = re.sub(r'<p>\s*<strong>\s*Attendees:\s*</strong>\s*(.*?)</p>', repl_strong, html, flags=re.I|re.S)
  html = re.sub(r'<p>\s*Attendees:\s*(.*?)</p>', repl_strong, html, flags=re.I|re.S)
  return html


def generate_page(src_md: Path, dest_html: Path, prev=None, next=None):
  md = src_md.read_text(encoding="utf-8")
  html = md_to_html(md)
  html = postprocess_html(html)
  title = src_md.stem
  prev_href = prev[1] if prev else None
  prev_text = prev[0] if prev else None
  next_href = next[1] if next else None
  next_text = next[0] if next else None
  rendered = PAGE_TEMPLATE.render(title=title, content=html, prev_href=prev_href, prev_text=prev_text, next_href=next_href, next_text=next_text, base_url = BASE_URL)
  dest_html.parent.mkdir(parents=True, exist_ok=True)
  dest_html.write_text(rendered, encoding="utf-8")


def build_all():
    # Mirror gitbook/meetings/**/*.md -> meetings/**/NAME.html
    # Generate pages with prev/next links within each category (general/technical)
    def gen_for_dir(dirpath):
      files = [p for p in sorted(dirpath.iterdir()) if p.suffix.lower() == '.md']
      # sort ascending (oldest -> newest) so next goes to newer
      files = sorted(files)
      for i, md in enumerate(files):
        rel = md.relative_to(GITBOOK_MEETINGS)
        out = SITE_MEETINGS / rel
        out = out.with_suffix('.html')
        prev = None
        nxt = None
        # prev: previous (older) entry
        if i-1 >= 0:
          date_prev, _ = extract_date_and_desc(files[i-1])
          # extract_date_and_desc returns (date, desc) but we want href
          # compute href from files[i-1]
          href_prev = files[i-1].with_suffix('.html').name
          prev = (date_prev, href_prev)
        # next: next (newer) entry
        if i+1 < len(files):
          date_next, _ = extract_date_and_desc(files[i+1])
          href_next = files[i+1].with_suffix('.html').name
          nxt = (date_next, href_next)
        generate_page(md, out, prev=prev, next=nxt)
        print(f"Wrote {out}")

    # generate for general and technical directories separately
    if (GITBOOK_MEETINGS / 'general').exists():
      gen_for_dir(GITBOOK_MEETINGS / 'general')
    if (GITBOOK_MEETINGS / 'technical').exists():
      gen_for_dir(GITBOOK_MEETINGS / 'technical')

    # After generating pages, build index for meetings.html
    build_index()


def extract_date_and_desc(md_path: Path):
    text = md_path.read_text(encoding="utf-8")
    # Try filename first for ISO date
    iso = re.search(r"(\d{4}-\d{2}-\d{2})", md_path.stem)
    if iso:
        try:
            dt = datetime.fromisoformat(iso.group(1))
            # Prefer platform-independent day format: use %-d where supported else strip leading zero
            date_text = dt.strftime("%b %d, %Y").replace(" 0", " ")
        except Exception:
            date_text = iso.group(1)
    else:
        # search in content for ISO or word date
        m_iso = re.search(r"(\d{4}-\d{2}-\d{2})", text)
        m_word = re.search(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\w*\s+\d{1,2},?\s+\d{4}", text)
        if m_iso:
            dt = datetime.fromisoformat(m_iso.group(1))
            date_text = dt.strftime("%b %d, %Y").replace(" 0", " ")
        elif m_word:
            try:
                # normalize month abbreviations
                dt = datetime.strptime(m_word.group(0), "%b %d, %Y")
                date_text = dt.strftime("%b %d, %Y").replace(" 0", " ")
            except Exception:
                date_text = m_word.group(0)
        else:
            date_text = md_path.stem

    # get short description: first non-header paragraph
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    desc = ""
    for ln in lines:
        if ln.startswith("#"):
            continue
        # skip 'Attendees:' line
        if re.match(r"Attendees?:", ln, re.I):
            continue
        desc = ln
        break
    return date_text, desc

def build_index():
    general_dir = GITBOOK_MEETINGS / "general"
    tech_dir = GITBOOK_MEETINGS / "technical"
    
    def gather(dirpath):
        items = []
        if not dirpath.exists():
            return items
        for md in sorted(dirpath.iterdir(), reverse=True):
            if md.suffix.lower() != ".md":
                continue
            date_text, desc = extract_date_and_desc(md)
            html_rel = Path("meetings") / md.relative_to(GITBOOK_MEETINGS)
            html_rel = html_rel.with_suffix('.html')

            # RELATIVE path 
            items.append((date_text, desc, html_rel.as_posix()))
        return items

    general_items = gather(general_dir)
    tech_items = gather(tech_dir)

    def group_by_year(items):
        groups = {}
        for date_text, desc, href in items:
            m = re.search(r"(\d{4})$", date_text)
            year = m.group(1) if m else "Unknown"
            groups.setdefault(year, []).append((date_text, href))
        return sorted(groups.items(), reverse=True)

    general_groups = group_by_year(general_items)
    tech_groups = group_by_year(tech_items)

    
    template = env.get_template("meetings.html")

    rendered = template.render(
        general_groups=general_groups,
        tech_groups=tech_groups,
        base_url = BASE_URL
    )

    (ROOT / "meetings.html").write_text(rendered, encoding="utf-8")
    print("Updated meetings.html using template")

if __name__ == "__main__":
    build_all()