#!/usr/bin/env node
/**
 * new-project —— 在项目集根目录新建独立项目，配件一次建齐
 *
 * 【为什么需要】
 * 项目集的建项配方是四件事：建项目目录 → 建项目 CLAUDE.md → 建 claude-memory/
 * → 在 PROJECTS.md 加一行。配方写得很清楚，但历史上曾有项目建区时漏了记忆。
 * 病根是：**规则躺在归档处，动作发生在创建那一刻**。本脚本把前三件收进一条
 * 命令；第四件仍人工（它改的是权威文档，脚本代笔不妥，但会打印可粘贴的一行）。
 *
 * 【用法】
 *   node .ai-agent/tools/new-project.js <名>              建下一个顺号项目
 *   node .ai-agent/tools/new-project.js --dry-run <名>     只显示将建什么
 *
 * 【建的什么】
 *   NN 自动取项目集内现有最大号 +1（`10-eos-engineering` 是主线工程块，
 *   不参与编号；`candidate-businesses` 不是项目，也不参与）
 *   NN-<名>/
 *   ├── CLAUDE.md                 项目 CLAUDE.md（隔离协议与边界齐备，定位留待填）
 *   └── claude-memory/
 *       ├── MEMORY.md             索引
 *       └── <名>项目.md            主记忆
 */

'use strict';

const fs = require('fs');
const path = require('path');

const REPO_ROOT = path.resolve(__dirname, '../..');
const MAINLINE = '10-eos-engineering';

const argv = process.argv.slice(2);
const DRY_RUN = argv.includes('--dry-run');
const name = argv.filter((a) => !a.startsWith('--'))[0];

if (!name) {
  console.error('用法：node .ai-agent/tools/new-project.js [--dry-run] <名>');
  console.error('  例：node .ai-agent/tools/new-project.js 供应链研究');
  process.exit(1);
}

// ── 取下一个顺号（主线块与候选业务池不参与） ──────────────────────
const used = fs.readdirSync(REPO_ROOT, { withFileTypes: true })
  .filter((e) => e.isDirectory() && e.name !== MAINLINE)
  .map((e) => /^(\d{2})-/.exec(e.name))
  .filter(Boolean)
  .map((m) => parseInt(m[1], 10))
  .filter((n) => n < 10);
const nn = String((used.length ? Math.max(...used) : 0) + 1).padStart(2, '0');

const DIR = path.join(REPO_ROOT, nn + '-' + name);
if (fs.existsSync(DIR)) {
  console.error('❌ 已存在：' + DIR);
  process.exit(1);
}

const today = new Date().toISOString().slice(0, 10);

const PROJECT_CLAUDE_MD = `# CLAUDE.md（${nn}-${name} · ${name}项目）

本目录是 AOS 项目集里的**独立项目**。**定位待补**——写清本项目负责共同目标「把不同专业的工作或事项工程化」在哪一个专业领域上的展开。

## 项目边界（项目集内 · 操作互不干扰）

本项目是 AOS 项目集的一员，各项目共同指向「**把不同专业的工作或事项工程化**」这一目标。按 AOS 根 CLAUDE.md §九 **自包含在本目录内**：

- **处理本项目**：工作目录 = 本目录（\`${nn}-${name}/\`），读本文件 + \`claude-memory/\`。
- **处理其他项目 / 主线工程**：工作目录 = 对应目录，读对应 CLAUDE.md——**不擅自改动其内容**，除非明确要求。
- **主题上可互引、操作上自包含**：本项目的方法与结论可被其他项目引用，反之亦然；改动落在谁家由谁做。

## 记忆隔离协议

本项目的记忆**独立存放**，与仓库根记忆（\`.claude/memory/\`）**互不干扰**：

- 本项目的记忆位于 [\`claude-memory/\`](claude-memory/)：\`claude-memory/MEMORY.md\`（索引）+ \`claude-memory/${name}项目.md\`（主记忆）。
- **编写/研究本项目时**：先读 \`claude-memory/MEMORY.md\` 与相关记忆文件，写入 \`claude-memory/\` 目录。
- **禁止**把本项目内容写入仓库根 \`.claude/memory/\`。

## 提交边界（单仓库 + 约定分区）

仓库是 AOS 单一 git 仓库，本项目不建独立 git。**每次提交只针对本目录内容**：commit message 注明归属（如 \`[${name}]\`），本目录改动不与其他项目或主线工程的改动混提；反之亦然。

## 工作风格与文档纪律

- **禁止选项式交互**：讨论/确认一律自由散文陈述（背景 + 问题 + 建议 + 理由），不用 AskUserQuestion 选项卡/选项卡片让用户做多选题；用户自由回答"改/不改/怎么改"，再据其指示执行（2026-08-25 用户定，仓库全级生效）。

## 文档规范

- Markdown + Mermaid；中文为主体、术语附英文。
- **md→PDF（用户指定的统一转换方式）**：用仓库根 \`.ai-agent/tools/md2pdf/\` 下的转换工具（\`node .ai-agent/tools/md2pdf/md2pdf.js <md路径> [输出.pdf]\`，marked + puppeteer 渲染，支持 Mermaid）。工具在仓库根，从本目录相对写即 \`../.ai-agent/tools/md2pdf/md2pdf.js\`；默认输出与源文件同名 .pdf。规则源头见 AOS 根 CLAUDE.md §七。

## 关键文件导航

（待补）
`;

