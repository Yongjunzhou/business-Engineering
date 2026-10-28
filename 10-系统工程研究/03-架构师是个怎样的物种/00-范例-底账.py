# -*- coding: utf-8 -*-
"""00-范例-底账.py —— 范例审查第〇步：机械底账（只读，不改正文）

用途
  1. 默认（无参数）：打印「章级总表」——各章的汉字数、节数、案例落点、
     引文块、表行、Mermaid、专业参数、专有细节、标准指针，用于定位
     "范例偏薄"的章。
  2. --sections：打印「节级标记表」——每章每一节带哪些范例标记
     （案例／引文／表／图／数／细节／标准／人／例），单看无标记的
     节标「零件」、只有一处标记的标「薄」。
  3. --md <路径>：把选中内容（默认章级总表，加 --sections 则两者都写）
     写成 markdown 文件。

口径
  · 专业参数＝数字带工程单位（℃／小时／分钟／秒／片／周／元／毫米／%…）。
  · 专有细节＝型号、版本号、日期、料号式编号、BOM／SOP／UAT／CNC 等。
  · 标准指针＝ISO／IEC／IEEE／GB／GJB／42010／42020／15288 等字样。
  · 本脚本只数"标记"，不判"应景／专业／领域匹配"——那三项靠人读，
    见 00-范例审查方案.md。
"""
import re
import os
import sys
import glob
import argparse

sys.stdout.reconfigure(encoding="utf-8")

BASE = os.path.dirname(os.path.abspath(__file__))

H2 = re.compile(r"^##\s+(?!#)(.*)$")
H3 = re.compile(r"^###\s+(?!#)(.*)$")
H4 = re.compile(r"^####\s+(.*)$")
FENCE = "```"
NUMU = re.compile(r"\d+(?:\.\d+)?\s*(?:℃|°C|小时|分钟|秒|毫秒|片|周|天|个月|月|年|元|万元|kg|公斤|克|毫米|厘米|伏|V|W|GB|MB|TB|%|‰|级|倍|人|台)")
DET = re.compile(r"(?:M3|v\d+\.\d+|20\d\d-\d\d-\d\d|\d+月\d+日|[A-Z]{2,}\d{2,}|BOM|SOP|UAT|CNC|PCBA|REQ-\d+)")
STD = re.compile(r"(?:ISO|IEC|IEEE|GB/T|GJB|42010|42020|15288|15289|29148|42030)")
PERSON = re.compile(r"(?:林涛|赵刚|石军|吴浩|季昭|小周|小张|曹峰|郑亮|罗建|苏婷|王默|顾言|小陈|小冯)")
EXH = re.compile(r"(?:比如|例如|打个比方|好比|举例)")
CASEH = re.compile(r"案例进展|案例回场|误解现场")
HAN = re.compile(r"[\u4e00-\u9fff]")


def chapters():
    out = []
    for f in sorted(glob.glob(os.path.join(BASE, "*.md"))):
        n = os.path.basename(f)
        if re.match(r"^\d\d-第\d+章", n) and "从教材到问题分析" not in n:
            out.append(f)
    return out


def scan(path):
    """返回 (章级计数, [(层级, 标题, 标记dict)])"""
    lines = open(path, encoding="utf-8").read().splitlines()
    text = "\n".join(lines)
    secs = []

    def newsec(level, title):
        m = dict(case=0, quote=0, tbl=0, mm=0, num=0, det=0, std=0, person=0, exh=0)
        secs.append((level, title, m))
        return m

    marks = newsec("h2", "(章首)")
    in_fence = False
    for l in lines:
        s = l.strip()
        if s.startswith(FENCE):
            if not in_fence and "mermaid" in s:
                marks["mm"] += 1
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m2, m3, m4 = H2.match(l), H3.match(l), H4.match(l)
        if m2 or m3 or m4:
            level, title = ("h2", m2.group(1)) if m2 else (("h3", m3.group(1)) if m3 else ("h4", m4.group(1)))
            marks = newsec(level, title.strip())
            if CASEH.search(title):
                marks["case"] += 1
        else:
            if s.startswith(">"):
                marks["quote"] += 1
            if s.startswith("|") and not re.match(r"^\|[\s:|-]+\|$", s):
                marks["tbl"] += 1
            marks["num"] += len(NUMU.findall(l))
            marks["det"] += len(DET.findall(l))
            marks["std"] += len(STD.findall(l))
            marks["person"] += len(PERSON.findall(l))
            marks["exh"] += len(EXH.findall(l))
            if CASEH.search(l):
                marks["case"] += 1
    total = dict(han=len(HAN.findall(text)), secs=len([x for x in secs if x[0] in ("h3", "h4")]))
    for k in ("case", "quote", "tbl", "mm", "num", "det", "std"):
        total[k] = sum(x[2][k] for x in secs)
    return total, secs


def table_header():
    return ("| 章 | 汉字 | 节 | 案例落点 | 引文块 | 表行 | 图 | 专业参数 | 专有细节 | 标准指针 |\n"
            "|---|---|---|---|---|---|---|---|---|---|\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sections", action="store_true")
    ap.add_argument("--md")
    a = ap.parse_args()

    rows, blocks = [], []
    for f in chapters():
        t, secs = scan(f)
        name = os.path.basename(f).replace(".md", "")
        short = re.sub(r"^(\d\d)-第(\d+)章.*$", r"ch\2", name).replace("ch", "ch")
        rows.append("| %s | %d | %d | %d | %d | %d | %d | %d | %d | %d |" % (
            short, t["han"], t["secs"], t["case"], t["quote"], t["tbl"], t["mm"],
            t["num"], t["det"], t["std"]))
        buf = ["### %s\n" % name]
        for level, title, m in secs:
            score = m["num"] + m["det"] + m["std"] + m["tbl"] + m["mm"] + m["quote"] + m["exh"]
            tag = ""
            if score == 0 and m["person"] == 0 and m["case"] == 0:
                tag = " ← 零件"
            elif score <= 1 and m["case"] == 0:
                tag = " ← 薄"
            flag = ["%s%d" % (k, m[k]) for k in ("case", "quote", "tbl", "mm", "num", "det", "std", "person", "exh") if m[k]]
            ind = {"h2": "", "h3": "  ", "h4": "    "}[level]
            buf.append("%s- [%s] %s  （%s）%s\n" % (ind, level, title, "·".join(flag) or "无标记", tag))
        blocks.append("".join(buf) + "\n")

    body = table_header() + "\n".join(rows) + "\n"
    print(body)
    if a.sections:
        print("".join(blocks))
    if a.md:
        with open(a.md, "w", encoding="utf-8") as fp:
            fp.write(body)
            if a.sections:
                fp.write("\n" + "".join(blocks))
        print("written:", a.md)


if __name__ == "__main__":
    main()
