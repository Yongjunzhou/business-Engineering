#!/usr/bin/env node
/**
 * fix-typ.mjs — 修补 pandoc 生成的 .typ：
 *   给 figure 内 image() 注入适配 A5 版心的宽度（防溢出、保比例）
 *   pandoc 输出的图片无宽度，SVG 内在尺寸差异极大（宽 1841px ~ 高 984px），
 *   统一 width:100% 会让高图溢出页面。按每图 viewBox 计算 scale 注入 pt 宽度。
 *
 * 用法：node fix-typ.mjs <build目录>
 */
import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const OUT = process.argv[2] || '.';
const MAX_W = (110 / 25.4) * 72;    // 版心宽 110mm → 312.2pt
const MAX_H = (150 / 25.4) * 72;    // 图最大高 150mm → 425.2pt（避免撑满整页）

function pngSize(p) {
  try {
    const b = readFileSync(p);
    // PNG 签名(8) + 长度(4) + "IHDR"(4) → 宽高大端序各 4 字节
    if (b.slice(0, 8).toString('latin1') !== '\x89PNG\r\n\x1a\n') return null;
    return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
  } catch { return null; }
}

for (const f of readdirSync(OUT).filter(f => f.endsWith('.typ'))) {
  const path = join(OUT, f);
  let t = readFileSync(path, 'utf8');
  const orig = t;
  // 统一行尾为 LF：pandoc 在 Windows 输出 CRLF，否则 ^…\n / #block[…\n 等行锚正则全部失配
  t = t.replace(/\r\n/g, '\n');
  // 剥掉 pandoc 生成的独立 label 行（如 <本章判据>）——各章同名 label 会破坏 outline 定位，
  // 而书内无 @ 交叉引用这些 label，剥离安全
  t = t.replace(/^<[^>\n]+>\n/gm, '');
  t = fitTableColumns(t);
  t = t.replace(/image\("figs\/([^"]+)", alt: "([^"]*)"\)/g, (m, file, alt) => {
    const sz = pngSize(join(OUT, 'figs', file));
    if (!sz) return m;
    const wpt = sz.w * 0.75;   // px(96dpi) → pt(72dpi)
    const hpt = sz.h * 0.75;
    const scale = Math.min(MAX_W / wpt, MAX_H / hpt, 1);
    const w = wpt * scale;
    return `image("figs/${file}", alt: "${alt}", width: ${w.toFixed(1)}pt)`;
  });
  // 序言/前言署名（fenced div .signature → pandoc 转 #block[名 日期]）→ 右对齐块
  // 正文全局 first-line-indent:2em，署名去缩进；内容门控（黄涛/周拥军）防误伤其他 #block
  t = t.replace(/#block\[\n([^\n]+)\n\n\]/g, (m, inner) => {
    if (!/(黄涛|周拥军)/.test(inner)) return m;
    return `#align(right)[\n  #set par(first-line-indent: 0em)\n  ${inner}\n]`;
  });
  if (t !== orig) {
    writeFileSync(path, t);
    console.log(`fix-typ: ${f}（注入图片宽度）`);
  }
}
console.log('fix-typ.mjs 完成');

