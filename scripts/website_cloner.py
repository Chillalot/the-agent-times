#!/usr/bin/env python3
"""
Website Cloner Tool — Trích xuất design tokens từ một website và áp dụng vào frontend
Dựa trên AI Website Cloner Template (JCodesMore, 25k⭐)
Phiên bản rút gọn cho Flask + CSS
"""
import re, sys, os, json
import requests
from bs4 import BeautifulSoup

USER_AGENTS = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/17.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0",
]


def fetch(url):
    """Fetch website HTML"""
    headers = {
        "User-Agent": USER_AGENTS[0],
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "vi-VN,vi;q=0.9",
    }
    r = requests.get(url, headers=headers, timeout=30)
    r.encoding = "utf-8"
    return r.text


def extract_css_variables(html):
    """Extract all CSS custom properties from :root"""
    vars_dict = {}
    # Match :root { ... } blocks
    blocks = re.findall(r':root\s*\{(.*?)\}', html, re.DOTALL)
    for block in blocks:
        # Match --variable: value;
        vars_found = re.findall(r'(--[\w-]+)\s*:\s*([^;]+);', block)
        for key, val in vars_found:
            vars_dict[key.strip()] = val.strip()
    return vars_dict


def extract_colors(html):
    """Extract all hex/rgb/hsl colors used in the page"""
    colors = []
    # Hex colors
    hex_colors = set(re.findall(r'#[0-9a-fA-F]{3,8}', html))
    # Filter meaningful colors (not just #fff, #000)
    for c in sorted(hex_colors):
        if c.lower() not in ['#fff', '#ffffff', '#000', '#000000', '#fff0', '#fffff0', '#f0ffff']:
            colors.append(c)
    # RGB colors
    rgb_colors = set(re.findall(r'rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)', html))
    for c in sorted(rgb_colors):
        colors.append(c)
    return colors[:20]


def extract_fonts(html):
    """Extract font families used"""
    fonts = set()
    # font-family in CSS
    for m in re.finditer(r'font-family\s*:\s*([^;}]+)', html, re.IGNORECASE):
        for font in m.group(1).split(','):
            font = font.strip().strip("'\"").strip()
            if font and font not in ['serif', 'sans-serif', 'monospace', 'inherit']:
                fonts.add(font)
    # Google Fonts
    for m in re.finditer(r'fonts\.googleapis\.com/css[^"\']*family=([^"\'&]+)', html):
        family = m.group(1).replace('+', ' ')
        fonts.add(family.split(':')[0])
    return sorted(fonts)


def extract_spacing(html):
    """Extract spacing/margin/padding values"""
    spaces = set()
    for m in re.finditer(r'(padding|margin|gap)\s*:\s*([^;}]+)', html, re.IGNORECASE):
        spaces.add(f"{m.group(1)}: {m.group(2).strip()}")
    return sorted(spaces)[:15]


def extract_logos(html, base_url):
    """Extract logo image URLs"""
    soup = BeautifulSoup(html, 'html.parser')
    logos = []
    # Look for logo in common places
    for img in soup.find_all('img'):
        src = img.get('src', '') or img.get('data-src', '')
        if not src:
            continue
        if any(k in img.get('class', []) + [img.get('alt', '').lower(), img.get('id', '').lower()]
               for k in ['logo', 'brand', 'site-logo']):
            if src.startswith('/'):
                src = base_url.rstrip('/') + src
            logos.append(src)
    # Also check OG image
    og = soup.find('meta', property='og:image')
    if og and og.get('content'):
        logos.append(og['content'])
    return logos[:5]


def generate_token_report(url, html):
    """Generate design token report"""
    base_url = '/'.join(url.split('/')[:3])
    
    report = {
        "source": url,
        "fetched_at": __import__('datetime').datetime.now().isoformat(),
        "design_tokens": {
            "css_variables": extract_css_variables(html),
            "colors": extract_colors(html),
            "fonts": extract_fonts(html),
            "spacing": extract_spacing(html),
        },
        "assets": {
            "logos": extract_logos(html, base_url),
        },
        "tech_stack": {
            "cms": "WordPress" if '/wp-content/' in html or 'wp-json' in html else "Unknown",
            "has_tailwind": 'tailwind' in html.lower(),
            "has_bootstrap": 'bootstrap' in html.lower(),
        }
    }
    return report


