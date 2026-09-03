#!/usr/bin/env python3
"""Insert favicon link tags into index.html bundle template."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
FAVICON = (ROOT / "src" / "favicon-links.html").read_text(encoding="utf-8").strip()
FAVICON_SHELL = """  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">"""


def to_embedded_json(html: str) -> str:
    dumped = json.dumps(html, ensure_ascii=False)
    return re.sub(r"</(script)\b", r"<\\u002Fscript", dumped, flags=re.IGNORECASE)


def insert_after_meta(html: str, block: str, name: str) -> str:
    if "/favicon.ico" in html:
        return html
    match = re.search(rf'<meta\s+name="{name}"[^>]*>', html, re.I)
    if not match:
        raise SystemExit(f'{name} meta not found')
    end = match.end()
    return html[:end] + "\n" + block + html[end:]


def main() -> None:
    content = INDEX.read_text(encoding="utf-8")
    marker = '<script type="__bundler/template">'
    marker_pos = content.find(marker)
    if marker_pos < 0:
        raise SystemExit("template script not found")

    shell = insert_after_meta(content[:marker_pos], FAVICON_SHELL, "theme-color")

    bundle = content[marker_pos:]
    line_start = bundle.find("\n") + 1
    line_end = bundle.find("\n", line_start)
    template = json.loads(bundle[line_start:line_end])
    template = insert_after_meta(template, FAVICON, "viewport")
    new_json = to_embedded_json(template)
    json.loads(new_json)

    bundle = bundle[:line_start] + new_json + bundle[line_end:]
    INDEX.write_text(shell + bundle, encoding="utf-8")
    print("Updated index.html (shell + bundle template)")


if __name__ == "__main__":
    main()
