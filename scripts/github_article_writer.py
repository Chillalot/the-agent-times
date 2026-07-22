#!/usr/bin/env python3
"""
GitHub Article Reporter — Mỗi repo thành bài báo
Đọc dữ liệu từ github_*.json trong REPORTS_DIR, parse từng repo,
tạo article JSON hoàn chỉnh cho mỗi repo.
"""

import json
import os
import re
from datetime import datetime

# ─── Config ────────────────────────────────────────────────────────────────
from scripts.config import SCRIPTS_DIR, REPORTS_DIR

# ─── Parse helpers ─────────────────────────────────────────────────────────

def find_repo_blocks(text):
    """
    Parse content_text and extract repo blocks.
    Each block starts with a ⭐ line and includes 📝, 🔤, 🔗 lines.
    Returns list of dicts: {stars, name, description, language, url, category}
    """
    lines = text.split("\n")
    blocks = []
    current = None

    # Category tracking — the text has sections like "⚙️  Automation & Workflow"
    current_category = "General"

    for line in lines:
        # Detect category headers
        cat_match = re.match(r'^\s*([⚙️🔒💼📢🤖🛒].+)$', line)
        if cat_match and not line.strip().startswith("─"):
            current_category = cat_match.group(1).strip()

        # Match ⭐ line
        star_match = re.match(r'^\s*⭐\s+(\d+)\s+(.+?)\s*$', line)
        if star_match:
            if current:
                blocks.append(current)
            current = {
                "stars": int(star_match.group(1)),
                "name": star_match.group(2).strip(),
                "description": "",
                "language": "N/A",
                "url": "",
                "category": current_category,
            }
            continue

        if current is None:
            continue

        # 📝 description
        desc_match = re.match(r'^\s*📝\s+(.+)$', line)
        if desc_match:
            current["description"] = desc_match.group(1).strip()
            continue

        # 🔤 language
        lang_match = re.match(r'^\s*🔤\s+(.+?)\s+🕐', line)
        if lang_match:
            current["language"] = lang_match.group(1).strip()
            continue

        # 🔗 url
        url_match = re.match(r'^\s*🔗\s+(https?://\S+)$', line)
        if url_match:
            current["url"] = url_match.group(1).strip()
            continue

    if current:
        blocks.append(current)

    return blocks


def categorize_repo(repo):
    """Determine tags and content style based on repo description and name."""
    text = (repo["description"] + " " + repo["name"]).lower()
    lang = repo["language"].lower()

    tags = ["github"]

    # Technology detection
    tech_map = {
        "python": "Python",
        "javascript": "JavaScript",
        "typescript": "TypeScript",
        "rust": "Rust",
        "go": "Golang",
        "java": "Java",
        "kotlin": "Kotlin",
        "swift": "Swift",
        "ruby": "Ruby",
        "c++": "C++",
        "c#": "C#",
        "php": "PHP",
        "solidity": "Solidity",
        "react": "React",
        "vue": "Vue.js",
        "angular": "Angular",
        "next.js": "Next.js",
        "node.js": "Node.js",
        "django": "Django",
        "flask": "Flask",
        "fastapi": "FastAPI",
        "tensorflow": "TensorFlow",
        "pytorch": "PyTorch",
        "docker": "Docker",
        "kubernetes": "Kubernetes",
        "aws": "AWS",
        "gcp": "GCP",
        "azure": "Azure",
        "api": "API",
        "cli": "CLI",
        "ai": "AI",
        "machine learning": "machine-learning",
        "ml": "machine-learning",
        "deep learning": "deep-learning",
        "llm": "LLM",
        "gpt": "GPT",
        "openai": "OpenAI",
        "chatgpt": "ChatGPT",
        "automation": "automation",
        "automat": "automation",
        "workflow": "workflow",
        "security": "security",
        "scanner": "security",
        "vulnerability": "security",
        "hack": "security",
        "dashboard": "dashboard",
        "analytics": "analytics",
        "business": "business",
        "marketing": "marketing",
        "affiliate": "affiliate",
        "cms": "CMS",
        "blog": "blog",
        "restaurant": "F&B",
        "food": "F&B",
        "pos": "F&B",
        "ordering": "F&B",
        "data": "data",
        "database": "database",
        "devops": "devops",
        "testing": "testing",
        "test": "testing",
        "generator": "generator",
        "tool": "tool",
        "framework": "framework",
        "library": "library",
    }

    for keyword, tag in tech_map.items():
        if keyword in text:
            if tag not in tags:
                tags.append(tag)

    # Add language as tag if not generic
    if lang and lang not in ("n/a", "na", ""):
        lang_tag = lang.replace(" ", "-")
        if lang_tag not in tags:
            tags.append(lang_tag)

    return tags


