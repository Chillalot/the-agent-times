# Axios Layout Research

## Overview
Axios is a news website known for its "Smart Brevity" approach — short, scannable news summaries that get straight to the point. The site emphasizes speed and clarity over long-form storytelling.

## Known Design Patterns

### Color Palette
- **Background**: Pure white (`#ffffff`) — clean, uncluttered canvas
- **Text**: Near-black (`#222222`) — high contrast for readability
- **Accent blue**: `#6b8cff` — used for links, highlights, and interactive elements
- **Borders**: Soft gray (`#e2e2e2`) — minimal, subtle separation between cards

### Typography
- **Headlines**: Serif (Georgia / Times New Roman) — bold, authoritative, traditional news feel
- **Body**: System sans-serif stack — clean, fast-loading, highly readable on all devices
- **Headline size**: ~28px for article titles
- **Body size**: ~17px for comfortable reading

### Layout Structure
- **Max width**: ~1040px — generous but not full-bleed
- **Content column**: ~680px — optimal reading width for articles
- **Grid**: 3-column layout on desktop — article cards arranged in a responsive grid
- **Navigation**: Simple top navigation bar with minimal items

### Key Components
1. **Article cards**: Minimal borders, white background, headline + brief summary + metadata
2. **Smart Brevity summaries**: Short bullet-style news digests with key takeaways
3. **Newsletter integration**: Prominent email signup calls-to-action
4. **Section headers**: Clear, bold category labels separating news sections

### Responsive Behavior
- Desktop: 3-column grid
- Tablet: 2-column grid
- Mobile: Single column, stacked layout

### Notes
- axios.com is behind Cloudflare, so direct scraping/access is blocked
- Design philosophy prioritizes speed — lightweight pages, minimal assets
- The "Smart Brevity" concept extends to visual design: clean lines, generous whitespace, no visual clutter
- Card-based layout with subtle separation rather than heavy box shadows or borders
