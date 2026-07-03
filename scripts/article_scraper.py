#!/usr/bin/env python3
"""
Article Scraper — Đọc nội dung từ URL báo, trích ảnh, lưu thành article JSON
Dùng readability-lxml (Mozilla algorithm) + requests
"""
import sys, os, json, re, time, hashlib
from datetime import datetime
from urllib.parse import urlparse
import requests
from readability import Document
from bs4 import BeautifulSoup

REPORTS_DIR = os.path.expanduser("~/.hermes/profiles/meow/reports")

USER_AGENTS = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
]

CATEGORY_MAP = {
    "kinh-doanh": "economic", "kinh tế": "economic", "gdp": "economic",
    "thuế": "legal", "pháp luật": "legal", "pháp lý": "legal", "giấy phép": "legal",
    "github": "github", "công nghệ": "github", "ai": "github", "automation": "github",
    "ăn": "fnb", "cơm": "fnb", "gà": "fnb", "nhà hàng": "fnb", "quán": "fnb",
    "affiliate": "affiliate", "kiếm tiền": "affiliate", "shop": "affiliate",
}

CATEGORY_NAMES = {
    "economic": {"name": "📊 Phân tích Kinh tế", "emoji": "📊"},
    "legal": {"name": "⚖️ Pháp lý & Thuế", "emoji": "⚖️"},
    "github": {"name": "🐙 Công nghệ", "emoji": "🐙"},
    "fnb": {"name": "🍗 F&B & Quán ăn", "emoji": "🍗"},
    "affiliate": {"name": "💰 Affiliate", "emoji": "💰"},
    "daily-briefing": {"name": "📰 Kinh tế & Công nghệ", "emoji": "📰"},
}


def detect_category(title, text):
    combined = (title + " " + text).lower()
    for keyword, cat in CATEGORY_MAP.items():
        if keyword in combined:
            return cat
    return "daily-briefing"


def extract_lead_image(soup, url):
    """6-step image fallback chain"""
    # 1. OG image
    og = soup.find("meta", property="og:image")
    if og and og.get("content"):
        return og["content"]
    # 2. Twitter image
    tw = soup.find("meta", attrs={"name": "twitter:image"})
    if tw and tw.get("content"):
        return tw["content"]
    # 3. Article containers with data-lazy-src
    for container_sel in [".entry-content", "article", ".article-content", ".post-content", ".main-content"]:
        container = soup.select_one(container_sel)
        if container:
            for img in container.find_all("img"):
                src = img.get("src") or img.get("data-lazy-src") or img.get("data-src") or ""
                if src and not src.startswith("data:") and len(src) > 20:
                    w = img.get("width")
                    if (w and w.isdigit() and int(w) > 200) or not w:
                        if "icon" not in src.lower() and "logo" not in src.lower():
                            if src.startswith("//"): src = "https:" + src
                            elif src.startswith("/"):
                                parsed = urlparse(url)
                                src = f"{parsed.scheme}://{parsed.netloc}{src}"
                            return src
    # 4. figure img
    for fig in soup.find_all("figure"):
        img = fig.find("img")
        if img:
            src = img.get("src") or img.get("data-src") or ""
            if src and not src.startswith("data:") and len(src) > 20:
                if src.startswith("//"): src = "https:" + src
                elif src.startswith("/"):
                    parsed = urlparse(url)
                    src = f"{parsed.scheme}://{parsed.netloc}{src}"
                return src
    # 5. Any img with width > 200
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src") or ""
        w = img.get("width")
        if w and w.isdigit() and int(w) > 200 and src and not src.startswith("data:") and len(src) > 20:
            if "icon" not in src.lower() and "logo" not in src.lower():
                if src.startswith("//"): src = "https:" + src
                elif src.startswith("/"):
                    parsed = urlparse(url)
                    src = f"{parsed.scheme}://{parsed.netloc}{src}"
                return src
    # 6. Fallback: first meaningful image
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src") or ""
        if src and not src.startswith("data:") and len(src) > 30:
            if "icon" not in src.lower() and "logo" not in src.lower():
                if src.startswith("//"): src = "https:" + src
                elif src.startswith("/"):
                    parsed = urlparse(url)
                    src = f"{parsed.scheme}://{parsed.netloc}{src}"
                return src
    return None


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


