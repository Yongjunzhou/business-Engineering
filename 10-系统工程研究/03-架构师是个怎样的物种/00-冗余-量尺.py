#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""《架构师是个怎样的物种？》冗余量尺（口径 **v5**，段级；v1 立尺 → v2 修正八 → v3 窗到前两段 → v4 小结同章不算账 → v5 ⑦ 摘掉认知反转与小结）

用途：表达优化轮**第二病（段落冗余·对本章目的目标的支撑度）**的单一量尺。
     与既有两把尺的分工：
       · `00-风格参考-量尺.py`  管章级配比与指代三查（①~⑥）
       · `00-表达-量尺.py`      管句级与段长红线（段>150）
       · **本尺**管段级冗余——一段该不该在，以及它重复了谁。

口径 v1（2026-10-28 立；判据在 `00-风格参考.md` §6.17 断点②"重读"与
       `00-逐章表达优化手册.md` §4.4 D 冗余桶；段落层判据见 `00-冗余优化台账.md` §二）
- **段**＝散文段，与 `00-表达-量尺.py` **同一套切段法**（空行切段；豁免标题行／表格行／
  代码围栏／引用块／清单行／`**…：**` 章前件标签行）。段数因此可与那把尺逐章对齐。
- **量什么**（全部**只报不判**——判读仍靠人做"删段检验"，见 `claude-memory/pending-第二病-段落冗余.md` §四）：
  ① **段长分布**：段数｜段中位｜最长段｜**段>200（新红线，2026-10-28 用户裁）**｜段>150（旧线，留痕比较）
     ｜分语体段中位（叙事＝章首＋案例；论证＝其余正文块）——用户裁定的目标值＝叙事 ≥40、论证 ≥55
  ② **空段**：段内**无人名、无专名、无阿拉伯数字、无引号引语**——"无人物无例"的窄定义
  ③ **重复段**：本段 6-gram 有 ≥45% 在本章**别的段**也出现过——"这一段说的都是本章别处说过的"
  ④ **同义重说**：
     ④a **逐字重复片段**（≥12 汉字，跨不同段）——含跨章，最硬的一笔
     ④b **近义重说对**（2-gram Jaccard ≥0.40 且各 ≥14 汉字，非逐字）——更宽，须逐条判
     两条都**扣除在册体例件**（能力级／概念总图／判据／自查／练习／人和物／本章要回答什么／附录答案）
  ⑥ **无增量段**：段内既没有**本章此前未出现的术语**（附录 A 宪法），也没有**具体要素**（人／物／号／话）
     ——"这一段没带来新东西"的可算形态
  ⑦ **判断族**（2026-10-28 补立）：句级、章内——两句都 ≥10 汉字、共享 ≥1 个术语、长度比 ≥0.5、
     共享 2-gram ≥6、单向包含率 ≥0.30。**这是"同一判断换一种说法再说一遍"的可算形态**：
     ④ 只抓得住"抄一遍"（12 字逐字／Jaccard 0.40），换过说法的抓不住（ch10 的承重测试四处即例）。
     已扣除在册体例件、有声明回指与**排比示范**（两句首 3~4 汉字相同＝同一句式换内容）。
- **声明回指（修正八，2026-10-28 用户裁；口径 v3 把窗放到前两段）**：不只认"本段内"点了第N章／上一章，也认
  **本段所在节的散文前两段**点了。修正八（v2）只认第一段，实测 ch19 五个回收块的声明都在**节的第二段**，
  段内声明扣不到，回收被当成账；v3 把窗放到前两段，全库 ④a 197→**175**（22 对摘账，逐对清单见台账 §八 8.4）。
  本修正只豁免**本节**，不放宽"同一判断一节内最多两遍"。`HEAD_FALSE` 拦下"节首段点了源章、可点的是另一件事"的假豁免
  （v3 新增一对：ch11 案例进展① 第二段"他想起上一章那句话"指的是"决定的集合／一句涵义加一组原则"，与重复的传感器约束无关）。
- **量不了的**（口径已勘明，见台账 §二）：**"对本章目的·目标的支撑度"做不成读数**——它是判法
  （删段检验：整段拿掉，本章目的那句还立不立得住／下一段接不接得上／`00-主线与各章支撑.md` 里
  本章目标那几条它撑着哪一条）。本尺只把四条可复算的读数当筛子。
- **红线（本步口径）**：`段>200` = **0**（用户 2026-10-28 裁，替代旧 150）；其余读数只报不判。

用法（在本目录下）：
    python 00-冗余-量尺.py                # 全书底账（19 章＋后记）
    python 00-冗余-量尺.py --show 10      # 单章逐段候选清单（带节题与命中理由，附本章目的·主线）
    python 00-冗余-量尺.py --dup          # 全书逐字重复片段与近义重说对（不截断，†＝在册体例件）
    python 00-冗余-量尺.py --kw 10        # 看该章"目标术语"取到了哪些（术语宪法×权威格）

