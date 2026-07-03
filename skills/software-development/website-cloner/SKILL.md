---
name: website-cloner
description: "Clone thiết kế từ bất kỳ website nào. Trích xuất design tokens (màu, font, spacing), download assets, áp dụng vào frontend. Dựa trên AI Website Cloner Template (JCodesMore, 25k⭐)."
version: 1.2.0
author: Phương
tags: [cloning, design, tokens, extraction, css, theming]
---

# Website Cloner Tool

## Khi nào dùng
- Khi Long muốn "lấy cảm hứng" design từ một website khác
- Khi cần clone giao diện từ WordPress/Webflow sang frontend
- Khi muốn phân tích design tokens của đối thủ

## Cách dùng

```bash
python3 ~/.hermes/profiles/meow/scripts/website_cloner.py <URL>
python3 ~/.hermes/profiles/meow/scripts/website_cloner.py <URL> --apply-css ~/.hermes/profiles/meow/frontend/static/style.css
```

## Output
1. **Design token report** — lưu tại `~/.hermes/profiles/meow/reports/cloned_*.json`
2. **CSS variables** — extract từ `:root {}`
3. **Colors** — tất cả hex/rgb colors sử dụng
4. **Fonts** — Google Fonts + font-family declarations
5. **Spacing** — margin, padding, gap patterns
6. **Logos** — logo URLs (OG image, img tags)

## Kỹ thuật
- Dùng `requests` + `BeautifulSoup` (Ponytail philosophy: thư viện đơn giản nhất)
- Trích xuất CSS variables với regex
- Phân tích tech stack (WordPress? Bootstrap? Tailwind?)
- Có thể apply tokens vào CSS tự động

## CRITICAL: Apply Workflow — Đừng chỉ extract, hãy THAY ĐỔI giao diện

> Bài học từ thực tế: User sẽ nói "có thay đổi gì đâu" nếu bạn chỉ thêm biến CSS mà không apply vào giao diện.

### Quy trình apply đúng (4 bước bắt buộc):

**Bước 1: Extract design tokens**
```bash
python3 website_cloner.py <URL>
# → tạo file cloned_<domain>.json
```

**Bước 2: Đọc report và xác định tokens nào cần đổi**
```bash
python3 -c "import json; d=json.load(open('reports/cloned_domain.json')); print('Accent:', [v for k,v in d['design_tokens']['css_variables'].items() if 'accent' in k.lower() or 'color' in k.lower()][:5])"
```

**Bước 3: Apply tokens vào CSS (thủ công — không chỉ dùng --apply-css)**
Ví dụ clone dep.com.vn (màu `#032435`, font `Be Vietnam Pro`, container `1040px`):
```bash
# 3a. Accent color
sed -i 's/--accent: #[A-Fa-f0-9]*;/--accent: #032435;/' style.css
sed -i 's/--accent-hover: #[A-Fa-f0-9]*;/--accent-hover: #032741;/' style.css

# 3b. Font heading
# Thêm Google Font link vào base.html:
# <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700&display=swap" rel="stylesheet">

# 3c. Container max-width  
sed -i 's/--max-width: [0-9]*px;/--max-width: 1040px;/' style.css

# 3d. Shadow system
sed -i 's/--shadow: .*;/--shadow: rgba(50,50,93,0.25) 0 2px 5px -1px, rgba(0,0,0,0.3) 0 1px 3px -1px;/' style.css

# 3e. Dark mode colors
sed -i 's/--bg: #[A-Fa-f0-9]*;/--bg: #0d1929;/' style.css
sed -i 's/--accent: #[A-Fa-f0-9]*;/--accent: #4a9eff;/' style.css
```

**Bước 4: Restart server và verify**
```bash
pkill -f "python3 app.py"
cd ~/.hermes/profiles/meow/frontend && python3 app.py &
# Mở browser http://localhost:5050 và kiểm tra accent color, font, spacing
```

### Checklist apply cho từng loại token:
| Token | Cần đổi | Verify bằng |
|-------|---------|-------------|
| `--accent` | Màu chính (hex từ site clone) | Header accent text, links, buttons |
| `--font-serif` | Font tiêu đề (Google Font name) | Headlines, article titles |
| `--font-sans` | Font UI | Navigation, metadata, buttons |
| `--max-width` | Chiều rộng container | Page wrapper thay đổi width |
| `--shadow` | Hệ thống đổ bóng | Cards, modals có shadow mới |
| `--bg-warm` | Màu nền phụ | Date nav background |
| `--text` | Màu chữ chính | Body text color |
| `[data-theme="dark"]` | Toàn bộ dark mode vars | Toggle theme → xem dark mode |

