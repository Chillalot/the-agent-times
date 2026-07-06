#!/usr/bin/env python3
"""
Phương's Daily — NYT-style Newspaper Server
Báo cáo Kinh tế, Công nghệ, GitHub, Pháp lý & F&B tự động hàng ngày
"""
import os, json, glob, subprocess, re, threading, time, atexit, signal, sys
from pathlib import Path
from datetime import datetime, date, timedelta
from flask import Flask, render_template, request, abort, redirect, url_for, make_response

app = Flask(__name__)

# === CACHE BUSTING — no cache for HTML/CSS ===
@app.after_request
def no_cache(response):
    """Prevent browser from caching HTML pages"""
    if response.content_type and 'text/html' in response.content_type:
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response

# === CONFIG ===
REPORTS_DIR = os.path.expanduser("~/.hermes/profiles/meow/reports")
SCRIPTS_DIR = os.path.expanduser("~/.hermes/profiles/meow/scripts")

CATEGORY_MAP = {
    "economy": {"name": "📰 Kinh tế", "emoji": "📰", "id": "economy"},
    "daily-briefing": {"name": "📰 Kinh tế", "emoji": "📰", "id": "daily-briefing"},  # legacy alias
    "technology": {"name": "💻 Công nghệ", "emoji": "💻", "id": "technology"},
    "github": {"name": "🐙 GitHub", "emoji": "🐙", "id": "github"},
    "legal": {"name": "⚖️ Pháp lý & Thuế", "emoji": "⚖️", "id": "legal"},
    "affiliate": {"name": "💰 Affiliate", "emoji": "💰", "id": "affiliate"},
    "fnb": {"name": "🍗 F&B & Quán ăn", "emoji": "🍗", "id": "fnb"},
    "economic": {"name": "📊 Phân tích Kinh tế", "emoji": "📊", "id": "economic"},
    "market": {"name": "📈 Thị trường", "emoji": "📈", "id": "market"},
}

# Category colors for TLDR digest — each has light/dark mode variants
CATEGORY_COLORS = {
    "economy": {"label": "Kinh tế", "bg": "#dbeafe", "text": "#1e40af", "border": "#2563eb"},
    "daily-briefing": {"label": "Kinh tế", "bg": "#dbeafe", "text": "#1e40af", "border": "#2563eb"},  # legacy
    "technology": {"label": "Công nghệ", "bg": "#ede9fe", "text": "#5b21b6", "border": "#7c3aed"},
    "github": {"label": "GitHub", "bg": "#f3e8ff", "text": "#6b21a8", "border": "#9333ea"},
    "fnb": {"label": "F&B", "bg": "#ffedd5", "text": "#9a3412", "border": "#ea580c"},
    "legal": {"label": "Pháp lý", "bg": "#fee2e2", "text": "#991b1b", "border": "#dc2626"},
    "affiliate": {"label": "Affiliate", "bg": "#d1fae5", "text": "#065f46", "border": "#059669"},
    "economic": {"label": "Phân tích", "bg": "#e0e7ff", "text": "#3730a3", "border": "#6366f1"},
    "market": {"label": "Thị trường", "bg": "#cffafe", "text": "#155e75", "border": "#0891b2"},
}

SHUTDOWN_TIMER = None  # Auto-shutdown after inactivity

# === REFRESH PROGRESS TRACKING ===
import threading as _threading
_REFRESH_JOBS = {}
_REFRESH_LOCK = _threading.Lock()

