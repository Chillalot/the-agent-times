# dep.com.vn Component Patterns — Exact Layout (v6)

> Live-fetched 2026-07-03. WordPress + gp-dep child theme + Elementor + Bootstrap 5.
> Font: Be Vietnam Pro (headings), Arial/Helvetica (body). Icons: Tabler Icons (inline SVGs).
> Full 992-line pixel-level analysis at `~/.hermes/profiles/meow/dep-exact-layout.md`

---

## 1. Image Box Hero — Full-Width with Gradient Overlay

The signature hero component. Full-width image with dark gradient overlay + centered white semi-transparent content box.

### HTML Structure

```html
<div class="image-box">
  <div class="image-box__image-wrapper">
    <!-- Full-width background image OR fallback emoji -->
    <div class="image-box__image" style="background-image:url('...');"></div>
    <div class="image-box__image-overlay"></div>
    <!-- OR fallback:
    <div class="image-box__image image-box__image--fallback">
      <span class="image-box__emoji">📰</span>
    </div> -->
  </div>

  <div class="image-box__content">
    <div class="image-box__content-wrapper">
      <div class="image-box__content-inner">
        <span class="post-card__category-link">{{ category_name }}</span>
        <h2 class="image-box__title">
          <a href="...">{{ title }}</a>
        </h2>
        <p class="image-box__excerpt">{{ excerpt }}</p>
        <div class="image-box__meta">{{ date }} <a href="...">Đọc tiếp →</a></div>
      </div>
    </div>
  </div>

  <!-- Entire card clickable overlay link -->
  <a class="image-box__overlay-link" href="..." title="..."></a>
</div>
```

### CSS

| Element | Key Properties |
|---------|----------------|
| `.image-box` | `position: relative; overflow: hidden; margin-bottom: 24px` |
| `.image-box__image` | `width: 100%; height: 380px; background-size: cover; background-position: center` |
| `.image-box__image:after` | Gradient: `linear-gradient(180deg, rgba(85,85,85,0), #000)` — 25% height from bottom |
| `.image-box__image-overlay` | `position: absolute; bottom: 0; height: 40%;` gradient overlay, `pointer-events: none` |
| `.image-box__content` | `position: absolute; bottom: 1.5em; left: 0; width: 100%; z-index: 3; pointer-events: none` |
| `.image-box__content-inner` | `max-width: 700px; margin: 0 auto; background: hsla(0,0%,100%,0.88); box-shadow: 0 3px 8px rgba(0,0,0,.24); padding: 1rem 1.5rem; text-align: center` |
| `.image-box__title` | `font-family: var(--font-heading); font-size: 20px → 26px (768px+); font-weight: 700; text-transform: uppercase; line-height: 2` |
| `.image-box__overlay-link` | `position: absolute; inset: 0; z-index: 4` |

### Mobile (@media max-width: 767px)

- `.image-box`: `min-height: 25vh; display: flex; align-items: flex-end`
- `.image-box__content`: `position: relative; bottom: 0; padding: 0 1em 1em`
- `.image-box__content-inner`: `background: none; box-shadow: none; padding: 0; text-align: left`
- `.image-box__image`: `position: absolute; inset: 0; width: 100%; height: 100%`
- `.image-box__image:after`: `height: 50%`
- `.image-box__title`: `color: var(--bs-white); font-size: 18px; line-height: 1.35`

### Dark Theme

```css
[data-theme="dark"] .image-box__content-inner {
  background: rgba(13,25,41,0.88);
}
[data-theme="dark"] .image-box__title a { color: var(--contrast); }
```

---

## 2. Post Card — Horizontal with 130px Thumbnail

When `lead_image` exists, the card switches to a horizontal layout with a 130px square thumbnail on the left.

### HTML Structure

```html
<!-- Standard (no image) / Grid (stacked) -->
<article class="post-card">
  <a class="post-card__image-link" href="...">
    <div class="post-card__image post-card__image--fallback">
      <span class="post-card__image-emoji">📄</span>
    </div>
  </a>
  <div class="post-card__content">...</div>
</article>

<!-- With lead_image → 130px thumbnail horizontal -->
<article class="post-card post-card--has-image">
  <a class="post-card__image-link" href="...">
    <div class="post-card__image">
      <img src="{{ lead_image }}" alt="..." loading="lazy">
    </div>
  </a>
  <div class="post-card__content">
    <p class="post-card__meta">
      <span class="post-card__category">
        <a class="post-card__category-link" href="...">Category</a>
      </span>
      <span class="post-card__date">03/07/2026</span>
    </p>
    <h3 class="post-card__title">
      <a class="post-card__title-link" href="...">Title</a>
    </h3>
  </div>
</article>
```

### CSS

```css
/* Base: stacked layout */
.post-card {
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 16px 0;
}
.post-card + .post-card { border-top: 1px solid rgba(0,0,0,.15); }
@media (min-width: 768px) {
  .post-card { padding: 16px; }
  .post-card + .post-card { border-top: none; }
}

/* 130px thumbnail variant */
.post-card--has-image {
  flex-direction: row;
  gap: 16px;
}
.post-card--has-image .post-card__image-link {
  width: 130px;
  flex-shrink: 0;
  margin-bottom: 0;
}
.post-card--has-image .post-card__content {
  flex: 1;
  min-width: 0;
}

/* Image */
.post-card__image {
  position: relative;
  aspect-ratio: 1 / 1;
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.post-card__image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: all .4s ease;
}
.post-card:hover .post-card__image img { transform: scale(1.05); }
```

### Responsive

