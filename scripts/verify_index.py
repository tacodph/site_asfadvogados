import json
import re
from pathlib import Path

html = Path("index.html").read_text(encoding="utf-8")
m = re.search(
    r'<script type="__bundler/template">\s*\n(.*?)\n\s*</script>',
    html,
    re.S,
)
if not m:
    raise SystemExit("template script not found")

# How the browser reads the template (stops at the first </script> in the file).
marker = '<script type="__bundler/template">'
start = html.find(marker)
start = html.find("\n", start) + 1
browser_end = html.find("</script>", start)
browser_text = html[start:browser_end]

regex_text = m.group(1)
for label, text in [("browser", browser_text), ("regex", regex_text)]:
    try:
        json.loads(text)
        print(f"{label} JSON OK ({len(text)} chars)")
    except json.JSONDecodeError as e:
        raise SystemExit(f"{label} JSON FAIL: {e}")

if len(browser_text) < len(regex_text) * 0.95:
    raise SystemExit(
        f"browser template truncated: {len(browser_text)} vs {len(regex_text)} chars "
        "(</script> inside bundle JSON is not escaped as \\u002F)"
    )

t = json.loads(browser_text)
print("decoded template OK", len(t))
print("Flavio", "FlavioAugusto" in t)
print("Danielle", "DanielleBatista" in t)
ld = html.find("application/ld+json")
lc = html.find("</script>", ld)
bm = html.find("document.addEventListener('DOMContentLoaded'")
print("bundler after ld+json close", bm > lc)
print("has broken backslash script", "<\\/script>" in html[:5000])