def fetch_article(url, retries=2):
    """Fetch article content từ URL"""
    headers = {
        "User-Agent": USER_AGENTS[0],
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "vi-VN,vi;q=0.9,en;q=0.8",
    }
    
    for attempt in range(retries + 1):
        try:
            if attempt > 0:
                headers["User-Agent"] = USER_AGENTS[(hash(url) + attempt) % len(USER_AGENTS)]
            
            r = requests.get(url, headers=headers, timeout=30)
            r.raise_for_status()
            r.encoding = 'utf-8'
            html = r.text
            
            # Readability extraction
            doc = Document(html)
            title = doc.title()
            
            # Title fallback chain
            full_soup = BeautifulSoup(html, "html.parser")
            h1 = full_soup.find("h1")
            if h1 and h1.get_text(strip=True):
                h1_text = h1.get_text(strip=True)
                if len(title) < 15 or len(h1_text) > len(title):
                    title = h1_text
            if (not title or len(title) < 10) and full_soup.title:
                title = full_soup.title.get_text(strip=True)
            
            content_html = doc.summary()
            
            # Content fallback if too short
            content_soup = BeautifulSoup(content_html, "html.parser")
            text_len = len(content_soup.get_text(strip=True))
            
            if text_len < 500:
                for sel in ["article", ".entry-content", ".article-content", ".post-content", ".main-content"]:
                    container = full_soup.select_one(sel)
                    if container:
                        for junk in container.find_all(["script", "style", "nav", "aside", "footer", "header"]):
                            junk.decompose()
                        content_html = str(container)
                        break
            
            # Clean the HTML
            content_html = clean_html(content_html)
            
            # Extract lead image from original HTML (not cleaned)
            lead_image = extract_lead_image(full_soup, url)
            
            # Extract sources
            sources = []
            for a in full_soup.find_all("a", href=True):
                href = a["href"]
                if href.startswith("http") and len(href) > 20:
                    sources.append(href)
            
            return {
                "title": title,
                "content_html": content_html,
                "lead_image": lead_image,
                "sources": sources[:10],
                "text_length": len(content_html),
                "success": True,
            }
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403 and attempt < retries:
                time.sleep(2)
                continue
            return {"success": False, "error": str(e)}
        except requests.exceptions.ConnectionError as e:
            if attempt < retries:
                time.sleep(3)
                continue
            return {"success": False, "error": f"Connection: {e}"}
        except Exception as e:
            if attempt < retries:
                time.sleep(1)
                continue
            return {"success": False, "error": str(e)}
    
    return {"success": False, "error": "Max retries exceeded"}


def save_as_article(url, fetched, category=None):
    """Lưu fetched content thành article JSON"""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    date_display = now.strftime("%A, %d/%m/%Y")
    
    title = fetched["title"]
    
    if not category:
        category = detect_category(title, fetched["content_html"])
    
    cat_info = CATEGORY_NAMES.get(category, {"name": "📰 Báo cáo", "emoji": "📰"})
    
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    article_id = f"article_{date_str}_{url_hash}"
    
    # Build HTML with image at top
    html_parts = []
    if fetched.get("lead_image"):
        html_parts.append(
            f'<figure style="margin:0 0 24px;">'
            f'<img src="{fetched["lead_image"]}" '
            f'alt="{title}" '
            f'style="width:100%;max-width:100%;" />'
            f'</figure>'
        )
    
    html_parts.append(fetched["content_html"])
    full_html = "\n".join(html_parts)
    
    # Excerpt from cleaned text
    text_content = BeautifulSoup(fetched["content_html"], "html.parser").get_text()
    excerpt = text_content[:200].strip().replace("\n", " ")
    if len(text_content) > 200:
        excerpt += "..."
    
    # Tags
    tags = []
    text_lower = text_content.lower()
    if any(w in text_lower for w in ["kinh tế", "gdp", "tăng trưởng"]):
        tags.append("kinh-tế")
    if any(w in text_lower for w in ["thuế", "pháp", "cấm xuất cảnh"]):
        tags.append("pháp-lý")
    if "trump" in text_lower:
        tags.append("thế-giới")
    if any(w in text_lower for w in ["apple", "nvidia", "công nghệ"]):
        tags.append("công-nghệ")
    if not tags:
        tags.append("tin-tức")
    
    article = {
        "id": article_id,
        "title": title,
        "date": date_str,
        "date_display": date_display,
        "category": category,
        "category_name": cat_info["name"],
        "emoji": cat_info["emoji"],
        "excerpt": excerpt,
        "content_html": full_html,
        "tags": tags,
        "sources": fetched.get("sources", [url]),
        "lead_image": fetched.get("lead_image"),
        "word_count": len(text_content.split()),
        "source_url": url,
        "generated_at": now.isoformat(),
    }
    
    os.makedirs(REPORTS_DIR, exist_ok=True)
    fpath = os.path.join(REPORTS_DIR, f"{article_id}.json")
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(article, f, ensure_ascii=False, indent=2)
    
    return fpath, article


def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
        category = sys.argv[2] if len(sys.argv) > 2 else None
        
        print(f"🔍 Đang đọc bài báo: {url}")
        fetched = fetch_article(url)
        
        if fetched["success"]:
            fpath, article = save_as_article(url, fetched, category)
            print(f"✅ Đã lưu: {article['title'][:80]}")
            print(f"📸 Ảnh: {'Có' if article.get('lead_image') else 'Không'}")
            print(f"📝 {article['word_count']} từ")
            return 0
        else:
            print(f"❌ Lỗi: {fetched.get('error')}")
            return 1
    else:
        url = input("🔗 URL: ").strip()
        if not url:
            return 1
        fetched = fetch_article(url)
        if fetched["success"]:
            fpath, article = save_as_article(url, fetched)
            print(f"\n✅ {article['title']}")
            print(f"📝 {article['word_count']} từ")
        else:
            print(f"\n❌ {fetched.get('error')}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
