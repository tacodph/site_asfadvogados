import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def check_html(html: str) -> list[str]:
    issues = []
    if "<\\/script>" in html[:8000]:
        issues.append("BROKEN: <\\/script> in head")
    ld = html.find("application/ld+json")
    if ld >= 0:
        lc = html.find("</script>", ld)
        bm = html.find("document.addEventListener('DOMContentLoaded'")
        if bm > 0 and lc > 0 and bm < lc:
            issues.append("BROKEN: bundler script before ld+json closes")
    m = re.search(
        r'<script type="__bundler/template">\s*\n(.*?)\n\s*</script>',
        html,
        re.S,
    )
    if not m:
        issues.append("no template script")
    else:
        try:
            json.loads(m.group(1))
            issues.append("template JSON OK")
        except json.JSONDecodeError as e:
            issues.append(f"template JSON FAIL: {e}")
    return issues


def main() -> None:
    labels = [
        ("working tree", ROOT / "index.html"),
        ("HEAD", None),
        ("origin/main", "origin/main"),
    ]
    for label, ref in labels:
        if ref is None and label == "HEAD":
            html = subprocess.check_output(
                ["git", "show", "HEAD:index.html"],
                cwd=ROOT,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
        elif isinstance(ref, str):
            html = subprocess.check_output(
                ["git", "show", f"{ref}:index.html"],
                cwd=ROOT,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
        else:
            html = ref.read_text(encoding="utf-8")
        print(label, check_html(html))


if __name__ == "__main__":
    main()
