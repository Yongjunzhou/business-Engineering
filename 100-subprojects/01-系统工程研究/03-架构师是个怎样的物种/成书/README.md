# 成书（教材书 → EPUB + PDF 双轨构建）

> **★ 2026-10-11 已重跑，产物为现行版。** 此前那轮"不可交付快照"的断链**已修复**：
>
> 1. **管道断链已修**——`preprocess.mjs` 会自重建 `manifest.txt`，重跑后为 **22 文件**（含 `18-第18章`），`main.typ` L55／L56 include 的两个文件均已生成。
> 2. **补渲了 3 张从未成功渲染的 mermaid 图**（`ch04-fig02`／`ch05-fig01`／`ch18-fig01`）——根因是 `build/puppeteer.json` 的 `executablePath` 指向 **Windows Chrome 路径**，在 macOS 上渲染必然失败；而 `build.sh` 第 2 步判据是"`figs/*.png` 非空则跳过"，**一张图都没渲出来也会被判为已渲**，于是缺失被掩盖了很久。**换机器重建前请先改 `puppeteer.json` 的 `executablePath`**（或在 macOS 上用一份临时配置）。
> 3. **全库 2011 语义清除已进入产物**——重跑后 `build/*.book.md` 与 EPUB 的内容扫描（`具身化｜架构构成物｜一层落地｜翻译成系统结构｜那组决定｜设计准则｜演进准则｜定演化原则｜基本元素`）**真残留 0 处**（仅存的命中全在变迁表／废止声明／术语注等护栏位）。
>
> **重跑命令**：`bash build.sh`（增量，图已存在则跳过）／`bash build.sh --rerender`（强制重渲全部 mermaid）。
> **★ 2026-10-19 重建（书侧定稿后首次）**：产物＝打印版 **10,965,402 B／1,047 页**、电子版 **3,876,663 B**（图 26 张全渲、蛇形图 1-5 重建）。同批修了两处**管道级的病**：
>
> 1. **中文引号开合全错**（老毛病，不是本次引入）——`pandoc` 的 smart 引号按"前一字符是否空白"判开合，而中文引号紧贴汉字，于是**几乎全判成闭引号**：修复前 `typ` 里 `”` 9,023 个 vs `“` 27 个，印出来是「回答的是**”**这一大类…」。**修法**：`build/preprocess.mjs` 增 `fixCjkQuotes()`——在预处理阶段按阅读顺序把 ASCII `"` 成对换成 `“`／`”`（跳过围栏代码与行内代码），`build.sh` 两处 pandoc 一律改 `-f markdown-smart`，不让它再改一遍。修复后 19 个文件共换 **10,290** 处，`“` 6,138／`”` 6,602，逐页复核正常。
> 2. **蛇形图渲染在非 Windows 机上必挂**——`build/render-fig05-snake.cjs` 把 Windows Chrome 路径写死，macOS 上 `build.sh` 虽已生成 `.puppeteer.local.json` 也不读，第 2.5 步直接抛错（且被 `| tail` 吞掉退出码）。**修法**：改成 `CHROME_PATH → .puppeteer.local.json → puppeteer.json → 常见路径` 依次解析，跨平台可用。
>
> **仍待核两件**（未动）：① **图 1-5 覆盖**（`ch01-fig05.png` 被蛇形占用，§1.6.4 阻抗生成树仍无处渲，两者取一须裁）；② **字体回退**（模板 `SERIF/SANS` 请求的是 SimSun／SimHei／微软雅黑，macOS 上缺失、typst 走回退，中文显示正常但非印刷级字形——要正解须在 `template/book.typ` 补思源或 macOS 字体名）。
> **仓库体积提醒**：PDF/EPUB 每次重建都进 git（`.git` 已 425 MB，历史里十几份 10 MB 的 PDF 快照）。若要瘦身，得另走历史处理，不是删文件能解决的。
> **★ 2026-10-19 EPUB 列宽同步（补）**：`fix-typ.mjs` 只管 PDF（typst）；EPUB 的列宽来自**表头分隔行的横线长度**（pandoc pipe 表规则），源文一律 `---`，于是 `<col style="width:25%">` 仍是等分。`preprocess.mjs` 增 `fitTableDashes()`——按各列内容最大视觉宽重写分隔行横线（长列封顶 48、0.75 次幂、最少 3 条），**一次同时管住 EPUB 与 PDF**（EPUB 实测 ch5 由 33/33/33 变 **34/18/47**）。
> **EPUB 终态自检（2026-10-19）**：`application/epub+zip` 首件正确；**25 个 xhtml**（封面＋扉页＋nav＋22 正文）；**171 张表**（与 PDF 侧 171 张一一对上）；**27 张图**（26 图＋封面）、**悬空引用 0**；XML 全部可解析；后记在 `ch021`、附录 `ch022`；**全书再无"审视清单"工作件**。
> **★ 2026-10-19 表格列宽改为按内容（用户令「列宽要照顾各列内容」）**：pandoc 输出的表格一律等分（`columns: 4` 或 `(33.33%, 33.33%, 33.33%)`），"①""提出者"这类窄列与整段定义平分版心。`build/fix-typ.mjs` 增 `fitTableColumns()`——按每列内容的最大视觉宽（CJK 记 2、西文记 1）估权重，0.75 次幂压缩长列、**9% 下限**，再归一成百分比；下限用**迭代回缩**（缺口摊给其余列），不回冲窄列。全书 **186 张表**全部改毕，最窄列 9%、最宽列按内容。个别 9 列宽表（如各章"概念一致性审视清单"）在 A5 上仍不可读，故工作件另按下一条排除。
>
> **★ 2026-10-19 发现并修两处"书不是它该有的样子"（用户问表格时查出）**：
> ① **PDF 里从来没有后记**——`main.typ` 的 include 清单停在"第1~18章 → 附录"，2026-10-17 重写落库的《后记·两间会议室，两年后》**从未被 PDF 收入**（EPUB 有、PDF 没有，两轨不一致）。已把 `#include "build/00-后记.typ"` 补在第 18 章与附录之间（PDF 现 **909 页**，后记占 pp.832–842）。
> ② **后记位置曾被内部清单顶替**——`preprocess.mjs` 用前缀 `00-后记` 找源文件，同目录的《00-后记-概念一致性审视清单.md》先被命中，于是 EPUB 里"后记"装的是 9 列审计表（也是上面那张崩版宽表的来路）。`EXCLUDE_RE` 已加 `审视清单\.md$` 与 `^00-ch`，工作件一律不进 MANIFEST。
> **★ 2026-10-19 版式两项改定（用户裁）**：`template/book.typ` 的 `set par(...)` 由 `leading: 1.6em, spacing: 0.3em` 改为 **`leading: 1.0em, spacing: 1.2em`**——
> ① **段间必须明显松于段内**：原 `spacing: 0.3em` 比行距还紧，段落粘连（1.2em 正是 typst 默认值，模板把它压到 0.3em 才是异常）；
> ② **段内行距收紧一档**：`1.6em → 1.0em`（1.6em 偏松，读数时"换行没换气"）。
> **产物随之重出**：页数 0.3em 间距时 **1,047 页** → 1.2em 间距且 1.6em 行距时 **1,122 页** → 本次定型（1.0em 行距／1.2em 段间）**922 页**；打印版 **10,838,053 B／909 页**（含后记）、电子版 **3,874,344 B**。段首两字缩进、两端对齐、五号字均未动。

