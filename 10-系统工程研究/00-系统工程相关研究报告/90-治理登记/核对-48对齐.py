# -*- coding: utf-8 -*-
"""核对-48对齐.py —— 报告库「与 48 号严格保持一致」的机械体检（只读）。

用法：
    python 核对-48对齐.py            # 全跑，打印五段读数
    python 核对-48对齐.py --quiet    # 只打印结论行

退出码：0＝无硬违规；1＝有硬违规（悬空指针／判废口径残影）。

口径：
  基准＝48 号（现行 v3.25）。本脚本只判"写着的东西能不能对上"，不判内容对错。
  硬违规两类：① 指向 48 号不存在节的指针；② 48 §15.1 已推翻的口径残影，且该行
  既无存史标记（已废／作废／原判／旧口径／撤／不再／曾／误／纠），也不带 48 号／46 号。
  其余作读数（软警示），逐句人工判——词可留、句必改（09 号教训第 8 条）。
"""

import os
import re
import sys
import glob
import collections

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.abspath(os.path.join(HERE, ".."))
R48 = os.path.join(LIB, "48-架构定义研究报告-从问题与机会到架构描述.md")

STD = ("42010", "42020", "15288", "42030", "ISO 9000", "ISO/IEC", "本报告", "48 号", "46 号")
HISTORY = ("已废", "判废", "作废", "历史", "原判", "原答", "旧口径", "旧式", "旧",
           "撤", "删", "停用", "不再", "曾", "误", "纠", "存史", "反证", "改")

HARD_PHRASES = {
    "架构描绘": "48 §10.5：已作废",
    "三格分流": "48 §5.5：现称去向差分卡，四个去向、五个出口",
    "四十四件": "48 §15.4 第 4 项：旧号轨已作废",
    "四十四份": "48 §15.4 第 4 项：旧号轨已作废",
    "位已废止": "48 文首术语纪律：位＝建模实体之简称",
    "角色位已废止": "48 §7.10：角色位＝八类位第 7 类",
    "旧称位": "48 文首术语纪律：位不是旧称",
}
SOFT_PHRASES = {
    "由目的裁": "判据位出现才改；存史与反证处不动",
    "目的必要性": "判据位出现才改；存史与反证处不动",
    "三把尺": "应写「一支填句三槽（三把尺＝三种填法）」，不得当判据本体",
    "承重测试": "降为体检提示，不作判据",
    "五张准入": "48 §2.11；引用时带节号",
    "七件": "最小集＝十四件；七件须带限定语（内容侧七件／44 号产出七件）",
    "关注点": "正名「关切」；国标译名只在首现括注一次",
    "唯一事实源": "合同审核例统一作「合同状态唯一权威源」",
}

COLD_FACTS = [("M3-0417", "箱号"), ("≥72 h", "断电保温"), ("30 s", "断链告警"),
              ("±0.5", "温控偏差"), ("4.8", "四点读数"), ("9.4", "四点读数")]

