---
name: design-master
description: "Universal design principles + UX psychology cho AI coding agents. Gồm Design-Craft (typography, color, spacing, layout, animation, anti-slop patterns) và Laws of UX (30 psychological rules: Hick, Fitts, Gestalt, Miller, Peak-End, Von Restorff, Jakob). Dùng khi thiết kế bất kỳ giao diện nào."
version: 1.0.0
author: Phương (merged từ FasalZein/design-craft + FasalZein/laws-of-ux)
tags: [design, ux, ui, typography, color, layout, animation, psychology, laws-of-ux]
---

# Design Master — Universal Design Principles + UX Psychology

## Khi nào dùng skill này
- Khi cần thiết kế giao diện từ đầu
- Khi cần đánh giá/cải thiện UI hiện tại
- Khi clone design từ website khác
- Khi cần đảm bảo UX đúng psychological principles
- LUÔN dùng skill này trước khi viết bất kỳ CSS/HTML nào

---

## PHẦN 1: DESIGN-CRAFT (HOW — Cách thiết kế)

### 1.1 Aesthetic Direction (TRƯỚC KHI CODE)
Commit to a specific design direction:
- **Purpose**: Problem này giải quyết gì? Ai dùng?
- **Tone**: Chọn 1: editorial/magazine (cho báo), brutally minimal, luxury, playful
- **Differentiation**: 1 điều người dùng nhớ về giao diện này

### 1.2 Anti-Slop Rules (CẤM)
| Pattern | Why |
|---------|-----|
| Gradient hero (xanh-tím) | #1 AI training pattern |
| Gradient text | Decorative vô dụng |
| Glassmorphism | Overrepresented in training data |
| 3-4 identical big-number cards | Generic SaaS template |
| Three identical icon-card grid | 90%+ template sites |
| Inter/Roboto/Arial mặc định | Không có brand consideration |
| Large rounded icons above headings | Templated |
| Cards inside cards | Visual redundancy |
| Purple-to-blue gradients | Cấm tuyệt đối |

### 1.3 Typography
- **Intentional font**: Không default Inter/Roboto/Arial. Alternatives: DM Sans, Instrument Sans, Plus Jakarta Sans, Geist
- **5-level scale**: Display (48px) → Heading (32px) → Body (16px) → Caption (13px) → Micro (11px)
- **Line height**: Body 1.5, Headings 1.2-1.3, Display 1.0-1.1
- **Line length**: 45-75ch (`max-w-prose` or `max-w-[65ch]`)
- **Body text**: `rem`/`em`, không `px`
- `tabular-nums` trên numeric data
- `text-balance` trên headings, `text-pretty` trên body
- Không quá 3 font weights per view
- Không disable zoom

### 1.4 Color — 3-Layer Token System
```css
/* Layer 1: Primitives — oklch */
--color-white: oklch(100% 0 0);
--color-navy-900: oklch(15% 0.05 250);
--color-accent: oklch(45% 0.15 250);

/* Layer 2: Semantic — ý nghĩa */
--bg: var(--color-white);
--text: var(--color-navy-900);
--accent: var(--color-accent);

/* Layer 3: Component — cụ thể */
--button-primary-bg: var(--accent);
--button-primary-text: var(--color-white);
```
- **60-30-10 rule**: 60% neutrals / 30% secondary / 10% accent
- **WCAG AA**: Contrast ≥ 4.5:1
- **Tint neutrals toward brand hue**: `oklch(95% 0.01 60)` không `#f5f5f5`
- **Dark mode**: Swap semantic layer, lighter surfaces (no shadows), desaturated accents, font weight 350 vs 400
- CấM: pure black/white large areas, gray text on colored backgrounds

### 1.5 Spacing — 4px Base Grid
| Token | px | Dùng cho |
|-------|-----|---------|
| `--space-1` | 4px | Tight within atoms |
| `--space-2` | 8px | Between group items |
| `--space-4` | 16px | Between groups |
| `--space-6` | 24px | Between sections |
| `--space-8` | 32px | Page margins |
| `--space-12` | 48px | Large sections |
| `--space-16` | 64px | Page margins large |

- **Visual rhythm**: Tight trong group, generous giữa sections
- **Gestalt proximity**: Spacing tạo groups mạnh hơn borders
- **Cấm**: `p-[13px]`, `gap-[7px]`, triple-layer responsive padding
- **Cấm**: same padding everywhere, cards inside cards

