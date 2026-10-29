#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""《架构师是个怎样的物种？》腔量尺（口径 **v1.1**，第四病·表达 AI 化）

判据户口＝`00-风格参考.md` §6.21（总判＋R-腔 1~4）；施工＝`00-逐章表达优化手册.md` §四 F 桶。
本尺**只报不判**：读数只作筛子（找嫌疑人），判决回到总判——
「每一处写法都要说得出内容上的理由；只能说'上一句就是这么排的'，就是腔」。

★ 段池与段号：沿用 `00-冗余-量尺.py` 的 `paragraphs()`（R7 段池统一），
  段号＝该函数返回列表的 1 起序号，**与 `--sec`／碎段量尺同源**，可直接互查。

★ 口径 v1 的一条决定（2026-10-29 开工立）：**章末附录（附录 A~E）不入段池**。
  理由＝实测：附录 C 误解清单是 `"……"——错。` 八条连排，把它算进来破折号与等长三连
  各虚高一倍（ch08 破折 9.30→5.89‰、ch01 7.56→3.67‰）。与第三病"裸短段%混体例件"
  同型：分子里混体例件，不扣就误判。段号仍按原序编号（附录段只跳过、不重排）。

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

# ── 段池：直接复用冗余量尺（R7 统一） ─────────────────────────────────────
_spec = importlib.util.spec_from_file_location('redund_ruler', BASE)
_R = importlib.util.module_from_spec(_spec)
with contextlib.redirect_stdout(io.StringIO()):      # 复用其 paragraphs()，屏蔽其自跑输出
    _spec.loader.exec_module(_R)
paragraphs = _R.paragraphs
items = _R.items
norm_chapter = _R.norm_chapter

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
# R-腔 5 元叙述（v1.1）：作者交代"本章／这一章要做什么、不做什么"
RE_MNARR = re.compile(r'(本章|这一章|本节|这一节|这一段|这块|这一块)(?=.{0,3}?(只|不|要|是|问|讲|做|说|答|给|把))')
# 统称代名（v1.1，§6.19 第五型）：只报不判，判法是人读
RE_GENERIC = re.compile(r'(东西|这些|那些|这一套|这一类|这类|几件|几样|各地|各种|若干|同一样)')

# ── 章级配比线（R-腔 4：配比病不是有无病；上限照范本量级，不设零线） ────────
# 范本实测（--ref）：数学之美 SD 18.7／ADJ 22.4／段首短 16.7／三连 0.00／破折 0.00
#                   DDIA     SD 17.9／ADJ 18.4／段首短  7.7／三连 0.83／破折 0.83
LINE = dict(sd=16.0, adj=17.0, head_short=16.0, neat3=0.80, dash=1.80)


def neat3_count(text):
    n = 0
    for m in RE_NEAT3.finditer(text):
        a, b, c = (han(x) for x in m.groups())
        if a >= 2 and max(a, b, c) - min(a, b, c) <= 1:
            n += 1
    return n


def chapter(path):
    """返回 (指标 dict, 段表 list, 成串 list)。段号沿用 paragraphs() 的原 1 起序号。"""
    paras, no = [], 0
    for text, kind, heading in paragraphs(path):
        no += 1
        if '附录' in heading:          # 口径 v1：章末附录不入段池（段号只跳过不重排）
            continue
        paras.append((no, text, kind, heading))
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
    stats = dict(
        han=total, paras=len(paras), sents=len(sents),
        smed=statistics.median(sl) if sl else 0,
        sd=statistics.pstdev(sl) if len(sl) > 1 else 0.0,
        adj=sum(adj) / len(adj) if adj else 0.0,
        head_short=100.0 * head_short / len(paras) if paras else 0.0,
        neat3=per1k(neat3_count(body)),
        dash=per1k(len(RE_DASH.findall(body))),
        judge=per1k(len(RE_JUDGE.findall(body))),
        abst=per1k(len(RE_ABST.findall(body))),
        meta=per1k(sum(body.count(w) for w in META)),
        meta_n=sum(body.count(w) for w in META),
        mnarr=per1k(len(RE_MNARR.findall(body))),
        mnarr_multi=sum(1 for p in paras if len(RE_MNARR.findall(p[1])) >= 2),
        generic=per1k(len(RE_GENERIC.findall(body))),
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
    print('=== ① 章级五型＋两项体检（正文；剔章末附录；段号同 --sec） ===')
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
        if st['dash'] > LINE['dash']:
            bad.append(f'破折 {st["dash"]:.2f}>{LINE["dash"]}')
        if bad:
            hit += 1
            print(f'  ch{lbl:<3}{"｜".join(bad)}')
    print(f'  —— 离目标线 {hit}／{len(allst)} 件（目标线是全书终值，不是现行红线；排产看下表）')

    # ── 排产：缺口分（五型对目标线的归一化缺口之和；破折与三连权重同，节奏两项各半） ──
    def gap(st):
        g = 0.0
        g += max(0.0, (LINE['sd'] - st['sd']) / LINE['sd']) * 0.75
        g += max(0.0, (LINE['adj'] - st['adj']) / LINE['adj']) * 0.75
        g += max(0.0, (st['head_short'] - LINE['head_short']) / LINE['head_short'])
        g += max(0.0, (st['neat3'] - LINE['neat3']) / LINE['neat3'])
        g += max(0.0, (st['dash'] - LINE['dash']) / LINE['dash'])
        return g
    print('\n=== ③ 排产次序（缺口分＝五型对目标线的归一化缺口之和） ===')
    rank = sorted(((gap(st), lbl, st) for lbl, st in allst), reverse=True)
    print('序  章   缺口分  主症')
    for i, (g, lbl, st) in enumerate(rank, 1):
        z = []
        if st['dash'] > LINE['dash']:
            z.append(f'破折 {st["dash"]:.2f}')
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
        t = '\n'.join(p[0] for p in paragraphs(path))
        for w in META:
            mc[w] += t.count(w)
    nz = {k: v for k, v in mc.items() if v}
    print('  全书合计', sum(nz.values()), '处 →', dict(sorted(nz.items(), key=lambda x: -x[1])))


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
