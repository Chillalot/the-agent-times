import pytest
from scripts.lib.article_writer import (
    build_article_html,
    build_full_article,
    _clean_paragraphs,
    _generate_excerpt,
    _extract_keywords,
    extract_body_images,
    _clean_light,
    _pick_fallback,
)
from bs4 import BeautifulSoup


class TestExtractKeywords:
    def test_keywords_extracted(self):
        text = "công nghệ AI startup"
        tags = _extract_keywords(text)
        assert isinstance(tags, list)
        assert all(isinstance(t, str) for t in tags)
        assert len(tags) > 0

    def test_keywords_deduplicated(self):
        text = "công nghệ công nghệ AI AI"
        tags = _extract_keywords(text)
        assert len(tags) == len(set(tags))

    def test_short_text_returns_fallback(self):
        tags = _extract_keywords("a b c")
        assert "tin-tức" in tags


class TestGenerateExcerpt:
    def test_excerpt_from_paragraph(self):
        paragraphs = [
            "<p>This is a long paragraph with enough words to create a proper excerpt that should be truncated.</p>"
        ]
        excerpt = _generate_excerpt(paragraphs)
        assert isinstance(excerpt, str)
        assert len(excerpt) > 0
        assert len(excerpt) <= 260

    def test_excerpt_removes_html(self):
        paragraphs = ["<p>Hello <b>world</b> this is a test paragraph with enough content</p>"]
        excerpt = _generate_excerpt(paragraphs)
        assert "<b>" not in excerpt
        assert "</b>" not in excerpt

    def test_excerpt_empty_fallback(self):
        excerpt = _generate_excerpt(["<p></p>"])
        assert excerpt == ""

    def test_short_paragraph_skipped(self):
        excerpts = _generate_excerpt(["<p>short</p>", "<p>This is a longer paragraph with enough content for excerpt.</p>"])
        assert len(excerpts) > 0


class TestCleanParagraphs:
    def test_removes_junk_from_html(self):
        html = (
            "<script>alert(1)</script>"
            "<p>This is a long enough paragraph that should be kept.</p>"
            "<style>.cls{}</style>"
            "<div>A short div that will be unwrapped and dropped</div>"
        )
        result = _clean_paragraphs(html)
        assert len(result) == 1
        assert "script" not in result[0]
        assert "style" not in result[0]
        assert "This is a long enough paragraph" in result[0]

    def test_short_paragraphs_filtered(self):
        result = _clean_paragraphs("<p>ab</p><p>This is a long enough paragraph with meaningful content to keep.</p>")
        assert len(result) == 1
        assert "meaningful content" in result[0]

    def test_empty_html_returns_fallback_handled(self):
        result = _clean_paragraphs("<p></p><div></div>")
        assert result == []

    def test_multiple_valid_paragraphs(self):
        html = (
            "<p>First long paragraph that has enough content to pass the threshold check.</p>"
            "<p>Second paragraph also long enough to be kept in the output list.</p>"
        )
        result = _clean_paragraphs(html)
        assert len(result) == 2


class TestBuildArticleHtml:
    def test_minimal_article(self):
        article = build_article_html(
            title="Test",
            content_html="<p>Hello world paragraph that is long enough for the filter.</p>",
            source_url="https://example.com",
        )
        assert "content_html" in article
        assert "excerpt" in article
        assert "tags" in article
        assert "word_count" in article

    def test_lead_image_included(self):
        article = build_article_html(
            title="Test",
            content_html="<p>Content here paragraph that is long enough for filtering.</p>",
            lead_image="https://example.com/img.jpg",
            source_url="https://example.com",
        )
        assert "img" in article["content_html"]
        assert "example.com/img.jpg" in article["content_html"]

    def test_source_attribution(self):
        article = build_article_html(
            title="Test",
            content_html="<p>Content paragraph that is long enough for the filter threshold.</p>",
            source_url="https://example.com/article",
            source_name="Example News",
            category="tech",
        )
        assert "Example News" in article["content_html"]

    def test_word_count_includes_source(self):
        article = build_article_html(
            title="Test",
            content_html="<p>one two three four five six seven eight nine ten</p>",
            source_url="https://example.com",
        )
        assert article["word_count"] > 0

    def test_tags_includes_category(self):
        article = build_article_html(
            title="Test",
            content_html="<p>Content about technology and AI paragraph that is long enough to be kept by the filter.</p>",
            source_url="https://example.com",
            category="technology",
        )
        assert "technology" in article["tags"]
        assert "ai" in article["tags"]


class TestCleanLight:
    def test_removes_script_style(self):
        soup = BeautifulSoup("<script>alert(1)</script><p>text</p>", "html.parser")
        result = _clean_light(soup)
        assert not result.find("script")

    def test_removes_class_and_style(self):
        soup = BeautifulSoup('<p class="test" style="color:red">text</p>', "html.parser")
        result = _clean_light(soup)
        p = result.find("p")
        assert "class" not in p.attrs or not p.get("class")
        assert "style" not in p.attrs or not p.get("style")


