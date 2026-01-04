"""Import images from a folder or zip into the site's assets.

Usage examples:
  # Import images from an 'incoming' folder in workspace root
  python scripts/import_images.py incoming

  # Import from a zip file and regenerate manifest
  python scripts/import_images.py uploads/images.zip --generate

Rules:
- If incoming contains a file named 'banner.*' it will be copied to assets/images/banner/banner.<ext>
- If incoming contains subfolders (e.g., card1, card2), those folders will be copied into assets/images/cards/<subfolder>
- If incoming contains files named like card1_1.jpg or card1-1.png they will be mapped to assets/images/cards/card1/<filename>
- After copying, you can use --generate to run scripts/generate_cards_json.py to update data/cards.json
- Use --optimize to run scripts/optimize_images.py (requires Pillow and requirements.txt)
"""
import argparse
import shutil
from pathlib import Path
import zipfile
import tempfile
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets' / 'images'
BANNER_DIR = ASSETS / 'banner'
CARDS_DIR = ASSETS / 'cards'

IMG_EXTS = {'.jpg', '.jpeg', '.png', '.webp'}

def is_image(p: Path):
    return p.suffix.lower() in IMG_EXTS

def copy_file_to(dest_dir: Path, src: Path):
    dest_dir.mkdir(parents=True, exist_ok=True)
    dst = dest_dir / src.name
    shutil.copy2(src, dst)
    return dst

def import_from_folder(folder: Path, generate=False, optimize=False):
    if not folder.exists():
        print('Source not found:', folder)
        return

    # banner file at root
    for f in folder.iterdir():
        if f.is_file() and f.name.lower().startswith('banner') and is_image(f):
            BANNER_DIR.mkdir(parents=True, exist_ok=True)
            dest = BANNER_DIR / f.name
            shutil.copy2(f, dest)
            print('Copied banner ->', dest)

    # subfolders like card1, card2
    for sub in [p for p in folder.iterdir() if p.is_dir()]:
        target = CARDS_DIR / sub.name
        for img in sorted(sub.iterdir()):
            if is_image(img):
                copy_file_to(target, img)
        print(f'Imported folder {sub.name} -> {target}')

    # files with prefix card1_1.jpg or card1-1.jpg
    for f in folder.iterdir():
        if f.is_file() and is_image(f):
            name = f.name
            parts = name.split('_', 1)
            if len(parts) == 2 and parts[0].lower().startswith('card'):
                target = CARDS_DIR / parts[0]
                copy_file_to(target, f)
                print('Imported', f, '->', target)
                continue
            parts = name.split('-', 1)
            if len(parts) == 2 and parts[0].lower().startswith('card'):
                target = CARDS_DIR / parts[0]
                copy_file_to(target, f)
                print('Imported', f, '->', target)

    if generate:
        print('Running generate_cards_json.py...')
        subprocess.run([sys.executable, str(ROOT / 'scripts' / 'generate_cards_json.py')], check=False)

    if optimize:
        print('Running optimize_images.py...')
        subprocess.run([sys.executable, str(ROOT / 'scripts' / 'optimize_images.py')], check=False)

def import_from_zip(zip_path: Path, generate=False, optimize=False):
    if not zip_path.exists():
        print('Zip not found:', zip_path)
        return
    with tempfile.TemporaryDirectory() as tmp:
        tmpd = Path(tmp)
        print('Extracting to', tmpd)
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(tmpd)
        import_from_folder(tmpd, generate=generate, optimize=optimize)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help='Folder or zip file containing images')
    parser.add_argument('--generate', action='store_true', help='Run scripts/generate_cards_json.py after import')
    parser.add_argument('--optimize', action='store_true', help='Run scripts/optimize_images.py after import (requires Pillow)')
    args = parser.parse_args()

    src = Path(args.source)
    if src.is_file() and zipfile.is_zipfile(src):
        import_from_zip(src, generate=args.generate, optimize=args.optimize)
    elif src.is_dir():
        import_from_folder(src, generate=args.generate, optimize=args.optimize)
    else:
        print('Source must be a folder or a zip file')

if __name__ == '__main__':
    main()
