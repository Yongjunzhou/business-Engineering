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

**2026-10-19 开工核验**：`git ls-remote` 四端与本地一致——新仓 GitHub 与 Gitee 均为 `a66d7585`，旧仓 GitHub 与 Gitee 均为 `f79cbb37`（＝本地 `archive-master`）；`.git/config` 的远端映射、双推送地址、`master` 上游与 `pre-push` 钩子均与 `REPO-MAINTENANCE.md` 相符。新仓当前 3 个提交、1241 个文件；旧仓快照 5989 个文件，差出的 4750 个全在既定排除范围（`90-hold/`、`80-sessions/`、两个"旧版归档"、技能 `temp/`、`node_modules/`），未丢其他内容。本地 `gitee/master` 跟踪 ref 曾停在 `ac81fc85`（`origin` 双推送只刷新 `origin/master`），`git fetch gitee` 后与 `a66d7585` 齐平——此后核对 Gitee 状态须先 fetch 再比。

**2026-10-19 平台侧核验**：新仓 `business-engineering` 两端均为**公开**仓库（匿名 HTTP 200；GitHub 建于 08:03、Gitee 08:01，描述「业务工程化研究」，默认分支 `master`，GitHub 侧约 182 MB），公开树含 `.claude/memory/`（203 项）与教材子项目记忆（146 项），记忆正文随仓库公开；旧仓 `AOS-system-design` 两端均为**私有**（匿名 404／403，带凭证的 SSH 仍读到 `f79cbb37`，是私有而非删除）。

**待改（不越界）**：教材子项目记忆 `100-subprojects/01-系统工程研究/claude-memory/pending-出版前姓名合规与去标识化.md` 仍把"远端两个"记作旧仓 `AOS-system-design`，该条是现行状况表，已因拆分失真；改它须在该子项目内办。