# 高风险八条：只收"违规写法"（否定句、存史句、另义句靠人判）
MATRIX_RULES = [
    ("C1 户口", [r"架构目标[（(]\s*42010", r"关键成功准则[（(]\s*42010",
                 r"关键成功准则的?定义", r"质量模型[（(]\s*42010",
                 r"质量模型的?定义", r"设计元素[（(]\s*42010"]),
    ("C3 三套名字", [r"架构实体[（(]描述", r"架构实体就是描述",
                     r"architecture entity.{0,12}描述元素"]),
    ("C4 架构两样", [r"架构就是结构", r"架构即结构", r"架构＝结构",
                     r"架构是(系统|企业)的结构", r"架构由元素(与|和)关系构成",
                     r"架构＝元素(与|和)关系"]),
    ("C13 清单≠描述", [r"清单就是描述", r"清单即描述", r"视图是清单的细化",
                       r"同一批内容的两种排法"]),
    ("C14 视图四问", [r"视图三问", r"三问即可", r"视图准入三问"]),
    ("C15 四层两道界", [r"架构元素＝系统元素", r"描述元素＝系统元素",
                        r"架构实体＝系统元素", r"分配落到系统元素"]),
    ("C24 评估三对象", [r"验证就是确认", r"验证＝确认", r"评估就是评描述",
                        r"评估对象只有架构"]),
    ("C28 产品数据判法", [r"产品数据就是文档", r"产品数据＝文档", r"齐套即合格",
                          r"齐套就是合格"]),
    ("C22 四条件厚度", [r"四条件[（(]\s*42020", r"42020.{0,20}四条件",
                        r"四条件.{0,8}标准规定", r"四条件.{0,8}标准要求"]),
    ("C23 名义与实得", [r"名义.{0,10}实得.{0,10}(相同|一样|同一)", r"收窄.{0,8}只有一种"]),
    ("C32 同案同数", [r"箱号\s*M3-(?!0417)\d{3,4}", r"(十|十二|\d+) ?个位"]),
    ("C29 权责与四档", [r"裁定(靠|由|按).{0,8}(投票|共识)", r"留痕.{0,4}(不必|可不|省略|免)",
                        r"〔读法〕.{0,4}(即为|就是)标准"]),
    ("C30 两例编号", [r"(功能|信息|接口|结构|关系)位\s*[4-9]",
                      r"(冷链|M3).{0,24}(\d+|十|十二) ?个位"]),
    ("C31 身份互冒", [r"(冷链|M3|合同审核).{0,8}(为|是)实测",
                      r"实测(数据|事实).{0,4}(冷链|M3|合同审核)"]),
    ("C6 三个定语", [r"(关键|基本|相关).{0,6}(可以|可)互换",
                     r"关键.{0,4}(就是|即).{0,4}(重要|优先级)",
                     r"三个定语(是同一|不分|可换)"]),
    ("C21 三档交付", [r"部分描述.{0,6}(不合格|不算)", r"完整.{0,6}十项都厚",
                      r"只定内容.{0,6}(最小集|完整)",
                      r"三档.{0,6}三种(文件|文档)"]),
    ("C25 输出与次序", [r"视图.{0,4}(齐了|齐全).{0,6}才.{0,4}评估",
                        r"后出的视图.{0,10}(升级|细化版)",
                        r"评估.{0,4}(必须|须).{0,6}先.{0,4}视图"]),
    ("C26 评估与决策", [r"评估通过.{0,2}(即|就是)\s*决定",
                        r"评估通过\s*[=＝]\s*决定", r"评估(即|就是)决策"]),
]


def read(p):
    with open(p, "rb") as f:
        return f.read().decode("utf-8-sig")


def sections48(text):
    ids = set()
    for ln in text.splitlines():
        m = re.match(r"^#{2,4}\s+(.+)$", ln)
        if not m:
            continue
        t = m.group(1).strip()
        mm = re.match(r"^([0-9]+(?:\.[0-9]+)*)\s", t)
        if mm:
            ids.add(mm.group(1))
            continue
        mc = re.match(r"^([C][0-9](?:\.[0-9]+)?)\s", t)
        if mc:
            ids.add(mc.group(1))
    return ids


