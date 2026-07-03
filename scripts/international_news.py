#!/usr/bin/env python3
"""
International News Reporter — fetch RSS từ 10 nước + translate + viết báo
=======================================================================
Lấy tin kinh tế/quốc tế từ các nước lớn, dịch sang tiếng Việt,
tạo article JSON trong REPORTS_DIR.

Usage:
    python3 international_news.py                              # Chạy đầy đủ
    python3 international_news.py --test                       # Chạy thử 2 feeds đầu
    python3 international_news.py --country us,uk              # Chạy feeds chỉ định
    python3 international_news.py --country us --scrape        # Có fetch full content
"""

import hashlib
import json
import os
import re
import ssl
import sys
import time
import traceback
from datetime import datetime
from xml.etree import ElementTree as ET

import urllib.request
import urllib.error

# ─── Config ────────────────────────────────────────────────────────────────
SCRIPTS_DIR = os.path.expanduser("~/.hermes/profiles/meow/scripts")
REPORTS_DIR = os.path.expanduser("~/.hermes/profiles/meow/reports")

sys.path.insert(0, SCRIPTS_DIR)
import article_scraper as scraper

# ─── Feeds: 10 nước ─────────────────────────────────────────────────────────
FEEDS = {
    "us": {
        "name": "Mỹ",
        "url": "https://feeds.bbci.co.uk/news/business/rss.xml",
        "category": "economic",
        "tags": ["quốc-tế", "mỹ", "kinh-tế"],
    },
    "uk": {
        "name": "Anh",
        "url": "https://www.theguardian.com/world/rss",
        "category": "economic",
        "tags": ["quốc-tế", "anh", "kinh-tế"],
    },
    "japan": {
        "name": "Nhật Bản",
        "url": "https://www.japantimes.co.jp/feed/",
        "category": "economic",
        "tags": ["quốc-tế", "nhật-bản", "kinh-tế"],
    },
    "china": {
        "name": "Trung Quốc",
        "url": "https://www.scmp.com/rss/4/feed",
        "category": "economic",
        "tags": ["quốc-tế", "trung-quốc", "kinh-tế"],
    },
    "france": {
        "name": "Pháp",
        "url": "https://www.france24.com/en/rss",
        "category": "economic",
        "tags": ["quốc-tế", "pháp", "kinh-tế"],
    },
    "germany": {
        "name": "Đức",
        "url": "https://rss.dw.com/rdf/rss-en-business",
        "category": "economic",
        "tags": ["quốc-tế", "đức", "kinh-tế"],
    },
    "skorea": {
        "name": "Hàn Quốc",
        "url": "http://www.koreaherald.com/rss/feed.php",
        "category": "economic",
        "tags": ["quốc-tế", "hàn-quốc", "kinh-tế"],
    },
    "australia": {
        "name": "Úc",
        "url": "https://www.abc.net.au/news/feed/45910/rss.xml",
        "category": "economic",
        "tags": ["quốc-tế", "úc", "kinh-tế"],
    },
    "singapore": {
        "name": "Singapore",
        "url": "https://www.straitstimes.com/news/feed",
        "category": "economic",
        "tags": ["quốc-tế", "singapore", "kinh-tế"],
    },
    "india": {
        "name": "Ấn Độ",
        "url": "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
        "category": "economic",
        "tags": ["quốc-tế", "ấn-độ", "kinh-tế"],
    },
}

CATEGORY_NAMES = {
    "economic": "📊 Phân tích Kinh tế",
    "github": "🐙 Công nghệ",
    "daily-briefing": "📰 Kinh tế & Công nghệ",
}

MAX_ITEMS_PER_FEED = 5
RSS_TIMEOUT = 20
SCRAPE_TIMEOUT = 10  # max seconds per article scrape attempt

# ─── RSS Fetch ──────────────────────────────────────────────────────────────

def fetch_rss(url, max_items=MAX_ITEMS_PER_FEED):
    """Fetch và parse RSS/Atom feed, trả về dict {error, items}."""
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
        desc = _strip_cdata(item.findtext("description", ""))
        desc = re.sub(r"<[^>]+>", "", desc).strip()
        if title:
            items.append({"title": title, "link": link, "desc": desc[:500]})
        if len(items) >= max_items:
            break

    # ── Fallback: Atom ──
    if not items:
        for entry in root.iter("{http://www.w3.org/2005/Atom}entry"):
            title_el = entry.find("{http://www.w3.org/2005/Atom}title")
            title = title_el.text.strip() if title_el is not None and title_el.text else ""
            link_el = entry.find("{http://www.w3.org/2005/Atom}link")
            link = link_el.get("href", "").strip() if link_el is not None else ""
            desc_el = (
                entry.find("{http://www.w3.org/2005/Atom}summary")
                or entry.find("{http://www.w3.org/2005/Atom}content")
            )
            desc = re.sub(r"<[^>]+>", "", (desc_el.text or "") if desc_el is not None else "").strip()
            if title:
                items.append({"title": title, "link": link, "desc": desc[:500]})
            if len(items) >= max_items:
                break

    return {"error": None, "items": items}


