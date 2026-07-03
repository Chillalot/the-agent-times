#!/usr/bin/env python3
"""
Tech News Reporter — Công nghệ VN & Quốc tế
===========================================
Fetch RSS từ các nguồn công nghệ, đọc full content + ảnh,
dịch tiếng Anh → Việt (cho nguồn quốc tế), lưu article JSON.

Usage:
    python3 tech_news.py                              # Chạy đầy đủ
    python3 tech_news.py --test                       # Chạy thử 2 feeds đầu
    python3 tech_news.py --source vnexpress-so-hoa    # Chạy feed cụ thể
    python3 tech_news.py --no-scrape                  # Chỉ lấy RSS (không fetch content)
"""

import hashlib
import json
import os
import re
import sys
import time
import traceback
import urllib.error
import urllib.request
from datetime import datetime
from xml.etree import ElementTree as ET

# ─── Paths ───────────────────────────────────────────────────────────────────
SCRIPTS_DIR = os.path.expanduser("~/.hermes/profiles/meow/scripts")
REPORTS_DIR = os.path.expanduser("~/.hermes/profiles/meow/reports")

sys.path.insert(0, SCRIPTS_DIR)
import article_scraper as scraper

# ─── Feeds ───────────────────────────────────────────────────────────────────
FEEDS = {
    # ── Việt Nam ──
    "vnexpress-so-hoa": {
        "name": "VnExpress Số hóa",
        "url": "https://vnexpress.net/rss/so-hoa.rss",
        "source_type": "vietnam",
        "source_tag": "vnexpress",
        "lang": "vi",
    },
    "vnexpress-khoa-hoc": {
        "name": "VnExpress Khoa học",
        "url": "https://vnexpress.net/rss/khoa-hoc.rss",
        "source_type": "vietnam",
        "source_tag": "vnexpress",
        "lang": "vi",
    },
    # ── Quốc tế ──
    "techcrunch": {
        "name": "TechCrunch",
        "url": "https://techcrunch.com/feed/",
        "source_type": "international",
        "source_tag": "techcrunch",
        "lang": "en",
    },
    "wired": {
        "name": "Wired",
        "url": "https://www.wired.com/feed/rss",
        "source_type": "international",
        "source_tag": "wired",
        "lang": "en",
    },
    "theverge": {
        "name": "The Verge",
        "url": "https://www.theverge.com/rss/index.xml",
        "source_type": "international",
        "source_tag": "theverge",
        "lang": "en",
    },
}

# ─── Constants ───────────────────────────────────────────────────────────────
MAX_ITEMS_PER_FEED = 5
RSS_TIMEOUT = 20
CATEGORY = "technology"
CATEGORY_NAME = "💻 Công nghệ"
EMOJI = "💻"

# ─── RSS Fetch ───────────────────────────────────────────────────────────────

