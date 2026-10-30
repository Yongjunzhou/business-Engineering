#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""《架构师是个怎样的物种？》腔量尺（口径 **v1.3**，第四病·表达 AI 化）

判据户口＝`00-风格参考.md` §6.21（总判＋R-腔 1~4）；施工＝`00-逐章表达优化手册.md` §四 F 桶。
本尺**只报不判**：读数只作筛子（找嫌疑人），判决回到总判——
「每一处写法都要说得出内容上的理由；只能说'上一句就是这么排的'，就是腔」。

★ 段池与段号：沿用 `00-冗余-量尺.py` 的 `paragraphs()`（R7 段池统一），
  段号＝该函数返回列表的 1 起序号，**与 `--sec`／碎段量尺同源**，可直接互查。

★ 口径 v1 的一条决定（2026-10-29 开工立）：**章末附录（附录 A~E）不入段池**。
  理由＝实测：附录 C 误解清单是 `"……"——错。` 八条连排，把它算进来破折号与等长三连
  各虚高一倍（ch08 破折 9.30→5.89‰、ch01 7.56→3.67‰）。与第三病"裸短段%混体例件"
  同型：分子里混体例件，不扣就误判。段号仍按原序编号（附录段只跳过、不重排）。

★ 口径 v1.2（2026-10-29 批五开工落）：上面那条决定 **v1.1 只落了一半**——它按
  `paragraphs()` 返回的 `heading`（最近一个二／三级标题）判，而附录小节名叫
  「A 本章概念总图」「B 本章的能力级」「C 自查」，**不含"附录"二字**，故附录下的散文段
  一直留在池里（实测全书 74 段＝2.4%／3,069 汉字／17 记破折）。**v1.2 改按"块"判**
  （`## 附录` 整块剔），切法借用 `00-腔-附录核查.py` 的 `parse()`，并**每次跑都自校验**
  与 `paragraphs()` 的段数／段文本逐段相同（池漂了就报错，不许静默）。判据一字未改。
  §二／§二·补 两张底账按旧口径留痕（与前三病同池可比），**v1.2 读数见台账 §二·补2**。

★ 口径 v1.3（2026-10-30 收口批开工落；批五三位主笔各报一笔，**误报与漏报同时存在**，
  问题不在阈值在正则；判据一字未动，四笔全改在"谁算一记"上）：
  ① `RE_GENERIC` 加负向排除：**"这些年／那些年／这些天"是时间词、不是统称代名**
     （ch09 段11／段89 各误报一记）。
  ② `RE_MNARR` 的 lookahead 由 3 字放宽到 6 字，动词集并入 **引／拿／追／画／推／用／叫／
     办／交／磨／量／走／立／收**——旧口径漏"本章前面引过一次"（ch16 段84）这一类。
  ③ `RE_MNARR` **只认章／节级标记**；"这一段／这块／这一块"另立 `RE_MNARR_BLK`
     **单列体检（只报不判）**：本书"这一段"多为**过程的段**（ch04 段17"这一段是创造性的"
     ＝流程阶段），不是"本章的段落"，旧口径在 ch04 误报约 45%，且按章差别极大。
  ④ `RE_ABST` 拆两栏：标记后接**中心词**者归"**指量短语**"（只报，如 ch05 段99"这一层边界"、
     ch16 段80"这一条机制"），其余才是**抽象指（独用回指）**。中心词起首表 `CENTER` 从实测取，
     新增先加表并在台账 §一 留痕——不许凭感觉扩表。
  ⑤ 一条体例豁免：**章首几问起句**（"本章，下面这几问，你应该答得出来。"，18 章各一记）
     不进元叙述分子——它是体例装置、由 `00-章首几问-核对.py` 管，混进来会把分子顶高一成二。

  一句话记法：**①管词义／②管漏报／③管"段"的两义／④管"条＋中心词"**。
  v1.2 读数见台账 §二·补2，v1.3 读数见 §二·补3（两栏并列）。

