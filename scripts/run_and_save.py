#!/usr/bin/env python3
"""
Cronjob Wrapper — Chạy script báo cáo và lưu thành article JSON
Cách dùng: python3 run_and_save.py daily_briefing.py daily-briefing "📰 Kinh tế & Công nghệ"
"""
import sys
import os
import subprocess
import json
import re
from datetime import datetime

from scripts.config import REPORTS_DIR, SCRIPTS_DIR

CATEGORY_MAP = {
    "daily-briefing": {"name": "📰 Kinh tế & Công nghệ", "emoji": "📰"},
    "github": {"name": "🐙 Công nghệ & GitHub", "emoji": "🐙"},
    "legal": {"name": "⚖️ Pháp lý & Thuế", "emoji": "⚖️"},
    "affiliate": {"name": "💰 Affiliate", "emoji": "💰"},
    "fnb": {"name": "🍗 F&B & Quán ăn", "emoji": "🍗"},
    "economic": {"name": "📊 Phân tích Kinh tế", "emoji": "📊"},
    "market": {"name": "📈 Thị trường", "emoji": "📈"},
}


def raw_text_to_html(text):
    """Chuyển text thuần thành HTML đẹp"""
    lines = text.split('\n')
    html_parts = []
    in_list = False
    num_pat = re.compile(r'^\d+[\.\)]\s*')
    
    for line in lines:
        stripped = line.strip()
        
        # Bỏ đường viền
        if all(c in '═╔╗╚╝║━━━□□■' for c in stripped) and len(stripped) > 5:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            continue
        
        # Headers
        if any(stripped.startswith(s) for s in ['📰', '🐙', '⚖️', '📊', '💰', '━━━']):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            if stripped.startswith('━━━'):
                continue
            html_parts.append(f'<h2>{stripped}</h2>')
            continue
        
        # Danh sách
        if stripped.startswith('• ') or stripped.startswith('▸ '):
            if not in_list:
                html_parts.append('<ul>')
                in_list = True
            content = stripped[2:]
            content = re.sub(
                r'https?://[^\s)\]]+',
                r'<a href="\g<0>" target="_blank" rel="noopener">🔗 Link</a>',
                content
            )
            html_parts.append(f'<li>{content}</li>')
            continue
        
        # Star counts
        if stripped.startswith('⭐'):
            if not in_list:
                html_parts.append('<ul>')
                in_list = True
            html_parts.append(f'<li>{stripped}</li>')
            continue
        
        # Numbered items
        if any(n in stripped for n in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣']):
            if not in_list:
                html_parts.append('<ul style="list-style:none;padding:0;">')
                in_list = True
            html_parts.append(f'<li style="margin-bottom:8px;">{stripped}</li>')
            continue
        
        # Empty
        if not stripped:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            continue
        
        # Numbered lines
        if num_pat.match(stripped):
            if not in_list:
                html_parts.append('<ol>')
                in_list = True
            html_parts.append(f'<li>{num_pat.sub("", stripped)}</li>')
            continue
        
        # Regular paragraph
        if in_list:
            html_parts.append("</ul>")
            in_list = False
        
        enriched = re.sub(
            r'https?://[^\s)\]]+',
            r'<a href="\g<0>" target="_blank" rel="noopener">\g<0></a>',
            stripped
        )
        enriched = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', enriched)
        html_parts.append(f'<p>{enriched}</p>')
    
    if in_list:
        html_parts.append("</ul>")
    
    return '\n'.join(html_parts)


def save_article(category, category_name, raw_text):
    """Lưu output script thành article JSON"""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    date_display = now.strftime("%A, %d/%m/%Y")
    article_id = f"{category}_{date_str}_{now.strftime('%H%M%S')}"
    
    urls = re.findall(r'https?://[^\s)\]]+', raw_text)
    cat_info = CATEGORY_MAP.get(category, {"emoji": "📄"})
    
    # Excerpt
    lines = [l.strip() for l in raw_text.split('\n') 
             if l.strip() and not l.strip().startswith('═') 
             and not l.strip().startswith('━')]
    excerpt_lines = [l for l in lines if len(l) > 10][:3]
    excerpt = ' | '.join(excerpt_lines)[:300]
    
    # Title
    title = f"Báo cáo {category_name} - {date_display}"
    for l in lines[:5]:
        if 'BÁO CÁO' in l.upper() or 'GITHUB' in l.upper():
            title = l.strip('║ ■□━═ ')
            break
    
    # Tags
    tags = []
    text_lower = raw_text.lower()
    if any(w in text_lower for w in ["kinh tế", "vnexpress", "gdp"]):
        tags.extend(["kinh-tế", "việt-nam"])
    if "github" in text_lower:
        tags.append("github")
    if any(w in text_lower for w in ["thuế", "pháp lý", "giấy phép"]):
        tags.extend(["thuế", "pháp-lý"])
    if any(w in text_lower for w in ["automation", "tự động"]):
        tags.append("tự-động-hóa")
    if "cơm" in text_lower or "quán" in text_lower:
        tags.append("kinh-doanh")
    if not tags:
        tags = ["báo-cáo", category]
    
    article = {
        "id": article_id,
        "title": title,
        "date": date_str,
        "date_display": date_display,
        "category": category,
        "category_name": category_name,
        "excerpt": excerpt,
        "content_html": raw_text_to_html(raw_text),
        "content_text": raw_text[:5000],
        "tags": list(set(tags)),
        "sources": urls[:15],
        "word_count": len(raw_text.split()),
        "emoji": cat_info.get("emoji", "📄"),
        "generated_at": now.isoformat(),
    }
    
    os.makedirs(REPORTS_DIR, exist_ok=True)
    fpath = os.path.join(REPORTS_DIR, f"{article_id}.json")
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(article, f, ensure_ascii=False, indent=2)
    
    return fpath


def main():
    if len(sys.argv) < 4:
        print("Cách dùng: python3 run_and_save.py <script.py> <category> <category_name>")
        print("Ví dụ: python3 run_and_save.py daily_briefing.py daily-briefing '📰 Kinh tế & Công nghệ'")
        sys.exit(1)
    
    script_name = sys.argv[1]
    category = sys.argv[2]
    category_name = sys.argv[3]
    
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    if not os.path.exists(script_path):
        print(f"❌ Không tìm thấy script: {script_path}")
        sys.exit(1)
    
    # Chạy script
    result = subprocess.run(
        ["python3", script_path],
        capture_output=True, text=True, timeout=120, cwd=SCRIPTS_DIR
    )
    
    # In output ra console (cronjob sẽ deliver cái này)
    if result.stdout:
        print(result.stdout)
    
    if result.stderr:
        print(f"[STDERR] {result.stderr[:500]}", file=sys.stderr)
    
    if result.returncode == 0 and result.stdout:
        # Lưu thành article
        fpath = save_article(category, category_name, result.stdout)
        print(f"\n📁 Article saved: {fpath}")
        print("✅ Đã lưu vào báo cáo — xem tại http://localhost:5050")
    
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
