# Changelog

All notable changes to The Agent Times will be documented in this file.

## [1.0.0] — 2026-07-04

### Added
- 🗞️ **News Aggregator Engine** — Scrape, parse, and display articles from 50+ RSS feeds
- 🌍 **International News** — 10-country RSS feeds with auto-translate to Vietnamese (US, UK, Japan, China, France, Germany, South Korea, Australia, Singapore, India)
- 🇻🇳 **Vietnamese News** — 9 RSS feeds covering economics, technology, law, science, F&B from VnExpress, Tuổi Trẻ, VietnamNet
- 💻 **Technology Section** — Tech news from VnExpress Số hóa + international (TechCrunch, Wired, The Verge), full content + images + Vietnamese translation
- 🐙 **GitHub Radar** — Trending repos scraper, filtered to 100+ stars, each repo becomes a full article
- 🔍 **Universal Article Scraper** — `article_scraper.py` with 6-step image fallback chain, readability-lxml extraction, automatic HTML cleanup
- 📄 **Clean Article HTML** — VnExpress wrappers stripped, classes removed, `rel="dofollow"` eliminated — professional-grade output
- 🌏 **Auto-Translation** — googletrans integration for international content to Vietnamese
- 🎨 **Responsive News Design** — NYT/Axios-inspired, 3-column grid, featured hero with full-bleed image
- 🌓 **Dark/Light Theme** — Semantic token swap, navy-based dark mode `#0d1929`
- 📰 **Article Sidebar** — Right column with related headlines for continued reading
- 📅 **Date Archive** — Browse articles by date with calendar picker and prev/next navigation
- 🔍 **Full-Text Search** — Search across all articles by title, content, tags, and category
- 🕐 **Daily Automation** — 6 cronjob pipelines for fully unattended operation
- 🛠️ **Desktop Launcher** — One-click desktop shortcut to start server + open browser
- 📘 **AI Design Skills** — `design-master` (Design-Craft + Laws of UX) for AI agents without vision
- 🖥️ **Flask Web Server** — Lightweight, zero-config, runs on port 5050

### Fixed
- HTML cleanup pipeline removes VnExpress `fck_detail`, `Normal`, `title-detail mt20` classes
- Image fallback chain covers OG, Twitter, article containers, figures, and generic img tags
- Title fallback chain handles generic site names, short titles, and readability failures
- Theme toggle missing `onclick` handler — restored
- Category system restructured: `economy` (replaces `daily-briefing`), `technology`, `github` separated
- GitHub articles filtered to 100+ stars only
- Raw low-word-count reports cleaned from economic category
- Race condition where parallel subagents overwrote each other's file changes

### Changed
- Category nav: 8 links (Tất cả, Kinh tế, Công nghệ, GitHub, Pháp lý, F&B, Affiliate, Phân tích)
- All cronjobs updated to daily frequency
- International news moved to `--scrape` mode for full content
- Article page layout: content 680px left + sidebar 300px right
- CSS complete rewrite with design-master principles (4px grid, 3-layer tokens, 5-level typography)