Ví dụ thực tế: Xem `reports/cloned_dep_com_vn.json` để tham khảo kết quả clone từ dep.com.vn (440KB page, 20 colors, 22 fonts, 50+ CSS variables extracted).

## Nguyên lý (từ AI Website Cloner Template)
1. **Reconnaissance** — fetch + extract design tokens
2. **Foundation** — update fonts, colors, globals
3. **Component Specs** — ghi lại computed styles
4. **Assembly** — áp dụng vào frontend

---

## ADVANCED: Full Template Restructure

Khi clone design từ một website lớn (WordPress magazine như dep.com.vn), việc chỉ thay CSS variables là chưa đủ. Bạn cần **restructure cả HTML template + CSS components** để giao diện thực sự giống.

### Pitfall: Browser bị 403 khi clone

Một số site (dep.com.vn) dùng NinjaFirewall / Cloudflare blocking browser automation. **Không panic** — dùng curl với user-agent desktop:

```bash
curl -s -L -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' 'https://target.com/' | head -300
```

Grep các phần tử chính:
```bash
# Lấy CSS variables
curl -s -L -A '...' 'https://target.com/' | grep -oP '--[a-z-]+:\s*[^;}]+' | sort -u

# Lấy class names từ components
curl -s -L -A '...' 'https://target.com/' | grep -oP 'class="[^"]*"' | sort -u | head -60

# Lấy CSS inline blocks
curl -s -L -A '...' 'https://target.com/' | grep -oP '<style[^>]*>.*?</style>' | head -5
```

### Quy trình Full Template Restructure (6 bước)

**Bước 1: Reconnaissance — Extract HTML class naming convention**

Site dùng BEM? Bootstrap? WordPress block classes? Inline styles? Ghi lại:

```bash
# Ví dụ dep.com.vn:
# - BEM convention: .post-card, .post-card__title, .post-card__content
# - WordPress classes: .wp-block-*, .menu-item, .subnav__*
# - Bootstrap: .container, .row, .col-*, .d-flex, .position-relative
# - Custom components: .image-box, .post-grid, .two-up-gallery-card
```

**Bước 2: Map old classes → new BEM classes**

Tạo mapping table. Ví dụ từ session dep.com.vn:

| Old Class (NYT-style) | New Class (dep.com.vn BEM) | Notes |
|---|---|---|
| `.newspaper-header` | `.site-header` → `.inside-header` | Logo left + nav right |
| `.section-nav` / `.section-nav-inner` | `.subnav` → `.subnav__inner` → `.subnav__list` | Horizontal scrollable, uppercase |
| `.date-nav` / `.date-nav-inner` | `.date-nav` → `.date-nav__inner` | Arrow buttons, picker, today link |
| `.news-featured.featured-card` | `.image-box` + `.image-box__content-inner` | Full-width bg, overlay, centered text |
| `.news-grid` / `.article-card` | `.post-grid` / `.post-card` | Square images, left-border badge |
| `.card-badge` | `.post-card__category-link` | `border-left: 2px solid` signature |
| `.search-area / .search-form` | `.header-search-form-compact` | Inline in header bar |
| `.newspaper-footer` | `.site-footer` → `.footer__inner` | Clean, opacity 0.75 |

**Bước 3: Restructure base.html**

Các thành phần cần có trong base.html cho magazine layout:

```
site-header (logo left + nav right + theme-toggle)
  ├── inside-header (flex, max-width container)
  │   ├── header-left + header-logo
  │   ├── main-nav > .menu > .menu-item (uppercase, letter-spacing)
  │   └── menu-bar-items (search form + theme toggle button)
subnav (horizontal scrollable category links)
  └── subnav__inner > subnav__list > subnav__item > subnav__link
date-nav (prev/next arrows, current date, date picker, today link)
site-main (main content area — {% block content %})
  └── todays-paper (section wrapper)
site-footer
  └── footer__inner (max-width constrained)
```

**Bước 4: Restructure index.html — Components**

- **Featured hero (image-box)**: `image-box__image-wrapper` (bg img) + `image-box__image-overlay` (gradient) + `image-box__content` (positioned bottom, centered white box with shadow)
- **Article grid (post-grid)**: `post-grid__row` (3-column grid on desktop, 1-col mobile) with `post-card` components
- **Date archive**: Reuse `.subnav__list` for horizontal date links
- **Empty state**: Keep standalone, no BEM needed