class TestExtractBodyImages:
    def test_extracts_img_tags(self):
        soup = BeautifulSoup(
            '<p>text</p><img src="https://example.com/photo.jpg" alt="photo">',
            "html.parser",
        )
        images = extract_body_images(soup)
        assert len(images) == 1
        assert images[0]["src"] == "https://example.com/photo.jpg"

    def test_skips_icon_logo(self):
        soup = BeautifulSoup(
            '<img src="https://example.com/icon.png" alt="icon">'
            '<img src="https://example.com/photo.jpg" alt="photo">',
            "html.parser",
        )
        images = extract_body_images(soup)
        assert len(images) == 1
        assert "photo" in images[0]["src"]

    def test_deduplicates(self):
        soup = BeautifulSoup(
            '<img src="https://example.com/img.jpg"><img src="https://example.com/img.jpg">',
            "html.parser",
        )
        images = extract_body_images(soup)
        assert len(images) == 1

    def test_empty_when_no_images(self):
        soup = BeautifulSoup("<p>no images here</p>", "html.parser")
        images = extract_body_images(soup)
        assert images == []


class TestPickFallback:
    def test_return_url_for_known_category(self):
        url = _pick_fallback("technology")
        assert url.startswith("http")
        assert "unsplash" in url

    def test_default_for_unknown_category(self):
        url = _pick_fallback("unknown-category")
        assert url.startswith("http")

    def test_all_categories_have_images(self):
        from scripts.lib.article_writer import FALLBACK_IMAGES
        assert "technology" in FALLBACK_IMAGES
        assert "economy" in FALLBACK_IMAGES
        assert "fnb" in FALLBACK_IMAGES
        assert "legal" in FALLBACK_IMAGES


class TestBuildFullArticle:
    def test_returns_expected_keys(self):
        result = build_full_article(
            title="Test",
            content_html="<p>This is a test paragraph that is long enough for the system.</p>",
            source_url="https://example.com",
        )
        assert "content_html" in result
        assert "excerpt" in result
        assert "tags" in result
        assert "word_count" in result
        assert "lead_image" in result
        assert "body_images" in result

    def test_preserves_short_paragraphs(self):
        result = build_full_article(
            title="Test",
            content_html="<p>Short</p><p>This is a longer paragraph that has enough text to be meaningful.</p>",
            source_url="https://example.com",
        )
        assert "Short" in result["content_html"]
        assert "meaningful" in result["content_html"]

    def test_fallback_image_when_none(self):
        result = build_full_article(
            title="Test",
            content_html="<p>Content with no images provided anywhere.</p>",
            source_url="https://example.com",
            category="technology",
        )
        assert result["lead_image"].startswith("http")
        assert "unsplash" in result["lead_image"]

    def test_preserves_html_structure(self):
        result = build_full_article(
            title="Test",
            content_html=(
                "<h2>Heading</h2>"
                "<p>Paragraph with content that is substantial.</p>"
                "<ul><li>Item one</li><li>Item two</li></ul>"
                "<blockquote>A quote of some significance.</blockquote>"
            ),
            source_url="https://example.com",
        )
        assert "<h2>" in result["content_html"]
        assert "<ul>" in result["content_html"]
        assert "<blockquote>" in result["content_html"]

    def test_body_images_extracted(self):
        result = build_full_article(
            title="Test",
            content_html=(
                "<p>First paragraph.</p>"
                '<img src="https://example.com/img1.jpg" alt="1">'
                "<p>Second paragraph.</p>"
                '<img src="https://example.com/img2.jpg" alt="2">'
            ),
            source_url="https://example.com",
        )
        assert len(result["body_images"]) == 2
        assert "img1" in result["body_images"][0]["src"]

    def test_lead_image_prioritized(self):
        result = build_full_article(
            title="Test",
            content_html='<img src="https://example.com/body.jpg"><p>Content.</p>',
            lead_image="https://example.com/lead.jpg",
            source_url="https://example.com",
        )
        assert result["lead_image"] == "https://example.com/lead.jpg"

    def test_excerpt_from_content(self):
        result = build_full_article(
            title="Test",
            content_html="<p>This is a sufficiently long paragraph that should produce a valid excerpt from the build full article function.</p>",
            source_url="https://example.com",
        )
        assert len(result["excerpt"]) > 20

    def test_tags_include_category(self):
        result = build_full_article(
            title="Test",
            content_html="<p>Content about technology and AI paragraph.</p>",
            source_url="https://example.com",
            category="technology",
        )
        assert "technology" in result["tags"]
