# GSAP Animation Patterns — Full Reference

> Source: [greensock/gsap-skills](https://github.com/greensock/gsap-skills) (10.8k⭐)
> Official skills: gsap-core | gsap-timeline | gsap-scrolltrigger | gsap-plugins
> gsap-utils | gsap-react | gsap-performance | gsap-frameworks
> GSAP is 100% free (all plugins including Club GSAP are free since Webflow acquisition).

## Core Tween Methods
```javascript
gsap.to(targets, vars)       // current → vars (most common)
gsap.from(targets, vars)     // vars → current (entrances)
gsap.fromTo(t, from, to)     // explicit start and end (no reading of current)
gsap.set(targets, vars)      // apply immediately (duration 0)
```

All return a **Tween** instance. Store it for playback control:
```javascript
const tween = gsap.to('.box', { x: 100, duration: 1 });
tween.pause(); tween.play(); tween.reverse();
tween.kill(); tween.progress(0.5); tween.time(0.2);
```

## Transform Aliases (prefer over raw transform string)

Always use **camelCase** for CSS properties (e.g. `backgroundColor`, `marginTop`).

| GSAP property | Equivalent CSS | Notes |
|---------------|---------------|-------|
| `x`, `y`, `z` | translateX/Y/Z | default unit px |
| `xPercent`, `yPercent` | translateX/Y in % | works on SVG |
| `scale`, `scaleX`, `scaleY` | scale | `scale` sets both X and Y |
| `rotation` | rotate | default deg, or `"1.25rad"` |
| `rotationX`, `rotationY` | 3D rotate | rotationZ = rotation |
| `skewX`, `skewY` | skew | deg or rad string |
| `transformOrigin` | transform-origin | e.g. `"left top"` |
| `autoAlpha` | opacity + visibility | **prefer over opacity alone** |
| `svgOrigin` (SVG only) | SVG global coordinate space | `"250 100"` no percentages |

### autoAlpha — Why Prefer It
When `autoAlpha: 0`, GSAP also sets `visibility: hidden` → no pointer events.
When non-zero, `visibility: inherit`. Avoids invisible elements blocking clicks.
```javascript
gsap.to('.fade', { autoAlpha: 0, duration: 0.5 });
```

### Directional Rotation
```javascript
gsap.to('.element', { rotation: '-170_short' });  // 20° clockwise
// _short = shortest path, _cw = clockwise, _ccw = counter-clockwise
gsap.to('.element', { rotationX: '+=30_cw' });
```

### clearProps
Remove inline styles from the element when the tween completes — useful when
a CSS class should take over after animation. Clearing any transform property
clears the **entire** transform.
```javascript
gsap.to('.box', { x: 100, duration: 0.5, clearProps: 'x' });
gsap.to('.fade', { autoAlpha: 0, duration: 0.5, clearProps: 'visibility' });
// clearProps: 'all' or true = remove all inline styles
```

### Relative Values
```javascript
gsap.to('.class', { x: '-=20' });   // 20px less than current
gsap.to('.class', { x: '+=20' });   // 20px more
gsap.to('.class', { x: '*=2' });    // double
gsap.to('.class', { x: '/=2' });    // half
```

### Function-Based Values
Called **once per target** when the tween first renders.
```javascript
gsap.to('.item', {
  x: (i, target, targetsArray) => i * 50,  // 0, 50, 100, 150...
  stagger: 0.1
});
```

## Easing — Complete Reference

### Built-in Eases
```javascript
"none"               // linear
"power1"             // gradual (mild)
"power2"             // medium (default feel) ← GSAP DEFAULT
"power3"             // strong
"power4"             // steepest (dramatic)
"back"               // overshoot
"bounce"             // bouncing ball
"circ"               // circular
"elastic"            // rubber band
"expo"               // exponential
"sine"               // sinusoidal
```

Each comes in 4 variants: `base` (same as `.out`), `.in`, `.out`, `.inOut`.
Default if unspecified = `.out`.

### Ease Selection Guide
| Use | Ease | Why |
|-----|------|-----|
| Subtle UI, metadata | `power1.out` | Nearly imperceptible |
| Cards, fade-in, general | `power2.out` | Natural, starts fast/eases out |
| Headers, hero sections | `power3.out` | More pronounced |
| Major entrances | `power4.out` | Dramatic, slow finish |
| Featured hero, pop effect | `back.out(1.7)` | Overshoots then settles |
| Badges, notifications | `elastic.out(1,0.3)` | Bouncy, attention-grabbing |
| Scroll-linked, progress bars | `none` | Linear = 1:1 with scroll |

### CustomEase (plugin, free)
```javascript
const myEase = CustomEase.create('my-ease', '.17,.67,.83,.67'); // cubic-bezier
const hop = CustomEase.create('hop', 'M0,0 C0,0 0.056,0.442 0.175,0.442 ...');
gsap.to('.item', { x: 100, ease: myEase, duration: 1 });
```

## Stagger Patterns
```javascript
// Simple
gsap.to('.item', { y: -20, stagger: 0.1 });

// Object syntax — fine-grained control
gsap.to('.card', {
  opacity: 1, y: 0,
  stagger: {
    amount: 0.5,        // total duration of stagger
    from: 'random'      // 'start' | 'center' | 'end' | 'edges' | index
  },
  ease: 'power2.out'
});
```

## gsap.defaults() — Project-Wide Defaults
```javascript
gsap.defaults({ duration: 0.6, ease: 'power2.out' });
// All tweens after this inherit these defaults
```

## gsap.matchMedia() — Responsive + Accessibility (v3.11+)

**The official pattern** — handles responsive breakpoints AND prefers-reduced-motion
in one API. Animations are automatically reverted when media query stops matching.

### Basic — Single Query
```javascript
const mm = gsap.matchMedia();
mm.add('(min-width: 800px)', () => {
  gsap.from('.card', { x: 100, stagger: 0.1 });
  return () => { /* optional cleanup */ };
});
```

### Advanced — Multiple Conditions (preferred pattern)
```javascript
const mm = gsap.matchMedia();
mm.add({
  isDesktop: '(min-width: 800px)',
  isMobile: '(max-width: 799px)',
  reduceMotion: '(prefers-reduced-motion: reduce)'
}, (context) => {
  const { isDesktop, reduceMotion } = context.conditions;

  // All animations in this block are managed by matchMedia
  gsap.to('.box', {
    rotation: isDesktop ? 360 : 180,
    duration: reduceMotion ? 0 : 2  // skip animation entirely when reduceMotion
  });

  return () => { /* cleanup when no condition matches */ };
});

// mm.revert() — cleanup all (e.g. on component unmount)
// gsap.matchMediaRefresh() — re-run all handlers (e.g. after toggling motion pref)
```

**Why gsap.matchMedia() instead of raw window.matchMedia:**
- Animations auto-revert when media query stops matching
- All ScrollTriggers inside are also cleaned up
- Supports nested responsive breakpoints
- No manual ScrollTrigger.refresh() on resize

## Timeline Sequencing

### Position Parameter (third argument)
```javascript
const tl = gsap.timeline({ defaults: { duration: 0.5, ease: 'power2.out' } });
tl.to('.a', { x: 100 }, 0);            // at 0 seconds
tl.to('.b', { y: 50 }, '+=0.5');       // 0.5s after last end
tl.to('.c', { opacity: 0 }, '<');       // same start as previous
tl.to('.d', { scale: 2 }, '<0.2');     // 0.2s after previous start
tl.to('.e', { y: -20 }, 'label+=0.3'); // 0.3s after label
```

### Labels
```javascript
const tl = gsap.timeline();
tl.addLabel('intro', 0);
tl.to('.a', { x: 100 }, 'intro');
tl.addLabel('outro', '+=0.5');
tl.to('.b', { opacity: 0 }, 'outro');
tl.play('outro');
tl.tweenFromTo('intro', 'outro');
```

### Nesting Timelines
```javascript
const master = gsap.timeline();
const child = gsap.timeline();
child.to('.a', { x: 100 }).to('.b', { y: 50 });
master.add(child, 0);
master.to('.c', { opacity: 0 }, '+=0.2');
```

### Playback Control
```javascript
tl.play() / tl.pause() / tl.reverse()
tl.restart()                     // from start
tl.time(2)                       // seek to 2s
tl.progress(0.5)                 // seek to 50%
tl.kill()                        // kill timeline + children
```

## ScrollTrigger Patterns

### Setup
```javascript
gsap.registerPlugin(ScrollTrigger);   // must be called once
```

### Pattern 1: Basic Trigger
```javascript
gsap.to('.box', {
  x: 500, duration: 1,
  scrollTrigger: {
    trigger: '.box',
    start: 'top center',
    end: 'bottom center',
    toggleActions: 'play reverse play reverse'
  }
});
```

### Pattern 2: Timeline + ScrollTrigger with Scrub
```javascript
const tl = gsap.timeline({
  scrollTrigger: {
    trigger: '.section',
    start: 'top top',
    end: '+=1000',
    scrub: 1,      // linked to scroll with 1s smooth catch-up
    pin: true,     // pin the trigger element
    markers: false // remove in production!
  }
});
tl.to('.visual', { scale: 1.1 })
  .to('.text', { y: -30 }, '<');
```

### Pattern 3: ScrollTrigger.batch() — IntersectionObserver Alternative
```javascript
ScrollTrigger.batch('.card', {
  interval: 0.1,
  batchMax: 4,
  onEnter: (batch) => gsap.to(batch, {
    opacity: 1, y: 0, stagger: 0.1, overwrite: true
  }),
  onLeaveBack: (batch) => gsap.set(batch, {
    opacity: 0, y: 50, overwrite: true
  }),
  start: 'top 80%',
  end: 'bottom 20%'
});
```

### Pattern 4: Standalone ScrollTrigger (No Animation)
```javascript
ScrollTrigger.create({
  trigger: '#progress-bar',
  start: 'top top',
  end: 'bottom 50%+=100px',
  onUpdate: (self) => {
    // self.progress (0-1), self.direction
    updateProgressBar(self.progress);
  }
});
```

### Pattern 5: Horizontal Scroll (containerAnimation)
```javascript
const scrollingEl = document.querySelector('.horizontal-wrap');
const scrollTween = gsap.to(scrollingEl, {
  xPercent: () => -(scrollingEl.scrollWidth - window.innerWidth),
  ease: 'none',  // ← REQUIRED for containerAnimation
  scrollTrigger: {
    trigger: scrollingEl.parentNode,
    pin: true,
    start: 'top top',
    end: '+=3000'
  }
});

// Nest other triggers based on the horizontal movement:
gsap.to('.nested-item', {
  y: 100,
  scrollTrigger: {
    containerAnimation: scrollTween,  // ← links to horizontal tween
    trigger: '.nested-wrapper',
    start: 'left center',
    toggleActions: 'play none none reset'
  }
});
```

### ScrollTrigger Best Practices (from official skill)
- ✅ Register plugin once: `gsap.registerPlugin(ScrollTrigger)`
- ✅ Put ScrollTrigger on timeline or top-level tween, NOT on child tweens
- ✅ Use **scrub** for scroll-linked progress OR **toggleActions** for discrete play/reverse — never both
- ✅ Call `ScrollTrigger.refresh()` after DOM/layout changes (new content, images, fonts)
- ✅ Create ScrollTriggers top-to-bottom on the page; set `refreshPriority` when dynamic
- ✅ Use `ease: 'none'` on horizontal animations using `containerAnimation`
- ❌ Don't nest ScrollTriggered animations inside parent timelines
- ❌ Don't leave `markers: true` in production
- ❌ Don't use `scrub` and `toggleActions` together
- ❌ Don't forget `ScrollTrigger.refresh()` after layout changes

### Cleanup
```javascript
ScrollTrigger.getAll().forEach(t => t.kill());
ScrollTrigger.getById('my-id')?.kill();
```

## gsap.utils — Helper Functions

All on `gsap.utils.*`. Omit the value argument to get a reusable function.

### Clamp & Range
```javascript
gsap.utils.clamp(0, 100, 150);             // 100
gsap.utils.mapRange(0, 100, 0, 500, 50);   // 250
gsap.utils.normalize(0, 100, 50);           // 0.5
```

### Interpolate
```javascript
gsap.utils.interpolate(0, 100, 0.5);                  // 50
gsap.utils.interpolate('#ff0000', '#0000ff', 0.5);    // mid color
gsap.utils.interpolate({ x: 0 }, { x: 100 }, 0.5);   // { x: 50 }
```

### Random & Snap
```javascript
gsap.utils.random(-100, 100);                        // number in range
gsap.utils.random(['red', 'blue', 'green']);          // random element
gsap.utils.random(0, 500, 5, true);                   // reusable function, snapped to 5
gsap.utils.snap(10, 23);                              // 20
gsap.utils.snap([0, 100, 200], 150);                  // 100 or 200 (nearest)

// String form in tween vars:
gsap.to('.box', { x: 'random(-100, 100, 5)', duration: 1 });
```

### Pipe & Distribute
```javascript
const fn = gsap.utils.pipe(
  (v) => gsap.utils.normalize(0, 100, v),
  (v) => gsap.utils.snap(0.1, v)
);

// distribute — grid-aware value spread
gsap.to('.class', {
  scale: gsap.utils.distribute({
    base: 0.5, amount: 2.5, from: 'center'
  })
});
```

### Wrap
```javascript
gsap.utils.wrap(0, 360, 370);    // 10 (cyclic)
gsap.utils.wrapYoyo(0, 100, 150); // 50 (bounce back)
```

### Arrays & Selectors
```javascript
const q = gsap.utils.selector(containerRef);
q('.box');                              // scoped to container

gsap.utils.toArray('.item');            // array from selector
gsap.utils.toArray('.item', container); // scoped

gsap.utils.shuffle([1, 2, 3, 4]);      // random order
```

## Performance Tips (from gsap-performance)
- ✅ Animate `x`/`y` instead of `left`/`top` (GPU composited)
- ✅ Use `autoAlpha` instead of `opacity` (avoids invisible blocking elements)
- ✅ Kill tweens on unmount (React/Vue/Svelte cleanup)
- ✅ Use `gsap.matchMedia()` for responsive + prefers-reduced-motion
- ❌ Don't animate `width`/`height` when `scale` achieves the same effect
- ❌ Don't forget `ScrollTrigger.refresh()` after dynamic layout changes

## React Patterns (from gsap-react)
```javascript
import { useGSAP } from '@gsap/react';
// or gsap.registerPlugin(useGSAP);

// Preferred: useGSAP hook — auto cleanup on unmount
useGSAP(() => {
  gsap.to(ref.current, { x: 100, duration: 1 });
}, { scope: containerRef });

// Manual approach:
// useEffect(() => {
//   const ctx = gsap.context(() => { ... }, containerRef);
//   return () => ctx.revert();
// }, []);
```

## Official Do Nots (compiled from all 8 skills)
- ❌ Animate layout-heavy properties (width, height, top, left) when transforms work
- ❌ Use both `svgOrigin` and `transformOrigin` on the same SVG element
- ❌ Rely on `immediateRender: true` when stacking multiple `from()`/`fromTo()` tweens
- ❌ Use invalid/non-existent ease names
- ❌ Chain animations with `delay` when a timeline can sequence them
- ❌ Nest ScrollTriggered animations inside parent timelines
- ❌ Use `scrub` and `toggleActions` together
- ❌ Use ease other than `'none'` with `containerAnimation` (breaks 1:1 scroll mapping)
- ❌ Leave `markers: true` in production
- ❌ Forget `ScrollTrigger.refresh()` after layout changes
