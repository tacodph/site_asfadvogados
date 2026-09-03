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
SEO_SHELL_IN = SRC / "seo-shell.html"
COMPONENT_MARKER = "<!-- @component -->"
SEO_MARKER = "<!-- @seo -->"
SEO_SHELL_MARKER = "<!-- @seo-shell -->"


def to_embedded_json(html: str) -> str:
    """JSON for __bundler/template: hide </script> from the HTML parser."""
    dumped = json.dumps(html, ensure_ascii=False)
    return re.sub(r"</(script)\b", r"<\\u002Fscript", dumped, flags=re.IGNORECASE)


def inject_block(html: str, marker: str, block: str) -> str:
    if marker in html:
        return html.replace(marker, block.strip() + "\n", 1)
    return html


def main() -> None:
    if not TEMPLATE_IN.exists() or not COMPONENT_IN.exists():
        raise SystemExit("Missing src files. Run: python scripts/unpack.py")
    if not SEO_IN.exists():
        raise SystemExit(f"Missing {SEO_IN.name}")

    seo = SEO_IN.read_text(encoding="utf-8")
    seo_shell = SEO_SHELL_IN.read_text(encoding="utf-8") if SEO_SHELL_IN.exists() else seo

    markup = inject_block(TEMPLATE_IN.read_text(encoding="utf-8"), SEO_MARKER, seo)
    component = COMPONENT_IN.read_text(encoding="utf-8").strip()

    if COMPONENT_MARKER not in markup:
        raise SystemExit(f"Marker {COMPONENT_MARKER!r} not found in {TEMPLATE_IN.name}")

    template = markup.replace(COMPONENT_MARKER, component, 1)
    template_json = to_embedded_json(template)
    json.loads(template_json)

    content = INDEX.read_text(encoding="utf-8")
    content = inject_block(content, SEO_SHELL_MARKER, seo_shell)

    lines = content.splitlines(keepends=True)
    out_lines = []
    replaced = False
    for line in lines:
        if line.startswith('"') and "doctype html" in line[:30].lower():
            out_lines.append(template_json + "\n")
            replaced = True
        else:
            out_lines.append(line)

    if not replaced:
        raise SystemExit("Template line not found in index.html")

    INDEX.write_text("".join(out_lines), encoding="utf-8")
    print(f"Rebuilt {INDEX.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
