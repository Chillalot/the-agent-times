#!/usr/bin/env python3
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

REPORTS_DIR = Path(os.environ.get("REPORTS_DIR", PROJECT_ROOT / "data" / "reports"))
SCRIPTS_DIR = Path(os.environ.get("SCRIPTS_DIR", PROJECT_ROOT / "scripts"))

PORT = int(os.environ.get("PORT", "5050"))
DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"
HOST = os.environ.get("HOST", "0.0.0.0")

CATEGORY_MAP = {
    "economy": {"name": "📰 Kinh tế", "emoji": "📰", "id": "economy"},
    "daily-briefing": {"name": "📰 Kinh tế", "emoji": "📰", "id": "daily-briefing"},
    "technology": {"name": "💻 Công nghệ", "emoji": "💻", "id": "technology"},
    "github": {"name": "🐙 GitHub", "emoji": "🐙", "id": "github"},
    "legal": {"name": "⚖️ Pháp lý & Thuế", "emoji": "⚖️", "id": "legal"},
    "affiliate": {"name": "💰 Affiliate", "emoji": "💰", "id": "affiliate"},
    "fnb": {"name": "🍗 F&B & Quán ăn", "emoji": "🍗", "id": "fnb"},
    "economic": {"name": "📊 Phân tích Kinh tế", "emoji": "📊", "id": "economic"},
    "market": {"name": "📈 Thị trường", "emoji": "📈", "id": "market"},
}

CATEGORY_COLORS = {
    "economy": {"label": "Kinh tế", "bg": "#dbeafe", "text": "#1e40af", "border": "#2563eb"},
    "daily-briefing": {"label": "Kinh tế", "bg": "#dbeafe", "text": "#1e40af", "border": "#2563eb"},
    "technology": {"label": "Công nghệ", "bg": "#ede9fe", "text": "#5b21b6", "border": "#7c3aed"},
    "github": {"label": "GitHub", "bg": "#f3e8ff", "text": "#6b21a8", "border": "#9333ea"},
    "fnb": {"label": "F&B", "bg": "#ffedd5", "text": "#9a3412", "border": "#ea580c"},
    "legal": {"label": "Pháp lý", "bg": "#fee2e2", "text": "#991b1b", "border": "#dc2626"},
    "affiliate": {"label": "Affiliate", "bg": "#d1fae5", "text": "#065f46", "border": "#059669"},
    "economic": {"label": "Phân tích", "bg": "#e0e7ff", "text": "#3730a3", "border": "#6366f1"},
    "market": {"label": "Thị trường", "bg": "#cffafe", "text": "#155e75", "border": "#0891b2"},
}

SITE_NAME = os.environ.get("SITE_NAME", "Phương's Daily")
SITE_SUBTITLE = os.environ.get("SITE_SUBTITLE", "Báo cáo Kinh tế & Công nghệ")