def _run_refresh_pipeline(job_id):
    """Run all pipelines in background thread, updating progress"""
    steps = [
        ("📰 Daily Briefing", ["bash", "autoreport_daily.sh"]),
        ("💻 Tech News", ["bash", "autoreport_tech.sh"]),
        ("🐙 GitHub Radar", ["bash", "autoreport_github.sh"]),
        ("🌍 International", ["python3", "international_news.py"]),
        ("🍗 F&B Report", ["bash", "autoreport_fnb.sh"]),
    ]
    logs = []
    for i, (name, cmd) in enumerate(steps):
        logs.append(f"⏳ {name}...")
        with _REFRESH_LOCK:
            _REFRESH_JOBS[job_id] = {"step": i, "total": len(steps), "logs": logs[:]}
        try:
            r = subprocess.run(
                cmd, capture_output=True, text=True, timeout=300, cwd=SCRIPTS_DIR
            )
            for line in r.stdout.split('\n'):
                line = line.strip()
                if line and ('✅' in line or '📰' in line or '🐙' in line or '🌍' in line or '💻' in line or '🍗' in line or '❌' in line):
                    logs.append(f"  {line}")
            logs.append(f"✅ {name} hoàn tất")
        except Exception as e:
            logs.append(f"❌ {name} lỗi: {e}")
        with _REFRESH_LOCK:
            _REFRESH_JOBS[job_id] = {"step": i+1, "total": len(steps), "logs": logs[:], "done": i == len(steps)-1}
    
    with _REFRESH_LOCK:
        _REFRESH_JOBS[job_id]["done"] = True
        _REFRESH_JOBS[job_id]["logs"].append("🎉 All pipelines complete!")


def load_all_articles():
    """Load tất cả articles từ reports directory"""
    articles = []
    rdir = Path(REPORTS_DIR)
    if not rdir.exists():
        return []
    
    for fpath in sorted(rdir.glob("*.json"), reverse=True):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            cat = data.get("category", "daily-briefing")
            cat_info = CATEGORY_MAP.get(cat, {"name": "📄 Báo cáo", "emoji": "📄"})
            
            articles.append({
                "id": data.get("id", fpath.stem),
                "title": data.get("title", "Báo cáo"),
                "date": data.get("date", "2026-01-01"),
                "date_display": data.get("date_display", "01/01/2026"),
                "category": cat,
                "category_name": data.get("category_name", cat_info["name"]),
                "emoji": data.get("emoji", cat_info["emoji"]),
                "excerpt": data.get("excerpt", ""),
                "content_html": data.get("content_html", ""),
                "tags": data.get("tags", []),
                "sources": data.get("sources", []),
                "word_count": data.get("word_count", 0),
            })
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[!] Lỗi đọc {fpath}: {e}")
    
    # Sort: articles with real images first, then by date
    def sort_key(a):
        has_real_img = a.get('lead_image') and 'icons8' not in a.get('lead_image', '') and 'http' in a.get('lead_image', '')
        is_news = a.get('category') in ('economy', 'daily-briefing', 'technology', 'github', 'legal', 'fnb', 'economic')
        return (0 if has_real_img else 1, 0 if is_news else 1, a["date"])
    articles.sort(key=sort_key, reverse=False)
    # Then reverse for chronological: newest first, but real images still prioritized
    news_articles = [a for a in articles if a.get('category') in ('economy', 'daily-briefing', 'technology', 'github', 'legal', 'fnb', 'economic')]
    other_articles = [a for a in articles if a.get('category') not in ('economy', 'daily-briefing', 'technology', 'github', 'legal', 'fnb', 'economic')]
    news_articles.sort(key=lambda a: a["date"], reverse=True)
    other_articles.sort(key=lambda a: a["date"], reverse=True)
    articles = news_articles + other_articles
    return articles


def get_available_dates(articles):
    """Trả về danh sách các ngày có báo cáo (sorted, mới nhất trước)"""
    dates = sorted(set(a["date"] for a in articles), reverse=True)
    return dates


def format_date_display(iso_date):
    """Chuyển 2026-07-03 thành 'Thứ Sáu, 03/07/2026'"""
    try:
        dt = datetime.strptime(iso_date, "%Y-%m-%d")
        weekday_map = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
        wd = weekday_map[dt.weekday()]
        return f"{wd}, {dt.strftime('%d/%m/%Y')}"
    except:
        return iso_date


