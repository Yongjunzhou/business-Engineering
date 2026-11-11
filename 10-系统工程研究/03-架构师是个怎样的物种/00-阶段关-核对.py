#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""00-阶段关-核对.py —— 每一关"该交的三件"有没有交齐（2026-11-11 立）

为什么要它：第17章阶段三第一次交件时，我只读了 §1.3.1（七件）就动手，
漏掉了 §1.3.3 的三处硬要求与"读者读三次"，还把"形式关自检"当成读数写进件里
（没跑 00-标题-形式关.py）。病根是"换一关，工序条没重抄一遍"。
本脚本把每一关该有的三件做成机械检查：**关内清单 / 量具读数 / 体检单**。

用法：
    python 00-阶段关-核对.py <入口文件.md> --gate=1|2|3|4|5|6|7|8

每关的检查项（PASS/FAIL）：
  通用（各关都要）：
    G1 有「关内清单」或「工序条」块
    G2 有「证据块」（守据/尺度/拦下三格）
    G3 有「体检单/读者体检」记录（阶段一、三、四、七、八；二、五、六可标"本关无体检"）
  阶段专有：
    阶段一：P1《读解表》五类在（另跑 00-开工读解-核对.py --stage=phase1 全过）
    阶段二：P2 有「全库点检表」「原料清单」「承重句表」三张
    阶段三：P3 有「标题清单」；P4 有「00-标题-形式关.py」的**脚本名与读数**（不是"自检"二字的印象）；
            P5 有三次体检的落点（块题／节题／全部）
    阶段四：P6 有「十三步」施工记录与复算读数
    阶段五：P7 有术语分级（基础/核心/普通）与不一致条数
    阶段六：P8 有名实四查与「00-标题-形式关.py」复跑读数
    阶段七：P9 有断点清单与四项对表
    阶段八：P10 有换位清单（每条标"代理未报/已报"）

退出码：0＝该关三件齐；1＝有缺口。
"""
import sys, re, pathlib

GENERIC = [
    ("G1", "有「关内清单」或「工序条」块", lambda t: ("关内清单" in t) or ("工序条" in t)),
    ("G2", "有「证据块」三格", lambda t: ("守据" in t) and ("尺度" in t) and ("拦下" in t)),
    ("G3", "有体检单或已声明本关无体检",
     lambda t: (t.count("读者体检") >= 1) or ("本关无体检" in t)),
]
BY_GATE = {
    "1": [("P1", "有《读解表》或五类读解记录", lambda t: ("读解表" in t) or ("读解基础记录" in t))],
    "2": [("P2", "有全库点检表＋原料清单＋承重句表",
           lambda t: ("全库点检表" in t) and ("原料清单" in t) and ("承重句表" in t))],
    "3": [("P3", "有标题清单", lambda t: "标题清单" in t),
          ("P4", "贴了 00-标题-形式关.py 的脚本名与读数",
           lambda t: ("00-标题-形式关.py" in t) and re.search(r"硬违规\s*[=:：]?\s*\d+", t) is not None),
          ("P5", "三次体检落点（块题／节题／全部）",
           lambda t: (t.count("块题") >= 1 and t.count("节题") >= 1 and "全部" in t))],
    "4": [("P6", "十三步施工记录＋复算读数",
           lambda t: ("十三步" in t) and re.search(r"段>?\s*1?50|段>200|标题\s*[0-9]+", t) is not None)],
    "5": [("P7", "术语分级（基础/核心/普通）＋不一致条数",
           lambda t: ("基础" in t and "核心" in t and "普通" in t) and ("不一致" in t))],
    "6": [("P8", "名实四查＋形式关复跑读数",
           lambda t: ("名实" in t) and ("00-标题-形式关.py" in t))],
    "7": [("P9", "断点清单＋四项对表", lambda t: ("断点清单" in t) and ("四项对表" in t))],
    "8": [("P10", "换位清单（标代理未报／已报）",
           lambda t: ("换位" in t) and (("代理未报" in t) or ("代理已报" in t)))],
}

def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    gate = None
    for a in sys.argv[1:]:
        m = re.match(r"--gate=(\d)$", a)
        if m:
            gate = m.group(1)
    if not args or not gate:
        print("用法：python 00-阶段关-核对.py <入口文件.md> --gate=N（1~8）")
        return 2
    p = pathlib.Path(args[0])
    if not p.exists():
        print(f"文件不存在：{p}")
        return 2
    t = p.read_text(encoding="utf-8")
    rules = GENERIC + BY_GATE.get(gate, [])
    print(f"=== 阶段关核对：{p}（阶段{gate}）===")
    ok = 0
    for code, desc, fn in rules:
        good = False
        try:
            good = bool(fn(t))
        except Exception:
            good = False
        print(f"  {code} {'PASS' if good else 'FAIL'}  {desc}")
        ok += 1 if good else 0
    print(f"读数：{len(rules)} 项过 {ok} 项" + ("（全过）" if ok == len(rules) else "（有缺口）"))
    return 0 if ok == len(rules) else 1

if __name__ == "__main__":
    sys.exit(main())
