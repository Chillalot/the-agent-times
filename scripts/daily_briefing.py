#!/usr/bin/env python3
"""
Daily Economic & Business Briefing cho Long - F&B Entrepreneur 🍗
Chạy mỗi sáng 8h: tổng hợp tin tức kinh tế, F&B, luật pháp, GitHub trending
Mở rộng: từ quán cơm gà → tổng thể F&B (trà sữa, cf, cloud kitchen, chain, ...)
"""

import subprocess, json, urllib.request, urllib.error, ssl, sys
from datetime import datetime
from xml.etree import ElementTree as ET

BLOGWATCHER = "/home/chillalot/.hermes/profiles/meow/bin/blogwatcher-cli"
PROFILE = "meow"
SCRIPTS_DIR = "/home/chillalot/.hermes/profiles/meow/scripts"

def run_cmd(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return r.stdout.strip()
    except Exception as e:
        return f"[Lỗi] {e}"

def fetch_rss(url, max_items=15):
    """Fetch và parse RSS feed"""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            data = resp.read()
        root = ET.fromstring(data)
        # Handle RSS 2.0
        items = []
        for item in root.iter("item"):
            title = item.findtext("title", "")
            link = item.findtext("link", "")
            pubdate = item.findtext("pubDate", "")
            desc = item.findtext("description", "")
            if title:
                items.append({
                    "title": title.strip(),
                    "link": link.strip(),
                    "date": pubdate.strip()[:25],
                    "desc": desc.strip()[:200]
                })
            if len(items) >= max_items:
                break
        # Handle Atom
        if not items:
            for entry in root.iter("{http://www.w3.org/2005/Atom}entry"):
                title = entry.findtext("{http://www.w3.org/2005/Atom}title", "")
                link_el = entry.find("{http://www.w3.org/2005/Atom}link")
                link = link_el.get("href", "") if link_el is not None else ""
                updated = entry.findtext("{http://www.w3.org/2005/Atom}updated", "")
                if title:
                    items.append({
                        "title": title.strip(),
                        "link": link.strip(),
                        "date": updated.strip()[:19],
                        "desc": ""
                    })
                if len(items) >= max_items:
                    break
        return items
    except Exception as e:
        return [{"title": f"[Lỗi RSS: {url[:50]}...]", "link": "", "date": "", "desc": str(e)[:100]}]

def get_blogwatcher_articles():
    """Lấy bài mới từ blogwatcher"""
    out = run_cmd([BLOGWATCHER, "scan"])
    out2 = run_cmd([BLOGWATCHER, "articles", "--all"])
    return out, out2

def get_github_trending():
    """Fetch GitHub trending repos relevant to business/F&B/automation/security"""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    topics = [
        ("fnb_restaurant", "restaurant+OR+food+OR+pos+OR+inventory+business"),
        ("automation", "automation+OR+workflow+OR+business+OR+efficiency"),
        ("security", "security+OR+auth+OR+identity"),
        ("ai_business", "AI+OR+LLM+OR+chatbot+OR+analytics+business"),
        ("affiliate", "affiliate+OR+marketing+OR+SEO+OR+landing+OR+cms"),
    ]
    results = {}
    for cat, query in topics:
        url = f"https://api.github.com/search/repositories?q={query}+sort:stars&per_page=5&sort=stars&order=desc"
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "HermesBot/1.0",
                "Accept": "application/vnd.github.v3+json"
            })
            with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
                data = json.loads(resp.read())
            repos = []
            for r in data.get("items", [])[:5]:
                repos.append({
                    "name": r["full_name"],
                    "stars": r["stargazers_count"],
                    "desc": (r["description"] or "")[:120],
                    "url": r["html_url"]
                })
            results[cat] = repos
        except Exception as e:
            results[cat] = [{"name": f"[Error]", "stars": 0, "desc": str(e)[:80], "url": ""}]
    return results

