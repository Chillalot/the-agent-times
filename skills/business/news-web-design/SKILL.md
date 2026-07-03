---
name: news-web-design
description: "Thiết kế giao diện báo/tạp chí điện tử + newsletter/news digest — NYT, Guardian, BBC, VnExpress, TLDR, Axios, The Hustle. Flask + CSS Grid + GSAP. Responsive grids, dark mode, Vietnamese typography."
version: 3.2.0
tags: [news, design, NYT, Guardian, VnExpress, BBC, flask, css, gsap, frontend, newspaper, responsive, dark-mode, vietnamese, newsletter, digest, tldr, axios, the-hustle]
---

# News Web Design — Multi-Site Pattern Library

## CRITICAL: Chống UI "Cứng Ngắc" — Đừng Chỉ Đổi Màu

## Subagent Coordination — Bài học từ 03/07/2026

**Vấn đề:** Nhiều delegation batches chạy song song cùng modify 1 file (style.css, base.html) → agent cuối ghi đè agent trước → mất work. User nói "có thay đổi gì đâu" dù code đã được sửa.

**Pattern an toàn:**
1. Mỗi file chỉ giao cho 1 agent duy nhất trong 1 phase
2. Phase sau PHẢI đợi phase trước hoàn thành
3. File cốt lõi (style.css, app.py): DO NOT DELEGATE write, chỉ delegate read
4. Dùng file tạm cho WIP → PM merge thủ công

**Debug khi user nói "có thay đổi gì đâu":**
- Kiểm tra file bị agent khác ghi đè không?
- Server restarted chưa? Browser cache clear chưa (Ctrl+F5)? CSS version bump? (v=N)

> **Bài học từ thực tế (session 03/07/2026):** Khi user nói "skill thiết kế của bạn chưa ok" hoặc "có thay đổi gì đâu", nghĩa là bạn mới chỉ: (a) thêm biến CSS, (b) đổi màu accent, (c) cập nhật font — mà KHÔNG restructure layout + components.
>
> ⇒ **Clone/fix design phải thay đổi CẢ layout (HTML templates) lẫn visual (CSS), không chỉ CSS variables.**
>
> ⇒ **Sau mỗi design change, luôn kiểm tra VISUALLY — nếu không khác trước thì chưa xong.**

### 5 lỗi thường gặp khiến UI bị "cứng" (từ user feedback thực tế)

| # | Lỗi | Biểu hiện | Fix |
|---|-----|-----------|-----|
| 1 | **Thiếu hover states** | Click vào button không thấy feedback | Thêm `:hover` + `:active` cho mọi interactive element |
| 2 | **Transition quá nhanh** | Hover shift đột ngột, không mượt | `transition: color 0.3s ease` (ít nhất 0.2s) |
| 3 | **Thiếu sequencing** | Mọi element xuất hiện cùng lúc | GSAP timeline: stagger entrance, `-=0.1` overlap |
| 4 | **Layout không responsive** | Breakpoint chỉ đổi màu không đổi cấu trúc | CSS Grid: `grid-template-columns: repeat(3,1fr)` → `1fr` |
| 5 | **Chỉ sửa CSS không sửa HTML** | Màu mới nhưng bố cục cũ | Restructure templates: header, hero, cards, footer |

### Checklist "Có thay đổi gì đâu?" Prevention (BẮT BUỘC trước khi báo done)

Trước khi nói "xong" cho bất kỳ design change nào, verify bằng câu hỏi:

1. **Người dùng sẽ thấy gì KHÁC khi refresh trang?**
   - [ ] Accent color đã đổi? (header accent, button, link — 3 nơi khác nhau)
   - [ ] Font đã đổi? (headline — body — UI — 3 levels khác nhau)
   - [ ] Layout có khác? (header, hero, cards, footer — 4 sections)
   - [ ] Spacing có khác? (gap, padding, margin — resize browser)
   - [ ] Dark mode có khác? (toggle → xem từng section)

2. **CSS variables không nằm một mình** — mỗi variable cần được dùng ở ít nhất 3 nơi trong CSS

3. **Template class names phải match CSS class names** — nếu đổi class trong HTML mà không đổi CSS → page mất style

4. **Test bằng curl + grep** để verify từng CSS property được render:
```bash
# Verify accent color trong CSS served
curl -s http://localhost:5050/static/style.css | grep -oP -- '--accent: [^;]+'

# Verify font loaded
curl -s http://localhost:5050/ | grep -oP -- 'fonts\.googleapis\.com.*display=swap'

# Verify page size (page < 20KB → thiếu content)
curl -s -o /dev/null -w "%{size_download} bytes\n" http://localhost:5050/
```

### Flow đúng cho design change (từ bài học clone dep.com.vn)

```
1. Extract design tokens từ target site  → website_cloner.py
2. Update CSS variables (theme colors)   → style.css :root
3. Update HTML templates (layout)        → base.html, index.html (thêm section, đổi class)
4. Update component CSS (BEM classes)    → style.css (thêm .image-box, .post-card, .subnav)
5. Add Google Font (nếu target site dùng) → base.html <link>
6. Update dark mode variables            → style.css [data-theme="dark"]
7. Restart server + VERIFY               → pkill + python3 app.py + curl test
8. User nhìn thấy KHÁC NGAY              → nếu không → quay lại bước 2-4
```



## Kiến thức từ Ponytail — Lazy Senior Dev Philosophy (72k⭐)
- **Repo:** [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)
- **Triết lý:** "The best code is the code you never wrote" — viết ít code nhất có thể, dùng native browser features
- **Benchmark:** ~54% less code, ~20% cheaper, ~27% faster, 100% safe (measured on real Claude Code sessions)

### 7-Rung Ladder (trước khi viết bất kỳ dòng code nào)
```
1. Có cần feature này không?         → Không → bỏ qua (YAGNI)
2. Đã có trong codebase chưa?         → Tái sử dụng, đừng viết lại
3. Standard library có làm được?       → Dùng nó
4. Native browser feature có sẵn?      → Dùng nó
5. Dependency đã cài có giải quyết?    → Dùng nó
6. Có thể viết 1 dòng?                → Viết 1 dòng
7. Chỉ khi tất cả đều không:          → Viết tối thiểu
```

### Ponytail Rules cho News Design
- **Không abstraction nào không được yêu cầu:** Đừng tạo component wrapper cho cái `<input type="date">` — browser có sẵn rồi
- **Không dependency mới nếu tránh được:** CSS Grid thay Bootstrap, `@media` queries thay matchMedia JS
- **Deletion > Addition, Boring > Clever:** File ít hơn, code ngắn hơn, đơn giản hơn
- **`ponytail:` comment:** Mark intentional simplifications. Nếu shortcut có ceiling (global lock, O(n²) scan), comment ghi rõ ceiling và upgrade path
- **Non-trivial logic = 1 test:** Một assert-based check hoặc 1 file test nhỏ, không framework, không fixtures

