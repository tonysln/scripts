#!/usr/bin/env python3
import logging
import os
import struct
import sys
from datetime import datetime
import exifread

logging.getLogger('exifread').setLevel(logging.ERROR)

def video_date(path):
    with open(path, 'rb') as f:
        while header := f.read(8):
            size, kind = struct.unpack('>I4s', header)
            if size == 1:  # 64-bit box size follows the header
                size = struct.unpack('>Q', f.read(8))[0] - 8
            if kind == b'mvhd':
                version = f.read(4)[0]
                secs = struct.unpack('>Q' if version else '>I', f.read(8 if version else 4))[0]
                return datetime.fromtimestamp(secs - 2082844800) if secs else None
            if kind != b'moov':  # step into moov, skip everything else
                if size < 8:  # size 0: box runs to end of file
                    return None
                f.seek(size - 8, 1)

def embedded_date(path):
    try:
        if path.lower().endswith(('.mov', '.mp4')):
            return video_date(path)
        with open(path, 'rb') as f:
            tags = exifread.process_file(f, details=False)
        for key in ('EXIF DateTimeOriginal', 'EXIF DateTimeDigitized', 'Image DateTime'):
            if key in tags:
                return datetime.strptime(str(tags[key])[:19], '%Y:%m:%d %H:%M:%S')
    except Exception:  # missing/malformed metadata, unsupported format
        pass

folder = sys.argv[1]
for name in sorted(os.listdir(folder)):
    try:
        ext = os.path.splitext(name)[1].lower().replace('jpeg', 'jpg')
        if ext not in ('.jpg', '.png', '.jxl', '.heic', '.heif', '.mov', '.mp4'):
            continue
        path = os.path.join(folder, name)
        date = embedded_date(path) or datetime.fromtimestamp(os.path.getmtime(path))
        base = date.strftime('%Y-%m-%d_%H-%M-%S')
        new, n = base + ext, 0
        while new != name and os.path.exists(os.path.join(folder, new)):
            n += 1
            new = f'{base}_{n}{ext}'
        os.rename(path, os.path.join(folder, new))
    except OSError as e:
        print(e)
