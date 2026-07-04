#!/usr/bin/env python3
"""
Publication Layout Engine — load, validate, apply layouts
Each layout is a folder with layout.json defining all visual tokens
"""
import json, os, glob

LAYOUTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "publication-layouts")
REGISTRY = {}

def discover_layouts():
    """Scan publication-layouts/ for all available layouts"""
    layouts = {}
    for d in sorted(glob.glob(os.path.join(LAYOUTS_DIR, "*"))):
        if not os.path.isdir(d):
            continue
        meta_path = os.path.join(d, "layout.json")
        if os.path.exists(meta_path):
            with open(meta_path) as f:
                meta = json.load(f)
            meta["id"] = os.path.basename(d)
            meta["path"] = d
            layouts[meta["id"]] = meta
    return layouts

def get_layout(layout_id):
    """Get a single layout by ID"""
    layouts = discover_layouts()
    return layouts.get(layout_id)

def get_design_tokens(layout_id):
    """Load design tokens for a layout"""
    layout = get_layout(layout_id)
    if not layout:
        return None
    tokens_path = os.path.join(layout["path"], "design-tokens.json")
    if os.path.exists(tokens_path):
        with open(tokens_path) as f:
            return json.load(f)
    return None

def generate_css(layout_id):
    """Generate CSS variables from design tokens"""
    tokens = get_design_tokens(layout_id)
    if not tokens:
        return ""
    
    lines = [f"/* {layout_id} — auto-generated from design-tokens.json */"]
    lines.append(f"[data-layout=\"{layout_id}\"] {{")
    
    for key, val in tokens.get("css-variables", {}).items():
        lines.append(f"  {key}: {val};")
    
    lines.append("}")
    return "\n".join(lines)

def list_layouts():
    """Return list of layout metadata for the UI"""
    return list(discover_layouts().values())

if __name__ == "__main__":
    layouts = discover_layouts()
    print(f"📐 Publication Layout Engine")
    print(f"   Found {len(layouts)} layouts:")
    for lid, meta in sorted(layouts.items()):
        print(f"   • {lid}: {meta.get('name', 'Unknown')}")
