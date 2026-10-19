#!/usr/bin/env node
/**
 * make-table-images.mjs — 为「表格转图版」EPUB 准备素材
 *
 * 为什么：WPS 不认 CSS 边框（表格只剩文字、行还是行），FBReader 干脆不支持 table
 * （每个 <td> 独占一行）。两者都对表样式无能为力 → 把表格渲染成 PNG 嵌进电子书，
 * 任何阅读器都能看见框线。（PDF 侧不动，表格仍是真表格。）
 *
 * 做法：读 成书/build/*.book.md → 找出 markdown 表格块（含引用块里的 `> |`）→ pandoc 转 typst
 * → typst 编译成 PNG（宽度=版心、高度自适应）→ 把表格块替换成 ![](tbl-images/xxx.png)
 * → 输出到 build-tblimg/（不动 build/）。
 *
 * 用法：node build/make-table-images.mjs <bookDir> <buildDir> <outDir>
 */
import { readFileSync, writeFileSync, mkdirSync, rmSync, existsSync } from 'node:fs';
import { join, resolve, delimiter } from 'node:path';
import { execFileSync } from 'node:child_process';

const SRC = resolve(process.argv[2] || '..');
const BUILD = resolve(process.argv[3] || 'build');
const OUT = resolve(process.argv[4] || 'build-tblimg');

/**
 * 取工具路径：环境变量 → PATH → 各平台常见安装位置。
 * 2026-10-19：原先 pandoc／typst 写死 Windows 路径，换了机器（macOS）就跑不起来；
 * 与 build.sh 的 Chrome 探测同一思路——先问环境、再问 PATH、最后试常见位置。
 */
function resolveTool(envVar, names, fallbacks) {
  const fromEnv = process.env[envVar];
  if (fromEnv && existsSync(fromEnv)) return fromEnv;
  const dirs = (process.env.PATH || '').split(delimiter).filter(Boolean);
  const exts = process.platform === 'win32' ? ['.exe', ''] : [''];
  for (const name of names) {
    for (const dir of dirs) {
      for (const ext of exts) {
        const p = join(dir, name + ext);
        if (existsSync(p)) return p;
      }
    }
  }
  for (const p of fallbacks) if (existsSync(p)) return p;
  throw new Error(`找不到 ${names[0]}：请设 ${envVar} 或把它放进 PATH`);
}

const PANDOC = resolveTool('PANDOC_PATH', ['pandoc'], [
  'C:\\Users\\HUAWEI\\AppData\\Local\\Pandoc\\pandoc.exe',
  '/opt/homebrew/bin/pandoc',
  '/usr/local/bin/pandoc',
  '/usr/bin/pandoc',
]);
const TYPST = resolveTool('TYPST_PATH', ['typst'], [
  'C:\\Users\\HUAWEI\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Typst.Typst_Microsoft.Winget.Source_8wekyb3d8bbwe\\typst-x86_64-pc-windows-msvc\\typst.exe',
  '/opt/homebrew/bin/typst',
  '/usr/local/bin/typst',
  '/usr/bin/typst',
]);

// 字体按平台给候选：先给 Windows 的字面（与既有表图同源），再补 macOS／Linux 常见名。
// typst 取候选里第一个装了的；全无则走默认字体（中文仍出，但字形未必是宋体）。
const SERIF_FONTS = [
  'Noto Serif SC', 'SimSun',
  'Songti SC', 'STSong', 'Noto Serif CJK SC', 'Source Han Serif SC',
  'Noto Serif', 'serif',
];
const FONT_LIST = SERIF_FONTS.map((f) => `"${f}"`).join(', ');

const IMGDIR = join(OUT, 'tbl-images');
rmSync(OUT, { recursive: true, force: true });
mkdirSync(IMGDIR, { recursive: true });

const isRow = l => /^\s*(>\s*)?\|.*\|\s*$/.test(l);

function renderTable(mdLines, id) {
  const mdPath = join(OUT, `.t-${id}.md`);
  const typPath = join(OUT, `.t-${id}.content.typ`);
  const docPath = join(OUT, `.t-${id}.typ`);
  const pngPath = join(IMGDIR, `${id}.png`);
  writeFileSync(mdPath, mdLines.join('\n') + '\n', 'utf8');
  execFileSync(PANDOC, ['-f', 'markdown-smart', '-t', 'typst', mdPath, '-o', typPath], { stdio: 'inherit' });
  const body = readFileSync(typPath, 'utf8');
  const doc = [
    '#set page(width: 118mm, height: auto, margin: 2pt)',
    '#set text(font: (' + FONT_LIST + '), size: 8.5pt, lang: "zh", region: "cn")',
    '#set par(justify: true, leading: 0.9em, spacing: 0.5em, first-line-indent: 0em)',
    '#show table: set text(size: 8.5pt)',
    '#set table(stroke: 0.6pt + rgb("#7d7264"), inset: (x: 4pt, y: 3pt))',
    body,
  ].join('\n');
  writeFileSync(docPath, doc, 'utf8');
  execFileSync(TYPST, ['compile', '--ppi', '190', docPath, pngPath], { stdio: 'inherit' });
  // 超高表（附录里的长表动辄上千行）不转图：一是一张图几十 MB，二是缩到屏宽后字不可读
  const b = readFileSync(pngPath);
  const h = b.readUInt32BE(20);
  if (h > 3000) {
    rmSync(pngPath, { force: true });
    return null;
  }
  return `tbl-images/${id}.png`;
}

const bases = readFileSync(join(BUILD, 'manifest.txt'), 'utf8').split(/\r?\n/).filter(Boolean);
let total = 0;
for (const base of bases) {
  const lines = readFileSync(join(BUILD, base + '.book.md'), 'utf8').split(/\r?\n/);
  const out = [];
  let n = 0;
  for (let i = 0; i < lines.length; i++) {
    if (!isRow(lines[i])) { out.push(lines[i]); continue; }
    // 收集连续表行
    const start = i;
    while (i + 1 < lines.length && isRow(lines[i + 1])) i++;
    const block = lines.slice(start, i + 1);
    const quoted = /^\s*>/.test(block[0]);
    const clean = block.map(l => l.replace(/^\s*>\s?/, '').trim());
    // 至少要有表头 + 分隔行 + 一行数据
    if (clean.length < 3) { out.push(...block); continue; }
    const id = `${base}-t${String(++n).padStart(2, '0')}`;
    const rel = renderTable(clean, id);
    if (!rel) { out.push(...block); continue; }   // 超高表保持原样
    out.push(quoted ? `> ![](${rel})` : `![](${rel})`);
    total++;
  }
  writeFileSync(join(OUT, base + '.book.md'), out.join('\n'), 'utf8');
}
writeFileSync(join(OUT, 'manifest.txt'), bases.join('\n') + '\n', 'utf8');
console.log(`表格转图：${total} 张 → ${IMGDIR}`);
