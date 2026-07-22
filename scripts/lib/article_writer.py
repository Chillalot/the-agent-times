import re
from bs4 import BeautifulSoup

FALLBACK_IMAGES = {
    "technology": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&auto=format",
    "github": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format",
    "economic": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&auto=format",
    "economy": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&auto=format",
    "fnb": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&auto=format",
    "legal": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=800&auto=format",
    "daily-briefing": "https://images.unsplash.com/photo-1504711434969-e33886168d6c?w=800&auto=format",
}

DEFAULT_IMAGE = "https://images.unsplash.com/photo-1495020689067-958852a7765e?w=800&auto=format"


def _pick_fallback(category):
    return FALLBACK_IMAGES.get(category, DEFAULT_IMAGE)


def _clean_light(soup):
    for junk in soup.find_all(["script", "style", "nav", "aside", "footer", "header", "iframe", "form", "noscript"]):
        junk.decompose()
    for el in soup.find_all(True):
        if el.name == "a" and not el.get("href"):
            el.unwrap()
            continue
        if el.name in ("img", "figure", "figcaption", "picture", "source", "video", "audio"):
            continue
        if "class" in el.attrs:
            del el["class"]
        if "style" in el.attrs:
            del el["style"]
        if "rel" in el.attrs:
            del el["rel"]
        if "id" in el.attrs and el.name not in ("h1", "h2", "h3", "h4", "h5", "h6"):
            del el["id"]
    return soup


def extract_body_images(soup, base_url=None):
    images = []
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src") or img.get("data-lazy-src") or ""
        if not src:
            continue
        if src.startswith("data:") or len(src) < 10:
            continue
        alt = img.get("alt", "") or ""
        if base_url:
            if src.startswith("//"):
                src = "https:" + src
            elif src.startswith("/") and "://" not in src:
                from urllib.parse import urlparse
                parsed = urlparse(base_url)
                src = f"{parsed.scheme}://{parsed.netloc}{src}"
        if any(kw in src.lower() for kw in ["icon", "logo", "avatar", "spacer", "pixel", "banner"]):
            continue
        images.append({"src": src, "alt": alt})
    seen = set()
    unique = []
    for img in images:
        if img["src"] not in seen:
            seen.add(img["src"])
            unique.append(img)
    return unique


def build_full_article(*, title, content_html, lead_image=None, source_url=None,
                       category=None, source_name=None):
    soup = BeautifulSoup(content_html, "html.parser")
    soup = _clean_light(soup)

    body_images = extract_body_images(soup, source_url)

    all_image_srcs = []
    if lead_image:
        all_image_srcs.append(lead_image)
    for img in body_images:
        all_image_srcs.append(img["src"])

    final_lead = all_image_srcs[0] if all_image_srcs else _pick_fallback(category)

    content_parts = []
    for el in soup.children:
        html_str = str(el)
        if not el.name:
            continue
        if el.name in ("img", "figure", "picture", "video", "audio", "source", "br", "hr", "iframe", "table"):
            content_parts.append(html_str)
        elif el.find_all("img"):
            content_parts.append(html_str)
        elif el.get_text(strip=True):
            content_parts.append(html_str)
        elif el.get_text(strip=True):
            content_parts.append(html_str)

    if not content_parts:
        content_parts = [f"<p>{content_html[:500]}</p>"]

    body = "\n".join(content_parts)

    text_plain = re.sub(r"<[^>]+>", "", body).strip()
    excerpt = ""
    for p in content_parts:
        text = re.sub(r"<[^>]+>", "", p).strip()
        text = re.sub(r"\s+", " ", text)
        if len(text) > 60:
            excerpt = text[:250].rsplit(" ", 1)[0] + "..." if len(text) > 250 else text
            break
    if not excerpt:
        excerpt = text_plain[:250].strip().replace("\n", " ")
        if len(text_plain) > 250:
            excerpt += "..."

    tags = _extract_keywords(text_plain)
    if category and category not in tags:
        tags.insert(0, category)

    word_count = len(text_plain.split())

    return {
        "content_html": body,
        "excerpt": excerpt,
        "tags": tags,
        "word_count": word_count,
        "lead_image": final_lead,
        "body_images": body_images,
    }


