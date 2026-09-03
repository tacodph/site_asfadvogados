import { chromium } from "playwright";

const url = process.argv[2] || "https://asfadvogados.com/";

const browser = await chromium.launch();
try {
  const page = await browser.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  page.on("console", (msg) => {
    if (msg.type() === "error") errors.push(msg.text());
  });
  await page.goto(url, { waitUntil: "networkidle", timeout: 120000 });
  await page.waitForTimeout(5000);
  const state = await page.evaluate(() => ({
    title: document.title,
    loading: document.getElementById("__bundler_loading")?.textContent || "",
    err: document.getElementById("__bundler_err")?.textContent || "",
    thumbDisplay: getComputedStyle(document.getElementById("__bundler_thumbnail") || document.body).display,
    thumbVisible: !!document.getElementById("__bundler_thumbnail"),
    bodyLen: document.body?.innerText?.length || 0,
    bodySample: document.body?.innerText?.slice(0, 120) || "",
    hero: !!document.querySelector("#hero, [id*='hero'], h1"),
  }));
  console.log(JSON.stringify({ url, state, errors }, null, 2));
} finally {
  await browser.close();
}
