#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""00-阈值-核对.py —— 手册总表的数与 00-阈值.py 的常量必须一致

用法：
    python 00-阈值-核对.py            # 逐键比对，退出码 0＝一致，1＝有漂移
    python 00-阈值-核对.py --quiet    # 只报不一致的键

判据：`00-逐章修订手册.md` §2.10之一「阈值总表」每一行的数值，
      必须等于 `00-阈值.py` 里同名键的值。任何一处改了另一处没改，
      本脚本即报错——**漂移由机器发现，不靠人记得**。

来历：2026-11-09。段长红线 2026-10-28 已由 150 改 200，但手册表与两个
脚本仍写 150，主笔按旧线施工。故立此核对，防"两处旧的互相背书"。
"""
import re
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
MANUAL = os.path.join(HERE, "00-逐章修订手册.md")

sys.path.insert(0, HERE)
try:
    import importlib.util

    spec = importlib.util.spec_from_file_location("thr", os.path.join(HERE, "00-阈值.py"))
    thr = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(thr)
except Exception as e:  # noqa
    print("读不到 00-阈值.py：%s" % e)
    sys.exit(1)


def parse_manual():
    """从手册 §2.10之一 的表格里抓 `| 键名 | 值 |` 行。"""
    if not os.path.exists(MANUAL):
        print("找不到手册：%s" % MANUAL)
        sys.exit(1)
    text = open(MANUAL, encoding="utf-8").read()
    m = re.search(r"#### 2\.10之一(.+?)(\n#### |\n### |\n## )", text, re.S)
    block = m.group(1) if m else ""
    found = {}
    for line in block.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        key, val = cells[0], cells[1]
        val = val.replace("**", "").replace("`", "").strip()
        num = re.search(r"-?\d+(?:\.\d+)?", val)
        if key and num:
            found[key] = float(num.group(0))
    return found


def main():
    quiet = "--quiet" in sys.argv
    manual = parse_manual()
    bad = []
    for key, want in thr.TABLE.items():
        got = manual.get(key)
        if got is None:
            bad.append((key, want, "手册总表里没有这一行"))
        elif abs(got - float(want)) > 1e-9:
            bad.append((key, want, "手册写 %s" % got))
    if bad:
        print("阈值漂移 %d 处（手册 §2.10之一 ↔ 00-阈值.py）：" % len(bad))
        for key, want, why in bad:
            print("  %-12s 代码=%s ｜ %s" % (key, want, why))
        sys.exit(1)
    if not quiet:
        print("阈值一致：%d 个键，手册 §2.10之一 ↔ 00-阈值.py 全对上。" % len(thr.TABLE))


if __name__ == "__main__":
    main()
