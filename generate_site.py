#!/usr/bin/env python3
"""
AID2E Website Generator
This script generates static HTML pages from Jinja2 templates.
"""

from jinja2 import Environment, FileSystemLoader
import os
import json
import markdown

# Configuration
TEMPLATE_DIR = 'templates'
OUTPUT_DIR = '.'

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


if __name__ == '__main__':
    generate_site()
