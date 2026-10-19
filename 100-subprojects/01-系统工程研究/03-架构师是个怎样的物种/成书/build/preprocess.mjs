#!/usr/bin/env node
/**
 * preprocess.mjs — 教材书 → .book.md 清洗脚本
 *
 * 职责（不动源文件，输出到 build/）：
 *   1. 按 MANIFEST 顺序组装（序言/前言/01~18 章/19 附录）
 *   2. 剔除每文件末尾「## 版本变更记录」表（写作元数据）
 *   3. 提取 mermaid 块 → build/.mmd/chNN-figKK.mmd 源，替换为 ![](figs/chNN-figKK.svg)
 *      图号「图 N-K」按章内序号；修复 ch9 裸 `&` 转义
 *   4. 非编号/含「章首」的 ##/### 标题追加 {.unlisted}（附录除外）——双轨目录排除
 *   5. 输出 build/*.book.md + build/manifest.txt（顺序清单）
 *
 * 用法：node preprocess.mjs <SRC目录> <OUT目录>
 */
import { readFileSync, writeFileSync, mkdirSync, readdirSync, rmSync, statSync } from 'node:fs';
import { join, resolve } from 'node:path';

const SRC = resolve(process.argv[2] || '..');   // 教材书/ 源目录
const OUT = resolve(process.argv[3] || 'build'); // 输出目录

for (const d of ['', '.mmd', 'figs', 'assets']) mkdirSync(join(OUT, d), { recursive: true });
// 清空上次构建的 .mmd 与 .book.md（figs 保留已渲染图可复用）
const rmFile = p => { if (statSync(p).isFile()) rmSync(p); };
for (const f of readdirSync(join(OUT, '.mmd'))) rmFile(join(OUT, '.mmd', f));
for (const f of readdirSync(OUT).filter(f => f.endsWith('.book.md')))
  rmFile(join(OUT, f));

// ---------- MANIFEST：磁盘 glob + 前缀匹配，抗文件名变化 ----------
const all = readdirSync(SRC).filter(f => f.endsWith('.md'));
// ★ 2026-10-19 修：`00-后记` 前缀会先撞上同目录的《00-后记-概念一致性审视清单.md》，
// 结果成书里"后记"位置装的是内部审计清单、真正的后记被顶掉（且该表 9 列在 A5 上崩版）。
// 故把一切 `*-审视清单.md` 与 `00-ch*` 类工作件排除在 MANIFEST 之外。
const EXCLUDE_RE = /从教材到问题分析|审视清单\.md$|^00-ch|^00-(全书框架|案例设定|方法论的底座|重构开工包|目录)/;
const files = all.filter(f => !EXCLUDE_RE.test(f));
function findFile(prefix) {
  const hit = files.find(f => f.startsWith(prefix));
  if (!hit) throw new Error(`preprocess: 未找到源文件 ${prefix}*（实际：${files.slice(0, 8).join(', ')}…）`);
  return hit;
}
const chapters = Array.from({ length: 18 }, (_, i) => `${String(i + 1).padStart(2, '0')}-第${i + 1}章`);
const MANIFEST = ['00-序言', '00-前言', ...chapters, '00-后记', '19-附录'].map(prefix => [findFile(prefix), prefix]);

