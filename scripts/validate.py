import json
from pathlib import Path

content = Path("index.html").read_text(encoding="utf-8")
line = next(
    l for l in content.splitlines()
    if l.startswith('"') and "doctype html" in l[:20].lower()
)
template = json.loads(line)
assert "FlavioAugusto" in template
assert "DanielleBatista" in template
print("JSON OK, template length", len(template))
