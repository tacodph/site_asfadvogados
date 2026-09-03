import re
import urllib.request

url = "https://asfadvogados.com/"
req = urllib.request.Request(url, headers={"User-Agent": "facebookexternalhit/1.1"})
html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", errors="replace")

def meta(prop, attr="property"):
    m = re.search(rf'<meta\s+{attr}="{re.escape(prop)}"\s+content="([^"]*)"', html, re.I)
    return m.group(1) if m else None

title = re.search(r"<title>([^<]*)</title>", html, re.I)
print("title:", title.group(1) if title else "MISSING")
print("og:title:", meta("og:title"))
print("og:description:", meta("og:description"))
print("og:image:", meta("og:image"))
print("description:", meta("description", "name"))
print("has Bundled Page:", "Bundled Page" in html[:5000])
