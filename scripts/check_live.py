import json
import re
import urllib.request

url = "https://asfadvogados.com/index.html"
html = urllib.request.urlopen(url, timeout=30).read().decode("utf-8", errors="replace")
print("live size", len(html))
ld = html.find("application/ld+json")
if ld >= 0:
    lc = html.find("</script>", ld)
    bm = html.find("document.addEventListener('DOMContentLoaded'")
    print("bundler after ld+json", bm > lc, "bm", bm, "lc", lc)
print("has backslash script in head", "<\\/script>" in html[:8000])
m = re.search(
    r'<script type="__bundler/template">\s*\n(.*?)\n\s*</script>',
    html,
    re.S,
)
if m:
    line = m.group(1)
    print("template line len", len(line))
    try:
        json.loads(line)
        print("template JSON OK")
    except json.JSONDecodeError as e:
        print("template JSON FAIL", e)
        print("context", repr(line[max(0, e.pos - 80) : e.pos + 80]))
else:
    print("no template match")
    # maybe script tag was closed early
    idx = html.find('<script type="__bundler/template">')
    print("template tag at", idx)
    if idx >= 0:
        print("snippet after tag", repr(html[idx : idx + 200]))
