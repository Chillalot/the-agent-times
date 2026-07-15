import re
import ssl
import urllib.error
import urllib.request
from xml.etree import ElementTree as ET

from scripts.config import RSS_TIMEOUT

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def _strip_cdata(text):
    if not text:
        return ""
    return re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", text)


def fetch_rss(url, max_items=15):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
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

    # RSS 2.0
    for item in root.iter("item"):
        title = _strip_cdata(item.findtext("title", "")).strip()
        link = item.findtext("link", "").strip()
        desc = _strip_cdata(item.findtext("description", ""))
        desc = re.sub(r"<[^>]+>", "", desc).strip()
        pub_date = item.findtext("pubDate", "").strip()
        author = item.findtext("author", "").strip() or item.findtext("{http://purl.org/dc/elements/1.1/}creator", "").strip()
        if title:
            items.append({"title": title, "link": link, "desc": desc[:500], "pub_date": pub_date, "author": author})
            if len(items) >= max_items:
                break

    # Atom fallback
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

            if title:
                items.append({"title": title, "link": link, "desc": desc[:500], "pub_date": pub_date})
                if len(items) >= max_items:
                    break

    return {"error": None, "items": items}
