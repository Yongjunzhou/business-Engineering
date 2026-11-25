#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""产品数据线的文风量尺（段・句・破折号・加粗・括号与两条可扫的忌）

用途：规程 4.2 四道机械关之关一的那一半——题面与列名有两只形式关脚本，散文层没有量具。
     本脚本补这一半：量出来的四个数进同号过程记录件的「题面与表达清单」与覆盖表。

口径（2026-11-25 用户裁：段长只守 200，段中位与短段占比不设、不报）
- 量什么：只量散文段——按空行切段，一行一段。豁免七类：标题行、表格行、围栏内、引用块、
  清单行、章前件（**…**： 型标签行）、版本记录段（行首作 **版本**：／版本：／v数字.数字（ 三种，
  与「更早的版本段移出」那一行）。版本记录是查着看的，不属顺着读的正文。
  判据：读者是顺着读还是查着看，只算顺着读的那部分。
- 节级豁免（口径 v4，2026-11-25 自定）：「## 修订记录／# 修订记录」一整节（含其下各小节）不进段池。
  理由同前一条——那一节是查着看的；且行首式的认法认不全（**判留 14 条**、**未编版·…**、**一、…**
  这类记录条目屡被报超长）。行首式仍留着，管那些把记录写在别处的件。
- 读数单位：汉字 [\\u4e00-\\u9fff]；编号、标点、拉丁字母与数字不计。
- 句界：。！？ 三样；分号与冒号不算句界。
- 段的判据只有一条硬线：段 >200 汉字须 0，超出才拆。段中位与短段占比不设线、不报数；
  段分不分只看一件事是不是被拆成了两段（《风格参考》§6.20 的一段一意）。
- 其余三数：句中位 ≤24（《风格参考》§6.12）、破折号密度 ≤10‰、加粗 ≤6 块/千字。
- 两条可扫的忌：元话语词表命中；括号里带句读（括号装内容）。
- 段 >150 只记数，不设限；拆段的唯一理由是段装了两件事，不是段长越线。

