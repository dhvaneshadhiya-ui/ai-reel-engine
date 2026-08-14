#!/usr/bin/env node
/**
 * Fetch an official brand logo SVG (svgl.app) and extract its paths for the
 * LogoAssemble scene. Writes:
 *   public/assets/logos/<name>.svg
 *   public/assets/logos/<name>.paths.json  ({ viewBox, paths: [{d, fill}] })
 *
 * Usage: node tools/get_logo.mjs <name> [--query <search>] [--index 0]
 * Then in a beat: { "type": "logoassemble", "logo": "assets/logos/<name>.paths.json", ... }
 */
import fs from "node:fs";
import path from "node:path";

const args = process.argv.slice(2);
const name = args[0];
if (!name) {
  console.error("usage: node tools/get_logo.mjs <name> [--query q] [--index n]");
  process.exit(1);
}
const q = args.includes("--query") ? args[args.indexOf("--query") + 1] : name;
const idx = args.includes("--index") ? Number(args[args.indexOf("--index") + 1]) : 0;

const dir = path.join(import.meta.dirname, "..", "public", "assets", "logos");
fs.mkdirSync(dir, { recursive: true });

const res = await fetch(`https://api.svgl.app?search=${encodeURIComponent(q)}`);
if (!res.ok) throw new Error(`svgl search failed: ${res.status}`);
const hits = await res.json();
if (!hits.length) throw new Error(`no svgl results for "${q}"`);
console.log("matches:", hits.map((h, i) => `${i}:${h.title}`).slice(0, 6).join("  "));
const hit = hits[idx];
const route = typeof hit.route === "string" ? hit.route : hit.route.light;
const svg = await (await fetch(route)).text();

const svgPath = path.join(dir, `${name}.svg`);
fs.writeFileSync(svgPath, svg);

// --- extract viewBox + paths (covers typical brand SVGs) ---
const viewBox = (svg.match(/viewBox="([^"]+)"/) || [])[1] ?? "0 0 24 24";
const rootFill = (svg.match(/<svg[^>]*fill="([^"]+)"/) || [])[1];
const paths = [];
const re = /<path\b[^>]*>/g;
let m;
while ((m = re.exec(svg))) {
  const tag = m[0];
  const d = (tag.match(/\sd="([^"]+)"/) || [])[1];
  if (!d) continue;
  const fill = (tag.match(/fill="([^"]+)"/) || [])[1] ?? rootFill ?? "currentColor";
  if (fill === "none") continue;
  paths.push({ d, fill });
}
if (!paths.length) throw new Error("no <path> elements found — inspect the svg manually");

const out = { viewBox, paths, source: route, title: hit.title };
fs.writeFileSync(path.join(dir, `${name}.paths.json`), JSON.stringify(out, null, 2));
console.log(`saved ${svgPath}`);
console.log(`saved ${name}.paths.json — ${paths.length} paths, viewBox "${viewBox}"`);