def get_prev_next_dates(iso_date, all_dates):
    """Lấy ngày trước và sau so với iso_date từ all_dates"""
    prev_d = next_d = None
    sorted_dates = sorted(all_dates, reverse=True)
    for i, d in enumerate(sorted_dates):
        if d == iso_date:
            if i < len(sorted_dates) - 1:
                prev_d = sorted_dates[i + 1]  # ngày cũ hơn
            if i > 0:
                next_d = sorted_dates[i - 1]   # ngày mới hơn
            break
    return prev_d, next_d


def get_common_context(selected_date=None, category=None, query=None):
    """Trả về context chung cho tất cả pages: date nav, v.v."""
    all_arts = load_all_articles()
    all_dates = get_available_dates(all_arts)
    
    today_str = date.today().isoformat()
    
    # Nếu không có selected_date, lấy ngày gần nhất có báo cáo
    if not selected_date:
        if category and category in CATEGORY_MAP:
            # Ưu tiên ngày có bài trong category này
            cat_dates = sorted(set(a["date"] for a in all_arts if a["category"] == category), reverse=True)
            selected_date = cat_dates[0] if cat_dates else (all_dates[0] if all_dates else today_str)
        else:
            selected_date = all_dates[0] if all_dates else today_str
    
    prev_date, next_date = get_prev_next_dates(selected_date, all_dates)
    
    context = {
        "selected_date_iso": selected_date,
        "selected_date_str": format_date_display(selected_date),
        "selected_date_display": format_date_display(selected_date),
        "prev_date": prev_date or selected_date,
        "next_date": next_date if next_date else None,
        "today_iso": today_str,
        "all_dates": all_dates,
        "active_nav": "home",
        "current_category": category or "",
        "category_colors": CATEGORY_COLORS,
    }
    
    # Filter articles
    filtered = all_arts
    
    # Lọc theo ngày
    filtered = [a for a in filtered if a["date"] == selected_date]
    
    # Lọc theo category
    if category and category in CATEGORY_MAP:
        filtered = [a for a in filtered if a["category"] == category]
        context["active_nav"] = category
        context["category_name"] = CATEGORY_MAP[category]["name"]
    
    # Lọc theo search query
    if query:
        q = query.lower().strip()
        filtered = [a for a in all_arts if (
            q in a["title"].lower() or
            q in a["excerpt"].lower() or
            any(q in t.lower() for t in a.get("tags", [])) or
            q in a["category_name"].lower()
        )]
        context["query"] = query
        # For search, show all dates
        context["selected_date_str"] = f'Tìm kiếm: "{query}"'
        context["selected_date_display"] = f'Tìm kiếm: "{query}"'
    
    context["articles"] = filtered
    
    return context


# === CLEANUP MECHANISM ===
SHUTDOWN_FILE = os.path.expanduser("~/.hermes/profiles/meow/frontend/.shutdown")

@app.route("/shutdown")
def shutdown():
    """Auto-shutdown: browser gọi cái này khi onbeforeunload"""
    # Ghi file báo hiệu shutdown
    with open(SHUTDOWN_FILE, "w") as f:
        f.write("1")
    
    def delayed_shutdown():
        time.sleep(2)
        os._exit(0)
    
    threading.Thread(target=delayed_shutdown, daemon=True).start()
    return "OK"


# === ROUTES ===

@app.route("/")
def home():
    ctx = get_common_context()
    return render_template("index.html", **ctx)


@app.route("/date/<date_str>")
def by_date(date_str):
    """Xem báo cáo theo ngày (YYYY-MM-DD)"""
    ctx = get_common_context(selected_date=date_str)
    return render_template("index.html", **ctx)


@app.route("/category/<category>")
def by_category(category):
    if category not in CATEGORY_MAP:
        abort(404)
    ctx = get_common_context(category=category)
    return render_template("index.html", **ctx)


@app.route("/category/<category>/date/<date_str>")
def by_category_date(category, date_str):
    if category not in CATEGORY_MAP:
        abort(404)
    ctx = get_common_context(selected_date=date_str, category=category)
    return render_template("index.html", **ctx)


