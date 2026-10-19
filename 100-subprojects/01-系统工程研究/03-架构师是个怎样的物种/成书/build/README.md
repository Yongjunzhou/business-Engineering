# build/ —— 中间产物与构建配置

> **⚠️ 本目录是生成件，不要手改。** 正确修法是重跑 `bash ../build.sh`（或按 `../build.sh` 的分步命令逐步走）。
>
> **断链已修复（此处曾登记 2026-10-11 的旧快照）**：`preprocess.mjs` 会自动重建 `manifest.txt`，当前为 **23 文件**（含 `18-第18章`），`main.typ` 的 include 清单与盘上文件一一对得上；PDF/EPUB 按这份清单全量重建。
>
> **改 `.typ` 的两处仍在 `fix-typ.mjs`（每次重建自动生效，别手改产物）**：
> 1. `unwrapTableFigures()`——拆掉 pandoc 给每张表套的 `#figure(…, kind: table)` 外壳（typst 的 figure 不跨页，长表会溢出丢内容）；
> 2. 图宽注入——**渲染自然尺寸封顶**（`px宽×0.75÷3`，`mmdc -s 3` 的 3 倍像素）；纯图号题注另注入 `numbering: none`，免与 typst 自动编号重号。
>
> 完整口径与理由见上级 [`../README.md`](../README.md) §关键设计决策末段（2026-10-19 两条）。

## 目录内容

| 文件 | 作用 |
|---|---|
| `preprocess.mjs` | 清洗：剔「版本变更记录」／mermaid 提取／`.unlisted` 归一化 |
| `render-fig05-snake.cjs` | 图1-5 蛇形直渲（mermaid 画不出，见上级 README「关键设计决策」） |
| `fix-typ.mjs` | 修补 pandoc→typst：剥重复 label／注入图宽（自然尺寸封顶）／图题关自动编号／解包表格 figure／列宽两档口径 |
| `crop-cover.ps1` | 封面裁书脊 → 前封 800×1132 |
| `metadata.yaml` | EPUB 元数据（书名／作者／语言） |
| `assets/book.css` | EPUB 版式 |
| `assets/ch01-fig05-snake.svg` | 图1-5 蛇形源（改版式改此文件 + `--rerender`） |
| `puppeteer.json` / `mermaid.json` | mmdc 复用本机 Chrome ／ 中文标签字体 |
| `manifest.txt` | 构建清单（`preprocess.mjs` 自重建，现为 23 件，`build.sh` 逐行读取） |
| `*.book.md` / `*.typ` | 中间产物（预处理后的正文／pandoc 转换结果） |
| `.mmd/` `figs/` | mermaid 源／渲染后的 PNG |

---

*2026-10-11 的断链诊断见 `claude-memory/架构语义立场表-ch10至ch18.md` §15.2／§17.10；该断链已在后续重建中修复，现行状态见文首。*
