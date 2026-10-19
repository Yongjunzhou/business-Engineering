---
name: repo-split-business-engineering
description: 仓库拆分：新仓 business-engineering（当前版本单提交基线）＋旧仓 AOS-system-design 转私有历史归档（2026-10-19）
metadata:
  type: project
---

**2026-10-19 定并执行**。远端由单仓改为两仓：

- **新仓 `business-engineering`**（Gitee `mickeychow` ／ GitHub `Yongjunzhou`）：当前版本基线，单提交 `d4edb3dd`，1239 个文件、约 244 MB；默认分支 `master`。
- **旧仓 `AOS-system-design`**：不改名、冻结、转私有，保留全部 2264 条提交，以及 `90-hold/`、`80-sessions/`、两个"旧版归档"目录。

本地 `E:\mywork\AOS`：`master` = 新仓基线；`archive-master` = 旧仓 `f79cbb37`；远端 `origin`／`gitee` 指向新仓，`archive-github`／`archive-gitee` 指向旧仓。

移出仓库的内容留在 `E:\mywork\AOS-移出仓外-20261019\`；`.tools/md2pdf/node_modules` 不再跟踪，由 `npm install` 重建。治理文档中指向 `90-hold/` 的三处归档说明已改指历史仓；`CLAUDE.md`／`AGENTS.md`／`README.md` 的目录树已删去 `90-hold/`、`80-sessions/` 两行。