**Bước 5: Responsive patterns — Image-box hero**

Desktop:
```html
<!-- image-box: full-width, content overlay at bottom -->
<div class="image-box position-relative">
  <div class="image-box__image-wrapper">
    <div class="image-box__image" style="background-image..."></div>
    <div class="image-box__image-overlay"></div>  <!-- gradient -->
  </div>
  <div class="image-box__content position-absolute">
    <div class="image-box__content-inner">  <!-- white bg, shadow -->
      <category badge + title + excerpt + meta>
    </div>
  </div>
  <a class="image-box__overlay-link" href="..."></a>
</div>
```

Mobile (<768px):
```css
/* image-box switches to flex + min-height */
.image-box { align-items: flex-end; display: flex; min-height: 40vh; }
.image-box__content { bottom: 0; position: relative; padding: 0 1em 1em; }
.image-box__content-inner { background: none; box-shadow: none; }
.image-box__image-wrapper { position: absolute; inset: 0; }
.image-box__title { color: white; }  /* no white overlay box on mobile */
.image-box__image-overlay { height: 60%; }
```

**Bước 6: Viết CSS từ đầu (không patch)**

Với restructure lớn, viết CSS mới hoàn toàn sẽ sạch hơn sed từng dòng. Giữ lại:
- Theme variables (`:root`, `[data-theme="dark"]`) — vì đã extract từ bước Foundation
- Article content styles (`.article-content h2`, blockquote, lists, etc.) — ổn định
- Empty state, refresh page, GSAP animations

Viết mới:
- Site layout (site-header, subnav, date-nav, site-footer)
- Components (image-box, post-card, post-grid)
- Responsive breakpoints
- All BEM class definitions

### Checklist Full Restructure

| Item | Verify bằng |
|------|-------------|
| Header có logo + nav right | Resize <768px → nav wraps |
| Subnav horizontal scrollable | Ctrl+Shift+I → confirm overflow-x: auto |
| Date nav arrows + picker | Click prev/next date → URL changes |
| Featured hero image + overlay | Mobile → text white, no overlay box |
| Card grid 3-col desktop | 1-col mobile, 3-col ≥960px |
| Category left-border badge | 2px solid accent, uppercase |
| Card image zoom on hover | Hover → scale(1.05) |
| All GSAP animations work | Check .fade-in.visible on scroll |
| Dark mode toggle | Toggle → all vars switch |
| No broken old classes | grep old class names → 0 matches |

## Deep CSS Layout Analysis (Pixel-Level)

Khi cần không chỉ clone tokens mà phân tích **toàn bộ layout** ở mức pixel — từng component, exact CSS values, hover effects, transitions.

### Use case
- User yêu cầu "phân tích layout siêu chi tiết", "từng pixel"
- Cần hiểu rõ component structure trước khi clone/recreate
- Site dùng WordPress inline CSS (không external stylesheet riêng)
- Cần so sánh layout giữa **nhiều page types** (homepage, category, article, archive)

### Workflow A — Single Page (curl + grep + Python)

Dùng khi chỉ phân tích 1 URL (live):

```bash
# 1. Fetch HTML với curl (bypass bot protection)
curl -s -L -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' \
  -H 'Accept-Language: vi-VN,vi;q=0.9' \
  'https://target.com/' -o /tmp/page.html

# 2. Extract class names để hiểu component structure
grep -oP 'class="([^"]*)"' /tmp/page.html | sort -u | head -200

# 3. Extract all CSS inline blocks (WordPress thường dùng inline)
python3 -c "
import re
with open('/tmp/page.html') as f:
    html = f.read()
styles = re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)
print(f'Found {len(styles)} style blocks')
for i, s in enumerate(styles):
    print(f'  Block {i}: {len(s):>6} chars — {\"CUSTOM\" if any(ck in s for ck in [\"post-card\",\"image-box\",\"subnav\",\"main-footer\",\"slideout\"]) else \"FRAMEWORK\"}'  )
"

# 4. Catalog hover effects + transitions
python3 -c "
import re
with open('/tmp/page.html') as f:
    html = f.read()
styles = re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)
for s in styles:
    hovers = re.findall(r'([.#]?[a-zA-Z_-]+(?::hover|:focus|:active)[^{]*\\{[^}]*\\})', s)
    for h in hovers:
        name = h.split('{')[0].strip()
        props = h.split('{')[1].rstrip('}')
        if 'transition' in props or 'color' in props or 'transform' in props:
            print(f'{name} | {props.strip()[:100]}')
"
```

