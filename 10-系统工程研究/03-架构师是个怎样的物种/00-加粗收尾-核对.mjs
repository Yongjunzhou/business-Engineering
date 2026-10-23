#!/usr/bin/env node
/**
 * 00-加粗收尾-核对.mjs —— 加粗（`**`）收尾的渲染安全自查（规则全文见手册 §2.12）
 *
 * 病：`**小标。**正文` 在 CommonMark 系渲染器里加粗闭不上，两个星号原样印出来。
 * 因：收尾的 `**` 必须"右邻接"——前面不能是标点（除非后面跟空白或标点）。
 *
 * 本脚本按 CommonMark 的 flanking 与"3 的规则"配对 `**`，报出会原样留下的标记数。
 * 用法：node 00-加粗收尾-核对.mjs        # 逐文件报数，合计应为 0
 *       node 00-加粗收尾-核对.mjs <文件>  # 报该文件的具体位置
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const isWs = (c) => c === undefined || /[ \t\r\n\u3000]/.test(c);
const isPunct = (c) => c !== undefined && /[\p{P}\p{S}]/u.test(c);

export function literalRuns(text) {
  const runs = [];
  const re = /\*\*+/g;
  let m;
  while ((m = re.exec(text))) {
    const start = m.index;
    const len = m[0].length;
    const prev = text[start - 1];
    const next = text[start + len];
    const left = !isWs(next) && (!isPunct(next) || isWs(prev) || isPunct(prev));
    const right = !isWs(prev) && (!isPunct(prev) || isWs(next) || isPunct(next));
    runs.push({ start, len, prev, next, canOpen: left, canClose: right, used: false });
  }
  for (let i = 0; i < runs.length; i++) {
    const c = runs[i];
    if (!c.canClose) continue;
    for (let j = i - 1; j >= 0; j--) {
      const o = runs[j];
      if (o.used || !o.canOpen) continue;
      const oddMatch =
        (o.canClose || c.canOpen) &&
        (o.len + c.len) % 3 === 0 &&
        !(o.len % 3 === 0 && c.len % 3 === 0);
      if (oddMatch) continue;
      o.used = true;
      c.used = true;
      break;
    }
  }
  return runs.filter((r) => !r.used);
}

/** 强调不跨块：按空行切段（带真实偏移），围栏内整段跳过 */
export function report(text) {
  const t = text.replace(/\r\n/g, '\n');
  const out = [];
  const sep = /\n[ \t]*\n/g;
  const blocks = [];
  let last = 0;
  let m;
  while ((m = sep.exec(t))) {
    blocks.push({ start: last, text: t.slice(last, m.index) });
    last = m.index + m[0].length;
  }
  blocks.push({ start: last, text: t.slice(last) });

  for (const b of blocks) {
    if (/^\s*(```|~~~)/.test(b.text)) continue;
    for (const r of literalRuns(b.text)) {
      out.push({ pos: b.start + r.start, prev: r.prev, next: r.next });
    }
  }
  return { text: t, hits: out };
}

const arg = process.argv[2];
if (arg) {
  const { text, hits } = report(fs.readFileSync(arg, 'utf8'));
  console.log(arg, '字面量', hits.length);
  for (const h of hits) {
    console.log('  prev', JSON.stringify(h.prev), 'next', JSON.stringify(h.next));
    console.log('  ...' + JSON.stringify(text.slice(Math.max(0, h.pos - 40), h.pos + 40)));
  }
} else {
  const files = fs
    .readdirSync(HERE)
    .filter((f) => /^(00-.*|\d\d-第\d+章.*)\.md$/.test(f) && !f.includes('从教材到'))
    .concat(['19-附录.md']);
  let total = 0;
  for (const f of files) {
    const n = report(fs.readFileSync(path.join(HERE, f), 'utf8')).hits.length;
    if (n) {
      console.log(f.padEnd(30), n);
      total += n;
    }
  }
  console.log('字面量合计', total, total === 0 ? '✓' : '（应为 0）');
}
