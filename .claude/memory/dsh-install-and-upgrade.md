---
name: dsh-install-and-upgrade
description: DSH（DeepSeek Harness）在 Windows 与 macOS 的安装位置、版本与升级要点；含 npm allow-scripts 坑、双形态共用 ~/.dsh、VS Code 扩展取 PATH 上的 dsh、macOS 的 v3→v4 会话行为
metadata:
  type: project
---

**2026-11-27 完成一次升级：Node 24.15.0→24.22.3，CLI 0.1.5-rc.2→0.2.2-rc.5，桌面版 0.2.0-rc.2→0.2.2-rc.5，pnpm 11.7.0。**

**三处安装**

- CLI：`C:\Users\HUAWEI\AppData\Roaming\npm\node_modules\@deepseek-ai\dsh`；命令 shim 在 `...\Roaming\npm\dsh{,.cmd,.ps1}`，该目录已在用户 PATH。
- 桌面版：`C:\Users\HUAWEI\AppData\Local\Programs\DeepSeek Harness`；应用版本看 `resources\runtime\primary-runtime\runtime.json` 的 `desktopVersion`——目录里的 `version` 文件是 Electron 版本，不是 DSH 版本。
- 数据：`C:\Users\HUAWEI\.dsh`，含会话、凭据、`settings.yaml`、`profiles/web`、`profiles/desktop`、`storages`；CLI 与桌面版共用这一份。

**升级要点**

- 版本源：npm `@deepseek-ai/dsh` 的 `latest` 与 `next` 都指向 RC；桌面 feed 是 `https://download.deepseek.com/dsh-desk/feeds/win-x64/{nightly,stable}.yml`。2026-11-27 两者同为 0.2.2-rc.5。
- npm 11.19 起默认拦安装脚本：`npm i -g @deepseek-ai/dsh@<ver>` 必须带 `--allow-scripts=@deepseek-ai/dsh-subprocess-local,koffi,node-pty,protobufjs`，否则 koffi／node-pty 的原生件不落盘。本次按此重装。
- Node 门槛：0.2.2-rc.5 要 `>=24.9.0`；0.2.3-alpha.2 要 `24.22.3+` 或 `26.13.1+`。本机已到 24.22.3，ABI 仍为 137（同大版本，原生件不必重编）。
- VS Code 扩展 `vithrive.deepseek-harness-vscode` 先取 PATH 上的 `dsh`，找不到才用桌面版内置 CLI；故升 npm 全局版即改变面板所用版本。
- `~/.dsh/profiles/node_modules` 下是指向全局安装的 junction；升级后留下 51 条断链（指向 0.2.2 已移除的包），无害——`--dump-config` 与 `dsh web` 启动均通过，尚未清理。

**备份与回滚**

- 备份：`C:\Users\HUAWEI\.dsh.bak-20261127-0742-clean`（6053 文件、1.396 GB；robocopy `/XJ` 跳过 482 个 junction）。
- CLI 回滚：`npm i -g @deepseek-ai/dsh@0.1.5-rc.2`；数据回滚用上述备份恢复 `~/.dsh`。
- 安装包留在 `C:\Users\HUAWEI\AppData\Local\Temp\dsh-upgrade-20261127\`（Node MSI、桌面版 EXE）。

**验证记录**

- `dsh --version` = 0.2.2-rc.5；`npm ls -g` 中只剩这一版。
- `dsh --profile web --dump-config` 退出 0（1303 行，四个配套插件在组合树中）。
- `dsh web --no-open --port 3081` 正常监听并返回 401（0.2.x 的浏览器认证围墙，属预期）。
- 最近会话 `session.v3.jsonl.zstd` 用 Node 的 zstd 解压后 51 行全部可解析；`storages/workspace.json` 仍是 unit version 2。

**macOS 侧（2026-11-28）**

- 只有 CLI 一处安装：`/opt/homebrew/lib/node_modules/@deepseek-ai/dsh`（Homebrew 的 Node 全局），命令在 `/opt/homebrew/bin/dsh`；Node v25.9.0、npm 11.12.1。npm 低于 11.19，不受 `--allow-scripts` 拦截；已确认 `koffi`、`node-pty` 在包内。
- 由 0.1.6-alpha.2 升到 0.2.2-rc.5，`dsh --version` 与 `npm ls -g` 一致；备份在 `~/dsh-backup-20261128/`（`settings.yaml`、`profiles/` 去 `node_modules`、`storages/`，16MB；372MB 会话未整份备份，因 v3 原文不改写）。
- 使用形态是终端 `dsh web` ＋ Edge 直连，不走 VS Code 面板；面板要用时需在提示里「粘贴认证链接」，因终端托管的实例扩展无法静默取 token。
- 旧 v3 会话在 `session/list` 里带 `formatStatus: "migration-required"`；`session/page` 可直接读历史且不落新文件，继续会话、产生首次写入时才生成 `session.v4.jsonl.zstd`。回滚到 0.1.6 后，0.2 期间新建的 v4 会话不可见，数据仍在磁盘。
- 回滚：`npm install -g @deepseek-ai/dsh@0.1.6-alpha.2`。

**关联**：[[env-dsh-pwsh-sandbox-acl]]
