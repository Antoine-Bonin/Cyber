#!/usr/bin/env python3
import sys
import os
from datetime import datetime
from PIL import Image, ExifTags

VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')


def parse_image(filepath):
    print(f"\n{'=' * 50}")
    print(f"File : {filepath}")
    print(f"{'=' * 50}")

    if not os.path.exists(filepath):
        print(f"Error : the file '{filepath}' doesn't exist.", file=sys.stderr)
        return

    if not filepath.lower().endswith(VALID_EXTENSIONS):
        print(f"Error : Format unsupported'{filepath}'.", file=sys.stderr)
        return

    stat = os.stat(filepath)
    creation_date = datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
    mod_date = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")

    print("\n--- Base attribute ---")
    print(f"Size                : {stat.st_size} octets")
    print(f"Creation date       : {creation_date}")
    print(f"Last modification   : {mod_date}")

    try:
        with Image.open(filepath) as img:
            print(f"Format            : {img.format}")
            print(f"Dimensions        : {img.size[0]} x {img.size[1]} px")
            print(f"Mode              : {img.mode}")

            print("\n--- EXIF Datas ---")
            exif_data = img._getexif()

            if not exif_data:
                print("No EXIF data found")
                return

            for tag_id, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                if isinstance(value, bytes):
                    value = value.decode(errors="ignore").strip()
                print(f"{tag_name:<25} : {value}")

    except Exception as e:
        print(f"Error while reading the file : {e}", file=sys.stderr)


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} FILE1 [FILE2 ...]", file=sys.stderr)
        sys.exit(1)

    for file_path in sys.argv[1:]:
        parse_image(file_path)


if __name__ == "__main__":
    main()
