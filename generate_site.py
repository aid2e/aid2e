#!/usr/bin/env python3
"""
AID2E Website Generator
This script generates static HTML pages from Jinja2 templates.
"""

from jinja2 import Environment, FileSystemLoader
import os
import json

# Configuration
TEMPLATE_DIR = 'templates'
OUTPUT_DIR = '.'

# Load collaborators data
def load_collaborators():
    """Load collaborators from JSON file."""
    with open('collaborators.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['institutions']

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
        'template': 'under_construction.html',
        'output': 'publications.html',
        'active_page': 'publications',
        'context': {
            'page_title': 'Publications'
        }
    },
    {
        'template': 'under_construction.html',
        'output': 'other-works.html',
        'active_page': 'other-works',
        'context': {
            'page_title': 'Other Works'
        }
    },
    {
        'template': 'under_construction.html',
        'output': 'projects.html',
        'active_page': 'projects',
        'context': {
            'page_title': 'Projects'
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
        context = {
            'active_page': page_config['active_page'],
            **page_config.get('context', {})
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
