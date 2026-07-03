# dep.com.vn Full Template Restructure (July 2026)

## Context
Complete rewrite of Phương's Daily frontend from NYT-style to dep.com.vn layout.
Scope: base.html, index.html, article.html, refresh.html, style.css.

## Source Analysis
- URL: https://dep.com.vn/
- Browser: 403 (NinjaFirewall) → used curl with desktop UA
- CMS: WordPress + Bootstrap + custom gp-dep theme
- Font: Be Vietnam Pro (already matched)
- Convention: BEM with `--`, WordPress block classes, Bootstrap utilities

## Old → New Class Mapping

| Old (NYT-style) | New (dep.com.vn BEM) | Notes |
|---|---|---|
| `.utility-bar` | _(removed)_ | Absorbed into `.inside-header` + `.menu-bar-items` |
| `.newspaper-header` / `.newspaper-name` | `.site-header` / `.header-logo__text` | Logo left + nav right |
| `.section-nav` / `.-inner` / `.-item` | `.subnav` / `.__inner` / `.__link` | Horizontal scrollable, uppercase, border-right separators |
| `.date-nav` / `.-inner` / `.-btn` / `.-current` / `.-today` | `.date-nav` / `.__inner` / `.__arrow` / `.__current` / `.__today` | Cleaner, simplified |
| `.news-featured.featured-card` | `.image-box` | Full-width bg image, gradient overlay, centered text box |
| `.featured-visual` | `.image-box__image` | Background image on wrapper |
| `.card-badge` | `.post-card__category-link` | `border-left: 2px solid var(--accent)` |
| `.card-title` | `.post-card__title` / `.image-box__title` | Heading within card/hero |
| `.card-excerpt` | `.post-card__excerpt` / `.image-box__excerpt` | Secondary text |
| `.card-meta` | `.post-card__meta` / `.image-box__meta` | Date + tags row |
| `.card-tags` / `.card-tag` | `.post-card__tags` / `.post-card__tag` | Tag chips |
| `.news-grid` / `.-grid-col` | `.post-grid` / `.__row` / `.__col` | CSS Grid (1/2/3 cols responsive) |
| `.article-card` | `.post-card` | Square image + content column |
| `.search-area` / `.search-form` / `.search-input` / `.search-btn` | `.header-search-form-compact` / `.search-field-compact` / `.search-submit-compact` | Inline in header bar |
| `.newspaper-sub` / `.header-decoration` | _(removed)_ | Simpler header |
| `.paper-header` | `.paper-header` | Kept (unchanged) |
| `.empty-day` | `.empty-day` | Kept (unchanged) |
| `.archive-section` / `.-header` / `.-dates` / `.-date-link` | `.archive-section` / `.-header` / `.subnav__list` (reused) / `.subnav__link` | Archive now reuses subnav component |
| `.newspaper-footer` | `.site-footer` / `.footer__inner` | Cleaner, max-width constrained |
| `.back-link-area` / `.back-link` | `.article-nav` / `.__link` | Renamed for clarity |
| `.article-section-badge` | `.article-section-badge` | Kept, content uses `.post-card__category-link` span |
| `.article-headline` | `.article-headline` | Kept, font-size 32-36px |
| `.article-content` | `.article-content` | Kept, body font 1rem/24px |
| `.article-sources` / h3 / ul | `.article-sources` / `.__title` / `.__list` | BEM-ified sub-elements |
| `.refresh-results` / `.ok` / `.fail` | `.refresh-results` / `.ok` / `.fail` | Kept (unchanged) |

## Curl Extraction Workflow (when browser gets 403)

```bash
# 1. Get full HTML with desktop UA
curl -s -L -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' 'https://dep.com.vn/' 2>&1 | head -500

# 2. Extract CSS variable definitions
curl -s -L -A '...' '...' | grep -oP '--[a-z-]+:\s*[^;}]+' | head -50

# 3. Extract Class names used in components
curl -s -L -A '...' '...' | grep -oP 'class="[^"]*"' | sort -u | head -60

# 4. Extract inline CSS blocks (custom theme CSS)
curl -s -L -A '...' '...' | grep -oP '<style[^>]*>.*?</style>' | head -3

# 5. Identify component patterns
curl -s -L -A '...' '...' | grep -oP '<div class="[^"]*">\s*<div class="[^"]*">' | head -10

# 6. Count total page size
curl -s -L -A '...' '...' | wc -c
```

