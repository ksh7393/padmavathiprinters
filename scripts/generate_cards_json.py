"""Generate data/cards.json by scanning assets/images/cards.

Usage:
  python scripts/generate_cards_json.py

This script will create or overwrite data/cards.json listing each subfolder and its images (sorted).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS_DIR = ROOT / 'assets' / 'images' / 'cards'
OUT_FILE = ROOT / 'data' / 'cards.json'

def main():
    items = []
    if not CARDS_DIR.exists():
        print(f'Cards folder not found: {CARDS_DIR}')
        return

    for folder in sorted([p for p in CARDS_DIR.iterdir() if p.is_dir()]):
        images = sorted([f.name for f in folder.iterdir() if f.suffix.lower() in ['.jpg','.jpeg','.png','.webp']])
        if not images:
            print(f'Skipping {folder.name} (no images)')
            continue
        items.append({
            'folder': folder.name,
            'title': folder.name.replace('-', ' ').title(),
            'description': '',
            'images': images,
        })

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUT_FILE.open('w', encoding='utf-8') as f:
        json.dump(items, f, indent=2)
    print(f'Wrote {OUT_FILE} with {len(items)} items')

if __name__ == '__main__':
    main()
