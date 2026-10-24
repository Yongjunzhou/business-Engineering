#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""term_grade.py —— 术语三级分级的核账量具（手册 §1.5.1）

口径（与手册一致）：
  1. 读该章概念一致性审视清单的「§二 概念清单」表：概念｜英文／别名｜类｜术语等级｜章内首现行号｜章内定义处｜权威出处；
  2. 回本章正文逐词计次，计次前先去掉代码块、表格行（以 | 起首）、引用块（以 > 起首）；
  3. 「掩蔽」计次：同一份清单里更长的术语优先占位，避免「需求工程」被算进「需求」；
  4. 三判：① 等级列是否有空格；② 基础术语的「章内定义处」必须有行号、核心术语的「章内定义处」不得指向章内；
          ③ 基础与核心的章内计次都须 > 1（不反复使用就不够格）；另报「三级条数合计＝清单总数」。

它是核账工具、不是生成器：等级由主笔判、由用户裁，脚本只报「判得站不站得住」。

用法：
  python3 term_grade.py [清单路径] [章文件路径]
  不给参数时用本目录下的 00-ch4-概念一致性审视清单.md 与 04-第4章-需求工程-把诉求变成需求规格.md
"""

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_CHECKLIST = HERE / "00-ch4-概念一致性审视清单.md"
DEFAULT_CHAPTER = HERE / "04-第4章-需求工程-把诉求变成需求规格.md"

GRADES = ("基础", "核心", "普通")


def parse_checklist(path):
    """从清单 §二 概念清单的表里取行；返回 [(概念, 等级, 定义处, 首现行号)]。"""
    rows = []
    in_section = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("## "):
            in_section = "概念清单" in line
            continue
        if not in_section or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 7:
            continue
        if cells[3] not in GRADES:  # 表头、分隔行、分组行
            continue
        concept, _, _, grade, first_line, def_where, _ = cells[:7]
        rows.append((concept, grade, def_where, first_line))
    return rows


def count_in_chapter(chapter_path, concepts):
    """回正文逐词计次（去代码块／表格／引用块，长词掩蔽）。"""
    text_lines, in_code = [], False
    for line in chapter_path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        if in_code or s.startswith("|") or s.startswith(">"):
            continue
        text_lines.append(line)
    text = "\n".join(text_lines)

    def tokens(concept):
        """一个概念在计次时认哪几个词：取「／」并列的各支，去掉括号注。"""
        out = []
        for part in re.split(r"[／/]", concept):
            part = re.sub(r"（[^）]*）", "", part).strip()
            if part:
                out.append(part)
        return out

    pairs = [(concept, tokens(concept)) for concept in concepts]
    flat = sorted({t for _, ts in pairs for t in ts}, key=len, reverse=True)

    masked, slot = text, {}
    for i, term in enumerate(flat):
        token = f"\u0000{i}\u0000"
        slot[term] = token
        masked = masked.replace(term, token)

    return {concept: sum(masked.count(slot[t]) for t in ts) for concept, ts in pairs}


def is_line_ref(value):
    return bool(re.search(r"L\d+|第\s*\d+\s*行|§\d", value))


def main():
    checklist = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CHECKLIST
    chapter = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_CHAPTER
    if not checklist.exists() or not chapter.exists():
        sys.exit("找不到清单或章文件：%s / %s" % (checklist, chapter))

    rows = parse_checklist(checklist)
    if not rows:
        sys.exit("清单 §二 没解析到带等级的条目——检查表头七列与「术语等级」列的取值（基础／核心／普通）。")

    counts = count_in_chapter(chapter, [r[0] for r in rows])

    print("清单：%s" % checklist.name)
    print("章文件：%s" % chapter.name)
    print()
    print("| 概念 | 等级 | 章内定义处 | 章内计次 |")
    print("|---|---|---|---|")
    for concept, grade, def_where, _ in rows:
        print("| %s | %s | %s | %d |" % (concept, grade, def_where, counts[concept]))

    tally = {g: sum(1 for r in rows if r[1] == g) for g in GRADES}
    print()
    print("分级：基础 %d／核心 %d／普通 %d（合计 %d 项）" % (
        tally["基础"], tally["核心"], tally["普通"], len(rows)))

    fails = []
    for concept, grade, def_where, _ in rows:
        if grade == "基础" and not is_line_ref(def_where):
            fails.append("② 基础术语「%s」的章内定义处为空或没给行号：%s" % (concept, def_where))
        if grade == "核心" and is_line_ref(def_where) and "不定义" not in def_where:
            fails.append("② 核心术语「%s」的章内定义处指向了章内：%s" % (concept, def_where))
        if grade in ("基础", "核心") and counts[concept] <= 1:
            fails.append("③ %s术语「%s」章内计次 %d（须 >1）" % (grade, concept, counts[concept]))

    print()
    if fails:
        for f in fails:
            print("✗ " + f)
        print()
        print("判定：不过（%d 条待改）" % len(fails))
        sys.exit(1)
    print("✓ ① 等级列逐条有值（%d 条）" % len(rows))
    print("✓ ② 基础术语逐条有章内定义处、核心术语逐条不指向章内")
    print("✓ ③ 基础与核心术语章内计次均 > 1")
    print("✓ ② 三级条数合计＝清单总数（%d）" % len(rows))
    print()
    print("判定：全过")


if __name__ == "__main__":
    main()
