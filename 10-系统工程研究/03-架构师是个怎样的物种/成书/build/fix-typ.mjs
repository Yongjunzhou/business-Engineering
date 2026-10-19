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
// ★ 2026-10-19：图内字号（用户：「图1-1的字号好大」）。
// mermaid 按 build.sh 的 `mmdc -s 3` 渲染——PNG 是 3 倍设备像素，故它的"纸上自然尺寸"
// 是 px 宽 ÷ 3 × 0.75pt（一图 px→0.75pt）。按版心放大若超过这个自然尺寸，
// 图里的字就比正文还大：图1-1 曾被撑到 294.9pt（自然 207pt），字约 17pt。
// 故宽度上限取自然尺寸，即最多放大到 1:1，不再越界。
const RENDER_SCALE = 3;

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
  t = unwrapTableFigures(t);
  t = t.replace(/image\("figs\/([^"]+)", alt: "([^"]*)"\)/g, (m, file, alt) => {
    const sz = pngSize(join(OUT, 'figs', file));
    if (!sz) return m;
    const wpt = sz.w * 0.75;   // px(96dpi) → pt(72dpi)
    const hpt = sz.h * 0.75;
    const scale = Math.min(MAX_W / wpt, MAX_H / hpt, 1);
    let w = wpt * scale;
    const natural = (sz.w * 0.75) / RENDER_SCALE;
    if (w > natural) w = natural;   // 不放大到超过渲染自然尺寸（否则图内字号反超正文）
    return `image("figs/${file}", alt: "${alt}", width: ${w.toFixed(1)}pt)`;
  });
  // 图题去重号（2026-10-19）：pandoc 把 Markdown 的 "图 1-1" 原样搬成 caption 正文，
  // 而 typst 的 figure 又自动在题前加 supplement＋计数器，PDF 里成了「图 1  图 1-1」。
  // 书中图号自带章号（图 X-Y），故关掉自动编号，题注只留原文。
  t = t.replace(
    /(#figure\(image\("figs\/[^"]+",[^)]*\),)\n[ \t]*caption: \[\n[ \t]*(图[ \t]*\d+[-–—]\d+)\n[ \t]*\]\n\)/g,
    (m, head, cap) => `${head}\n  numbering: none,\n  caption: [\n    ${cap}\n  ]\n)`,
  );
  // 序言/前言署名（fenced div .signature → pandoc 转 #block[名 日期]）→ 右对齐块
  // 正文全局 first-line-indent:2em，署名去缩进；内容门控（四位署名者）防误伤其他 #block
  // ★ 2026-10-19 补：宋宁／宋海伟两处此前漏网（只认黄涛／周拥军），PDF 里左对齐；EPUB 的 .signature 是右对齐，两轨不一致，一并收进
  t = t.replace(/#block\[\n([^\n]+)\n\n\]/g, (m, inner) => {
    if (!/(黄涛|周拥军|宋宁|宋海伟)/.test(inner)) return m;
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

// 最长"不可断片断"的视觉宽：西文单词整词不能断（否则切到单元格外面），
// 汉字可逐字换行，故汉字记 2、西文单词按字母数记 1。
function longestToken(s) {
  const plain = s
    .replace(/#strong\[([^\]]*)\]/g, '$1')
    .replace(/#emph\[([^\]]*)\]/g, '$1')
    .replace(/#link\([^)]*\)\[([^\]]*)\]/g, '$1')
    .replace(/\\(.)/g, '$1')
    .replace(/[*_`]/g, '');
  let best = 0;
  for (const m of plain.matchAll(/[A-Za-z0-9][A-Za-z0-9.'’\-]*/g)) {
    // 表内已开英文断字（book.typ：show table 设 hyphenate），长词可在音节处断开，
    // 不再要求整词宽度；六字母以内仍按整词算。
    const L = m[0].length;
    best = Math.max(best, L <= 6 ? L : Math.max(6, Math.ceil(L * 0.55)));
  }
  if (/[\u2e80-\u9fff\uf900-\ufaff\uff00-\uff60]/.test(plain)) best = Math.max(best, 2);
  return best;
}

function rewriteTableColumns(block) {  const m = block.match(/columns:\s*(\([^)]*\)|\d+)/);
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
  const heaviest = Math.max(...colMax);
  let pct;
  if (heaviest > 60) {
    // ★ 2026-10-19：长单元格表（附录 A 术语表、附录 C 五病对照、附录 D 文献表）
    // 不能按"最大内容宽"分配——一格里能塞一千多视觉宽，谁最长谁吃满，其余列被压成
    // 一列竖排字（术语列只剩两个字宽，一行折九截，236 条词条占六七十页）。
    // 改为两段式：
    //   ① 最小可容宽 floor：按该列最长**不可断片断**（西文单词、CJK 单字）折成版心百分比，
    //      保证英文术语不被切、汉字不竖排；
    //   ② 余量按"该列 75 分位内容长 − floor"分配，最长的定义列自然拿到大头，
    //      极端长的个别单元格交给换行，不再由它独占宽度。
    const PAGE_PT = 312.2;           // A5 版心宽 110mm
    const UNIT_PT = 4.5;             // 1 视觉单位 ≈ 半个汉字 ≈ 4.5pt（9pt 表字号）
    const PAD_PT = 7;                // 单元格内边距（table.cell inset x=2pt×2 ＋ 断行余量）
    const floor = new Array(n).fill(0);   // 硬下限：不断词、不竖排
    const soft = new Array(n).fill(0);    // 软下限：常见内容宽（可压缩）
    const want = new Array(n).fill(0);
    for (let c = 0; c < n; c++) {
      const vals = [], tokens = [];
      for (let r = 0; r < rows; r++) {
        const cell = cells[r * n + c] || '';
        vals.push(vlen(cell));
        tokens.push(longestToken(cell));
      }
      vals.sort((a, b) => a - b);
      want[c] = vals[Math.floor((vals.length - 1) * 0.75)] || 0;   // 75 分位
      // 下限＝两者之大：
      //   ① 硬下限：该列最长不可断片断（表内已开英文断字，长词折半算）——守住不切词；
      //   ② 常见内容宽封顶 8%（"第11章""T-58"这类短列不竖排成一条线）。
      // 不按"最大内容宽"也不按面板均分：短列各守 8%，余下六成以上全给最长的定义/条款列。
      const tokenFloor = (Math.max(...tokens) * UNIT_PT + PAD_PT) / PAGE_PT * 100;
      floor[c] = Math.max(tokenFloor, 8);
    }
    const floorSum = floor.reduce((a, b) => a + b, 0);
    if (floorSum >= 96) {                       // 窄列太多、版面装不下：按 floor 等比缩
      pct = floor.map(v => (v / floorSum) * 100);
    } else {
      const extra = want.map((v, c) => Math.max(v - (floor[c] / 100) * (PAGE_PT / UNIT_PT), 1));
      const extraSum = extra.reduce((a, b) => a + b, 0);
      const rest = 100 - floorSum;
      pct = floor.map((f, c) => f + (rest * extra[c]) / extraSum);
    }
  } else {
    // 短单元格表：原口径——封顶 60 视觉宽（≈版心一半）、0.75 次幂、9% 下限
    const w = colMax.map(v => Math.pow(Math.min(Math.max(v, 4), 60), 0.75));
    const sum = w.reduce((a, b) => a + b, 0);
    pct = w.map(v => (v / sum) * 100);
    const FLOOR = 9;
    for (let it = 0; it < 12; it++) {
      const below = pct.filter(v => v < FLOOR).length;
      if (!below) break;
      let fixedSum = 0, freeSum = 0;
      for (const v of pct) { if (v < FLOOR) fixedSum += FLOOR; else freeSum += v; }
      const k = (100 - fixedSum) / (freeSum || 1);
      pct = pct.map(v => (v < FLOOR ? FLOOR : v * k));
    }
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

// ---------- 拆掉表格的 figure 外壳（2026-10-19） ----------
// pandoc 把每张表包成
//   #figure(
//     align(center)[#table(…)]
//     , kind: table
//     )
// 而 typst 的 figure 是**不可跨页**的原子块：短表无碍，长表（附录 C 五病对照、
// 附录 A／D 长清单）放不下一页就整块溢出版心，页脚处压成一团黑，行文丢失。
// 书内表格一律无题注（caption 只属于图），拆壳不损失信息；拆后裸表可正常分页，
// 表头随 table.header() 逐页重复。拆法：括号配对找到 align(center)[…] 的内层，
// 只回填内层，外壳连 `, kind: table` 一并丢弃。
function unwrapTableFigures(t) {
  const OPEN = '#figure(\n  align(center)[';
  let out = '', i = 0;
  for (;;) {
    const p = t.indexOf(OPEN, i);
    if (p < 0) { out += t.slice(i); break; }
    out += t.slice(i, p);
    const contentStart = p + OPEN.length;
    let bracket = 1, j = contentStart;
    for (; j < t.length; j++) {
      const ch = t[j];
      if (ch === '[') bracket++;
      else if (ch === ']') { bracket--; if (bracket === 0) break; }
    }
    const tail = t.slice(j + 1, j + 60);
    const m = tail.match(/^\s*,\s*kind:\s*table\s*\)/);
    if (!m) {                       // 不是表格外壳（例如带题注的图），原样保留
      out += t.slice(p, j + 1);
      i = j + 1;
      continue;
    }
    out += t.slice(contentStart, j);   // 只留 align(center)[ 的内层，#table(…) 本体
    i = j + 1 + m[0].length;
  }
  return out;
}
