import json
import re
from pathlib import Path

# Full simulation of bundler template parse
content = Path("index.html").read_text(encoding="utf-8")
m = re.search(r'<script type="__bundler/template">\s*\n(.*?)\n\s*</script>', content, re.S)
template = json.loads(m.group(1))

checks = {
    "has body": "<body>" in template,
    "has x-dc": "<x-dc>" in template,
    "has hero": 'id="hero"' in template,
    "has DCLogic": "DCLogic" in template,
    "script closes": template.count("</script>") >= 3,
    "no broken close": "<\\u002Fscript>" not in template and "<\\/script>" not in template,
}
for k, v in checks.items():
    print(f"{k}: {v}")
print("ALL OK:", all(checks.values()))
