"""Optional: Optimize images in assets/images/cards by resizing and saving optimized JPEGs.

Usage:
  pip install -r requirements.txt
  python scripts/optimize_images.py --max-size 1600

This will overwrite images in-place after confirmation.
"""
import argparse
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CARDS_DIR = ROOT / 'assets' / 'images' / 'cards'

def optimize(max_size=1600, quality=85):
    for p in CARDS_DIR.rglob('*'):
        if p.suffix.lower() not in ('.jpg','.jpeg','.png'):
            continue
        try:
            img = Image.open(p)
            img.thumbnail((max_size, max_size))
            if img.mode in ('RGBA','LA'):
                img = img.convert('RGB')
            img.save(p, optimize=True, quality=quality)
            print('Optimized', p)
        except Exception as e:
            print('Failed', p, e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-size', type=int, default=1600)
    parser.add_argument('--quality', type=int, default=85)
    args = parser.parse_args()
    optimize(args.max_size, args.quality)
