# dep.com.vn — Exact Layout Analysis (Pixel-Level)

> **Source**: https://dep.com.vn/ (fetched live 2026-07-03)
> **Full file**: `~/.hermes/profiles/meow/dep-exact-layout.md` (992 lines, 29KB)
>
> This is a condensed reference. Load the full file for complete CSS values.

## Design System Overview

| Token | Value |
|-------|-------|
| Body font | Arial, Helvetive, sans-serif at 16px/24px |
| Heading font | Be Vietnam Pro (Google Font) |
| Body text | `#222222` (--contrast) |
| Accent hover | `#337ab7` (--bs-secondary) — ALL interactive elements |
| Borders | `#dee2e6` (--bs-gray-300) |
| Page bg | `#f7f8f9` (--base-2) |
| Container max | 1180px (--container-max-xxl) |
| Navigation font | 13px, 700 weight, 1px letter-spacing, uppercase |

## 15 Components (Summary)

1. **Header**: White bg, logo 67×35px, nav right, 0.5em padding
2. **Hamburger**: 36×36px button, 24×24px icon, hover `#337ab7`
3. **Search**: Absolute dropdown, `#f8f9fa` bg, box-shadow layered
4. **Main Nav**: `font-size: 13px`, `font-weight: 700`, `letter-spacing: 1px`, uppercase
5. **Hero Slider**: 1348×605px images (2.23:1), gradient overlay, 80% white text box
6. **Post Card**: Square 1:1 images (385×385px), hover scale(1.05), 0.4s ease
7. **Category Badge**: 2px solid left border `#495057`, 10px padding-left, 12px/uppercase
8. **Section Title**: Be Vietnam Pro, centered, h3 size
9. **Subnav**: Horizontal scroll, uppercase links, border-top/bottom `#dee2e6`
10. **Gallery**: 2:3 portrait images, content overlaps bottom, shadow
11. **Footer**: White bg, 13px text, 0.75 opacity, 2em padding
12. **Highlight Section**: Sidebar 305px + main calc(100% - 305px)
13. **Slideout**: 300px, right-side, 0.5s translateX, shadow layered
14. **Social Links**: 24×24px icons, hover translateY(-3px), 0.4s
15. **Đặt báo**: Plain text link in header bar

## Key Design Patterns

### All Hover Effects (unified `color .4s ease`)
| Element | Normal | Hover |
|---------|--------|-------|
| `.post-card__category-link` | `#222222` | `#337ab7` |
| `.post-card__title-link` | `#222222` | `#337ab7` |
| `.subnav__link` | `#222222` | `#337ab7` |
| `.slideout-menu__menu li a` | `#222222` | `#337ab7` |
| `.site-header__search-button` | `#222222` | `#337ab7` |
| `.post-card__image img` | scale(1) | **scale(1.05)** — all `.4s ease` |

### Shadow System
| Usage | Shadow value |
|-------|-------------|
| Hero text box | `0 3px 8px rgba(0,0,0,.24)` |
| Gallery content | `0 3px 8px rgba(0,0,0,.24)` |
| Post grid (border) | `0 4px 12px rgba(0,0,0,.1)` |
| Slideout panel | `0 1px 2px 0 rgba(60,64,67,.3), 0 2px 6px 2px rgba(60,64,67,.15)` |
| Search form | `0 10px 15px -3px rgba(0,0,0,.1), 0 4px 6px -2px rgba(0,0,0,.05)` |

### Border System
| Location | Width | Color |
|----------|-------|-------|
| Category badge (left) | 2px | `#495057` |
| Subnav (top/bottom) | 1px | `#dee2e6` |
| Gallery category (left/right) | 1px | `#212529` |

### Responsive Breakpoints
| Breakpoint | Change |
|------------|--------|
| >= 1280px | Post grid: 4 columns |
| >= 960px | Post grid: 2→3 cols; Hero text bottom: 2em; Highlight: sidebar + main |
| >= 768px | Post grid: 2 columns; Subnav overflow auto |
| >= 600px | Wide containers |
| < 768px | Post grid: 1 column; Hero: no overlay box, white text |

### Image Aspect Ratios
| Context | Ratio | Pixels |
|---------|-------|--------|
| Hero slider | 2.23:1 | 1348×605 |
| Post card | 1:1 | 385×385 |
| Gallery | 2:3 | 150% padding-top |
| Video | 16:9 | — |

## How This Was Extracted

WordPress inline CSS blocks (24 blocks, 442KB HTML):
- Block 14 (99KB) — Bootstrap 5 custom theme
- Block 15 (39KB) — Swiper + **all component CSS** (target block)
- Block 7 (8KB) — GeneratePress theme
- Block 20 (4KB) — WP custom CSS

**Tool used**: curl + Python regex → manual extraction of component classes from HTML → matching with CSS in inline style blocks.

For full methodology, see the "Deep CSS Layout Analysis" section in the website-cloner SKILL.md.
