#!/usr/bin/env python3
"""
Layout Registry — registers publication layouts with Flask app
Auto-discovers layouts from publication-layouts/ directory
"""
import json, os, glob
from flask import Blueprint, jsonify

layouts_dir = os.path.join(os.path.dirname(__file__), "..", "..", "publication-layouts")
layout_bp = Blueprint("layouts", __name__)

def discover():
    """Discover all installed layouts"""
    layouts = {}
    for d in sorted(glob.glob(os.path.join(layouts_dir, "*"))):
        if not os.path.isdir(d):
            continue
        meta_path = os.path.join(d, "layout.json")
        if os.path.exists(meta_path):
            with open(meta_path) as f:
                meta = json.load(f)
            meta["id"] = os.path.basename(d)
            meta["path"] = d
            # Check for preview
            preview = os.path.join(d, "preview.png")
            meta["preview"] = f"/static/layouts/{meta['id']}/preview.png" if os.path.exists(preview) else None
            layouts[meta["id"]] = meta
    return layouts

@layout_bp.route("/api/layouts")
def list_layouts():
    """API endpoint for the Publication Hub"""
    return jsonify(list(discover().values()))

@layout_bp.route("/api/layouts/<layout_id>")
def get_layout(layout_id):
    layouts = discover()
    l = layouts.get(layout_id)
    if not l:
        return jsonify({"error": "not found"}), 404
    return jsonify(l)

def get_layout_css(layout_id):
    """Generate CSS for a given layout from its design-tokens.json"""
    layouts = discover()
    l = layouts.get(layout_id)
    if not l:
        return ""
    tokens_path = os.path.join(l["path"], "design-tokens.json")
    if not os.path.exists(tokens_path):
        return ""
    with open(tokens_path) as f:
        tokens = json.load(f)
    
    lines = [f"[data-layout=\"{layout_id}\"] {{"]
    for key, val in tokens.get("css-variables", {}).items():
        lines.append(f"  {key}: {val};")
    lines.append("}")
    return "\n".join(lines)

def generate_all_layouts_css():
    """Generate combined CSS for all installed layouts"""
    parts = []
    layouts = discover()
    for lid in layouts:
        css = get_layout_css(lid)
        if css:
            parts.append(css)
    return "\n\n".join(parts)