### 1.6 Layout
- Grid/Flexbox, KHÔNG absolute positioning for structure
- `h-dvh` — KHÔNG `h-screen`
- `safe-area-inset` cho fixed elements
- Left-align với asymmetric layouts
- **Progressive disclosure**: Steps > 12-field forms. Sheets for detail. Expand/collapse for optional.
- **Một primary action per view** — two equal CTAs = hierarchy failure

### 1.7 Animation & Motion
| Duration | Usage |
|----------|-------|
| 100-150ms | Feedback (press, toggle, tooltip) |
| 200-300ms | State changes (menu, hover, accordion) |
| 300-500ms | Layout (modal, drawer, panel) |
| 500-800ms | Entrance (page load, hero) |

- **Easing**: `--ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1)` default
- **Only animate**: `transform` + `opacity`. Cấm `blur()`/`backdrop-filter`
- **prefers-reduced-motion**: Reset ALL animations
- **Button press**: `active:scale-[0.97]`, 100ms
- **List stagger**: 30-50ms/item, max 5-8
- **Cấm**: bounce/elastic easing, decorative animation, will-change outside scope

### 1.8 Interaction States
Mọi interactive element PHẢI có:
| State | Implementation |
|-------|---------------|
| Default | Resting appearance |
| Hover | Subtle lift, color shift |
| Focus | `:focus-visible` ring (2px solid, 2px offset) |
| Active | `active:scale-[0.97]` |
| Disabled | `opacity-50 pointer-events-none` |
| Loading | Inline spinner, disable interaction |
| Error | Border + inline message |

### 1.9 Empty States
- **MUST have**: warm message + primary CTA + optional illustration
- BAD: "No results" | GOOD: "No articles yet. Your daily briefing will appear here at 8:00 AM."
- **Errors**: What happened? Why? How to fix? Include retry + recovery action
- Không humor, không jargon (500, ECONNREFUSED)

### 1.10 Self-Check (TRƯỚC KHI KẾT THÚC)
1. **No slop** — Zero gradients, glassmorphism, glow, hero metrics, identical cards
2. **No hardcoded colors** — All from semantic tokens
3. **No arbitrary values** — No `text-[13px]`, `p-[17px]`
4. **Focus visible** — Every interactive element has `:focus-visible`
5. **Empty/error states** — Every list has empty state
6. **No `transition-all`** — Specify `transition-colors`, `transition-transform`, `transition-opacity`

---

## PHẦN 2: LAWS OF UX (WHY — Tại sao thiết kế như vậy)

### 2.1 Reduce Decision & Memory Cost
- **Hick's Law**: Decision time ↑ với số lượng choices. Limit primary nav ≤7 items. Highlight recommended choice.
- **Miller's Law**: Working memory ~7±2 items. Chunking: group related inputs (address block, payment block).
- **Cognitive Load**: Mỗi element thêm vào cạnh tranh attention. Pre-fill known values. Show only needed for current step.
- **Choice Overload**: Too many options → paralysis. Smart defaults. Filters/search cho catalogs lớn.
- **Tesler's Law**: Irreducible complexity exists — push it into system, not user. Auto-detect timezones.
- **Occam's Razor**: Simplest solution preferred. Remove until further removal breaks function.

### 2.2 Build on Familiarity
- **Jakob's Law**: Users spend time on OTHER sites — expect yours to work same way. Logo top-left → home. Search top-right. Settings behind gear icon.
- **Mental Model**: Match user's model, not data model. "Shopping cart" works because people understand physical carts.
- **Paradox of Active User**: Users start immediately, never read manuals. Make primary action obvious. Inline help > onboarding tutorials.

### 2.3 Direct Attention & Create Emphasis
- **Von Restorff Effect**: Item that differs is most remembered. ONE visually distinct CTA. Restraint — if everything is emphasized, nothing is.
- **Selective Attention**: Users filter out irrelevant info. Guide with visual hierarchy. Banner blindness — don't put important content where ads go.
- **Serial Position Effect**: First + last items remembered best. Most important nav at edges, least in middle.
- **Aesthetic-Usability Effect**: Beautiful interfaces perceived as more usable. But aesthetics can MASK usability problems.

### 2.4 Shape Experience & Memory
- **Peak-End Rule**: Judge experience by peak moment + ending. Invest disproportionately in (1) most intense moment + (2) final step. Negative peaks remembered more vividly.
- **Zeigarnik Effect**: Incomplete tasks remembered better. Use progress indicators. "3 of 5 steps complete" → motivation.
- **Goal-Gradient Effect**: Motivation ↑ as approaching goal. Show progress visually. Artificial progress ("You're 20% done!") works.
- **Flow**: Remove unnecessary friction. Immediate feedback. Don't interrupt mid-task with modals.