### Ponytail Examples Áp Dụng cho News
| Task | Without Ponytail | With Ponytail | Saving |
|------|-----------------|---------------|--------|
| **Date picker** | Install flatpickr + wrapper + stylesheet | `<input type="date">` | 404 → 23 lines |
| **Color picker** | React color picker component | `<input type="color">` | 287 → 23 lines |
| **Deep clone** | `npm install lodash` + `cloneDeep()` | `structuredClone(obj)` | 1 dep → 0 dep |
| **Debounce search** | Utility function + class wrapper + config | `setTimeout`/`clearTimeout` inline | 116 → 10 lines |
| **CSV sum** | `pandas` DataFrame | `csv.DictReader` one-liner | 20 → 3 lines |
| **Email validation** | Regex validator class | `<input type="email">` | 75 → 3 lines |

### Native Browser APIs cho News (thay vì library)
| Thay vì | Dùng |
|----------|------|
| Date picker library | `<input type="date">` |
| Color picker | `<input type="color">` |
| Email validation | `<input type="email">` |
| URL validation | `<input type="url">` |
| Accordion JS | `<details>` / `<summary>` |
| Progress bar | `<progress>` |
| Modal/dialog | `<dialog>` + `showModal()` |
| Form validation library | `Constraint Validation API` (`checkValidity()`) |
| Number input + validation | `<input type="number" min max>` |
| Lazy loading library | `<img loading="lazy">` |
| Smooth scroll JS | `scroll-behavior: smooth` CSS |
| Deep clone utility | `structuredClone()` |
| Debounce utility | `setTimeout`/`clearTimeout` (chỉ khi cần ở 3+ nơi mới extract) |