def _strip_cdata(text):
    """Remove CDATA wrapper if present."""
    if not text:
        return ""
    return re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", text)


# ─── Translation ────────────────────────────────────────────────────────────

_translator = None

def get_translator():
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
    except Exception as e:
        print(f"  ⚠️  Lỗi dịch: {e}", end="")
        return text


# ─── Article Helpers ────────────────────────────────────────────────────────

COUNTRY_TAG = {
    "us": "mỹ", "uk": "anh", "japan": "nhật-bản", "china": "trung-quốc",
    "france": "pháp", "germany": "đức", "skorea": "hàn-quốc",
    "australia": "úc", "singapore": "singapore", "india": "ấn-độ",
}


def make_article_id(country_code, title, source_url):
    """Tạo article ID duy nhất từ md5."""
    raw = f"{country_code}_{title[:60]}_{source_url}"
    h = hashlib.md5(raw.encode()).hexdigest()[:8]
    today = datetime.now().strftime("%Y-%m-%d")
    return f"intl_{country_code}_{today}_{h}"


def build_article_html(title_vi, desc_vi, source_url, lead_image=None):
    """Tạo HTML content từ tiêu đề và mô tả đã dịch."""
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
        # Split into paragraphs
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
        f'🤖 Bài viết được dịch tự động bởi AI từ nguồn tin quốc tế.'
        f'</p>'
    )
    return "\n".join(parts)


def save_article_json(article_data, overwrite=False):
    """Lưu article JSON vào REPORTS_DIR. Nếu overwrite=False, bỏ qua nếu đã tồn tại."""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    fpath = os.path.join(REPORTS_DIR, f"{article_data['id']}.json")
    if os.path.exists(fpath):
        if overwrite:
            os.remove(fpath)  # remove old version so new content gets saved
        else:
            print(f"    ⏭️  Đã tồn tại: {os.path.basename(fpath)}")
            return fpath, False
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(article_data, f, ensure_ascii=False, indent=2)
    return fpath, True


# ─── Process One Article ────────────────────────────────────────────────────

def process_article(item, country_code, country_info, do_scrape=False):
    """
    Xử lý một bài RSS: dịch, tùy chọn fetch nội dung, lưu article JSON.
    Trả về dict article hoặc None.
    """
    title_en = item["title"]
    desc_en = item["desc"]
    link = item["link"]
    country_name = country_info["name"]
    category = country_info["category"]
    tags = list(country_info["tags"])

    if not title_en:
        return None

    print(f"\n  📄 [{country_name}] {title_en[:90]}")

    # ── 1. Translate ──
    print(f"    🔤 Đang dịch...", end="")
    title_vi = translate_text(title_en)
    desc_vi = translate_text(desc_en) if desc_en else (desc_en or "")
    print(f" ✅")
    print(f"    🇻🇳 {title_vi[:90]}")

    # ── 2. Optional: scrape full content ──
    content_html = None
    lead_image_url = None

    if do_scrape and link:
        print(f"    📡 Đang đọc bài viết...", end="", flush=True)
        try:
            scraped = scraper.fetch_article(link)

            if scraped.get("success"):
                raw_html = scraped.get("content_html", "")
                lead_image_url = scraped.get("lead_image")
                text_length = scraped.get("text_length", 0)

                if raw_html and text_length > 200:
                    from bs4 import BeautifulSoup
                    raw_text = BeautifulSoup(raw_html, "html.parser").get_text()
                    word_count = len(raw_text.split())

                    if word_count > 200:
                        # ── Translate full content ──
                        translated_text = translate_text(raw_text[:5000])

                        # ── Build HTML: ảnh ở đầu + <p> tags ──
                        html_parts = []
                        if lead_image_url:
                            html_parts.append(
                                f'<figure style="margin:0 0 24px;">'
                                f'<img src="{lead_image_url}" alt="{title_vi}" '
                                f'style="width:100%;max-width:100%;border-radius:8px;" />'
                                f'</figure>'
                            )
                        for para in translated_text.split("\n"):
                            para = para.strip()
                            if para:
                                html_parts.append(f"<p>{para}</p>")
                        # Add source attribution
                        html_parts.append(
                            f'<p style="margin-top:24px;font-size:14px;color:#888;">'
                            f'📎 Nguồn: <a href="{link}" target="_blank" rel="noopener">{link}</a>'
                            f'</p>'
                        )
                        html_parts.append(
                            f'<p style="font-size:13px;color:#aaa;">'
                            f'🤖 Bài viết được dịch tự động bởi AI từ nguồn tin quốc tế.'
                            f'</p>'
                        )
                        content_html = "\n".join(html_parts)
                        print(f" ✅ ({word_count} từ, {'📸 ảnh' if lead_image_url else 'không ảnh'})")
                    else:
                        print(f" ⚠️ bài ngắn ({word_count} từ, <200), dùng RSS")
                else:
                    print(f" ⚠️ nội dung ngắn ({text_length} chars), dùng RSS")
            else:
                print(f" ⚠️ {scraped.get('error', 'lỗi')}")
        except Exception as e:
            print(f" ⚠️ {e}")

    # ── 3. Fallback HTML ──
    if not content_html:
        content_html = build_article_html(title_vi, desc_vi, link, lead_image_url)

    # ── 4. Build article dict ──
    today = datetime.now().strftime("%Y-%m-%d")
    today_display = datetime.now().strftime("%A, %d/%m/%Y")
    text_plain = re.sub(r"<[^>]+>", "", content_html).strip()
    excerpt = text_plain[:200].strip().replace("\n", " ")
    if len(text_plain) > 200:
        excerpt += "..."

    cat_name = CATEGORY_NAMES.get(category, "📰 Tin quốc tế")
    article_id = make_article_id(country_code, title_en, link)

    ct = COUNTRY_TAG.get(country_code, country_code)
    if ct not in tags:
        tags.append(ct)

    article = {
        "id": article_id,
        "title": f"🌍 {country_name}: {title_vi}",
        "date": today,
        "date_display": today_display,
        "category": category,
        "category_name": cat_name,
        "emoji": "🌍",
        "excerpt": excerpt,
        "content_html": content_html,
        "tags": tags,
        "sources": [link] if link else [],
        "lead_image": lead_image_url,
        "word_count": len(text_plain.split()),
        "source_url": link,
        "source_country": country_name,
        "original_title": title_en,
        "generated_at": datetime.now().isoformat(),
    }
    return article


