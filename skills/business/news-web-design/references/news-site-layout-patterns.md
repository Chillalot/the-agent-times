# News Site Layout Patterns — Live Research

> Research conducted July 2026 via live browser inspection (JS console, computed styles, stylesheet enumeration) of NYT, The Guardian, and VnExpress. BBC was unreachable from the research network; its patterns are from established knowledge.

---

## 1. Article Cards

### 1.1 New York Times (`.story-wrapper`)

```css
.story-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0;
  font-family: "Times New Roman", serif;
  font-size: 16px;
  line-height: 16px;
}
```

**Card anatomy:**
- **Thumbnail** — `figure` element, block display, responsive width
- **Headline** — `<h3>` or block-level link, `nyt-franklin` sans-serif, `13px` / `18px` line-height
- **Summary** — `<p>` element, `font-size: 13px`, `line-height: 18px`, `font-weight: 500`, color `#363636`
- **Metadata** — `font-family: nyt-franklin`, `font-size: 11px`, `color: #5a5a5a`, margins `0 0 16px`
- **Kicker/label** — uppercase section name, `11px`, `font-weight: 700`, letter-spaced

**Key NYT approach:**
- Cards in a section are wrapped in a flex row (`display: flex; flex-direction: row`), not CSS Grid
- `section` has `max-width: 1605px` (very wide); header has `max-width: 1200px`
- `section` elements have `padding: 4px 15px 8px` — very tight spacing
- Story links use `color: rgb(0, 0, 0)` with `background-color: rgb(255, 255, 255)`, class `css-*` hash

### 1.2 The Guardian (`.fc-item`, `.dcr-bpr716`)

```css
/* Card container */
.dcr-bpr716 { position: relative; }
@media (min-width: 740px) {
  .dcr-bpr716 { width: 280px; flex-direction: row; }
}

/* Card inner */
.dcr-1xggi2v {
  display: flex;
  flex-direction: column;
  gap: 4px;
  justify-content: space-between;
}

/* Card headline */
.dcr-10xs001 {
  font-family: "GH Guardian Headline", "Guardian Egyptian Web", Georgia, serif;
  font-size: 1.0625rem;  /* 17px */
  line-height: 1.15;
  font-weight: 500;
}
@media (min-width: 375px) and (max-width: 479.9px) {
  .dcr-1xggi2v .headline-text { font-size: 1rem; }
}

/* Card overlay link — entire card clickable */
.dcr-idxb0f {
  position: absolute;
  inset: 0;
  background-color: transparent;
  z-index: 2;
}
.dcr-idxb0f:focus { outline: 0; }
html:not(.src-focus-disabled) .dcr-idxb0f:focus {
  box-shadow: rgb(0, 119, 182) 0 0 0 3px;
}

/* Card hover */
.dcr-bpr716:hover .media-overlay {
  position: absolute; bottom: 0; right: 0;
  height: 100%; width: 100%;
  background-color: var(--card-background-hover);
}

/* Timestamp */
time {
  font-family: GuardianTextSans, "Guardian Text Sans Web", Helvetica, Arial, sans-serif;
  font-size: 12px;
  font-weight: 700;
  line-height: 15.6px;
  color: #707070;
}
```

**Card anatomy:**
- **Kicker** — bold uppercase category label (e.g., "Ukraine", "Iran") as `StaticText` prefix
- **Headline** — GH Guardian Headline at 17px (1.0625rem), 1.15 line-height, weight 500
- **Standfirst** — block text below headline for the excerpt
- **Image** — `figure` element in `dcr-1oe1tgl` (98px wide, flex-end aligned) or full-width for leads
- **Footer** — `sectionfooter` with `time` element
- **Trail text** — summary text below headline

### 1.3 VnExpress (`.item-news`, `.title-news`)