def apply_tokens_to_css(tokens, css_path):
    """Apply extracted design tokens to our CSS file"""
    colors = tokens["design_tokens"]["colors"]
    fonts = tokens["design_tokens"]["fonts"]
    vars_dict = tokens["design_tokens"]["css_variables"]
    
    with open(css_path, 'r') as f:
        css = f.read()
    
    changes = []
    
    # Find the accent color (most used non-neutral color)
    color_counts = {}
    for c in colors:
        if isinstance(c, str) and c.startswith('#'):
            color_counts[c] = css.count(c)
    
    # Apply fonts
    if fonts:
        primary_font = fonts[0]
        # Replace --font-serif with the site's font
        if 'font-serif' in css:
            # Just add a comment instead of replacing (keep our serif but add theirs)
            pass
    
    # Apply accent colors
    if vars_dict:
        accent = vars_dict.get('--swiper-pagination-color') or vars_dict.get('--accent')
        if accent:
            if '--accent' in css:
                # Add their accent as a secondary variable
                css = css.replace(
                    '--radius: 0px;',
                    f'--radius: 0px;\n  --cloned-accent: {accent};'
                )
                changes.append(f"Added accent: {accent}")
    
    # Write back
    with open(css_path, 'w') as f:
        f.write(css)
    
    return changes


def main():
    if len(sys.argv) < 2:
        print("📡 Website Cloner Tool")
        print(f"Cách dùng: {sys.argv[0]} <URL> [--apply-css PATH]")
        print("  --apply-css PATH: apply design tokens vào file CSS")
        sys.exit(1)
    
    url = sys.argv[1]
    apply_css = None
    if '--apply-css' in sys.argv:
        idx = sys.argv.index('--apply-css')
        apply_css = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None
    
    print(f"🔍 Cloning: {url}")
    print(f"📡 Fetching...")
    
    html = fetch(url)
    print(f"✅ Fetched: {len(html)} bytes")
    
    print(f"🔬 Extracting design tokens...")
    report = generate_token_report(url, html)
    
    print(f"\n{'='*50}")
    print(f"📊 DESIGN TOKEN REPORT")
    print(f"{'='*50}")
    
    print(f"\n🎨 COLORS:")
    for c in report["design_tokens"]["colors"][:10]:
        print(f"   {c}")
    
    print(f"\n🔤 FONTS:")
    for f in report["design_tokens"]["fonts"]:
        print(f"   {f}")
    
    print(f"\n📐 CSS VARIABLES:")
    for k, v in list(report["design_tokens"]["css_variables"].items())[:15]:
        print(f"   {k}: {v}")
    
    print(f"\n🖼 LOGOS:")
    for l in report["assets"]["logos"]:
        print(f"   {l}")
    
    print(f"\n🏗 TECH: {json.dumps(report['tech_stack'], ensure_ascii=False)}")
    
    # Save report
    reports_dir = os.path.expanduser("~/.hermes/profiles/meow/reports")
    fname = f"cloned_{url.split('://')[1].split('/')[0].replace('.','_')}.json"
    fpath = os.path.join(reports_dir, fname)
    os.makedirs(reports_dir, exist_ok=True)
    with open(fpath, 'w') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Saved: {fpath}")
    
    # Apply CSS if requested
    if apply_css:
        print(f"\n✏️  Applying tokens to CSS: {apply_css}")
        changes = apply_tokens_to_css(report, apply_css)
        for c in changes:
            print(f"   ✅ {c}")
        print(f"✅ CSS updated!")
    
    print(f"\n✅ Done!")


if __name__ == "__main__":
    main()
