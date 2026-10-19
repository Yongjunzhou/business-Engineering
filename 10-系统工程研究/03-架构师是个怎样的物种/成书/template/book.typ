// book.typ — 《架构师是个怎样的物种？》A5 书模板
//
// 由 pandoc（markdown→typst）产出的各章 .typ 被 #include 进来，
// 本模板负责全部版式：A5 页面/页眉页脚/字体/标题/表格/引用/ASCII 盒/图。
// 图宽由 build/fix-typ.mjs 按 viewBox 注入（适配 A5 版心，防溢出）。

#let accent = rgb("#A63D2F")
#let SERIF = ("Noto Serif SC", "SimSun")
#let SANS = ("Noto Sans SC", "SimHei", "Microsoft YaHei")

#let book(book-title: "", body) = {
  set document(title: book-title)

  set page(
    paper: "a5",                                  // 148×210mm
    margin: (x: 19mm, top: 18mm, bottom: 20mm),   // 版心 110×172mm
    header: context {
      // 页眉 = 当前页所属章名（最近的前置一级标题；每章起新页，按页码判定）；封面页（第1页）不显示
      if counter(page).get().first() != 1 {
        let cur = here().page()
        let ch = query(heading.where(level: 1)).rev().find(h => h.location().page() <= cur)
        if ch != none {
          set text(size: 8pt, font: SANS, fill: luma(140))
          align(center)[#ch.body]
        }
      }
    },
    footer: context {
      if counter(page).get().first() != 1 {
        set text(size: 9pt, font: SANS)
        align(center)[#counter(page).display()]
      }
    },
  )

  // 中文正文：思源宋体、五号（10.5pt）、两端对齐、1.6 倍行距、段首两字缩进、段间留白
  // 行距 1.0em / 段间距 1.2em：段间必须明显松于段内行距。原为 leading 1.6em（偏松）、spacing 0.3em（比行距还紧、段落粘连）——2026-10-19 用户裁「段间要比段内松」「段内行距再小一些」后改定
  // ★ 2026-10-19 用户裁「每一节的第一段的首行没有缩进」：typst 的 first-line-indent 默认只管"块内第二个及以后的段落"，标题后的首段不缩进；改 all: true，标题后首段同缩两字
  set text(font: SERIF, size: 10.5pt, lang: "zh", region: "cn")
  set par(justify: true, leading: 1.0em, spacing: 1.2em, first-line-indent: (amount: 2em, all: true))
  set heading(numbering: none)                     // 编号已内嵌在标题文本（范式丙）
  show list: set par(first-line-indent: 0em)       // 列表段不缩进
  show enum: set par(first-line-indent: 0em)       // 有序列表段不缩进
  show quote: set par(first-line-indent: 0em)      // 引用块不缩进

  show strong: set text(weight: 700)               // 思源可变字体原生加粗

  // 标题：思源黑体，按层级缩放；章级起新页
  show heading.where(level: 1): it => pagebreak(weak: true) + it
  show heading.where(level: 1): set text(font: SANS, size: 20pt, weight: 700)
  show heading.where(level: 2): set text(font: SANS, size: 14pt, weight: 700)
  show heading.where(level: 3): set text(font: SANS, size: 12pt, weight: 700)
  show heading.where(level: 4): set text(font: SANS, size: 10.5pt, weight: 700)

  // ★ 2026-10-19 用户裁「节标题行与其首段首行间距过小」：标题上松下紧——上方留出与上文的分界、下方留足与首段的一口气
  // （typst 默认 heading 间距约 0.6em/0.4em，A5 上节题与正文贴得太近）
  show heading.where(level: 1): set block(above: 0em, below: 1.2em)
  show heading.where(level: 2): set block(above: 1.9em, below: 1.0em)
  show heading.where(level: 3): set block(above: 1.6em, below: 1.0em)
  show heading.where(level: 4): set block(above: 1.2em, below: .8em)

  // 引用块（章首导语 + 概念卡）：朱红左竖线
  show quote: it => block(
    width: 100%,
    stroke: (left: 2pt + accent),
    inset: (left: 1em, top: .3em, bottom: .3em),
    it,
  )

  // 表格：9pt 小字防溢出；列宽/对齐沿用 pandoc 默认（auto），整体居中由 figure 负责
  // ★ 2026-10-19：表内开英文断字（附录 A 术语表、附录 D 文献表的英文术语列要靠它——
  // 一行 "requirements engineering" 不断词就得吃掉 20% 版心）。正文仍按中文排，不受影响。
  show table: set text(size: 9pt, hyphenate: true, lang: "en")
  show table: set par(first-line-indent: 0em, justify: true, linebreaks: "simple")
  show table: set par(first-line-indent: 0em)   // 表内不缩进（first-line-indent all:true 会带进来）
  show table.header: set text(weight: 700)
  show table.cell: set block(inset: (x: 2pt, y: 1.5pt))

  // 裸围栏 ASCII 概念档案：NSimSun 保证 box-drawing（┌─│┐）与 ASCII 同格宽对齐
  show raw: set text(font: ("NSimSun", "SimSun", "DejaVu Sans Mono"), size: 8.5pt)
  show raw: set block(fill: none, inset: 0pt, radius: 0pt, stroke: none)

  // 图：居中；宽度由 fix-typ.mjs 注入
  show figure: it => align(center, it)
  show figure.caption: set text(size: 9pt, fill: luma(120))
  show figure.caption: set par(first-line-indent: 0em)

  body
}
