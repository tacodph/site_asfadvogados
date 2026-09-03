#!/usr/bin/env python3
"""Extract readable source files from index.html bundle."""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
SRC = ROOT / "src"
TEMPLATE_OUT = SRC / "index.template.html"
COMPONENT_OUT = SRC / "index.component.js"
COMPONENT_MARKER = "<!-- @component -->"
SEO_MARKER = "<!-- @seo -->"
SEO_IN = SRC / "seo-meta.html"


def format_html(path: Path) -> None:
    try:
        subprocess.run(
            ["npx", "--yes", "prettier@3.5.3", "--parser", "html", str(path), "-w"],
            check=True,
            cwd=ROOT,
            capture_output=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"Warning: could not format {path.name}: {exc}", file=sys.stderr)


def format_js_in_component(path: Path) -> None:
    content = path.read_text(encoding="utf-8")
    match = re.match(
        r'(<script type="text/x-dc"[^>]*>)(.*?)(</script>)',
        content,
        re.DOTALL,
    )
    if not match:
        return

    open_tag, body, close_tag = match.groups()
    tmp = SRC / "_component_body.js"
    tmp.write_text(body.strip() + "\n", encoding="utf-8")
    try:
        subprocess.run(
            ["npx", "--yes", "prettier@3.5.3", str(tmp), "-w"],
            check=True,
            cwd=ROOT,
            capture_output=True,
        )
        formatted_body = tmp.read_text(encoding="utf-8").rstrip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        formatted_body = body.strip()
    finally:
        tmp.unlink(missing_ok=True)

    path.write_text(f"{open_tag}\n{formatted_body}\n{close_tag}\n", encoding="utf-8")


def main() -> None:
    content = INDEX.read_text(encoding="utf-8")
    template_line = next(
        line for line in content.splitlines()
        if line.startswith('"') and "doctype html" in line[:20].lower()
    )
    template = json.loads(template_line)

    SRC.mkdir(exist_ok=True)

    match = re.search(
        r'(<script type="text/x-dc"[^>]*>)(.*?)(</script>)',
        template,
        re.DOTALL,
    )
    if not match:
        raise SystemExit("DC component script not found in template")

    markup = template[: match.start()].rstrip() + f"\n    {SEO_MARKER}\n    {COMPONENT_MARKER}\n"
    component = match.group(0).strip() + "\n"
    markup_after = template[match.end() :].lstrip()

    if SEO_MARKER not in markup and SEO_IN.exists():
        seo = SEO_IN.read_text(encoding="utf-8").strip()
        if seo in markup:
            markup = markup.replace(seo, SEO_MARKER, 1)

    TEMPLATE_OUT.write_text(markup + markup_after, encoding="utf-8")
    COMPONENT_OUT.write_text(component, encoding="utf-8")

    format_html(TEMPLATE_OUT)
    format_js_in_component(COMPONENT_OUT)

    print(f"Wrote {TEMPLATE_OUT.relative_to(ROOT)}")
    print(f"Wrote {COMPONENT_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