def generate_excerpt(repo):
    """Generate a 1-2 sentence engaging excerpt from the repo description."""
    desc = repo["description"]
    if not desc or desc == "No description":
        return f"⭐ {repo['stars']} stars — {repo['name']} là một dự án đáng chú ý trên GitHub."
    
    # Clean description
    desc = desc.strip()
    if len(desc) > 150:
        desc = desc[:147] + "..."

    if repo["stars"] >= 100:
        return f"🔥 Dự án {repo['name']} đạt {repo['stars']} sao trên GitHub. {desc}"
    else:
        return f"📌 {repo['name']} — {desc}"


def generate_html_article(repo):
    """Generate full HTML article content for a repo."""
    name = repo["name"]
    stars = repo["stars"]
    lang = repo["language"]
    desc_raw = repo["description"] or "Không có mô tả chi tiết."
    url = repo["url"]

    # Star ranking
    if stars >= 1000:
        popularity = "cực kỳ phổ biến"
        badge = "🔥🔥🔥"
    elif stars >= 100:
        popularity = "rất được quan tâm"
        badge = "🔥🔥"
    elif stars >= 10:
        popularity = "đang thu hút sự chú ý"
        badge = "🔥"
    else:
        popularity = "mới nổi"
        badge = "🌟"

    # Build description paragraphs
    desc_clean = desc_raw.strip()
    if desc_clean.endswith("."):
        desc_clean = desc_clean[:-1]

    paragraphs = []

    # Opening
    paragraphs.append(
        f"<p><strong>{badge}</strong> <strong>{name}</strong> là một dự án {popularity} "
        f"trên GitHub với <strong>{stars} sao</strong>. "
        f"{desc_clean}.</p>"
    )

    # Main body
    tech_note = ""
    if lang and lang != "N/A":
        tech_note = (
            f" Dự án được xây dựng bằng <strong>{lang}</strong>, "
            f"một ngôn ngữ mạnh mẽ và linh hoạt phù hợp cho phát triển phần mềm hiện đại."
        )

    paragraphs.append(
        f"<h3>Tính năng chính</h3>"
        f"<p>{desc_clean}.{tech_note}</p>"
        f"<p>Với {stars} sao trên GitHub, dự án này đã nhận được sự công nhận "
        f"từ cộng đồng developer. Đây là minh chứng cho chất lượng và tính hữu dụng "
        f"của mã nguồn.</p>"
    )

    # Use cases section
    paragraphs.append(
        f"<h3>Use cases & Ứng dụng thực tế</h3>"
        f"<p>{name} phù hợp cho các nhà phát triển đang tìm kiếm giải pháp "
        f"trong lĩnh vực này. Dự án có thể được sử dụng như:</p>"
        f"<ul>"
        f"<li>Thư viện / công cụ tích hợp vào dự án hiện có</li>"
        f"<li>Reference code cho những ai muốn học hỏi kinh nghiệm</li>"
        f"<li>Nền tảng để phát triển thêm các tính năng mở rộng</li>"
        f"</ul>"
    )

    # Conclusion
    paragraphs.append(
        f"<h3>Kết luận</h3>"
        f"<p><strong>{name}</strong> là một dự án GitHub đáng chú ý{' với ' + str(stars) + ' sao' if stars > 0 else ''}."
        f" Nếu bạn đang làm việc trong lĩnh vực này, đây chắc chắn là một dự án "
        f"đáng để theo dõi và đóng góp.</p>"
        f"<p>🔗 <a href=\"{url}\" target=\"_blank\" rel=\"noopener\">Xem trên GitHub →</a></p>"
    )

    return "\n".join(paragraphs)