### Workflow B — Multi-Page Cross-Comparison (files saved locally)

Dùng khi có sẵn HTML files của nhiều page types (homepage, category, article, magazines). **Quy trình 6 bước:**

#### Bước 1: Inventory
```bash
ls -lh /tmp/dep_pages/
# Check file sizes — >300KB often has full inline CSS
```

#### Bước 2: Quick Scan — Pattern counting
Use the `search_files` tool with `output_mode='count'` to find which pages have which components:

```python
# Count patterns across files
# 'post-grid' → homepage has most (7 vs 1-2 on other pages)
# 'post-card' → homepage ~39, category ~18, article ~12
# 'pagination' → only category pages
# 'fullwidth-slider' → homepage only
# 'subnav' → homepage + category pages; article has only 2
```

#### Bước 3: Component Extraction
Use `search_files` with `context=N` to get HTML samples for each component. Compare variants across files:

```python
# Example variant discovery:
# homepage post-card classes: --post, --default, --highlight
# article post-card classes: --post, --highlight, --small-row
# magazine post-card classes: --default, --magazine
```

#### Bước 4: Detail Extraction — Python script

Write a Python script to extract structured data from each page's body (not <head>), component by component:

```python
import re
from pathlib import Path

html = Path('/tmp/dep_pages/homepage.html').read_text()
body = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL).group(1)

# Count post cards + extract variants
cards = re.findall(r'<article[^>]*class="([^"]*)"[^>]*>', body)
post_cards = [c for c in cards if 'post-card' in c]
print(f"Count: {len(post_cards)}, Variants: {set(post_cards)}")

# Extract header HTML
header = re.search(r'<header[^>]*class="[^"]*site-header[^"]*"[^>]*>(.*?)</header>', body, re.DOTALL)

# Extract footer
footer = re.search(r'<footer[^>]*class="[^"]*site-info[^"]*"[^>]*>(.*?)</footer>', body, re.DOTALL)
# Note: footer uses class 'site-info', NOT 'site-footer'

# Extract first post-card full structure
card = re.search(r'<article[^>]*class="[^"]*post-card[^"]*"[^>]*>(.*?)</article>', body, re.DOTALL)

# Extract fullwidth slider
slider = re.search(r'class="[^"]*fullwidth-slider[^"]*"', body)

# Extract pagination
pag = re.search(r'<div[^>]*class="[^"]*pagination[^"]*"[^>]*>(.*?)</div>', body, re.DOTALL)

# Extract hero-title
hero = re.search(r'<div[^>]*class="[^"]*hero-title[^"]*"[^>]*>(.*?)</div>', body, re.DOTALL)

# Extract article content
article = re.search(r'<article[^>]*id="[^"]*post[^"]*"[^>]*>(.*?)</article>', body, re.DOTALL)

# Extract entry-content (article body text)
entry = re.search(r'<div[^>]*class="[^"]*entry-content[^"]*"[^>]*>', body)
```

**Key insight:** Use regex to find open-tag + class pattern, don't parse full HTML — WordPress inline output is too irregular for parser-based approaches.

#### Bước 5: Cross-Reference Table

Synthesize findings into a comparison table:

| Feature | Homepage | Category | Article | Magazines |
|---------|----------|----------|---------|-----------|
| **Body class** | `home` | `archive category` | `single-post` | `page-template-page-magazine` |
| **Post-grid count** | 7 | 2 | 1 | 1 |
| **Post-card count** | ~39 | ~18 | ~12 | ~10 |
| **Fullwidth slider** | ✅ Hero | ❌ | ❌ | ❌ |
| **Hero title** | ❌ | ✅ `--archive` | ✅ `--singular` | hidden |
| **Subnav** | `--highlight` | `--archive --category` | ❌ | `--archive` |
| **Pagination** | ❌ | ✅ `--default-archive` | ❌ | ✅ JS-driven |
| **post-card variants** | 3 | 3 | 3 | 2 |
| **Image ratio** | `ratio-1x1` | `ratio-1x1` | `ratio-1x1` | `ratio-16x9` |
| **Grid columns** | 4 cols (xxl) | 3 cols (lg) | 3 cols (lg) | 2 cols (md) |

#### Bước 6: Generate Output

Compile into one markdown file with:
- **ASCII diagrams** for each page type (text-based box drawing)
- **Exact HTML structure** — class names, attribute hierarchy from live source
- **CSS variable tokens** (`:root {}`)
- **Responsive breakpoints** reference table
- **Component detail sections** — all variants documented