```css
@media (max-width: 767px) {
  .post-card--has-image { gap: 10px; }
  .post-card--has-image .post-card__image-link { width: 100px; }
}
@media (min-width: 768px) and (max-width: 959px) {
  .post-card--has-image .post-card__image-link { width: 120px; }
}
```

---

## 3. Category Badge — Border-Left 2px Accent

dep.com.vn's signature: a 2px solid left border on the category name — acts as a visual accent/divider.

```css
.post-card__category-link {
  display: inline-block;
  border-left: 2px solid var(--accent);   /* #032435 light, #4a9eff dark */
  padding-left: 10px;
  font-size: 0.75rem;
  font-weight: var(--font-semibold);
  text-transform: uppercase;
  text-decoration: none;
  line-height: 1;
  color: var(--contrast);
  transition: color .4s ease;
}
.post-card__category-link:hover { color: var(--bs-secondary); }
```

Used in:
- Hero content-inner (`.image-box__content-inner .post-card__category-link`)
- Post grid cards (`.post-card__category-link`)
- Article page section badge

```html
<!-- In hero overlay -->
<span class="post-card__category-link" style="border-left-color:var(--accent);">
  {{ featured.category_name }}
</span>

<!-- In article page section badge -->
<span class="post-card__category-link"
      style="border-left-color:var(--accent); display:inline-block; padding-left:10px;
             font-size:11px; text-transform:uppercase; letter-spacing:2px; font-weight:700;">
  {{ article.category_name }}
</span>
```

---

## 4. Subnav — Horizontal Scroll (Category Nav)

Uppercase category links in a horizontal scrollable strip with dep.com.vn exact values.

### CSS

```css
.subnav--archive .subnav__inner,
.subnav--highlight .subnav__inner {
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}

.subnav__inner {
  max-width: var(--container-max, 1040px);
  margin: 0 auto;
  padding: 0 var(--container-gutter, 20px);
}

.subnav__list {
  display: flex;
  flex-wrap: nowrap;
  align-items: center;
  justify-content: space-between;
  list-style: none;
  margin: 0;
  padding: 0.5em 0;
  overflow-x: auto;
  white-space: nowrap;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;           /* Firefox — hide scrollbar */
}
.subnav__list::-webkit-scrollbar { display: none; } /* Chrome/Safari — hide scrollbar */

.subnav__item {
  flex-shrink: 0;
  margin-right: 1em;
  margin-bottom: 0.25em;
}
.subnav__item:last-child { margin-right: 0; }
.subnav__item.is-active .subnav__link {
  font-weight: var(--font-semibold, 600);
  color: var(--bs-secondary, #337ab7);
}

.subnav__link {
  display: block;
  font-family: var(--font-heading);   /* Be Vietnam Pro */
  font-size: 0.85rem;                  /* 13.6px */
  font-weight: var(--font-normal, 400);
  text-transform: uppercase;
  text-decoration: none;
  padding: 0.5em 0;
  color: var(--contrast, #222);
  white-space: nowrap;
  transition: color .4s ease;
}
.subnav__link:hover { color: var(--bs-secondary, #337ab7); }
```

---

## 5. Design Tokens — dep.com.vn Exact

### Key Colors

| Token | Light | Dark |
|-------|-------|------|
| `--accent` | `#032435` (deep navy) | `#4a9eff` (bright blue) |
| `--bs-secondary` | `#337ab7` | `#6aafff` |
| `--bs-gray-700` | `#495057` | `#6a6a8a` |
| `--bs-gray-300` | `#dee2e6` | `#2a3a4a` |
| `--contrast` | `#222222` | `#e8e8f0` |
| `--contrast-2` | `#575760` | `#9898b8` |
| `--contrast-3` | `#b2b2be` | `#6868a0` |
| `--base` | `#f0f0f0` | `#143149` |
| `--base-2` | `#f7f8f9` | `#0b1116` |
| `--base-3` | `#ffffff` | `#0d1929` |
| `--bs-light` | `#f8f9fa` | `#152029` |

### Container

```css
--container-max: 1040px;
--container-max-xxl: 1180px;
--container-gutter: 20px;
```

### Shadows

```css
--shadow-hero: 0 3px 8px rgba(0,0,0,.24);
--shadow-search: 0 10px 15px -3px rgba(0,0,0,.1), 0 4px 6px -2px rgba(0,0,0,.05);
```

### Typography

```css
--font-heading: 'BeVietnamPro', Arial, Helvetica, sans-serif;
--font-default: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, …;
```

### Hover Summary

All interactive elements use `transition: color .4s ease` with hover color `var(--bs-secondary)` (#337ab7 light / #6aafff dark):
- Category links, post card titles, subnav links, header nav items, search buttons

---

## 6. Responsive Breakpoints

| Min-width | Grid | Hero height | Thumbnail width |
|-----------|------|-------------|-----------------|
| < 768px | 1 col | 250px | 100px |
| 768px | 2 cols | 320px | 120px |
| 960px | 2 cols | 360px | 130px |
| 1280px | 4 cols | 400px | 130px |

---

## 7. CSS Version Cache Busting

Always version static CSS to avoid stale caches:

```html
<!-- base.html -->
<link rel="stylesheet" href="/static/style.css?v=6">
```

When CSS changes, bump the version number. Convention: `v=1`, `v=2`, … `v=6` (latest).

---

## 8. Post Grid Breakpoint Columns

```css
/* dep.com.vn: 1 → 2 → 4 columns */
.post-grid__row {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--grid-gutter, 10px);
}
@media (min-width: 768px) { .post-grid__row { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 1280px) { .post-grid__row { grid-template-columns: repeat(4, 1fr); } }
```
