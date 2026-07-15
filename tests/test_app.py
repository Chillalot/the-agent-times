import json
import os


class TestAppRoutes:
    def test_homepage_returns_200(self, client):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_homepage_sets_no_cache_headers(self, client):
        resp = client.get("/")
        assert resp.headers.get("Cache-Control") == "no-cache, no-store, must-revalidate, max-age=0"

    def test_404_returns_200_with_content(self, client):
        resp = client.get("/nonexistent")
        assert resp.status_code == 404

    def test_category_valid(self, client):
        resp = client.get("/category/economy")
        assert resp.status_code == 200

    def test_category_invalid_returns_404(self, client):
        resp = client.get("/category/nonexistent")
        assert resp.status_code == 404

    def test_search_returns_200(self, client):
        resp = client.get("/search?q=test")
        assert resp.status_code == 200

    def test_search_empty_returns_200(self, client):
        resp = client.get("/search?q=")
        assert resp.status_code == 200

    def test_article_404_returns_404(self, client):
        resp = client.get("/article/nonexistent")
        assert resp.status_code == 404

    def test_date_route_200(self, client):
        resp = client.get("/date/2026-07-15")
        assert resp.status_code == 200


class TestAppWithArticles:
    def test_homepage_with_article(self, client, reports_dir, sample_article):
        fpath = os.path.join(reports_dir, f"{sample_article['id']}.json")
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(sample_article, f)

        resp = client.get("/")
        assert resp.status_code == 200
        assert sample_article["title"].encode() in resp.data

    def test_article_page(self, client, reports_dir, sample_article):
        fpath = os.path.join(reports_dir, f"{sample_article['id']}.json")
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(sample_article, f)

        resp = client.get(f"/article/{sample_article['id']}")
        assert resp.status_code == 200
        assert sample_article["title"].encode() in resp.data
