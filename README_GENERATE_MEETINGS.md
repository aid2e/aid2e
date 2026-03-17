# Generating Meetings HTML

This repository includes a small script to generate site HTML pages from the GitBook Markdown source in `gitbook/meetings`.

Usage:

1. Install dependencies (recommended in a virtualenv):

```bash
pip install -r requirements.txt
```

2. Run the generator:

```bash
python scripts/generate_meetings.py
```

The script writes HTML files under `meetings/` corresponding to the Markdown files in `gitbook/meetings`.
