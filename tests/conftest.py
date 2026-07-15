import json
import os
import tempfile
import pytest


@pytest.fixture
def reports_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture(autouse=True)
def isolate_reports_dir(monkeypatch, request):
    if "no_auto_isolate" in request.keywords:
        return
    tmp = tempfile.mkdtemp()
    monkeypatch.setattr("scripts.config.REPORTS_DIR", tmp)
    monkeypatch.setattr("scripts.lib.storage.REPORTS_DIR", tmp)


@pytest.fixture
def sample_article():
    return {
        "id": "article_2026-07-15_test1234",
        "title": "Test Article Title",
        "date": "2026-07-15",
        "date_display": "Wednesday, 15/07/2026",
        "category": "economy",
        "category_name": "Kinh tế",
        "emoji": "📰",
        "excerpt": "This is a test article excerpt...",
        "content_html": "<p>Test content paragraph.</p>",
        "tags": ["kinh-te", "test"],
        "sources": ["https://example.com/article"],
        "lead_image": "https://example.com/image.jpg",
        "word_count": 50,
        "source_url": "https://example.com/article",
        "generated_at": "2026-07-15T08:00:00",
    }


@pytest.fixture
def app(reports_dir):
    import frontend.app
    frontend.app.REPORTS_DIR = reports_dir
    from frontend.app import app
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()
