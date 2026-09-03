import json
import re
from pathlib import Path

for name in ["index.html", "_old_index.html"]:
    p = Path(name)
    if not p.exists():
        print(name, "missing")
        continue
    html = p.read_text(encoding="utf-8")
    m = re.search(r'<script type="__bundler/template">\s*\n(.*?)\n\s*</script>', html, re.S)
    if not m:
        print(name, "no template block")
        continue
    body = m.group(1)
    try:
        t = json.loads(body)
        print(name, "OK", "raw", len(body), "decoded", len(t), "hero", 'id="hero"' in t)
    except json.JSONDecodeError as e:
        print(name, "FAIL", e)
