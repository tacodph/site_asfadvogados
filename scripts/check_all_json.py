import json
from pathlib import Path

content = Path("index.html").read_text(encoding="utf-8")
import re

for m in re.finditer(r'<script type="__bundler/([^"]+)">\s*\n?(.*?)\s*</script>', content, re.DOTALL):
    kind = m.group(1)
    body = m.group(2).strip()
    print(f"\n=== {kind} === len={len(body)} lines={body.count(chr(10))+1}")
    if len(body) < 5000:
        try:
            json.loads(body)
            print("JSON OK")
        except json.JSONDecodeError as e:
            print("JSON ERROR:", e)
            print("context:", repr(body[max(0, e.pos-80):e.pos+80]))
    else:
        # first line only for huge template
        first = body.split('\n')[0]
        print("first line len", len(first))
        try:
            json.loads(first if kind == 'template' else body)
            print("JSON OK")
        except json.JSONDecodeError as e:
            print("JSON ERROR:", e)
            print("context:", repr(body[max(0, e.pos-80):e.pos+80]))
