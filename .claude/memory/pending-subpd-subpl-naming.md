---
name: pending-subpd-subpl-naming
description: 已决——子线目录名统一为 subpd，9 个目录已 git mv（2026-10-19）
metadata:
  node_type: memory
  type: project
  originSessionId: 5ff7b330-61c6-4f82-a69e-77b676f52e87
  modified: 2026-10-19T00:00:00.000Z
---

**2026-10-19 定并执行：采用 `subpd`。**

## 处置

- 9 个子线目录已 `git mv`：`10-pl4pleos-subpl-sysdev` → `10-pl4pleos-subpd-sysdev` 等（`10-pl4pleos` 4 个、`20-pl4eos` 5 个）。
- 文档侧 39 个文件、135 处相对链接本来写的就是 `subpd`，此次无需改动——**改目录是成本最低的解**。
- 记忆正文中的旧名与旧路径按「事实快照」处理，不作历史改写；现行导航以新目录为准。

## 原冲突（留档）

- 磁盘与 git 里曾只有 `subpl`；`subpd` 目录**从未存在于 git**。
- 39 个文档文件写 `subpd`，含根 `CLAUDE.md`、`README.md`、`AGENTS.md`、13 个现行规范／SKILL；其中约 135 处在相对链接里。
- 2026-09-17「三形态命名体系」（`4b1803c2`、`b491289a`）主动改成 `subpd`；同日 `27ce333d` 又改回 `subpl`，只动 3 份文件，改到一半停下。

相关：[[chain-form-three-tiers-naming]]、[[biz-chain-renumbering-2026-09-16]]、[[project-directory-migration-2026-10-19]]
