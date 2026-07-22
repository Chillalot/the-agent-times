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
import os
import re
import sys
import time
import traceback
from datetime import datetime

from scripts.config import REPORTS_DIR, MAX_ITEMS_PER_FEED
from scripts.lib.rss import fetch_rss
from scripts.lib.translate import translate_text
from scripts.lib.storage import save_article_json
from scripts.lib.article_writer import build_article_html, build_full_article
from bs4 import BeautifulSoup
from scripts import article_scraper as scraper

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
CATEGORY = "technology"
CATEGORY_NAME = "💻 Công nghệ"
EMOJI = "💻"

# ─── Article Helpers ─────────────────────────────────────────────────────────


def make_article_id(source_key, title, source_url):
    """Tạo article ID duy nhất từ md5."""
    raw = f"{source_key}_{title[:80]}_{source_url}"
    h = hashlib.md5(raw.encode()).hexdigest()[:8]
    today = datetime.now().strftime("%Y-%m-%d")
    return f"tech_{source_key}_{today}_{h}"


# ─── Process One Article ─────────────────────────────────────────────────────


def process_article(item, feed_key, feed_info, do_scrape=True):
    title_orig = item["title"]
    desc_orig = item.get("desc", "")
    link = item.get("link", "")
    source_name = feed_info["name"]
    source_type = feed_info["source_type"]
    source_tag = feed_info["source_tag"]
    is_international = (source_type == "international")

    if not title_orig:
        return None

    print(f"\n  📄 [{source_name}] {title_orig[:90]}")

    if is_international:
        print(f"    🔤 Đang dịch tiêu đề...", end="", flush=True)
        title_vi = translate_text(title_orig, src="en", dest="vi")
        print(f" ✅")
        print(f"    🇻🇳 {title_vi[:90]}")
        desc_vi = translate_text(desc_orig, src="en", dest="vi") if desc_orig else ""
    else:
        title_vi = title_orig
        desc_vi = desc_orig

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
                        raw_soup = BeautifulSoup(raw_html, "html.parser")
                        raw_text = raw_soup.get_text()
                        if raw_text and len(raw_text) > 80:
                            img_tags = []
                            for img in raw_soup.find_all("img"):
                                src = img.get("src", "")
                                if src and not src.startswith("data:") and len(src) > 20:
                                    img_tags.append(str(img))
                            chunk_size = 4000
                            chunks = [raw_text[i:i + chunk_size] for i in range(0, len(raw_text), chunk_size)]
                            translated_parts = []
                            for chunk in chunks:
                                translated_chunk = translate_text(chunk, src="en", dest="vi")
                                if translated_chunk and translated_chunk != chunk:
                                    translated_parts.append(translated_chunk)
                                else:
                                    translated_parts.append(chunk)
                            translated_text = "".join(translated_parts)
                            paras = [
                                f"<p>{p.strip()}</p>"
                                for p in translated_text.split("\n")
                                if p.strip()
                            ]
                            if img_tags:
                                paras.append('<div class="article-gallery">')
                                paras.extend(img_tags)
                                paras.append('</div>')
                            content_html = "\n".join(paras)
                        else:
                            content_html = raw_html
                    else:
                        content_html = raw_html
                print(f" ✅ ({scraped.get('text_length', 0)} chars)")
            else:
                print(f" ⚠️ {scraped.get('error', 'lỗi')}")
        except Exception as e:
            print(f" ⚠️ {e}")

    if not content_html:
        content_html = f"<p>{desc_vi}</p>"

    aw_result = build_full_article(
        title=title_vi,
        content_html=content_html,
        lead_image=lead_image_url,
        source_url=link,
        source_name=source_name,
        category=CATEGORY,
    )

    today = datetime.now().strftime("%Y-%m-%d")
    today_display = datetime.now().strftime("%A, %d/%m/%Y")

    tags = aw_result["tags"]
    if "công-nghệ" not in tags:
        tags.insert(0, "công-nghệ")
    vi_tag = "việt-nam" if source_type == "vietnam" else "quốc-tế"
    if vi_tag not in tags:
        tags.append(vi_tag)
    if source_tag not in tags:
        tags.append(source_tag)

    text_plain = re.sub(r"<[^>]+>", "", content_html).strip()
    title_lower = title_orig.lower()
    tech_keywords = {
        "ai": "ai", "artificial intelligence": "ai", "trí tuệ nhân tạo": "ai",
        "machine learning": "ai", "học máy": "ai",
        "startup": "startup", "blockchain": "blockchain",
        "crypto": "crypto", "bitcoin": "crypto",
        "security": "bảo-mật", "bảo mật": "bảo-mật", "hack": "bảo-mật",
        "apple": "apple", "google": "google", "microsoft": "microsoft",
        "meta": "meta", "facebook": "meta", "amazon": "amazon",
        "spacex": "space", "nasa": "space", "vũ trụ": "space",
        "electric": "xe-điện", "ev": "xe-điện", "tesla": "xe-điện",
        "smartphone": "mobile", "điện thoại": "mobile", "iphone": "mobile",
        "android": "mobile",
    }
    for kw, tag in tech_keywords.items():
        if kw in text_plain.lower() or kw in title_lower:
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
        "excerpt": aw_result["excerpt"],
        "content_html": aw_result["content_html"],
        "tags": tags,
        "sources": [link] if link else [],
        "lead_image": aw_result["lead_image"],
        "word_count": aw_result["word_count"],
        "source_url": link,
        "source_name": source_name,
        "source_type": source_type,
        "original_title": title_orig,
        "author": item.get("author", ""),
        "body_images": aw_result.get("body_images", []),
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
