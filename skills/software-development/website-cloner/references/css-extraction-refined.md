# CSS Extraction — Refined Technique

## Problem

WordPress sites ship CSS as multiple inline `<style>` blocks, many without `id` attributes. Identical CSS blocks (Bootstrap, Swiper, theme CSS) appear in every HTML page file. Standard extraction by style ID misses unnamed blocks.

## Solution

### 1. Capture ALL `<style>` blocks (named + unnamed)

```python
for match in re.finditer(r'<style[^>]*>(.*?)</style>', html, re.DOTALL):
    css_text = match.group(1).strip()
    full_tag = match.group(0)
    id_match = re.search(r'id="([^"]*)"', full_tag)
    style_id = id_match.group(1) if id_match else "(unnamed)"
```

### 2. Content-based deduplication across files

Hash the first ~200–300 chars of each block to identify duplicates across files:

```python
seen_hashes = set()
for each style block:
    h = hash(css_text[:300])  # or hashlib.md5(…).hexdigest()
    if h in seen_hashes: continue
    seen_hashes.add(h)
```

### 3. Brace-matching parser for minified CSS

Simple depth counter handles nested braces in minified CSS (gradients, calc, attribute selectors):

```python
depth = 1
j = brace_start + 1
while j < len(css) and depth > 0:
    if css[j] == '{': depth += 1
    elif css[j] == '}': depth -= 1
    j += 1
```

### 4. Structural elements to extract separately

- `@import` — regex `@import[^;]+;` (watch for semicolons inside URLs)
- `@font-face` — brace-matched block
- `@keyframes` — brace-matched block
- `:root` — CSS custom properties block
- `@media` — outer brace-matched block (don't try to parse inner rules individually)

### 5. Component classification by keyword matching

Use BEM-style class names as classification signals. Check more specific patterns first:

```python
if '.site-header' in s: return "HEADER"
if '.subnav' in s: return "SUBNAV"
if '.post-card' in s: return "POST CARDS"
```

Order matters: check SUBNAV before HEADER (both contain 'nav'), check specific patterns before generic.

### 6. Pitfall: @import with semicolons in URL

Google Fonts URLs contain semicolons (`wght@400;600;700`). The regex `@import[^;]+;` stops at the first `;` inside the URL, truncating it. Fix:

```python
# Better: match @import until the closing parenthesis + semicolon
imports = re.findall(r'@import\s+url\([^)]+\);', css)
```

### 7. Pitfall: Merge function inflating rule count

The naive merge (expand → split on `\\n}` → find selector) can misinterpret multi-line compound selectors like `body,\\nhtml {`, creating spurious entries. Fix: parse the raw rule string directly — find first `{` for selector, last `}` for body — without intermediate expansion.

### 8. Bug: Selector discarded by depth-0 brace handler in char-by-char parser

When implementing a character-by-character CSS rule parser with depth tracking, DO NOT replace the accumulator on encountering `{` at depth 0:

```python
# WRONG — current = [char] discards selector text ('body' in 'body{color:red}')
if char == '{':
    if depth == 0:
        current = [char]   # BUG: selector lost!
    depth += 1

# RIGHT — append; never replace the accumulator
if char == '{':
    current.append(char)
    depth += 1
```

The selector text accumulated at depth 0 before the `{` is valid — only clear on full rule extraction (when `}` returns depth to 0).

### 9. Pitfall: Don't exclude `generate-style` — it's the theme component CSS

WordPress sites using GeneratePress ship all component CSS under `id="generate-style-inline-css"`. This **is** the custom theme CSS containing `.site-header`, `.main-navigation`, `.post-card`, `.image-box`, `.subnav`, `.pagination` — your target rules.

Safe exclude list for WordPress-internal-only blocks:

```python
EXCLUDE_IDS = ['wp-img-auto-sizes', 'wp-emoji-styles', 'classic-theme-styles', 'global-styles']
```

Keep `generate-style`, `gp-dep-*`, and `wp-custom-css` — they carry the actual component styles. A single `'generate-style'` in the exclude list silences ALL component extraction with no error.

### 10. Technique: @media body filtering to exclude WordPress block CSS

When matching @media rules by selector alone (`@media` in `sel`), you capture ALL media queries — including those from WordPress core blocks and Elementor. These inflate output 5–10×.

Filter: check the BODY (content between `{}`) for component selectors before including:

```python
if sel.startswith('@media'):
    body = rule[rule.find('{'):]   # everything after first {
    has_target = any(cs in body for cs in COMPONENT_SELECTORS)
    has_wp_block = any(wp in body for wp in [
        '.wp-block', '.wp-lightbox', '.blocks-gallery', '.elementor-'
    ])
    if has_target and not has_wp_block:
        keep(rule)
```

WordPress block patterns to exclude from @media bodies:
| Pattern | Source |
|---------|--------|
| `.wp-block-` | WordPress core blocks |
| `.wp-lightbox-` | WordPress lightbox |
| `.blocks-gallery-` | WordPress gallery |
| `.elementor-` | Elementor page builder |

### 11. Edge case: `@medianot` parse error

Some WordPress-generated CSS contains `@medianot(prefers-reduced-motion) { ... }` (missing space between `@media` and `not`). Browsers handle this leniently but regex-based parsers may split incorrectly. If your parser produces malformed rules around `not(prefers-reduced-motion)`, special-case it: treat `@medianot` as a valid `@media` prefix and keep the rule body as-is (it contains animation keyframes for reduced-motion preferences).

## File structure for extracted CSS

```
dep-css-master.css
├── 1. FONTS & IMPORTS        — @import + @font-face
├── 2. CSS VARIABLES           — :root { --* }
├── 3. HEADER                  — site-header, nav, menu
├── 4. HERO                    — sliders, image-box, swiper
├── 5. POST CARDS              — post-card, grid, entry blocks
├── 6. CATEGORY BADGE          — cat-links, category badges
├── 7. SUBNAV                  — subnav, dropdowns, sub-menu
├── 8. FOOTER                  — site-footer, copyright
├── 9. ARTICLE                 — entry-content, WP blocks
├── 10. PAGINATION             — page-numbers, nav-links
├── 11. RESPONSIVE             — @media blocks
├── 12. OTHER                  — Bootstrap, plugins, utilities
└── 13. KEYFRAMES              — @keyframes animations
```