`100-subprojects/01-系统工程研究/03-架构师是个怎样的物种/` 的 Markdown 教材书《架构师是个怎样的物种？——从工程师到架构师》转为双轨成品的构建管道。**源 `.md` 零改动**，全部构建产物在本目录。

## 产物

| 文件 | 说明 |
|---|---|
| `架构师-打印版.pdf` | A5 打印稿（实体书版式：封面/版权页/目录/页眉页码/正文宋体） |
| `架构师-电子版.epub` | 电子书（微信读书 / Apple Books / 多看等，重排版式） |

## 重建

```bash
bash build.sh        # 增量：mermaid 图已存在则跳过渲染
bash build.sh --rerender   # 强制重渲全部 19 个 mermaid 图
```

一键产出双格式。命令内部自行设置工具 PATH，无需额外环境变量。

## 目录结构

```
成书/
  build.sh             # 单入口（预处理 → 图 → 封面 → pandoc→typst → typst → pandoc→epub）
  main.typ             # PDF 入口：封面/版权/序前/目录/章节/封底组装
  template/book.typ    # A5 版式模板（页面/字体/标题/表格/引用/ASCII 盒/图）
  build/
    preprocess.mjs     # 清洗：剔「版本变更记录」/ mermaid 提取 / .unlisted 归一化
    render-fig05-snake.cjs  # 图1-5 蛇形直渲（mermaid 画不出，见「关键设计决策」）
    fix-typ.mjs        # 修补 pandoc→typst：剥重复 label / 按图尺寸注入适配宽度
    crop-cover.ps1     # 封面裁书脊（60px）→ 前封 800×1132
    metadata.yaml      # EPUB 元数据（书名/作者/语言）
    assets/book.css    # EPUB 版式
    assets/ch01-fig05-snake.svg  # 图1-5 蛇形源（改版式改此文件 + --rerender）
    puppeteer.json     # mmdc 复用本机 Chrome（免下载 Chromium）
    mermaid.json       # mmdc 中文标签字体
    *.book.md / *.typ  # 中间产物（预处理后的正文 / pandoc 转换结果）
    .mmd/ figs/        # mermaid 源 / 渲染后的 PNG
```

