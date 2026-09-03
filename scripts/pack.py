#!/usr/bin/env python3
"""Rebuild index.html bundle from src/ source files."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
SRC = ROOT / "src"
TEMPLATE_IN = SRC / "index.template.html"
COMPONENT_IN = SRC / "index.component.js"
SEO_IN = SRC / "seo-meta.html"
COMPONENT_MARKER = "<!-- @component -->"
SEO_MARKER = "<!-- @seo -->"


def inject_seo(html: str, seo: str) -> str:
    if SEO_MARKER not in html:
        raise SystemExit(f"Marker {SEO_MARKER!r} not found")
    return html.replace(SEO_MARKER, seo.strip() + "\n", 1)


def main() -> None:
    if not TEMPLATE_IN.exists() or not COMPONENT_IN.exists():
        raise SystemExit("Missing src files. Run: python scripts/unpack.py")
    if not SEO_IN.exists():
        raise SystemExit(f"Missing {SEO_IN.name}")

    seo = SEO_IN.read_text(encoding="utf-8")
    markup = inject_seo(TEMPLATE_IN.read_text(encoding="utf-8"), seo)
    component = COMPONENT_IN.read_text(encoding="utf-8").strip()

    if COMPONENT_MARKER in markup:
        template = markup.replace(COMPONENT_MARKER, component, 1)
    else:
        raise SystemExit(f"Marker {COMPONENT_MARKER!r} not found in {TEMPLATE_IN.name}")

    template_json = json.dumps(template, ensure_ascii=False)
    json.loads(template_json)

    content = inject_seo(INDEX.read_text(encoding="utf-8"), seo)
    lines = content.splitlines(keepends=True)
    out_lines = []
    replaced = False
    for line in lines:
        if line.startswith('"') and "doctype html" in line[:20].lower():
            out_lines.append(template_json + "\n")
            replaced = True
        else:
            out_lines.append(line)

    if not replaced:
        raise SystemExit("Template line not found in index.html")

    INDEX.write_text("".join(out_lines), encoding="utf-8")
    print(f"Rebuilt {INDEX.relative_to(ROOT)} (SEO + template)")


if __name__ == "__main__":
    main()
