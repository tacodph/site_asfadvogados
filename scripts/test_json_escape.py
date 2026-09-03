import json

# What JS JSON.parse does with \u002F in JSON text
cases = [
    '"<\\u002Fscript>"',
    '"</script>"',
    r'"<\u002Fscript>"',
]
for c in cases:
    try:
        v = json.loads(c)
        print(c, "->", repr(v))
    except Exception as e:
        print(c, "ERR", e)

# Correct approach: put unicode escape in JSON output
html = "<script src=x></script>"
# Replace close with chars that json.dumps will encode as \u002F? 
# Actually replace / in closing only:
escaped = html.replace("</script>", "<" + "\u002F" + "script>")  # same as </script>
print("same?", escaped == html)

# Manual JSON string building for the close tag part:
out = json.dumps(html).replace("</script>", "<\\u002Fscript>")
print("dump replace out:", out)
print("parsed:", json.loads(out))
