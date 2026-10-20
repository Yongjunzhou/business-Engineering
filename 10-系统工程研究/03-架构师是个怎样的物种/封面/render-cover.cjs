/**
 * render-cover.cjs — 封面（前封 800 + 书脊 60 → 860×1132）SVG → PNG 预览渲染
 *
 * 源即 SVG（改版式改 SVG 后跑 node render-cover.cjs 即可），与成书管线 build/render-fig05-snake.cjs 同法。
 *
 * 用法：
 *   node render-cover.cjs                       # 默认 1×，输出 封面-前封书脊.png
 *   node render-cover.cjs --scale 2             # 2× 出图（1720×2264）
 *   node render-cover.cjs --out 出片.png --scale 4
 *
 * 依赖解析（**不再需要手动设 NODE_PATH**，换设备或换 Chrome 版本也不用改脚本）：
 *   puppeteer-core：require("puppeteer-core") → 本目录 node_modules → 成书 build/node_modules
 *                  → npx 缓存（%LOCALAPPDATA%\npm-cache\_npx\*\node_modules，或 ~/.npm/_npx/*）
 *   Chrome       ：CHROME_PATH / PUPPETEER_EXECUTABLE_PATH 环境变量
 *                  → .puppeteer.local.json（本目录，再成书 build；支持 Git-Bash 的 /c/... 写法）
 *                  → ~/.cache/puppeteer/chrome/*（取版本号最大者，Windows / macOS / Linux 三平台）
 *                  → 常见安装路径（Chrome、Edge）
 *   任一环命中不了就打印全部候选再退出，不静默回退。
 */
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const HERE = __dirname;
const BOOK_BUILD = path.join(HERE, '..', '成书', 'build');
const SRC = path.join(HERE, '封面-前封书脊.svg');
const DEFAULT_OUT = path.join(HERE, '封面-前封书脊.png');

// ── 命令行参数 ───────────────────────────────────────────────
const argv = process.argv.slice(2);
function argValue(flag) {
  const i = argv.indexOf(flag);
  return i >= 0 && i + 1 < argv.length ? argv[i + 1] : null;
}
const SCALE = Math.max(1, Number(argValue('--scale') || 1));
const OUT = argValue('--out') ? path.resolve(HERE, argValue('--out')) : DEFAULT_OUT;

// ── 小工具 ───────────────────────────────────────────────────
function readJsonSafe(file) {
  try { return JSON.parse(fs.readFileSync(file, 'utf8')); } catch { return null; }
}

/** Git-Bash 风格 /c/Users/... → C:/Users/...；其余原样返回 */
function normPath(p) {
  if (!p) return p;
  const m = /^\/cygdrive\/([a-zA-Z])\/(.*)$/.exec(p) || /^\/([a-zA-Z])\/(.*)$/.exec(p);
  return m ? `${m[1].toUpperCase()}:/${m[2]}` : p;
}

/** 版本号大到小排序（win64-148.0.7778.97 这类目录名） */
function byVersionDesc(a, b) {
  const num = (s) => (s.match(/\d+/g) || []).map(Number);
  const x = num(a), y = num(b);
  for (let i = 0; i < Math.max(x.length, y.length); i++) {
    if ((x[i] || 0) !== (y[i] || 0)) return (y[i] || 0) - (x[i] || 0);
  }
  return 0;
}

// ── Chrome 解析 ──────────────────────────────────────────────
function chromeCandidates() {
  const list = [];
  const push = (p, note) => { if (p) list.push({ path: normPath(p), note }); };

  for (const k of ['CHROME_PATH', 'PUPPETEER_EXECUTABLE_PATH']) {
    if (process.env[k]) push(process.env[k], `环境变量 ${k}`);
  }

  for (const dir of [HERE, BOOK_BUILD]) {
    for (const name of ['.puppeteer.local.json', 'puppeteer.json']) {
      const file = path.join(dir, name);
      const j = readJsonSafe(file);
      if (j && j.executablePath) {
        push(path.resolve(dir, normPath(j.executablePath)), path.join(path.basename(dir), name));
      }
    }
  }

  const cacheRoot = path.join(os.homedir(), '.cache', 'puppeteer', 'chrome');
  if (fs.existsSync(cacheRoot)) {
    for (const v of fs.readdirSync(cacheRoot).sort(byVersionDesc)) {
      const d = path.join(cacheRoot, v);
      push(path.join(d, 'chrome-win64', 'chrome.exe'), `puppeteer 缓存 ${v}`);
      push(path.join(d, 'chrome-win32', 'chrome.exe'), `puppeteer 缓存 ${v}`);
      push(path.join(d, 'chrome-mac-arm64', 'Google Chrome for Testing.app', 'Contents', 'MacOS', 'Google Chrome for Testing'), `puppeteer 缓存 ${v}`);
      push(path.join(d, 'chrome-mac', 'Google Chrome for Testing.app', 'Contents', 'MacOS', 'Google Chrome for Testing'), `puppeteer 缓存 ${v}`);
      push(path.join(d, 'chrome-linux64', 'chrome'), `puppeteer 缓存 ${v}`);
    }
  }

  const local = process.env.LOCALAPPDATA || '';
  for (const [p, note] of [
    ['C:/Program Files/Google/Chrome/Application/chrome.exe', 'Chrome 安装路径'],
    ['C:/Program Files (x86)/Google/Chrome/Application/chrome.exe', 'Chrome 安装路径'],
    [local && path.join(local, 'Google/Chrome/Application/chrome.exe'), 'Chrome 用户安装'],
    ['C:/Program Files/Microsoft/Edge/Application/msedge.exe', 'Edge 兜底'],
    ['C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', 'Edge 兜底'],
    ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', 'macOS 安装路径'],
    ['/usr/bin/google-chrome', 'Linux 安装路径'],
    ['/usr/bin/chromium', 'Linux 安装路径'],
    ['/usr/bin/chromium-browser', 'Linux 安装路径'],
  ]) push(p, note);

  return list;
}