// ---------- 变换 ----------
function stripVersionRecord(text) {
  const i = text.search(/^##\s*版本变更记录\s*$/m);
  if (i === -1) return text;
  return text.slice(0, i).replace(/\n---\s*\n?$/, '').replace(/\s+$/, '\n');
}

/**
 * 剔除首标题后的元信息引用块（仅序言/前言）——写作契约保留在源文件，不入书。
 * 与「版本变更记录」同属写作元数据；章首导语（第4章/附录等给读者看）不受影响。
 * 结构：`# 标题` + 空行 + `> 元信息` + 空行 + `---`；替换后剩 `# 标题` + 空行 + `---`
 */
function stripLeadingMetaQuote(text, base) {
  if (base !== '00-序言' && base !== '00-前言' && base !== '00-后记') return text;
  return text.replace(/^(# .*?)\n\n>.*?\n\n(?=---)/ms, '$1\n\n');
}

function extractMermaid(text, chapterNo) {
  let figCount = 0;
  const chapDisp = String(parseInt(chapterNo, 10) || 0); // 图注用「1-3」非「01-3」
  return text.replace(/```mermaid\s*\n([\s\S]*?)\n```/g, (_m, body) => {
    figCount++;
    const figId = `ch${chapterNo}-fig${String(figCount).padStart(2, '0')}`;
    // 修复裸 &（ch9 "design & evolution"）；已转义实体原样保留
    const cleaned = body.replace(/&(?!amp;|lt;|gt;|quot;|#\d+;|#x[0-9a-fA-F]+;)/g, '&amp;');
    writeFileSync(join(OUT, '.mmd', figId + '.mmd'), cleaned + '\n');
    // 用 PNG（mermaid 的 SVG 含 <foreignObject>，typst 无法渲染；PNG 中文完整、3× 栅格打印清晰）
    return `\n![图 ${chapDisp}-${figCount}](figs/${figId}.png)\n`;
  });
}

function markUnlisted(text, isAppendix) {
  if (isAppendix) return text;
  return text.split('\n').map(line => {
    const m = line.match(/^(\#{2,3})\s+(.+?)\s*$/);
    if (!m) return line;
    // 保留 heading 已有 classes（如 .pagebreak，EPUB section 分页用），再合并 .unlisted（双轨目录排除）
    const attrMatch = m[2].match(/\{([^}]*)\}/);
    const existing = attrMatch ? ((attrMatch[1].match(/\.([\w-]+)/g) || []).map(s => s.slice(1))) : [];
    const title = m[2].replace(/\s*\{[^}]*\}\s*$/, '').trim();
    // 章首·误解现场（带编号但约定不入目录）或未编号章末件 → 目录排除
    if (title.includes('章首') || !/^\d/.test(title)) {
      const classes = [...new Set([...existing, 'unlisted'])];
      return `${m[1]} ${title} {.${classes.join(' .')}}`;
    }
    return line;
  }).join('\n');
}


// ---------- 中文引号开合修复 ----------
// 背景：pandoc 的 smart 引号按"前一字符是否空白"判开合，中文引号紧贴汉字 → 几乎全部被判成闭引号
// （实测 typ 里 9,023 个 ” vs 27 个 “，印出来是"回答的是”这一大类…"）。故在预处理阶段按阅读顺序
// 成对替换为 “ 与 ”，并让 pandoc 关掉 smart（-f markdown-smart），避免它再改一遍。
function fixCjkQuotes(text) {
  const parts = text.split(/(```[\s\S]*?```)/g);
  let open = true, n = 0;
  const joined = parts.map((seg, i) => {
    if (i % 2 === 1) return seg;                 // 围栏代码块：原样
    return seg.replace(/(`+[^`]*`+)|"/g, (m, code) => {
      if (code) return code;                      // 行内代码：原样
      const q = open ? '“' : '”';
      open = !open; n++;
      return q;
    });
  }).join('');
  if (!open) console.warn('  ⚠ 引号总数为奇数，末一个未闭合——请核源文');
  console.log(`  引号：ASCII " → “/” ${n} 处`);
  return joined;
}


// ---------- 表格列宽：按内容重写分隔行横线（2026-10-19） ----------
// pandoc 的列宽取自表头分隔行的横线长度（pipe 表）——源文一律 `---`，于是 EPUB 里
// 每列等宽（`<col style="width:25%">`）。这里按各列内容的最大视觉宽（CJK 2／西文 1）
// 重写横线长度，使 EPUB 与 PDF 两侧都拿到"按内容分配"的列宽。
function vwidth(s) {
  const plain = s.replace(/\*\*/g, '').replace(/\*/g, '').replace(/`/g, '');
  let n = 0;
  for (const ch of plain) {
    const c = ch.codePointAt(0);
    n += (c >= 0x2e80 && c <= 0xa4cf) || (c >= 0xac00 && c <= 0xd7a3) ||
         (c >= 0xf900 && c <= 0xfaff) || (c >= 0xfe30 && c <= 0xfe4f) ||
         (c >= 0xff00 && c <= 0xff60) || (c >= 0xffe0 && c <= 0xffe6) ? 2 : 1;
  }
  return n;
}

function fitTableDashes(text) {
  const lines = text.split('\n');
  const isRow = l => /^\s*\|.*\|\s*$/.test(l);
  const isSep = l => isRow(l) && l.split('|').slice(1, -1).every(c => /^\s*:?-{3,}:?\s*$/.test(c));
  let n = 0;
  for (let i = 1; i < lines.length; i++) {
    if (!isRow(lines[i - 1]) || !isSep(lines[i])) continue;
    // 找到表格块的范围
    let s = i - 1, e = i + 1;
    while (s > 0 && isRow(lines[s - 1])) s--;
    while (e < lines.length && isRow(lines[e])) e++;
    const cellCount = lines[i].split('|').slice(1, -1).length;
    if (cellCount < 2) continue;
    const w = new Array(cellCount).fill(3);
    for (const row of lines.slice(s, e)) {
      if (isSep(row)) continue;
      const cells = row.split('|').slice(1, -1);
      cells.forEach((c, k) => { if (k < cellCount) w[k] = Math.max(w[k], vwidth(c.trim())); });
    }
    // 长列封顶 + 0.75 次幂软化，最少 3 条横线
    const ww = w.map(v => Math.pow(Math.min(Math.max(v, 4), 48), 0.75));
    lines[i] = '|' + ww.map(v => '-'.repeat(Math.max(3, Math.round(v)))).join('|') + '|';
    n++;
  }
  if (n) console.log(`  表格列宽：按内容重写分隔行 ${n} 处`);
  return lines.join('\n');
}

// ---------- 主循环 ----------
const manifestRows = [];
for (const [srcName, base] of MANIFEST) {
  let text = readFileSync(join(SRC, srcName), 'utf8');
  text = stripVersionRecord(text);
  text = stripLeadingMetaQuote(text, base);
  const chap = base.match(/^(\d+)/)?.[1] ?? '00';
  text = extractMermaid(text, chap);
  text = fixCjkQuotes(text);
  text = fitTableDashes(text);
  text = markUnlisted(text, base === '19-附录');
  writeFileSync(join(OUT, base + '.book.md'), text);
  manifestRows.push(base);
  console.log(`✓ ${srcName} → ${base}.book.md（${(text.length / 1024).toFixed(0)} KB）`);
}
writeFileSync(join(OUT, 'manifest.txt'), manifestRows.join('\n') + '\n');
const mmdCount = readdirSync(join(OUT, '.mmd')).length;
console.log(`manifest.txt: ${manifestRows.length} 文件；mermaid 源 ${mmdCount} 个`);