def word_count(html):
    """Count words in HTML content (strip tags first)."""
    text = re.sub(r'<[^>]+>', '', html)
    text = re.sub(r'&[a-z]+;', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return len(text.split())


def make_article_id(repo_name):
    """Create a deterministic article ID from repo name (no timestamp)."""
    safe = re.sub(r'[^a-zA-Z0-9_-]', '_', repo_name.strip())
    safe = re.sub(r'_+', '_', safe).strip('_')
    return f"github_article_{safe}"


def build_article(repo):
    """Build a complete article JSON dict for a single repo."""
    short_name = repo["name"].split("/")[-1] if "/" in repo["name"] else repo["name"]
    tags = categorize_repo(repo)
    excerpt = generate_excerpt(repo)
    html = generate_html_article(repo)
    wc = word_count(html)
    today = datetime.now().strftime("%Y-%m-%d")
    today_display = datetime.now().strftime("%A, %d/%m/%Y")

    # Determine language for title
    lang_display = repo["language"] if repo["language"] != "N/A" else "Đa ngôn ngữ"

    article = {
        "id": make_article_id(repo["name"]),
        "title": f"{short_name} — {lang_display} | ⭐{repo['stars']} — phân tích chi tiết",
        "date": today,
        "date_display": today_display,
        "category": "github",
        "category_name": "🐙 Công nghệ & GitHub",
        "emoji": "🐙",
        "excerpt": excerpt,
        "content_html": html,
        "tags": tags,
        "sources": [repo["url"]] if repo["url"] else [],
        "word_count": wc,
        "generated_at": datetime.now().isoformat(),
    }

    return article


def save_article(article, reports_dir):
    """Save article JSON to reports directory. Skip if already exists."""
    fname = f"{article['id']}.json"
    fpath = os.path.join(reports_dir, fname)
    # Skip if article with same repo already exists
    if os.path.exists(fpath):
        return None
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(article, f, ensure_ascii=False, indent=2)
    return fpath


# ─── Main ──────────────────────────────────────────────────────────────────

def main():
    reports_dir = os.environ.get("REPORTS_DIR", str(REPORTS_DIR))

    # Find all github_*.json files
    input_files = sorted([
        f for f in os.listdir(reports_dir)
        if f.startswith("github_") and f.endswith(".json")
    ])

    if not input_files:
        print(f"⚠️  Không tìm thấy file github_*.json trong {reports_dir}")
        return

    print(f"📂 Tìm thấy {len(input_files)} file dữ liệu GitHub Radar")
    print("─" * 50)

    all_repos = []
    seen_names = set()

    for fname in input_files:
        fpath = os.path.join(reports_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)

        text = data.get("content_text", "")
        if not text:
            print(f"  ⚠️  {fname}: Không có content_text, bỏ qua")
            continue

        repos = find_repo_blocks(text)
        # Deduplicate by repo name (keep first occurrence)
        for r in repos:
            if r["name"] not in seen_names and r["url"] and r["stars"] >= 100:
                seen_names.add(r["name"])
                all_repos.append(r)

        print(f"  📄 {fname}: {len(repos)} repos → {sum(1 for r in repos if r['name'] not in seen_names or r['stars'] <= 0)} mới")

    if not all_repos:
        print("⚠️  Không có repo nào để viết bài (tất cả đã có hoặc không có sao)")
        return

    print(f"\n✍️  Đang viết {len(all_repos)} bài báo...")
    print("─" * 50)

    written = 0
    skipped = 0
    for repo in all_repos:
        article = build_article(repo)
        fpath = save_article(article, reports_dir)
        if fpath:
            print(f"  ✅ {repo['name']} (⭐{repo['stars']}) → {os.path.basename(fpath)}")
            written += 1
        else:
            print(f"  ⏭️  {repo['name']} (⭐{repo['stars']}) — đã tồn tại, bỏ qua")
            skipped += 1

    print(f"\n{'=' * 50}")
    print(f"✅ Đã viết {written} bài mới, bỏ qua {skipped} bài đã tồn tại")
    print(f"📁 Lưu tại: {reports_dir}")


if __name__ == "__main__":
    main()
