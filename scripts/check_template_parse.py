import json
import re
from pathlib import Path

content = Path("index.html").read_text(encoding="utf-8")
m = re.search(
    r'<script type="__bundler/template">\s*\n(.*?)\n\s*</script>',
    content,
    re.DOTALL,
)
if not m:
    raise SystemExit("template script tag not found")

body = m.group(1)
print("template textContent len:", len(body))
print("contains raw </script>:", bool(re.search(r"(?<!\\)</script>", body, re.I)))

try:
    parsed = json.loads(body)
    print("JSON OK, decoded len:", len(parsed))
    print("decoded has escaped closers:", "<\\/script>" in parsed or r"<\/script>" in parsed)
except json.JSONDecodeError as e:
    print("JSON ERROR:", e)
    print("context:", repr(body[max(0, e.pos - 80) : e.pos + 80]))
