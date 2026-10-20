---
name: project-directory-migration-2026-10-19
description: 目录重排——项目提升到顶层、主线降为 20-eos-engineering、AI 工具收进 .ai-agent（2026-10-19）；2026-10-20 收尾删除 20-eos-engineering/40-review
metadata:
  type: project
---

**2026-10-19 定并执行。** 仓库顶层从「主线 + `100-subprojects/`」改为**业务工程化项目集**：每个编号目录是一个独立项目，主线降为一个项目。

## 新顶层

```
00-candidate-businesses/  ← 原 100-subprojects/00；占 00 号，性质不是项目
10-系统工程研究/          ← 原 100-subprojects/01
11-AI部署研究/            ← 原 100-subprojects/02
12-健康研究报告/          ← 原 100-subprojects/03
13-现代思维工具研究/      ← 原 100-subprojects/04
14-投资工程研究/          ← 原 100-subprojects/05
20-eos-engineering/       ← 原顶层 00-generalspec/10-pl4pleos/20-pl4eos/30-eos/40-review
.ai-agent/                ← tools/（原 .tools）、scripts/（原 .scripts）、work/（原 .work-ch8）
.claude/                  ← 保留：Claude Code 的固定发现点（设置/技能/记忆）
```

## 关键约定

- **`.claude/` 与 `.git/` 不迁入 `.ai-agent/`**：前者是 Claude Code 的项目发现点，后者是仓库根定义。
- `.agents/skills` 与 `.claude/skills` 完全重复（仅 `.claude` 多 `next-chapter`），已删除 `.agents/`。
- 项目工具改名：`new-subproject.js` → `new-project.js`、`check-subprojects.js` → `check-projects.js`；四个脚本的根路径计算已从 `..` 改为 `../..`。
- 子线目录统一为 `subpd`（见 [[pending-subpd-subpl-naming]]）。
- 主线工程使用仓库根 `.claude/memory/`；各独立项目使用自己的 `claude-memory/`。

## 验证

- 相对链接回归检查：迁移前基线 283 处断链，迁移后仍 283 处，**新增 0 处**（15 处断链已按旧→新映射自动修复）。
- `node .ai-agent/tools/check-projects.js`：6 个条目全齐。
- `node .ai-agent/tools/next-chapter.js`：章状态与工作目录正常。

## 2026-10-20 收尾：删除 `20-eos-engineering/40-review/`

用户令「都不要了」，整目录 `git rm`，共 17 个文件：三份概念笔记的旧载体（`工程概念精讲笔记.html`／`评审概念体系精讲-从Review定义到需求管理.html`／`需求工程概念精讲笔记.pdf`）、`figures/` 九张 SVG 源、`需求开发程序` 与 `需求管理程序`（md＋pdf）、初建时的占位 README。

- **内容不丢**：三份笔记的现行维护版都在 `10-系统工程研究/00-系统工程相关研究报告/`——工程概念＝05 号、评审概念＝03 号、需求工程＝02 号。两份程序文件仓库内无副本（用户裁决一并删除，不迁移）。
- **引用同步**：根 `CLAUDE.md`、`README.md`、`AGENTS.md`、`20-eos-engineering/CLAUDE.md` 四处目录树删行；06 号报告附录 A 的两条 html 链接改指 05／03 号；本记忆 [[architecture-fundamentals-document-v2]] 的来源指针改指四份研究报告。
- **未动**：`02-eos-sysdev-review.md` 两处 `40-review/不具名-20260815-…` 存档路径（迁移前即已断链，属历史归档记录）；各记忆的历史日志保留旧称。

## 未做（下一步候选）

- 教材书内部重排（`00-写作权威/`、`10-正文/`、`20-工具/`、`90-成书/`、`91-封面/`）——涉及 build 脚本，单列一步。
- 研究库内部按「本库报告／外部标准／讲读笔记／素材」分栏。
- 283 处既有断链的逐项清理（本次只保证不新增）。
