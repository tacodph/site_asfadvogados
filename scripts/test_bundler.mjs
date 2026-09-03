// Simulate bundler: read index.html, extract template script textContent length, JSON.parse
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const root = path.dirname(fileURLToPath(new URL("../index.html", import.meta.url)));
const html = fs.readFileSync(path.join(root, "index.html"), "utf8");

// Simulate HTML parser: script tag ends at first </script> (case insensitive)
const start = html.indexOf('<script type="__bundler/template">');
if (start < 0) throw new Error("no template script");
const contentStart = html.indexOf("\n", start) + 1;
const end = html.indexOf("</script>", contentStart);
const body = html.slice(contentStart, end);
console.log("template body len", body.length);
const template = JSON.parse(body);
console.log("parsed OK, decoded len", template.length);
console.log("has hero", template.includes('id="hero"'));
console.log("script tags in decoded", (template.match(/<\/script>/gi) || []).length);

// Check outer head: bundler main script exists before body
const bundlerMain = html.indexOf("document.addEventListener('DOMContentLoaded'");
const ldJson = html.indexOf("application/ld+json");
const ldClose = html.indexOf("</script>", ldJson);
console.log("ld+json closes before bundler:", ldClose < bundlerMain && ldClose > 0);
