---
name: 成书 EPUB 的 XML 修复
description: 2026-10-19 记录——Apple Books 报整页 XML 错的根因（table-inline.html 注释里的裸尖括号）与修法、管道新增的 EPUB 出厂体检，以及仍挂着的表图版管道问题
metadata:
  type: progress
---

# 成书 EPUB：XML 解析失败（2026-10-19 已修）

## 一 现象

用户把 `架构师-电子版.epub` 放进 Mac／iOS 的「图书」，**每一页都是满屏红框**：

> error on line 36 at column 11: Opening and ending tag mismatch: head line 12 and style

两个 EPUB（标准版、表格转图版）**同病**，各 **26 个 xhtml 无一通过** XML 解析。

## 二 根因

`成书/build/table-inline.html` 的 CSS 注释里写了 `<head>` 字面（落在生成后 xhtml 的**第 12 行**，与报错精确对上）。pandoc 用 `--include-in-header` 把该文件原样塞进每个 xhtml 的 `<style>`；而 **XHTML 按 XML 解析**（不按 HTML），注释里的 `<head>` 被当成起始标签 → `style` 未闭合即撞 `head` → 整本书解析失败。

**为什么此前一直没发现**：浏览器把 `<style>` 当原始文本（HTML 解析），WPS／FBReader／Calibre 也都不报；旧自检只数文件与表数，**从不解析 XML**。Apple Books 是唯一走严格 XML 的阅读器。

## 三 修法（已落库）

1. **改源头**：注释改写为不含尖括号的措辞，并在同一文件立规矩「此处严禁裸尖括号，非写不可用实体」。
2. **标准版重出**：`pandoc … --include-in-header=build/table-inline.html` 单跑第 6 步 → **3,885,212 B／26 xhtml／168 表／26 图**，`xml.etree` 解析 **26/26 通过**。
3. **表格转图版**：支线产物、表图未变，按同一处注释**就地补字重打包**（zip 内只替换 26 个 xhtml 的这一行；mimetype 仍为首件且 STORED）→ **17,576,801 B／194 图**，同样 26/26 通过。
4. **新增 `build/check-epub.py` ＋ `build.sh` 第 7 步**：出书后逐个 xhtml／opf／ncx 走 XML 解析，并查 mimetype 是否首件且未压缩；不过即 `exit 1`。表格转图版若在库则顺带体检，报红只提示不拦（build.sh 不重建它）。
5. **PDF 未动**：`table-inline.html` 只喂 EPUB 那条 pandoc 命令，typst 侧不读它。

## 四 教训与表图版管道

- **教训**：EPUB 属于 XML 文档，**能过 HTML 解析器不等于能过 XML 解析器**。凡"往 EPUB 里注 HTML／CSS"，注释里也不许出现裸 `<`。
- **表图版管道已跨平台化（2026-10-19 同日办）**：`build/make-table-images.mjs` 原先 `PANDOC`／`TYPST` 写死 Windows 路径（`C:\Users\HUAWEI\…`），换机即废。现改为 **环境变量（`PANDOC_PATH`／`TYPST_PATH`）→ PATH → 各平台常见位置** 依次解析；字体候选由 `Noto Serif SC／SimSun` 扩为再加 `Songti SC／STSong／Noto Serif CJK SC／Source Han Serif SC` 等（typst 取第一个装了的）。**实测**：单跑第1章（11 张表）2.5 秒出图，883×171 级 PNG、三列表框线与中文宋体正常；按其速率全书 168 张约 40 秒。
- **表图未重渲**：本轮只修补产物（表图仍是 Windows 那批），故两份 EPUB 的表图一致；日后要重出表图版，直接 `node build/make-table-images.mjs .. build build-tblimg` 再 pandoc 即可，无需再改脚本。
- 本条只关管道，**源 `.md` 零改动**；书稿内容与 PDF 均不受影响。
