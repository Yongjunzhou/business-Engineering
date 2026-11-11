#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
00-开工读解-核对.py —— 阶段一「开工前读解」的机械关（2026-11-11 立）

用途
    拿一份章节入口文件（pending-chN-*.md），核对「开工前读解不得降档」那组规则
    有没有被写进件里、有没有被降档。规则正文在 00-逐章修订手册.md：
        §1.1.1（五类读解）｜§0.8 做法第 1 步（抄工序条）｜§0.6 甲·守据行（引工序条）
        ｜§0.9.1（《读解表》＋两条禁令）｜§0.4之三 三十九（来历）

用法
    python 00-开工读解-核对.py <入口文件.md> [--prev=16] [--stage=entry|phase1]
        --prev=16       前序章数（默认 16），用于核对"三句＋两句"表的行数够不够
        --stage=phase1  默认。阶段一展示时用：八项全过才算过（读解表已填、三句两句表已有、体检已做）
        --stage=entry   收工备入口时用：只查"开工单在、且没把读解降档、且写明了要交《读解表》"三项

判据（八项；phase1 全过才退出码 0，entry 档只查 R1／R2／R9）
    R1 有「§〇 开工单」节
    R2 开工单里有「读解基础」，且**未把读解降成"卡片"**（正则命中即违规）
    R3 有《读解表》/读解表，且五类各一行（① ② ③ ④ ⑤ 或 工1~工5）
    R4 有「三句＋两句」表（表头含"讲到哪儿为止"或"不得重复"），且数据行 ≥ 前序章数
    R5 有工序条块（工1…或"工序条"字样）
    R6 证据块守据行引到 §1.1.1（工序条），不只是"展示→体检→确认"
    R7 有「不适用条目」一行
    R8 有「读者体检」相关记录 ≥2 处（停点①②）
    R9（仅 entry 档）开工单里写明要交《读解表》

读数
    每项一行 ✓/✗，末尾一行 `读数：8 项过 N 项`；退出码 0＝全过、1＝有缺口。
"""
import sys, re, pathlib

RULES = [
    ("R1", "有「§〇 开工单」节"),
    ("R2", "读解基础在，且未降档为\"卡片\""),
    ("R3", "《读解表》五类各一行"),
    ("R4", "「三句＋两句」表行数够"),
    ("R5", "有工序条块"),
    ("R6", "守据引到 §1.1.1"),
    ("R7", "有\"不适用条目\"一行"),
    ("R8", "读者体检记录 ≥2 处"),
]
ENTRY_RULES = [
    ("R1", "有「§〇 开工单」节"),
    ("R2", "读解基础在，且未降档为\"卡片\""),
    ("R9", "开工单写明要交《读解表》"),
]

def check(path: pathlib.Path, prev: int):
    t = path.read_text(encoding="utf-8")
    lines = t.splitlines()
    res = {}

    # R1（允许整节被包在引文块里，如 "> ## §〇 开工单"）
    res["R1"] = bool(re.search(r"^[>\s]*#{2,3} .*§〇.*开工单", t, re.M))

    # R2
    has_read = "读解基础" in t
    downgraded = re.search(r"读解[^\n]{0,30}卡片", t) is not None
    res["R2"] = has_read and not downgraded

    # R3
    table = ("读解表" in t)
    cls_hits = sum(1 for c in "①②③④⑤" if re.search(r"^\|\s*" + c + r"\s*\|", t, re.M))
    work_hits = sum(1 for i in range(1, 6) if re.search(r"^\|\s*工" + str(i) + r"\s*\|", t, re.M))
    res["R3"] = table and max(cls_hits, work_hits) >= 5

    # R4
    r4 = False
    for i, ln in enumerate(lines):
        if ln.startswith("|") and ("讲到哪儿为止" in ln or "不得重复" in ln):
            rows = 0
            for nxt in lines[i + 1:]:
                if not nxt.startswith("|"):
                    break
                if re.match(r"^\|[\s\-:|]+\|$", nxt):
                    continue
                rows += 1
            r4 = rows >= prev
            break
    res["R4"] = r4

    # R5
    res["R5"] = ("工序条" in t) or re.search(r"^\|\s*工1\s*\|", t, re.M) is not None

    # R6
    res["R6"] = bool(re.search(r"守据[^\n]{0,20}（?工序条", t)) or bool(
        re.search(r"守据[\s\S]{0,400}§1\.1\.1", t))

    # R7
    res["R7"] = "不适用条目" in t

    # R8
    res["R8"] = t.count("读者体检") >= 2

    # R9（entry 档）
    res["R9"] = "读解表" in t

    return res

def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    prev = 16
    stage = "phase1"
    for a in sys.argv[1:]:
        m = re.match(r"--prev=(\d+)$", a)
        if m:
            prev = int(m.group(1))
        m = re.match(r"--stage=(entry|phase1)$", a)
        if m:
            stage = m.group(1)
    if not args:
        print("用法：python 00-开工读解-核对.py <入口文件.md> [--prev=16] [--stage=entry|phase1]")
        return 2
    p = pathlib.Path(args[0])
    if not p.exists():
        print(f"文件不存在：{p}")
        return 2
    res = check(p, prev)
    rules = ENTRY_RULES if stage == "entry" else RULES
    print(f"=== 开工读解核对：{p}（stage={stage}，前序章数 {prev}）===")
    for code, desc in rules:
        print(f"  {code} {'PASS' if res.get(code) else 'FAIL'}  {desc}")
    ok = sum(1 for c, _ in rules if res.get(c))
    print(f"读数：{len(rules)} 项过 {ok} 项" + ("（全过）" if ok == len(rules) else "（有缺口）"))
    return 0 if ok == len(rules) else 1

if __name__ == "__main__":
    sys.exit(main())