# ─── Main ───────────────────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(description="International News Reporter")
    parser.add_argument("--test", action="store_true",
                        help="Chạy thử 2 feeds đầu (nhanh, không scrape)")
    parser.add_argument("--country", type=str, default=None,
                        help="Chạy feeds chỉ định (vd: us,uk,japan)")
    parser.add_argument("--scrape", action="store_true",
                        help="Fetch full content từ link gốc (chậm hơn)")
    args = parser.parse_args()

    # Chọn feeds
    feed_keys = list(FEEDS.keys())
    if args.test:
        feed_keys = feed_keys[:2]
        print("🧪 TEST MODE — 2 feeds đầu (dịch RSS, không scrape)\n")
    elif args.country:
        selected = [c.strip().lower() for c in args.country.split(",")]
        feed_keys = [k for k in feed_keys if k in selected]
        if not feed_keys:
            print(f"❌ Không tìm thấy feeds: {args.country}")
            print(f"   Có sẵn: {', '.join(FEEDS.keys())}")
            return 1

    # Header
    print("╔══════════════════════════════════════════════╗")
    print("║  🌍 INTERNATIONAL NEWS REPORTER              ║")
    print(f"║  {datetime.now().strftime('%A, %d/%m/%Y')}               ║")
    print("╠══════════════════════════════════════════════╣")
    print(f"║  {len(feed_keys)}/{len(FEEDS)} nước • {'có scrape' if args.scrape else 'RSS + dịch'}      ║")
    print("╚══════════════════════════════════════════════╝")
    print()

    stats = {"processed": 0, "saved": 0, "errors": 0, "skipped": 0}

    for feed_key in feed_keys:
        info = FEEDS[feed_key]
        country_name = info["name"]
        url = info["url"]

        print(f"\n{'='*60}")
        print(f"📡 {country_name} — {url}")
        print(f"{'='*60}")

        print(f"  📥 Fetch RSS...", end="", flush=True)
        result = fetch_rss(url)
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
                article = process_article(item, feed_key, info, do_scrape=args.scrape)
                if article:
                    fpath, is_new = save_article_json(article, overwrite=args.scrape)
                    status = "✅ MỚI" if is_new else "⏭️ SKIP"
                    print(f"    {status}: {os.path.basename(fpath)} ({article['word_count']} từ)")
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
                time.sleep(0.5)  # nhẹ nhàng giữa các bài

        if feed_key != feed_keys[-1]:
            print(f"  ⏳ Nghỉ 2s...")
            time.sleep(2)

    # Summary
    print(f"\n{'='*60}")
    print(f"📊 TỔNG KẾT")
    print(f"{'='*60}")
    print(f"  🌐 Số nước:        {len(feed_keys)}")
    print(f"  📄 Đã xử lý:       {stats['processed']}")
    print(f"  ✅ Đã lưu mới:     {stats['saved']}")
    print(f"  ⏭️  Bỏ qua:         {stats['skipped']}")
    print(f"  ❌ Lỗi:            {stats['errors']}")
    print(f"  📁 Thư mục:        {REPORTS_DIR}")
    print(f"  ⏰ {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")

    if stats["saved"] > 0:
        print("\n📋 Bài viết mới trong thư mục reports:")
        intl_files = sorted(
            f for f in os.listdir(REPORTS_DIR) if f.startswith("intl_")
        )
        for fname in intl_files:
            print(f"  📰 {fname}")

    return 0 if stats["errors"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
