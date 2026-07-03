# News Site Design Patterns — Live Research Summary

Research conducted July 2026 via live browser inspection. Full 1313-line report at `/home/chillalot/news-layout-research.md`.

## Key Takeaways

| Feature | Best Practice | Source |
|---------|--------------|--------|
| Grid system | Guardian's named-line CSS Grid (12 cols @ 60px desktop) | Guardian |
| Card pattern | flex-column, border-bottom separator, absolute overlay link | NYT + Guardian |
| Vietnamese typography | Merriweather (headline) + Arial (body) | VnExpress |
| Article width | 680px for optimal Vietnamese readability | VnExpress |
| Dark mode | CSS custom properties + `[data-theme]` attribute | Guardian |
| Breakpoints | 740/980/1140/1300px with named grid lines | Guardian |

## Guardian Grid Details (Live CSS)

```
.dcr-lypmm {
  display: grid;
  grid-auto-rows: auto;
  column-gap: 10px;
}
```

### Breakpoints and Column Counts
| Viewport | Columns | Grid Template |
|----------|---------|---------------|
| <740px | 4 equal | `[viewport-start] 0px [content-start main-column-start] repeat(4, minmax(0px, 1fr)) [content-end main-column-end] 0px [viewport-end]` |
| 740-979px | 12×40px | `minmax(0px, 1fr) repeat(12, 40px) minmax(0px, 1fr)` |
| 980-1139px | 12×60px | `minmax(0px, 1fr) repeat(12, 60px) minmax(0px, 1fr)` |
| 1140+px | 12×60px | Container 1140px or 1300px |

## Container Widths
- 740px → 980px → 1140px → 1300px (Guardian)
- 1200px (NYT header), 1605px (NYT sections)
- 1130px with 71px margin (VnExpress)

## Dark Mode Approaches
| Site | Method | Detail |
|------|--------|--------|
| Guardian | `[data-theme]` + CSS vars | Most robust, supports light/dark/auto |
| NYT | Class toggle `.tpl-dark` | Simple toggle, no `prefers-color-scheme` |
| BBC | `@media (prefers-color-scheme)` | Auto only, no manual toggle |
| VnExpress | None | All colors hardcoded, no dark mode |

## Article Typography Comparison
| Site | Headline | Body | UI |
|------|----------|------|----|
| NYT | 40px Times New Roman | 22px Times New Roman | 11px nyt-franklin |
| Guardian | 2.25rem GH Guardian Headline | 1.0625rem Guardian Egyptian | 12px GuardianTextSans |
| VnExpress | 32px Merriweather | 18px/28.8px Arial | 14px Arial |
| BBC | 20-28px BBC Reith | 14-16px BBC Reith | 12px BBC Reith |
