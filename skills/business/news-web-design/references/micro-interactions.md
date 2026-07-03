# Micro-Interactions Reference

## CSS Transitions Cheat Sheet

### Common Durations
```css
/* Ultra fast — instant feedback */
transition: transform 0.1s ease;

/* Fast — hover/tap */
transition: all 0.2s ease;

/* Normal — panel slide, theme switch */
transition: all 0.3s ease;

/* Slow — emphasis, zoom */
transition: all 0.4s cubic-bezier(0.2, 0, 0, 1);
```

### Custom Easing
```css
/* Custom ease-out: nhanh đầu, chậm cuối — tự nhiên nhất */
cubic-bezier(0.2, 0, 0, 1)

/* Ease-out mặc định (hơi cứng ở cuối) */
ease-out

/* Mượt hơn ease-out, cho chuyển động vật lý */
cubic-bezier(0.4, 0, 0.2, 1)
```

### Hover Effects cho Cards
```css
/* Nâng lên + shadow */
.card {
  transition: transform 0.25s cubic-bezier(0.2,0,0,1),
              box-shadow 0.25s cubic-bezier(0.2,0,0,1);
}
.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}

/* Border highlight */
.card-link {
  color: var(--text-gray);
  transition: color 0.2s ease;
}
.card-link:hover {
  color: var(--accent);
}
```

### Active/Click States
```css
.button:active {
  transform: scale(0.96);
  transition: transform 0.1s ease;  /* phải nhanh hơn hover */
}
```

### Theme Switch — Critical Pattern
```css
/* Áp dụng cho mọi element có màu thay đổi theo theme */
/* Dùng chung transition để đồng bộ */
* {
  /* KHÔNG dùng all — performance */
  transition: background-color 0.3s ease,
              color 0.3s ease,
              border-color 0.3s ease,
              box-shadow 0.3s ease;
}
```

## Smooth Loading Patterns

### Skeleton Screen
```css
.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}
@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### Content Fade-in
```css
.content {
  opacity: 0;
  animation: contentFadeIn 0.5s ease-out forwards;
}
@keyframes contentFadeIn {
  to { opacity: 1; }
}
```

## Vietnamese-Specific Tips
- Vietnamese text với diacritics cần line-height lớn hơn (1.6-1.85) để không bị overlapping
- Font Arial render diacritics tốt hơn serif fonts ở cỡ nhỏ (<14px)
- Line-height cho body text nên là 1.8 (cao hơn English standard 1.5) — VnExpress dùng 28.8px với font 18px (1.6)
