# Article HTML Cleaning Pipeline

## Vấn đề
Readability và các scraper trả về HTML bẩn:
- `<html><body><div>` wrappers
- VnExpress-specific classes: `fck_detail`, `title-detail mt20`, `Normal`, `description`
- `rel="dofollow"` attributes trên links
- Inline `style="border-radius:2px"` và các style khác
- Empty tags `<div></div>`, `<span></span>`

## Giải pháp — clean_html() function

```python
import re

def clean_html(html_content):
    """Clean scraped HTML for professional display"""
    # Remove html/body/div wrappers from readability
    html_content = re.sub(r'<html><body><div>', '', html_content)
    html_content = re.sub(r'</div></body></html>', '', html_content)
    # Remove all class attributes
    html_content = re.sub(r'\s+class="[^"]*?"', '', html_content)
    # Remove empty tags
    html_content = re.sub(r'<([a-z0-9]+)[^>]*?>\s*</\1>', '', html_content)
    # Remove rel attributes
    html_content = re.sub(r'\s+rel="[^"]*?"', '', html_content)
    # Remove style attributes
    html_content = re.sub(r'\s+style="[^"]*?"', '', html_content)
    # Normalize whitespace
    html_content = re.sub(r'\n\s*\n', '\n\n', html_content)
    html_content = html_content.strip()
    return html_content
```

## Image Extraction — 6-Step Fallback Chain

```python
def extract_lead_image(soup, url):
    # 1. OG image: meta[property="og:image"]
    # 2. Twitter image: meta[name="twitter:image"]
    # 3. Article containers (.entry-content, article, .post-content) — check data-lazy-src too, skip images under 200px
    # 4. figure img — first figure-contained image
    # 5. Any img with width > 200
    # 6. First meaningful img (fallback)
```

## Article Save — Lead Image at Top

```python
# Build HTML with image at top
html_parts = []
if fetched.get("lead_image"):
    html_parts.append(
        f'<figure style="margin:0 0 24px;">'
        f'<img src="{fetched["lead_image"]}" alt="{title}" style="width:100%;max-width:100%;" />'
        f'</figure>'
    )
html_parts.append(fetched["content_html"])
full_html = "\n".join(html_parts)
```

## File tham khảo
- Script đầy đủ: `~/.hermes/profiles/meow/scripts/article_scraper.py`
