#!/usr/bin/env python3
"""Generate layout CSS from layout.json files"""
import json, os, glob

LAYOUTS_DIR = os.path.expanduser("~/.hermes/profiles/meow/publication-layouts")
OUTPUT = os.path.expanduser("~/.hermes/profiles/meow/frontend/static/layouts.css")

def generate_css():
    """Generate CSS for all publication layouts"""
    parts = []
    
    for d in sorted(glob.glob(os.path.join(LAYOUTS_DIR, "*"))):
        if not os.path.isdir(d):
            continue
        meta_path = os.path.join(d, "layout.json")
        if not os.path.exists(meta_path):
            continue
        
        lid = os.path.basename(d)
        with open(meta_path) as f:
            meta = json.load(f)
        
        lines = [f"/* === {meta.get('name', lid)} === */"]
        lines.append(f"[data-layout=\"{lid}\"] {{")
        
        # Colors → CSS variables
        colors = meta.get("colors", {})
        color_map = {
            "bg": "--bg",
            "text": "--text",
            "accent": "--accent",
            "border": "--border",
            "gray": "--text-gray",
            "light": "--text-light",
        }
        for key, var in color_map.items():
            if key in colors:
                lines.append(f"  {var}: {colors[key]};")
        
        # Typography
        typo = meta.get("typography", {})
        if "heading" in typo:
            lines.append(f"  --font-heading: {typo['heading']};")
        if "body" in typo:
            lines.append(f"  --font-body: {typo['body']};")
        
        # Layout
        layout = meta.get("layout", {})
        if "max-width" in layout:
            lines.append(f"  --max-width: {layout['max-width']};")
        if "content-width" in layout:
            lines.append(f"  --content-width: {layout['content-width']};")
        if "border-radius" in layout:
            lines.append(f"  --radius: {layout['border-radius']};")
        
        # Motion
        motion = meta.get("motion", {})
        if "duration-fast" in motion:
            lines.append(f"  --duration-fast: {motion['duration-fast']};")
        if "duration-normal" in motion:
            lines.append(f"  --duration-normal: {motion['duration-normal']};")
        
        lines.append("}")
        lines.append("")
        parts.append("\n".join(lines))
    
    return "\n".join(parts)

css = generate_css()
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
with open(OUTPUT, "w") as f:
    f.write(css)

print(f"✅ Generated {OUTPUT}")
print(f"   Lines: {len(css.split(chr(10)))}")
for line in css.split('\n'):
    if line.startswith('/* =='):
        print(f"   {line.replace('/*','').replace('*/','').strip()}")