def fetch_rss(url, max_items=MAX_ITEMS_PER_FEED):
    """Fetch và parse RSS/Atom feed, trả về dict {error, items}."""
    import ssl

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                ),
                "Accept": "application/rss+xml, application/xml, text/xml, */*",
            },
        )
        with urllib.request.urlopen(req, timeout=RSS_TIMEOUT, context=ctx) as resp:
            data = resp.read()
    except Exception as e:
        return {"error": str(e), "items": []}

    raw_text = data.decode("utf-8", errors="replace")
    raw_text = raw_text.replace("\ufeff", "")

    try:
        root = ET.fromstring(raw_text.encode("utf-8"))
    except ET.ParseError as e:
        return {"error": f"Parse error: {e}", "items": []}

    items = []

    # ── Try RSS 2.0 ──
    for item in root.iter("item"):
        title = _strip_cdata(item.findtext("title", "")).strip()
        link = item.findtext("link", "").strip()
        desc_html = _strip_cdata(item.findtext("description", ""))
        desc = re.sub(r"<[^>]+>", "", desc_html).strip()
        # Also try content:encoded
        content_encoded = _strip_cdata(
            item.findtext("{http://purl.org/rss/1.0/modules/content/}encoded", "")
            or item.findtext("content:encoded", "")
        )
        pub_date = item.findtext("pubDate", "").strip()
        author = item.findtext("author", "").strip() or item.findtext("{http://purl.org/dc/elements/1.1/}creator", "").strip()

        if title:
            items.append({
                "title": title,
                "link": link,
                "desc": desc[:500] if desc else "",
                "pub_date": pub_date,
                "author": author,
                "content_encoded": content_encoded,
            })
        if len(items) >= max_items:
            break

    # ── Fallback: Atom ──
    if not items:
        NS_ATOM = "http://www.w3.org/2005/Atom"
        for entry in root.iter(f"{{{NS_ATOM}}}entry"):
            title_el = entry.find(f"{{{NS_ATOM}}}title")
            title = (title_el.text or "").strip() if title_el is not None else ""
            link_el = entry.find(f"{{{NS_ATOM}}}link")
            link = (link_el.get("href", "") or "").strip() if link_el is not None else ""
            desc_el = (
                entry.find(f"{{{NS_ATOM}}}summary")
                or entry.find(f"{{{NS_ATOM}}}content")
            )
            desc_raw = (desc_el.text or "") if desc_el is not None else ""
            desc = re.sub(r"<[^>]+>", "", desc_raw).strip()
            pub_el = entry.find(f"{{{NS_ATOM}}}published") or entry.find(f"{{{NS_ATOM}}}updated")
            pub_date = (pub_el.text or "").strip() if pub_el is not None else ""
            author_el = entry.find(f"{{{NS_ATOM}}}author/{{{NS_ATOM}}}name")
            author = (author_el.text or "").strip() if author_el is not None else ""

            if title:
                items.append({
                    "title": title,
                    "link": link,
                    "desc": desc[:500],
                    "pub_date": pub_date,
                    "author": author,
                    "content_encoded": "",
                })
            if len(items) >= max_items:
                break

    return {"error": None, "items": items}


def _strip_cdata(text):
    """Remove CDATA wrapper if present."""
    if not text:
        return ""
    return re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", text)


# ─── Translation ─────────────────────────────────────────────────────────────

_translator = None


def get_translator():
    """Lazy-init googletrans Translator."""
    global _translator
    if _translator is None:
        try:
            from googletrans import Translator

            _translator = Translator()
        except Exception as e:
            print(f"  ⚠️  Không thể khởi tạo googletrans: {e}")
            _translator = False
    return _translator if _translator is not False else None


def translate_text(text, src="en", dest="vi"):
    """Dịch text sang tiếng Việt. Trả về text gốc nếu lỗi."""
    if not text or len(text.strip()) < 3:
        return text
    translator = get_translator()
    if translator is None:
        return text
    try:
        result = translator.translate(text[:5000], src=src, dest=dest)
        if result and result.text:
            return result.text
        return text
    except Exception:
        return text


# ─── Article Helpers ─────────────────────────────────────────────────────────


def make_article_id(source_key, title, source_url):
    """Tạo article ID duy nhất từ md5."""
    raw = f"{source_key}_{title[:80]}_{source_url}"
    h = hashlib.md5(raw.encode()).hexdigest()[:8]
    today = datetime.now().strftime("%Y-%m-%d")
    return f"tech_{source_key}_{today}_{h}"