### Workflow Comparison

| Aspect | Workflow A (Single Page) | Workflow B (Multi-Page Cross) |
|--------|-------------------------|-------------------------------|
| Input | 1 URL (live fetch) | N local HTML files |
| Primary tools | curl + grep + Python regex | search_files + read_file + Python regex |
| Analysis depth | Component CSS values + styles | Component structure + cross-page diff |
| Output | CSS token report + computed values | Comparison table + HTML hierarchy |
| Best for | Clone 1 page design | Understand full site architecture |

### Key CSS Block Identification (từ thực tế dep.com.vn)

WordPress inline CSS thường có cấu trúc blocks như sau:

| Block # | Contents | Size | Notes |
|---------|----------|------|-------|
| 0-3 | Early custom vars + font imports | < 2KB | `--font-heading`, Google Fonts |
| 4 | WordPress block CSS | < 1KB | `wp-block-button` |
| 5 | Global styles (wp-preset) | ~11KB | Colors, gradients, spacing |
| 6 | Base theme CSS (GeneratePress) | ~20KB | Reset, typography, layout |
| 7 | Theme dynamic CSS | ~8KB | `.site-header`, `.main-navigation` |
| 8-10 | Plugin CSS (ads, slider) | < 2KB | Advanced Ads, Unslider |
| 11 | Elementor CSS | ~55KB | Full Elementor framework |
| 12 | Elementor kit variables | ~2KB | Custom Elementor colors |
| 13 | FontAwesome 4.7 | ~31KB | Icon font |
| 14 | **Bootstrap 5 custom theme** | ~99KB | Theme's main CSS + overrides |
| 15 | **Swiper + Component CSS** | ~39KB | **Target block** — post-card, image-box, subnav, slideout |
| 16+ | Custom CSS | < 5KB | Theme customizations |

**Critical insight**: Block 14-15 chứa **component styles** (post-card, image-box, subnav, slideout, video-thumbnail, two-up-gallery, header-search, social-links, ad-float). Framework blocks (Elementor, FontAwesome, Bootstrap) có thể bỏ qua khi phân tích layout.

### Component Documentation Template

Document từng component theo cấu trúc:

```markdown
### Component: [Tên]
**Selectors**: `.component-class`

#### Normal State
| Property | Value |
|----------|-------|
| background | `#ffffff` |
| font-size | `1rem` (16px) |
| padding | `1em` |
| border | `1px solid #dee2e6` |

#### Hover State
| Property | Value |
|----------|-------|
| color | `#337ab7` |
| transition | `color .4s ease` |

#### HTML Structure
```html
<!-- component HTML hierarchy từ live page -->
```

#### Responsive
| Breakpoint | Change |
|------------|--------|
| >= 960px | 4 columns |
| < 768px | 1 column |
```

### Hover & Transition Cataloging (giá trị nhất)

Ghi lại tất cả hover effects trong 1 bảng:

```markdown
| Element | Normal | Hover | Transition |
|---------|--------|-------|------------|
| .post-card__title-link | #222222 | #337ab7 | color .4s ease |
| .post-card__image img | scale(1) | scale(1.05) | all .4s ease |
| .subnav__link | #222222 | #337ab7 | color .4s ease |
```

### Output Examples

- `references/dep-exact-layout.md` — pixel-level analysis of **1 page** (homepage only), 992 lines, 15 components, computed CSS values.
- `references/dep-master-layout.md` — **cross-page type analysis** (homepage + category + article + magazines), 1030 lines, comparison tables, ASCII diagrams, HTML hierarchy from actual WordPress source.

## CloakBrowser (Stealth Browser)
CloakBrowser đã được cài đặt để bypass anti-bot detection. Xem `references/cloakbrowser-integration.md` cho chi tiết.

## Xem thêm
- Skill `news-web-design` — thiết kế giao diện báo chí
- File `design-research.md` — 28 components từ báo thật
- `references/dep-com-vn-full-restructure.md` — class mapping + CSS từ session rewrite
- `references/dep-exact-layout.md` — pixel-level layout analysis (1 page)
- `references/dep-master-layout.md` — cross-page type layout analysis (4 page types)
- `references/css-extraction-refined.md` — kỹ thuật extract CSS từ inline `<style>` blocks: unnamed blocks, dedup bằng hash, brace-matching parser, component classification keywords, các pitfalls
