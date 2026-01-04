"""Generate favicon.ico from assets/images/logo.svg

Requires: cairosvg, Pillow
Usage:
  pip install cairosvg Pillow
  python scripts/generate_favicon.py
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SVG = ROOT / 'assets' / 'images' / 'logo.svg'
TMP_PNG = ROOT / 'assets' / 'images' / 'logo_favicon.png'
OUT_ICO = ROOT / 'favicon.ico'

def main():
    if not SVG.exists():
        print('logo.svg not found at', SVG)
        return 1
    # Import libraries; allow exceptions to surface for debugging
    try:
        import cairosvg
    except Exception as e:
        print('Failed to import cairosvg (will fallback to Pillow-only generation):', repr(e))
        cairosvg = None
    try:
        from PIL import Image
    except Exception as e:
        print('Failed to import Pillow (PIL):', repr(e))
        print('Install with: pip install Pillow')
        return 1

    if cairosvg is not None:
        # Render SVG to temporary PNG at large size
        cairosvg.svg2png(url=str(SVG), write_to=str(TMP_PNG), output_width=512, output_height=512)
    else:
        # Fallback: draw a simple logo (rounded blue square with white 'P') using Pillow
        print('Generating favicon with Pillow fallback...')
        size = 512
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = Image.Draw.Draw(img) if hasattr(Image, 'Draw') else None
        try:
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(img)
        except Exception:
            draw = None

        # Draw rounded rectangle background
        bg = (13, 110, 253, 255)  # --primary blue
        if draw:
            try:
                draw.rounded_rectangle([(0,0),(size,size)], radius=64, fill=bg)
            except Exception:
                # older Pillow fallback
                draw.rectangle([(0,0),(size,size)], fill=bg)

        # Draw centered 'P'
        try:
            # Try common Windows font first
            font = ImageFont.truetype('arial.ttf', 300)
        except Exception:
            try:
                font = ImageFont.truetype('DejaVuSans-Bold.ttf', 300)
            except Exception:
                font = ImageFont.load_default()

        if draw:
            try:
                bbox = draw.textbbox((0,0), 'P', font=font)
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
            except Exception:
                try:
                    w, h = font.getsize('P')
                except Exception:
                    w, h = (200, 200)
            draw.text(((size-w)/2, (size-h)/2 - 10), 'P', font=font, fill=(255,255,255,255))
    sizes = [16,32,48,64,128,256]
    # Save as multi-size ICO
    try:
        img.save(OUT_ICO, format='ICO', sizes=[(s,s) for s in sizes])
        print('Wrote', OUT_ICO)
    except Exception as e:
        print('Failed to save ICO:', e)

    try:
        if TMP_PNG.exists():
            TMP_PNG.unlink()
    except Exception:
        pass
    return 0

if __name__ == '__main__':
    sys.exit(main())