def build_fallback_html(title_vi, desc_vi, source_url, lead_image=None):
    """Tạo HTML fallback khi không scrape được full content."""
    parts = []
    if lead_image:
        parts.append(
            f'<figure style="margin:0 0 24px;">'
            f'<img src="{lead_image}" alt="{title_vi}" '
            f'style="width:100%;max-width:100%;border-radius:8px;" />'
            f'</figure>'
        )
    parts.append(f"<h2>{title_vi}</h2>")
    if desc_vi:
        for para in desc_vi.split("\n"):
            para = para.strip()
            if para:
                parts.append(f"<p>{para}</p>")
    parts.append(
        f'<p style="margin-top:24px;font-size:14px;color:#888;">'
        f'📎 Nguồn: <a href="{source_url}" target="_blank" rel="noopener">{source_url}</a>'
        f'</p>'
    )
    parts.append(
        f'<p style="font-size:13px;color:#aaa;">'
        f'🤖 Bài viết được tổng hợp tự động bởi AI.'
        f'</p>'
    )
    return "\n".join(parts)


def save_article_json(article_data):
    """Lưu article JSON vào REPORTS_DIR. Bỏ qua nếu đã tồn tại."""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    fpath = os.path.join(REPORTS_DIR, f"{article_data['id']}.json")
    if os.path.exists(fpath):
        print(f"    ⏭️  Đã tồn tại: {os.path.basename(fpath)}")
        return fpath, False
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(article_data, f, ensure_ascii=False, indent=2)
    return fpath, True


# ─── Process One Article ─────────────────────────────────────────────────────