@app.route("/article/<article_id>")
def article(article_id):
    all_arts = load_all_articles()
    art = None
    for a in all_arts:
        if a["id"] == article_id:
            art = a
            break
    if not art:
        abort(404)
    
    # === Related articles: up to 7 ===
    same_cat_same_date = [a for a in all_arts 
                         if a["category"] == art["category"] 
                         and a["id"] != art["id"] 
                         and a["date"] == art["date"]]
    same_cat_other_date = [a for a in all_arts 
                          if a["category"] == art["category"] 
                          and a["id"] != art["id"] 
                          and a["date"] != art["date"]]
    # Sort by date descending (newest first)
    same_cat_other_date.sort(key=lambda a: a["date"], reverse=True)
    
    related = same_cat_same_date + same_cat_other_date
    
    # If not enough, fill with most recent articles of any category
    if len(related) < 7:
        other_ids = {a["id"] for a in related} | {art["id"]}
        fillers = [a for a in all_arts if a["id"] not in other_ids]
        fillers.sort(key=lambda a: a["date"], reverse=True)
        needed = 7 - len(related)
        related += fillers[:needed]
    
    related_articles = related[:7]
    
    # Context cơ bản cho date nav
    ctx = get_common_context(selected_date=art["date"])
    
    return render_template("article.html", 
                         article=art,
                         related_articles=related_articles,
                         selected_date_iso=ctx["selected_date_iso"],
                         selected_date_str=ctx["selected_date_str"],
                         selected_date_display=ctx["selected_date_display"],
                         prev_date=ctx["prev_date"],
                         next_date=ctx["next_date"],
                         today_iso=ctx["today_iso"],
                         all_dates=ctx["all_dates"],
                         active_nav=art["category"],
                         category_colors=ctx["category_colors"])


@app.route("/search")
def search():
    query = request.args.get("q", "")
    ctx = get_common_context(query=query)
    return render_template("index.html", **ctx)


@app.route("/refresh")
def refresh_page():
    """Show refresh loading page immediately"""
    import uuid
    job_id = str(uuid.uuid4())[:8]
    # Start background thread
    t = _threading.Thread(target=_run_refresh_pipeline, args=(job_id,), daemon=True)
    t.start()
    with _REFRESH_LOCK:
        _REFRESH_JOBS[job_id] = {"step": 0, "total": 5, "logs": ["🚀 Starting all pipelines..."]}
    ctx = get_common_context()
    ctx["job_id"] = job_id
    return render_template("refresh.html", **ctx)


@app.route("/refresh/status/<job_id>")
def refresh_status(job_id):
    """JSON status endpoint for polling"""
    with _REFRESH_LOCK:
        job = _REFRESH_JOBS.get(job_id)
    if not job:
        return {"error": "not found", "done": True}
    return {
        "step": job.get("step", 0),
        "total": job.get("total", 5),
        "logs": job.get("logs", []),
        "done": job.get("done", False),
    }


# === ERROR HANDLERS ===

@app.errorhandler(404)
def not_found(e):
    ctx = get_common_context()
    return render_template("index.html", **ctx), 404


# === LAUNCH DETECTION ===
# If running via launch script, this file marks the session
MARKER = os.path.expanduser("~/.hermes/profiles/meow/frontend/.launched")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    
    # Ghi marker khi launch
    with open(MARKER, "w") as f:
        f.write(str(os.getpid()))
    
    # Cleanup khi exit
    def cleanup():
        for f in [MARKER, SHUTDOWN_FILE]:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except:
                pass
    
    atexit.register(cleanup)
    signal.signal(signal.SIGTERM, lambda *a: sys.exit(0))
    
    print(f"\n  📡  Phương's Daily — NYT-style Newspaper")
    print(f"  ─────────────────────────────────────")
    print(f"  🌐  http://localhost:{port}")
    print(f"  📂  {REPORTS_DIR}")
    print(f"  🛑  Ctrl+C để dừng server\n")
    
    app.run(host="0.0.0.0", port=port, debug=False)
