#!/usr/bin/env python3
import argparse
import sys
import os
from urllib.parse import urljoin, urlparse
from html.parser import HTMLParser
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; Spider/1.0; +https://42.fr)'}

visited_pages = set()
downloaded_images = set()


class SpiderHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        attr_dict = {k.lower(): v for k, v in attrs if v is not None}
        if tag == "img" and "src" in attr_dict:
            self.images.append(attr_dict["src"])
        elif tag == "a" and "href" in attr_dict:
            self.links.append(attr_dict["href"])


def get_unique_filepath(dest_folder: str, filename: str) -> str:
    filepath = os.path.join(dest_folder, filename)
    if not os.path.exists(filepath):
        return filepath

    base, ext = os.path.splitext(filename)
    counter = 1
    while True:
        candidate = os.path.join(dest_folder, f"{base}_{counter}{ext}")
        if not os.path.exists(candidate):
            return candidate
        counter += 1


def download_image(img_url: str, dest_folder: str):
    if img_url in downloaded_images:
        return
    downloaded_images.add(img_url)

    try:
        parsed_path = urlparse(img_url).path
        filename = os.path.basename(parsed_path)
        if not filename:
            return

        filepath = get_unique_filepath(dest_folder, filename)

        try:
            resp = requests.get(img_url, headers=HEADERS, timeout=10, stream=True)
        except requests.exceptions.SSLError:
            resp = requests.get(img_url, headers=HEADERS, timeout=10, stream=True, verify=False)

        if resp.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"[+] Image saved : {os.path.basename(filepath)}")
        else:
            print(f"[-] Error {resp.status_code} sur {img_url}", file=sys.stderr)
    except requests.RequestException as e:
        print(f"[!] Fail on {img_url} : {e}", file=sys.stderr)


def crawl(current_url: str, base_domain: str, dest_folder: str, current_depth: int, max_depth: int, recursive: bool):
    if current_url in visited_pages or current_depth > max_depth:
        return
    visited_pages.add(current_url)

    print(f"[*] Scraping [Depth: {current_depth}/{max_depth}] : {current_url}")

    try:
        try:
            response = requests.get(current_url, headers=HEADERS, timeout=10)
        except requests.exceptions.SSLError:
            response = requests.get(current_url, headers=HEADERS, timeout=10, verify=False)

        content_type = response.headers.get('content-type', '').lower()
        if response.status_code != 200 or 'text/html' not in content_type:
            return
    except requests.RequestException:
        return

    parser = SpiderHTMLParser()
    try:
        parser.feed(response.text)
    except Exception:
        pass

    for img_src in parser.images:
        full_img_url = urljoin(current_url, img_src)
        parsed_img = urlparse(full_img_url).path
        if parsed_img.lower().endswith(VALID_EXTENSIONS):
            download_image(full_img_url, dest_folder)

    if recursive and current_depth < max_depth:
        for link in parser.links:
            next_url = urljoin(current_url, link).split('#')[0]
            parsed_next = urlparse(next_url)

            if parsed_next.scheme in ('http', 'https') and parsed_next.netloc == base_domain:
                crawl(next_url, base_domain, dest_folder, current_depth + 1, max_depth, recursive)


def main():
    parser = argparse.ArgumentParser(
        description="Spider - Recusrive image hoover",
        usage="./spider [-rlp] URL"
    )
    parser.add_argument("url", type=str, help="Target url")
    parser.add_argument("-r", "--recursively", action="store_true", help="Activate recursive download")
    parser.add_argument("-l", "--recursive_depth", type=int, default=5, help="Max depth (default 5)")
    parser.add_argument("-p", "--download_path", type=str, default="./data/", help="Donwload directory (defaut: ./data/)")

    args = parser.parse_args()

    if args.recursive_depth < 0:
        print("Error : depth must be positive", file=sys.stderr)
        sys.exit(1)

    parsed_target = urlparse(args.url)
    if not parsed_target.scheme:
        args.url = "http://" + args.url
        parsed_target = urlparse(args.url)

    base_domain = parsed_target.netloc
    if not base_domain:
        print("Error : URL invalid", file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.download_path, exist_ok=True)
    max_depth = args.recursive_depth if args.recursively else 0

    print("=== Spider launched ===")
    print(f"Target          : {args.url}")
    print(f"Recursive mode  : {'Oui' if args.recursively else 'Non'}")
    if args.recursively:
        print(f"Max depth : {max_depth}")
    print(f"Destination    : {args.download_path}")
    print("=" * 22)

    crawl(
        current_url=args.url,
        base_domain=base_domain,
        dest_folder=args.download_path,
        current_depth=0,
        max_depth=max_depth,
        recursive=args.recursively
    )

    print(f"=== end of treatment. {len(downloaded_images)} image(s) found(s) ===")


if __name__ == "__main__":
    main()