def process_article(item, feed_key, feed_info, do_scrape=True):
    """
    Xử lý một bài RSS:
      - VN sources: scrape full content (đã tiếng Việt)
      - International: scrape + dịch sang Việt
    Trả về article dict hoặc None.
    """
    title_orig = item["title"]
    desc_orig = item.get("desc", "")
    link = item.get("link", "")
    source_name = feed_info["name"]
    source_type = feed_info["source_type"]
    source_tag = feed_info["source_tag"]
    lang = feed_info.get("lang", "en")
    is_international = (source_type == "international")

    if not title_orig:
        return None

    print(f"\n  📄 [{source_name}] {title_orig[:90]}")

    # ── Translate title / desc if international ──
    if is_international:
        print(f"    🔤 Đang dịch tiêu đề...", end="", flush=True)
        title_vi = translate_text(title_orig, src="en", dest="vi")
        print(f" ✅")
        print(f"    🇻🇳 {title_vi[:90]}")
        desc_vi = translate_text(desc_orig, src="en", dest="vi") if desc_orig else ""
    else:
        title_vi = title_orig
        desc_vi = desc_orig

    # ── Scrape full content ──
    content_html = None
    lead_image_url = None

    if do_scrape and link:
        print(f"    📡 Đang đọc bài viết...", end="", flush=True)
        try:
            scraped = scraper.fetch_article(link)

            if scraped.get("success"):
                raw_html = scraped.get("content_html", "")
                lead_image_url = scraped.get("lead_image")

                if raw_html:
                    if is_international:
                        # Dịch nội dung sang tiếng Việt
                        raw_text = (
                            BeautifulSoup(raw_html, "html.parser").get_text()
                            if "BeautifulSoup" in dir()
                            else _extract_text(raw_html)
                        )
                        if raw_text and len(raw_text) > 80:
                            translated_content = translate_text(
                                raw_text[:4000], src="en", dest="vi"
                            )
                            if translated_content and translated_content != raw_text[:4000]:
                                paras = [
                                    f"<p>{p.strip()}</p>"
                                    for p in translated_content.split("\n")
                                    if p.strip()
                                ]
                                content_html = "\n".join(paras)
                            else:
                                content_html = raw_html
                        else:
                            content_html = raw_html
                    else:
                        # VN source: giữ nguyên HTML
                        content_html = raw_html

                print(f" ✅ ({scraped.get('text_length', 0)} chars)")
            else:
                print(f" ⚠️ {scraped.get('error', 'lỗi')}")
        except Exception as e:
            print(f" ⚠️ {e}")

    # ── If scraping produced content but we need BeautifulSoup ──
    if content_html is None and do_scrape and link:
        # Import here for fallback use
        try:
            from bs4 import BeautifulSoup as BS

            if scraped_local := scraper.fetch_article(link):
                if scraped_local.get("success"):
                    raw_html = scraped_local.get("content_html", "")
                    if raw_html and is_international:
                        raw_text = BS(raw_html, "html.parser").get_text()
                        if raw_text and len(raw_text) > 80:
                            translated = translate_text(
                                raw_text[:4000], src="en", dest="vi"
                            )
                            if translated:
                                content_html = "\n".join(
                                    f"<p>{p.strip()}</p>"
                                    for p in translated.split("\n")
                                    if p.strip()
                                )
                    elif raw_html:
                        content_html = raw_html
        except Exception:
            pass

    # ── Fallback HTML ──
    if not content_html:
        content_html = build_fallback_html(title_vi, desc_vi, link, lead_image_url)

    # ── Build article dict ──
    today = datetime.now().strftime("%Y-%m-%d")
    today_display = datetime.now().strftime("%A, %d/%m/%Y")

    # Extract plain text for excerpt + word count
    try:
        from bs4 import BeautifulSoup as BS

        text_plain = BS(content_html, "html.parser").get_text()
    except Exception:
        text_plain = re.sub(r"<[^>]+>", "", content_html).strip()

    excerpt = text_plain[:200].strip().replace("\n", " ")
    if len(text_plain) > 200:
        excerpt += "..."

    # Tags
    tags = ["công-nghệ"]
    tags.append("việt-nam" if source_type == "vietnam" else "quốc-tế")
    tags.append(source_tag)

    # Add specific tech tags
    text_lower = text_plain.lower()
    title_lower = title_orig.lower()
    tech_keywords = {
        "ai": "ai",
        "artificial intelligence": "ai",
        "trí tuệ nhân tạo": "ai",
        "machine learning": "ai",
        "học máy": "ai",
        "startup": "startup",
        "blockchain": "blockchain",
        "crypto": "crypto",
        "bitcoin": "crypto",
        "security": "bảo-mật",
        "bảo mật": "bảo-mật",
        "hack": "bảo-mật",
        "apple": "apple",
        "google": "google",
        "microsoft": "microsoft",
        "meta": "meta",
        "facebook": "meta",
        "amazon": "amazon",
        "spacex": "space",
        "nasa": "space",
        "vũ trụ": "space",
        "electric": "xe-điện",
        "ev": "xe-điện",
        "tesla": "xe-điện",
        "smartphone": "mobile",
        "điện thoại": "mobile",
        "iphone": "mobile",
        "android": "mobile",
    }
    for kw, tag in tech_keywords.items():
        if kw in text_lower or kw in title_lower:
            if tag not in tags:
                tags.append(tag)

    article_id = make_article_id(feed_key, title_orig, link)

    article = {
        "id": article_id,
        "title": f"💻 {title_vi}",
        "date": today,
        "date_display": today_display,
        "category": CATEGORY,
        "category_name": CATEGORY_NAME,
        "emoji": EMOJI,
        "excerpt": excerpt,
        "content_html": content_html,
        "tags": tags,
        "sources": [link] if link else [],
        "lead_image": lead_image_url,
        "word_count": len(text_plain.split()),
        "source_url": link,
        "source_name": source_name,
        "source_type": source_type,
        "original_title": title_orig,
        "author": item.get("author", ""),
        "generated_at": datetime.now().isoformat(),
    }
    return article