★ 口径 v1.4（2026-10-30，用户裁「同意你的建议」后落，**只改破折这一条线的适用范围与性质**，
  其余六项读数与成串阈值一字不动）：
  **破折线由"全书单一线（章级 ≤1.80‰）"改为"分语体线"**——论证块（argue）≤1.80 立案，
  案例／章首／小结／认知反转四类 ≤2.20 只作提示；**章级破折‰ 仍报、不再是超线判据**。
  **线的性质写死：配比提示、不是刀口**（本轮不再压文）。
  取证与"为什么不把超线洗白"的看法见 LINE 上方注释与台账 §14.5；逐章读数落 §14.5 表。

读数八项（① 章级五型＋② 成串）
  ① 节奏：句长标准差 SD｜邻句长差 ADJ          ——越低越平（机器相）
  ② 段首短断言%（段首句 ≤10 汉字）              ——越高越像模板起手
  ③ 等长三连/千（三项并列且三项汉字数差 ≤1）
  ④ 破折号/千（`——`）
  ⑤ 判断式/千（才是｜就是在｜不是…而是｜不是…，是）
  ⑥ 抽象指/千（这件事｜这一点｜这一层｜这一步｜这一处｜这一条｜那件事｜这一问｜那一问）
  ⑦ 成串（R-腔 1：单发无罪、连发即病）
  ⑧ 元话语体检（首先／其次／总之……，只报不判——实测全书 0.2~1.7‰，低于两部范本）

用法（本目录下）：
    python 00-腔-量尺.py               # 全书底账（19 章＋后记）＋配比判过/超线＋元话语体检
    python 00-腔-量尺.py --ch 19       # 单章明细：逐处成串嫌疑（带段号与首句）
    python 00-腔-量尺.py --ref         # 三份范本同尺读数（目标值的来处）
    python 00-腔-量尺.py --susp        # 全书成串嫌疑总表（不截断）

口径 v1.1（2026-10-29，批二开工前）：① `—` 进 RE_NEAT3 的排除字符（旧口径把"以破折号引入的三项并列"
  整类漏掉，ch07 改完三连反升 1.97→2.36 即此）；② 新增 R-腔 5 元叙述/千 ＋ 同段 ≥2 段数；
  ③ 新增统称代名/千（§6.19 第五型，只报不判）。**判据一字未改，只改量法；旧三连读数作废。**

