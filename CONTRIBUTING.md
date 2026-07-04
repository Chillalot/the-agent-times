# Contributing to The Agent Times

Thank you for considering contributing! This project is designed to be easily extended with new RSS feeds, categories, and design themes.

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/the-agent-times.git
cd the-agent-times

# Install dependencies
pip install -r frontend/requirements.txt

# Start the development server
cd frontend
python3 app.py
# → http://localhost:5050
```

## Project Structure

```
the-agent-times/
├── frontend/           # Flask web app (app.py, templates, CSS)
├── scripts/            # Data collection & processing scripts
├── skills/             # AI agent skills (design, UX, scaffolding)
├── data/reports/       # Article JSON files (auto-generated)
└── docs/               # Documentation, architecture
```

## Adding a New RSS Feed

1. Open the relevant script (`daily_briefing.py`, `international_news.py`, or `tech_news.py`)
2. Add a new entry to the `FEEDS` dictionary:

```python
FEEDS = {
    "my-feed": {
        "name": "My Feed Name",
        "url": "https://example.com/rss",
        "category": "economic",  # or technology/github/legal/fnb/affiliate
        "tags": ["my-tag", "tin-tức"],
    },
}
```

3. Category auto-detection happens in `autoreport_daily.sh` based on URL patterns. Add patterns if needed.

## Adding a New Category

1. Edit `frontend/app.py` → Add to `CATEGORY_MAP` and `CATEGORY_COLORS`
2. Edit `frontend/templates/base.html` → Add nav link
3. Create or update a scraper script that produces articles with your new `category` field

## Customizing the Design

All visual tokens are in `frontend/static/style.css`:
- **Colors**: Edit `:root` CSS custom properties
- **Fonts**: Change `--font-heading` and `--font-body`
- **Layout**: Adjust `--max-width` and `--content-width`
- **Dark mode**: Edit `[data-theme="dark"]` section

The design follows [Design-Craft](https://github.com/FasalZein/design-craft) principles:
- 4px spacing grid
- 3-layer color tokens (Primitives → Semantic → Component)
- 5-level typography scale
- Only `transform` + `opacity` animations

## Style Guidelines

- **Python**: Follow PEP 8, use type hints
- **HTML**: Semantic HTML5, Jinja2 templates
- **CSS**: Custom properties, BEM-like naming, design tokens
- **JavaScript**: Vanilla JS, GSAP for animations

## Commit Format

```
type(scope): description

Examples:
feat(rss): add Singapore Straits Times feed
fix(scraper): handle missing og:image meta tag
design(css): adjust article card spacing
docs(readme): add international news setup
```

## Pull Request Checklist

- [ ] Tested locally (`python3 app.py`)
- [ ] All categories render correctly (`/category/...`)
- [ ] Articles have images + full content
- [ ] Dark mode works
- [ ] Mobile responsive
- [ ] CHANGELOG.md updated (if notable change)

## Issue Reporting

Report issues at: https://github.com/Chillalot/the-agent-times/issues

When reporting:
1. Describe expected vs actual behavior
2. Include error logs if applicable
3. Mention your Python version and OS

## License

MIT — feel free to use, modify, and distribute.
