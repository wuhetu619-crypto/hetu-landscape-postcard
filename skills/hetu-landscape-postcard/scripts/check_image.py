#!/usr/bin/env python3
"""Read image header dimensions; no image edits or visual-quality claims."""
import argparse
import json
import math
import struct
from pathlib import Path


def dimensions(path):
    data = Path(path).read_bytes()
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        if len(data) < 33 or data[12:16] != b'IHDR':
            raise ValueError('Invalid PNG header')
        w, h = struct.unpack('>II', data[16:24])
        fmt = 'PNG'
    elif data[:2] == b'\xff\xd8':
        pos = 2
        sof = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
        while pos < len(data):
            if data[pos] != 0xFF:
                raise ValueError('Invalid JPEG marker')
            while pos < len(data) and data[pos] == 0xFF:
                pos += 1
            if pos >= len(data):
                break
            marker = data[pos]
            pos += 1
            if marker in (0xD9, 0xDA):
                break
            if marker in {0x01, 0xD8, *range(0xD0, 0xD8)}:
                continue
            if pos + 2 > len(data):
                break
            size = int.from_bytes(data[pos:pos + 2], 'big')
            if size < 2 or pos + size > len(data):
                raise ValueError('Truncated JPEG segment')
            if marker in sof:
                if size < 8:
                    raise ValueError('Invalid JPEG frame')
                h, w = struct.unpack('>HH', data[pos + 3:pos + 7])
                fmt = 'JPEG'
                break
            pos += size
        else:
            raise ValueError('Missing JPEG frame')
        if 'fmt' not in locals():
            raise ValueError('Missing JPEG frame')
    elif data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        pos = 12
        fmt = 'WEBP'
        while pos + 8 <= len(data):
            kind = data[pos:pos + 4]
            size = int.from_bytes(data[pos + 4:pos + 8], 'little')
            chunk = data[pos + 8:pos + 8 + size]
            if len(chunk) != size:
                raise ValueError('Truncated WebP chunk')
            if kind == b'VP8X' and size >= 10:
                w = 1 + int.from_bytes(chunk[4:7], 'little')
                h = 1 + int.from_bytes(chunk[7:10], 'little')
                break
            if kind == b'VP8L' and size >= 5 and chunk[0] == 0x2F:
                bits = int.from_bytes(chunk[1:5], 'little')
                w, h = 1 + (bits & 0x3FFF), 1 + ((bits >> 14) & 0x3FFF)
                break
            if kind == b'VP8 ' and size >= 10 and chunk[3:6] == b'\x9d\x01\x2a':
                w, h = struct.unpack('<HH', chunk[6:10])
                w, h = w & 0x3FFF, h & 0x3FFF
                break
            pos += 8 + size + size % 2
        else:
            raise ValueError('Missing WebP size header')
    else:
        raise ValueError('Supported formats: PNG, JPEG, WebP')
    if w <= 0 or h <= 0:
        raise ValueError('Invalid dimensions')
    return fmt, w, h


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('image', type=Path)
    p.add_argument('--aspect', help='Expected stored width:height, e.g. 3:4')
    p.add_argument('--tolerance', type=float, default=0.01, help='Relative ratio error tolerance (default 1%%)')
    args = p.parse_args()
    try:
        if not math.isfinite(args.tolerance) or args.tolerance < 0:
            raise ValueError('Tolerance must be finite and nonnegative')
        fmt, w, h = dimensions(args.image)
        result = dict(file=args.image.name, format=fmt, width=w, height=h,
                      note='Header only; EXIF orientation and full decoding not checked; visual review still required.')
        ok = True
        if args.aspect:
            a, b = map(float, args.aspect.split(':'))
            if not all(math.isfinite(n) and n > 0 for n in (a, b)):
                raise ValueError('Aspect components must be finite and positive')
            error = abs((w / h) / (a / b) - 1)
            ok = error <= args.tolerance
            result.update(expected_aspect=args.aspect, relative_error=round(error, 6), aspect_pass=ok)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if ok else 1
    except (OSError, ValueError, struct.error) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False))
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