def get_news_roundup():
    """Tổng hợp tin tức từ các RSS feeds — mở rộng F&B"""
    feeds = {
        "🇻🇳 Kinh doanh VN": "https://vnexpress.net/rss/kinh-doanh.rss",
        "🌍 Thế giới": "https://vnexpress.net/rss/the-gioi.rss",
        "🚀 Startup": "https://vnexpress.net/rss/startup.rss",
        "🍗 Ẩm thực / F&B": "https://vnexpress.net/rss/doi-song.rss",
        "📈 Kinh tế Tuổi Trẻ": "https://tuoitre.vn/rss/kinh-te.rss",
        "⚖️ Pháp luật VN": "https://vnexpress.net/rss/phap-luat.rss",
        "🔬 Khoa học": "https://vnexpress.net/rss/khoa-hoc.rss",
        "💻 Công nghệ": "https://vnexpress.net/rss/so-hoa.rss",
        "🏢 VietnamNet Kinh doanh": "https://vietnamnet.vn/rss/kinh-doanh.rss",
    }
    results = {}
    for name, url in feeds.items():
        results[name] = fetch_rss(url, 6)
    return results

def main():
    today = datetime.now().strftime("%A, %d/%m/%Y")
    print(f"╔══════════════════════════════════════════════╗")
    print(f"║  📊 BÁO CÁO KINH TẾ & F&B HÀNG NGÀY        ║")
    print(f"║  {today}                    ║")
    print(f"╠══════════════════════════════════════════════╣")
    print(f"║  Cho: Long - Entrepreneur 🍗 F&B            ║")
    print(f"╚══════════════════════════════════════════════╝")
    print()

    # 1. TIN TỨC KINH TẾ & F&B
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📰  TIN TỨC KINH TẾ & F&B VIỆT NAM")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    news = get_news_roundup()
    for category, items in news.items():
        print(f"\n  ▸ {category}:")
        count = 0
        for item in items:
            title = item["title"]
            if "RSS" in title or "Tin nhanh" in title or len(title) < 10:
                continue
            count += 1
            if count > 5:
                break
            print(f"    • {title}")
            if item["link"]:
                print(f"      🔗 {item['link']}")

    # 2. F&B INSIGHTS CORNER
    print("\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🍗  GÓC F&B — Ý TƯỞNG & XU HƯỚNG")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("""
  💡 HÔM NAY NHỚ:
  • Theo dõi giá nguyên liệu (gà, gạo, dầu ăn, gia vị) — ảnh hưởng giá vốn
  • Để ý xu hướng F&B đang hot: cloud kitchen, take-away, fast-casual
  • Các mô hình mới: trà sữa, cà phê specialty, ăn vặt healthy
  • Quản lý chuỗi: tiêu chuẩn hoá quy trình, kiểm soát nhiều cửa hàng
  """)
    # Check for F&B related keywords in today's news
    fnb_keywords = ["thực phẩm", "đồ uống", "Ẩm thực", "nhà hàng", "quán ăn",
                    "cơm", "gà", "trà", "cà phê", "cloud kitchen", "F&B",
                    "food", "beverage", "restaurant"]
    fnb_mentions = []
    for category, items in news.items():
        for item in items:
            for kw in fnb_keywords:
                if kw.lower() in item["title"].lower():
                    fnb_mentions.append(f"• {item['title']} ({category})")
                    break
    if fnb_mentions:
        print("  🔥 TIN LIÊN QUAN F&B HÔM NAY:")
        for m in fnb_mentions[:3]:
            print(f"    {m}")

    # 3. GITHUB TRENDING RADAR
    print("\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🐙  GITHUB TRENDING RADAR")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    github_data = get_github_trending()
    emojis = {"fnb_restaurant": "🍽️", "automation": "⚙️", "security": "🔒",
              "ai_business": "🤖", "affiliate": "📢"}
    labels = {"fnb_restaurant": "F&B / NHÀ HÀNG", "automation": "TỰ ĐỘNG HOÁ",
              "security": "BẢO MẬT", "ai_business": "AI / KINH DOANH",
              "affiliate": "AFFILIATE / MARKETING"}
    for cat, repos in github_data.items():
        print(f"\n  {emojis.get(cat, '📦')} {labels.get(cat, cat.upper())}:")
        for r in repos:
            if r["name"].startswith("[Error]"):
                continue
            print(f"    ⭐ {r['stars']} — {r['name']}")
            if r["desc"]:
                print(f"       {r['desc']}")
            if r["url"]:
                print(f"       {r['url']}")

    # 4. LEGAL & TAX CORNER
    print("\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("⚖️  GÓC PHÁP LÝ & THUẾ - F&B")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("""
  📋 HỘ KINH DOANH CÁ THỂ — Mô hình cơ bản cho quán nhỏ:
     • 1 người/nhóm người/hộ gia đình làm chủ
     • Dưới 10 lao động, 1 địa điểm duy nhất
     • Chịu trách nhiệm vô hạn bằng tài sản cá nhân

  🏢 MỞ RỘNG: CÔNG TY TNHH / CHUỖI:
     • Nếu mở >1 quán → cần lên Công ty TNHH
     • Vốn điều lệ tối thiểu: không quy định (chỉ cần đủ)
     • Đăng ký tại Sở KHĐT tỉnh/thành phố
     • Có con dấu pháp nhân, được xuất hóa đơn GTGT
     • Chi phí thành lập: ~5-10 triệu (kể cả dịch vụ)

  📑 GIẤY TỜ CẦN CÓ (quán ăn):
     1️⃣ Đăng ký hộ KD cá thể / Giấy CN ĐKKD
     2️⃣ Giấy ATVS thực phẩm (theo NĐ 15/2018)
     3️⃣ Đăng ký mã số thuế
     4️⃣ Hợp đồng thuê mặt bằng
     5️⃣ Giấy khám sức khỏe cho chủ + nhân viên
     6️⃣ Tập huấn kiến thức ATTP

  💰 THUẾ (hộ KD cá thể - F&B):
     • Thuế môn bài: MIỄN (<100tr/n) → 300k-1tr
     • GTGT: 1% doanh thu
     • TNCN: 1.5% doanh thu
     • Tổng thuế khoán: ~2.5% doanh thu
  """)
    print("  ⚠️  Xem chi tiết: python3 ~/.hermes/profiles/meow/scripts/legal_tax_guide.py")
    print("  💡 Với chuỗi: cần chuyển sang Công ty TNHH + kế toán dịch vụ")

    # 5. F&B BUSINESS MODEL SPOTLIGHT
    print("\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("✨  SPOTLIGHT: MÔ HÌNH F&B ĐANG HOT")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("""
  🏪 Quán cơm gà (foundation): 
     • Vốn thấp, quay vòng nhanh, dễ mở rộng
     • Tiềm năng: thêm chi nhánh, thêm dịch vụ giao hàng

  ☕ Cà phê / Trà sữa:
     • Biên lợi nhuận cao (60-75%)
     • Cạnh tranh khốc liệt, cần concept độc đáo

  🥗 Ăn vặt healthy / Fast-casual:
     • Xu hướng mới, ít đối thủ
     • Khách hàng trẻ, sẵn sàng trả giá cao

  🏭 Cloud Kitchen (bếp trung tâm):
     • Tiết kiệm mặt bằng, chỉ phục vụ giao hàng
     • Vận hành tinh gọn, scale nhanh

  🔗 Mô hình chuỗi / franchise:
     • Tiêu chuẩn hoá → nhân rộng
     • Cần hệ thống quản lý, đào tạo, kiểm soát chất lượng
  """)
    print("  📅 Thứ 4 hàng tuần: Báo cáo F&B Business Insights chi tiết")

    # 6. GÓC NHẮN CHO LONG
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("💡  GÓC NHẮN CHO LONG")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("""
  • 🍗 Quán cơm gà = nền móng. Học vận hành, tối ưu, rồi nhân rộng.
  • 📊 Ghi chép chi phí hàng ngày — số liệu mới là sức mạnh
  • 🧮 Giá thành mỗi suất = Nguyên liệu + Nhân công + Điện/nước + Mặt bằng (khấu hao)
  • 💵 Giá bán = Giá thành × 1.8 ~ 2.5 (tuỳ khu vực)
  • 🔄 Content Automation: chờ Long hướng dẫn setup!
  • 📚 Học quản lý chuỗi: skill fnb-chain-management đã được tạo
  """)

    # 7. BLOGWATCHER STATUS
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📡  BLOGWATCHER STATUS")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    scan_out, art_out = get_blogwatcher_articles()
    print(f"  {scan_out[:300]}")
    print(f"\n  Bài mới:\n{art_out[:300]}")

if __name__ == "__main__":
    main()
