# FAQ

## Why JSON instead of SQL?

JSON files are portable, easy to inspect, trivial to back up with rsync, and require zero database setup. At the scale of a personal news aggregator (thousands of articles), filesystem reads are fast enough that a database provides no meaningful benefit. If you need multi-user access or complex queries, the JSON schema is simple enough to import into SQLite or PostgreSQL.

## Does translation require an API key?

No. googletrans is a free Python library that uses the Google Translate web API. No API key, no registration, no rate limiting for personal use. If you need higher throughput or production reliability, replace `translate_text()` with a paid service (DeepL, Google Cloud Translation).

## Can I add my own RSS feeds?

Yes. Open the relevant script (daily_briefing.py, international_news.py, or tech_news.py) and add a new entry to the `FEEDS` dictionary:

```python
FEEDS = {
    "my-feed": {
        "name": "My Feed Name",
        "url": "https://example.com/rss",
        "category": "economic",
        "tags": ["my-tag"],
    },
}
```

The next time the script runs, it will fetch, scrape, and store articles from your new feed.

## Can I deploy with Docker?

Not yet. The project currently runs directly on Python. A Docker Compose setup is on the roadmap. For now, installation is three commands: `git clone`, `pip install`, `python app.py`.

## How do I change the design?

All visual tokens are CSS custom properties in `frontend/static/style.css`. Colors, fonts, spacing, and max-width are governed by variables in the `:root` block. Dark mode variables are in `[data-theme="dark"]`. No build step, no framework — edit the file and reload the page.

## The agent skill says it uses CloakBrowser. Is it required?

No. The system works with Playwright, which is installed automatically. CloakBrowser is only needed for sites with aggressive anti-bot protection (Cloudflare, FingerprintJS). For normal RSS feeds (BBC, Guardian, TechCrunch, VnExpress), readability-lxml and requests are sufficient.

## How many articles can it handle?

The filesystem backend has been tested with 500+ JSON files with no performance issues. The Flask server reads individual files on demand and does not load everything into memory. Search iterates through files — for very large archives, adding SQLite would improve search speed.
