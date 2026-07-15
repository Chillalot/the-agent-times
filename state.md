# The Agent Times — State

## Architecture

```
RSS feeds ──→ scrape (requests) ──→ browser fallback (cloakbrowser) ──→ translate ──→ build article JSON ──→ Flask server
```

- **`scripts/tech_news.py`** — VnExpress + international tech feeds, translates EN→VI
- **`scripts/international_news.py`** — 10 countries (US, UK, Japan, China, France, Germany, SKorea, Australia, Singapore, India), translates all to VI
- **`scripts/daily_briefing.py`** — VnExpress daily digest
- **`scripts/github_article_writer.py`** — GitHub commit summaries
- **`scripts/website_cloner.py`** — Clones articles from configured sites
- **`frontend/app.py`** — Flask app serving articles at localhost:5050

## Library (`scripts/lib/`)

| Module | Purpose |
|---|---|
| `article_writer.py` | `build_full_article()` — constructs final JSON with content, images, tags, categories |
| `browser_scraper.py` | Cloakbrowser wrapper — singleton browser, `fetch_article()` returns full HTML with all images |
| `translate.py` | `deep-translator` singleton (GoogleTranslator), replaces broken googletrans |
| `rss.py` | RSS feed parsing |
| `storage.py` | File I/O for article JSONs |
| `config.py` | Source configs (feeds, countries, categories) |

## Key Fixes

### Translation HTML stripping (latest fix)
`international_news.py` and `tech_news.py` were calling `BeautifulSoup(raw_html).get_text()` before translating, which stripped ALL HTML — including gallery images fetched by cloakbrowser. Fixed by extracting `<img>` tags before translation and re-appending them as `<div class="article-gallery">` after translated text.

### Browser fallback
`article_scraper.py` `fetch_article()` falls back to cloakbrowser when content has < 3 images. `_browser_fetch()` uses readability for text extraction + injects all `<img>` tags from the full browser HTML via string concatenation (readability output lacks `<body>` tag, so `soup.body.append()` caused NoneType error).

### Gallery image injection in `build_full_article()`
`content_parts` builder was skipping `<div>` wrappers that contained only images (no text nodes). Added `elif el.find_all("img")` check.

### googletrans → deep-translator
Cloakbrowser installation upgraded httpx from 0.13.3 → 0.28.1, breaking googletrans. Replaced with `deep-translator` in `scripts/lib/translate.py`.

## Current State

- **Server:** running at `http://localhost:5050`
- **Tests:** 62 passing (`python -m pytest tests/`)
- **Articles:** ~29 articles (3 VnExpress + 15 Australia + 6 India + leftovers), 15-53 images each for Australia
- **Cloakbrowser:** v0.4.10, downloads Chromium ~200MB on first run, singleton browser instance

## Known Issues

| Issue | Status |
|---|---|
| BBC (bbc.com) DNS blocked from server — cloakbrowser can't fix | Open |
| BBC (bbc.co.uk) TCP timeout | Open |
| Korea Herald returns 403 | Open |
| deep-translator rate limits with many chunks | Workaround: sleep 1s between chunks (already in code) |
| `build_full_article()` uses `_clean_light()` which may strip some images | Needs review |