def main():
    quiet = "--quiet" in sys.argv
    t48 = read(R48)
    secs = sections48(t48)
    chapters = sorted({s.split(".")[0] for s in secs})

    files = [f for f in sorted(glob.glob(os.path.join(LIB, "*.md")))
             if re.match(r"^(\d\d-|20250326)", os.path.basename(f))]
    files = [f for f in files if not os.path.basename(f).startswith("48-")]
    reports = [f for f in files if "对话记录" not in os.path.basename(f)]

    hard, bad_ptr, chapter_ref = [], [], []
    soft = collections.defaultdict(lambda: collections.Counter())
    case_claim, case_missing, case_loose = [], [], []
    bare = collections.Counter()
    ref_pat = re.compile(r"48\s*号\s*(?:v[\d.]+)?\s*§\s*([0-9]+(?:\.[0-9]+)*)")

    for f in files:
        b = os.path.basename(f)
        t = read(f)
        lines = t.splitlines()

        for i, ln in enumerate(lines, 1):
            for m in ref_pat.finditer(ln):
                s = m.group(1)
                if s in secs:
                    continue
                if "." not in s and s in chapters:
                    chapter_ref.append((b, i, s))
                else:
                    bad_ptr.append((b, i, s, ln.strip()[:110]))

            hist = any(k in ln for k in HISTORY)
            for p, why in HARD_PHRASES.items():
                if p in ln:
                    if hist or "48 号" in ln or "46 号" in ln:
                        soft[p + "〔存史／对照〕"][b] += 1
                    else:
                        hard.append((b, i, p, why, ln.strip()[:110]))
            for p, why in SOFT_PHRASES.items():
                if p in ln:
                    if p == "三把尺" and ("三种填法" in ln or "俗名" in ln or "一支填句" in ln):
                        continue
                    soft[p][b] += 1

            if "最小集" in ln and "七件" in ln and "十四" not in ln:
                soft["最小集＋七件"][b] += 1

            if "§" in ln and not any(k in ln for k in STD):
                bare[b] += 1

        # 案例：只在"声称同案同数／照 48 号 §14"的件里核事实；只提名字的另记
        cold_n = len(re.findall("冷链|M3", t))
        if cold_n:
            claim = ("同案同数" in t) or ("48 号 §14" in t) or ("与 48 号 §14" in t)
            if claim:
                miss = [w + "（" + why + "）" for w, why in COLD_FACTS if w not in t]
                if miss:
                    case_missing.append((b, miss))
                case_claim.append(b)
            elif cold_n >= 5:
                case_loose.append((b, cold_n))
        if ("合同审核" in t or "合同审批" in t) and "唯一事实源" in t:
            soft["唯一事实源"][b] += 0

    # ---------------- 打印 ----------------
    if not quiet:
        print("== 一、48 号指针 ==")
        print("  48 号节号 %d 个；指向不存在节 %d 处" % (len(secs), len(bad_ptr)))
        for b, i, s, ln in bad_ptr:
            print("    %s:%d §%s | %s" % (b, i, s, ln))
        print("  章级引用（建议写节号）%d 处" % len(chapter_ref))
        for b, i, s in chapter_ref:
            print("    %s:%d §%s" % (b, i, s))

        print("== 二、判废口径残影（硬违规）==")
        print("  %d 处" % len(hard))
        for b, i, p, why, ln in hard:
            print("    %s:%d 「%s」%s | %s" % (b, i, p, why, ln))

        print("== 三、软警示（逐句判）==")
        for p in sorted(soft):
            tot = sum(soft[p].values())
            dist = " ".join("%s×%d" % (k[:2], v) for k, v in sorted(soft[p].items()))
            print("  %-20s %4d  %s" % (p, tot, dist))

        print("== 四、案例事实 ==")
        print("  声明同案同数 %d 件：%s" % (len(case_claim), "、".join(x[:2] for x in case_claim)))
        for b, miss in case_missing:
            print("    缺事实 %s : %s" % (b[:40], "、".join(miss)))
        print("  只提案名、未声明同案同数（≥5 处）%d 件：%s"
              % (len(case_loose), "、".join("%s×%d" % (x[0][:2], x[1]) for x in case_loose)))

        print("== 五、号形：整行有 § 而整行无标准名/本报告/48 号（裸 § 候选）==")
        for b, c in bare.most_common(10):
            print("  %-56s %d" % (b[:54], c))

        print("== 六、高风险八条：违规写法扫描（C1／C3／C4／C13／C14／C15／C24／C28）==")
        for name, pats in MATRIX_RULES:
            hits = []
            for f in files:
                b = os.path.basename(f)
                for i, ln in enumerate(read(f).splitlines(), 1):
                    for p in pats:
                        if re.search(p, ln):
                            hits.append((b[:2], i, ln.strip()[:80]))
                            break
            print("  %-14s %2d 处" % (name, len(hits)))
            for h in hits:
                print("     %s:%d %s" % h)

    print("== 结论 ==")
    print("  件 %d（报告 %d／对话记录 %d）｜悬空指针 %d｜硬违规 %d"
          % (len(files), len(reports), len(files) - len(reports), len(bad_ptr), len(hard)))
    ok = (len(bad_ptr) == 0 and len(hard) == 0)
    print("  " + ("PASS（无硬违规）" if ok else "FAIL（先清硬违规）"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
