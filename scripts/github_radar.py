#!/usr/bin/env python3
"""
GitHub Trending Radar cho Long
Quét các repo hot về: automation, business, security, affiliate
"""

import urllib.request, json, ssl, sys
from datetime import datetime

def search_github(query, per_page=5):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page={per_page}"
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "HermesBot/1.0",
            "Accept": "application/vnd.github.v3+json"
        })
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            return json.loads(resp.read())
    except Exception as e:
        return {"items": [], "error": str(e)}

def main():
    print(f"🐙 GITHUB RADAR — {datetime.now().strftime('%d/%m/%Y')}")
    print("=" * 60)
    
    categories = [
        ("⚙️  Automation & Workflow", "automation+workflow+tool+topic:automation", 10),
        ("🔒  Security & Auth", "security+vulnerability+scanner+topic:security", 10),
        ("💼  Business & Analytics", "business+analytics+dashboard+topic:business", 10),
        ("📢  Affiliate & Marketing", "affiliate+marketing+cms+landing-page", 10),
        ("🤖  AI for Business", "AI+business+automation+topic:artificial-intelligence", 10),
        ("🛒  F&B / Restaurant Tech", "restaurant+food+ordering+point-of-sale", 5),
    ]
    
    seen = set()
    total = 0
    
    for cat_name, query, limit in categories:
        print(f"\n{cat_name}")
        print("─" * 50)
        data = search_github(urllib.parse.quote(query), limit)
        
        count = 0
        for repo in data.get("items", []):
            name = repo["full_name"]
            if name in seen:
                continue
            seen.add(name)
            if count >= limit:
                break
            stars = repo["stargazers_count"]
            desc = (repo.get("description") or "No description")[:120]
            lang = repo.get("language") or "N/A"
            url = repo["html_url"]
            created = repo.get("created_at", "")[:10]
            updated = repo.get("updated_at", "")[:10]
            
            print(f"  ⭐ {stars:>6}  {name}")
            print(f"     📝 {desc}")
            print(f"     🔤 {lang}  🕐 Created: {created}  Updated: {updated}")
            print(f"     🔗 {url}")
            count += 1
            total += 1
        
        if not data.get("items"):
            print("  (no results)")
    
    print(f"\n{'=' * 60}")
    print(f"📊 Total repos found: {total}")
    print(f"💡 Gợi ý: Check các repo mới (< 7 ngày) có growth bất thường!")

if __name__ == "__main__":
    import urllib.parse
    main()