## 依赖

- **pandoc**（markdown→typst / markdown→epub3）
- **typst**（typst compile）
- **node/npx + @mermaid-js/mermaid-cli**（mermaid 图渲染，复用本机 Chrome）
- **calibre**（EPUB 校验/精修，可选）

## 关键设计决策

- **图用 PNG 而非 SVG**：mermaid 的 SVG 含 `<foreignObject>`，typst 无法渲染（中文标签会消失）。PNG 为 3× 栅格，A5 打印清晰度 >600dpi。
- **图1-5 两列蛇形（手绘 SVG 特例）**：全书认知链 17 章，单列竖排时方块在 A5 版心只能压到 ~5pt 字；mermaid 11.16 的子图 `direction` 指令失效又画不出两列蛇形 → 改用**手绘 SVG**（`build/assets/ch01-fig05-snake.svg`，第1~8章左列、9~17章右列、底部回绕箭头）经无头 Chrome 直渲（步骤 2.5，`render-fig05-snake.cjs`）。md 源已是显式 `![图 1-5](figs/ch01-fig05.png)` 引用；改版式改 SVG + `--rerender`。蛇形满版宽 ~110×150mm、字 ~7pt，可读。**待核**：ch1 第 5 个 mermaid 块（§1.6.4 阻抗生成树）与蛇形共用 `ch01-fig05.png` 这一文件名，蛇形渲染会覆盖前者——两者取一须裁（2026-09-23 登记）。
- **目录自动生成**：PDF 用 typst `outline()`、EPUB 用 pandoc `--toc`。章首·误解现场与章末件（本章问题/判据/练习等）通过 `{.unlisted}` → `outlined:false` 排除，与 `00-目录.md` 的三级结构一致。
- **剔「版本变更记录」**：每文件尾的写作元数据表不入书；章末参考文献保留。
- **图片尺寸按 viewBox 注入**：mermaid 图宽高差异极大（1841×94 到 220×734），`fix-typ.mjs` 按比例适配 A5 版心（宽≤110mm、高≤150mm）防溢出。

## 注意

- `puppeteer.json` 里是本机 Chrome 路径；若换机器，改该文件或装 puppeteer 自带 Chromium。
- 渲染好的 `figs/*.png` 已随构建提交，拉取后无需重渲（除非图源变化）。
- 生成 PDF/EPUB 是构建产物，随提交保留（书籍成品即版本快照）。
