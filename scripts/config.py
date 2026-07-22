#!/usr/bin/env python3
import os
from pathlib import Path

# Base directories — override via env vars
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = Path(os.environ.get("SCRIPTS_DIR", PROJECT_ROOT / "scripts"))
REPORTS_DIR = Path(os.environ.get("REPORTS_DIR", PROJECT_ROOT / "data" / "reports"))

# Ensure reports dir exists
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# RSS defaults
RSS_TIMEOUT = int(os.environ.get("RSS_TIMEOUT", "20"))
MAX_ITEMS_PER_FEED = int(os.environ.get("MAX_ITEMS_PER_FEED", "15"))

# Translation
TRANSLATION_ENABLED = os.environ.get("TRANSLATION_ENABLED", "1") == "1"

# Category metadata (single source of truth)
CATEGORY_MAP = {
    "economy": {"name": "Kinh tế", "emoji": "📰", "id": "economy"},
    "daily-briefing": {"name": "Kinh tế", "emoji": "📰", "id": "daily-briefing"},
    "technology": {"name": "Công nghệ", "emoji": "💻", "id": "technology"},
    "github": {"name": "GitHub / Công nghệ", "emoji": "🐙", "id": "github"},
    "legal": {"name": "Pháp lý & Thuế", "emoji": "⚖️", "id": "legal"},
    "affiliate": {"name": "Affiliate", "emoji": "💰", "id": "affiliate"},
    "fnb": {"name": "F&B & Quán ăn", "emoji": "🍗", "id": "fnb"},
    "economic": {"name": "Phân tích Kinh tế", "emoji": "📊", "id": "economic"},
    "market": {"name": "Thị trường", "emoji": "📈", "id": "market"},
}

CATEGORY_NAMES = {k: v["name"] for k, v in CATEGORY_MAP.items()}
CATEGORY_EMOJIS = {k: v["emoji"] for k, v in CATEGORY_MAP.items()}
