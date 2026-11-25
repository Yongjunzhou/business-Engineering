#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""00-列名-形式关.py —— 表格列名（字段名）的机械检查

用法：
    python 00-列名-形式关.py <md 文件>            # 查该文件全部表格的列名
    python 00-列名-形式关.py <md 文件> --json      # 机器可读

判据出自《产品数据规范编制规范》4.4（字段与列名的关口）与《产品数据范例编制规程》
4.8「列名的取名法」、4.2 第六阶段的列名页、5.2 第 17 条：

  ① 汉字数四到八个，最好不超过六个（两处例外：48 号卡与各册 3.2 已定的中文字段名；
     表头的序号列）
  ② 不带括注（取值域写节首，不写进列名）
  ③ 不带数字
  ④ 不带代词族（这・那・该・本・各・其・每・某・谁・哪・什么・怎么……）
  ⑤ 是名词短语：不带问号、不以「吗／呢」收尾（问句判不过，人工复核）

退出码：0＝无硬违规；1＝有（超八个／不足四个／括注／数字／代词／问句）。
"""
import sys, re, json

# 48 号卡与各册 3.2 已定的中文字段名，不足四个字照卡不改（4.4 例外一）
# 例外二（2026-11-23 用户裁）：两栏名各含一个「・」（U+30FB），是列名的一部分，非表名与字段名的分隔，照裁不改。
CARD_NAMES = {"编号", "角色", "说明", "现状", "强制性", "关切名", "名称", "类型", "词", "序", "#", "字段名", "写法", "不成立", "处置", "规则号", "判法", "反例", "出处", "来源",
              "主角色・被度对象", "触发事件・质量特性", "主角色", "承接档", "结论", "去向"}
PRONOUNS = ["我们", "你们", "他们", "自己", "大家", "这", "那", "该", "本", "其", "每", "某", "另",
            "谁", "哪", "什么", "怎么", "多少", "几", "何", "彼此", "互相"]
PRONOUNS.sort(key=len, reverse=True)


def cjk(s):
    return len(re.findall(r"[\u4e00-\u9fff]", s))


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def scan(path):
    lines = open(path, encoding="utf-8").read().split("\n")
    rows = []
    for i in range(len(lines) - 1):
        nxt = lines[i + 1].strip()
        if not lines[i].startswith("|") or not nxt.startswith("|---"):
            continue
        for j, name in enumerate(cells(lines[i]), 1):
            n = cjk(name)
            probe = name
            for w in ("版本", "脚本", "基本", "文本", "样本", "成本", "资本", "本份", "本册"):
                probe = probe.replace(w, "")
            hits = [p for p in PRONOUNS if p in probe]
            hits = [h for h in hits if not any(h != o and h in o for o in hits)]
            rows.append({
                "line": i + 1, "col": j, "name": name, "chars": n,
                "paren": ("（" in name) or ("(" in name),
                "digit": bool(re.search(r"[0-9０-９]", name)),
                "pronouns": hits,
                "question": name.endswith(("？", "?", "吗", "呢")),
                "exempt": name in CARD_NAMES,
            })
    return rows


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    rows = scan(args[0])
    bad = 0
    print(f"{'行':>5} {'列':>3} {'列名':24s} 汉字 括注 数字 代词 问句")
    for r in rows:
        flags = []
        if r["exempt"]:
            pass
        elif r["chars"] > 8:
            flags.append("超八"); bad += 1
        elif r["chars"] < 4:
            flags.append("不足四"); bad += 1
        if r["paren"]:
            flags.append("括注"); bad += 1
        if r["digit"]:
            flags.append("数字"); bad += 1
        if r["pronouns"]:
            flags.append("代词:" + "/".join(r["pronouns"])); bad += 1
        if r["question"]:
            flags.append("问句"); bad += 1
        tail = ("  <== " + "；".join(flags)) if flags else ""
        print(f"{r['line']:>5} {r['col']:>3} {r['name'][:22]:24s} {r['chars']:>3} "
              f"{'Y' if r['paren'] else '-':4s} {'Y' if r['digit'] else '-':4s} "
              f"{('/'.join(r['pronouns']) or '-'):5s} {'Y' if r['question'] else '-'}"
              f"{tail}")
    print(f"\n共 {len(rows)} 个列名；硬违规 {bad} 项（超八／不足四／括注／数字／代词／问句）。"
          f"宜不过六、是否名词短语两项人工核。")
    if "--json" in sys.argv:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
