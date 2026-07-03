# dep.com.vn — Master Layout Analysis

> Generated 2026-07-03 from 7 raw HTML files in `/tmp/dep_pages/`
> Page types: homepage + 4 category pages + article + magazines
> Theme: WordPress GeneratePress child theme `gp-dep` + Elementor + Bootstrap 5

## Shared Components (identical across all page types)

### HEADER
```
header.site-header.has-inline-mobile-toggle#masthead
  div.inside-header.grid-container
    div.site-logo                     ← logo 67×35px
    nav.main-navigation.mobile-menu-control-wrapper  ← hamburger + Đặt báo + search
    nav.main-navigation.has-menu-bar-items.sub-menu-right#site-navigation
      div.inside-navigation.grid-container
        div#primary-menu.main-nav
          ul#menu-main-menu.menu.sf-menu
            li.menu-item (7 items: Thời Trang, Làm Đẹp, Giải Trí, Sống, Đẹp 300, E-Magazine, Gentlemen)
    div.header-search-form            ← hidden by default, toggled via JS
```
- **Active nav:** `current-menu-item` + `aria-current="page"` on category; `current-post-ancestor` on article

### FOOTER
```
footer.site-info                      ← NOTE: NOT '.site-footer'
  div.inside-site-info.grid-container
    div.copyright-bar                 ← "© Bản quyền thuộc về tạp chí Đẹp..."
```

### SOCIAL LINKS (footer)
```
div.social-links.social-links--footer
  ul.social-links__list
    li.social-links__item.social-links__item--facebook
    li.social-links__item.social-links__item--instagram
```

## Page-Type-Specific Layouts

### HOMEPAGE
```
<body class="home ...">
[header]
[ad-float--home]                    ← floating desktop ads
[section.fullwidth-slider]          ← Swiper.js hero (image-box × N slides)
[section.post-grid] ×7              ← "Tin nổi bật", categories, etc.
[highlight-section--frontpage] ×N   ← sidebar(305px) + main grid + subnav
[footer]
```

**Key counts:** 7 post-grid sections, ~39 post-cards, 1 fullwidth slider  
**post-card variants:** `--post`, `--default`, `--highlight`  
**Grid cols:** `col-md-6 col-xxl-3` (4 cols on xxl)

### CATEGORY PAGE
```
<body class="archive category ...">
[header]
[section.hero-title--archive]       ← h1 category name
[section.subnav--archive.subnav--category]  ← sub-category links
[section.highlight-section.has-ad-slot]
  → sidebar (highlight card) + main (first grid) + ad column
[section.post-grid.post-grid--default-archive]
[pagination--default-archive]       ← [1][2][3]...[873][Tiếp theo]
[footer]
```

**Key counts:** 2 post-grid sections, ~18 post-cards  
**Hero title:** `h1.hero-title__title.mb-0.fw-normal.h3.text-uppercase`  
**Subnav:** `<li class="subnav__item px-lg-2"><a class="subnav__link"` (horizontal scrollable)  
**Pagination:** `.pagination__block > span.page-numbers.current + a.page-numbers`

### ARTICLE PAGE
```
<body class="post-template-default single single-post ...">
[header]
[section.hero-title--singular.hero-title--center]  ← article title h1
[div.top-post-meta]                   ← category link + social share buttons
[article#post-NNN.inside-article]
  [div.entry-content]                ← WordPress content
[div.bottom-post-meta]               ← author + date + social share
[section.highlight-section--singular]  ← "From the same category" (related posts)
[footer]
```

**Key counts:** 1 post-grid (related), ~12 post-cards  
**post-card variant unique:** `--small-row` (100px thumbnail, 2-line clamp title)  
**Social share:** `div.social-links.social-links--single-post` with FB + Pinterest

### MAGAZINES PAGE
```
<div class="section subnav subnav--archive" data-magazine-categories>
<div class="section post-grid" data-magazine-grid>
  div.post-grid__wrapper
    div.row.post-grid__main[data-magazine-posts]
      div.post-grid__col.col-12.col-md-6
        article.post-card.post-card--default.post-card--magazine
<div class="mt-2 pagination" data-magazine-pagination>
```

**Key differences from category:** JS-driven (`data-magazine-*`), `ratio-16x9` images, links to `magazine.dep.com.vn`, only 2 grid columns

## Component Details