## Responsive Image-Box Hero Pattern

Key HTML structure:
```html
<div class="image-box">                          <!-- position-relative on desktop, flex on mobile -->
  <div class="image-box__image-wrapper">         <!-- 100% width, absolute on mobile -->
    <div class="image-box__image"                <!-- background-image, 380px height desktop -->
         style="background-image:url(...);">
    </div>
    <div class="image-box__image-overlay">       <!-- gradient overlay, 40% height bottom -->
    </div>
  </div>
  <div class="image-box__content">               <!-- absolute bottom:1.5em on desktop,
                                                       position:relative bottom:0 on mobile -->
    <div class="image-box__content-inner">       <!-- white bg + shadow on desktop,
                                                       none on mobile -->
      <!-- category-badge + title + excerpt + meta -->
    </div>
  </div>
  <a class="image-box__overlay-link"></a>        <!-- full-area click target, z-index:4 -->
</div>
```

Key responsive CSS:
```css
/* Desktop */
.image-box__image { height: 380px; }
.image-box__content { position: absolute; bottom: 1.5em; }
.image-box__content-inner { background: hsla(0,0%,100%,0.88); box-shadow: 0 3px 12px rgba(0,0,0,0.15); }
.image-box__image-overlay { height: 40%; background: linear-gradient(180deg, rgba(85,85,85,0), rgba(0,0,0,0.6)); }

/* Mobile <768px */
.image-box { align-items: flex-end; display: flex; min-height: 40vh; }
.image-box__image-wrapper { position: absolute; inset: 0; }
.image-box__content { bottom: 0; position: relative; padding: 0 1em 1em; }
.image-box__content-inner { background: none; box-shadow: none; padding: 0; text-align: left; }
.image-box__title { color: white; font-size: 18px; }
.image-box__image-overlay { height: 60%; }
.image-box__excerpt { display: none; }
```

## Post Card Structure

```html
<div class="post-grid__row">          <!-- 1/2/3 col CSS Grid -->
  <div class="post-grid__col">
    <article class="post-card">
      <a class="post-card__image-link" href="...">
        <div class="post-card__image">  <!-- aspect-ratio: 1/1 -->
          <img src="..." alt="">
        </div>
      </a>
      <div class="post-card__content">
        <p class="post-card__meta">
          <span class="post-card__category">
            <a class="post-card__category-link" href="...">  <!-- border-left: 2px accent -->
              Category
            </a>
          </span>
          <span class="post-card__date">Date</span>
        </p>
        <h3 class="post-card__title">
          <a class="post-card__title-link" href="...">Title</a>
        </h3>
        <p class="post-card__excerpt">...</p>
        <div class="post-card__tags">
          <span class="post-card__tag">tag</span>
        </div>
      </div>
    </article>
  </div>
</div>
```

## GSAP Animations (adapted for new selectors)

```javascript
// Old selectors → New
// '.utility-bar'        → '.site-header'
// '.newspaper-header'   → (removed)
// '.section-nav'        → '.subnav'
// '.date-nav'            → '.date-nav' (kept)
// '.featured-card'       → '.image-box'
// '.news-grid'          → '.post-grid__main'
// '.article-card'       → '.post-card'

master.from('.site-header', { y: -20, opacity: 0, duration: 0.3 });
master.from('.subnav', { opacity: 0, duration: 0.3 }, '-=0.15');
master.from('.date-nav', { opacity: 0, y: -8, duration: 0.3 }, '-=0.15');
master.from('.image-box', { opacity: 0, y: 30, scale: 0.98, duration: 0.7, ease: 'back.out(1.4)' }, '-=0.1');
// Scroll-triggered stagger:
gsap.from('.post-card', { opacity: 0, y: 40, duration: 0.6, stagger: 0.08, ease: 'power2.out',
  scrollTrigger: { trigger: '.post-grid__main', start: 'top 85%', toggleActions: 'play none none none' }
});
```

## Verdict
- CSS variables: already matched dep.com.vn from prior session
- New in this session: Full template restructure + CSS rewrite + 26 class mappings + responsive hero
