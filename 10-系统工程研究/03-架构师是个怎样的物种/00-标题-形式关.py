#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""00-标题-形式关.py —— 逐章标题的机械检查（第12章阶段三立）

用法：
    python 00-标题-形式关.py <章节md>            # 检查该章全部 ## / ### 标题
    python 00-标题-形式关.py <md> --json          # 机器可读

判据来自 `00-逐章修订手册.md` §2.6 第一道·形式关九项（①~⑨）与「题面的三不许」。
本脚本只查**可机械化**的五项：⑥ 数字、⑦ 汉字数、⑤ 代词族（词表见下）、
② 符号表达式、⑧ 下一级题面是否带上二级标题的一个词（取最长公共子串 ≥2 字）。
查不了的（① 实词起首、③ 非喻体、④ 有户口、⑨ 统一句式）仍需人工过。

★ 词表与手册 §2.6 ⑤ **同源**：手册里"这·那·该·其·它·此……"曾用省略号，
  导致自写检查只覆盖前五个、误报"无代词"。故把族列全，脚本与条文同一份清单。

退出码：0＝无硬违规；1＝有硬违规（超长／数字／符号／代词）。
"""
import sys, re, json

# ---- 代词族（与手册 §2.6 ⑤ 同源；多字词优先匹配）----
PRONOUNS = [
    # 人称
    "我们", "你们", "他们", "她们", "它们", "咱们", "自己", "自身", "大家", "人家",
    "我", "你", "您", "他", "她", "它",
    # 指示
    "这", "那", "此", "该", "其", "本", "每", "各", "某", "另",
    # 疑问
    "为什么", "怎么样", "怎样", "什么", "哪里", "哪儿", "多少", "谁", "哪", "几", "何", "怎么",
    # 无定 / 反身 / 相互
    "有人", "别人", "某些", "彼此", "互相",
]
PRONOUNS.sort(key=len, reverse=True)

SYMBOLS = ["vs", "≠", "＝", "=", "⊃", "→", "->"]

# 体例锚：豁免 ⑧（仍查代词／数字／长度）
EXEMPT_8 = {"误解现场", "本章的人和物", "本章要回答什么", "认知反转", "小结", "附录"}


def cjk_len(s: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", s))


def strip_no(t: str) -> str:
    m = re.match(r"^([0-9]+(?:\.[0-9]+)*|[A-E])\s+(.*)$", t.strip())
    return m.group(2).strip() if m else t.strip()


def longest_common(a: str, b: str) -> str:
    a2 = re.sub(r"[^\u4e00-\u9fff]", "", a)
    b2 = re.sub(r"[^\u4e00-\u9fff]", "", b)
    best = ""
    for i in range(len(a2)):
        for j in range(i + 1, len(a2) + 1):
            if a2[i:j] in b2 and len(a2[i:j]) > len(best):
                best = a2[i:j]
    return best


def scan(path):
    lines = open(path, encoding="utf-8").read().split("\n")
    parent, rows = "", []
    for ln in lines:
        m2 = re.match(r"^##\s+(.+)$", ln)
        m3 = re.match(r"^###\s+(.+)$", ln)
        if m2 and not ln.startswith("###"):
            parent = strip_no(m2.group(1))
            continue
        if not m3:
            continue
        raw = strip_no(m3.group(1))
        n = cjk_len(raw)
        hits = [p for p in PRONOUNS if p in raw]
        # 去重（"什么"与"什么"子串、"哪"与"哪里"）
        hits = [h for h in hits if not any(h != o and h in o for o in hits)]
        digits = bool(re.search(r"[0-9]", raw))
        syms = [s for s in SYMBOLS if s in raw]
        exempt = (raw in EXEMPT_8) or (parent == "附录")
        shared = "" if exempt else longest_common(raw, parent)
        rows.append({
            "parent": parent, "title": raw, "chars": n,
            "pronouns": hits, "digits": digits, "symbols": syms,
            "shared": shared, "exempt8": exempt,
        })
    return rows


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    rows = scan(args[0])
    bad = 0
    print(f"{'父题':16s} {'题面':28s} 汉字 代词 数字 符号 ⑧带词")
    for r in rows:
        flags = []
        if r["chars"] > 15:
            flags.append("超15"); bad += 1
        exempt = r["exempt8"]
        if r["pronouns"]:
            flags.append(("体例锚·" if exempt else "") + "代词:" + "/".join(r["pronouns"]))
            if not exempt: bad += 1
        if r["digits"]:
            flags.append(("体例锚·" if exempt else "") + "数字")
            if not exempt: bad += 1
        if r["symbols"]:
            flags.append("符号:" + "/".join(r["symbols"])); bad += 1
        if not r["exempt8"] and not r["shared"]:
            flags.append("⑧无带词")
        print(f"{r['parent'][:15]:16s} {r['title'][:27]:28s} {r['chars']:>3} "
              f"{'/'.join(r['pronouns']) or '-':8s} {'Y' if r['digits'] else '-':2s} "
              f"{'/'.join(r['symbols']) or '-':6s} {r['shared'] or '-':8s} "
              f"{'  <== ' + '；'.join(flags) if flags else ''}")
    print(f"\n共 {len(rows)} 题；硬违规 {bad} 项（超15／代词／数字／符号）。"
          f"⑧ 无带词只报不判（人工核）。")
    if "--json" in sys.argv:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
