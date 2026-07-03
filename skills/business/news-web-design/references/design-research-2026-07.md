# News Site Design Research — July 2026

> Live browser inspection (JS console, computed styles, stylesheet enumeration) of VnExpress, NYT, and The Guardian.
> BBC was unreachable (DNS resolution failure).
> 28 components documented across 3 sites.

## Key Findings Summary

| Pattern | VnExpress | NYT | Guardian |
|---------|-----------|-----|----------|
| Border-radius | 0px (all) | 0px (all) | 0px (all) |
| Card box-shadow | None | None | None |
| Nav position | static | static | static |
| Image ratio | 5:3 | 5:3 (~) | 5:3 (~) |
| Hover intensity | Color per category | Subtle color | Light bg + color |
| Headline font | Merriweather | nyt-cheltenham | GH Guardian Headline |
| Body font | Arial | nyt-imperial | Guardian Egyptian |
| UI font | Arial | nyt-franklin | GuardianTextSans |

**Cardinal rule:** flat design, subtle interactions, serif headlines, sans-serif UI.

## 1. Color Palettes

### 1.1 VnExpress — Exact Colors

| Role | Color |
|---|---|
| Body background | `#ffffff` |
| Section bg (featured card) | `rgb(247, 247, 247)` |
| Dark footer bg | `rgb(32, 33, 36)` |
| Text primary | `#222222` |
| Text secondary | `rgb(117, 117, 117)` |
| Text muted | `rgb(79, 79, 79)` / `rgb(154, 160, 166)` |
| Link blue | `rgb(7, 109, 182)` |
| Brand accent | `rgb(180, 38, 82)` / `#b42652` |
| Nav link | `rgb(79, 79, 79)` |
| Nav bg | `rgb(247, 247, 247)` |
| Footer text | `rgb(143, 143, 143)` |
| Border/divider | `rgb(229, 229, 229)` |

### 1.2 VnExpress — Category Hover Colors

```css
.kinhdoanh:hover a → color: rgb(6, 94, 157)     /* Business: blue */
.giaitri:hover a    → color: rgb(236, 50, 107)    /* Entertainment: pink */
.thethao:hover a    → color: rgb(95, 174, 46)     /* Sports: green */
.phapluat:hover a   → color: rgb(146, 58, 60)    /* Law: maroon */
.giaoduc:hover a    → color: rgb(235, 118, 0)    /* Education: orange */
.suckhoe:hover a    → color: rgb(4, 155, 147)    /* Health: teal */
.doisong:hover a    → color: rgb(48, 159, 192)   /* Lifestyle: cyan */
.dulich:hover a     → color: rgb(0, 131, 214)    /* Travel: bright blue */
.khoahoc:hover a    → color: rgb(173, 150, 52)   /* Science: olive */
.xe:hover a         → color: rgb(131, 146, 160)  /* Cars: gray */
```

### 1.3 NYT — Color Token System (50+ tokens)

| Token | Light | Dark |
|---|---|---|
| `--color-background-primary` | `#ffffff` | `#121212` |
| `--color-background-secondary` | `#f8f8f8` | `#2a2a2a` |
| `--color-content-primary` | `#121212` | `#f8f8f8` |
| `--color-content-secondary` | `#363636` | `#dfdfdf` |
| `--color-content-tertiary` | `#5a5a5a` | `#bbb` |
| `--color-signal-editorial` | `#326891` | `#6ba1dd` |
| `--color-signal-negative` | `#a90111` | `#ea7980` |
| `--color-signal-positive` | `#267c30` | `#63a859` |
| `--color-stroke-primary` | `#121212` | `#f8f8f8` |

**Design principle:** 5-tier background (primary→secondary→tertiary→overlay→scrim) + 5-tier content (primary→quintary).

## 2. Typography

### 2.1 NYT — Full Scale (inspected live)

| Token | Size | Weight | Font | Use |
|---|---|---|---|---|
| headline-news-48 | 48px | 700 | nyt-cheltenham | Breaking news |
| headline-news-40 | 40px | 700 | nyt-cheltenham | Lead story |
| headline-news-28 | 28px | 700 | nyt-cheltenham | Section lead |
| headline-news-20 | 20px | 700 | nyt-cheltenham | Card headline |
| body-regular | 20px / 1.5 | 400 | nyt-imperial | Article body |
| body-16 | 16px / 1.39 | 400 | nyt-imperial | Compact body |
| text-16 | 16px | 500 | nyt-franklin | UI text |
| label-emphasis | 11px | 800 | nyt-franklin | Section labels |
| story-list-headline | 22px | 500 | nyt-cheltenham | List headlines |

**3-font system:** nyt-cheltenham (headlines, serif), nyt-imperial (body, serif), nyt-franklin (UI, sans-serif).

### 2.2 VnExpress — Computed

