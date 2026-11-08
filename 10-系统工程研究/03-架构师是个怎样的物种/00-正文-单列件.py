#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""00-正文-单列件.py —— 正文可单列件的"裸量词／代词起首"体检（2026-11-06 立）

用法：
    python 00-正文-单列件.py <章节md>
    python 00-正文-单列件.py <章节md> --all     # 连同"代词起首"一并列出

判据来源：手册 §2.13（自足四条判法）与 §2.6 ⑤（代词族与量词），
**只管可单列件**——道理、目的、目标、主线、气脉、内涵各句、块题节题。
本脚本只扫**散文行**（去标题、引用块、表格、清单、围栏），并给出两类读数：

  ① 裸量词：量词后面紧跟虚词或标点，前面没有可指认的名词
     （"这一处是""一处、""这一个定"）——第13章阶段一栽过两轮，
      第一遍栽"它／它们"，第二遍栽"一处／一个"。
  ② 代词起首：整行以"这／那／它"开头（**只报不判**，承接句合法）。

**只报不判**：这两类都要人看上下文。退出码恒 0（它是体检，不是闸门）。
真正的闸门是阶段一关内清单第 0 行（逐件剪读），本脚本只是把"我列的窄清单"
换成"同一份词表"的工具。

词表与手册 §2.6 ⑤ 同源；改动词表必须两处同改。
"""
import sys
import re

# 量词族（与 §2.6 ⑤ 的"数词＋量的纯代称"同源）
QUANT = "个条支套种"   # ★ 只留真量词：栏／位／处／份／块／片／行／格 本身可作名词，"那一栏""这一位"是正常用法，不收

# 虚词与标点：量词后面紧跟这些，说明它没带名词
TAIL = "的是也就才都又在有不很最会能可把被让给对从到和与或，。；：、！？）】"


def cjk(s):
    return len(re.findall(r"[\u4e00-\u9fff]", s))


def is_prose(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    if s.startswith(("#", ">", "|", "-", "```", "1.", "2.", "3.", "4.", "5.",
                     "6.", "7.", "8.", "9.")):
        return False
    if re.match(r"^\d+\.", s):
        return False
    return True


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 0
    path = sys.argv[1]
    show_pron = "--all" in sys.argv
    lines = open(path, encoding="utf-8").read().split("\n")

    bare, pron = [], []
    pat_bare = re.compile(r"([这一那个条支套种份块片行栏格位]{0,2}[%s])(?=[%s])"
                          % (QUANT, TAIL))
    for i, line in enumerate(lines, 1):
        if not is_prose(line):
            continue
        for m in pat_bare.finditer(line):
            frag = m.group(1)
            # 只报"看起来是代称"的：单字量词，或"这/那/哪＋量词"
            if len(frag) == 1 or frag[0] in "这那哪":
                s = max(0, m.start() - 12)
                e = min(len(line), m.end() + 12)
                bare.append((i, frag, line[s:e].strip()))
        st = line.strip()
        if st and st[0] in "这那它":
            pron.append((i, st[:46]))

    print("=" * 72)
    print("正文可单列件体检：%s" % path)
    print("=" * 72)
    print("\n① 裸量词 —— %d 处（量词后紧跟虚词／标点，前面没有名词）" % len(bare))
    for i, frag, ctx in bare:
        print("   L%-5d %-4s … %s" % (i, frag, ctx))
    if show_pron:
        print("\n② 代词起首 —— %d 行（只报不判：承接句合法）" % len(pron))
        for i, s in pron:
            print("   L%-5d %s" % (i, s))
    else:
        print("\n② 代词起首 —— %d 行（加 --all 列出；只报不判）" % len(pron))
    print("\n读数：裸量词 %d｜代词起首 %d｜散文行 %d"
          % (len(bare), len(pron), sum(1 for l in lines if is_prose(l))))
    print("提醒：本脚本只报不判。阶段一关内清单第 0 行仍要逐件剪读。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
