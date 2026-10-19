---
name: project-directory-migration-2026-10-19
description: 目录重排——项目提升到顶层、主线降为 10-eos-engineering、AI 工具收进 .ai-agent（2026-10-19）
metadata:
  type: project
---

**2026-10-19 定并执行。** 仓库顶层从「主线 + `100-subprojects/`」改为**业务工程化项目集**：每个编号目录是一个独立项目，主线降为一个项目。

## 新顶层

```
00-系统工程研究/       ← 原 100-subprojects/01
01-AI部署研究/         ← 原 100-subprojects/02
02-健康研究报告/       ← 原 03
03-现代思维工具研究/   ← 原 04
04-投资工程研究/       ← 原 05
10-eos-engineering/    ← 原顶层 00-generalspec/10-pl4pleos/20-pl4eos/30-eos/40-review
_topic-research/       ← 原 100-subprojects/00；不占项目编号
.ai-agent/             ← tools/（原 .tools）、scripts/（原 .scripts）、work/（原 .work-ch8）
.claude/               ← 保留：Claude Code 的固定发现点（设置/技能/记忆）
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

## 未做（下一步候选）

- 教材书内部重排（`00-写作权威/`、`10-正文/`、`20-工具/`、`90-成书/`、`91-封面/`）——涉及 build 脚本，单列一步。
- 研究库内部按「本库报告／外部标准／讲读笔记／素材」分栏。
- 283 处既有断链的逐项清理（本次只保证不新增）。
