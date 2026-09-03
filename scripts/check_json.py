import json
from pathlib import Path

content = Path("index.html").read_text(encoding="utf-8")
for i, line in enumerate(content.splitlines(), 1):
    if line.startswith('"') and "doctype html" in line[:30].lower():
        print("template line", i, "len", len(line))
        try:
            json.loads(line)
            print("JSON OK")
        except json.JSONDecodeError as e:
            print("JSON error:", e)
            pos = e.pos
            print("context:", repr(line[max(0, pos - 100) : pos + 100]))
        break
