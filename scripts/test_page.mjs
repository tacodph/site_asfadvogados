import { chromium } from "playwright-core";
import path from "path";
import { fileURLToPath } from "url";
import { createServer } from "http";
import { readFileSync } from "fs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");

const server = createServer((req, res) => {
  const url = req.url === "/" ? "/index.html" : req.url;
  const file = path.join(root, decodeURIComponent(url.split("?")[0]));
  try {
    const data = readFileSync(file);
    const ext = path.extname(file);
    const types = { ".html": "text/html", ".js": "text/javascript", ".png": "image/png", ".jpeg": "image/jpeg", ".jpg": "image/jpeg" };
    res.writeHead(200, { "Content-Type": types[ext] || "application/octet-stream" });
    res.end(data);
  } catch {
    res.writeHead(404);
    res.end("not found");
  }
});

await new Promise((r) => server.listen(0, r));
const port = server.address().port;
const browser = await chromium.launch();
const page = await browser.newPage();
const errors = [];
page.on("pageerror", (e) => errors.push(String(e)));

await page.goto(`http://127.0.0.1:${port}/`, { waitUntil: "networkidle", timeout: 120000 });
const hero = await page.locator("#hero").count();
const text = await page.locator("body").innerText();
console.log("hero:", hero);
console.log("has ASF:", text.includes("ASF"));
console.log("errors:", errors);
await browser.close();
server.close();
process.exit(hero > 0 ? 0 : 1);
