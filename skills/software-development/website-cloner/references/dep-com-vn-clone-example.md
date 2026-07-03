# dep.com.vn Clone Example

## Source
- URL: https://dep.com.vn/
- CMS: WordPress + Bootstrap
- Fetched: 440KB HTML
- Extracted: 20 colors, 22 fonts, 50+ CSS variables, 28 component patterns

## Design Tokens Applied

| Token | Old Value | New Value (from dep.com.vn) |
|-------|-----------|---------------------------|
| `--accent` | `#b80000` (NYT red) | `#032435` (navy) |
| `--accent-hover` | `#8f0000` | `#032741` |
| `--text` | `#121212` | `#222222` |
| `--text-gray` | `#5a5a5a` | `#575760` |
| `--text-light` | `#8a8a8a` | `#a09f9f` |
| `--bg-warm` | `#faf8f5` | `#f7f8f9` |
| `--font-serif` | Georgia | Be Vietnam Pro |
| `--font-sans` | system-ui | Be Vietnam Pro |
| `--max-width` | 1200px | 1040px |
| `--shadow` | single layer | multi-layer rgba(50,50,93,.25) |

## Google Font Added
```html
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700&display=swap" rel="stylesheet">
```

## Dark Mode
| Token | Old Value | New Value |
|-------|-----------|-----------|
| `--bg` | `#0a0a1a` | `#0d1929` |
| `--bg-card` | `#14142e` | `#152029` |
| `--accent` | `#6c5ce7` | `#4a9eff` |
| `--btn-bg` | `#6c5ce7` | `#4a9eff` |

## Files Modified
1. `~/.hermes/profiles/meow/frontend/static/style.css` — CSS variables updated
2. `~/.hermes/profiles/meow/frontend/templates/base.html` — Google Font CDN added

## Result
- Giao diện chuyển từ tông NYT đỏ → tông navy trầm (dep.com.vn style)
- Chữ Việt Nam đẹp hơn với Be Vietnam Pro (font designed cho Vietnamese)
- Container hẹp hơn (1040px) → dễ đọc hơn
- Shadow mượt hơn với multi-layer shadow
