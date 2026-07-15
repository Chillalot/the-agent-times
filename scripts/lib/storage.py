import json
import os
from pathlib import Path

from scripts.config import REPORTS_DIR


def save_article_json(article_data, overwrite=False):
    os.makedirs(REPORTS_DIR, exist_ok=True)
    fpath = os.path.join(REPORTS_DIR, f"{article_data['id']}.json")
    if os.path.exists(fpath):
        if overwrite:
            os.remove(fpath)
        else:
            print(f"    Skipping (exists): {os.path.basename(fpath)}")
            return fpath, False
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(article_data, f, ensure_ascii=False, indent=2)
    return fpath, True


def load_all_articles(reports_dir=None):
    articles = []
    rdir = Path(reports_dir or REPORTS_DIR)
    if not rdir.exists():
        return []

    for fpath in sorted(rdir.glob("*.json"), reverse=True):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            articles.append(data)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[!] Error reading {fpath}: {e}")

    return articles
