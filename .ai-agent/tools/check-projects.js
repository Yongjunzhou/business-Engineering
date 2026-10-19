#!/usr/bin/env node
/**
 * check-projects —— 校验项目集内每个独立项目都有独立记忆
 *
 * 【为什么需要】
 * AOS 根 CLAUDE.md §九 要求：项目集内每个独立项目都建 `claude-memory/`
 * （`MEMORY.md` 索引 ＋ 一份主记忆）。规则写得很清楚，但历史上曾有项目
 * 建区时漏了记忆，很久之后才发现——病根是规则躺在归档处，而动作发生在
 * 创建那一刻。本脚本把「漏了」从隐性变成显性：跑一遍即报。
 *
 * 【用法】
 *   node .ai-agent/tools/check-projects.js            列出所有项目状态
 *   node .ai-agent/tools/check-projects.js --quiet     只在有缺口时输出（供钩子用）
 *
 * 【扫描范围】
 * - 仓库根下 `NN-<名>/` 的独立项目；
 * - `00-candidate-businesses/`（候选业务池，不是项目，但同样要求独立记忆）；
 * - 跳过 `10-eos-engineering/`——主线工程块使用仓库根 `.claude/memory/`。
 *
 * 【退出码】有缺口 → 1；全齐 → 0
 */

'use strict';

const fs = require('fs');
const path = require('path');

const REPO_ROOT = path.resolve(__dirname, '../..');
const QUIET = process.argv.includes('--quiet');
const MAINLINE = '10-eos-engineering';
const CANDIDATES = '00-candidate-businesses';

// 一个条目合规 = claude-memory/ 存在 ＋ MEMORY.md 存在 ＋ 至少一份主记忆
function problemsOf(dir) {
  const mem = path.join(dir, 'claude-memory');
  if (!fs.existsSync(mem) || !fs.statSync(mem).isDirectory()) {
    return ['缺 claude-memory/'];
  }
  const files = fs.readdirSync(mem);
  const p = [];
  if (!files.includes('MEMORY.md')) p.push('缺 claude-memory/MEMORY.md');
  if (!files.some((f) => f.endsWith('项目.md'))) p.push('缺主记忆（<项目名>项目.md）');
  return p;
}

const entries = fs.readdirSync(REPO_ROOT, { withFileTypes: true })
  .filter((e) => e.isDirectory())
  .map((e) => e.name)
  .filter((name) => (/^\d{2}-/.test(name) && name !== MAINLINE) || name === CANDIDATES)
  .sort();

const lines = [];
let gaps = 0;
for (const name of entries) {
  const p = problemsOf(path.join(REPO_ROOT, name));
  if (p.length) { gaps++; lines.push('  ✗ ' + name + ' —— ' + p.join('；')); }
  else lines.push('  ✓ ' + name);
}

if (gaps) {
  console.log('项目记忆校验：' + entries.length + ' 个条目，' + gaps + ' 个有缺口\n');
  console.log(lines.join('\n'));
  console.log('\n补齐办法见 AOS 根 CLAUDE.md §九 项目集与项目记忆。');
  process.exit(1);
}
if (!QUIET) console.log('项目记忆校验：' + entries.length + ' 个条目全齐 ✓（主线 ' + MAINLINE + ' 使用根 .claude/memory/）');
process.exit(0);
