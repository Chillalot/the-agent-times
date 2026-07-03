# Design Tokens Implemented — Phương's Daily v8

Tokens thực tế đã implement cho frontend báo điện tử. Dùng làm reference khi clone design.

## CSS Custom Properties — 3-Layer System

### Layer 1: Primitives
```css
--color-white: #ffffff;
--color-black: #121212;
--color-navy: #032435;
--color-gray-50: #f7f8f9;
--color-gray-100: #f0f0f0;
--color-gray-200: #e2e2e2;
--color-gray-300: #dee2e6;
--color-gray-400: #b2b2be;
--color-gray-500: #8a8a8a;
--color-gray-600: #575760;
--color-gray-700: #495057;
--color-accent: #032435;
--color-accent-hover: #032741;
```

### Layer 2: Semantic
```css
--bg: var(--color-white);
--bg-warm: var(--color-gray-50);
--bg-section: var(--color-gray-100);
--bg-card: var(--color-white);
--text: #222222;
--text-gray: var(--color-gray-600);
--text-light: var(--color-gray-400);
--border: var(--color-gray-300);
--border-light: var(--color-gray-100);
--accent: var(--color-accent);
--accent-hover: var(--color-accent-hover);
```

### Layer 3: Component
```css
--font-heading: 'Be Vietnam Pro', Arial, Helvetica, sans-serif;
--font-body: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
--font-ui: var(--font-body);
```

## Spacing — 4px Base Grid
```css
--space-1: 4px;   /* Tight within atoms */
--space-2: 8px;   /* Between group items */
--space-3: 12px;
--space-4: 16px;  /* Between groups */
--space-5: 20px;
--space-6: 24px;  /* Between sections */
--space-8: 32px;  /* Page margins */
--space-10: 40px;
--space-12: 48px; /* Large sections */
--space-16: 64px; /* Page margins large */
```

## Key Component Patterns
- **Hero**: `.featured-card` — 2-column CSS Grid (text left, image right)
- **Card grid**: 3-column → 2-column (768px) → 1-column (<768px)
- **Article body**: max-width 700px, font-size 17px, line-height 1.75
- **Headline**: font-heading, 34px (desktop) → 26px (mobile), font-weight 700
- **Badge**: border-left 2px accent, padding-left 6px, uppercase 9px
- **Button**: flat, no border-radius, bg accent, hover darker
