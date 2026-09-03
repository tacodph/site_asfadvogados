import { chromium } from "playwright";
import { createServer } from "http";
import { readFileSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, "..");
const html = readFileSync(resolve(root, "index.html"));

const server = createServer((req, res) => {
  res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
  res.end(html);
});

await new Promise((r) => server.listen(0, "127.0.0.1", r));
const port = server.address().port;
const url = `http://127.0.0.1:${port}/`;

let browser;
try {
  browser = await chromium.launch();
  const page = await browser.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  page.on("console", (msg) => {
    if (msg.type() === "error") errors.push(msg.text());
  });
  await page.goto(url, { waitUntil: "networkidle", timeout: 60000 });
  await page.waitForTimeout(3000);
  const bodyText = await page.evaluate(() => document.body?.innerText?.slice(0, 500) || "");
  const errEl = await page.evaluate(() => document.getElementById("__bundler_err")?.textContent || "");
  const loading = await page.evaluate(() => document.getElementById("__bundler_loading")?.textContent || "");
  const hasHero = await page.evaluate(() => !!document.querySelector("h1, [class*='hero'], main"));
  console.log(JSON.stringify({ bodyText: bodyText.slice(0, 200), errEl, loading, hasHero, errors }, null, 2));
} finally {
  if (browser) await browser.close();
  server.close();
}
