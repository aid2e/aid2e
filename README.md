# AID2E Website

This website is built using Jinja2 templates for easy maintenance and consistency.

## Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

This will install:
- `jinja2` - Template engine for generating HTML pages

## Usage

### Generate the Website

To generate all HTML pages from templates, run:

```bash
python generate_site.py
```

This will:
- Read templates from the `templates/` directory
- Generate static HTML files in the root directory
- Apply the configuration defined in `generate_site.py`

### File Structure

```
aid2e/
├── templates/
│   ├── base.html              # Base template with navbar and footer
│   ├── index.html             # Home page template
│   └── under_construction.html # Template for pages under construction
├── assets/
│   ├── css/
│   │   └── style.css          # Custom styles
│   └── images/                # Logo images
├── generate_site.py           # Script to generate static HTML
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

### Customization

#### Adding/Modifying Institutes

Edit the `INSTITUTES` list in `generate_site.py`:

```python
INSTITUTES = [
    {'name': 'Institute Name', 'logo': 'logo.png', 'width': 180},
    {'name': 'Special Institute', 'logo': 'special.png', 'width': 180, 'special_class': 'white-bg-logo'},
]
```

#### Creating New Pages

1. Create a new template in `templates/` directory
2. Add page configuration to `PAGES` list in `generate_site.py`:

```python
{
    'template': 'your_template.html',
    'output': 'output-filename.html',
    'active_page': 'page-id',
    'context': {
        'custom_variable': 'value'
    }
}
```

3. Run `python generate_site.py` to regenerate

#### Modifying Common Elements

- **Navbar/Footer**: Edit `templates/base.html`
- **Styles**: Edit `assets/css/style.css`
- **Home Page**: Edit `templates/index.html`

## Development Workflow

1. Make changes to templates in `templates/` directory
2. Update configuration in `generate_site.py` if needed
3. Run `python generate_site.py` to regenerate HTML files
4. Test the generated HTML files in a browser

## Notes

- All generated HTML files (index.html, collaboration.html, etc.) are created in the root directory
- The `templates/` directory contains the source templates
- Never edit the generated HTML files directly - always edit the templates