def _extract_text(html_str):
    """Extract plain text from HTML without BeautifulSoup."""
    text = re.sub(r"<script[^>]*>.*?</script>", "", html_str, flags=re.DOTALL)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ─── Main ────────────────────────────────────────────────────────────────────


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Tech News Reporter — Công nghệ VN & Quốc tế"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Chạy thử 2 feeds đầu (nhanh, ít bài)",
    )
    parser.add_argument(
        "--source",
        type=str,
        default=None,
        help="Chạy feed cụ thể (vd: vnexpress-so-hoa, techcrunch)",
    )
    parser.add_argument(
        "--no-scrape",
        action="store_true",
        help="Chỉ lấy RSS, không fetch full content",
    )
    parser.add_argument(
        "--max-items",
        type=int,
        default=MAX_ITEMS_PER_FEED,
        help=f"Số bài tối đa mỗi feed (mặc định: {MAX_ITEMS_PER_FEED})",
    )
    args = parser.parse_args()

    # Chọn feeds
    feed_keys = list(FEEDS.keys())
    if args.test:
        feed_keys = feed_keys[:2]
        print("🧪 TEST MODE — 2 feeds đầu\n")
    elif args.source:
        if args.source in FEEDS:
            feed_keys = [args.source]
        else:
            print(f"❌ Không tìm thấy feed: {args.source}")
            print(f"   Có sẵn: {', '.join(FEEDS.keys())}")
            return 1

    do_scrape = not args.no_scrape

    # Header
    print("╔══════════════════════════════════════════════╗")
    print("║  💻 TECH NEWS REPORTER                      ║")
    print(f"║  {datetime.now().strftime('%A, %d/%m/%Y')}               ║")
    print("╠══════════════════════════════════════════════╣")
    print(f"║  {len(feed_keys)} feeds • {'có scrape' if do_scrape else 'RSS only'}       ║")
    print("╚══════════════════════════════════════════════╝")
    print()

    stats = {"processed": 0, "saved": 0, "errors": 0, "skipped": 0}

    for feed_key in feed_keys:
        info = FEEDS[feed_key]
        source_name = info["name"]
        url = info["url"]

        print(f"\n{'='*60}")
        print(f"📡 {source_name} — {url}")
        print(f"{'='*60}")

        print(f"  📥 Fetch RSS...", end="", flush=True)
        result = fetch_rss(url, max_items=args.max_items)
        if result["error"]:
            print(f" ❌ {result['error']}")
            stats["errors"] += 1
            continue

        items = result["items"]
        if not items:
            print(f" ⚠️ Không có bài")
            stats["errors"] += 1
            continue
        print(f" ✅ {len(items)} bài")

        for i, item in enumerate(items):
            try:
                article = process_article(
                    item, feed_key, info, do_scrape=do_scrape
                )
                if article:
                    fpath, is_new = save_article_json(article)
                    status = "✅ MỚI" if is_new else "⏭️ SKIP"
                    print(
                        f"    {status}: {os.path.basename(fpath)} "
                        f"({article['word_count']} từ)"
                    )
                    stats["saved"] += 1 if is_new else 0
                else:
                    print(f"    ⚠️ Bỏ qua (thiếu title)")
                    stats["skipped"] += 1
                stats["processed"] += 1
            except Exception as e:
                print(f"    ❌ Lỗi: {e}")
                traceback.print_exc()
                stats["errors"] += 1

            if i < len(items) - 1:
                time.sleep(0.5)

        if feed_key != feed_keys[-1]:
            print(f"  ⏳ Nghỉ 2s...")
            time.sleep(2)

    # Summary
    print(f"\n{'='*60}")
    print(f"📊 TỔNG KẾT")
    print(f"{'='*60}")
    print(f"  📡 Số feeds:       {len(feed_keys)}")
    print(f"  📄 Đã xử lý:       {stats['processed']}")
    print(f"  ✅ Đã lưu mới:     {stats['saved']}")
    print(f"  ⏭️  Bỏ qua:         {stats['skipped']}")
    print(f"  ❌ Lỗi:            {stats['errors']}")
    print(f"  📁 Thư mục:        {REPORTS_DIR}")
    print(f"  ⏰ {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")

    if stats["saved"] > 0:
        print("\n📋 Bài viết mới trong thư mục reports:")
        tech_files = sorted(
            f
            for f in os.listdir(REPORTS_DIR)
            if f.startswith("tech_")
        )
        for fname in tech_files:
            print(f"  💻 {fname}")

    return 0 if stats["errors"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
