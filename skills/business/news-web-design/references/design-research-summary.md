# Design Research — Live Inspection July 2026

## Sources Inspected
- VnExpress (vnexpress.net) — Vietnamese news leader
- New York Times (nytimes.com) — US paper of record  
- The Guardian (theguardian.com) — UK progressive broadsheet
- BBC (bbc.com) — documented from established knowledge (DNS blocked)

## Summary: 28 Components Documented

Full file: `/home/chillalot/design-research.md` (622 lines, 21KB)

### VnExpress (9 components)
1. Featured Article Card
2. Sub-item Card (Medium)
3. List Card (Small)
4. Navigation Bar
5. Image Thumbnail
6. Headline (h3)
7. Category Nav
8. Header/Top Bar
9. Footer

### NYT (10 components)
1. Story Card (standard)
2. Primary Navigation
3. Section Nav
4. Section Header
5. Headline Link
6. Byline/Meta
7. Standard Button
8. Emphatic Button
9. Masthead/Top Bar
10. Story Image

### Guardian (9 components)
1. Featured Card
2. Masthead Navigation
3. Card Headline
4. Image Container
5. Utility Top Bar
6. Highlights Carousel
7. Primary Button
8. Section Container
9. Kicker/Label

## Key Findings Applied

### Flat Design
- All 3 sites use 0px border-radius on cards
- No box-shadow on cards (flat design standard)
- Separators: border-bottom only

### Hover Effects (Very Subtle)
- **NYT**: Color change only (0.1s ease-out)
- **Guardian**: Light bg change `rgba(18,18,18,0.1)`  
- **VnExpress**: Color per category system

### Navigation
- Position: `static` (NONE use sticky/fixed on homepage)
- Each site scrolls naturally with page

### Image Aspect Ratio
- Consistent 5:3 (1.67:1) across all sites for thumbnails

### Vietnamese Typography
- VnExpress: Merriweather (headline) + Arial (body)
- dep.com.vn: Be Vietnam Pro (both)
- Recommendation: Be Vietnam Pro for Vietnamese readability