```css
.item-news {
  width: 100%;
  float: left;
  padding-bottom: 15px;
  margin-bottom: 15px;
  border-bottom: 1px solid #e5e5e5;
}

.title-news {
  font-family: Merriweather, serif;
  font-size: 20px;
  font-weight: 700;
  line-height: 32px;
  color: #222;
}

h3 {  /* homepage hero */
  font-family: Merriweather, serif;
  font-size: 20px;
  font-weight: 700;
  line-height: 32px;
  color: #222;
  margin: 0 0 10px;
}

.description {
  font-family: arial, sans-serif;
  font-size: 14px;
  line-height: 19.6px;
  color: #4f4f4f;
}

.meta-news {
  font-family: Arial, sans-serif;
  font-size: 14px;
  line-height: 19.6px;
  color: #757575;
}

.thumb-art {
  width: 520px;
  margin-right: 20px;
}

.thumb {
  background: #f4f4f4;
  display: block;
  padding-bottom: 312px;  /* fixed aspect ratio for hero */
}
```

**VnExpress card approach:**
- Uses **floats** (not flexbox/grid): `.item-news { width: 100%; float: left; }`
- Two-column layout: `col-left` (780px) + `col-right` (320px)
- Hero story: `thumb-art` at `520px` + headline in `Merriweather` at `20px/32px`
- Excerpt: `14px` Arial, color `#4f4f4f`, `line-height: 19.6px`
- Metadata: `meta-news` with category link + comment count + timestamp

### 1.4 BBC

```css
.bbc-card {
  display: block;
  border-top: 1px solid #e0e0e0;
  padding: 16px 0;
}
.bbc-card__headline {
  font-family: 'BBC Reith', 'Helvetica', 'Arial', sans-serif;
  font-size: 20px;
  font-weight: 700;
  line-height: 1.2;
  color: #1a1a1a;
}
.bbc-card__summary {
  font-family: 'BBC Reith', 'Helvetica', 'Arial', sans-serif;
  font-size: 14px;
  line-height: 1.35;
  color: #555;
}
```

---

## 2. Featured / Hero Sections

### 2.1 NYT — Lede Story

Lead story is the first `.story-wrapper` in the section — no special "hero" wrapper. NYT relies on **content hierarchy** (larger image, longer headline, more summary text).

### 2.2 Guardian — Front Container Grid

```css
.dcr-lypmm {
  display: grid;
  grid-auto-rows: auto;
  column-gap: 10px;
}

/* MOBILE: 4-column equal flex */
@media (max-width: 739px) {
  .dcr-lypmm {
    grid-template-columns: [viewport-start] 0px
      [content-start main-column-start] repeat(4, minmax(0px, 1fr))
      [content-end main-column-end] 0px [viewport-end];
  }
}
/* TABLET: 12 columns at 40px */
@media (min-width: 740px) {
  .dcr-lypmm {
    grid-template-columns: [viewport-start] minmax(0px, 1fr)
      [content-start main-column-start] repeat(12, 40px)
      [content-end main-column-end] minmax(0px, 1fr) [viewport-end];
  }
}
/* DESKTOP: 12 columns at 60px */
@media (min-width: 980px) {
  .dcr-lypmm {
    grid-template-columns: [viewport-start] minmax(0px, 1fr)
      [content-start main-column-start] repeat(12, 60px)
      [content-end main-column-end] minmax(0px, 1fr) [viewport-end];
  }
}
```

**Named grid lines:** `viewport-start/end` (gutters), `content-start/end` (inner area), `main-column-start/end` (main/span boundary), `title-start/end`, `hide-start/end`.

### 2.3 VnExpress — Top Story

```css
.article-topstory .thumb-art { width: 520px; }
@media (max-width: 1129px) {
  .article-topstory .thumb-art { width: 440px; }
}
@media (max-width: 979px) {
  .col-left-top { width: 100%; }
  .col-right-top { display: none; }
}
```

### 2.4 BBC Hero

Full-width with 16:9 image, headline `28px` desktop / `20px` mobile, sometimes text-overlaid on image with dark gradient. Secondary stories in `grid-template-columns: repeat(3, 1fr)`.

