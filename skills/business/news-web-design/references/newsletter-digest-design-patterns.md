# Newsletter / News Digest Design Patterns

> Research conducted July 2026 — 10 sites analyzed
> Sites: Stratechery, The Hustle, Every, 1440, TLDR Newsletter, Figma Blog, Notion Blog, Stripe Blog, Linear (Now), Axios AM

## Mục lục

1. [Tổng quan các mẫu](#1-tổng-quan-các-mẫu)
2. [Phân tích chi tiết từng site](#2-phân-tích-chi-tiết-từng-site)
3. [Patterns so sánh — Digest vs Newspaper](#3-patterns-so-sánh--digest-vs-newspaper)
4. [5 Design patterns áp dụng cho Flask project](#4-5-design-patterns-áp-dụng-cho-flask-project)
5. [CSS + Typography recommendations](#5-css--typography-recommendations)

---

## 1. Tổng quan các mẫu

| # | Tên | Loại | Layout | Images | Độ phức tạp |
|---|-----|------|--------|--------|-------------|
| 1 | **Stratechery** | Blog phân tích chuyên sâu | 1 cột | Không | Thấp |
| 2 | **The Hustle** | Newsletter business + bài viết | 2 cột (feature + grid) | Có | Trung bình |
| 3 | **Every** | Longform tech newsletter | 1 cột list | Có (thumbnails) | Trung bình |
| 4 | **1440** | Daily digest + knowledge base | Grid responsive | Có | Cao |
| 5 | **TLDR Newsletter** | Tech news digest | 1 cột list | Có (thumbnails) | Thấp |
| 6 | **Figma Blog (Shortcut)** | Design/tech blog | Grid cards | Có (large hero) | Cao |
| 7 | **Notion Blog (Tools & Craft)** | Product blog | Grid cards | Có (thumbnails) | Trung bình |
| 8 | **Stripe Blog** | Product/business blog | Grid + list | Có (hero images) | Cao |
| 9 | **Linear (Now)** | Product updates / changelog | 1 cột list | Minimal | Thấp |
| 10 | **Axios AM** | Morning news brief | 1 cột | Bullet-style | Thấp |

---

## 2. Phân tích chi tiết từng site

### 2.1. Stratechery (stratechery.com)

Ben Thompson — Phân tích tech strategy.

- **Layout:** 1 cột, content width ~700px, centered. Sidebar phải cho "Recent Updates" + "Podcasts".
- **Article card:** Blog-style đơn giản: heading → date/time → excerpt text. Không images, không card border.
- **Typography:**
  - Font: Serif (Georgia hoặc font stack mặc định) cho body
  - Heading: 24-28px, bold
  - Body: ~16-18px, leading rộng (~1.6)
  - Date: small, uppercase, grey (#666)
- **Màu sắc:** Chủ đạo trắng (#fff), text đen (#333), link xanh dương (#336699)
- **Điểm đặc biệt:** Cực kỳ minimal — gần như không có design. Checkbox "Continue reading↓" để mở rộng excerpt.
- **Phù hợp:** Style "viết blog chuyên sâu, chữ là chính"

### 2.2. The Hustle (thehustle.co)

Business newsletter (HubSpot-owned).

- **Layout:** Hybrid — landing page newsletter + article grid.
  - Header: Email subscription form CTA
  - Featured article: 1 card lớn, full-width
  - "Top Stories": 2-column grid (heading + author + date)
  - "Hustle Originals": 2-column card grid (heading + image placeholder)
- **Article card:**
  - Featured: heading lớn (28px) + summary paragraph + author name + date
  - Grid: heading (18-20px) + author + date, minimal text
- **Typography:**
  - Font: Sans-serif system font stack
  - Heading: Bold, 20-32px tuỳ cấp độ
  - Author/date: Màu xám (#666), kích thước nhỏ (14px)
- **Màu sắc:** Trắng, đen, accent xanh dương (#0077b5), vàng cho "Free guide" section
- **Điểm đặc biệt:** Newsletter CTA chiếm ưu thế ở hero section. Content hierarchy rõ ràng: feature → grid → supplementary sections.
- **Phù hợp:** Newsletter-focused landing page, mix content promotion + subscription

### 2.3. Every (every.to)

Longform tech essays + AI focus.

- **Layout:** 1 cột list, articles xếp theo thời gian
- **Article card:**
  - Date + Category label (vd: "JUL 1, 2026 IN CONTEXT WINDOW")
  - Heading (28px)
  - Author link
  - Description paragraph (optional)
  - Separator: horizontal line giữa các articles
- **Typography:**
  - Font: Sans-serif (hệ thống)
  - Date+category: Uppercase, small, tracking rộng (letter-spacing)
  - Author: Normal weight, màu phụ
- **Màu sắc:** Trắng chủ đạo, đen cho text, accent xám. Nhiều whitespace.
- **Điểm đặc biệt:** Category labels đóng vai trò quan trọng — dùng để filter/tag content. Date format nhất quán: "MONTH DAY, YEAR IN CATEGORY".
- **Phù hợp:** Blog/news digest với categories riêng

### 2.4. 1440 (join1440.com)

Daily digest + knowledge platform.

- **Layout:** Next.js app, responsive grid.
  - Hero: Headline lớn + subheadline
  - 4-column grid feature cards
  - Topics grid: 8 categories
  - Articles: Card-based grid
- **Article card:** image + heading + brief description
- **Typography:**
  - Font: Adobe Typekit custom font (proprietary)
  - Headings: Serif cho display, Sans-serif cho body
  - Fluid typography: text-heading-700, text-display-1600
- **Màu sắc:** Trắng (#fff), xám (#f5f5f5), blue-100 (#e8f0fe), cyan accent
- **Điểm đặc biệt:**
  - Design system rất chặt chẽ với CSS utility classes
  - Topic icons là SVGs inline
  - Search là tính năng trung tâm
  - Newsletter subscription form prominent ở top
- **Phù hợp:** Tham khảo design system naming conventions, responsive patterns

### 2.5. TLDR Newsletter (tldr.tech)

Tech news digest — nhiều editions (Tech, DevOps, Product, Founders, Crypto).

- **Layout:** 1 cột list, chia thành sections theo category (News, Strategies, Tools, Miscellaneous)
- **Article card:**
  - Image thumbnail + Title link + TLDR summary
  - Metadata: source, reading time, category tag
  - Separator giữa articles
  - Click tracking link (utm parameters)
- **Typography:**
  - Font: System sans-serif
  - Title: Semibold, 16-18px
  - TLDR summary: Normal, 14-15px, grey
  - Category tag: Badge nhỏ
- **Màu sắc:** Trắng, xám nhạt, link xanh
- **Điểm đặc biệt:**
  - Mỗi article có summary ngắn (TLDR) — feature cực kỳ quan trọng
  - Sponsorship section rõ ràng (Sponsored Blog)
  - Categories phân loại articles (headlines, strategies, tools, quick, miscellaneous)
  - Click counts hiển thị cho mỗi article
- **Phù hợp:** Mẫu lý tưởng cho news digest có multiple categories

### 2.6. Figma Blog — Shortcut (figma.com/blog)

Design/tech blog.

- **Layout:** Grid cards, 2-column trên desktop
- **Article card:**
  - Large hero image / video thumbnail
  - Category tag (vd: "INSIDE FIGMA", "PRODUCT UPDATES", "CONFIG")
  - Heading (22-26px)
  - Author + Date
  - Summary paragraph
- **Typography:**
  - Font: Custom sans-serif (Figma)
  - Tag badges: Bold, uppercase, small
  - Headings: 24-32px, bold
- **Màu sắc:** Trắng, đen, accent tím
- **Điểm đặc biệt:** Slideshow/carousel cho featured content. Tags system phức tạp. Hero images rất chất lượng.
- **Phù hợp:** Nếu muốn design "sang, xịn" với images chất lượng cao

### 2.7. Notion Blog — Tools & Craft (notion.com/blog)

Product blog.

- **Layout:** Grid cards 2-3 columns, category filter tabs
- **Article card:**
  - Thumbnail image (illustration style)
  - Category label (Notion HQ, Tech, Inspiration, For Teams...)
  - Heading + description (có thể truncate)
  - Author name
- **Typography:**
  - Font: Sans-serif (Notion custom)
  - Category: semibold, 14px
  - Heading: 20-24px
  - Description: 15-16px
- **Màu sắc:** Trắng (#fff), đen, accent xanh lá (#0f7b6c)
- **Điểm đặc biệt:** Filter tabs cho categories. Mỗi article có illustration riêng biệt (branded style).
- **Phù hợp:** Thumbnails + category filtering pattern

### 2.8. Stripe Blog (stripe.com/blog)

Product/business blog premium.

- **Layout:** Large hero feature + grid bên dưới
- **Article card:**
  - Large image (16:9)
  - Category badge
  - Heading (24px+)
  - Description
  - Date
- **Typography:**
  - Font: Custom sans-serif (Stripe design system)
  - Very clean, nhiều whitespace
- **Màu sắc:** Trắng, đen, accent xanh Stripe (#635bff)
- **Phù hợp:** Design inspiration chung

### 2.9. Linear — Now (linear.app/now)

Product updates/changelog — tối giản nhất.

- **Layout:** 1 cột list, filter tabs (All, Changelog, Community, News, Craft, AI, Practices, Press)
- **Article card:**
  - Heading (20px)
  - 1-2 câu description
  - Author + Date
  - "→" arrow để drill down
  - Không image, không card border
- **Typography:**
  - Font: Inter (sans-serif)
  - Heading: semibold, 20px
  - Body: 15px, leading 1.5
  - Meta: 13px, grey
- **Màu sắc:** Trắng (#fff), đen (#111), xám nhạt (#f5f5f5)
- **Điểm đặc biệt:** Cực kỳ minimal — focus hoàn toàn vào content. Mỗi update chỉ là 1 card nhỏ gọn.
- **Phù hợp:** Daily digest với 5-10 articles mỗi ngày

### 2.10. Axios AM (axios.com/newsletters/axios-am)

"Smart Brevity" format — morning news brief.

- **Layout:** 1 cột, bullet point style
- **Article card:**
  - **Bold headline** → 1-2 sentence summary → "Why it matters" box
  - Numbers/bullets for key points
  - "Between the lines" analysis boxes
  - No images in newsletter version
- **Typography:**
  - Font: Sans-serif
  - Headlines: Bold, 20-24px
  - "Why it matters": Bold label + italic text
- **Màu sắc:** Xanh navy, trắng, đỏ accent
- **Điểm đặc biệt:**
  - "Smart Brevity" format: cực kỳ hiệu quả cho người bận rộn
  - "Why it matters" là USP — giải thích tại sao tin này quan trọng
  - "By the numbers" section cho business analysis
- **Phù hợp:** Cực kỳ phù hợp cho đối tượng cần giải thích ngắn gọn "tại sao tin này quan trọng"

---

## 3. Patterns so sánh — Digest vs Newspaper

### 3.1. Layout patterns cho multiple articles

| Pattern | Mô tả | Ví dụ | Khi nào dùng |
|---------|-------|-------|-------------|
| **A. Single-column list** | Articles xếp dọc, mỗi article 1 card | TLDR, Every, Linear | 5-15 articles, mobile-friendly |
| **B. Feature + grid** | 1 article chính lớn + grid các article phụ | The Hustle, Stripe Blog | Có 1 tin chính nổi bật |
| **C. Grid cards** | Grid đều (2-4 cột) | Figma, Notion, 1440 | Nhiều articles, visual-heavy |
| **D. Category sections** | Chia page thành sections theo category | TLDR (News/Strategies/Tools) | Content có multiple topics |
| **E. Bullet digest** | Mỗi tin = bullet ngắn + link | Axios AM | Siêu ngắn gọn, 5-10 items |

### 3.2. Hierarchy handling

1. **Size differential:** Article chính → 28-32px, article phụ → 18-22px (The Hustle)
2. **Position:** Article chính ở top, càng xuống càng phụ (TLDR)
3. **Category labels:** "HEADLINES" → "STRATEGIES" → "TOOLS" (TLDR)
4. **Visual weight:** Article chính có hero image; phụ chỉ text (Figma)
5. **"Why it matters" box:** Axios — highlight relevance

### 3.3. Image usage comparison

| Cách dùng | Ví dụ | Ghi chú |
|-----------|-------|---------|
| **Không images** | Stratechery, Axios AM, Linear | Load nhanh, mobile tốt |
| **Hero image lớn** | Figma, Stripe | Cho featured article |
| **Thumbnail vuông/nhỏ** | TLDR (200×200), Notion | Cho grid view |
| **Thumbnail horizontal** | Every (16:9), 1440 | Card-style layout |
| **Illustration** | Notion Blog | Branded style |

### 3.4. Newsletter-specific features

| Feature | Mô tả | Sites dùng |
|---------|-------|------------|
| **TLDR Summary** | 1-2 paragraph summary mỗi article | TLDR Newsletter |
| **"Why it matters"** | Context box | Axios AM |
| **Category filters** | Tabs để lọc articles | Notion, Linear |
| **Sponsorship slot** | Sponsored blog/content rõ ràng | TLDR |
| **Subscription CTA** | Email signup form prominent | The Hustle, 1440 |
| **Click tracking** | Số clicks per article | TLDR |
| **Reading time** | "X minute read" | Many |
| **Daily/Weekly digest** | Schedule indicator | Every (weekly roundup) |

### 3.5. Key differences: Digest vs Newspaper

| Aspect | Traditional Newspaper (NYT/Guardian) | Newsletter/Digest (TLDR/Axios) |
|--------|--------------------------------------|--------------------------------|
| **Content depth** | Longform, multiple columns | Short summaries, scan-friendly |
| **Images** | Mandatory for every article | Optional; minimal when present |
| **Typography** | Serif-heavy, authoritative | Sans-serif, clean, modern |
| **Whitespace** | Dense, information-rich | Generous, scannable |
| **CTA** | Hidden (paywall) | Prominent (subscription) |
| **Sponsorship** | Separate ad units | Integrated sponsored content |
| **Mobile priority** | Progressive enhancement | Mobile-first by design |
| **Update frequency** | Real-time rolling | Daily/weekly batch |
| **Reader goal** | Deep reading | Skim → click → read elsewhere |

---

## 4. 5 Design patterns áp dụng cho Flask project

### Pattern 1: News Digest 1-Cột + Category Sections (TLDR-inspired)

```
Header: [Title + Date + Subscription CTA]
────────────────────────────────────────────
Category: KINH TẾ (label)
┌─────────────────────────────────────────┐
│ ● GDP quý 2 tăng trưởng ấn tượng       │
│   Tổng cục Thống kê công bố số liệu... │
│   📊 3 phút đọc · VnExpress            │
├─────────────────────────────────────────┤
│ ● Lãi suất ngân hàng tiếp tục giảm     │
│   NHNN điều chỉnh lãi suất điều hành...│
│   📊 2 phút đọc · CafeF                │
└─────────────────────────────────────────┘

Category: F&B (label)
┌─────────────────────────────────────────┐
│ ● Giá thịt gà giảm 5% trong tháng 6    │
│   Nguồn cung dồi dào, giá thức ăn...   │
│   🍗 4 phút đọc · Báo Đầu Tư           │
└─────────────────────────────────────────┘
```

**Implement:** single-column, max-width 720px; heading 19px bold; summary 15px; meta 13px grey; category badges = colored per-category.

### Pattern 2: Smart Brevity Card (Axios-inspired)

```
┌──────────────────────────────────────────────┐
│ 💡 Giá gas tăng 15% từ tháng sau             │
│                                              │
│ Petrovietnam thông báo điều chỉnh giá gas... │
│                                              │
│ ⚡ TẠI SAO QUAN TÂM:                          │
│ Giá gas tăng → chi phí nấu nướng tăng →      │
│ giá thành món gà rán có thể phải điều chỉnh  │
│                                              │
│ 📰 Nguồn: CafeF · 2 phút đọc                 │
└──────────────────────────────────────────────┘
```

**Implement:** bordered card (border-radius 8-12px); icon prefix; "Tại sao quan tâm?" box for relevance; source + reading time at bottom.

### Pattern 3: Feature Article + Grid (The Hustle-inspired)

```
┌─── FEATURE ────────────────────────────────┐
│ ┌─────────────────┐                        │
│ │  (OG Image)     │   [KINH TẾ]            │
│ │  16:9            │   Tiêu đề feature...   │
│ └─────────────────┘   Tóm tắt 2-3 câu...   │
│                        Tác giả · 5 phút đọc│
└─────────────────────────────────────────────┘

┌─── OTHER NEWS ───────────────────────────┐
│ ┌──────┐ ┌──────┐ ┌──────┐               │
│ │Image │ │Image │ │Image │               │
│ │Title │ │Title │ │Title │               │
│ └──────┘ └──────┘ └──────┘               │
└───────────────────────────────────────────┘
```

**Implement:** 1 featured + OG image; 3-column grid below; collapse to 1-col on mobile.

### Pattern 4: Linear-style Minimal List

```
Filter: [Tất cả] [Kinh tế] [Công nghệ] [F&B]

┌─────────────────────────────────────────────┐
│ Giá gas tăng 15% từ tháng sau               │
│ Petrovietnam thông báo điều chỉnh giá...    │
│ CafeF · 3 giờ trước →                       │
├─────────────────────────────────────────────┤
│ Apple ra mắt chip M4 mới                    │
│ Hiệu năng tăng 50% so với thế hệ trước...   │
│ TechCrunch · 5 giờ trước →                  │
└─────────────────────────────────────────────┘
```

**Implement:** no card border, only horizontal rules; category filter tabs above; relative dates.

### Pattern 5: Dark Mode Newsletter

- Background: #0a0a0a
- Text: #e0e0e0
- Accent: cyan #00bcd4 hoặc cam #ff6d00
- Cards: #1a1a1a với border #333
- CSS custom properties cho theme toggle; JS toggle + localStorage

---

## 5. CSS + Typography recommendations

### Font stack
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
/* Hoặc system font stack */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```

### Heading sizes
```css
--text-heading-xl: 28px;  /* Feature article */
--text-heading-lg: 22px;  /* Article title */
--text-heading-md: 18px;  /* Sub-article title */
--text-body: 15px;        /* Summary */
--text-meta: 13px;        /* Source, date, reading time */
```

### Color palette
```css
--color-bg: #ffffff;
--color-bg-alt: #f8f9fa;
--color-text: #1a1a1a;
--color-text-secondary: #6b7280;
--color-border: #e5e7eb;
--color-accent-blue: #2563eb;     /* Kinh tế */
--color-accent-purple: #7c3aed;   /* Công nghệ */
--color-accent-orange: #ea580c;   /* F&B */
--color-link: #2563eb;
```

### Component structure
```
templates/
├── base.html              # Layout chính
├── components/
│   ├── article-card.html  # Card component (reusable)
│   ├── category-label.html
│   ├── featured-card.html
│   ├── why-it-matters.html (Smart Brevity box)
│   └── dark-mode-toggle.html
├── digest.html            # Page: 1-cột digest
├── feature-grid.html      # Page: Feature + grid
├── minimal.html           # Page: Linear-style
└── single.html            # Page: 1 article
```
