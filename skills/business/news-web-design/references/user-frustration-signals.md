# User Frustration Signals — Design Quality

> **Context:** The user said "skill thiết kế của bạn chưa ngon lắm", "code của bạn cũng còn cứng ngắc", "có thay đổi gì đâu" — these are FIRST-CLASS skill signals, not just complaints.

## Signal → Root Cause → Fix

| Signal | Root Cause | Immediate Fix |
|--------|-----------|---------------|
| "Chưa ngon lắm" | CSS-only change, no template restructure | Rewrite ALL 4 files (CSS + 3 templates) |
| "Có thay đổi gì đâu" | Variables updated but no visual diff | Check page in browser, verify each component |
| "Code cứng ngắc" | Missing hover states, transitions too fast | Add hover/active styles, 0.3s+ transitions |
| "Bạn update chưa vậy" | Server not restarted after changes | pkill + restart + browser refresh |

## Prevention Checklist (before saying "done")

1. □ All 4 files changed? (style.css, base.html, index.html, article.html)
2. □ Server restarted? (pkill + python3 app.py)
3. □ Browser hard-refreshed? (Ctrl+F5, not just F5)
4. □ 3 visual differences visible to naked eye?
5. □ CSS variables used in ≥3 places each?
6. □ Hover states feel smooth (≥0.3s transition)?
7. □ Mobile responsive looks intentional?
