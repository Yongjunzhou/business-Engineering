#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""00-交稿-体检.py —— 一份数据（册・本体・过程记录）交稿前的机械转诊

为什么有这一只：规程 5.2 列了二十二条机械核对，散在各节，靠人一条一条记得住的不多。
这一只把它们里能跑的并成一条命令，按件分条：册十三条、本体十四条、过程记录件十一条，跑完出一张表，有一条不过就不许交。
判据不改，只转诊：能跑的出读数，跑不出的标「人工」，不假装跑过。

用法：
    python 00-交稿-体检.py 04-产品数据范例/02-相关方与关切规范.md \
                            04-产品数据范例/02-相关方与关切.md \
                            04-产品数据范例/02-相关方与关切-过程记录.md

    不带参数时跑 02 这一份三件，作样子。
退出码：0＝没有不过项；1＝有不过项；2＝用法不对。

一条规矩：报「不过」的，改到过或者写进未完项并写明谁办几时办，不许挂账交稿。
"""
import importlib.util
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE = os.path.dirname(os.path.abspath(__file__))
HYGIENE = os.path.join(BASE, "00-文风-量尺.py")
COLNAME = os.path.join(BASE, "00-列名-形式关.py")
DUIJOU = os.path.join(BASE, "00-对偶-形式关.py")
TITLE = os.path.join(os.path.dirname(BASE), "03-架构师是个怎样的物种", "00-标题-形式关.py")

HAN = re.compile(r"[\u4e00-\u9fff]")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def han(s):
    return len(HAN.findall(s))


def read(path):
    return open(path, encoding="utf-8").read()


def kind(path):
    name = os.path.basename(path)
    if name.endswith("规范.md"):
        return "册"
    if name.endswith("-过程记录.md"):
        return "过程记录"
    return "本体"


def tables(text):
    """返回 [(表头行列数, 不齐行号[], 行号, 有无表题)]"""
    lines = text.split("\n")
    out = []
    for i in range(len(lines) - 1):
        if lines[i].startswith("|") and lines[i + 1].strip().startswith("|---"):
            n = len([c for c in lines[i].strip().strip("|").split("|")])
            bad = []
            j = i + 2
            while j < len(lines) and lines[j].startswith("|"):
                m = len([c for c in lines[j].strip().strip("|").split("|")])
                if m != n:
                    bad.append(j + 1)
                j += 1
            titled = any(re.match(r"^\*\*表\d+-\d+：", lines[k].strip())
                         for k in range(max(0, i - 3), i))
            out.append((n, bad, i + 1, titled))
    return out


def sections(text, level):
    pat = re.compile(r"^%s\s+(.+)$" % ("#" * level))
    return [m.group(1).strip() for ln in text.split("\n") if (m := pat.match(ln))]


def versions(text):
    return re.findall(r"v(\d+\.\d+(?:\.\d+)?)", text)


def check_file(path):
    text = read(path)
    k = kind(path)
    rows = []

    def add(no, name, status, note, fix=None):
        rows.append({"no": no, "name": name, "status": status, "note": note, "fix": fix})

    # 01 表数＝表题数
    tb = tables(text)
    n_title = len(re.findall(r"^\*\*表\d+-\d+：", text, re.M))
    add("01", "表数＝表题数", "过" if len(tb) == n_title else "不过",
        "%d＝%d" % (len(tb), n_title),
        "缺题的表补 **表N-M：…**，写在上方" if len(tb) != n_title else None)

    # 02 表格列数一致
    bad_rows = [ln for _, b, _, _ in tb for ln in b]
    add("02", "表格列数一致", "过" if not bad_rows else "不过",
        "%d 张表，%d 行不齐" % (len(tb), len(bad_rows)),
        "行号 %s" % bad_rows[:6] if bad_rows else None)

    # 03 版本号一处一致
    vs = versions(text)
    uniq = sorted(set(vs))
    if not vs:
        add("03", "版本号一处一致", "人工", "本件未出现版本号")
    elif len(uniq) == 1:
        add("03", "版本号一处一致", "过", "只一个：v%s（%d 处）" % (uniq[0], len(vs)))
    else:
        add("03", "版本号一处一致", "人工", "出现 %s 几个号，跨版本记录可容许，人核" % "、".join(uniq))

    # 04 版本段条数与长度
    seg = [ln for ln in text.split("\n") if ln.startswith("版本：") or ln.startswith("**版本**：")]
    if not seg:
        add("04", "版本段三条・300 字", "人工", "无版本段（册见附录 B，数据见户头）")
    else:
        hs = [han(x) for x in seg]
        ok = len(seg) <= 3 and sum(hs) <= 300
        add("04", "版本段三条・300 字", "过" if ok else "不过",
            "%d 条，合计 %d 字" % (len(seg), sum(hs)),
            "删到三条、压到 300 字以内" if not ok else None)

    # 05 记号零命中
    hits = []
    for pat, why in ((r"3[ABC]", "字母记号"), (r"PD-0", "废号"), (r"序 \d", "旧序号")):
        n = len(re.findall(pat, text))
        if n:
            hits.append("%s %d" % (why, n))
    add("05", "字母记号・废号・旧序号", "过" if not hits else "不过",
        "、".join(hits) if hits else "零命中")

    # 06 标题关
    t = load(TITLE, "title_gate")
    tr = t.scan(path)
    tbad = 0
    for r in tr:
        if r["chars"] > 15 or r["symbols"]:
            tbad += 1
        elif r["pronouns"] and not r["exempt8"]:
            tbad += 1
        elif r["digits"] and not r["exempt8"]:
            tbad += 1
    add("06", "题面形式关", "过" if tbad == 0 else "不过", "%d 题，硬违规 %d" % (len(tr), tbad))

    # 07 列名关
    c = load(COLNAME, "col_gate")
    cr = c.scan(path)
    cbad = 0
    for r in cr:
        if r["exempt"]:
            continue
        if r["chars"] > 8 or r["chars"] < 4 or r["paren"] or r["digit"] or r["pronouns"] or r["question"]:
            cbad += 1
    add("07", "列名形式关", "过" if cbad == 0 else "不过", "%d 项，硬违规 %d" % (len(cr), cbad))

    # 08 文风量尺
    h = load(HYGIENE, "hygiene")
    m = h.measure(path)
    if m is None:
        add("08", "文风量尺", "人工", "无散文段")
    else:
        bad = []
        if m["s_med"] > h.L_SENT_MED:
            bad.append("句中位 %.1f" % m["s_med"])
        if m["dash_permille"] > h.L_DASH:
            bad.append("破折号 %.1f‰" % m["dash_permille"])
        if m["bold_per_k"] > h.L_BOLD:
            bad.append("加粗 %.1f" % m["bold_per_k"])
        if m["p_over200"]:
            bad.append("段 >200 有 %d 段" % m["p_over200"])
        if m["nest"]:
            bad.append("嵌套括号 %d" % m["nest"])
        if m["inner_punct"]:
            bad.append("括号装内容 %d" % m["inner_punct"])
        if m["meta"]:
            bad.append("元话语 %d" % m["meta"])
        add("08", "文风量尺", "过" if not bad else "不过",
            "%d 段・%d 字・%d 句，句中位 %.1f" % (m["paras"], m["total"], m["sents"], m["s_med"]),
            "；".join(bad) if bad else None)

    # 09 对偶口诀命中（只报，逐条要有处置）
    d = load(DUIJOU, "duiou_gate")
    dh = d.scan(path)
    add("09", "对偶口诀命中", "报备" if dh else "过",
        "%d 处，逐条判改或判留（判留写理由）" % len(dh) if dh else "零命中")

    # 按件分：册
    if k == "册":
        want = ["1 概述", "2 术语", "3 数据表的张数与字段写法", "4 字段的来源与转换",
                "5 验收准则与判定结论", "6 下游用法与错法"]
        got = [x for x in sections(text, 2) if re.match(r"^[0-9]", x)]
        miss = [w for w in want if w not in got]
        add("10", "册的六章名与序", "过" if not miss and len(got) == 6 else "不过",
            "六章%s" % ("齐" if not miss and len(got) == 6 else "缺 %s" % miss),
            "照《产品数据规范编制规范》7.1 的章名与序改" if miss or len(got) != 6 else None)
        app = sections(text, 2)
        add("11", "两个附录", "过" if "附录 A 现成示范" in app and "附录 B 版本记录" in app else "不过",
            "附录 A／B %s" % ("齐" if "附录 A 现成示范" in app and "附录 B 版本记录" in app else "缺"))
        # 附录 A 的版本指针与本体现版一致
        m_a = re.search(r"## 附录 A.*?(?=\n## |\Z)", text, re.S)
        avs = set(versions(m_a.group(0))) if m_a else set()
        body = path.replace("规范.md", ".md")
        if avs and os.path.exists(body):
            bvs = set(versions(read(body)))
            same = avs & bvs
            add("12", "附录 A 指针＝本体现版", "过" if same else "不过",
                "附录 A 写 v%s，本体见 v%s" % ("／".join(sorted(avs)), "／".join(sorted(bvs))),
                "附录 A 只指版本与节号，改到现版" if not same else None)
        else:
            add("12", "附录 A 指针＝本体现版", "人工", "本体未给或无版本号")
        # 判读单是否落了账外件
        dd = os.path.dirname(path)
        nn = os.path.basename(path)[:2]
        found = [f for f in os.listdir(dd) if f.startswith(nn) and "判读单" in f]
        add("13", "四道判读单落账", "过" if found else "不过",
            found[0] if found else "同目录无 %s-*-判读单-*" % nn,
            "四道（表号、数据项、逐句、并段）的判读单是交稿要件，补一份" if not found else None)

    # 按件分：本体
    if k == "本体":
        # 题名之后先跳过标题行（## 1 概述 一类），取第一行正文：户头写在章题之下，不以表格起头即算过。
        first = next((ln for ln in text.split("\n")[1:] if ln.strip() and not ln.strip().startswith("#")), "")
        add("10", "户头作开头一段", "过" if not first.startswith("|") and not first.startswith("#") else "不过",
            "开头是%s" % ("一张表，仍是四行户头" if first.startswith("|") else "一段散文"),
            "规程 4.5：户头写作开头一段，四样都在" if first.startswith("|") else None)
        have = sections(text, 3)
        want = ["取值的来路", "示例值登记", "取值的变换与追溯", "从略清单"]
        miss = [w for w in want if not any(w in x for x in have)]
        add("11", "第四章四节", "过" if not miss else "不过",
            "四节%s" % ("齐" if not miss else "缺 %s" % miss))
        # 示例值三处对账：只数正文（第四章以前）的处数，对示例值登记的行数
        m4 = re.search(r"\n## 4 ", text)
        body_text = text[:m4.start()] if m4 else text
        n_body = body_text.count("（示例值）")
        m_reg = re.search(r"###[^\n]*示例值登记.*?(?=\n### |\Z)", text, re.S)
        n_reg = len([ln for ln in m_reg.group(0).split("\n") if ln.startswith("|")]) - 2 if m_reg else 0
        add("12", "示例值三处对账", "过" if n_body == n_reg else "报备",
            "正文 %d 处，示例值登记 %d 行" % (n_body, max(n_reg, 0)),
            "三处不等：正文、登记、取值的来路" if n_body != n_reg else None)

        # 14 自称与件名零命中（只判本体；过程记录与判读单是工作件，不扫）
        self_words = ["本份", "本表", "本册", "本登记册", "账外件", "户头", "资产三问", "节末一行"]
        hits = [w for w in self_words if w in body_text or w in text]
        add("14", "自称与件名零命中", "过" if not hits else "不过",
            "零命中" if not hits else "命中：" + "、".join(hits),
            "数据本体不写自称：写表号或「这里」（规程 4.5、元规范 8.1）" if hits else None)

        # 15 阶段数一处（只判本体）
        has7 = "七个阶段" in text
        has8 = "八个阶段" in text
        add("15", "阶段数一处", "过" if not (has7 and has8) else "不过",
            "七个阶段与八个阶段并现" if (has7 and has8) else "只一处",
            "阶段数只在一处写，别处引用（规程 5.2 第二十二条）" if (has7 and has8) else None)

    # 按件分：过程记录
    if k == "过程记录":
        have = sections(text, 3)
        want = ["验收准则与判定结论", "核对结果", "散文句覆盖与抽测", "题面与表达清单",
                "上游待改", "下游待改", "改动痕", "未完项", "交稿回执"]
        miss = [w for w in want if not any(w in x for x in have)]
        add("10", "过程记录九节", "过" if not miss else "不过",
            "九节%s" % ("齐" if not miss else "缺 %s" % miss),
            "照规程 4.11 补到九节，没有的写「无」" if miss else None)
        add("11", "第一节题作验收准则与判定结论", "过" if have and "验收准则与判定结论" in have[0] else "不过",
            have[0] if have else "无节")

    return {"path": path, "kind": k, "rows": rows}


def main(argv):
    files = argv or [
        os.path.join(BASE, "02-相关方与关切规范.md"),
        os.path.join(BASE, "02-相关方与关切.md"),
        os.path.join(BASE, "02-相关方与关切-过程记录.md"),
    ]
    total_fail = 0
    for f in files:
        if not os.path.exists(f):
            print("找不到：%s" % f)
            total_fail += 1
            continue
        r = check_file(f)
        print("=" * 78)
        print("体检：%s（%s）" % (os.path.basename(f), r["kind"]))
        for row in r["rows"]:
            mark = {"过": "✓", "不过": "✗", "报备": "!", "人工": "?"}[row["status"]]
            print("  %s %s %-24s %s" % (mark, row["no"], row["name"], row["note"]))
            if row["fix"]:
                print("        └ 改法：%s" % row["fix"])
            if row["status"] == "不过":
                total_fail += 1
        n = len(r["rows"])
        nf = sum(1 for x in r["rows"] if x["status"] == "不过")
        nw = sum(1 for x in r["rows"] if x["status"] == "报备")
        nh = sum(1 for x in r["rows"] if x["status"] == "人工")
        print("  —— %d 条：过 %d・不过 %d・报备 %d・人工 %d" % (n, n - nf - nw - nh, nf, nw, nh))
    print("=" * 78)
    print("不过项合计 %d。不过的不许交：改到过，或者写进未完项并写明谁办、几时办、落哪一行。" % total_fail)
    return 0 if total_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
