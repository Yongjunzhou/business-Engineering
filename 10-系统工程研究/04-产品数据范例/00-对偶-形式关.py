#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""00-对偶-形式关.py —— 「两条规定压成一副口诀」的机械检查

为什么另立一只：段长、句中位、破折号、加粗、括号、元话语六样都能量，
唯独「一行一个岗，写到岗不写人名」这一类量不出来，而它正是腔最重的一种形。
判据的正本在《风格参考》§6.21 总判与《产品数据范例编制规程》4.9 的忌表，
本脚本只把那种形扫出来，不改判据。

扫五类形，只扫散文行（表格行、围栏、引用块、标题、表题、版本记录同量尺的口径）：

  R1 数量叠压   一X一Y：一行一个·一条一个·一格一个·一项一个
  R2 写A不写B   写/按/记/列/判/取/给 + …… + 不（写/按/记/列/判/取/给）
  R3 无谓语并置 两个分句都用逗号连、各不超过八个汉字、且都不含动词
  R4 短句对举   逗号后那一句以「不」「只」「各」「均」起头，且前后分句都不超过十字
  R5 压缩语     词表命中的名词化与自造简称（多对多、那一半、认者、落成、按号引、
                按节对数、写指针、必列、逐处、各归其位、至此、据此、据此判）

用法：`python 00-对偶-形式关.py <文件> [<文件> …] [--json]`
退出码：0＝零命中；1＝有命中。
"""
import json
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HAN = re.compile(r"[\u4e00-\u9fff]")
SENT_SPLIT = re.compile(r"[。！？；]")

# R1 数量叠压（叠字复用如「一条一条」不算，那是正常说法）
R1 = re.compile(r"一(行|条|格|项|句|户|处|人|栏)一(个|条|样|件|号|岗|事)")

# R2 写 A 不写 B 型
R2 = re.compile(r"(写|按|记|列|判|取|给)[^，。；]{0,6}不(写|按|记|列|判|取|给)")

# R4 短句对举：段内逗号分句，后句以不/只/各/均起头
R4_HEAD = ("不", "只", "各", "均", "都")

# R5 压缩语词表（随判例库维护；命中即报，是否改由人判）
# 不收「占号不占行」：那是规程 4.5 定死的术语，不许改字，命中不算缺陷。
R5_WORDS = [
    "多对多", "那一半", "认者", "落成", "按号引", "按节对数", "写指针",
    "必列", "逐处", "各归其位", "至此", "据此", "回填表",
]

VERBS = set("写记列编填取判落给算读改删并挂定立核数存归走做用带指抄搬换拆合连分标检退补加减留保压含收叫称成有在到从进出上下动排变整除")


def han(s):
    return len(HAN.findall(s))


def cjk_only(s):
    return "".join(HAN.findall(s))


def prose_lines(text):
    """与 00-文风-量尺.py 同口径：只取散文行。"""
    out, fence, in_record, record_level = [], False, False, 0
    for i, raw in enumerate(text.split("\n"), 1):
        s = raw.strip()
        if s.startswith("```"):
            fence = not fence
            continue
        if fence or not s:
            continue
        if s.startswith("#"):
            m = re.match(r"^(#{1,6})\s+(.*)$", s)
            if m:
                level, title = len(m.group(1)), m.group(2)
                if "修订记录" in title or "版本记录" in title:
                    record_level, in_record = level, True
                elif in_record and level <= record_level:
                    in_record, record_level = False, 0
            continue
        if in_record or s.startswith("|") or s.startswith(">"):
            continue
        if re.match(r"^([-*+]|\d+[.)])\s", s):
            continue
        if re.match(r"^\*\*[^*]{1,12}\*\*：", s):
            continue
        if re.match(r"^\*\*表\d+-\d+：", s):
            continue
        if (s.startswith("**版本**：") or s.startswith("版本：")
                or re.match(r"^v\d+\.\d+（", s) or s.startswith("更早的版本段移出")
                or re.match(r"^\*\*v\d+\.\d+", s)):
            continue
        out.append((i, s))
    return out


def clauses(s):
    """只按逗号切。顿号是并列项的分隔，切开会把「文档9、文档12」误读成两个分句。"""
    return [c.strip() for c in s.split("，") if c.strip()]


def scan_line(ln, s):
    hits = []
    for sent in SENT_SPLIT.split(s):
        sent = sent.strip()
        if not sent:
            continue
        if R1.search(sent):
            m = R1.search(sent).group(0)
            if m[1] != m[3]:  # 「一条一条」这类叠字复用不算
                hits.append((ln, "R1 数量叠压", sent, m))
        if R2.search(sent) and len(R2.search(sent).group(0)) <= 12:
            hits.append((ln, "R2 写A不写B", sent, R2.search(sent).group(0)))
        cl = clauses(sent)
        for a, b in zip(cl, cl[1:]):
            ha, hb = han(a), han(b)
            if ha == 0 or hb == 0:
                continue
            if ha <= 8 and hb <= 8:
                va = any(ch in VERBS for ch in a)
                vb = any(ch in VERBS for ch in b)
                if not va and not vb:
                    hits.append((ln, "R3 无谓语并置", sent, a + "，" + b))
                    continue
            if hb <= 10 and ha <= 10 and b.startswith(R4_HEAD):
                hits.append((ln, "R4 短句对举", sent, a + "，" + b))
    for w in R5_WORDS:
        if w in s:
            hits.append((ln, "R5 压缩语", s, w))
    return hits


def scan(path):
    text = open(path, encoding="utf-8").read()
    hits = []
    for ln, s in prose_lines(text):
        hits.extend(scan_line(ln, s))
    return hits


def main(argv):
    files = [a for a in argv if not a.startswith("--")]
    if not files:
        print(__doc__)
        return 2
    total = 0
    out = {}
    for path in files:
        hits = scan(path)
        total += len(hits)
        name = path.replace("\\", "/").split("/")[-1]
        print("=" * 78)
        print("%s　命中 %d 处" % (name, len(hits)))
        for ln, rule, sent, frag in hits:
            head = sent if han(sent) <= 34 else sent[:34] + "…"
            print("  L%-5d %-14s %-22s %s" % (ln, rule, frag, head))
        out[name] = [{"line": ln, "rule": r, "sentence": s, "frag": f} for ln, r, s, f in hits]
    print("=" * 78)
    print("合计命中 %d 处。判法：命中只说明这一句是那种形，改不改由人按《风格参考》§6.21 总判定。" % total)
    if "--json" in argv:
        print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
