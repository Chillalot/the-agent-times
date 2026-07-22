import os
import json
import pytest
from scripts.lib.storage import save_article_json, load_all_articles
from scripts.config import REPORTS_DIR as DEFAULT_REPORTS_DIR


@pytest.fixture(autouse=True)
def use_tmp_reports_dir(monkeypatch, tmp_path):
    monkeypatch.setattr("scripts.config.REPORTS_DIR", tmp_path)
    monkeypatch.setattr("scripts.lib.storage.REPORTS_DIR", tmp_path)


class TestSaveArticle:
    def test_save_new_article(self, tmp_path):
        article = {"id": "test_001", "title": "Test", "date": "2026-07-15"}
        fpath, is_new = save_article_json(article)
        assert is_new is True
        assert os.path.exists(fpath)

    def test_save_duplicate_skips(self, tmp_path):
        article = {"id": "test_002", "title": "Test", "date": "2026-07-15"}
        fpath, is_new = save_article_json(article)
        assert is_new is True

        fpath2, is_new2 = save_article_json(article)
        assert is_new2 is False
        assert fpath == fpath2

    def test_save_overwrite(self, tmp_path):
        article = {"id": "test_003", "title": "V1", "content": "old"}
        fpath, _ = save_article_json(article)

        article["content"] = "new"
        fpath2, is_new = save_article_json(article, overwrite=True)
        assert is_new is True

        with open(fpath2, "r") as f:
            data = json.load(f)
        assert data["content"] == "new"


class TestLoadArticles:
    def test_load_empty_dir(self, tmp_path):
        articles = load_all_articles(reports_dir=tmp_path)
        assert articles == []

    def test_load_articles(self, tmp_path):
        for i in range(3):
            article = {"id": f"test_{i:03d}", "title": f"Article {i}", "date": f"2026-07-{15-i:02d}"}
            fpath = os.path.join(tmp_path, f"test_{i:03d}.json")
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(article, f)

        articles = load_all_articles(reports_dir=tmp_path)
        assert len(articles) == 3

    def test_skip_invalid_json(self, tmp_path):
        fpath = os.path.join(tmp_path, "invalid.json")
        with open(fpath, "w") as f:
            f.write("not json")

        articles = load_all_articles(reports_dir=tmp_path)
        assert len(articles) == 0