口径变更必须先改本文件，并在 `00-冗余优化台账.md` §一口径 留痕（"量法本身就是判据"）。
"""
import os
import re
import sys
import glob
import statistics
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BOOK = os.path.dirname(os.path.abspath(__file__))
SUPPORT = os.path.join(BOOK, '00-主线与各章支撑.md')
HAN = re.compile(r'[\u4e00-\u9fff]')


LIMIT_LONG = 200          # 新红线（用户 2026-10-28 裁）
OLD_LONG = 150            # 旧红线，只作留痕比较
REP_TH = 0.45             # ③a 整段重复：本章他处已说过的 6-gram 占比达到此值即候选

# ── ② 空段判据用的人与物（名单取 `00-案例设定.md` §二 团队表与配角行） ──────────
PERSONS = ['罗建', '顾言', '苏婷', '王默', '郑亮', '曹峰',          # 恒信 6
           '林涛', '石军', '吴浩', '季昭', '小周', '赵刚', '小张',   # 冰链 7
           '小冯', '刘主任', '小庄', '审计员']                      # 散见配角
PROPER = ['冰链', '恒信', 'M3', '疾控', '42010', '42020', '15288', '29148', '24748',
          'ISO', '9000', 'CMMI', 'ConOps', 'SRS', 'UAT', 'ADR']
QUOTE = re.compile(r'[“”「」『』"]')
DIGIT = re.compile(r'[0-9０-９]')


def han(s):
    return len(HAN.findall(s))


def clean(s):
    return ''.join(HAN.findall(s))


# ── 切块与归类：与 `00-风格参考-量尺.py` 同一套（口径 v3），此处只借归类 ────────
SKIP = ['参考文献', '版本变更记录']


def kind(h):
    if any(k in h for k in SKIP):
        return 'skip'
    if '误解现场' in h or '本章的人和物' in h or '本章要回答什么' in h:
        return 'open'
    if '案例进展' in h or '案例回场' in h:
        return 'case'
    if '概念总图' in h or '能力级' in h:
        return 'map'
    if '认知反转' in h:
        return 'reversal'
    if '本章判据' in h:
        return 'criteria'
    if '自查' in h:
        return 'selfcheck'
    if '练习' in h:
        return 'exercise'
    if '小结' in h:
        return 'summary'
    return 'argue'


LEAD = re.compile(r'^\*\*([^*]{1,40})\*\*')


def items():
    """(标签, 路径) —— 19 章＋后记（附录为查阅件，本尺不扫）。"""
    out = []
    for f in sorted(glob.glob(os.path.join(BOOK, '*.md'))):
        n = os.path.basename(f)
        m = re.match(r'^(\d\d)-第(\d+)章-', n)
        if m and '从教材到问题分析' not in n:
            out.append((m.group(2).zfill(2), f))
    post = os.path.join(BOOK, '20-后记.md')
    if os.path.exists(post):
        out.append(('后', post))
    return out


def is_prose(t):
    t = t.strip()
    if not t:
        return False
    for pre in ('#', '|', '>', '```', '---', '- ', '* ', '+ ', '　'):
        if t.startswith(pre):
            return False
    if re.match(r'^\d+[.、)]\s', t):
        return False
    if re.match(r'^\*\*[^*]+：\*\*', t):
        return False
    return True


def paragraphs(path):
    """返回 [(段文本, 语体 kind, 所在块标题)]。

    切段法与 `00-表达-量尺.py` **逐字一致**（空行切段＋散文行豁免）；
    只在读进每行时多记一个"当前块标题"，供归语体与定位置。
    """
    out, buf = [], []
    heading, in_code = '', False
    inline = False
    with open(path, encoding='utf-8') as f:
        head_txt = f.read()
    inline = ('**误解现场。**' in head_txt) or ('**误解现场**。' in head_txt)

    def flush():
        if not buf:
            return
        p = ' '.join(buf)
        label = ''
        m = LEAD.match(p)
        if m:
            label = m.group(1)
        k = kind(label) if (inline and label and kind(label) != 'argue') else kind(heading)
        out.append((p, k, heading))
        del buf[:]

    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.strip().startswith('```'):
                in_code = not in_code
                flush()
                continue
            if in_code:
                continue
            if re.match(r'^#{2,3} ', line):
                flush()
                heading = re.sub(r'^#+\s*', '', line).strip()
                if any(s in heading for s in SKIP):
                    heading = '【跳过】' + heading
                continue
            if not line.strip():
                flush()
                continue
            if is_prose(line):
                if heading.startswith('【跳过】'):
                    continue          # 参考文献／版本记录整块不计
                buf.append(line.strip())
            else:
                flush()
    flush()
    return out


def sentences(p):
    return [x for x in re.split(r'(?<=[。！？])', p) if han(x)]


def grams(s, n):
    c = clean(s)
    return {c[i:i + n] for i in range(len(c) - n + 1)} if len(c) >= n else set()


# ── 权威格：从 `00-主线与各章支撑.md` §二 表取「目的＋主线」两格 ──────────────────
def goal_texts():
    """从权威表取每章「目的＋主线」原文；返回 {章号: (目的, 主线)}。"""
    out = {}
    if not os.path.exists(SUPPORT):
        return out
    for ln in open(SUPPORT, encoding='utf-8'):
        if not ln.startswith('|'):
            continue
        cells = [c.strip() for c in ln.strip().strip('|').split('|')]
        if len(cells) < 5:
            continue
        m = re.search(r'\*\*(\d{1,2})\s', cells[0])
        if not m:
            continue
        out[m.group(1).zfill(2)] = (cells[1], cells[2])
    return out


TERMS_PATH = os.path.join(BOOK, '21-附录.md')
TERM_RE = re.compile(r'^\*\*(T-\d+)[　 ]+([^*]+)\*\*')


def terms():
    """附录 A 术语表（术语宪法）里的术语名——⑤ 的目标词只从"宪法"里取，不从散文片段里拼。"""
    out = []
    if not os.path.exists(TERMS_PATH):
        return out
    for ln in open(TERMS_PATH, encoding='utf-8'):
        m = TERM_RE.match(ln.strip())
        if not m:
            continue
        for name in re.split(r'\s*/\s*', m.group(2)):
            name = name.strip()
            if 2 <= len(name) <= 14:
                out.append(name)
    return out


def keywords(goal):
    """本章「目的＋主线」两格里点到的术语（附录 A 宪法）——只作 `--show` 的上下文，不作读数。"""
    keep = []
    for t in TERMS:
        if t in goal and t not in keep:
            keep.append(t)
    return keep


RECALL = re.compile(r'第\s*[0-9一二三四五六七八九十百]+\s*章|上一章|前一章|前面第')


def recall(p):
    """有声明回指：段里点了"第N章／上一章"——那是本书的结构（逐章回收），不是冗余。"""
    return bool(RECALL.search(p))


def concrete(p):
    """段内的**具体要素**：人名／专名／阿拉伯数字／引号引语（与 ② 空段同一套判据）。"""
    return (any(n in p for n in PERSONS) or any(n in p for n in PROPER)
            or bool(DIGIT.search(p)) or bool(QUOTE.search(p)))


# ── 读全书 ───────────────────────────────────────────────────────────────────
TERMS = terms()
data = {}     # 章号 -> dict(paras=[(文本,kind,heading)], kw=[...], gained=[bool])
path_of = {}
for tag, path in items():
    path_of[tag] = path
    paras = paragraphs(path)
    text = ''.join(p[0] for p in paras)
    data[tag] = dict(paras=paras, text=text, kw=None)

GOALS = goal_texts()
for tag, d in data.items():
    d['kw'] = keywords(GOALS[tag][0] + ' ' + GOALS[tag][1]) if tag in GOALS else []
    # ⑥ 无增量：按章内顺序走，记"这一段有没有带来新东西"——
    #   ① 新术语（附录 A 的术语，本章此前没出现过）或 ② 具体要素（人／物／号／话）。
    seen, gained = set(), []
    for p, _k, _h in d['paras']:
        new_terms = [t for t in TERMS if t in p and t not in seen]
        seen.update(t for t in TERMS if t in p)
        gained.append(bool(new_terms) or concrete(p))
    d['gained'] = gained


# ── 修正八（2026-10-28 用户裁）：声明回指也认"本节第一段" ───────────────────────
# 修正四只认段内点了"第N章／上一章"。实测 ch19 两个回收块（19.3.2 点第 12 章、19.4.1 点第 15 章）
# 声明都在同节第一段，段内声明扣不到，六对被当成账。本节边界与 paragraphs() 同一套切法。
# **声明只豁免本节**，不放宽台账 §八 的"同一判断一节内最多两遍"。
# HEAD_FALSE：节首段虽点了源章，可点的是另一件事——人工一瞥拦下，不豁免。
HEAD_FALSE = {
    ('03', '04'): '目的展开成目标',   # ch04 §4.3.1 节首段点第3章说的是需求三形态，重复的是"目标→需求"转化
    ('10', '11'): '新增传感器类型',   # ch11 案例进展① 第二段"他想起上一章那句话"指的是"决定的集合／一句涵义加一组原则"，
                                     # 与重复的"新增传感器类型不得破坏已有的…"无关（口径 v3 扩到前两段后新露出的一对假豁免）
}


def head_first(paras):
    """每节的第一段散文段（paragraphs() 只收散文，表格／引文／清单天然不在内）。"""
    m, cur = {}, None
    for p, _k, h in paras:
        if h != cur:
            cur = h
        if h not in m:
            m[h] = p
    return m


HEAD = {tag: head_first(d['paras']) for tag, d in data.items()}


def head_two(paras):
    """每节的**前两段**散文段（口径 v3，2026-10-28 用户裁：修正八的窗由一节首段放到前两段）。

    理由不是为降数，而是**窗口设错的代价落在判读工上**：A 账第一、二批共 9 对的声明都落在节的
    第二段，每批都要重新判一遍"这是回收吗"，而答案早已由裁定 3 定死。窗放到前两段，这 9 对转入
    "已声明"，判读单只留一行。松的只是位置：仍要求**点的是对面那一章**，`HEAD_FALSE` 拦假豁免不变。
    """
    m, cur = {}, None
    for p, _k, h in paras:
        if h != cur:
            cur = h
            m[h] = []
        if p not in m[h] and len(m[h]) < 2:
            m[h].append(p)
    return m


HEAD2 = {tag: head_two(d['paras']) for tag, d in data.items()}


def _points_to(text, tag, other):
    """text 里的声明是不是指向 other 那一章（数字章号，或相邻章的"上一章／前一章"）。"""
    if other.isdigit():
        for m in re.finditer(r'第\s*(\d+)\s*章', text):
            if m.group(1).zfill(2) == other:
                return True
    if tag.isdigit() and other.isdigit():
        return (int(other) == int(tag) - 1) and bool(re.search(r'上一章|前一章', text))
    return False


def declared(tag, pi, other):
    """声明回指（修正八＋v3）：本段点了，或本段所在节的**前两段**点了——点的必须是**对面那一章**。"""
    p, _k, h = data[tag]['paras'][pi]
    if recall(p):
        return True
    for hp in HEAD2[tag].get(h, []):
        if hp != p and _points_to(hp, tag, other):
            return True
    return False


def stat_long(d):
    lens = [han(p[0]) for p in d['paras']]
    narr = [han(p[0]) for p in d['paras'] if p[1] in ('open', 'case')]
    argue = [han(p[0]) for p in d['paras'] if p[1] == 'argue']
    med = lambda a: statistics.median(a) if a else 0
    return dict(n=len(lens), med=med(lens), mx=max(lens) if lens else 0,
                over200=sum(1 for v in lens if v > LIMIT_LONG),
                over150=sum(1 for v in lens if v > OLD_LONG),
                narr=len(narr), narr_med=med(narr), argue=len(argue), argue_med=med(argue))


def blank(p):
    """② 空段：无人、无专名、无阿拉伯数字、无引号引语。"""
    t = p
    if any(n in t for n in PERSONS):
        return False
    if any(n in t for n in PROPER):
        return False
    if DIGIT.search(t):
        return False
    if QUOTE.search(t):
        return False
    return True


def para_repeat(tag, pi):
    """③ 新信息量：本段 6-gram 中**在本章别的段也出现过**的比例（重复率）。

    重复率 ≥ REP_TH → 重复段候选（这一段说的都是本章别处说过的）。
    低值 = 新信息多；高值 = 复述。**这是本尺最硬的一条读数**，因为它直接对应"重读"。
    """
    d = data[tag]
    g = d['g6'][pi]
    if not g:
        return 0.0
    df = d['df6']
    return sum(1 for x in g if df.get(x, 0) >= 2) / len(g)


def exempt(kind_, head):
    """在册体例件：能力级／概念总图／本章判据／自查／练习／章节人和物／附录答案。

    §4.5 不动项——它们的重复是体例，不是冗余；④ 三种重复读数**扣除**这些位置后再算。
    """
    if kind_ in ('map', 'criteria', 'selfcheck', 'exercise'):
        return True
    if '人和物' in (head or '') or '答案' in (head or '') or '本章要回答什么' in (head or ''):
        return True
    return False


def summary_same_chapter(ta, ha, tb, hb):
    """口径 v4（2026-10-28 用户裁「小结与本章正文的重复不算账」）。

    **小结的功能就是把人已经在正文读过的判词再收一遍**——把它当账，等于要求小结不复述，
    那是另一本书的体例。窗口只放到**同章**：小结与**别的章**之间的重复仍入账（那属跨章回收，
    由裁定 3 的声明规则管）。
    """
    if ta != tb:
        return False
    return ('小结' in (ha or '')) or ('小结' in (hb or ''))


# ③ 每章 6-gram 与段内 df
for tag, d in data.items():
    g6, df6 = [], defaultdict(int)
    for p, _k, _h in d['paras']:
        gs = grams(p, 6)
        g6.append(gs)
        for x in gs:
            df6[x] += 1
    d['g6'], d['df6'] = g6, df6

# ④a 逐字重复片段（≥12 汉字，跨不同段）
FRAG = 12
frag_idx = defaultdict(set)      # 片段 -> {(item, para_idx)}
for tag, d in data.items():
    for pi, (p, _k, _h) in enumerate(d['paras']):
        c = clean(p)
        for i in range(len(c) - FRAG + 1):
            frag_idx[c[i:i + FRAG]].add((tag, pi))
repeated = {g: v for g, v in frag_idx.items() if len(v) >= 2}


def longest_run(tag, pi, gs):
    """同一段落对里的若干 12-gram 合并成一条最长连续片段（段落 A 一侧的跨度）。"""
    c = clean(data[tag]['paras'][pi][0])
    spans = sorted((c.find(g), g) for g in gs if c.find(g) >= 0)
    best, lo, hi = 0, None, None
    for st, g in spans:
        if lo is None:
            lo, hi = st, st + len(g)
        elif st <= hi:
            hi = max(hi, st + len(g))
        else:
            best = max(best, hi - lo)
            lo, hi = st, st + len(g)
    if lo is not None:
        best = max(best, hi - lo)
    return best


def dup_pairs():
    """逐字重复：同片段出现在不同段（可同章可跨章）；每对一条，按跨度降序。"""
    seen = {}
    for g, locs in repeated.items():
        locs = sorted(locs)
        for a in range(len(locs)):
            for b in range(a + 1, len(locs)):
                seen.setdefault((locs[a], locs[b]), []).append(g)
    out = {}
    for key, gs in seen.items():
        (ta, pa), (tb, pb) = key
        n = longest_run(ta, pa, gs)
        if n > out.get(key, 0):
            out[key] = n
    res = []
    for key, n in out.items():
        (ta, pa), (tb, pb) = key
        c = clean(data[ta]['paras'][pa][0])
        # 取跨度最长的那条片段原文（取段 A 上最长合并段）
        best_txt, best_len = '', 0
        spans = sorted((c.find(g), g) for g in seen[key] if c.find(g) >= 0)
        lo = hi = None
        for st, g in spans:
            if lo is None:
                lo, hi = st, st + len(g)
            elif st <= hi:
                hi = max(hi, st + len(g))
            else:
                if hi - lo > best_len:
                    best_txt, best_len = c[lo:hi], hi - lo
                lo, hi = st, st + len(g)
        if lo is not None and hi - lo > best_len:
            best_txt, best_len = c[lo:hi], hi - lo
        pa_txt, pb_txt = data[ta]['paras'][pa][0], data[tb]['paras'][pb][0]
        body_ex = (exempt(data[ta]['paras'][pa][1], data[ta]['paras'][pa][2])
                   or exempt(data[tb]['paras'][pb][1], data[tb]['paras'][pb][2])
                   or summary_same_chapter(ta, data[ta]['paras'][pa][2],
                                           tb, data[tb]['paras'][pb][2])
                   or recall(pa_txt) or recall(pb_txt))
        head_ex = (not body_ex) and (declared(ta, pa, tb) or declared(tb, pb, ta))
        if head_ex and (best_txt.startswith(HEAD_FALSE.get((ta, tb), '\0'))
                        or best_txt.startswith(HEAD_FALSE.get((tb, ta), '\0'))):
            head_ex = False          # 人工一瞥：假豁免，仍算账
        ex = '†' if body_ex else ('‡' if head_ex else '')
        res.append((ta, pa, tb, pb, n, best_txt, ex))
    return sorted(res, key=lambda x: -x[4])


# ④b 近义重说对（2-gram Jaccard）
sents = []
for tag, d in data.items():
    for pi, (p, _k, _h) in enumerate(d['paras']):
        for s in sentences(p):
            c = clean(s)
            if len(c) >= 14:
                sents.append((tag, pi, s, frozenset(c[i:i + 2] for i in range(len(c) - 1))))
idx2 = defaultdict(list)
for si, (_t, _p, _s, g) in enumerate(sents):
    for x in g:
        idx2[x].append(si)
near = []
for si, (t1, p1, s1, g1) in enumerate(sents):
    cand = defaultdict(int)
    for x in g1:
        if len(idx2[x]) <= 40:
            for sj in idx2[x]:
                if sj > si:
                    cand[sj] += 1
    for sj, shared in cand.items():
        if shared < 6:
            continue
        t2, p2, s2, g2 = sents[sj]
        if (t1, p1) == (t2, p2):
            continue
        j = shared / len(g1 | g2)
        if j >= 0.40:
            near.append((round(j, 2), t1, p1, s1, t2, p2, s2))
near.sort(key=lambda x: -x[0])


# ⑦ 判断族：**同一章里同一判断换几种说法**（2026-10-28 补立；④ 的 12 字逐字与 0.40 近义都够不着它）
#   判据：两句都 ≥10 汉字、共享 ≥1 个术语（附录 A 宪法）、2-gram 单向包含率 ≥ FAM_TH。
#   **为什么用"包含率"而不是 Jaccard**：四次说法长短不一（一句是定义、一句是应用），长句套住短句才是常态。
#   **为什么要术语作门**：只有 2-gram 相似会淹在"这件事/这个系统"里，术语是"说同一件事"的锚。
FAM_TH = 0.30
fam = {}                      # tag -> [(包含率, 段i, 句i, 段j, 句j, 共享术语)]
for tag, d in data.items():
    pool = []
    for pi, (p, k, h) in enumerate(d['paras']):
        if exempt(k, h) or recall(p):
            continue
        # 口径 v5（2026-10-28 用户裁）：一侧落在「小结」或「认知反转」的对不入账——与 v4 摘
        # ④a 的"小结同章"同理：小结的功能就是复述本章判词，认知反转是章末回炉，都是体例。
        if ('小结' in (h or '')) or ('认知反转' in (h or '')):
            continue
        for s in sentences(p):
            if han(s) < 10:
                continue
            pool.append((pi, s, grams(s, 2), frozenset(t for t in TERMS if t in s)))
    out = []
    for i in range(len(pool)):
        for j in range(i + 1, len(pool)):
            pi, si, gi, ti = pool[i]
            pj, sj, gj, tj = pool[j]
            shared_t = ti & tj
            if not shared_t:
                continue
            li, lj = len(gi), len(gj)
            if not li or not lj:
                continue
            # 长度悬殊的两句不算重说：一句短断语（"XX 还没验"）的 2-gram 必然被长句整段包住，
            # 那是"提到同一个词"，不是"说同一件事"。故要求两句长度比 ≥0.5。
            if min(li, lj) / max(li, lj) < 0.5:
                continue
            shared = len(gi & gj)
            if shared < 6:
                continue
            c = shared / min(li, lj)
            if c >= FAM_TH:
                out.append((round(c, 2), pi, si, pj, sj, sorted(shared_t)))
    fam[tag] = sorted(out, key=lambda x: -x[0])
# 排比示范（同一句式换内容，如"第一处……第二处……""上一版方案……文档目录……"）不算重说：
# 判据＝两句去标点后**首 3 汉字相同**，或首 4 汉字相同——这是并列，不是复述。
def parallel(si, sj):
    a, b = clean(si), clean(sj)
    return a[:3] == b[:3] or a[:4] == b[:4]


fam_par = {t: sum(1 for x in v if parallel(x[2], x[4])) for t, v in fam.items()}
fam = {t: [x for x in v if not parallel(x[2], x[4])] for t, v in fam.items()}


# ── 输出 ─────────────────────────────────────────────────────────────────────
if '--kw' in sys.argv:
    want = sys.argv[sys.argv.index('--kw') + 1].strip().zfill(2) if len(sys.argv) > sys.argv.index('--kw') + 1 else ''
    print('=== 本章目标术语（「目的＋主线」两格点到的术语；取自附录 A 宪法） ===')
    for tag in ([want] if want in data else list(data)):
        d = data[tag]
        print('ch{}（{} 个）：{}'.format(tag, len(d['kw']), '、'.join(d['kw'])))
    sys.exit(0)

if '--dup' in sys.argv:
    print('=== ④a 逐字重复片段（≥{} 汉字，跨不同段；†＝在册体例件或段内声明，‡＝节首声明） ==='.format(FRAG))
    ps = dup_pairs()
    for ta, pa, tb, pb, n, txt, ex in ps:
        mark = '跨章' if ta != tb else '同章'
        print('  {} {} 字｜ch{}〔{}〕↔ ch{}〔{}〕：「{}」'.format(
            ex or ' ', n, ta, data[ta]['paras'][pa][2][:12] or '—',
            tb, data[tb]['paras'][pb][2][:12] or '—', txt[:36]))
    print()
    print('=== ④b 近义重说对（2-gram Jaccard ≥0.40；非逐字，须逐条判；†＝在册体例件） ===')
    for j, t1, p1, s1, t2, p2, s2 in near:
        ex = (exempt(data[t1]['paras'][p1][1], data[t1]['paras'][p1][2])
              or exempt(data[t2]['paras'][p2][1], data[t2]['paras'][p2][2])
              or declared(t1, p1, t2) or declared(t2, p2, t1))
        print('  {} {:.2f} ch{}〔{}〕「{}」↔ ch{}〔{}〕「{}」'.format(
            '†' if ex else ' ', j, t1, data[t1]['paras'][p1][2][:10] or '—', clean(s1)[:22],
            t2, data[t2]['paras'][p2][2][:10] or '—', clean(s2)[:22]))
    print('  共 {} 对'.format(len(near)))
    sys.exit(0)

rows = []
PS = dup_pairs()
inv_a, inv_b = set(), set()
for ta, pa, tb, pb, n, txt, ex in PS:
    if ex:
        continue
    inv_a.add((ta, pa))
    inv_a.add((tb, pb))
for j, t1, p1, s1, t2, p2, s2 in near:
    if (exempt(data[t1]['paras'][p1][1], data[t1]['paras'][p1][2])
            or exempt(data[t2]['paras'][p2][1], data[t2]['paras'][p2][2])
            or declared(t1, p1, t2) or declared(t2, p2, t1)):
        continue
    inv_b.add((t1, p1))
    inv_b.add((t2, p2))

for tag, d in data.items():
    s = stat_long(d)
    bl = rep = gain = heavy = 0
    ia = ib = 0
    for pi, (p, _k, h) in enumerate(d['paras']):
        is_blank = blank(p)
        r = para_repeat(tag, pi)
        is_rep = r >= REP_TH and not exempt(_k, h)
        no_gain = not d['gained'][pi]
        bl += is_blank
        rep += is_rep
        gain += no_gain
        heavy += no_gain and is_rep
        ia += (tag, pi) in inv_a
        ib += (tag, pi) in inv_b
    fp = fam.get(tag) or []
    fs = len({(x[1], x[2]) for x in fp} | {(x[3], x[4]) for x in fp})
    rows.append(dict(tag=tag, **s, blank=bl, rep=rep, gain=gain, heavy=heavy,
                     inv_a=ia, inv_b=ib, fam=len(fp), fam_s=fs, tot=han(d['text'])))

if '--blind' in sys.argv:
    i = sys.argv.index('--blind')
    want = sys.argv[i + 1].strip().zfill(2) if len(sys.argv) > i + 1 else '10'
    path = path_of.get(want)
    d = data.get(want)
    if not d or not path:
        print('--blind 用法：--blind 10（两位章号）［--out 输出路径］；未找到该章。')
        sys.exit(1)
    # ⑨ 冷读用的**盲读稿**：读者看到的就是读者在纸上看到的那一页——
    #   节题与块题都在，**清单项／表格／引文原样保留**（缺了它们，读者会误报"承诺了却没给"），
    #   段号只挂在散文段上（与 --sec／--show 同一套）；不带章目标、不带任何判据与提示。
    buf, nxt = [], []          # nxt＝待输出的非散文块
    pi = [-1]
    in_fence = False
    skip_block = False

    out = []

    def emit(s=''):
        out.append(s)

    def flush_other():
        if nxt:
            kind = '原样'
            emit('〔紧接第{}段·原样〕'.format(pi[0]) if pi[0] >= 0 else '〔本节开头·原样〕')
            for l in nxt:
                emit(l)
            emit()
            del nxt[:]

    def flush_prose():
        if buf and not skip_block:
            pi[0] += 1
            emit('[段{}] {}'.format(pi[0], ' '.join(buf)))
            emit()
        del buf[:]

    for line in open(path, encoding='utf-8').read().split('\n'):
        t = line.rstrip()
        s = t.strip()
        if s.startswith('```'):
            flush_prose()
            nxt.append(t)
            in_fence = not in_fence
            continue
        if in_fence:
            nxt.append(t)
            continue
        if re.match(r'^#{2,3} ', s):
            flush_prose(); flush_other()
            lvl = '■ 节题' if s.startswith('###') else '◆ 块题'
            title = re.sub(r'^#+\s*', '', s).strip()
            skip_block = any(k in title for k in SKIP)
            emit()
            emit('{}：{}'.format(lvl, title))
            emit()
            continue
        if not s:
            flush_prose()          # 空行只收散文段；清单／表格／引文连续跨空行，合成一块
            continue
        if is_prose(t):
            if skip_block:
                continue
            if nxt:
                flush_other()
            buf.append(s)
        else:
            flush_prose()
            nxt.append(t)
    flush_prose(); flush_other()

    text = '=== 盲读稿 ch{}（读者看到的这一份就是全部） ===\n\n'.format(want) + '\n'.join(out) + '\n'
    if '--out' in sys.argv:
        dst = sys.argv[sys.argv.index('--out') + 1]
        with open(dst, 'w', encoding='utf-8') as f:
            f.write(text)
        print('已写出盲读稿：{}（{} 字符，{} 段）'.format(dst, len(text), pi[0] + 1))
    else:
        sys.stdout.write(text)
    sys.exit(0)

if '--sec' in sys.argv:
    i = sys.argv.index('--sec')
    want = sys.argv[i + 1].strip().zfill(2) if len(sys.argv) > i + 1 else '10'
    d = data.get(want)
    if not d:
        print('--sec 用法：--sec 10（两位章号）；未找到该章。')
        sys.exit(1)
    print('=== 节级判读单 ch{}（⑧ 判法：节题＝承诺；逐段打 兑现／铺陈／重复／离题） ==='.format(want))
    if want in GOALS:
        print('本章目的：{}'.format(re.sub(r'\*\*', '', GOALS[want][0])[:160]))
        print('本章主线：{}'.format(re.sub(r'\*\*', '', GOALS[want][1])[:200]))
    print()
    order, grouped = [], {}
    for pi, (p, k, h) in enumerate(d['paras']):
        if h not in grouped:
            grouped[h] = []
            order.append(h)
        grouped[h].append(pi)
    fmap = {}
    for c, pi, si, pj, sj, tt in (fam.get(want) or []):
        fmap.setdefault(pi, []).append((c, pj, si, sj, tt))
        fmap.setdefault(pj, []).append((c, pi, sj, si, tt))
    for h in order:
        pis = grouped[h]
        terms_here = sorted({t for pi in pis for t in TERMS if t in d['paras'][pi][0]})
        print('【{}】{} 段｜本节术语：{}'.format(
            h or '（无题）', len(pis), '、'.join(terms_here[:12]) or '（无）'))
        for pi in pis:
            p, k, _ = d['paras'][pi]
            first = re.split(r'(?<=[。！？])', p)[0][:40]
            mark = ''
            if exempt(k, h):
                mark = '〔体例件·不动〕'
            elif para_repeat(want, pi) >= REP_TH:
                mark = '〔③本次与本章别处重复〕'
            print('  [{:>3}] {:>3}字 {}{}\n        {}'.format(pi, han(p), mark, '', first))
            for c, pj, si, sj, tt in (fmap.get(pi) or [])[:3]:
                if pj > pi:
                    print('        ↳ ⑦ {:.2f} 与段{}同判断〔{}〕：{}'.format(
                        c, pj, '、'.join(tt), sj[:34]))
        print()
    sys.exit(0)

if '--show' in sys.argv:
    i = sys.argv.index('--show')
    want = sys.argv[i + 1].strip().zfill(2) if len(sys.argv) > i + 1 else '10'
    d = data.get(want)
    if not d:
        print('--show 用法：--show 10（两位章号）；未找到该章。')
        sys.exit(1)
    print('=== 单章逐段候选（ch{}）：硬证据＝③本章内重复／④全书同义重说｜软迹象＝②空段／⑥无增量 ==='.format(want))
    if want in GOALS:
        print('本章目的：{}'.format(re.sub(r'\*\*', '', GOALS[want][0])[:200]))
        print('本章主线：{}'.format(re.sub(r'\*\*', '', GOALS[want][1])[:260]))
    print('本章目标术语（{}）：{}'.format(len(d['kw']), '、'.join(d['kw'])))
    print()
    hard, soft = [], []
    for pi, (p, k, h) in enumerate(d['paras']):
        flags = []
        r = para_repeat(want, pi)
        if r >= REP_TH and not exempt(k, h):
            flags.append('③重复{:.0%}'.format(r))
        if (want, pi) in inv_a:
            flags.append('④a逐字重复')
        if (want, pi) in inv_b:
            flags.append('④b近义重说')
        is_hard = any(f[0] in '③④' for f in flags)
        if blank(p):
            flags.append('②空段')
        if not d['gained'][pi]:
            flags.append('⑥无增量')
        if not flags:
            continue
        line = '[{:>3}] {} 段{}字｜{}\n     {}{}'.format(
            pi, h[:20] or '—', han(p), '／'.join(flags), p[:56],
            '…' if len(p) > 56 else '')
        (hard if is_hard else soft).append(line)
    print('【一 有硬证据的段】{} 段'.format(len(hard)))
    for x in hard:
        print(x)
    print()
    print('【二 只有软迹象的段】{} 段'.format(len(soft)))
    for x in soft:
        print(x)
    print()
    print('ch{}：硬 {} 段｜软 {} 段｜全章 {} 段'.format(want, len(hard), len(soft), len(d['paras'])))
    print()
    fp = fam.get(want) or []
    print('【三 ⑦ 判断族（同一章里同一判断换了几种说法）】{} 对，涉及 {} 句'.format(
        len(fp), len({(x[1], x[2]) for x in fp} | {(x[3], x[4]) for x in fp})))
    for c, pi, si, pj, sj, tt in fp:
        print('  {:.2f} 段{}↔段{}〔{}〕'.format(c, pi, pj, '、'.join(tt)))
        print('     A: {}'.format(si[:70]))
        print('     B: {}'.format(sj[:70]))
    sys.exit(0)

print('=== ① 段长与语体（红线 v2：段>{} = 0；用户 2026-10-28 裁） ==='.format(LIMIT_LONG))
print('件   散文汉字  段数  段中位  最长段  >{}  >{}   叙事段(段数/中位)  论证段(段数/中位)'.format(
    LIMIT_LONG, OLD_LONG))
for r in rows:
    print('{}  {:>8}  {:>4}  {:>6}  {:>6}  {:>4}  {:>3}   {:>8} / {:<3}   {:>8} / {:<3}'.format(
        r['tag'], r['tot'], r['n'], int(r['med']), r['mx'], r['over200'], r['over150'],
        r['narr'], int(r['narr_med']), r['argue'], int(r['argue_med'])))
tot = sum(r['tot'] for r in rows)
print('—' * 100)
print('合计散文 {} 汉字｜段 {}｜段>{} 共 {} 段｜段>{} 共 {} 段｜段中位全书 {}'.format(
    tot, sum(r['n'] for r in rows), LIMIT_LONG,
    sum(r['over200'] for r in rows), OLD_LONG, sum(r['over150'] for r in rows),
    int(statistics.median([r['med'] for r in rows]))))

print()
print('=== ② ③ ⑥ ④ ⑦ 只报不判：空段／重复段／无增量段／同义重说／判断族 ===')
print('件   段数  ②空段 占比  ③重复段(≥{:.0%}) 占比  ⑥无增量 占比  ④a涉及段 ④b涉及段  ⑦句对 ⑦涉及句'.format(REP_TH))
for r in rows:
    p = lambda v: 100.0 * v / r['n'] if r['n'] else 0.0
    print('{}  {:>4}  {:>5}  {:>5.1f}%  {:>9}  {:>5.1f}%  {:>7}  {:>5.1f}%  {:>7}  {:>7}  {:>5}  {:>5}'.format(
        r['tag'], r['n'], r['blank'], p(r['blank']), r['rep'], p(r['rep']),
        r['gain'], p(r['gain']), r['inv_a'], r['inv_b'], r['fam'], r['fam_s']))
print('—' * 110)
TN = sum(r['n'] for r in rows)
pc_all = lambda k: 100.0 * sum(r[k] for r in rows) / TN
print('合计（{} 段）：②空段 {} 段 {:.1f}%｜③重复段 {} 段 {:.1f}%｜⑥无增量 {} 段 {:.1f}%'
      '｜④a 涉及 {} 段｜④b 涉及 {} 段｜⑦判断族 {} 对（涉及 {} 句）'.format(
          TN, sum(r['blank'] for r in rows), pc_all('blank'),
          sum(r['rep'] for r in rows), pc_all('rep'),
          sum(r['gain'] for r in rows), pc_all('gain'),
          sum(r['inv_a'] for r in rows), sum(r['inv_b'] for r in rows),
          sum(r['fam'] for r in rows), sum(r['fam_s'] for r in rows)))

print()
print('=== ④ 同义重说（④a 逐字 ≥{} 汉字；④b 近义 Jaccard ≥0.40） ==='.format(FRAG))
ps = dup_pairs()
real = [x for x in ps if not x[6]]
print('④a 逐字重复片段 {} 对（跨章 {}／同章 {}）；**扣除体例件与有声明回指后 {} 对**'.format(
    len(ps), sum(1 for x in ps if x[0] != x[2]), sum(1 for x in ps if x[0] == x[2]), len(real)))
print('  最长十对（扣除后）：')
for ta, pa, tb, pb, n, txt, ex in real[:10]:
    print('    {} 字｜ch{}「{}」↔ ch{}'.format(n, ta, txt[:30], tb))
near_real = [x for x in near
             if not (exempt(data[x[1]]['paras'][x[2]][1], data[x[1]]['paras'][x[2]][2])
                     or exempt(data[x[4]]['paras'][x[5]][1], data[x[4]]['paras'][x[5]][2])
                     or recall(data[x[1]]['paras'][x[2]][0]) or recall(data[x[4]]['paras'][x[5]][0]))]
print('④b 近义重说对 {} 对；**扣除体例件与有声明回指后 {} 对**'.format(len(near), len(near_real)))

print()
print('=== 一页诊断（按 ④涉及段占比 → ③重复段 → ⑥无增量 排序；只作筛子，判读靠删段检验） ===')
rank = sorted(rows, key=lambda r: (-((r['inv_a'] + r['inv_b']) / r['n'] if r['n'] else 0),
                                   -(r['rep'] / r['n'] if r['n'] else 0),
                                   -(r['gain'] / r['n'] if r['n'] else 0)))
for i, r in enumerate(rank, 1):
    p = lambda v: 100.0 * v / r['n'] if r['n'] else 0.0
    print('{:>2}. ch{:<3} ④a {:>3} 段 ④b {:>3} 段｜③重复段 {:>3} 段｜⑥无增量 {:>5.1f}%'
          '｜②空段 {:>5.1f}%｜段中位 {:>3}｜>{} {}'.format(
              i, r['tag'], r['inv_a'], r['inv_b'], r['rep'],
              p(r['gain']), p(r['blank']), int(r['med']), LIMIT_LONG, r['over200']))
print()
print('注：三条读数都是**筛子**，不是判决——')
print('    ②"没有具体的人、物、号、话"：论证段本来就密，空段多不等于废话多；')
print('    ③"本章别处已说过"：重合率高可能是刻意回扣（回指前节、小结复述）；')
print('    ⑥"没带来新东西"：只看"新术语／新具体要素"，判不出"同一批词做出新判断"的段。')
print('    真正的判法是**删段检验**：整段拿掉，本章目的那句还立不立得住、下一段接不接得上、')
print('    `00-主线与各章支撑.md` 里本章目标那几条它撑着哪一条——三条有一条答不出，才轮到删或压。')