---

## 3. Guardian Grid System — Full Details

| Breakpoint | Grid Columns | Container Width |
|-----------|-------------|-----------------|
| < 740px | 4 cols, 10px gap | fluid (0px gutters) |
| 740–979px | 12 cols × 40px + 1fr gutters | 740px |
| 980–1139px | 12 cols × 60px + 1fr gutters | 980px |
| 1140–1299px | same grid | 1140px |
| ≥ 1300px | same grid | 1300px |

**Container widths:**
```css
@media (min-width: 740px)  { /* width: 740px */ }
@media (min-width: 980px)  { /* width: 980px */ }
@media (min-width: 1140px) { /* width: 1140px */ }
@media (min-width: 1300px) { /* width: 1300px */ }
```

**Content placement:**
```css
.article-card--full    { grid-column: content-start / content-end; }
.article-card--main    { grid-column: content-start / main-column-end; }
.article-card--sidebar { grid-column: main-column-end / content-end; }
```

---

## 4. VnExpress Layout — Full Details

### Category Page Layout
```css
.col-left { width: 780px; padding-right: 20px; }
.col-right { width: 320px; padding-left: 20px; }

@media (max-width: 979px) {
  .col-left { width: 100%; padding-right: 0; }
  .col-right { display: none; }
}
```

### Container
```css
.container {
  display: flex;
  flex-direction: row;
  margin: 0 71px;
  max-width: 1130px;
  width: 1130px;
  padding: 0 15px;
}
```

### VnExpress Breakpoints
| Breakpoint | What changes |
|-----------|-------------|
| < 600px | Cat menu: 50% width |
| < 768px | Left/right topic columns: 50%; hide weather; reduce hero padding |
| < 979px | Full-width col-left; hide sidebar; 33% cat menu |
| < 1025px | Tablet subnav: horizontal scroll |
| < 1129px | Hero thumb: 440px; 20% cat menu |
| 1129px+ | Full desktop: 1130px container |

---

## 5. Article Typography — Live CSS

### VnExpress
```css
h1 { font-family: Merriweather, serif; font-size: 32px; line-height: 48px; font-weight: 700; color: #222; margin: 20px 0 15px; }
article { font-family: arial, sans-serif; font-size: 18px; line-height: 28.8px; width: 680px; }
article p { font-size: 18px; line-height: 28.8px; margin: 0 0 15px; }
.description { font-family: arial, sans-serif; font-size: 18px; line-height: 28.8px; }
figure { max-width: 100%; margin: 0 0 15px; }
figcaption { font-family: arial, sans-serif; font-size: 18px; line-height: 28.8px; }
```

### Guardian (established)
```css
.article-headline { font-family: "GH Guardian Headline", "Guardian Egyptian Web", Georgia, serif; font-size: 2.25rem; line-height: 1.08; font-weight: 500; }
@media (max-width: 739px) { .article-headline { font-size: 1.75rem; line-height: 1.1; } }
.article-standfirst { font-family: GuardianTextSans, Helvetica, Arial, sans-serif; font-size: 1.125rem; line-height: 1.4; font-weight: 500; }
.article-body p { font-family: "Guardian Egyptian Web", Georgia, serif; font-size: 1.0625rem; line-height: 1.6; }
```

### Drop Caps
```css
/* Guardian */
.article-body p:first-child:first-letter {
  font-family: "GH Guardian Headline", Georgia, serif;
  float: left; font-size: 4.5rem; line-height: 0.8;
  margin-right: 6px; padding-top: 4px; font-weight: 700;
}

/* NYT */
.story-body p:first-child:first-letter {
  font-family: "Times New Roman", Georgia, serif;
  float: left; font-size: 85px; line-height: 0.7; font-weight: 700;
  padding: 5px 8px 0 0;
}
```