用法：`python 00-文风-量尺.py <文件> [<文件> …]`；有红线被破则退出码 1。
"""
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HAN = re.compile(r"[\u4e00-\u9fff]")
SENT = re.compile(r"[。！？]")
META = ["一句：", "本轮", "★", "必须点破", "这就", "只说一点", "先立一句", "一句话说透"]

# 判据：段只守 200 硬线，段中位与短段占比不设线（2026-11-25 用户裁：「每段不超过 200 就 ok 了，
# 不需要设定段中位」「也不需要报」）；句中位 ≤24、加粗 ≤6 取《风格参考》§6.12；
# 段 >150 只记数、破折号 ≤10‰ 取教材侧 00-阈值.py；段的一意判据见 §6.20。
L_SENT_MED, L_BOLD = 24, 6.0
L_PARA_HARD, L_PARA_NOTE, L_DASH = 200, 150, 10.0


def han(s):
    return len(HAN.findall(s))


def prose_lines(text):
    """返回 [(行号, 段落文本)]，只含散文段。"""
    out, fence, in_record, record_level = [], False, False, 0
    for i, raw in enumerate(text.split("\n"), 1):
        s = raw.strip()
        if s.startswith("```"):
            fence = not fence
            continue
        if fence or not s:
            continue
        if s.startswith("#"):
            # 节级豁免：「修订记录」一节整节不量（含它下面各小节），到下一个同级或更高级标题为止。
            m = re.match(r"^(#{1,6})\s+(.*)$", s)
            if m:
                level, title = len(m.group(1)), m.group(2)
                if "修订记录" in title:
                    record_level = level
                    in_record = True
                elif in_record and level <= record_level:
                    in_record, record_level = False, 0
            continue
        if in_record:
            continue
        if s.startswith("|") or s.startswith(">"):
            continue
        if re.match(r"^([-*+]|\d+[.)])\s", s):
            continue
        if re.match(r"^\*\*[^*]{1,12}\*\*：", s):      # 章前件：**…**：标签行
            continue
        if (s.startswith("**版本**：") or s.startswith("版本：")
                or re.match(r"^v\d+\.\d+（", s) or s.startswith("更早的版本段移出")
                or re.match(r"^\*\*v\d+\.\d+", s)):
            continue
        out.append((i, s))
    return out


def brackets(s):
    """返回 (括号对数, 嵌套括号数, 括号内含句读的对数)。"""
    pairs = nest = inner_punct = 0
    depth = 0
    buf = []
    for ch in s:
        if ch in "（(":
            depth += 1
            if depth > 1:
                nest += 1
            if depth == 1:
                buf = []
            pairs += 1 if depth == 1 else 0
        elif ch in "）)":
            if depth == 1 and any(c in "。，；！？" for c in buf):
                inner_punct += 1
            depth = max(0, depth - 1)
        elif depth >= 1:
            buf.append(ch)
    return pairs, nest, inner_punct


def dash_count(s):
    n = s.count("——")
    return n + (s.replace("——", "").count("—"))


def measure(path):
    text = open(path, encoding="utf-8").read()
    lines = prose_lines(text)
    paras = [(ln, han(s)) for ln, s in lines]
    total = sum(h for _, h in paras)
    if not paras or total == 0:
        return None
    sents = []
    dash = bold = pair = nest = inp = meta = 0
    long_paras = []
    for ln, s in lines:
        for piece in SENT.split(s):
            h = han(piece)
            if h:
                sents.append((ln, h))
        dash += dash_count(s)
        bold += s.count("**") // 2
        p, n, ip = brackets(s)
        pair += p
        nest += n
        inp += ip
        for w in META:
            meta += s.count(w)
        long_paras.append((ln, han(s), s))
    sents_sorted = sorted(h for _, h in sents)
    med = lambda a: a[len(a) // 2] if len(a) % 2 else (a[len(a) // 2 - 1] + a[len(a) // 2]) / 2
    return {
        "path": path,
        "paras": len(paras),
        "total": total,
        "s_med": med(sents_sorted) if sents_sorted else 0,
        "sents": len(sents),
        "s_max": max(sents_sorted) if sents_sorted else 0,
        "dash": dash,
        "dash_permille": round(dash * 1000 / total, 1),
        "bold": bold,
        "bold_per_k": round(bold * 1000 / total, 1),
        "p_over150": sum(1 for _, h in paras if h > L_PARA_NOTE),
        "p_over200": sum(1 for _, h in paras if h > L_PARA_HARD),
        "pair": pair,
        "nest": nest,
        "inner_punct": inp,
        "meta": meta,
        "top": sorted(long_paras, key=lambda x: -x[1])[:8],
    }


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    bad = 0
    for path in argv:
        r = measure(path)
        if r is None:
            print("空文件或无散文段：%s" % path)
            continue
        name = path.replace("\\", "/").split("/")[-1]
        print("=" * 78)
        print("%s　散文 %d 段・汉字 %d・句 %d" % (name, r["paras"], r["total"], r["sents"]))
        rows = [
            ("句中位", r["s_med"], L_SENT_MED, r["s_med"] <= L_SENT_MED),
            ("最长句", r["s_max"], "-", True),
            ("破折号‰", r["dash_permille"], L_DASH, r["dash_permille"] <= L_DASH),
            ("加粗块/千字", r["bold_per_k"], L_BOLD, r["bold_per_k"] <= L_BOLD),
            ("段 >150（记数）", r["p_over150"], "-", True),
            ("段 >200", r["p_over200"], 0, r["p_over200"] == 0),
            ("括号对", r["pair"], "-", True),
            ("嵌套括号", r["nest"], 0, r["nest"] == 0),
            ("括号装内容", r["inner_punct"], 0, r["inner_punct"] == 0),
            ("元话语命中", r["meta"], 0, r["meta"] == 0),
        ]
        for k, v, line, ok in rows:
            mark = "" if ok else "  <== 破线"
            print("  %-14s %-8s 线 %-6s%s" % (k, v, line, mark))
            if not ok:
                bad += 1
        print("  最长的几段：")
        for ln, h, s in r["top"]:
            head = s if len(s) <= 42 else s[:42] + "…"
            print("    L%-5d %4d 字  %s" % (ln, h, head))
    print("=" * 78)
    print("红线：段长 200 硬线（150 只记数）・句中位 24・加粗 6・破折号 10‰；段中位不设线、不报。")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
