import { chromium } from "playwright";
import { resolve, dirname } from "path";
import { fileURLToPath, pathToFileURL } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const fileUrl = pathToFileURL(resolve(__dirname, "..", "index.html")).href;

const browser = await chromium.launch();
try {
  const page = await browser.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  page.on("console", (msg) => {
    if (msg.type() === "error") errors.push(msg.text());
  });
  await page.goto(fileUrl, { waitUntil: "networkidle", timeout: 120000 });
  await page.waitForTimeout(5000);
  const bodyText = await page.evaluate(() => document.body?.innerText?.slice(0, 300) || "");
  const errEl = await page.evaluate(() => document.getElementById("__bundler_err")?.textContent || "");
  const loading = await page.evaluate(() => document.getElementById("__bundler_loading")?.textContent || "");
  console.log(JSON.stringify({ fileUrl, bodyText: bodyText.slice(0, 150), errEl, loading, errors }, null, 2));
} finally {
  await browser.close();
}