### Pull Quotes
```css
.pull-quote {
  font-family: Georgia, Times, serif;
  font-size: 28px; line-height: 1.3; font-style: italic;
  color: #333; margin: 30px 0;
  padding: 20px 0 20px 24px;
  border-left: 3px solid #c70000;
  max-width: 600px;
}
```

---

## 6. Dark Mode — Three Approaches

### 6.1 NYT — Class-Based Toggle

```html
<html class="nytapp-vi-homepage tpl-always-light">
```

Class-based switching on `<html>` element. `tpl-always-light` forces light mode. `tpl-dark` would activate dark variables. Server-side / JS-switched.

### 6.2 Guardian — CSS Custom Properties with `data-theme`

```css
:root, [data-theme="light"] { /* light vars */ }
[data-theme="dark"] { /* dark vars */ }

@media (prefers-color-scheme: dark) {
  [data-theme="auto"] { /* auto-follow vars */ }
}
```

CSS variables pattern: `--card-background`, `--headline-color`, `--border-color`, etc.

### 6.3 BBC — `prefers-color-scheme` Media Query

```css
:root { /* light defaults */ }
@media (prefers-color-scheme: dark) {
  :root { /* dark overrides */ }
}
```

### Recommended Three-Mode System
```css
:root { color-scheme: light; /* light vars */ }
@media (prefers-color-scheme: dark) { :root { color-scheme: dark; /* dark vars */ } }
[data-theme="dark"] { color-scheme: dark; /* dark vars */ }
[data-theme="light"] { color-scheme: light; /* light vars */ }

/* Toggle JS */
function toggleTheme() {
  const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
}
```

---

## 7. Font Stacks Comparison

| Site | Headline | Body | UI/Meta |
|------|----------|------|---------|
| NYT | `nyt-franklin, helvetica, arial, sans-serif` | `"Times New Roman", Georgia, serif` | `nyt-franklin, helvetica, arial, sans-serif` |
| Guardian | `"GH Guardian Headline", "Guardian Egyptian Web", Georgia, serif` | `"Guardian Egyptian Web", Georgia, serif` | `GuardianTextSans, "Helvetica Neue", Arial, sans-serif` |
| VnExpress | `Merriweather, serif` | `arial, sans-serif` | `Arial, sans-serif` |
| BBC | `"BBC Reith", "Helvetica", "Arial", sans-serif` | `"BBC Reith", "Helvetica", "Arial", sans-serif` | `"BBC Reith", "Helvetica", "Arial", sans-serif` |

---

## 8. Sidebar Widget Patterns

### Most Read (numbered)
```css
.most-read { counter-reset: most-read-counter; }
.most-read__item::before {
  content: counter(most-read-counter);
  font-family: "GH Guardian Headline", Georgia, serif;
  font-size: 28px; font-weight: 700; color: #c70000;
  float: left; width: 36px;
}
```

### Related Stories
```css
.related-stories__grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
@media (max-width: 480px) { .related-stories__grid { grid-template-columns: 1fr; } }
```

### Date Archive
```css
.date-archive__heading { font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
.date-archive__item { padding: 6px 0; border-bottom: 1px solid #eee; }
```

---

## 9. Key Differences Summary

| Feature | NYT | Guardian | VnExpress | BBC |
|---------|-----|----------|-----------|-----|
| Grid | Flex wrap | Named-line CSS Grid | Float + flex | CSS Grid (4→3→2→1) |
| Card technique | `.story-wrapper` flex column | `.dcr-bpr716` absolute overlay link | `.item-news` float left | Flex column + border-top |
| Typography | Serif body, sans-serif UI | Custom "Guardian Egyptian" headline | Merriweather + Arial | Custom "BBC Reith" |
| Breakpoints | Fluid + 1200px max | 740/980/1140/1300px | 979/768/600/1129px | 1008/672/480px |
| Dark mode | Class toggle (`.tpl-dark`) | CSS vars + `data-theme` attr | None | `prefers-color-scheme` |
| Focus style | N/A (paywall) | `box-shadow: 0 0 0 3px #0077b6` | None | Standard outline |
