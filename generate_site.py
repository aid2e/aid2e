#!/usr/bin/env python3
"""
AID2E Website Generator
This script generates static HTML pages from Jinja2 templates.
"""

from jinja2 import Environment, FileSystemLoader
import os
import json
import markdown
import re
from datetime import datetime

# Configuration
TEMPLATE_DIR = 'templates'
OUTPUT_DIR = '.'
BASE_URL = os.getenv("BASE_URL", "/")
# (No SITE_ROOT here; links are generated root-absolute where appropriate)

# Load collaborators data
def load_collaborators():
    """Load collaborators from JSON file."""
    with open('collaborators.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['institutions']

# Load projects data
def load_projects():
    """Load projects from JSON file and parse markdown content."""
    with open('projects.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    md = markdown.Markdown(extensions=['extra', 'codehilite'])
    
    # Process software infrastructure projects
    for project in data['software_infrastructure']:
        if 'markdown_file' in project:
            try:
                with open(project['markdown_file'], 'r', encoding='utf-8') as f:
                    project['content'] = md.convert(f.read())
                md.reset()
            except FileNotFoundError:
                project['content'] = '<p>Content coming soon.</p>'
    
    # Process ePIC use cases
    for project in data['epic_use_cases']:
        if 'markdown_file' in project:
            try:
                with open(project['markdown_file'], 'r', encoding='utf-8') as f:
                    project['content'] = md.convert(f.read())
                md.reset()
            except FileNotFoundError:
                project['content'] = '<p>Content coming soon.</p>'
    
    # Process other use cases
    for project in data['other_use_cases']:
        if 'markdown_file' in project:
            try:
                with open(project['markdown_file'], 'r', encoding='utf-8') as f:
                    project['content'] = md.convert(f.read())
                md.reset()
            except FileNotFoundError:
                project['content'] = '<p>Content coming soon.</p>'
    
    return data

# Load publications data
def load_publications():
    """Load publications from JSON file."""
    with open('publications.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Sort papers by year in descending order
    data['papers'].sort(key=lambda x: x.get('year', 0), reverse=True)
    # Sort talks by year and month in descending order
    data['talks'].sort(key=lambda x: (x.get('year', 0), x.get('month', 0)), reverse=True)
    # Sort other activities by year in descending order
    data['other_activities'].sort(key=lambda x: x.get('year', 0), reverse=True)

    return data

# Institute data in alphabetical order
INSTITUTES = [
    {'name': 'Brookhaven National Laboratory', 'logo': 'BNL.png', 'size': 'large'},
    {'name': 'Catholic University of America', 'logo': 'CUA.png', 'size': 'large'},
    {'name': 'Duke University', 'logo': 'Duke.png', 'size': 'large'},
    {'name': 'Jefferson Lab', 'logo': 'JLab.png', 'size': 'large'},
    {'name': 'William & Mary', 'logo': 'W&M.png', 'size': 'small', 'special_class': 'lead-institute'},
]

# Page configurations
PAGES = [
    {
        'template': 'index.html',
        'output': 'index.html',
        'active_page': 'home',
        'context': {
            'institutes': INSTITUTES
        }
    },
    {
        'template': 'collaboration.html',
        'output': 'collaboration.html',
        'active_page': 'collaboration',
        'context': {
            'institutions': load_collaborators()
        }
    },
    {
        'template': 'publications.html',
        'output': 'publications.html',
        'active_page': 'publications',
        'context': lambda: {
            'papers': load_publications()['papers'],
            'talks': load_publications()['talks']
        }
    },
    {
        'template': 'other_activities.html',
        'output': 'other-activities.html',
        'active_page': 'other-activities',
        'context': lambda: {
            'activities': load_publications()['other_activities']
        }
    },
    {
        'template': 'projects.html',
        'output': 'projects.html',
        'active_page': 'projects',
        'context': lambda: {
            'software_infrastructure': load_projects()['software_infrastructure'],
            'epic_use_cases': load_projects()['epic_use_cases'],
            'other_use_cases': load_projects()['other_use_cases']
        }
    },
    {
        'template': 'meetings.html',
        'output': 'meetings.html',
        'active_page': 'meetings',
        'context': lambda: load_meetings_index()
    },
]


def generate_site():
    """Generate all static HTML pages from templates."""
    
    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    
    # Generate each page
    for page_config in PAGES:
        print(f"Generating {page_config['output']}...")
        
        # Load template
        template = env.get_template(page_config['template'])
        
        # Prepare context
        context_data = page_config.get('context', {})
        # Handle callable context (for lazy loading)
        if callable(context_data):
            context_data = context_data()
        
        context = {
            'active_page': page_config['active_page'],
            'base_url': BASE_URL,
            **context_data
        }
        
        # Render template
        html_content = template.render(**context)
        
        # Write output file
        output_path = os.path.join(OUTPUT_DIR, page_config['output'])
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"  ✓ Created {output_path}")
    
    print("\n✅ Site generation complete!")


def extract_date_and_desc(md_path):
    """Return a (date_text, short_description) tuple for a markdown file path."""
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        return (os.path.splitext(os.path.basename(md_path))[0], '')

    # Try filename ISO date first
    stem = os.path.splitext(os.path.basename(md_path))[0]
    m_iso = re.search(r"(\d{4}-\d{2}-\d{2})", stem)
    if m_iso:
        try:
            dt = datetime.fromisoformat(m_iso.group(1))
            date_text = dt.strftime("%b %d, %Y").replace(" 0", " ")
        except Exception:
            date_text = m_iso.group(1)
    else:
        # fallback: look for ISO or word date inside content
        m_iso2 = re.search(r"(\d{4}-\d{2}-\d{2})", text)
        m_word = re.search(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\w*\s+\d{1,2},?\s+\d{4}", text)
        if m_iso2:
            try:
                dt = datetime.fromisoformat(m_iso2.group(1))
                date_text = dt.strftime("%b %d, %Y").replace(" 0", " ")
            except Exception:
                date_text = m_iso2.group(1)
        elif m_word:
            date_text = m_word.group(0)
        else:
            date_text = stem

    # short description: first non-header, non-attendees paragraph
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    desc = ''
    for ln in lines:
        if ln.startswith('#'):
            continue
        if re.match(r"Attendees?:", ln, re.I):
            continue
        desc = re.sub(r'<[^>]+>', '', ln)
        break

    return date_text, desc


def group_by_year(items):
    groups = {}
    for date_text, desc, href in items:
        m = re.search(r"(\d{4})$", date_text)
        if m:
            year = m.group(1)
        else:
            m2 = re.search(r"(\d{4})-(\d{2})-(\d{2})", href)
            year = m2.group(1) if m2 else 'Unknown'
        groups.setdefault(year, []).append((date_text, href))
    return sorted(groups.items(), reverse=True)


def load_meetings_index():
    """Scan gitbook/meetings and return dict with general/technical groups and items.

    Returns keys: general_groups, tech_groups, general_items, technical_items
    """
    root = os.path.join('gitbook', 'meetings')
    def gather(section):
        path = os.path.join(root, section)
        items = []
        if not os.path.isdir(path):
            return items
        files = sorted([f for f in os.listdir(path) if f.lower().endswith('.md')], reverse=True)
        for fn in files:
            md_path = os.path.join(path, fn)
            date_text, desc = extract_date_and_desc(md_path)
            html_rel = os.path.join('meetings', section, os.path.splitext(fn)[0] + '.html')
            # use relative links so they work on GitHub Pages project sites
            href = html_rel.replace(os.sep, '/')
            items.append((date_text, desc, href))
        return items

    general_items = gather('general')
    technical_items = gather('technical')

    general_groups = group_by_year(general_items)
    tech_groups = group_by_year(technical_items)

    return {
        'general_groups': general_groups,
        'tech_groups': tech_groups,
        'general_items': general_items,
        'technical_items': technical_items,
    }


if __name__ == '__main__':
    generate_site()