function resolveChrome() {
  const list = chromeCandidates();
  for (const c of list) {
    if (fs.existsSync(c.path)) return c;
  }
  const lines = list.map((c) => `  ✗ ${c.path}  （${c.note}）`).join('\n');
  throw new Error(`未找到 Chrome/Edge 可执行文件，候选：\n${lines}\n可设环境变量 CHROME_PATH，或在 .puppeteer.local.json 里写 executablePath。`);
}

// ── puppeteer-core 解析 ──────────────────────────────────────
function loadPuppeteerCore() {
  const tried = [];
  const tryRequire = (spec, note) => {
    try { return { mod: require(spec), from: note }; }
    catch (e) { tried.push(`  ✗ ${note}  （${e.code || e.message}）`); return null; }
  };

  let r = tryRequire('puppeteer-core', 'require("puppeteer-core")');
  if (r) return r;

  const npxRoots = [
    process.env.LOCALAPPDATA && path.join(process.env.LOCALAPPDATA, 'npm-cache', '_npx'),
    path.join(os.homedir(), '.npm', '_npx'),
  ].filter((p) => p && fs.existsSync(p));

  for (const root of npxRoots) {
    let entries = [];
    try { entries = fs.readdirSync(root); } catch { entries = []; }
    for (const d of entries) {
      const cand = path.join(root, d, 'node_modules', 'puppeteer-core');
      if (!fs.existsSync(cand)) continue;
      r = tryRequire(cand, cand);
      if (r) return r;
    }
  }

  for (const cand of [path.join(HERE, 'node_modules', 'puppeteer-core'), path.join(BOOK_BUILD, 'node_modules', 'puppeteer-core')]) {
    if (!fs.existsSync(cand)) continue;
    r = tryRequire(cand, cand);
    if (r) return r;
  }

  throw new Error(`未找到 puppeteer-core，已试：\n${tried.join('\n')}\n可在本目录 npm i puppeteer-core，或先用 npx 装过一次 puppeteer（缓存里就有）。`);
}

// ── SVG 内在尺寸 ─────────────────────────────────────────────
function svgSize(file) {
  const head = fs.readFileSync(file, 'utf8').slice(0, 4000);
  const tag = /<svg[^>]*>/.exec(head);
  if (!tag) throw new Error(`SVG 根标签没找到：${file}`);
  const w = /\swidth="(\d+(?:\.\d+)?)"/.exec(tag[0]);
  const h = /\sheight="(\d+(?:\.\d+)?)"/.exec(tag[0]);
  return { W: w ? Math.round(Number(w[1])) : 860, H: h ? Math.round(Number(h[1])) : 1132 };
}

// ── 渲染 ─────────────────────────────────────────────────────
(async () => {
  if (!fs.existsSync(SRC)) throw new Error(`SVG 源缺失：${SRC}`);
  const { W, H } = svgSize(SRC);
  const { mod: puppeteer, from } = loadPuppeteerCore();
  const chrome = resolveChrome();

  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  const browser = await puppeteer.launch({
    executablePath: chrome.path, headless: 'new', args: ['--no-sandbox', '--disable-gpu'],
  });
  try {
    const page = await browser.newPage();
    await page.setViewport({ width: W, height: H, deviceScaleFactor: SCALE });
    await page.goto('file://' + SRC.replace(/\\/g, '/'), { waitUntil: 'load' });
    await new Promise((r) => setTimeout(r, 500));
    await page.screenshot({ path: OUT });
  } finally {
    await browser.close();
  }
  console.log(`render-cover: ${OUT}（${W * SCALE}×${H * SCALE}px，${SCALE}×）`);
  console.log(`  Chrome        ${chrome.path}  〔${chrome.note}〕`);
  console.log(`  puppeteer-core ${from}`);
})().catch((e) => { console.error(e.message || e); process.exit(1); });
