# NYT Design System — Implementation Reference

> Thiết kế giao diện báo điện tử phong cách NYT.  
> Hệ thống thật chạy tại `http://localhost:5050`, source tại `~/.hermes/profiles/meow/frontend/`.

## 1. Color Palette

```css
:root {
  --bg: #ffffff;
  --bg-warm: #faf8f5;
  --text: #121212;
  --text-gray: #5a5a5a;
  --text-light: #8a8a8a;
  --border: #e2e2e2;
  --border-light: #f0f0f0;
  --accent: #b80000;        /* signature NYT red */
  --link: #567b99;          /* muted NYT blue */
  --font-serif: Georgia, 'Times New Roman', Times, serif;
  --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
  --max-width: 1200px;
  --content-width: 680px;
}
```

**Why NYT colors work:** High contrast (#121212 on #fff) for readability, red sparingly for hierarchy, warm #faf8f5 for date nav creates subtle section demarcation.

## 2. Component Patterns

### Utility Bar
- All-black background, 11px sans-serif, gray links
- Left: live date (JS-generated in `vi-VN` locale)
- Right: navigation links

### Newspaper Header
- Centered layout
- Name: 42px serif, bold, -1px letter-spacing
- Decorative line: 60px × 1px, centered
- Subtitle: 11px uppercase, 3px letter-spacing

### Section Nav
- 2px solid bottom border (signature NYT style)
- Items: 12px uppercase, 1.2px letter-spacing
- Separators: 1px right border, lighter than text
- Active state: accent color
- Overflow-x: auto for mobile

### Date Navigation
- Background: warm paper (#faf8f5)
- Three-part: prev button | current date | next button + today link
- Buttons: bordered, 12px sans-serif
- Current date: 18px serif, bold
- Native `<input type="date">` with `onchange` redirect

### Article Grid (Today's Paper)
- 3-column CSS grid, 24px gap
- Featured article: full-width, 2-column inner (text + visual emoji area)
- Cards: bottom border separator, no box shadow (authentic newspaper feel)

### Article Detail
- Max-width: 680px (optimized reading width)
- Headline: 40px serif, bold, -0.5px letter-spacing
- Drop cap: `p:first-child::first-letter` — 56px, float left, 10px margin-right
- Body: 17px serif, 1.85 line-height
- Sources: small uppercase heading, sans-serif URLs with em dash prefix

## 3. Grid Implementation

```css
.news-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.news-featured {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: 1fr 1fr;
}

.news-grid-col {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
```

## 4. Responsive Breakpoints

| Breakpoint | Grid | Headline | Notes |
|---|---|---|---|
| >900px | 3 columns | 40px | Desktop |
| 600-900px | 2 columns | 30px | Tablet |
| <600px | 1 column | 24px | Mobile, wrap date nav |

## 5. GSAP Animation Patterns

```javascript
// Page load: stagger cards in
gsap.from('.article-card', {
  opacity: 0, y: 30, duration: 0.6,
  stagger: 0.1, ease: 'power2.out',
  scrollTrigger: { trigger: '.news-grid', start: 'top 85%' }
});

// Featured card entrance
gsap.from('.featured-card', {
  opacity: 0, y: 20, duration: 0.8, ease: 'power2.out'
});

// Article detail entrance
gsap.from('.article-headline', {
  opacity: 0, y: 20, duration: 0.8, ease: 'power2.out'
});
gsap.from('.article-content', {
  opacity: 0, y: 10, duration: 0.6, delay: 0.3
});
```

**Why GSAP over CSS animations:** GSAP's `stagger` + `ScrollTrigger` gives per-item control that CSS `animation-delay` can't match. The `power2.out` easing mimics natural deceleration.

## 6. Ponytail Lessons Applied

| Over-engineered approach | Ponytail approach |
|--------------------------|-------------------|
| React + Next.js SPA | Flask + Jinja2 templates |
| Moment.js/Luxon for dates | Python `datetime.strftime` |
| jQuery UI Datepicker | `<input type="date">` |
| Bootstrap/Tailwind | Custom CSS (small, focused) |
| Axios fetch | `<a>` links + `onchange` redirect |

## 7. Flask Route Architecture

```python
@app.route("/")                          # Homepage
@app.route("/date/<date_str>")           # Reports by date
@app.route("/category/<category>")       # Filter by section
@app.route("/article/<article_id>")      # Single article
@app.route("/search")                    # Full-text search
@app.route("/refresh")                   # Regenerate reports
```
