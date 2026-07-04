# The Guardian Layout Research

> Researched via Playwright on https://www.theguardian.com/international and a live article page.
> Date: 2026-07-04

---

## 1. Grid System

The Guardian uses a CSS Grid layout with named grid lines. Two primary grid containers power the site:

### Front Page Grid (`.dcr-lypmm` grid)

| Breakpoint | Grid Template Columns |
|---|---|
| < 740px (mobile) | `[viewport-start] 0px [content-start main-column-start] repeat(4, minmax(0px, 1fr)) [content-end main-column-end] 0px [viewport-end]` |
| ≥ 740px (tablet) | `[viewport-start] minmax(0px, 1fr) [content-start main-column-start] repeat(12, 40px) [content-end main-column-end] minmax(0px, 1fr) [viewport-end]` |
| ≥ 980px (desktop) | `[viewport-start] minmax(0px, 1fr) [content-start main-column-start] repeat(12, 60px) [content-end main-column-end] minmax(0px, 1fr) [viewport-end]` |
| ≥ 1140px (wide) | `[viewport-start] minmax(0px, 1fr) [content-start left-column-start] repeat(2, 60px) [left-column-end main-column-start] repeat(12, 60px) [content-end main-column-end] minmax(0px, 1fr) [viewport-end]` |
| ≥ 1300px (max) | `[viewport-start] minmax(0px, 1fr) [content-start left-column-start] repeat(3, 60px) [left-column-end main-column-start] repeat(12, 60px) [main-column-end] repeat(1, 60px) [content-end] minmax(0px, 1fr) [viewport-end]` |

- **Column gap**: `20px` (≥480px), `10px` (<480px)
- **Grid auto-rows**: `auto`

### Article Page Grid (`.dcr-hnbs0y` grid)

Actually measured at 1300px viewport:
```
[grid-start] 62.5px [left-column-start] 60px 60px [left-column-end centre-column-start]
60px 60px 60px 60px 60px 60px 60px 60px [centre-column-end right-column-start]
60px 60px 60px 60px [right-column-end] 62.5px [grid-end]
```
- 16 columns of 60px each = 960px + 62.5px gutters × 2 = 1085... actually the grid measures 1265px total width
- Column gap: `20px`
- Named zones:
  - `left-column`: 2 cols (120px) — at 1140px+
  - `centre-column`: 8 cols (480px) — main article content
  - `right-column`: 4 cols (240px) — sidebar

### Highlights Container Grid (`.dcr-22655`)

Used for the "Highlights" / "Headlines" carousel section.

| Breakpoint | Columns |
|---|---|
| < 740px | `[decoration-start] 0px [content-start title-start] repeat(3, minmax(0px, 1fr)) [hide-start] minmax(0px, 1fr) [content-end title-end hide-end] 0px [decoration-end]` |
| ≥ 740px | `minmax(0px, 1fr) [decoration-start content-start title-start] repeat(11, 40px) [hide-start] 40px [decoration-end content-end title-end hide-end] minmax(0px, 1fr)` |
| ≥ 980px | `minmax(0px, 1fr) [decoration-start content-start title-start] repeat(11, 60px) [hide-start] 60px [decoration-end content-end title-end hide-end] minmax(0px, 1fr)` |
| ≥ 1140px | `minmax(0px, 1fr) [decoration-start title-start] repeat(2, 60px) [title-end content-start] repeat(11, 60px) [hide-start] 60px [decoration-end hide-end content-end] minmax(0px, 1fr)` |
| ≥ 1300px | `minmax(0px, 1fr) [decoration-start title-start] repeat(3, 60px) [title-end content-start] repeat(12, 60px) [content-end hide-start] 60px [decoration-end hide-end] minmax(0px, 1fr)` |

- Column gap: `10px` (<480px), `20px` (≥480px)
- Grid rows: `[headline-start controls-start] auto [controls-end headline-end content-toggleable-start content-start] auto [content-end content-toggleable-end bottom-content-start] auto [bottom-content-end]`

### Content Container Max-Widths

Class `.dcr-1un8ko5`:
- ≥ 740px: max-width 740px
- ≥ 980px: max-width 980px
- ≥ 1140px: max-width 1140px
- ≥ 1300px: max-width 1300px

---

## 2. Typography

### Font Families

