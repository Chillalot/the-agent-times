# Report JSON Schema — Data Format cho Article

> Mỗi báo cáo được lưu dưới dạng JSON trong `~/.hermes/profiles/meow/reports/`.  
> Flask app đọc các file này và render thành trang báo.

## Schema

```json
{
  "id": "daily-briefing_2026-07-03_152721",
  "title": "📊 BÁO CÁO KINH TẾ & CÔNG NGHỆ HÀNG NGÀY",
  "date": "2026-07-03",
  "date_display": "Thứ Sáu, 03/07/2026",
  "category": "daily-briefing",
  "category_name": "📰 Kinh tế & Công nghệ",
  "excerpt": "Tin tức kinh tế VN | GitHub trending repos | Góc pháp lý & thuế",
  "content_html": "<h2>📰 TIN TỨC...</h2><ul><li>...</li></ul>",
  "content_text": "Raw text version...",
  "tags": ["kinh-tế", "việt-nam", "github", "thuế"],
  "sources": ["https://vnexpress.net/..."],
  "word_count": 915,
  "emoji": "📰",
  "generated_at": "2026-07-03T15:27:21"
}
```

## Category Values

| category | category_name | emoji |
|----------|---------------|-------|
| `daily-briefing` | 📰 Kinh tế & Công nghệ | 📰 |
| `github` | 🐙 GitHub Radar | 🐙 |
| `legal` | ⚖️ Pháp lý & Thuế | ⚖️ |
| `affiliate` | 💰 Affiliate | 💰 |
| `fnb` | 🍗 F&B & Quán ăn | 🍗 |
| `economic` | 📊 Phân tích Kinh tế | 📊 |
| `market` | 📈 Thị trường | 📈 |

## Cách Article được tạo

1. Script (e.g., `daily_briefing.py`) chạy → output text
2. `run_and_save.py` bắt stdout → phân tích → tạo JSON + HTML
3. `raw_text_to_html()` chuyển text thành HTML với:
   - Headers (h2) cho các section
   - Unordered lists cho bullet points
   - Ordered lists cho numbered items
   - Links tự động phát hiện URL
   - Bỏ qua decorative borders (═╔╗╚╝ etc.)
4. JSON lưu vào `reports/` → Flask app serve ngay lập tức

## Template Variables (Flask Context)

```python
{
  "selected_date_iso": "2026-07-03",
  "selected_date_str": "Thứ Sáu, 03/07/2026",
  "selected_date_display": "Thứ Sáu, 03/07/2026",
  "prev_date": "2026-07-02",
  "next_date": None,  # None nếu là ngày mới nhất
  "today_iso": "2026-07-03",
  "all_dates": ["2026-07-03", "2026-07-02"],
  "active_nav": "home",
  "articles": [...],
  "category_name": None,  # Set khi filter
  "query": None,          # Set khi search
}
```
