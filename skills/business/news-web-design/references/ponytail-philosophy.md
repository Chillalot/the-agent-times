# Ponytail Philosophy — Full Reference

> Source: [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) (72k⭐)
> Tagline: "The best code is the code you never wrote."

## The 7-Rung Ladder

Before writing any code, stop at the first rung that holds:

```
1. Does this need to exist?          → No → skip it (YAGNI)
2. Already in this codebase?         → Reuse it, don't rewrite
3. Standard library does it?         → Use it
4. Native platform feature?          → Use it
5. Installed dependency does it?     → Use it
6. Can this be one line?             → One line
7. Only then: write the minimum that works
```

The ladder runs **after** you understand the problem, not instead of it:
read the code the change touches and trace the real flow before picking a rung.
Lazy about the solution, never about reading.

## Benchmark Results

Measured on real Claude Code sessions editing tiangolo's full-stack-fastapi-template
(FastAPI + React), scored on `git diff`. Twelve feature tickets, n=4, Haiku 4.5.

| Metric | ponytail vs baseline | caveman | "YAGNI + one-liners" |
|--------|---------------------|---------|----------------------|
| LOC | **-54%** | -20% | -33% |
| Tokens | **-22%** | +7% | -14% |
| Cost | **-20%** | +3% | -21% |
| Time | **-27%** | +2% | -30% |
| Safe | **100%** | 100% | 95% |

ponytail is the **only** arm that cuts every metric and the only one that stays
fully safe while doing it.

## The Rules

### 1. No abstraction that wasn't requested
Don't create a component wrapper for `<input type="date">` — the browser has one.
Don't extract a utility function until you need it on 3+ call sites.

### 2. No new dependency if avoidable
Before `npm install`, check: does the standard library do it? Does the native
platform API do it? Is the 20-line inline version good enough?

### 3. No boilerplate nobody asked for
Don't add a build step, a configuration file, or a plugin unless the code
actually needs it.

### 4. Deletion over addition. Boring over clever.
When in doubt between adding a guard or deleting a code path, prefer deletion.
A plain `for` loop beats a generator pipeline if the latter makes the next
reviewer stop and think.

### 5. Shortest working diff wins
But only once you understand the problem. The smallest change in the wrong
place isn't lazy — it's a second bug.

### 6. ponytail: comments
Mark intentional simplifications with a `ponytail:` comment. If the shortcut
has a known ceiling (global lock, O(n²) scan, naive heuristic), the comment
names the ceiling and the upgrade path:

```python
# ponytail: linear scan, fine for <1000 items. Swap to dict lookup if perf matters.
items = [x for x in all_items if x.id == target_id]
```

### 7. Bug fix = root cause, not symptom
A report names a symptom. Grep every caller of the function you touch and fix
the shared function once — one guard there is a smaller diff than one per
caller, and patching only the path the ticket names leaves a sibling caller
still broken.

### 8. Non-trivial logic = one self-check
Leave ONE runnable check behind, the smallest thing that fails if the logic
breaks. An assert-based demo/self-check or one small test file. No frameworks,
no fixtures. Trivial one-liners need no test.

## Ponytail is Not Lazy About
- **Understanding the problem** — read it fully and trace the real flow before
  picking a rung. A small diff you don't understand is laziness dressed up as
  efficiency.
- **Input validation at trust boundaries**
- **Error handling that prevents data loss**
- **Security**
- **Accessibility**
- **Calibration real hardware needs** — the platform is never the spec ideal,
  a clock drifts, a sensor reads off
- **Anything explicitly requested**

## Before / After Examples

These are real model output from benchmark runs, same model (Claude Haiku 4.5),
same prompt, verbatim.

### Date Picker
**Without (404 lines):** Install flatpickr, write wrapper component, add stylesheet
```html
<!-- Without: 404 lines of flatpickr + wrapper + stylesheet -->
```
**With (23 lines):**
```html
<!-- ponytail: browser has one -->
<input type="date">
```

### Deep Clone
**Without:** `npm install lodash` + `import { cloneDeep }`
```js
import { cloneDeep } from "lodash";
const copy = cloneDeep(original);
```
**With:**
```js
// ponytail: structuredClone does this
const copy = structuredClone(original);
```
Handles Date, Map, Set, ArrayBuffer, RegExp, circular references — everything
JSON.parse/stringify silently drops. Available in every browser since 2022 and
Node.js since v17.

### Debounce Search
**Without (116 lines):** Debounce utility function + class wrapper + config object
```js
function debounce(func, delay) { /* 20 lines */ }
const debouncedSearch = debounce(handleSearch, 300);
// + loading state, error handling, HTML example, CSS styles
```

**With (10 lines):**
```js
const searchInput = document.querySelector('input[type="search"]');
let debounceTimer;
searchInput.addEventListener('input', (e) => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    fetch(`/api/search?q=${encodeURIComponent(e.target.value)}`)
      .then(r => r.json())
      .then(data => console.log(data));
  }, 300);
});
```
Skipped: debounce utility function, class wrapper, config object. setTimeout +
clearTimeout IS the debounce. Add a utility when you need it on 3+ inputs.

### CSV Sum
**Without (20 lines):** pandas DataFrame
**With (3 lines):**
```python
import csv
total = sum(float(row['amount']) for row in csv.DictReader(open('sales.csv')))
print(total)
```
Skipped: pandas, error handling, file closing. Add when the CSV is large,
malformed, or you need more analysis.

### Email Validation
**Without (75 lines):** Regex validator class + test + error messages
**With (3 lines):**
```html
<!-- ponytail: browser validates email -->
<input type="email">
```

## Native Browser APIs Cheat Sheet

| Over-engineered | Native alternative |
|----------------|-------------------|
| Date picker library | `<input type="date">` |
| Color picker component | `<input type="color">` |
| Email regex validation | `<input type="email">` |
| URL validation | `<input type="url">` |
| Number input + validation | `<input type="number" min max>` |
| Accordion JS | `<details>` / `<summary>` |
| Progress bar | `<progress>` |
| Modal/dialog | `<dialog>` + `showModal()` |
| Form validation library | Constraint Validation API (`checkValidity()`) |
| Lazy loading library | `<img loading="lazy">` |
| Smooth scroll JS | `scroll-behavior: smooth` CSS |
| Deep clone utility | `structuredClone()` |
| Debounce utility | `setTimeout`/`clearTimeout` (only extract at 3+ sites) |

## Related Skills in This Profile

- `news-web-design` — has a detailed **Kiến thức từ Ponytail** section with the
  7-rung ladder, rules, and native API substitutions applied to news design
- `news-writing-agent` — Ponytail approach for scraping-first writing:
  "scrape first, API second, manual third, never make up data"