// ---------- 表格列宽：按各列内容算百分比（2026-10-19） ----------
// pandoc 输出的表格列宽一律等分（`columns: 4` 或 `(33.33%, 33.33%, 33.33%)`），
// 于是"提出者""①"这类窄列与整段定义文字平分版心，读起来极不经济。
// 这里按每列内容的最大视觉宽度（CJK 记 2、西文记 1）估算权重再归一成百分比，
// 并用 0.75 次幂压缩长列、设 9% 下限，避免一列吃掉半页或窄列挤成两字一行。
function vlen(s) {
  const plain = s
    .replace(/#strong\[([^\]]*)\]/g, '$1')
    .replace(/#emph\[([^\]]*)\]/g, '$1')
    .replace(/#link\([^)]*\)\[([^\]]*)\]/g, '$1')
    .replace(/\\(.)/g, '$1')
    .replace(/[*_`]/g, '')
    .replace(/<br\s*\/?>/g, '');
  let n = 0;
  for (const ch of plain) {
    const c = ch.codePointAt(0);
    n += (c >= 0x2e80 && c <= 0xa4cf) || (c >= 0xac00 && c <= 0xd7a3) ||
         (c >= 0xf900 && c <= 0xfaff) || (c >= 0xfe30 && c <= 0xfe4f) ||
         (c >= 0xff00 && c <= 0xff60) || (c >= 0xffe0 && c <= 0xffe6) ? 2 : 1;
  }
  return n;
}

function rewriteTableColumns(block) {
  const m = block.match(/columns:\s*(\([^)]*\)|\d+)/);
  if (!m) return block;
  const n = m[1].startsWith('(')
    ? m[1].slice(1, -1).split(',').map(s => s.trim()).filter(Boolean).length
    : parseInt(m[1], 10);
  if (!n || n < 2) return block;
  // 收集 cells（列宽元组之后的顶层 [...]）
  const cells = [];
  let bracket = 0, start = -1;
  const from = m.index + m[0].length;
  for (let j = from; j < block.length; j++) {
    const ch = block[j];
    if (ch === '[') { if (bracket === 0) start = j + 1; bracket++; }
    else if (ch === ']') { bracket--; if (bracket === 0 && start >= 0) { cells.push(block.slice(start, j)); start = -1; } }
  }
  if (cells.length < n * 2) return block;
  const rows = Math.floor(cells.length / n);
  const colMax = new Array(n).fill(0);
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < n; c++) {
      colMax[c] = Math.max(colMax[c], vlen(cells[r * n + c] || ''));
    }
  }
  // 长文本列封顶（60 视觉宽 ≈ 版心的一半），再 0.75 次幂软化
  const w = colMax.map(v => Math.pow(Math.min(Math.max(v, 4), 60), 0.75));
  const sum = w.reduce((a, b) => a + b, 0);
  let pct = w.map(v => (v / sum) * 100);
  // 下限 9%，其余列按比例回缩（迭代到稳定）——不能把缺口一股脑压给一列，
  // 否则多列表（如后记 9 列）会被压到 3% 以下
  const FLOOR = 9;
  for (let it = 0; it < 12; it++) {
    const below = pct.filter(v => v < FLOOR).length;
    if (!below) break;
    let fixedSum = 0, freeSum = 0;
    for (const v of pct) { if (v < FLOOR) fixedSum += FLOOR; else freeSum += v; }
    const k = (100 - fixedSum) / (freeSum || 1);
    pct = pct.map(v => (v < FLOOR ? FLOOR : v * k));
  }
  const rounded = pct.map(v => Math.round(v * 100) / 100);
  // 尾差补到最宽列（不回冲到窄列）
  const widest = rounded.indexOf(Math.max(...rounded));
  const diff = Math.round((100 - rounded.reduce((a, b) => a + b, 0)) * 100) / 100;
  rounded[widest] = Math.round((rounded[widest] + diff) * 100) / 100;
  const cols = '(' + rounded.map(v => v + '%').join(', ') + ')';
  return block.slice(0, m.index) + 'columns: ' + cols + block.slice(m.index + m[0].length);
}

function fitTableColumns(t) {
  let out = '', i = 0;
  const KEY = '#table(';
  for (;;) {
    const p = t.indexOf(KEY, i);
    if (p < 0) { out += t.slice(i); break; }
    out += t.slice(i, p);
    let depth = 0, bracket = 0, j = p + KEY.length - 1;
    for (; j < t.length; j++) {
      const ch = t[j];
      if (ch === '[') bracket++;
      else if (ch === ']') bracket--;
      else if (bracket === 0) {
        if (ch === '(') depth++;
        else if (ch === ')') { depth--; if (depth === 0) break; }
      }
    }
    const block = t.slice(p, j + 1);
    out += rewriteTableColumns(block);
    i = j + 1;
  }
  return out;
}