口径变更必须先改本文件，并在 `00-腔优化台账.md` §一 留痕。
"""
import os
import re
import sys
import glob
import io
import contextlib
import statistics
import importlib.util
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BOOK = os.path.dirname(os.path.abspath(__file__))
SAMPLE = os.path.join(BOOK, '00-风格参考-样本.md')
BASE = os.path.join(BOOK, '00-冗余-量尺.py')
APX = os.path.join(BOOK, '00-腔-附录核查.py')

# ── 段池：直接复用冗余量尺（R7 统一） ─────────────────────────────────────
_spec = importlib.util.spec_from_file_location('redund_ruler', BASE)
_R = importlib.util.module_from_spec(_spec)
with contextlib.redirect_stdout(io.StringIO()):      # 复用其 paragraphs()，屏蔽其自跑输出
    _spec.loader.exec_module(_R)
paragraphs = _R.paragraphs
items = _R.items
norm_chapter = _R.norm_chapter

# ── 块级切法（口径 v1.2）：附录核查脚本自带与 paragraphs() 的逐段自校验 ──────
_spec2 = importlib.util.spec_from_file_location('appendix_ruler', APX)
_A = importlib.util.module_from_spec(_spec2)
with contextlib.redirect_stdout(io.StringIO()):
    _spec2.loader.exec_module(_A)


def pool(path):
    """口径 v1.2 段池：按 `## ` 块剔章末附录整块；段号沿用 paragraphs() 原序（跳过不重排）。

    每跑一次都与 `paragraphs()` 比段数、逐段比段文本——池漂了立刻报错，不许静默降级。
    """
    ps = _A.parse(path)
    _A.verify(path, ps)
    return [(p['no'], p['text'], p['kind'], p['block']) for p in ps if '附录' not in p['block']]

HAN = re.compile(r'[\u4e00-\u9fff]')
han = lambda s: len(HAN.findall(s))
SENT = re.compile(r'(?<=[。！？])')

# ── 成串判腔的阈值（R-腔 1；改这里＝改口径） ──────────────────────────────
TH_NEAT3_IN_PARA = 2      # 同一段内 ≥2 次等长三连
TH_NEAT3_IN_WIN = 3       # 或相邻三段合计 ≥3 次
TH_DASH_IN_WIN = 4        # 相邻三段合计 ≥4 个破折号
TH_JUDGE_IN_PARA = 2      # 同一段内 ≥2 次判断式对举
TH_SHORT_HEAD_RUN = 3     # 连续 ≥3 段以 ≤10 汉字短句起头
WIN = 3                   # 窗口＝相邻三段
SHORT_HEAD = 10           # "短断言"的句长线（汉字）

# ── 元话语体检词（只报不判） ────────────────────────────────────────────
META = ['首先', '其次', '再次', '再者', '总之', '综上', '总而言之', '由此可见', '不难看出',
        '值得注意的是', '需要指出的是', '需要注意的是', '值得强调的是', '换句话说', '也就是说',
        '具体来说', '具体而言', '总的来说', '总体而言', '简而言之', '与此同时', '事实上', '实际上',
        '某种意义上', '从本质上', '归根结底', '这意味着', '这说明', '这告诉我们', '这就意味着',
        '我们知道', '我们发现', '我们可以看到', '让我们', '我们将', '我们会', '你会发现',
        '更重要的是', '进一步说', '更进一步', '反过来看', '另一方面', '一方面']

RE_NEAT3 = re.compile(r'([^，。；：！？、“”—]{1,10})、([^，。；：！？、“”—]{1,10})、([^，。；：！？、“”—]{1,10})')
RE_DASH = re.compile(r'——')
RE_JUDGE = re.compile(r'(才是|就是在|不是[^。！？]{1,20}?，?而是|不是[^。！？]{1,20}?，是)')
RE_ABST = re.compile(r'(这件事|这一点|这一层|这一步|这一处|这一条|那件事|这一问|那一问)')
# ④ 指量短语：标记后接中心词（"这一条＋机制"＝指物，不是抽象回指）。表从实测取，新增先留痕。
CENTER = set('线界边内备差变机规')
# R-腔 5 元叙述（v1.1；v1.3 改）：作者交代"本章／这一章要做什么、不做什么"
# ② 窗口 3→6，③ 只认章／节级
RE_MNARR = re.compile(r'(本章|这一章|本节|这一节)'
                      r'(?=.{0,6}?(只|不|要|是|问|讲|做|说|答|给|把|引|拿|追|画|推|用|叫|办|交|磨|量|走|立|收))')
# ⑤ 体例豁免：章首几问起句（18 章各一记），算体例装置不算腔
RE_MNARR_EXEMPT = re.compile(r'(本章|这一章)(?=，下面这几问)')
# ③ 段／块起手：只报不判（分不清"过程的段"与"本章的段落"）
RE_MNARR_BLK = re.compile(r'(这一段|这块|这一块)'
                          r'(?=.{0,6}?(只|不|要|是|问|讲|做|说|答|给|把|引|拿|追|画|推|用|叫|办|交|磨|量|走|立|收))')
# 统称代名（v1.1，§6.19 第五型）：只报不判，判法是人读
# ① v1.3 排除"这些年／那些年／这些天"（时间词，非统称）
RE_GENERIC = re.compile(r'(东西|这些(?!年|天|日子)|那些(?!年|天|日子)|这一套|这一类|这类|几件|几样|各地|各种|若干|同一样)')

# ── 章级配比线（R-腔 4：配比病不是有无病；上限照范本量级，不设零线） ────────
# 范本实测（--ref）：数学之美 SD 18.7／ADJ 22.4／段首短 16.7／三连 0.00／破折 0.00
#                   DDIA     SD 17.9／ADJ 18.4／段首短  7.7／三连 0.83／破折 0.83
#
# ★ 口径 v1.4（2026-10-30，用户裁「同意你的建议」后落）：**破折线由"全书单一线"改为"分语体线"，
#   并把这条线的性质写死为"配比提示、不是刀口"**。
#   来由＝收口批取证（台账 §14.5）：**全书论证块合计 1.80‰ 恰在线上**（218 记／121,192 汉字），
#   而章级超线的 11 章里超出的部分主要落在章首 2.70／认知反转 2.81／小结 2.61／案例 1.93；
#   ch10~13 四章零记（同一作者换题材就没了）——**密度是题材的函数**。
#   **但分语体并不把超线的章洗白**：逐章算论证块，仍有 **11／20 章**在 1.80 之上
#   （ch14 4.66／ch19 4.61／ch08 3.25…）。所以这一改的落点**不是"改完就达标"**，
#   而是把适用范围与性质写明：**论证块 ≤1.80 立案、其余四类 ≤2.20 提示；全部只作提示，本轮不再压文**
#   （逐处审计与两轮盲判无一记判撤；反向抽样里撤破折那处，盲判反而选回了破折）。
#   **章级破折‰ 仍报，但不再是超线判据**——跨轮对比要用它，所以留着。
LINE = dict(sd=16.0, adj=17.0, head_short=16.0, neat3=0.80, dash=1.80, dash_other=2.20)


def neat3_count(text):
    n = 0
    for m in RE_NEAT3.finditer(text):
        a, b, c = (han(x) for x in m.groups())
        if a >= 2 and max(a, b, c) - min(a, b, c) <= 1:
            n += 1
    return n


def mnarr_count(text):
    """R-腔 5 元叙述（口径 v1.3）：章／节级，剔章首几问起句。"""
    return sum(1 for m in RE_MNARR.finditer(text) if not RE_MNARR_EXEMPT.match(text, m.start()))


def abst_split(text):
    """口径 v1.3：返回（抽象指·独用回指, 指量短语·标记后接中心词）。"""
    a = q = 0
    for m in RE_ABST.finditer(text):
        if m.end() < len(text) and text[m.end()] in CENTER:
            q += 1
        else:
            a += 1
    return a, q


def chapter(path):
    """返回 (指标 dict, 段表 list, 成串 list)。段号沿用 paragraphs() 的原 1 起序号。"""
    paras = pool(path)                     # 口径 v1.2：附录按块整块剔
    body = '\n'.join(p[1] for p in paras)
    sents = []
    per_para = []
    for _, text, _, _ in paras:
        ss = [s.strip() for s in SENT.split(text) if s.strip() and han(s) >= 2]
        per_para.append(ss)
        sents.extend(ss)
    sl = [han(s) for s in sents]
    total = sum(han(p[1]) for p in paras)
    per1k = lambda n: 1000.0 * n / total if total else 0.0
    adj = [abs(sl[i] - sl[i - 1]) for i in range(1, len(sl))]
    head_short = sum(1 for ss in per_para if ss and han(ss[0]) <= SHORT_HEAD)
    ab, abq = abst_split(body)                 # v1.3：抽象指／指量短语分栏
    mn = mnarr_count(body)                     # v1.3：章／节级、剔章首几问
    blk = len(RE_MNARR_BLK.findall(body))      # v1.3：段／块起手，只报不判
    # 口径 v1.4：分语体破折（论证块的线才算线，见 LINE 上方注释）
    byk = {}
    for _, text, kind, _ in paras:
        h0, n0 = byk.get(kind, (0, 0))
        byk[kind] = (h0 + han(text), n0 + text.count('——'))
    def kpm(k):
        h0, n0 = byk.get(k, (0, 0))
        return 1000.0 * n0 / h0 if h0 else 0.0
    stats = dict(
        han=total, paras=len(paras), sents=len(sents),
        smed=statistics.median(sl) if sl else 0,
        sd=statistics.pstdev(sl) if len(sl) > 1 else 0.0,
        adj=sum(adj) / len(adj) if adj else 0.0,
        head_short=100.0 * head_short / len(paras) if paras else 0.0,
        neat3=per1k(neat3_count(body)),
        dash=per1k(len(RE_DASH.findall(body))),
        judge=per1k(len(RE_JUDGE.findall(body))),
        abst=per1k(ab), abst_n=ab,
        abstq=per1k(abq), abstq_n=abq,
        meta=per1k(sum(body.count(w) for w in META)),
        meta_n=sum(body.count(w) for w in META),
        mnarr=per1k(mn), mnarr_n=mn,
        mnarr_multi=sum(1 for p in paras if mnarr_count(p[1]) >= 2),
        mnarr_blk=per1k(blk), mnarr_blk_n=blk,
        generic=per1k(len(RE_GENERIC.findall(body))), generic_n=len(RE_GENERIC.findall(body)),
        dash_argue=kpm('argue'), dash_case=kpm('case'), dash_open=kpm('open'),
        dash_sum=kpm('summary'), dash_rev=kpm('reversal'),
        han_argue=byk.get('argue', (0, 0))[0], dash_n_argue=byk.get('argue', (0, 0))[1],
    )

    # ── R-腔 1 成串（单发无罪、连发即病） ────────────────────────────────
    susp = []
    n3 = [neat3_count(p[1]) for p in paras]
    nd = [len(RE_DASH.findall(p[1])) for p in paras]
    nj = [len(RE_JUDGE.findall(p[1])) for p in paras]
    hs = [bool(ss) and han(ss[0]) <= SHORT_HEAD for ss in per_para]
    for i, (no_, text, _, _) in enumerate(paras):
        if n3[i] >= TH_NEAT3_IN_PARA:
            susp.append((no_, '等长三连', f'本段 {n3[i]} 次', text[:60]))
        if nj[i] >= TH_JUDGE_IN_PARA:
            susp.append((no_, '判断式连用', f'本段 {nj[i]} 次', text[:60]))
    for i in range(len(paras) - WIN + 1):
        s3 = sum(n3[i:i + WIN])
        sd_ = sum(nd[i:i + WIN])
        if s3 >= TH_NEAT3_IN_WIN:
            susp.append((paras[i][0], '等长三连', f'{WIN} 段合计 {s3} 次', paras[i][1][:60]))
        if sd_ >= TH_DASH_IN_WIN:
            susp.append((paras[i][0], '破折号', f'{WIN} 段合计 {sd_} 个', paras[i][1][:60]))
    run = 0
    for i, h in enumerate(hs + [False]):
        if h:
            run += 1
            continue
        if run >= TH_SHORT_HEAD_RUN:
            susp.append((paras[i - run][0], '短断言起头', f'连 {run} 段', paras[i - run][1][:60]))
        run = 0
    # 去重（同一段同一型只留第一条）
    seen, out = set(), []
    for s in susp:
        k = (s[0], s[1])
        if k in seen:
            continue
        seen.add(k)
        out.append(s)
    return stats, paras, out


def sect_span(path, marker):
    """取 `marker` 起、至下一个同级或更高级标题之前的行区间（1 起）。"""
    lines = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n').split('\n')
    start = next(i for i, l in enumerate(lines) if l.startswith(marker))
    lvl = len(marker) - len(marker.lstrip('#'))
    for j in range(start + 1, len(lines)):
        l = lines[j]
        if re.match(r'^#{1,%d} ' % lvl, l):
            return start + 2, j + 1        # 跳过标题行本身的下一行起
    return start + 2, len(lines) + 1


def ref_stats():
    out = []
    for name, mk in [('范·A（本书 ch10）', '### 一·A'), ('范·数学之美', '### 二·5'), ('范·DDIA', '### 二·1')]:
        a, b = sect_span(SAMPLE, mk)
        tmp = os.path.join(os.environ.get('TEMP', '.'), '_cao_ref_%s.md' % abs(hash(mk)))
        open(tmp, 'w', encoding='utf-8').write(
            '\n'.join(open(SAMPLE, encoding='utf-8', newline='').read()
                      .replace('\r\n', '\n').split('\n')[a - 1:b - 1]))
        st, _, _ = chapter(tmp)
        out.append((name, st))
    return out


def rows():
    return [(norm_chapter(lbl), p) for lbl, p in items()]


def show_all():
    print('=== ① 章级五型＋两项体检（正文；段池 v1.2 按块剔章末附录、量法 v1.3；段号同 --sec） ===')
    print('章   散文汉字  段  句  句中位  句长SD  邻句长差 │ 段首短%  三连/千  破折/千  判断式  抽象指 │ 元叙述/千 同段≥2 统称/千 │ 成串')
    print('-' * 132)
    allst, allsusp = [], []
    for lbl, path in rows():
        st, _, susp = chapter(path)
        allst.append((lbl, st))
        allsusp.append((lbl, susp))
        print(f'{lbl:<5}{st["han"]:>7}{st["paras"]:>5}{st["sents"]:>4}{st["smed"]:>7.0f}{st["sd"]:>7.1f}{st["adj"]:>9.1f} │'
              f'{st["head_short"]:>7.1f}{st["neat3"]:>8.2f}{st["dash"]:>8.2f}{st["judge"]:>7.2f}{st["abst"]:>7.2f} │'
              f'{st["mnarr"]:>9.2f}{st["mnarr_multi"]:>7}{st["generic"]:>7.2f} │{len(susp):>5}')
    med = lambda k: statistics.median([s[k] for _, s in allst])
    tot = sum(s['han'] for _, s in allst)
    print('-' * 132)
    print(f'合计 散文 {tot:,}｜段 {sum(s["paras"] for _, s in allst)}｜句 {sum(s["sents"] for _, s in allst)}'
          f'｜**中位** 句中位 {med("smed"):.0f}／SD {med("sd"):.1f}／邻差 {med("adj"):.1f}'
          f'／段首短 {med("head_short"):.1f}%／三连 {med("neat3"):.2f}／破折 {med("dash"):.2f}'
          f'／判断式 {med("judge"):.2f}／抽象指 {med("abst"):.2f}／元叙述 {med("mnarr"):.2f}／统称 {med("generic"):.2f}'
          f'｜同段元叙述≥2 共 {sum(s["mnarr_multi"] for _, s in allst)} 段｜成串 {sum(len(s) for _, s in allsusp)} 处')

    print('\n=== ② 章级配比线（R-腔 4；目标线，超线只立案、不作逐句刀） ===')
    print('   ★ 口径 v1.4：破折这一行改判**论证块**（argue）≤1.80；章级破折‰ 仍报、不再是超线判据')
    hit = 0
    for lbl, st in allst:
        bad = []
        if st['sd'] < LINE['sd']:
            bad.append(f'SD {st["sd"]:.1f}<{LINE["sd"]}')
        if st['adj'] < LINE['adj']:
            bad.append(f'邻差 {st["adj"]:.1f}<{LINE["adj"]}')
        if st['head_short'] > LINE['head_short']:
            bad.append(f'段首短 {st["head_short"]:.1f}%>{LINE["head_short"]}%')
        if st['neat3'] > LINE['neat3']:
            bad.append(f'三连 {st["neat3"]:.2f}>{LINE["neat3"]}')
        if st['dash_argue'] > LINE['dash']:
            bad.append(f'论证块破折 {st["dash_argue"]:.2f}>{LINE["dash"]}（章级 {st["dash"]:.2f}）')
        if bad:
            hit += 1
            print(f'  ch{lbl:<3}{"｜".join(bad)}')
    print(f'  —— 离目标线 {hit}／{len(allst)} 件（目标线是全书终值，不是现行红线；排产看下表）')

    # ── 排产：缺口分（五型对目标线的归一化缺口之和；破折按论证块算） ──
    def gap(st):
        g = 0.0
        g += max(0.0, (LINE['sd'] - st['sd']) / LINE['sd']) * 0.75
        g += max(0.0, (LINE['adj'] - st['adj']) / LINE['adj']) * 0.75
        g += max(0.0, (st['head_short'] - LINE['head_short']) / LINE['head_short'])
        g += max(0.0, (st['neat3'] - LINE['neat3']) / LINE['neat3'])
        g += max(0.0, (st['dash_argue'] - LINE['dash']) / LINE['dash'])
        return g
    print('\n=== ③ 排产次序（缺口分＝五型对目标线的归一化缺口之和；破折用论证块） ===')
    rank = sorted(((gap(st), lbl, st) for lbl, st in allst), reverse=True)
    print('序  章   缺口分  主症')
    for i, (g, lbl, st) in enumerate(rank, 1):
        z = []
        if st['dash_argue'] > LINE['dash']:
            z.append(f'论证块破折 {st["dash_argue"]:.2f}')
        if st['neat3'] > LINE['neat3']:
            z.append(f'三连 {st["neat3"]:.2f}')
        if st['head_short'] > LINE['head_short']:
            z.append(f'段首短 {st["head_short"]:.1f}%')
        if st['sd'] < LINE['sd']:
            z.append(f'SD {st["sd"]:.1f}')
        print(f'{i:<4}ch{lbl:<3}{g:>6.2f}  {"｜".join(z) if z else "达标"}')

    print('\n=== ④ 元话语体检（只报不判；实测低于两范本，不列刀口） ===')
    mc = Counter()
    for lbl, path in rows():
        t = '\n'.join(p[1] for p in pool(path))
        for w in META:
            mc[w] += t.count(w)
    nz = {k: v for k, v in mc.items() if v}
    print('  全书合计', sum(nz.values()), '处 →', dict(sorted(nz.items(), key=lambda x: -x[1])))

    print('\n=== ⑤ 两项体检（口径 v1.3 新增，只报不判、不入任何分子） ===')
    print(f'  段／块起手（这一段／这块／这一块）全书 {sum(s["mnarr_blk_n"] for _, s in allst)} 记')
    print('    —— 分不清"过程的段"与"章节的段"，故从元叙述分子里拆出来（ch04 误报约 45%）')
    print(f'  指量短语（标记＋中心词，CENTER={"".join(sorted(CENTER))}）全书 {sum(s["abstq_n"] for _, s in allst)} 记')
    print('    —— 标记指一件具体物，不是抽象回指，故从抽象指分子里拆出来')
    print(f'  分子逐项（全书）：元叙述 {sum(s["mnarr_n"] for _, s in allst)}'
          f'｜抽象指 {sum(s["abst_n"] for _, s in allst)}｜统称 {sum(s["generic_n"] for _, s in allst)}')

    print('\n=== ⑥ 破折分语体（口径 v1.4；论证块 ≤1.80 判线，其余四类 ≤2.20 只作提示） ===')
    AGG = {}
    for lbl, st in allst:
        pass
    for k, lab, line in (('dash_argue', '论证 argue', 1.80), ('dash_case', '案例 case', 2.20),
                         ('dash_open', '章首 open', 2.20), ('dash_sum', '小结 summary', 2.20),
                         ('dash_rev', '认知反转 reversal', 2.20)):
        vals = [s[k] for _, s in allst]
        over = [lbl for lbl, s in allst if s[k] > line]
        print(f'  {lab:<18} 中位 {statistics.median(vals):.2f}‰｜最高 {max(vals):.2f}‰'
              f'｜超 {line:.2f} 的 {len(over)}／{len(allst)} 章'
              + (f'：{"／".join("ch" + x for x in over)}' if over else ''))
    print('  全书：论证块 ' + '%.2f‰' % (1000.0 * sum(s['dash_n_argue'] for _, s in allst) / sum(s['han_argue'] for _, s in allst))
          + '（' + str(sum(s['dash_n_argue'] for _, s in allst)) + ' 记／' + f'{sum(s["han_argue"] for _, s in allst):,} 汉字）'
          + '；章级破折合计 ' + str(sum(int(round(s['dash'] * s['han'] / 1000)) for _, s in allst)) + ' 记（只报，不作超线判据）')


def show_ch(arg):
    lbl = norm_chapter(arg)
    path = dict(rows()).get(lbl)
    if not path:
        print('找不到章：', arg)
        return
    st, paras, susp = chapter(path)
    print(f'=== ch{lbl} 腔量尺明细 ===')
    print(f'散文 {st["han"]}｜段 {st["paras"]}｜句 {st["sents"]}｜句中位 {st["smed"]:.0f}｜SD {st["sd"]:.1f}'
          f'｜邻差 {st["adj"]:.1f}｜段首短 {st["head_short"]:.1f}%｜三连 {st["neat3"]:.2f}｜破折 {st["dash"]:.2f}'
          f'｜判断式 {st["judge"]:.2f}｜抽象指 {st["abst"]:.2f}｜元叙述 {st["mnarr"]:.2f}/千（同段≥2 {st["mnarr_multi"]} 段）'
          f'｜统称 {st["generic"]:.2f}/千｜成串 {len(susp)} 处')
    print(f'破折分语体（口径 v1.4）：论证 {st["dash_argue"]:.2f}（线 1.80）｜案例 {st["dash_case"]:.2f}'
          f'｜章首 {st["dash_open"]:.2f}｜小结 {st["dash_sum"]:.2f}｜认知反转 {st["dash_rev"]:.2f}'
          f'（其余四类提示线 2.20、不作刀口）')
    print('\n成串嫌疑（R-腔 1；段号＝--sec 同源段号）')
    for no, typ, why, head in sorted(susp):
        print(f'  段{no:<4}{typ:<8}{why:<16}{head}')
    if not susp:
        print('  （无）')


def show_susp():
    print('=== 全书成串嫌疑（R-腔 1；单发不列） ===')
    n = 0
    for lbl, path in rows():
        _, _, susp = chapter(path)
        if not susp:
            continue
        print(f'--- ch{lbl}（{len(susp)} 处）---')
        for no, typ, why, head in sorted(susp):
            n += 1
            print(f'  段{no:<4}{typ:<8}{why:<16}{head}')
    print(f'—— 合计 {n} 处')


def main():
    a = sys.argv[1:]
    if not a:
        show_all()
    elif a[0] == '--ch' and len(a) > 1:
        show_ch(a[1])
    elif a[0] == '--susp':
        show_susp()
    elif a[0] == '--ref':
        print('=== 三份范本同尺（目标值的来处） ===')
        for name, st in ref_stats():
            print(f'{name:<18}散文 {st["han"]:>5}｜段 {st["paras"]:>3}｜句中位 {st["smed"]:>3.0f}｜SD {st["sd"]:>5.1f}'
                  f'｜邻差 {st["adj"]:>5.1f}｜段首短 {st["head_short"]:>5.1f}%｜三连 {st["neat3"]:>4.2f}'
                  f'｜破折 {st["dash"]:>4.2f}｜判断式 {st["judge"]:>4.2f}｜抽象指 {st["abst"]:>4.2f}')
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
