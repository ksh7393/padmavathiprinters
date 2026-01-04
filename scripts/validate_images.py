"""Validate image files under assets/images.

Checks:
- file exists and is readable
- file size (warn if < 200 bytes)
- file signature (magic bytes) for JPEG/PNG/WEBP

Usage:
  python scripts/validate_images.py
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / 'assets' / 'images'

MAGICS = {
    'jpeg': [b'\xff\xd8\xff'],
    'png': [b'\x89PNG\r\n\x1a\n'],
    'webp': [b'RIFF'],
}

def check_file(p: Path):
    try:
        size = p.stat().st_size
    except Exception as e:
        return ('error', str(e))

    if size == 0:
        return ('empty', size)
    if size < 200:
        # likely a placeholder or corrupted tiny file
        return ('tiny', size)

    # read first bytes
    try:
        with p.open('rb') as f:
            head = f.read(16)
    except Exception as e:
        return ('error', str(e))

    # check known magics
    for fmt, sigs in MAGICS.items():
        for sig in sigs:
            if head.startswith(sig):
                # extra check for webp: 'RIFF' then 'WEBP' at offset 8
                if fmt == 'webp':
                    if head[:4] == b'RIFF':
                        # try reading more
                        with p.open('rb') as f:
                            data = f.read(16)
                            if b'WEBP' in data:
                                return ('ok', fmt)
                            else:
                                return ('unknown', head.hex())
                return ('ok', fmt)

    return ('unknown', head.hex())

def main():
    if not IMAGES.exists():
        print('No images folder found at', IMAGES)
        return

    total = 0
    problems = []
    print('Scanning images under', IMAGES)
    for p in sorted(IMAGES.rglob('*')):
        if p.is_file():
            total += 1
            status, info = check_file(p)
            if status != 'ok':
                problems.append((p.relative_to(ROOT), status, info))
                print(f'  {p.relative_to(ROOT)} -> {status} ({info})')
    print('\nSummary:')
    print('  total files scanned:', total)
    print('  problems found:', len(problems))
    if problems:
        print('Problems:')
        for p, status, info in problems:
            print(f' - {p}: {status} ({info})')

if __name__ == '__main__':
    main()
