# dep.com.vn Clone Reference — Design Tokens & Component Specs

> Extracted 03-07-2026 từ 7 pages (3MB HTML)

## Color System

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| `--accent` | `#032435` | `#4a9eff` | Primary brand, links, CTAs |
| `--contrast` | `#222222` | `#e8e8f0` | Body text |
| `--contrast-2` | `#575760` | `#9898b8` | Secondary text |
| `--contrast-3` | `#b2b2be` | `#6868a0` | Muted text |
| `--bg` | `#ffffff` | `#0d1929` | Page background |
| `--bg-warm` | `#f7f8f9` | `#0b1116` | Section background |
| `--bg-card` | `#ffffff` | `#152029` | Card background |
| `--border` | `#dee2e6` | `#2a3a4a` | Borders, separators |
| `--badge-border` | `#495057` | `#6868a0` | Category badge border-left |

## Typography

| Level | Size | Weight | Line Height | Font |
|-------|------|--------|-------------|------|
| Display | 48px | 700 | 1.0-1.1 | Be Vietnam Pro |
| Heading 1 | 36px | 700 | 1.75 | Be Vietnam Pro |
| Heading 2 | 24px | 700 | 1.3 | Be Vietnam Pro |
| Heading 3 | 20px | 600 | 1.3 | Be Vietnam Pro |
| Body | 16px (1rem) | 400 | 1.5 | system-ui |
| Caption | 13px (0.85rem) | 400 | 1.4 | system-ui |
| Micro | 11px | 400 | 1.3 | system-ui |
| Nav | 13px | 700 | 1.6 | Be Vietnam Pro (uppercase, 1px letter-spacing) |
| Meta | 0.85rem | 400 | 1.4 | system-ui (opacity .5) |

## Spacing (4px Base Grid)

| Token | px | Used For |
|-------|-----|----------|
| `--space-1` | 4 | Atom padding, tight spacing |
| `--space-2` | 8 | Between group items, nav padding |
| `--space-4` | 16 | Between groups, card padding |
| `--space-6` | 24 | Between sections |
| `--space-8` | 32 | Page margins |
| `--space-12` | 48 | Large sections |
| `--space-16` | 64 | Page margins (desktop) |

## Container Widths

| Breakpoint | Max Width |
|-----------|-----------|
| Mobile | 100% (20px padding) |
| Tablet (768px) | 100% |
| Desktop (960px) | 1040px |
| Wide (1280px) | 1180px |

## Component Specs

### Header (`.site-header`)
- Padding: 0.5em top/bottom
- Logo: img 67x35px
- Nav items: 13px, 700 weight, uppercase, 1px letter-spacing, padding 8px 12px
- Active: color change on hover (0.4s ease)

### Hero Slider (`.image-box`)
- Image: 1348x605px (5:3 aspect ratio)
- Gradient overlay: `linear-gradient(180deg, rgba(85,85,85,0), #000)` 25% height
- Text box: `hsla(0,0%,100%,.8)` background, box-shadow `0 3px 8px rgba(0,0,0,.24)`
- Title: uppercase, line-height 2, font-size h5
- Link: absolute overlay (`.image-box__overlay-link`)

### Post Card (`.post-card`)
- Border-bottom: 1px `rgba(0,0,0,.15)`
- Image: 130px width (thumbnail) on mobile, 100% on desktop
- Image hover: `scale(1.05)` transition 0.4s ease
- Category badge: `border-left: 2px solid #495057`, padding-left: 10px
- Title: 1rem (16px), bold
- Meta: 0.85rem, opacity 0.5
- Spacing: padding-left 1em (thumbnail layout)

### Subnav (`.subnav__list`)
- Display: flex, nowrap
- Overflow-x: auto/scroll
- White-space: nowrap
- Border-top + border-bottom: 1px solid `#dee2e6`
- Link padding: 0.5em 1em
- Active: font-weight 500

### Footer (`.inside-site-info`)
- Font-size: 13px
- Opacity: 0.75
- Text-align: left
- Padding: 2em 20px

### Article Page
- Headline: 32px → 36px (768px+), line-height 1.75
- Featured image: full-width, height 450px, object-fit cover
- Body: 1rem, line-height 24px
- Content width: 680px

## Responsive Breakpoints

| Name | Min Width | Layout Changes |
|------|-----------|----------------|
| xs | 0 | Single column, 20px gutter |
| sm | 600px | 2 columns |
| md | 782px | Subnav visible |
| lg | 960px | 3-4 columns |
| xl | 1080px | Full width 1040px |
| xxl | 1280px | Wide 1180px |

## Hover Effects
- Nav links: color transition 0.4s ease
- Post card images: transform scale(1.05) 0.4s ease
- Social links: translateY(-3px) 0.4s ease
- Category links: color transition 0.4s ease
- Video thumbnails: image scale(1.1) 0.4s ease
