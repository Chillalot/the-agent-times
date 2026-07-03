# 🗞️ The Agent Times

**A self-hosted, AI-powered news aggregator** — crawl, translate, and publish a personalized daily newspaper from global sources, all automated.

> Built by an AI agent for a human who wanted a newspaper that actually reads the sources for them.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🌍 **50+ RSS feeds** | Vietnam (VnExpress, Tuổi Trẻ, VietnamNet) + 10 countries (BBC, Guardian, TechCrunch, Wired, DW, SCMP...) |
| 🔄 **Auto-scrape** | Every link in the RSS → full article content + lead image extracted |
| 🌏 **Auto-translate** | International news translated to Vietnamese (via googletrans) |
| 🐙 **GitHub Radar** | Trending repos with 100+ stars, each becomes an article |
| 🐣 **Beginner-friendly** | Article scraper handles all sources (VnExpress, Guardian, BBC, TechCrunch...) |
| 🎨 **Clean design** | NYT/Axios-inspired, dark/light theme, responsive, GSAP animations |
| 📰 **Sidebar browsing** | Article page has sidebar with headlines of related articles |
| 📅 **Date archive** | Browse articles by date with calendar picker |
| 🔍 **Full-text search** | Search across all articles |
| 🕐 **Fully automated** | Cronjobs run daily — wake up to fresh news |
| 🛠️ **Customizable** | Add your own RSS feeds, categories, design theme |
| 📘 **AI Design Skills** | Comes with `design-master` (Design-Craft + Laws of UX) for AI agents without vision |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js (for some optional scripts)
- Git

### 1. Clone & Install
```bash
git clone https://github.com/YOUR_USERNAME/the-agent-times.git
cd the-agent-times
pip install -r frontend/requirements.txt
```

### 2. Start the Server
```bash
cd frontend
python3 app.py
```

### 3. Open the Newspaper
Visit **http://localhost:5050** in your browser.

### 4. (Optional) Generate Your First Articles
```bash
cd scripts
python3 daily_briefing.py          # Fetch VN news RSS
python3 article_scraper.py <URL>   # Scrape a specific article
python3 international_news.py --test  # Test international news
```

### 5. (Optional) Desktop Shortcut
Double-click `The-Agent-Times.desktop` to launch with one click.

---

## 📂 Project Structure

```
the-agent-times/
├── frontend/
│   ├── app.py                 # Flask server (port 5050)
│   ├── launch.sh              # Desktop launcher
│   ├── requirements.txt       # Python deps
│   ├── static/
│   │   └── style.css          # Clean news design (dark/light)
│   └── templates/
│       ├── base.html          # Layout: header, nav, footer
│       ├── index.html         # Homepage: hero + grid + archive
│       ├── article.html       # Article: content + sidebar
│       └── refresh.html       # Loading state
│
├── scripts/
│   ├── daily_briefing.py      # VN RSS Collector (9 feeds)
│   ├── article_scraper.py     # Universal article scraper
│   ├── international_news.py  # 10-country RSS + translate
│   ├── tech_news.py           # Tech RSS (VN + global)
│   ├── github_radar.py        # GitHub trending repos
│   ├── github_article_writer.py # Repo → article converter
│   ├── fnb_market_report.py   # F&B market analysis
│   ├── website_cloner.py      # Clone any site's design tokens
│   ├── run_and_save.py        # Report → article JSON
│   ├── legal_tax_guide.py     # VN business legal guide
│   └── autoreport_*.sh        # Shell pipeline wrappers
│
├── skills/                    # AI Agent Skills (for Hermes/Claude)
│   ├── design/design-master/  # Design-Craft + Laws of UX
│   ├── software-development/  # stealth-cloner, website-cloner
│   └── business/              # news-web-design, regulations
│
├── data/reports/              ← Your articles go here (JSON)
├── .gitignore
└── README.md
```

---

## ⚙️ Configuration

### Adding RSS Feeds
Edit any script's `FEEDS` dict at the top of the file:
```python
FEEDS = {
    "my-feed": {
        "name": "My Feed Name",
        "url": "https://example.com/rss",
        "category": "economic",
        "tags": ["my-tag", "tin-tức"],
    },
}
```

### Adding Categories
1. Edit `frontend/app.py` → `CATEGORY_MAP` dict
2. Edit `frontend/templates/base.html` → nav section
3. Add a scraper script that produces articles with your new category

### Changing Theme Colors
Edit `frontend/static/style.css` → `:root` CSS variables:
```css
:root {
  --accent: #032435;       /* Your brand color */
  --font-heading: '...';   /* Your heading font */
  --max-width: 1040px;     /* Layout width */
}
```

---

## 🧠 How It Works

### Data Pipeline
```
RSS Feeds → daily_briefing.py → Extract URLs → article_scraper.py → Clean HTML → Article JSON → Frontend
```

### Article Format
Each article is a JSON file in `data/reports/`:
```json
{
  "id": "article_2026-07-03_hash123",
  "title": "Vietnamese Title",
  "date": "2026-07-03",
  "category": "economic",
  "content_html": "<p>Full article content...</p>",
  "lead_image": "https://example.com/image.jpg",
  "tags": ["kinh-tế", "thế-giới"],
  "source_url": "https://source.com/article"
}
```

The Flask server reads these JSON files and renders them as a beautiful newspaper.

### Cronjobs (for automation)
```bash
07:00 — International News (10 countries)
08:00 — Daily Briefing + Scrape
08:30 — AI News Writer
09:00 — GitHub Radar (≥100⭐)
10:00 — F&B Reports
```

On Hermes Agent, use `cronjob action=create` to schedule these.

---

## 🎨 Design Principles

This project uses [Design-Craft](https://github.com/FasalZein/design-craft) and [Laws of UX](https://github.com/FasalZein/laws-of-ux):

- **3-layer color tokens**: Primitives → Semantic → Component
- **4px spacing grid**: Visual rhythm through proximity (Gestalt)
- **5-level typography**: Display 48px → Micro 11px
- **Animation**: Only `transform` + `opacity`, 100-800ms timing
- **Anti-slop**: No gradients, no glassmorphism, no hero metrics
- **Hick's Law**: ≤7 nav items
- **Fitts's Law**: 44px+ touch targets
- **Peak-End Rule**: Invest in peak moment + ending
- **prefers-reduced-motion**: Full accessibility support
- **Dark mode**: Semantic token swap (navy #0d1929)

---

## 🤝 Contributing

1. Fork the repo
2. Add your RSS feeds or improve the design
3. Submit a PR with clear description of changes

Ideas for contributions:
- More RSS feeds (sports, entertainment, science)
- Better translation (OpenAI/Claude API instead of googletrans)
- Mobile app frontend
- Email newsletter generation
- Sentiment analysis / topic clustering
- More design themes (color schemes)

---

## 📜 License

MIT — Free for personal and commercial use.

## 🙏 Credits

- [Design-Craft](https://github.com/FasalZein/design-craft) by FasalZein — Universal design principles
- [Laws of UX](https://github.com/FasalZein/laws-of-ux) by FasalZein — UX psychology
- [AI Website Cloner Template](https://github.com/JCodesMore/ai-website-cloner-template) — Website cloning approach
- [CloakBrowser](https://cloakhq.com/) — Stealth browser for tough sites
- [Hermes Agent](https://hermes-agent.nousresearch.com) — AI agent runtime
