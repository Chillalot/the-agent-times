# TLDR-Style 1-Column Digest — CSS + Flask Patterns (v8, current)

> Generated from: Session 2026-07-03 — Rewriting templates (dep.com.vn v7 → TLDR v8)
> Source artifact: `~/.hermes/profiles/meow/frontend/static/style.css` (~650 lines)
> Source Flask: `~/.hermes/profiles/meow/frontend/app.py`

## Design Decisions v8

| Dimension | dep.com.vn (v7, previous) | TLDR Digest (v8, current) |
|-----------|---------------------------|---------------------------|
| Container | 1040px variable | 720px fixed narrow |
| Grid | Multi-column (2-4 cols) | 1 column list |
| Background | `#f0f0f0` (base gray) | `#ffffff` (white) |
| Font | Be Vietnam Pro (serif + sans) | Inter (sans-serif only) |
| Category accent | 2px border-left on cards | Colored pill badge + border-bottom on section header |
| Card images | 130px thumbnail, 1:1 ratio | Hero only (conditional on `lead_image` existence) |
| Card hover | Image scale(1.05) | Background color change (subtle) |
| Header | `position: relative` | `position: sticky; top: 0` |
| Border radius | 0px (flat) | 6-8px (soft) |
| Animation | GSAP timeline per section | GSAP stagger on `.tldr-main > *` (simpler) |
| Category colors | Single `--accent` var | Inline `--badge-bg`/`--badge-text` via Flask context |
| CSS size | ~1678 lines | ~650 lines |
| Dark mode | Navy (#0d1929) | Deep navy (#0d1929) |

## Architecture: Flask-Level Category Colors

The key difference from v7: **category colors live in the Flask `CATEGORY_COLORS` dict**, not in CSS variables. This avoids per-category CSS classes and keeps the badge styling uniform.

```python
# app.py — canonical source for all 7 categories
CATEGORY_COLORS = {
    "daily-briefing": {"label": "Kinh tế", "bg": "#dbeafe", "text": "#1e40af", "border": "#2563eb"},
    "github":          {"label": "Công nghệ", "bg": "#ede9fe", "text": "#5b21b6", "border": "#7c3aed"},
    "fnb":             {"label": "F&B",       "bg": "#ffedd5", "text": "#9a3412", "border": "#ea580c"},
    "legal":           {"label": "Pháp lý",   "bg": "#fee2e2", "text": "#991b1b", "border": "#dc2626"},
    "affiliate":       {"label": "Affiliate", "bg": "#d1fae5", "text": "#065f46", "border": "#059669"},
    "economic":        {"label": "Phân tích", "bg": "#e0e7ff", "text": "#3730a3", "border": "#6366f1"},
    "market":          {"label": "Thị trường","bg": "#cffafe", "text": "#155e75", "border": "#0891b2"},
}
```

Passed to all templates via `get_common_context()`:
```python
context = { ..., "category_colors": CATEGORY_COLORS, ... }
```

And in the article route explicitly:
```python
return render_template("article.html", ..., category_colors=ctx["category_colors"])
```

## CSS Token Architecture

### Light mode

```css
:root, [data-theme="light"] {
  --accent: #2563eb;
  --contrast: #1a1a2e;
  --contrast-2: #4b5563;
  --base: #ffffff;
  --base-2: #f9fafb;
  --base-3: #f3f4f6;
  --border: #e5e7eb;
  --border-light: #f0f0f0;
  --text-primary: #1a1a2e;
  --text-secondary: #6b7280;
  --text-muted: #9ca3af;
  --card-bg: #ffffff;
  --card-hover-bg: #f9fafb;
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --content-max: 720px;
  --radius: 8px;
  --radius-sm: 6px;
}
```

### Dark mode

```css
[data-theme="dark"] {
  --accent: #60a5fa;
  --contrast: #e8e8f0;
  --contrast-2: #9898b8;
  --base: #0d1929;
  --base-2: #111d2e;
  --base-3: #182538;
  --border: #2a3a4a;
  --border-light: #1e2d3d;
  --text-primary: #e8e8f0;
  --text-secondary: #9898b8;
  --text-muted: #6868a0;
  --card-bg: #111d2e;
  --card-hover-bg: #182538;
}
```

### Typography scale

```css
--text-xs: 12px;    /* Meta, badges */
--text-sm: 14px;    /* Captions, excerpts */
--text-base: 16px;  /* Body */
--text-lg: 18px;    /* Large body */
--text-xl: 20px;    /* Sub-headings */
--text-2xl: 24px;   /* Section headings */
--text-3xl: 30px;   /* Article headline */
```

## Component Class System

### `.tldr-badge` — shared pill badge

Single class, colors via inline `style` from Flask context:

```css
.tldr-badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 20px;
  font-size: var(--text-xs);
  font-weight: 600;
  background: var(--badge-bg, #e5e7eb);
  color: var(--badge-text, #374151);
  white-space: nowrap;
}
```

Usage: `<span class="tldr-badge" style="--badge-bg:#dbeafe; --badge-text:#1e40af;">📰 Kinh tế</span>`

### `.tldr-section__header` — category section divider

Bottom border colored per category via `--section-color`:

```css
.tldr-section__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 10px;
  margin-bottom: 16px;
  border-bottom: 2px solid var(--section-color, var(--border));
}
```

### `.tldr-card` — article card in category list

```css
.tldr-card {
  padding: 16px 0;
  border-bottom: 1px solid var(--border-light);
  transition: background 0.15s ease;
}
.tldr-card:last-child {
  border-bottom: none;
}
.tldr-card:hover {
  background: var(--card-hover-bg);
  margin: 0 -12px;
  padding: 16px 12px;
  border-radius: var(--radius-sm);
}
```

Hover: background change + negative margin to extend beyond the container content area, creating a visual highlight without affecting layout flow.

### `.tldr-featured` — hero card (conditional on lead_image)

Shown only when `articles[0].get('lead_image')` exists. Hidden entirely otherwise.

```css
.tldr-featured {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  margin-bottom: 32px;
}
.tldr-featured:hover { box-shadow: var(--shadow-md); }

.tldr-featured__image {
  width: 100%;
  max-height: 360px;
  object-fit: cover;
  transition: transform 0.4s ease;
}
.tldr-featured:hover .tldr-featured__image { transform: scale(1.02); }

.tldr-featured__title {
  font-size: 22px;
  font-weight: 700;
  line-height: 1.35;
}
```

### `.tldr-article` — single article page

```css
.tldr-article__headline {
  font-size: 30px;
  font-weight: 700;
  line-height: 1.3;
  letter-spacing: -0.3px;
}
.tldr-article__body {
  font-size: 18px;
  line-height: 1.75;
}
```

Article body handles all rich HTML from scrapers: `<h2>`, `<h3>`, `<p>`, `<ul>/<ol>`, `<figure>`/`<figcaption>`, `<blockquote>`, `<pre>`/`<code>`.

### Empty state

```css
.tldr-empty {
  text-align: center;
  padding: 60px 20px;
}
```

### Date archive

```css
.tldr-archive__item {
  display: inline-block;
  padding: 4px 12px;
  border-radius: var(--radius-sm);
  font-size: var(--text-xs);
  border: 1px solid var(--border);
}
.tldr-archive__item.is-active {
  color: white;
  background: var(--accent);
  border-color: var(--accent);
}
```

## GSAP Animation (v8)

Simplified from v7 — single stagger on all main content:

```javascript
gsap.from('.tldr-main > *', {
  opacity: 0, y: 20,
  duration: 0.5, stagger: 0.08,
  delay: 0.25,
  ease: 'power2.out'
});
```

Header/nav/date-nav each get individual fade-ins with slight delays and overlaps:

```javascript
gsap.from('.tldr-header',  { opacity: 0, y: -12, duration: 0.35, ease: 'power2.out' });
gsap.from('.tldr-nav',     { opacity: 0, duration: 0.3, delay: 0.1 });
gsap.from('.tldr-date-nav',{ opacity: 0, y: -8, duration: 0.3, delay: 0.15 });
```

Reduced motion check uses:
```javascript
if (typeof gsap !== 'undefined' && !document.documentElement.classList.contains('reduce-motion'))
```

## Responsive Breakpoints

```css
/* Tablet (max-width: 768px) */
--container-gutter: 16px;
.tldr-featured__title { font-size: 18px; }
.tldr-article__headline { font-size: 24px; }
.tldr-article__body { font-size: 16px; }
.tldr-nav__item { padding: 8px 12px; font-size: var(--text-xs); }

/* Mobile (max-width: 480px) */
.tldr-main { padding: 16px gap 32px; }
.tldr-header__actions { width: 100%; justify-content: flex-end; padding-top: 8px; border-top: 1px solid var(--border-light); }
.tldr-featured__image-wrapper { max-height: 220px; }
.tldr-article__headline { font-size: 22px; }
```

## Jinja2 Template Flow (index.html)

```
articles? ──NO──→ .tldr-empty (📭 + "Chưa có báo cáo")
  │
 YES
  │
  ├── .tldr-page-header (title + subtitle)
  │
  ├── Set featured = articles[0], remaining = articles[1:]
  │
  ├── has lead_image? ──YES──→ .tldr-featured (image + badge + title + excerpt + meta)
  │
  └── remaining? ──YES──→ [for group in remaining|groupby('category')]
       │
       ├── .tldr-section__header (colored border + badge)
       └── .tldr-card (for each article: title + excerpt + meta)
```

## Pitfalls (from session)

### 1. groupby only on `remaining`, not all articles

```jinja2
{% set remaining = articles[1:] %}
{% for group in remaining|groupby('category') %}
```

`articles[0]` is the featured. It should NOT appear in category sections. If no `lead_image`, the featured article is simply the first one shown in its category section — no hero appears, no content is lost.

### 2. Category not in CATEGORY_COLORS → gray fallback

```jinja2
{% set cc = category_colors.get(slug, {}) %}
{# Then use cc.get('bg','#e5e7eb'), cc.get('text','#374151'), cc.get('border','#6b7280') #}
```

### 3. Both bg and text must be set for each category

Dark mode inherits the same inline styles — there is no CSS-level dark mode override for badges. The Flask dict's `bg`/`text` properties are the only source of badge colors. This means the colors must work in BOTH light and dark modes. Current colors are light-mode optimized (pale pastel bg + dark text) which also looks good on dark backgrounds.

### 4. Sticky header requires no overflow:hidden on parent

`.tldr-header` has `position: sticky; top: 0; z-index: 100`. This only works if no parent element has `overflow: hidden`. The body and main containers must not clip overflow.

### 5. CSS bundle reduced from 1678 → 650 lines

When switching from dep.com.vn (v7) to TLDR (v8), the CSS shrank by ~60%. This is because:
- No Bootstrap compat layer removed (`.d-flex`, `.w-100`, `.mt-2` etc.)
- Single container instead of multi-column grid
- No per-category CSS classes → inline styles handle colors
- Simplified hover effects (background only, no transform/shadow)
- No separate components for image-box, post-card variants, pagination etc.
