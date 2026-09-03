import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
commit = sys.argv[1] if len(sys.argv) > 1 else "001d970"
content = subprocess.check_output(["git", "show", f"{commit}:index.html"], cwd=ROOT, text=True)

import json, re
m = re.search(r'<script type="__bundler/template">\s*\n(.*?)\n\s*</script>', content, re.S)
t = json.loads(m.group(1))
print("commit", commit)
print("template len", len(t))
print("hero", 'id="hero"' in t)
print("outer broken close", "<\\/script>" in content[:4000])
