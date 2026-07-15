import pytest
from scripts.article_scraper import detect_category, clean_html, extract_lead_image
from bs4 import BeautifulSoup


class TestDetectCategory:
    def test_economic_keyword(self):
        cat = detect_category("GDP growth", "economy grows")
        assert cat == "economic"

    def test_legal_keyword(self):
        cat = detect_category("Tax law", "new regulation on thuế")
        assert cat == "legal"

    def test_fnb_keyword(self):
        cat = detect_category("Best quán cơm", "nhà hàng review")
        assert cat == "fnb"

    def test_default_category(self):
        cat = detect_category("Random title", "some random text")
        assert cat == "daily-briefing"


class TestCleanHtml:
    def test_removes_readability_wrappers(self):
        html = '<html><body><div><p>Hello</p></div></body></html>'
        result = clean_html(html)
        assert '<html>' not in result
        assert '<body>' not in result
        assert '<p>Hello</p>' in result

    def test_removes_class_attributes(self):
        html = '<p class="some-class">Text</p>'
        result = clean_html(html)
        assert 'class=' not in result
        assert '<p>Text</p>' in result

    def test_removes_empty_tags(self):
        html = '<p></p><span>Content</span>'
        result = clean_html(html)
        assert '<p></p>' not in result
        assert '<span>Content</span>' in result

    def test_removes_rel_attributes(self):
        html = '<a href="http://x.com" rel="noopener">Link</a>'
        result = clean_html(html)
        assert 'rel=' not in result


class TestExtractLeadImage:
    def test_og_image_returns_first(self):
        html = '''
        <html>
          <meta property="og:image" content="https://og.image.jpg">
          <meta name="twitter:image" content="https://twitter.image.jpg">
        </html>
        '''
        soup = BeautifulSoup(html, "html.parser")
        result = extract_lead_image(soup, "https://example.com")
        assert result == "https://og.image.jpg"

    def test_twitter_image_fallback(self):
        html = '''
        <html>
          <meta name="twitter:image" content="https://twitter.image.jpg">
        </html>
        '''
        soup = BeautifulSoup(html, "html.parser")
        result = extract_lead_image(soup, "https://example.com")
        assert result == "https://twitter.image.jpg"

    def test_no_image_returns_none(self):
        html = '<html><body><p>No images here</p></body></html>'
        soup = BeautifulSoup(html, "html.parser")
        result = extract_lead_image(soup, "https://example.com")
        assert result is None

    def test_relative_url_resolved(self):
        html = '''
        <html>
          <meta property="og:image" content="/images/photo.jpg">
        </html>
        '''
        soup = BeautifulSoup(html, "html.parser")
        result = extract_lead_image(soup, "https://example.com/page")
        assert result == "https://example.com/images/photo.jpg"
