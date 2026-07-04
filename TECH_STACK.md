# Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend Language | Python 3.11+ |
| Web Framework | Flask 3.0+ |
| Template Engine | Jinja2 |
| Article Extraction | readability-lxml |
| HTML Parsing | BeautifulSoup 4 |
| RSS Parsing | xml.etree.ElementTree |
| Translation | googletrans |
| Frontend Animations | GSAP 3.12+ |
| Frontend Runtime | Vanilla JavaScript |
| CSS | Custom properties, no framework |
| Article Image Extraction | 6-step fallback chain (OG → Twitter → article → figure) |
| AI Agent Runtime | Hermes Agent |
| Screenshot / Demo | Playwright |
| Video Conversion | ffmpeg |
| Image Optimization | Pillow, ImageMagick |

## Why These Choices

**Flask over FastAPI** — Simpler for a file-based reader. No async needed for JSON reads.

**readability-lxml** — The same algorithm Firefox uses for reader mode. Proven, stable, no AI dependency.

**googletrans** — Free, no API key. Sufficient for personal use. For production, swap in a paid translation API.

**GSAP** — Professional-grade animation library. Handles scroll-triggered entrances, timeline sequencing, and respects `prefers-reduced-motion` without additional code.

**JSON storage** — Zero configuration. Portable across systems. Easy to inspect, debug, and back up with rsync.