const MEMORY_INDEX = `# ${name}项目记忆索引（独立于仓库根记忆）

> 本目录是 **${nn}-${name} 项目** 的**独立记忆**，与仓库根记忆（\`.claude/memory/\`）**互不干扰**。
> 处理本项目内容时：先读本索引 → 读对应记忆文件 → 写入本目录；**不要**写入仓库根 \`.claude/memory/\`。
> 本记忆随仓库版本管理（位于项目内），可跨设备共享（机制见 AOS 根 CLAUDE.md §八）。

- **${today} 建项**：按 AOS 根 CLAUDE.md §九 建项配方建项（项目 CLAUDE.md 与 \`claude-memory/\` 由 \`.ai-agent/tools/new-project.js\` 一次建齐）。定位与内容待补。详见 [${name}项目.md](${name}项目.md)
`;

const MAIN_MEMORY = `---
name: ${name}项目
description: ${name}项目主记忆——本项目的定位/现行内容/决策（独立于仓库根记忆，存放于 ${nn}-${name}/claude-memory/）
metadata:
  type: project
---

> 本文件是 **${nn}-${name} 项目** 的独立主记忆，与仓库根 \`.claude/memory/\` 互不干扰。处理本项目内容时读/写本目录。

## 定位

AOS 项目集的一员。项目集内各项目共同指向「**把不同专业的工作或事项工程化**」；本项目负责该目标在 **<待补>** 上的展开。${today} 建项。

## 现行内容

（待补）
`;

const FILES = [
  [path.join(DIR, 'CLAUDE.md'), PROJECT_CLAUDE_MD],
  [path.join(DIR, 'claude-memory', 'MEMORY.md'), MEMORY_INDEX],
  [path.join(DIR, 'claude-memory', name + '项目.md'), MAIN_MEMORY],
];

console.log('new-project —— 在项目集根目录新建独立项目\n');
console.log('  仓库根   : ' + REPO_ROOT);
console.log('  新目录   : ' + nn + '-' + name);
console.log('  编号来源 : 项目集内现有最大号 ' + (used.length ? Math.max(...used) : 0) + ' + 1\n');
console.log('将要建：');
for (const [f] of FILES) console.log('  ' + path.relative(REPO_ROOT, f));

if (DRY_RUN) {
  console.log('\n（--dry-run：未写入任何文件。）');
  process.exit(0);
}

for (const [f, content] of FILES) {
  fs.mkdirSync(path.dirname(f), { recursive: true });
  fs.writeFileSync(f, content, 'utf-8');
}

console.log('\n✅ 已建。\n');
console.log('还剩一件要人工做——到仓库根 PROJECTS.md 的「项目清单」加一行：\n');
console.log('  | ' + name + ' | `' + nn + '-' + name + '/` | 研究型 | `claude-memory/` | <一句话说明>。见 [`CLAUDE.md`](' + nn + '-' + name + '/CLAUDE.md) |\n');
console.log('建完可跑 node .ai-agent/tools/check-projects.js 复验。');