### 2.5 Motor Cost & Timing
- **Fitts's Law**: Time = f(distance, size). Targets ≥44×44px. Primary actions near natural resting position. Destructive actions small + far from primary.
- **Doherty Threshold**: Feedback <400ms keeps flow. Skeleton screens for longer waits. Every submit button MUST have loading state (spinner + "Processing...").
- **Parkinson's Law**: Tasks expand to fill time. Smart defaults reduce completion time. Design UI to match expected task time.

### 2.6 Perception & Grouping (Gestalt)
- **Proximity**: Nearby elements perceived as related. PRIMARY tool for visual organization.
- **Similarity**: Visually similar = related function. Navigation links look alike.
- **Common Region**: Elements in bounded area = group. But prefer proximity first.
- **Uniform Connectedness**: Connected elements = more related. Stronger than proximity.
- **Prägnanz**: People interpret complex visuals as simplest form. Simplify.

### 2.7 Robustness
- **Postel's Law**: Liberal in what you accept, conservative in what you send. Accept varied input formats. Validate on submit, not per-keystroke.
- **Pareto Principle**: 80% of effects from 20% of causes. Focus on primary flow; edge cases can be adequate.
- **Cognitive Bias**: Users satisfice, not optimize. Design for real behavior. Use ethically: pre-select best option.

### Decision Matrix
| Decision | Apply |
|----------|-------|
| How many nav items? | Hick + Miller: ≤7, highlight default |
| Form too long? | Chunking + Tesler: multi-step |
| Where to place CTA? | Fitts + Serial Position: big, edge |
| What to emphasize? | Von Restorff: ONE thing different |
| Multi-step flow? | Goal-Gradient + Zeigarnik: show progress |
| Users confused? | Jakob: match convention |
| Slow response? | Doherty: feedback <400ms |
| Post-flow satisfaction? | Peak-End: invest in peak + end |
| Grouping unclear? | Proximity > Similarity > Common Region |
| Where to invest? | Pareto: 20% features = 80% users |

---

## Self-Check TRƯỚC KHI HOÀN THÀNH
1. **No decision overload** — 1 primary button per view. Nav ≤7 items visible.
2. **Conventions respected** — Logo top-left. Search header. Gear for settings.
3. **Progress visible** — Multi-step has indicator.
4. **Feedback on every action** — Every button has hover + focus + loading state.
5. **Attention guided** — Exactly ONE distinct element per view.
6. **Errors recoverable** — Accept varied input, inline validation, inline errors.
7. **Peak+end designed** — Final screen deliberately crafted.
8. **No anti-slop** — Check ALL anti-slop rules.
9. **Colors from tokens** — No hardcoded colors in HTML.
10. **Animation correct** — Only transform+opacity, correct timing.

---

## Practical Notes (từ session thực tế với Long)

### Khi frontend không thay đổi dù đã sửa CSS
1. Kiểm tra CSS version string trong `<link>` — có tăng `v=` không?
2. Start server (pkill → restart) — cache có thể giữ CSS cũ
3. Dùng curl verify exact properties: `curl -s http://localhost:5050/static/style.css | grep -- '--accent'`
4. Kiểm tra page SIZE: nếu size không đổi, template chưa được update
5. **Cache-busting**: thêm random version string + `no-cache` headers

### Khi clone design từ site khác
- LUÔN extract HTML + CSS từ thật (fetch site → grep class names → extract style blocks)
- **Pitfall**: CSS-only change không đủ — cần restructure templates để thêm các section mới (hero image-box, post-card layout, subnav)
- Verify bằng cách so sánh page size trước/sau (tăng = có thêm content)
- Dùng curl confirm structure: `curl -s http://localhost:5050/ | grep -c 'image-box\|post-card'`

### Tone preference (Axios-style)
Long thích phong cách **Axios** (clean, minimal, serif headlines, sans-serif body, blue accent, lots of whitespace). Áp dụng khi thiết kế news/reporting site.

### Anti-overwrite
Khi dispatch subagents, KHÔNG cho 2 agent cùng sửa CSS hoặc templates. Xem `multi-agent-orchestration` skill.

## References
- `references/dep-com-vn-clone-reference.md` — Complete design tokens từ dep.com.vn
- `multi-agent-orchestration` skill — Cách dispatch subagents theo đúng phases
- `news-web-design` skill — Frontend implementation cho báo điện tử
- `website-cloner` (with cloakbrowser-integration reference) — Cách scrape, extract CSS, clone website
