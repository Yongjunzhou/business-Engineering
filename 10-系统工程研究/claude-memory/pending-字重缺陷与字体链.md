---
name: pending-字重缺陷与字体链
description: 挂账——六件成品正文/标题均为最细字重（无真加粗），根因是可变字体；三条修法已备，2026-10-20 用户「先不动」
metadata:
  type: project
---

# 挂账 · 字重缺陷与字体链（未修）

> **状态**：2026-10-20 用户裁「先不动」。**风险**：现有六件成品（完整版三件＋赠阅版三件）的正文与标题都是**最细字重**，书里所有加粗标记在纸上看不出来——**印前必须重出一次**。

## 一、现象（实测，不是猜）

`架构师-打印版.pdf` 第 1–30 页内嵌字体名只有两种：

- `/NotoSerifSC-ExtraLight`（正文，宋体系）
- `/NotoSansSC-Thin`（标题与页眉，黑体系）

小样实测（`typst 0.15.1`，同一文档内 `#set text(weight: 400)` 与 `weight: 700`）：两次都编译出 `NotoSerifSC-ExtraLight`。即**字重轴没生效，全书没有真正的加粗**。

## 二、根因

本机装的是**可变字体**：

- `C:\Windows\Fonts\NotoSerifSC-VF.ttf`（25,129,160 B）
- `C:\Windows\Fonts\NotoSansSC-VF.ttf`（17,773,244 B）

typst 把它们固定到默认实例（ExtraLight／Thin），模板 `template/book.typ` 里 `#let SERIF = ("Noto Serif SC", "SimSun")` 的第一位就命中这个 VF，链上第二位 `SimSun` 永远轮不到。同理 `#let SANS = ("Noto Sans SC", "SimHei", "Microsoft YaHei")`。

## 三、另一处（无害但与同源）

表格转图（`build/make-table-images.mjs`）与表格模板的字体串里写着本机不存在的名字：`Songti SC`／`Noto Serif CJK SC`／`Source Han Serif SC`／`serif`——那串 `unknown font family` 警告即出在这里。命中的是链首的 `Noto Serif SC`（仍是 VF 的 ExtraLight）。

**本机 typst 可见的中文字体**（172 个家族中相关者）：`SimSun`／`SimHei`／`NSimSun`／`STSong`／`STZhongsong`／`STKaiti`／`STFangsong`／`KaiTi`／`FangSong`／`Microsoft YaHei`／`Microsoft JhengHei UI`／`HarmonyOS Sans SC`（Regular／Medium／Bold 三个静态字面）／`Noto Sans SC`／`Noto Serif SC`（均为 VF）。**没有** SimSun Bold、没有静态的思源宋／黑。

## 四、三条修法（已试小样，待选）

| 案 | 做法 | 得失 |
|---|---|---|
| **甲** | 正文 `SimSun`；强调 `#show strong` 改挂 `STZhongsong`（华文中宋，同族加重的中文老办法）；标题 `Microsoft YaHei` 700 | 全用本机现成字体、不下载；宋体正是中文书正体；**已出样张，层次看得出** |
| **乙** | 正文也换无衬线（`Microsoft YaHei` 或 `HarmonyOS Sans SC`，两者有真 Bold） | 加粗彻底生效，但整本书从「宋体思想著作」变「技术手册」 |
| **丙** | 装 `Noto Serif SC` 的 Regular＋Bold 静态字重（需联网下载），模板链不动 | 最接近原设计观感、加粗生效；但要下载并装字体，跨设备不可复现 |

## 五、改的时候动哪几处

1. `成书/template/book.typ`：`SERIF`／`SANS` 两个常量，按选的案子改；若走甲案再加一条 `#show strong: set text(font: ("STZhongsong", ...))`（该文件 L46 现为 `show strong: set text(weight: 700)`，注释「思源可变字体原生加粗」）。
2. `成书/build/make-table-images.mjs` 与表格 typ 模板里的字体串：收敛到本机确实有的名字。
3. 重出六件：`bash build.sh --tblimg` ＋ `bash build.sh --no-front --tblimg`；**后者会把 `build/` 中间件留在赠阅版状态**，跑完要用 `BOOK_EDITION=full` 重跑 preprocess＋pandoc＋fix-typ 复原（见 `封面题词.md` §六 末条）。

## 六、触发条件

出版社定下字体与开本后（届时可能整版重排，修法要按其要求重选），或用户说「改」。

## 七、旁证：为什么不只是"警告"

若只是字体名没命中，typst 会回退到下一位并照常出粗体；这次是**链首位命中了但字重轴失效**——两者后果不同：前者只丢日志，后者丢的是全书的强调语义。判断依据是 PDF 内嵌字体名与 `weight: 400/700` 的小样对照，可直接复算。