| Font Name | CSS Name | Used For |
|---|---|---|
| **GH Guardian Headline** | `"GH Guardian Headline", "Guardian Egyptian Web", Georgia, serif` | Headlines, article titles, section headings |
| **Guardian Text Egyptian** | `GuardianTextEgyptian, "Guardian Text Egyptian Web", Georgia, serif` | Body text, article copy |
| **Guardian Text Sans** | `GuardianTextSans, "Guardian Text Sans Web", "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif` | Navigation, meta info, card trail, timestamps |

### Headline Weights

- `font-weight: 300` — Light
- `font-weight: 400` — Regular (from `GHGuardianHeadline-Regular.woff2`)
- `font-weight: 500` — Medium
- `font-weight: 700` — Bold

### Specific Styles

| Element | Font | Size | Weight | Line-Height | Color |
|---|---|---|---|---|---|
| **Article h1 headline** | GH Guardian Headline | 34px | 500 | 39.1px (1.15) | #8B0000 (dark red) |
| **Section h2 headline** | GH Guardian Headline | 24px | 700 | 27.6px (1.15) | #121212 |
| **Standfirst** | GH Guardian Headline | 20px | 500 | 23px (1.15) | #000000 |
| **Body paragraph** | GuardianTextEgyptian | 17px | 400 | 23.8px (1.4) | #121212 |
| **Byline link** | GH Guardian Headline | 17px | 700 | 19.55px (1.15) | #C70000 |
| **Nav link (desktop)** | GuardianTextSans | 17px (1.0625rem) | 700 | 1.3 | var(--masthead-nav-link-text) |
| **Nav link (sub)** | GuardianTextSans | 14px (0.875rem) | 400 | 1.3 | var(--masthead-nav-link-text) |
| **Card trail text** | GuardianTextSans | 14px (0.875rem) | 400 | 1.3 | #707070 |
| **Card kicker** | GuardianTextSans | 15px (0.9375rem) | 400 | 1 | var(--highlights-card-kicker-text) |
| **Card headline** | GH Guardian Headline | 17px (1.0625rem) | 500 | 1.15 | var(--highlights-card-headline) |
| **Timestamp** | GuardianTextSans | 12px (0.75rem) | 700 | 1.3 | — |
| **Section headline pill** | GuardianTextSans | 12px (0.75rem) | 700 | 1.3 | var(--pill-text) |

### Font Size Scale (rem)

| Size | rem | px (approx) |
|---|---|---|
| 0.75rem | 0.75 | 12px |
| 0.875rem | 0.875 | 14px |
| 0.9375rem | 0.9375 | 15px |
| 1rem | 1 | 16px |
| 1.0625rem | 1.0625 | 17px |
| 1.25rem | 1.25 | 20px |
| 1.5rem | 1.5 | 24px |
| 1.75rem | 1.75 | 28px |

---

## 3. Colors

### Brand & Primary

| Token | Color | Usage |
|---|---|---|
| `--masthead-nav-background` | `#052962` | Dark blue — main navigation bar |
| `--masthead-top-bar-background` | `#041F4A` | Darker blue — top bar (jobs, sign in) |
| `--button-background-primary` | `#052962` | Dark blue — primary buttons |
| `--byline` / `--byline-anchor` | `#C70000` | Guardian red — bylines, links |
| `--byline-background` | `#FFE500` | Yellow — byline highlight |
| **Section headline color** | `#8B0000` | Dark red — headline colour |
| **Accent #005689** | `#005689` | Medium blue — cricket scoreboard borders, football |

### Pillar Colors

| Pillar | Color |
|---|---|
| News (section title) | `#121212` |
| Opinion | `#C74600` |
| Sport | `#0077B6` |
| Culture | `#866D50` |
| Lifestyle | `#BB3B80` |

### Card Colors

| Token | Color |
|---|---|
| `--card-headline` | `#121212` |
| `--card-kicker-text` | `#C70000` |
| `--card-trail-text` | `#707070` (grey) |
| `--card-background` | `transparent` |
| `--card-border-top` | `#BABABA` |
| `--card-border-supporting` | `#DCDCDC` |
| `--highlights-card-background` | `#FFF4F2` |
| `--highlights-card-headline` | `#C70000` |
| `--highlights-card-kicker-text` | `#121212` |
| `--highlights-container-separator` | `#DCDCDC` |

### Text & Surfaces

