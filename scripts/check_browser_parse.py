import json
import re
import urllib.request
from pathlib import Path

def browser_template_text(html: str) -> str | None:
    """What the browser reads from script[type=__bundler/template] textContent."""
    marker = '<script type="__bundler/template">'
    start = html.find(marker)
    if start < 0:
        return None
    start = html.find("\n", start) + 1
    end = html.find("</script>", start)
    return html[start:end]


def regex_template_text(html: str) -> str | None:
    m = re.search(
        r'<script type="__bundler/template">\s*\n(.*?)\n\s*</script>',
        html,
        re.S,
    )
    return m.group(1) if m else None


import subprocess

sources = [("local", Path("index.html").read_text(encoding="utf-8"))]
for ref in ("HEAD", "origin/main"):
    sources.append(
        (
            ref,
            subprocess.check_output(
                ["git", "show", f"{ref}:index.html"],
                text=True,
                encoding="utf-8",
                errors="replace",
            ),
        )
    )
try:
    live_html = urllib.request.urlopen(
        "https://asfadvogados.com/index.html", timeout=30
    ).read().decode("utf-8", errors="replace")
    sources.append(("live", live_html))
except Exception as e:
    print("live fetch skipped:", e)

for label, source in sources:
    browser = browser_template_text(source)
    regex = regex_template_text(source)
    print(f"\n=== {label} ===")
    print("browser len", len(browser or ""))
    print("regex len", len(regex or ""))
    for name, text in [("browser", browser), ("regex", regex)]:
        if not text:
            print(name, "missing")
            continue
        try:
            json.loads(text)
            print(name, "JSON OK")
        except json.JSONDecodeError as e:
            print(name, "JSON FAIL", e)
            print("context", repr(text[max(0, e.pos - 60) : e.pos + 60]))
    if browser:
        print("browser has literal </script>", "</script>" in browser)
        print("browser has \\u002F", "\\u002Fscript" in browser)