def _clean_paragraphs(html):
    soup = BeautifulSoup(html, "html.parser")
    for junk in soup.find_all(["script", "style", "nav", "aside", "footer", "header", "iframe", "form"]):
        junk.decompose()
    for tag in soup.find_all(True):
        if tag.name in ("figure", "img", "blockquote", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "li", "p", "table"):
            continue
        tag.unwrap()
    paragraphs = []
    for el in soup.find_all(["p", "blockquote", "ul", "ol", "h2", "h3", "h4", "figure", "img"]):
        text = el.get_text(strip=True)
        if el.name == "p" and len(text) > 30:
            paragraphs.append(str(el))
        elif el.name in ("blockquote", "h2", "h3", "h4") and len(text) > 10:
            paragraphs.append(str(el))
        elif el.name in ("ul", "ol"):
            items = el.find_all("li")
            valid = [li for li in items if len(li.get_text(strip=True)) > 10]
            if valid:
                new_list = soup.new_tag(el.name)
                for li in valid:
                    new_list.append(li)
                paragraphs.append(str(new_list))
        elif el.name in ("figure", "img") and el.get("src"):
            paragraphs.append(str(el))
    return paragraphs


def _generate_excerpt(paragraphs, max_len=250):
    for p in paragraphs:
        text = re.sub(r"<[^>]+>", "", p).strip()
        text = re.sub(r"\s+", " ", text)
        if len(text) > 40:
            if len(text) > max_len:
                return text[:max_len].rsplit(" ", 1)[0] + "..."
            return text
    return ""


def _extract_keywords(text, max_tags=6):
    keywords = [
        ("kinh tế", "kinh-tế"), ("gdp", "kinh-tế"), ("tăng trưởng", "kinh-tế"),
        ("thuế", "pháp-lý"), ("pháp luật", "pháp-lý"), ("quy định", "pháp-lý"),
        ("công nghệ", "công-nghệ"), ("ai", "ai"), ("trí tuệ nhân tạo", "ai"),
        ("startup", "startup"), ("blockchain", "blockchain"),
        ("apple", "apple"), ("google", "google"), ("microsoft", "microsoft"),
        ("nvidia", "nvidia"), ("facebook", "meta"), ("meta", "meta"),
        ("chứng khoán", "chứng-khoán"), ("đầu tư", "đầu-tư"),
        ("bất động sản", "bất-động-sản"), ("nhà đất", "bất-động-sản"),
        ("thế giới", "thế-giới"), ("mỹ", "mỹ"), ("trung quốc", "trung-quốc"),
        ("việt nam", "việt-nam"), ("fnb", "fnb"), ("ẩm thực", "fnb"),
        ("nhà hàng", "fnb"), ("thực phẩm", "fnb"),
    ]
    text_lower = text.lower()
    tags = []
    for kw, tag in keywords:
        if kw in text_lower and tag not in tags:
            tags.append(tag)
            if len(tags) >= max_tags:
                break
    return tags if tags else ["tin-tức"]


def build_article_html(*, title, content_html, lead_image=None, source_url=None,
                       category=None, source_name=None):
    paragraphs = _clean_paragraphs(content_html)
    if not paragraphs:
        paragraphs = [f"<p>{content_html[:500]}</p>"]
    parts = []
    if lead_image:
        parts.append(
            f'<figure class="article-featured-image" style="margin:0 0 24px;">'
            f'<img src="{lead_image}" alt="{title}" '
            f'style="width:100%;max-width:100%;border-radius:8px;" />'
            f'</figure>'
        )
    excerpt = _generate_excerpt(paragraphs)
    if excerpt:
        parts.append(
            f'<blockquote class="article-summary" '
            f'style="border-left:3px solid var(--accent,#c00);margin:0 0 24px;'
            f'padding:8px 16px;font-style:italic;color:var(--text-gray,#666);">'
            f'{excerpt}'
            f'</blockquote>'
        )
    parts.extend(paragraphs)
    if source_url:
        source_label = source_name or source_url
        parts.append(
            f'<p style="margin-top:24px;font-size:13px;color:#888;border-top:1px solid #eee;'
            f'padding-top:16px;">'
            f'📎 Nguồn: <a href="{source_url}" target="_blank" rel="noopener">{source_label}</a>'
            f'</p>'
        )
    full_html = "\n".join(parts)
    text_plain = re.sub(r"<[^>]+>", "", full_html).strip()
    word_count = len(text_plain.split())
    if not excerpt:
        excerpt = text_plain[:250].strip().replace("\n", " ")
        if len(text_plain) > 250:
            excerpt += "..."
    tags = _extract_keywords(text_plain)
    if category and category not in tags:
        tags.insert(0, category)
    return {
        "content_html": full_html,
        "excerpt": excerpt,
        "tags": tags,
        "word_count": word_count,
    }