| Token | Color |
|---|---|
| `--article-text` / `--card-headline` | `#121212` (near-black) |
| `--article-background` | `#FFFFFF` |
| `--front-page-background` | `#FFFFFF` |
| `--article-border` / divider | `#DCDCDC` |
| `--headline-colour` | `#8B0000` |
| `--card-footer-text` / `--card-trail-text` | `#707070` |
| `--masthead-nav-link-text` | `#FFFFFF` |
| `--masthead-nav-link-text-hover` | `#FFE500` |
| `--nav-reader-revenue-link-text` | `#FFE500` |
| `--masthead-top-bar-link-text` | `#FFFFFF` |
| `--masthead-veggie-burger-background` | `#FFE500` |
| `--masthead-veggie-burger-icon` | `#052962` |
| `--pill-background` | `rgba(18, 18, 18, 0.7)` |
| `--pill-text` | `#FFFFFF` |

---

## 4. Navigation

### Top Bar
- Items: "Print subscriptions", "Search jobs", "Sign in"
- Background: `#041F4A` (--masthead-top-bar-background)
- Link text: White
- Font: GuardianTextSans, 17px (1.0625rem), weight 700

### Edition Selector
- Button: "Int" (International edition active)
- Dropdown: UK, US, Australia, Europe editions
- Active item: bold weight, uses `.dcr-uubqks`
- Inactive: regular weight, uses `.dcr-1rdl5s8`

### Main Navigation
| Link | Path |
|---|---|
| News | `/` |
| Opinion | `/commentisfree` |
| Sport | `/sport` |
| Culture | `/culture` |
| Lifestyle | `/lifeandstyle` |

- Background: `#052962` (--masthead-nav-background)
- Font: GH Guardian Headline, responsive sizes (0.875rem → 1.5rem)
- Active pillar has underline accent (varies per pillar via --pillar-underline)

### Sub-navigation (under "Show more")
| Link | Path |
|---|---|
| World | `/world` |
| World Cup 2026 | `/football/world-cup-2026` |
| US politics | `/us-news/us-politics` |
| UK news | `/uk-news` |
| Climate crisis | `/environment/climate-crisis` |
| Middle East | `/world/middleeast` |
| Ukraine | `/world/ukraine` |
| Environment | `/environment` |
| Science | `/science` |
| Global development | `/global-development` |
| Football | `/football` |
| Tech | `/technology` |
| Business | `/business` |
| Obituaries | `/obituaries` |

### Mobile Menu (Slide-out)
- `position: fixed`, full-screen on small viewports
- Max-height: calc(100% - 50px)
- Left: 0, Right: 0
- Z-index: 37
- Navigation items: GH Guardian Headline, 1.5rem, weight 700

---

## 5. Cards

### Highlights Card (`.dcr-bpr716`)

This is the card used in the carousel at the top of the page.

| Property | Value |
|---|---|
| Display | `flex` |
| Flex direction | `column` (<740px), `row` (≥740px) |
| Padding | `8px 8px 0px` (<740px), `10px 10px 0px` (≥740px) |
| Background | `var(--highlights-card-background)` = `#FFF4F2` (off-white/pink tint) |
| Min-height | `174px` (<375px), `194px` (375-740px) |
| Width | `160px` (740px), `280px` (740px+ row), `300px` (980px) |
| Column-gap | `8px` |
| Justify-content | `space-between` |
| Word-break | `break-word` |

### Card Headline (`.dcr-10xs001`)

| Breakpoint | Font | Size | Weight |
|---|---|---|---|
| < 740px | GH Guardian Headline | 0.9375rem (15px) | 500 |
| 375-740px | GH Guardian Headline | 1.0625rem (17px) | 500 |
| ≥ 740px | GH Guardian Headline | 1.0625rem (17px) | 500 |
| ≥ 980px | GH Guardian Headline | 1.0625rem (17px) | 500 |

---

## 6. Article Layout

### Article Page Structure

Measured at 1300px viewport width:

| Component | Width | Notes |
|---|---|---|
| Overall grid container | 1265px | `.dcr-hnbs0y` |
| Left gutter | 62.5px | |
| Left column (2 cols) | 120px | 2 × 60px — appears at 1140px+ |
| Centre column | 480px (8 cols) | Main content — headline, text |
| Right column | 240px (4 cols) | Sidebar — right-column |
| Right gutter | 62.5px | |
| Column gap | 20px | |

