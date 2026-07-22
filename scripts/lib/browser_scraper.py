import re
import time
from bs4 import BeautifulSoup

_BROWSER = None
_BROWSER_REFCOUNT = 0


def get_browser():
    global _BROWSER, _BROWSER_REFCOUNT
    if _BROWSER is None:
        from cloakbrowser import launch
        _BROWSER = launch(headless=True)
    _BROWSER_REFCOUNT += 1
    return _BROWSER


def release_browser():
    global _BROWSER_REFCOUNT, _BROWSER
    _BROWSER_REFCOUNT -= 1
    if _BROWSER_REFCOUNT <= 0 and _BROWSER is not None:
        try:
            _BROWSER.close()
        except Exception:
            pass
        _BROWSER = None


def extract_from_html(html, url):
    soup = BeautifulSoup(html, "html.parser")
    for junk in soup.find_all(["script", "style", "nav", "aside", "footer", "header", "noscript"]):
        junk.decompose()
    title = soup.title.get_text(strip=True) if soup.title else ""
    h1 = soup.find("h1")
    if h1:
        title = h1.get_text(strip=True)
    content_html = str(soup.body) if soup.body else str(soup)
    lead_image = None
    og = soup.find("meta", property="og:image")
    if og and og.get("content"):
        lead_image = og["content"]
    if not lead_image:
        tw = soup.find("meta", attrs={"name": "twitter:image"})
        if tw and tw.get("content"):
            lead_image = tw["content"]
    if not lead_image:
        first_img = soup.find("img")
        if first_img:
            src = first_img.get("src") or ""
            if src and not src.startswith("data:") and len(src) > 20:
                if "icon" not in src.lower() and "logo" not in src.lower():
                    lead_image = src
    return {"title": title, "content_html": content_html, "lead_image": lead_image, "success": True}


def fetch_article(url, timeout=45):
    browser = get_browser()
    try:
        page = browser.new_page()
        page.set_default_timeout(timeout * 1000)
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=timeout * 1000)
        except Exception:
            try:
                page.goto(url, timeout=timeout * 1000)
            except Exception:
                page.close()
                return {"success": False, "error": "Timeout loading page"}
        time.sleep(3)
        try:
            page.wait_for_load_state("networkidle", timeout=8000)
        except Exception:
            pass
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        html = page.content()
        page.close()
        result = extract_from_html(html, url)
        result["content_html"] = str(BeautifulSoup(html, "html.parser"))
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}