| Element | Size | Weight | Line Ht | Font | Color |
|---|---|---|---|---|---|
| h1 | 24px | 400 | 30px | Arial | `#9aa0a6` |
| h3 (featured) | 20px | 700 | 32px | Merriweather | `#222` |
| h3 (sub) | 15px | 700 | 24px | Merriweather | `#222` |
| Body | 15px | 400 | 24px | Arial | `#222` |
| Description | 14px | 400 | 19.6px | Arial | `#4f4f4f` |
| Meta | 12-13px | 400 | — | Arial | `#757575` |

## 3. 28 Components Documented

### VnExpress (9)
1. **Featured Article Card**: 780×300px, flex layout, bg #f7f7f7, hover: link color change
2. **Sub-item Card**: 247×228px, grid gap 20px, no border
3. **List Card**: 380px, padding 12px top, border-bottom separation
4. **Navigation Bar**: height ~40px, bg #f7f7f7, static position
5. **Image Thumbnail**: 5:3 aspect ratio, object-fit cover, 0 radius
6. **Headline h3**: Merriweather 20px/32px bold, color #222
7. **Category Nav**: per-category hover colors (see §1.2)
8. **Header/Top Bar**: date + stock tickers, not sticky
9. **Footer**: dark bg #202124, text #8f8f8f

### NYT (10)
1. **Story Card (.story-wrapper)**: flex-column, no border, no shadow
2. **Primary Navigation (.css-1l3wkyj)**: franklin 11px, uppercase, static
3. **Section Nav**: uppercase labels, border-right separators
4. **Section Header**: section title + "More in..." link
5. **Headline Link**: #121212, hover → editorial blue
6. **Byline/Meta**: nyt-franklin 11px, weight 600, color #5a5a5a
7. **Standard Button**: border + fill → hover: solid dark bg
8. **Emphatic Button**: solid dark → hover: opacity 0.8
9. **Masthead/Top Bar**: date + stocks, nyt-franklin 11px
10. **Story Image**: aspect-ratio 5/3, no hover effects

### Guardian (9)
1. **Featured Card (.dcr-1ozbgom)**: absolute link overlay pattern
2. **Masthead Navigation**: bg #052962, brand-centered
3. **Card Headline (.dcr-10xs001)**: GH Guardian Headline 1.0625rem/1.15
4. **Image Container (.dcr-1i0w7lt)**: aspect-ratio container
5. **Utility Top Bar**: bg #041F4A, small utility links
6. **Highlights Carousel**: horizontal scroll section
7. **Primary Button (.dcr-d6dwh4)**: bg #052962 → hover: darker
8. **Section Container (.dcr-1n2m5rc)**: grid with named lines
9. **Kicker/Label (.dcr-kick)**: uppercase 12px, underscores topics

## 4. Guardian Named-Line Grid System

```css
.dcr-lypmm { display: grid; grid-auto-rows: auto; column-gap: 10px; }

/* mobile */
@media (max-width: 739px) {
  grid-template-columns: [viewport-start] 0px
    [content-start main-column-start] repeat(4, minmax(0px, 1fr))
    [content-end main-column-end] 0px [viewport-end];
}

/* tablet */  @media (min-width: 740px) { repeat(12, 40px) }
/* desktop */ @media (min-width: 980px) { repeat(12, 60px) }

/* Placement */
.article-card--full    { grid-column: content-start / content-end; }
.article-card--main    { grid-column: content-start / main-column-end; }
.article-card--sidebar { grid-column: main-column-end / content-end; }
```

**Container widths:** 740px → 980px → 1140px → 1300px

## 5. Button States

### NYT Standard Button
- Normal: bg #fff, border 1px #121212, 44px height
- Hover: bg #121212, color #f8f8f8
- Pressed: bg #121212, opacity 0.8

### NYT Emphatic
- Normal: bg #121212, color #f8f8f8
- Hover: opacity 0.8

## 6. Hover Effects Comparison

| Site | Card | Headline | Link | Button |
|---|---|---|---|---|
| VnExpress | None | Color | Per-category color | Fill |
| NYT | None | Color (0.1s) | Color | Fill dark |
| Guardian | `rgba(18,18,18,0.1)` | Inherit | Color | Darken |

**Pattern:** Extremely conservative — no scale, shadow, or transforms.

## 7. Responsive Breakpoints

| Site | Desktop | Tablet | Mobile |
|---|---|---|---|
| VnExpress | >979px | — | <979px (full width) |
| NYT | 1605px container | Fluid flex | 1 column |
| Guardian | 740/980/1140/1300 | Named grid | 4→1 |

## 8. Design Research Files

Full raw research (622 lines, all 28 components with selectors, states, responsive):
- `~/.hermes/profiles/meow/design-research.md`

Additional live-inspected data:
- `references/news-site-layout-patterns.md` — Guardian/VnExpress layout specifics
- `references/nyt-design-system.md` — NYT token system details
- `references/micro-interactions.md` — Transition timing details
