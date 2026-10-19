#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""四件对表 · 逐章读数（口径逐行抄自 .work-ch3/ruler4.py（同一把尺）＝同一把尺）
口径：去代码块／表格／引用块／清单行进段；段以空行切；句只以「。」断（不拆句末引号）。
报：散文汉字 / 段数 / 段长中位 / 句数 / 句长中位 / 句长均值 / 带人带例段占比 / 破折号每千字
另报：句长分档形状（1-10 / 11-20 / 21-27 / 28-40 / 41-60 / 61+）
用法：python .work-ch4/ruler4.py <章文件路径> [范本散文汉字下限]
"""
import io
import re
import statistics
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HAN = re.compile(r"[\u4e00-\u9fff]")
cjk = lambda s: len(HAN.findall(s))
F = chr(96) * 3
NAMES = ["万辉", "徐漾", "玉杰", "满海", "黄程", "小白", "水忠", "逸人", "文正", "董勐",
         "李旭", "恒信", "冰链", "M3", "泰坦尼克", "挑战者", "737"]
BANDS = [(1, 10), (11, 20), (21, 27), (28, 40), (41, 60), (61, 999)]


def prose_paras(lines):
    recs, cur, incode = [], [], False
    for line in lines:
        if line.strip().startswith(F):
            incode = not incode
            continue
        if incode:
            continue
        s = line.strip()
        if not s:
            if cur:
                recs.append(" ".join(cur)); cur = []
            continue
        if s[0] in "|>#" or s.startswith("- ") or s.startswith("* ") or re.match(r"^\d+\. ", s):
            if cur:
                recs.append(" ".join(cur)); cur = []
            continue
        cur.append(s)
    if cur:
        recs.append(" ".join(cur))
    return [p for p in recs if cjk(p) > 0]


def measure(lines):
    recs = prose_paras(lines)
    lens = [cjk(p) for p in recs]
    sents = []
    for p in recs:
        for x in re.split(r"。(?![」』）])", p):
            if cjk(x) > 0:
                sents.append(cjk(x))
    prose = "\n".join(recs)
    withp = sum(1 for p in recs if any(n in p for n in NAMES))
    return dict(p50p=statistics.median(lens), p50s=statistics.median(sents),
                mean=sum(sents) / len(sents), ex=100.0 * withp / len(lens),
                dash=1000.0 * len(re.findall("——", prose)) / cjk(prose),
                total=cjk(prose), np=len(lens), ns=len(sents)), sents


P = sys.argv[1] if len(sys.argv) > 1 else \
    r"03-架构师是个怎样的物种\04-第4章-需求工程-从诉求到依据.md"
lines = io.open(P, encoding="utf-8").read().split("\n")
m, sents = measure(lines)

print("文件：%s" % P)
print("散文汉字 %d｜段数 %d｜段长中位 %.0f｜句数 %d｜句长中位 %.1f｜句长均值 %.1f｜带人带例 %.0f%%｜破折号 %.2f/千字"
      % (m["total"], m["np"], m["p50p"], m["ns"], m["p50s"], m["mean"], m["ex"], m["dash"]))
print("\n句长分档形状：")
for lo, hi in BANDS:
    c = sum(1 for x in sents if lo <= x <= hi)
    print("  %-8s %4d 句  %5.1f%%" % ("%d-%d" % (lo, hi) if hi < 999 else "61+", c, 100.0 * c / m["ns"]))
print("\n红线自查：段长中位 ≥45 ？%s｜破折号 ≤10 ？%s｜带人带例 ≥15%% ？%s"
      % ("✓" if m["p50p"] >= 45 else "✗", "✓" if m["dash"] <= 10 else "✗",
         "✓" if m["ex"] >= 15 else "✗"))