## Kiến thức từ GSAP — Official Skills (10.8k⭐)
- **Repo:** [greensock/GSAP](https://github.com/greensock/GSAP) — 100% free (mọi plugin kể cả Club GSAP đều free sau Webflow acquisition)
- **Official AI skills:** [greensock/gsap-skills](https://github.com/greensock/gsap-skills) — 8 skills: core, timeline, scrolltrigger, plugins, utils, react, performance, frameworks
- **Cấu trúc skills:** gsap-core, gsap-timeline, gsap-scrolltrigger, gsap-plugins, gsap-utils, gsap-react, gsap-performance, gsap-frameworks

### Core Patterns (gsap-core)
- **`gsap.to(targets, vars)`** — animate từ current state → vars (thông dụng nhất)
- **`gsap.from(targets, vars)`** — animate từ vars → current state (entrance)
- **`gsap.fromTo(targets, fromVars, toVars)`** — explicit start & end, không đọc current values
- **`gsap.set(targets, vars)`** — apply ngay lập tức (duration 0)

### Transform Aliases (prefer over raw transform string)
```javascript
// GSAP transform aliases — apply in consistent order, more performant
x, y, z              // translateX/Y/Z (default px)
xPercent, yPercent   // translateX/Y in %
scale, scaleX, scaleY
rotation             // rotate (deg)
rotationX, rotationY // 3D rotate
skewX, skewY
transformOrigin      // e.g. "left top", "50% 50%"
autoAlpha            // opacity + visibility: hidden (prefer over opacity alone)
```

### Easing Functions — Complete Guide (từ gsap-core official skill)
```javascript
// Built-in eases: base (same as .out), .in, .out, .inOut
"none"               // linear
"power1"             // gradual (mild)
"power2"             // medium (default feel) ← default
"power3"             // strong (mượt, hơi chậm)
"power4"             // steepest (dramatic)
"back"               // overshoot nhẹ (pop effect)
"bounce"             // nảy như quả bóng
"circ"               // circular ease
"elastic"            // đàn hồi, nảy nhiều
"expo"               // exponential
"sine"               // sinusoidal
```

| Ease | Cảm giác | Dùng cho |
|------|----------|----------|
| `power1.out` | Nhẹ, gần như linear | Subtle UI, metadata |
| `power2.out` | Mượt tự nhiên (default) | Cards, fade-in, general |
| `power3.out` | Mượt hơn, hơi chậm | Headers, hero sections |
| `power4.out` | Dramatic, chậm rãi | Major entrances |
| `back.out(1.7)` | Overshoot nhẹ — pop | Featured card, highlights |
| `elastic.out(1,0.3)` | Nảy mềm như dây thun | Badges, notifications |
| `none` | Linear | Progress bars, scroll-linked |

### Stagger Patterns (từ gsap-core official)
```javascript
// Cơ bản
gsap.to(".item", { y: -20, stagger: 0.1 });

// Advanced: from: "random" | "start" | "center" | "end" | "edges"
gsap.to(".card", {
  opacity: 1, y: 0,
  stagger: { amount: 0.5, from: "random" },  // 0.5s total, random order
  ease: "power2.out"
});

// Function-based values
gsap.to(".item", {
  x: (i) => i * 50,  // first = 0, second = 50, third = 100...
  stagger: 0.1
});
```

### autoAlpha (prefer over opacity alone)
```javascript
gsap.to(".element", { autoAlpha: 0, duration: 0.5 });
// Khi autoAlpha = 0: GSAP set opacity:0 + visibility:hidden (không block click)
// Khi autoAlpha ≠ 0: visibility: inherit
// Tránh invisible elements blocking pointer events
```

### gsap.matchMedia() — Responsive Animation (v3.11+)
**Pattern official từ gsap-core skill — dùng thay vì window.matchMedia thủ công:**
```javascript
const mm = gsap.matchMedia();

mm.add({
  isDesktop: "(min-width: 800px)",
  isMobile: "(max-width: 799px)",
  reduceMotion: "(prefers-reduced-motion: reduce)"
}, (context) => {
  const { isDesktop, reduceMotion } = context.conditions;

  gsap.to(".box", {
    rotation: isDesktop ? 360 : 180,
    duration: reduceMotion ? 0 : 2
  });

  return () => { /* cleanup khi condition không match */ };
});

// Khi component unmount:
// mm.revert();
// Để re-run: gsap.matchMediaRefresh();
```

### gsap.defaults() — Project-wide defaults
```javascript
gsap.defaults({ duration: 0.6, ease: "power2.out" });
// Apply cho mọi tween sau đó
```

### Directional Rotation
```javascript
gsap.to(".element", { rotation: "-170_short" });  // 20° clockwise
// _short = shortest path, _cw = clockwise, _ccw = counter-clockwise
```

### clearProps — Khi CSS class cần take over sau animation
```javascript
gsap.to(".element", {
  x: 100, duration: 0.5,
  clearProps: "x"  // xóa inline style khi complete
});
// clearProps: "all" hoặc true = xóa tất cả inline styles
```

## NYT Design Patterns

### Header
- Newspaper name ở giữa, font serif, size lớn (36-42px)
- Small cap subtitle
- Decorative line (hr ngắn, centered)
- Section nav: uppercase, small font, border-right separator

### Date Navigation
- Previous / Next day buttons (border style)
- Date picker (native `<input type="date">` with onchange)
- "Hôm nay" link
- Background: warm light (#faf8f5)

### Article Grid (Today's Paper)
- 3-column CSS grid
- Featured article: full-width, 2-column inner split (text + visual)
- Article cards: badge (uppercase accent), headline (serif), excerpt (gray)
- Grid-col: flex column để các article xếp dọc

### Article Page (Single)
- Section badge (uppercase, accent color, small)
- Headline: 40px serif, bold, -0.5px letter-spacing
- Decorative line (50px, border)
- Byline: sans-serif, 13px, gray
- Drop cap: first-letter pseudo-element, 56px float
- Body: 17px serif, 1.85 line-height
- Sources section: small uppercase heading, sans-serif urls
- Back link: bordered button, centered

### Article Page — Two-Column with Sidebar (Related Articles)

A variant of the single article page that adds a **sidebar with related article headlines** on the right. Used in production at Phương's Daily (Flask + Jinja2).

**Layout (flex, not grid):**
```css
.article-layout {
  max-width: 1040px;
  margin: var(--space-8) auto;
  padding: 0 20px;
  display: flex;
  gap: var(--space-10);
  align-items: flex-start;
}
.article-main       { flex: 0 0 680px; max-width: 680px; }  /* content column */
.article-sidebar    { flex: 0 0 300px; width: 300px; }       /* sidebar column */
```

**Sidebar component (`.article-sidebar`):**
- **Container:** `background: var(--bg-warm)`, `border: 1px solid var(--border-light)`, `padding: var(--space-6)`, `position: sticky; top: 20px` — scrolls with page, stays visible
- **Heading:** `📰 Có thể bạn muốn đọc` — heading with `border-bottom: 2px solid var(--accent)`, 14px bold
- **Related list (`.related-list`):** vertical flex, no gap — each item is a divider-separated row
- **Item (`.related-item`):** clickable `<a>`, flex row with emoji (26px) + text column (title + date), `border-bottom: 1px solid var(--border-light)`, hover changes bg to `--bg-card` with negative margin for full-width highlight
- **Title (`.related-title`):** 13px heading, `-webkit-line-clamp: 2` for 2-line truncation, color to `--accent` on hover
- **Date (`.related-date`):** 10px uppercase, `--text-light`, letter-spaced
- **More link (`.sidebar-more`):** bottom section with `border-top`, centered "Xem thêm →" link to category page

**Backend data logic (Flask):**
Priority order for populating up to 7 related articles:
1. Same category + same date (same-day related content)
2. Same category + other dates (newest first)
3. Most recent articles of any category (fallback fillers)

```python
same_cat_same_date = [a for a in all_arts 
                     if a["category"] == art["category"] 
                     and a["id"] != art["id"] 
                     and a["date"] == art["date"]]
same_cat_other_date = [a for a in all_arts 
                      if a["category"] == art["category"] 
                      and a["id"] != art["id"] 
                      and a["date"] != art["date"]]
same_cat_other_date.sort(key=lambda a: a["date"], reverse=True)
related = same_cat_same_date + same_cat_other_date
if len(related) < 7:
    other_ids = {a["id"] for a in related} | {art["id"]}
    fillers = [a for a in all_arts if a["id"] not in other_ids]
    fillers.sort(key=lambda a: a["date"], reverse=True)
    needed = 7 - len(related)
    related += fillers[:needed]
related_articles = related[:7]
```

Pass to template: `return render_template("article.html", article=art, related_articles=related_articles, ...)`

**Template pattern (Jinja2):**
```html
<div class="article-layout">
  <div class="article-main">
    <article class="article-wrap">
      ...existing article content (badge, headline, body, sources, nav)...
    </article>
  </div>
  <aside class="article-sidebar">
    <div class="sidebar-heading">📰 Có thể bạn muốn đọc</div>
    {% for rel in related_articles %}
    <a href="/article/{{ rel.id }}" class="related-item">
      <span class="related-emoji">{{ rel.emoji or '📄' }}</span>
      <span class="related-text">
        <span class="related-title">{{ rel.title }}</span>
        <span class="related-date">{{ rel.date_display }}</span>
      </span>
    </a>
    {% endfor %}
    <div class="sidebar-more">
      <a href="/category/{{ article.category }}" class="sidebar-more-link">Xem thêm →</a>
    </div>
  </aside>
</div>
```

**GSAP entrance (sidebar slides in from right):**
```javascript
gsap.from('.article-sidebar', { opacity: 0, x: 20, duration: 0.5, delay: 0.3 });
```

**Responsive (≤768px):**
- `.article-layout` → `flex-direction: column` (sidebar drops below content)
- `.article-main` → `flex: 1 1 auto; max-width: 100%` (full width)
- `.article-sidebar` → `flex: 1 1 auto; width: 100%; position: static` (full width, no sticky)

### Color Palette — Light Mode (default — dep.com.vn inspired)
```css
:root, [data-theme="light"] {
  --bg: #ffffff;
  --bg-warm: #f7f8f9;
  --bg-card: #ffffff;
  --text: #222222;
  --text-gray: #575760;
  --text-light: #a09f9f;
  --border: #e2e2e2;
  --border-light: #f0f0f0;
  --accent: #032435;        /* Deep navy — cloned from dep.com.vn */
  --accent-hover: #032741;
  --link: #032435;
  --btn-bg: #032435;
  --btn-text: #ffffff;
}
```

### Color Palette — Dark Mode (dep.com.vn navy-inspired)
```css
[data-theme="dark"] {
  --bg: #0d1929;
  --bg-warm: #0b1116;
  --bg-card: #152029;
  --text: #e8e8f0;
  --text-gray: #9898b8;
  --text-light: #6868a0;
  --border: #2a3a4a;
  --border-light: #1a2a3a;
  --accent: #4a9eff;        /* Bright blue on dark */
  --accent-hover: #6aafff;
  --link: #4a9eff;
  --btn-bg: #4a9eff;
  --btn-text: #0d1929;
}
```

### Three-Mode Theme System (Dark/Light/Auto)
```javascript
// 1. On page load — check localStorage, then system preference
(function() {
  const saved = localStorage.getItem('phuong-theme');
  if (saved) {
    document.documentElement.setAttribute('data-theme', saved);
  } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    document.documentElement.setAttribute('data-theme', 'dark');
  }
})();

// 2. Toggle function
function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('phuong-theme', next);
}
```

### Vietnamese Font Stack (from VnExpress + dep.com.vn research)
For Vietnamese readability, **Be Vietnam Pro** (Google Font) + serif is optimal:
```css
--font-serif: 'Be Vietnam Pro', Georgia, 'Times New Roman', Times, serif;  /* headlines */
--font-sans: 'Be Vietnam Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;  /* body */
```
**Why Be Vietnam Pro:** Designed specifically for Vietnamese diacritics — renders cleaner than Georgia/Arial at all sizes. Used by dep.com.vn and other major Vietnamese sites.
- **Headlines** (40px): Be Vietnam Pro bold — clean, modern
- **Body** (17px, 1.85 line-height): Be Vietnam Pro — optimized for Vietnamese
- **UI/Metadata** (11-13px): Be Vietnam Pro — retains legibility at small sizes
- **Fallback:** Georgia/Times New Roman cho serif, Arial cho sans-serif
- **Google Fonts CDN:** `<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700&display=swap" rel="stylesheet">`

### NYT Color Token System (Live-Inspected — 50+ tokens)

All background → content → stroke levels map to a consistent 5-tier system:

```css
/* Background tiers: primary → secondary → tertiary → overlay → scrim */
--color-background-primary:   #ffffff;  /* white page */
--color-background-secondary: #f8f8f8;  /* subtle gray */
--color-background-tertiary:  #ebebeb;  /* loading/skeleton */

/* Content tiers: primary → secondary → tertiary → quarternary → quintary */
--color-content-primary:   #121212;  /* headings */
--color-content-secondary: #363636;  /* body text */
--color-content-tertiary:  #5a5a5a;  /* metadata */
--color-content-quaternary: #727272; /* captions */
--color-content-quintary:  #8b8b8b;  /* disabled */

/* Signal colors */
--color-signal-editorial:  #326891;  /* teal-blue accent */
--color-signal-negative:   #a90111;  /* red */
--color-signal-positive:   #267c30;  /* green */
--color-signal-breaking:   #d0021b;  /* breaking news */
--color-signal-highlight:  #fefad1;  /* yellow highlight */

/* Stroke/Divider tiers */
--color-stroke-primary:   #121212;
--color-stroke-secondary: #8b8b8b;
--color-stroke-tertiary:  #c7c7c7;
```

### NYT Typography System (Live-Inspected)

Full scale with font families, weights, and line-heights — see `references/design-research-2026-07.md` for the complete table.

**Design principle:** 3 font families for 3 purposes:
- **nyt-cheltenham** (serif) → headlines, story titles, authoritative voice
- **nyt-imperial** (serif) → body text, readable at 16-20px
- **nyt-franklin** (sans-serif) → UI, labels, bylines, buttons, metadata

### NYT Spacing System (Live-Inspected)

```css
/* 12-step spacing scale from 0.25rem to 5rem */
--tpl-size-spacing-0-5: 0.25rem  /* 4px  — micro */
--tpl-size-spacing-1:   0.5rem   /* 8px  — tight */
--tpl-size-spacing-1-5: 0.75rem  /* 12px — snug */
--tpl-size-spacing-2:   1rem     /* 16px — base */
--tpl-size-spacing-2-5: 1.25rem  /* 20px — comfortable */
--tpl-size-spacing-3:   1.5rem   /* 24px */
--tpl-size-spacing-4:   2rem     /* 32px */
--tpl-size-spacing-5:   2.5rem   /* 40px */
--tpl-size-spacing-6:   3rem     /* 48px */
--tpl-size-spacing-7:   3.5rem   /* 56px */
--tpl-size-spacing-8:   4rem     /* 64px */
--tpl-size-spacing-9:   4.5rem   /* 72px */
--tpl-size-spacing-10:  5rem     /* 80px */
```

### NYT Button States (Live-Inspected)

**Standard button:**
```css
/* Normal */  background: #fff;  border: 1px solid #121212;  border-radius: 3px;  color: #121212;
/* Hover  */  background: #121212;  color: #f8f8f8;
/* Pressed */ background: #121212;  opacity: 0.8;
```

**Emphatic (Subscribe CTA):**
```css
/* Normal */  background: #121212;  color: #f8f8f8;
/* Hover  */  opacity: 0.8;
```

### NYT Navigation Behavior

- Position: `static` (scrolls with page — **not sticky**)
- Top bar: date + stock tickers + "Today's Paper"
- Nav links: `nyt-franklin`, 11px, weight 600, uppercase
- Transitions: `outline-color 0.1s ease-out` (subtle)

### Responsive Breakpoints (Guardian-inspired)
| Breakpoint | Grid | Headline | Notes |
|-----------|------|----------|-------|
| >900px | 3 columns | 40px | Desktop full |
| 600-900px | 2 columns | 30px | Tablet |
| <600px | 1 column | 24px | Mobile, wrap date nav |

---

## Guardian Grid System (Live-Inspected `dcr-*` Classes)

### Main Grid (`.dcr-lypmm`)
```css
.dcr-lypmm { display: grid; grid-auto-rows: auto; column-gap: 10px; }

/* MOBILE: 4 equal columns, zero gutters */
@media (max-width: 739px) {
  grid-template-columns:
    [viewport-start] 0px
    [content-start main-column-start] repeat(4, minmax(0px, 1fr))
    [content-end main-column-end] 0px [viewport-end];
}

/* TABLET: 12 cols × 40px + 1fr gutters */
@media (min-width: 740px) {
  grid-template-columns:
    [viewport-start] minmax(0px, 1fr)
    [content-start main-column-start] repeat(12, 40px)
    [content-end main-column-end] minmax(0px, 1fr) [viewport-end];
}

/* DESKTOP: 12 cols × 60px + 1fr gutters */
@media (min-width: 980px) {
  grid-template-columns:
    [viewport-start] minmax(0px, 1fr)
    [content-start main-column-start] repeat(12, 60px)
    [content-end main-column-end] minmax(0px, 1fr) [viewport-end];
}
```

**Named lines:** `viewport-start/end` (gutters), `content-start/end` (content), `main-column-start/end` (main queue), `title-start/end`, `hide-start/end`.

**Container widths:** 740px → 980px → 1140px → 1300px.

### Card Pattern (`.dcr-bpr716` + `.dcr-idxb0f`)
```css
/* Whole-card clickable overlay */
.dcr-idxb0f { position: absolute; inset: 0; z-index: 2; }
.dcr-idxb0f:focus { outline: 0; }
html:not(.src-focus-disabled) .dcr-idxb0f:focus {
  box-shadow: rgb(0, 119, 182) 0 0 0 3px;
}

/* Card headline */
.dcr-10xs001 {
  font-family: "GH Guardian Headline", "Guardian Egyptian Web", Georgia, serif;
  font-size: 1.0625rem; line-height: 1.15; font-weight: 500;
}

/* Card container */
@media (min-width: 740px) { .dcr-bpr716 { width: 280px; flex-direction: row; } }
```

**Placement by column span:**
```css
.article-card--full    { grid-column: content-start / content-end; }
.article-card--main    { grid-column: content-start / main-column-end; }
.article-card--sidebar { grid-column: main-column-end / content-end; }
```

---

## dep.com.vn Component Patterns (v6 — Live-Fetched 2026-07-03)

> **Full pixel-level analysis**: `references/dep-exact-layout-components.md`
> Includes: Image Box Hero, 130px thumbnail card, category badge border-left, subnav scroll, responsive breakpoints, design tokens.

dep.com.vn (WordPress + GeneratePress + Elementor) is the reference for Phương's Daily frontend. Key patterns:

### 1. Image Box Hero — Full-width + Gradient Overlay + Centered Content Box

```html
<div class="image-box">
  <div class="image-box__image-wrapper">
    <div class="image-box__image" style="background-image:url('...');"></div>
    <div class="image-box__image-overlay"></div>
  </div>
  <div class="image-box__content">
    <div class="image-box__content-inner">
      <span class="post-card__category-link">{{ category }}</span>
      <h2 class="image-box__title"><a href="...">{{ title }}</a></h2>
    </div>
  </div>
  <a class="image-box__overlay-link" href="..."></a>
</div>
```

| Part | Key Props |
|------|-----------|
| `.image-box__image` | `height: 380px; background-image; background-size: cover` |
| `.image-box__image:after` | Gradient overlay: `linear-gradient(180deg, rgba(85,85,85,0), #000)` at bottom 25% |
| `.image-box__content-inner` | `background: hsla(0,0%,100%,0.88); box-shadow: 0 3px 8px rgba(0,0,0,.24); padding: 1rem 1.5rem; text-align: center` |
| `.image-box__overlay-link` | `position: absolute; inset: 0; z-index: 4` |
| **Mobile (<768px)** | Content becomes `position: relative`, bg/box-shadow removed, title turns white |

### 2. Post Card — 130px Thumbnail Horizontal Variant

When `lead_image` exists, add class `post-card--has-image` for a horizontal layout:

```css
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
```

Image stays `aspect-ratio: 1/1` with `object-fit: cover` and `scale(1.05)` zoom on hover.

### 3. Category Badge — 2px Border-Left Accent

Signature dep.com.vn visual accent — a 2px solid left border on the category link:

```css
.post-card__category-link {
  border-left: 2px solid var(--accent);
  padding-left: 10px;
  font-size: 0.75rem;
  font-weight: var(--font-semibold);
  text-transform: uppercase;
  line-height: 1;
  transition: color .4s ease;
}
.post-card__category-link:hover { color: var(--bs-secondary); }
```

### 4. Subnav — Horizontal Scroll (Hidden Scrollbars)

```css
.subnav__list {
  display: flex;
  flex-wrap: nowrap;
  overflow-x: auto;
  white-space: nowrap;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;           /* Firefox */
}
.subnav__list::-webkit-scrollbar { display: none; }  /* WebKit */
```

### 5. Responsive Grid Columns

| Breakpoint | Post Grid | Hero Height | Thumbnail |
|-----------|-----------|-------------|-----------|
| <768px | 1 col | 250px | 100px |
| 768px | 2 cols | 320px | 120px |
| 960px | 2 cols | 360px | 130px |
| 1280px | 4 cols | 400px | 130px |

### 6. CSS Version Cache Busting

```html
<link rel="stylesheet" href="/static/style.css?v=N">
```

Bump `N` each time CSS changes. Convention: `v=1` → `v=6` (current).

### 7. Footer — dep.com.vn Exact

```css
.site-footer { background: var(--base-3); border-top: 1px solid var(--border); }
.footer__inner { text-align: left; font-size: 13px; opacity: 0.75; }
```

---

## VnExpress Layout Patterns (Live-Inspected — Vietnamese-Optimized)

### Navigation Hover Colors (Per-Category System)

Each category has a unique hover color — a distinctive VnExpress pattern not used by NYT or Guardian:

```css
.main-nav .parent li.kinhdoanh:hover a  → color: #065e9d  /* Business: blue */
.main-nav .parent li.giaitri:hover a    → color: #ec326b  /* Entertainment: pink */
.main-nav .parent li.thethao:hover a    → color: #5fae2e  /* Sports: green */
.main-nav .parent li.phapluat:hover a   → color: #923a3c  /* Law: maroon */
.main-nav .parent li.giaoduc:hover a    → color: #eb7600  /* Education: orange */
.main-nav .parent li.suckhoe:hover a    → color: #049b93  /* Health: teal */
.main-nav .parent li.doisong:hover a    → color: #309fc0  /* Lifestyle: cyan */
.main-nav .parent li.dulich:hover a     → color: #0083d6  /* Travel: bright blue */
.main-nav .parent li.khoahoc:hover a    → color: #ad9634  /* Science: olive */
.main-nav .parent li.xe:hover a         → color: #8392a0  /* Cars: gray */
.main-nav .parent li.home:hover a       → background: #b52759  /* Home: red-pink bg */
```

### Navigation Behavior

- Position: `static` (scrolls with page — **not sticky**)
- Height: ~40px
- Background: `#f7f7f7`
- Sub-menu: `.sub` appears on hover with `border-top: 1px solid rgb(159, 34, 78)`
- Mobile: hamburger menu with `.all-menu:hover .hamburger { background: #b52759; }`

### Container & Two-Column Layout
```css
.container { display: flex; max-width: 1130px; margin: 0 71px; padding: 0 15px; }
.col-left  { width: 780px; padding-right: 20px; }
.col-right { width: 320px; padding-left: 20px; }

@media (max-width: 979px) {
  .col-left { width: 100%; padding-right: 0; }
  .col-right { display: none; }
}
```

### Card & Typography
```css
.item-news { width: 100%; float: left; padding-bottom: 15px; margin-bottom: 15px; border-bottom: 1px solid #e5e5e5; }
.title-news { font-family: Merriweather, serif; font-size: 20px; line-height: 32px; font-weight: 700; color: #222; }
h1          { font-family: Merriweather, serif; font-size: 32px; line-height: 48px; font-weight: 700; }
article     { font-family: arial, sans-serif; font-size: 18px; line-height: 28.8px; width: 680px; }
.description { font-family: arial, sans-serif; font-size: 14px; line-height: 19.6px; color: #4f4f4f; }
.meta-news   { font-family: Arial; font-size: 14px; color: #757575; }
```

---

## BBC Pattern (Reference)

**Grid:** CSS Grid `repeat(4,1fr)` → `repeat(3,1fr)` at 1008px → `repeat(2,1fr)` at 672px → `1fr` at 480px.
**Card:** `border-top: 1px solid #e0e0e0; padding: 16px 0;`
**Font:** `"BBC Reith", "Helvetica", "Arial", sans-serif` — headline `20px/1.2/700`, summary `14px/1.35`.

---

## Font Stack Comparison

| Site | Headline | Body | UI/Meta |
|------|----------|------|---------|
| **NYT** | `nyt-franklin, helvetica, arial, sans-serif` | `"Times New Roman", Georgia, serif` | `nyt-franklin, helvetica, arial, sans-serif` |
| **Guardian** | `"GH Guardian Headline", "Guardian Egyptian Web", Georgia, serif` | `"Guardian Egyptian Web", Georgia, serif` | `GuardianTextSans, "Helvetica Neue", Arial, sans-serif` |
| **VnExpress** | `Merriweather, serif` | `arial, sans-serif` | `Arial, sans-serif` |
| **BBC** | `"BBC Reith", "Helvetica", "Arial", sans-serif` | `"BBC Reith", "Helvetica", "Arial", sans-serif` | `"BBC Reith", "Helvetica", "Arial", sans-serif` |

---

## Cấu trúc Flask App cho News

```
app.py (Flask)
  ├── Routes:
  │   GET /                        → Homepage (latest date)
  │   GET /date/<YYYY-MM-DD>       → Reports by date
  │   GET /category/<slug>         → Filter by section
  │   GET /article/<id>            → Single article
  │   GET /search?q=               → Full-text search
  │   GET /refresh                 → Regenerate reports
  └── Helpers:
      load_all_articles()          → Load JSON from reports/
      get_common_context()         → Date nav + filters
      format_date_display()        → "Thứ Sáu, 03/07/2026"
      related_articles logic       → article() route: same-cat same-date → same-cat other-date → most recent (up to 7)
```

## Component Micro-Interactions — Chống "cứng ngắc"

> UI bị **cứng** khi thiếu hover states, transition quá nhanh, không feedback khi click.

### Card Hover
```css
.article-card {
  transition: transform 0.25s cubic-bezier(0.2, 0, 0, 1),
              box-shadow 0.25s cubic-bezier(0.2, 0, 0, 1);
}
.article-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}
```

### Button Active
```css
.date-nav-btn:active, .back-link:active {
  transform: scale(0.96);
}
```

### Theme Switch Transition (cho tất cả elements)
```css
body, .utility-bar, .newspaper-header, .section-nav, .date-nav,
.article-card, .newspaper-footer {
  transition: background-color 0.3s ease,
              color 0.3s ease,
              border-color 0.3s ease;
}
```

### Transition Duration Table
| Component | Duration | Easing |
|-----------|----------|--------|
| Card hover | 0.25s | cubic-bezier(0.2,0,0,1) |
| Theme switch | 0.3s | ease |
| Button active | 0.1s | ease |
| GSAP fade-in | 0.6-0.8s | power2.out |

## GSAP vs CSS — Decision Table
| Situation | Use | Why |
|-----------|-----|-----|
| Page entrance (sequencing) | GSAP timeline | Overlap control |
| Card stagger on scroll | GSAP + ScrollTrigger | Scroll-driven |
| Hero pop (overshoot) | GSAP back.out() | CSS can't overshoot |
| Hover effects | CSS transitions | Performance |
| Theme switch | CSS transitions | GPU-accelerated |
| Button active | CSS transitions | 0.1s, no JS needed |

**Ponytail rule:** GSAP for entrance + scroll; CSS for interaction + theme.

## GSAP Animation Patterns — Advanced (Chống cứng ngắc)

Nguyên nhân chính làm animation bị **cứng ngắc**: dùng từng `gsap.from()` rời rạc, thiếu sequencing, thiếu stagger mượt.

### Quy tắc Ponytail
> "Use what's there. Animate smoothly. Don't over-engineer."
- Dùng `gsap.timeline()` cho page entrance thay vì nhiều lệnh rời
- Dùng `ScrollTrigger` cho card grid (scroll-triggered)
- Dùng `stagger` với `from: "random"` hoặc `0.08` spacing
- Luôn check `prefers-reduced-motion` trước khi chạy

### GSAP Timeline — Position Parameter (từ gsap-timeline official skill)

**Third argument** (hoặc position property trong vars) controls placement:

```javascript
const tl = gsap.timeline({ defaults: { duration: 0.5, ease: "power2.out" } });

tl.to(".a", { x: 100 }, 0);            // at 0 seconds
tl.to(".b", { y: 50 }, "+=0.5");       // 0.5s sau last end
tl.to(".c", { opacity: 0 }, "<");       // same start as previous
tl.to(".d", { scale: 2 }, "<0.2");     // 0.2s sau previous start
tl.to(".e", { y: -20 }, "label+=0.3"); // 0.3s sau label
```

**Position parameter values:**
| Value | Meaning |
|-------|---------|
| `1` | Absolute: at 1 second |
| `"+=0.5"` | 0.5s sau khi tween trước kết thúc |
| `"-=0.2"` | 0.2s trước khi tween trước kết thúc (overlap) |
| `"<"` | Cùng lúc với tween vừa thêm |
| `">"` | Khi tween vừa thêm kết thúc (default) |
| `"<0.2"` | 0.2s sau khi tween vừa thêm bắt đầu |
| `"labelName"` | Tại label position |
| `"labelName+=0.3"` | 0.3s sau label |

### Labels — Maintainable Sequencing
```javascript
const tl = gsap.timeline();
tl.addLabel("intro", 0);
tl.to(".a", { x: 100 }, "intro");
tl.addLabel("outro", "+=0.5");
tl.to(".b", { opacity: 0 }, "outro");
tl.play("outro");       // play from label
```

### Nesting Timelines
```javascript
const master = gsap.timeline();
const child = gsap.timeline();
child.to(".a", { x: 100 }).to(".b", { y: 50 });
master.add(child, 0);
master.to(".c", { opacity: 0 }, "+=0.2");
```

### gsap.utils (từ gsap-utils official skill)

Dùng trong function-based values, ScrollTrigger callbacks, hoặc bất kỳ JS nào drive GSAP:

```javascript
// clamp — giới hạn giá trị
gsap.utils.clamp(0, 100, 150);  // 100
let clampFn = gsap.utils.clamp(0, 100);
clampFn(150); // 100

// mapRange — map từ range này sang range khác
gsap.utils.mapRange(0, 100, 0, 500, 50); // 250

// normalize — normalize về 0-1
gsap.utils.normalize(0, 100, 50); // 0.5

// random — random number hoặc từ array
gsap.utils.random(-100, 100);
gsap.utils.random(["red", "blue", "green"]);

// snap — snap về step gần nhất
gsap.utils.snap(10, 23);  // 20
gsap.utils.snap([0, 100, 200], 150);  // nearest in array

// pipe — compose functions
const fn = gsap.utils.pipe(
  (v) => gsap.utils.normalize(0, 100, v),
  (v) => gsap.utils.snap(0.1, v)
);

// distribute — advanced stagger (grid-aware)
gsap.to(".class", {
  scale: gsap.utils.distribute({
    base: 0.5,
    amount: 2.5,
    from: "center"
  })
});

// wrap — cyclic values (infinite scroll)
gsap.utils.wrap(0, 360, 370);  // 10
```

### Master Timeline (Page Entrance)
```javascript
var master = gsap.timeline({ defaults: { ease: 'power3.out' } });

master.from('.utility-bar',      { y: -20, opacity: 0, duration: 0.3 })
      .from('.newspaper-header',  { opacity: 0, y: 10, duration: 0.4 }, '-=0.1')
      .from('.section-nav',       { opacity: 0, duration: 0.3 }, '-=0.2')
      .from('.date-nav',          { opacity: 0, y: -8, duration: 0.3 }, '-=0.1')
      .from('.featured-card',     {
        opacity: 0, y: 30, scale: 0.98,
        duration: 0.7, ease: 'back.out(1.4)'  // overshoot nhẹ = mượt
      }, '-=0.1');
```
**Lưu ý:** `-=0.1` = overlap 0.1s giữa các step — tạo cảm giác flow liên tục.

### Scroll-Triggered Stagger (Grid Cards) — Official GSAP Patterns

**Quy tắc quan trọng từ gsap-scrolltrigger official skill:**
- **Register plugin 1 lần:** `gsap.registerPlugin(ScrollTrigger);`
- **ScrollTrigger trên timeline hoặc top-level tween,** không phải trên child tween bên trong timeline
- **Dùng scrub** cho scroll-linked progress HOẶC **toggleActions** cho discrete play/reverse — không dùng cả 2
- **Gọi `ScrollTrigger.refresh()`** sau DOM/layout changes (new content, images, fonts)
- **Tạo ScrollTriggers theo thứ tự top → bottom** trên trang; nếu dynamic thì set **refreshPriority**
- **Không dùng ease khác `"none"`** trên horizontal animation khi dùng `containerAnimation`

```javascript
// Pattern 1: Scroll-triggered stagger (phổ biến cho card grid)
gsap.from('.article-card', {
  opacity: 0, y: 40, duration: 0.6,
  stagger: 0.08,
  ease: 'power2.out',
  scrollTrigger: {
    trigger: '.news-grid',
    start: 'top 85%',
    toggleActions: 'play none none none'
  }
});

// Pattern 2: Timeline + ScrollTrigger with scrub (parallax reading)
const tl = gsap.timeline({
  scrollTrigger: {
    trigger: '.featured-article',
    start: 'top top',
    end: '+=1000',
    scrub: 1,
    pin: true,
    markers: false  // tắt markers ở production!
  }
});
tl.to('.featured-visual', { scale: 1.1, duration: 1 })
  .to('.featured-text', { y: -30, duration: 1 }, '<');

// Pattern 3: ScrollTrigger.batch() — batch multiple elements
ScrollTrigger.batch('.card', {
  interval: 0.1,
  batchMax: 4,
  onEnter: (batch) => gsap.to(batch, {
    opacity: 1, y: 0, stagger: 0.1, overwrite: true
  }),
  onLeaveBack: (batch) => gsap.set(batch, {
    opacity: 0, y: 50, overwrite: true
  }),
  start: 'top 80%',
  end: 'bottom 20%'
});

// Pattern 4: Standalone ScrollTrigger (no tween linked)
ScrollTrigger.create({
  trigger: '#progress-indicator',
  start: 'top top',
  end: 'bottom 50%+=100px',
  onUpdate: (self) => {
    // self.progress (0-1), self.direction
    document.getElementById('progress-bar').style.width = `${self.progress * 100}%`;
  }
});
```

### Article Detail Entrance
```javascript
gsap.from('.article-headline', {
  opacity: 0, y: 20, duration: 0.8, ease: 'power2.out'
});
gsap.from('.article-content', {
  opacity: 0, y: 10, duration: 0.6, delay: 0.3, ease: 'power1.out'
});
gsap.from('.article-sources', {
  opacity: 0, duration: 0.5, delay: 0.6
});
```

### Respect prefers-reduced-motion — Official GSAP Pattern

**Dùng `gsap.matchMedia()` (GSAP 3.11+) — pattern official từ gsap-core skill:**

```javascript
const mm = gsap.matchMedia();

mm.add({ reduceMotion: "(prefers-reduced-motion: reduce)" }, (context) => {
  const { reduceMotion } = context.conditions;

  // Tất cả animation trong block này đều được quản lý
  gsap.from('.article-card', {
    opacity: 0, y: 40, duration: 0.6,
    stagger: 0.08,
    ease: 'power2.out',
    scrollTrigger: {
      trigger: '.news-grid',
      start: 'top 85%',
      toggleActions: 'play none none none'
    }
  });

  // Nếu reduceMotion === true, duration = 0 (skip animation)
  gsap.to('.hero-title', {
    y: reduceMotion ? 0 : 20,
    opacity: 1,
    duration: reduceMotion ? 0 : 0.8
  });

  return () => {}; // cleanup khi không match
});

// mm.revert() khi cleanup
```

**Lý do dùng matchMedia thay vì if-check thủ công:**
- matchMedia tự động revert animation khi media query không còn match
- Tất cả ScrollTriggers trong handler cũng được cleanup
- Hỗ trợ responsive breakpoints: `{ isDesktop: "(min-width:800px)", isMobile: "(max-width:799px)" }`
- Không cần gọi `ScrollTrigger.refresh()` thủ công khi resize

### Key GSAP Easing cho News
| Ease | Cảm giác | Dùng cho |
|------|----------|----------|
| `power2.out` | Mượt, tự nhiên (default) | Cards, fade-in |
| `power3.out` | Mượt hơn, hơi chậm | Header, timeline base |
| `back.out(1.4)` | Overshoot nhẹ, pop | Featured hero, highlights |
| `elastic.out(1,0.3)` | Nảy nhẹ | Badges (hiếm) |

## Article Images — Lead Image + Thumbnail

### Featured Card (Trang chủ)
Dùng `background-image` CSS inline khi article có `lead_image`:
```html
<div class="featured-visual"
     {% if article.lead_image %}
     style="background-image:url('{{ article.lead_image }}');"
     {% endif %}>
</div>
```
```css
.featured-visual {
  background-size: cover;
  background-position: center;
  min-height: 200px;
}
```

### Article Detail Page
Scraper tự động chèn `<figure>` với lead image ở đầu `content_html`:
```html
<figure style="margin:0 0 24px;">
  <img src="{{ lead_image }}" alt="..." style="width:100%;" />
</figure>
```

#---

## Newsletter / News Digest Design Patterns

> **Full report:** `references/newsletter-digest-design-patterns.md` — 10-site analysis with layout patterns, hierarchy handling, image usage, and 5 implementable templates.
>
> **Implementation reference:** `references/tldr-digest-css-patterns.md` — current v8 CSS class system, component patterns, responsive breakpoints.

### 5 Digest Patterns to apply

1. **1-Cột + Category Sections** (TLDR) — simplest, mobile-best; articles grouped by topic with colored category badges
2. **Smart Brevity Card** (Axios) — bordered card with "Tại sao quan tâm" context box (key for non-expert readers)
3. **Feature + Grid** (The Hustle) — hero article with OG image + grid of supporting articles
4. **Minimal List** (Linear) — no borders, only horizontal rules; category filter tabs; relative dates
5. **Dark Mode toggle** — CSS custom properties; low effort, high perceived value

### ⚡ Flask-TLDR Integration Pattern (v8, current)

The v8 implementation moves **category colors from CSS to Flask context** — the canonical source of truth is a `CATEGORY_COLORS` dict in `app.py`, passed to all templates via `get_common_context()`:

```python
CATEGORY_COLORS = {
    "economy":         {"label": "Kinh tế",   "bg": "#dbeafe", "text": "#1e40af", "border": "#2563eb"},
    "daily-briefing":  {"label": "Kinh tế",   "bg": "#dbeafe", "text": "#1e40af", "border": "#2563eb"},  # legacy alias
    "technology":      {"label": "Công nghệ", "bg": "#ede9fe", "text": "#5b21b6", "border": "#7c3aed"},
    "github":          {"label": "GitHub",    "bg": "#f3e8ff", "text": "#6b21a8", "border": "#9333ea"},
    "fnb":             {"label": "F&B",       "bg": "#ffedd5", "text": "#9a3412", "border": "#ea580c"},
    "legal":           {"label": "Pháp lý",   "bg": "#fee2e2", "text": "#991b1b", "border": "#dc2626"},
    "affiliate":       {"label": "Affiliate", "bg": "#d1fae5", "text": "#065f46", "border": "#059669"},
    "economic":        {"label": "Phân tích", "bg": "#e0e7ff", "text": "#3730a3", "border": "#6366f1"},
    "market":          {"label": "Thị trường","bg": "#cffafe", "text": "#155e75", "border": "#0891b2"},
}
```

**Why Flask-side instead of CSS-only:** 7 categories × 3 color properties = 21 values that dark mode can handle via the same inline variable mechanism. No CSS class per category needed — every badge shares one `.tldr-badge` class with `style="--badge-bg:...; --badge-text:..."` set by Jinja2.

**Jinja2 template patterns for category sections:**

```jinja2
{# Group remaining articles by category using groupby filter #}
{% for group in remaining|groupby('category') %}
  {% set slug = group.grouper %}
  {% set cat_articles = group.list %}
  {% set cc = category_colors.get(slug, {}) %}

  <section class="tldr-section">
    <div class="tldr-section__header" style="--section-color:{{ cc.get('border','#6b7280') }};">
      <h2 class="tldr-section__title">
        <span class="tldr-section__badge"
              style="--badge-bg:{{ cc.get('bg','#e5e7eb') }}; --badge-text:{{ cc.get('text','#374151') }};">
          {{ cc.get('label', slug) }}
        </span>
      </h2>
    </div>
    {# ... card list ... #}
  </section>
{% endfor %}
```

**Featured hero pattern (conditional on lead_image):**

```jinja2
{% set featured = articles[0] %}
{% set remaining = articles[1:] %}

{% if featured.get('lead_image') %}
  {# Show hero card with image, title, excerpt #}
{% endif %}
{# Always show category sections from remaining #}
```

**CSS class naming convention — `tldr-*` prefix:**
- `.tldr-header` / `.tldr-nav` / `.tldr-date-nav` / `.tldr-main`
- `.tldr-section` / `.tldr-section__header` / `.tldr-section__badge`
- `.tldr-card` / `.tldr-card__title` / `.tldr-card__excerpt` / `.tldr-card__meta`
- `.tldr-badge` (shared pill badge, colors via inline `--badge-bg`/`--badge-text`)
- `.tldr-featured` / `.tldr-featured__image` / `.tldr-featured__content`
- `.tldr-article` / `.tldr-article__headline` / `.tldr-article__body`
- `.tldr-empty` / `.tldr-archive` / `.tldr-footer`

**Key pitfalls (v8):**
- **Không có lead_image → hero section bị skip hoàn toàn**, không fallback emoji. Nếu ko có `lead_image`, articles[0] chỉ xuất hiện trong category section.
- **Category không nằm trong CATEGORY_COLORS → dùng fallback gray** (`#e5e7eb` / `#374151` / `#6b7280`). Luôn `.get(slug, {})` với fallback.
- **groupby trên `articles[1:]`** (remaining), không phải tất cả articles — articles[0] là featured (kể cả khi không có image) và không xuất hiện trong category sections.
- **CSS bundle giảm từ 1678 → ~650 lines** khi chuyển từ dep.com.vn v7 sang TLDR v8 — cập nhật cả HTML lẫn CSS đồng thời.
- **Sticky header**: `.tldr-header` có `position: sticky; top: 0; z-index: 100` — chỉ hoạt động nếu parent element không có `overflow:hidden`.

### Newsletter-specific template components

Build these reusable components in `templates/components/`:
- `article-card.html` — reusable card (variant: with/without image, with/without "why it matters")
- `category-label.html` — colored badge per category (Kinh tế=blue, Công nghệ=purple, F&B=orange)
- `featured-card.html` — hero card with OG image overlay + gradient
- `why-it-matters.html` — "⚡ TẠI SAO QUAN TÂM" context box (Axios-inspired)
- `dark-mode-toggle.html` — CSS variable toggle button + localStorage persistence

## Cross-Site Design Patterns (Live Research — July 2026)

### Image Aspect Ratios

All three major news sites converge on **5:3 (1.67:1)** as the standard article thumbnail ratio:

| Context | VnExpress | NYT | Guardian |
|---|---|---|---|
| Featured | 520×312 (1.67) | ~600×360 (est.) | ~460×276 |
| Medium card | 247×148 (1.67) | ~288×173 | ~300×180 |
| Small/list | 145×87 (1.67) | — | ~174×104 |

Consistent across all: `object-fit: cover`, `border-radius: 0px`, no image hover effects.

### Navigation Sticky Behavior

| Site | Position | Height | Bg | Sub-nav |
|---|---|---|---|---|
| NYT | static | ~48px | `#fff` | Dropdown on hover |
| Guardian | static | 171px | `#052962` | Dropdown on hover |
| VnExpress | static | ~40px | `#f7f7f7` | Dropdown on hover, `border-top: 1px` |

**Key finding:** All three use `position: static` — **none** use sticky/fixed nav on the homepage.

### Hover Effects Comparison

| Site | Card Container | Link | Button |
|---|---|---|---|
| VnExpress | None | Color per category | Background fill |
| NYT | None | Color change, 0.1s ease-out | Fill `#121212` |
| Guardian | `rgba(18,18,18,0.1)` | Color change | Darken |

**Conservative hover principle:** No scale, no shadow, no dramatic transforms — only color/bg transitions.

### Best Practices Synthesis

1. **Cards: 0 border-radius** — flat design across all sites
2. **No box-shadow on cards** — flat design standard
3. **Image ratio: 5:3 (1.67:1)** for article thumbnails
4. **Subtle hover effects** — color or light bg change only
5. **Non-sticky nav** on homepage; scrolls naturally
6. **Serif headlines** (Cheltenham, Merriweather, Guardian Egyptian)
7. **Sans-serif UI** (Franklin, Arial, GuardianTextSans)
8. **CSS Grid** for responsive layouts (Guardian leads with named grid lines)
9. **Dark mode: CSS variables** with dark/light token pairs (NYT most comprehensive)
10. **Buttons: border + fill** → solid fill on hover (NYT pattern)

---\n- Hệ thống chạy tại: `http://localhost:5050`\n- Source: `~/.hermes/profiles/meow/frontend/`\n- Reports: `~/.hermes/profiles/meow/reports/`\n- **Article HTML Cleaning Pipeline** — Cách clean readability output: xoá `<html><body><div>` wrapper, classes, rel attributes, empty tags. Code pattern ở `scripts/article_scraper.py` function `clean_html()`. Full reference: `references/article-html-cleaning-pipeline.md`.\n- **TLDR 1-column digest CSS reference** (class map, token layers, key patterns, v7→v8 diff): `references/tldr-digest-css-patterns.md`
- **Live research report** (NYT, Guardian, BBC, VnExpress CSS patterns): `references/news-site-layout-patterns.md`
- **July 2026 design research** (exact tokens, buttons, spacing, hovers): `references/design-research-2026-07.md`
- **GSAP animation patterns** (core, timeline, scrolltrigger): `references/gsap-patterns.md`
- **Ponytail philosophy** (code simplicity + native features): `references/ponytail-philosophy.md`
- **dep.com.vn exact layout components** (image-box hero, 130px thumbnail, category badge, subnav scroll, 15-component analysis): `references/dep-exact-layout-components.md`
- **User workflow patterns** (plan→approve→build, anti-code-mù, subagent splitting rules, verify checklist): `references/user-workflow-patterns.md`