Actual content width measurements:
- **Headline (h1) area**: 620px wide
- **Article body text**: 620px wide container, paragraphs 540px wide
- **Standfirst**: 540px wide
- **Side metas**: 140px wide (aside elements)
- **Key facts / rich content**: 300px wide
- **Figure / images**: 620px wide

### Article Typography Detail

| Element | Font | Size | Weight | Line-Height | Color |
|---|---|---|---|---|---|
| **Kicker/label** (`content__label__link`) | GH Guardian Headline | 17px | 700 | 19.55px | #C70000 |
| **Article h1** | GH Guardian Headline | 34px | 500 | 39.1px (1.15) | #8B0000 |
| **Standfirst** (first p) | GH Guardian Headline | 20px | 500 | 23px (1.15) | #000000 |
| **Body text** (p) | GuardianTextEgyptian | 17px | 400 | 23.8px (1.4) | #121212 |

### Article Spacing

- Margins between article children: 0px (grid handles spacing)
- Padding: varied per component, h1 gets `4px 0px 0px`
- Image captions use `GuardianTextSans`, ~14px

---

## 7. Spacing

### Layout Spacing

| Context | Value |
|---|---|
| Content padding (mobile, body) | `0px 12px` |
| Content padding (tablet+) | `0px 20px` |
| Section padding Y | `8px 0px 12px` |
| Section padding (tablet) | `8px 20px` |
| Column gap (grid) | `10px` (<480px), `20px` (≥480px) |
| Row gap (various) | `10px`, `8px` |
| Card gap | `8px` (column) |
| Card padding | `8px` / `10px` |
| Margin-top for nav items | `4px` |
| Margin-bottom for section headings | `0px` |

### Container Max-Widths

| Breakpoint | Max-width |
|---|---|
| 740px | 700px (content) |
| 980px | 940px (content) |
| 1140px | 1100px (content) |
| 1300px | 1260px (content) |

---

## 8. Responsive Breakpoints

The Guardian uses these breakpoints (in pixels):

| Name | Min-width | Column width | Notes |
|---|---|---|---|
| **Mobile** | `375px` | fluid | Larger phones |
| **MobileLand** | `480px` | fluid | Landscape phones, column-gap changes to 20px |
| **Tablet** | `740px` | 40px | Grid columns become fixed width |
| **Desktop** | `980px` | 60px | Column width increases to 60px |
| **LeftCol** | `1140px` | 60px | Left sidebar column appears |
| **Wide** | `1300px` | 60px | Full layout with right sidebar |

Also used:
- `max-width: 374.9px` — small phones
- `max-width: 739.9px` — phones (non-tablet)
- `max-width: 979.9px` — tablets (non-desktop)
- `max-width: 1139.9px` — desktop without left column
- `max-width: 1299.9px` — wide without extras

### Key Responsive Behaviors

1. **Grid**: 4 cols (fluid) → 12 cols + gutters → 12 cols + left col → 12 cols + left col + right col
2. **Navigation**: Horizontal on desktop, sliding drawer on mobile
3. **Card layout**: Single column → multi-column at 740px+
4. **Highlights carousel**: Horizontal scroll on all sizes, sticky scroll-padding increases at larger breakpoints
5. **Section titles**: Font sizes increase at each breakpoint

---

## CSS Custom Properties (Design Tokens)

Over 250 CSS custom properties define the Guardian design system. Key categories:
- `--article-*` — Article page surfaces, text, borders
- `--card-*` — Card backgrounds, text, kicker, headline, borders
- `--masthead-*` — Navigation bar backgrounds, link colors
- `--highlights-*` — Highlight carousel cards
- `--discussion-*` — Comments section
- `--football-*` — Football/sports widgets
- `--pill-*` — Section label pills
- `--ad-*` — Advertisement containers
- `--button-*` — Button states

### Notable Design Tokens Not Already Listed

| Token | Value |
|---|---|
| `--article-link-text` | `#C70000` |
| `--article-link-border-hover` | `#C70000` |
| `--drop-cap` | `#8B0000` |
| `--headline-background` | `transparent` |
| `--headline-byline` | `inherit` |
| `--headline-match-colour` | `#C70000` |
| `--byline-hover` | `#AB0613` |
| `--pullquote-text` | `#121212` |
| `--pullquote-icon` | `#999999` |
| `--block-quote-text` | `#121212` |
| `--block-quote-link` | `#C70000` |
| `--key-event-bullet` | `#AB0613` |
| `--live-block-border-top` | `#C70000` |
