import json
import re
from pathlib import Path

c = Path("index.html").read_text(encoding="utf-8")
m = re.search(r'<script type="__bundler/template">\s*\n(.*?)\n\s*</script>', c, re.S)
raw = m.group(1)
i = raw.find("099734f8")
print("RAW FILE:", repr(raw[i : i + 70]))
t = json.loads(raw)
i2 = t.find("099734f8")
snippet = t[i2 : i2 + 70]
print("AFTER PARSE:", repr(snippet))
print("ends with </script>:", snippet.endswith("</script>"))

# simulate DOM: count script tags if we had proper closers
closes = t.count("</script>")
ucloses = t.count("<\\u002Fscript>")
print("count </script>:", closes, "count literal \\u002F:", ucloses)