### POST CARD (5 variants)
```
article.d-flex.flex-wrap.post-card.post-card--{variant}.no-cached
  a.post-card__image-link             ← 130px wide (mobile), 100% (desktop)
    figure.image.image--cover.post-card__image.ratio.ratio-1x1
      img.image__img
  div.post-card__content
    p.post-card__meta
      span.post-card__category
        a.post-card__category-link    ← border-left: 2px solid #495057
      span.post-card__date
    h3.post-card__title
      a.post-card__title-link
```
| Variant | When used | Image ratio | Special behavior |
|---------|-----------|-------------|------------------|
| `--post` | Default everywhere | 1:1 | Standard |
| `--default` | Explicit default variant | 1:1 | Same as --post |
| `--highlight` | Sidebar/sticky | 1:1 | Uppercase title, sticky on desktop |
| `--small-row` | Related posts (article) | 1:1 | 100px thumbnail, 2-line clamp |
| `--magazine` | Magazines page | 16:9 | External link target |

### FULLWIDTH SLIDER (hero)
```
div.section.fullwidth-slider
  div.js-swiper.swiper(data-settings='{"autoplay":4000,"prevNextButtons":true}')
    div.swiper-wrapper
      div.swiper-slide
        div.image-box.position-relative
          div.image-box__image-wrapper
            figure.image-box__image       ← 1348×605px (2.23:1)
            div.image-box__image-overlay  ← gradient overlay
          div.image-box__content.position-absolute
            div.image-box__content-inner  ← white bg with shadow, centered
              p.image-box__title
          a.image-box__overlay-link       ← full click area
      div.swiper-slide.is-not-loaded      ← lazy loaded
        noscript                          ← fallback img
```

### HIGHLIGHT SECTION (3 variants)
| Variant | Pages | Structure |
|---------|-------|-----------|
| `--frontpage` | Homepage | Has `.highlight-section__nav` + subnav |
| `has-ad-slot` | Category | Has `.highlight-section__col-ad` (160px) |
| `--singular` | Article | Related posts, "From the same category" title |

### SIDEBAR
```
.highlight-section__col-sidebar        ← 305px desktop, 100% mobile
  article.post-card.post-card--highlight  ← sticky on desktop (≥960px)
```

## Grid Responsiveness

| Breakpoint | Container max | Columns | Notes |
|------------|---------------|---------|-------|
| <600px | 100% | 1 | Mobile |
| 600px | 540px | 1 | sm |
| 782px | 720px | 2 | md |
| 960px | 940px | 3 | lg — sidebar appears |
| 1080px | 800px | 3 | xl |
| 1280px | 960px | 4 (homepage) | xxl |
| 1440px | 1120px | 4 | xxxl |

## Design Tokens
```css
--font-heading: 'Be Vietnam Pro', Arial, Helvetica, sans-serif;
--font-default: -apple-system, BlinkMacSystemFont, 'Segoe UI', ...;
--swiper-pagination-color: #032435;
--swiper-navigation-color: #032435;
--bs-primary: #1c2b36;
--bs-secondary: #337ab7;
--gray-text-color: #a09f9f;
--dark-gray-text-color: #333;
```

## Cross-Page Comparison

| Feature | Homepage | Category | Article | Magazines |
|---------|----------|----------|---------|-----------|
| Body class | `home` | `archive category` | `single-post` | `page-template-page-magazine` |
| Post-grid count | 7 | 2 | 1 | 1 |
| Post-card count | ~39 | ~18 | ~12 | ~10 |
| Fullwidth slider | ✅ Hero | ❌ | ❌ | ❌ |
| Hero title | ❌ | ✅ `--archive` | ✅ `--singular` | hidden |
| Subnav | `--highlight` | `--archive --category` | ❌ | `--archive` |
| Highlight section | `--frontpage` | `has-ad-slot` | `--singular` | ❌ |
| Pagination | ❌ | ✅ `--default-archive` | ❌ | ✅ JS-driven (`data-page`) |
| Top/bottom meta | ❌ | ❌ | ✅ | ❌ |
| Social share | ❌ | ❌ | ✅ `--single-post` | ❌ |
| post-card variants | 3 | 3 | 3 | 2 |
| Grid columns | `col-md-6 col-xxl-3` | `col-md-6 col-lg-4` | `col-md-6 col-lg-4` | `col-md-6` |
| Image ratio | `ratio-1x1` | `ratio-1x1` | `ratio-1x1` | `ratio-16x9` |

## Key Notes
- **Footer** uses `site-info` class (GeneratePress default), not `site-footer`
- **No `featured-image` div** — hero-title section handles it
- **No `article-wrapper`** — content is `article > .inside-article > .entry-content`
- **Menu active**: `current-menu-item` (category), `current-post-ancestor` (article)
- **Hamburger button**: `site-header__slideout-menu-button.js-open-slideout-menu`
- **Search toggle**: `site-header__search-button.js-search-button` with icon-open/icon-close swap
