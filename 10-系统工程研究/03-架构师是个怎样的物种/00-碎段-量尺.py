#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""《架构师是个怎样的物种？》碎段量尺（第三病·段落碎片化，口径 **v2**，段级）

用途：表达优化轮 **第三病（段落碎片化）** 的单一量尺。
      与既有三把尺的分工：
        · `00-风格参考-量尺.py`  章级配比与指代三查（①~⑥）
        · `00-表达-量尺.py`      句级与段长红线（段>150／>200）
        · `00-冗余-量尺.py`      段级冗余（②空段／③重复段／⑥无增量／④同义／⑦判断族）
        · **本尺**管碎段——一段是不是太短、短段是不是连成串、两段是不是粘成一段。

**段池与段号＝`00-冗余-量尺.py` 的 `paragraphs()`（逐字同一套切法）**：空行切段＋散文行豁免
（剔标题行／表格／引用块／清单行／代码围栏／`---`／`**X：**` 式字段行），因此本尺报的
**段号与 `--sec <章>` 完全同源**，可直接对判读单、台账、`--show` 互查。

量什么（**全部只报不判**——碎不碎要靠人看上下文）：

  ① **短段%**：段汉字 ≤20 的散文段 ÷ 该章散文段。全书按此排序。
  ② **短段定性五类**（本尺的核心补丁）：裸百分比会把"对白装置"与"加粗小标"算成碎段，
     后记就是现成一例（裸 25.3%，扣体例后 6.3%）——
       K0 加粗小标段（段首 `**` 起头；`**小标。**正文` 属同一段，不算短段）
       K1 **引语引导段**（以 `：` 收尾，且紧随其后的第一行是引文／对白）
       K2 **对白**（含 `：“`，或以引号起头）
       K3 体例短标（含破折号的极短标签行）
       K4 **可并**（其余——本步的刀只落这一类）
  ③ **论块短段%**：论证块内 K4 短段 ÷ 论块段。**这才是病的密度**（叙事块与章末件各有
     自己的节奏，短是体例；论证块里一句一段才是碎）。
  ④ **短段连排（三分）**：论证块内**连续 ≥2 段**都是 K4 短段——成串才是病（单发的短段
     多是落点句／推力句，判留）。**v2 补丁**：按两段之间"夹着什么"分三类——
       **ok**＝真相邻（可并，本步的刀）
       **block**＝夹着件（表／清单／引文／术语注／`####` 标题）→ 判留
       **cross**＝夹着节题（`###`）→ 跨节，判留
     2026-10-29 实测：口径 v1 报 25 串，分真相邻后只剩 **13 串**可并——**连排是"段序相邻"，
     不是"版面相接"**。
  ⑤ **上端三数（R4′ 的验线）**：论证段的**均值／P90／≥100 汉字占比**，另报章内最长段与
     ≥130 段数。范本《数学之美》二·5 的 ≥100 占比是 **25%**，本书 **3.9%**——**中位持平而
     尾部差 6.4 倍**，故验收看尾部，不看中位（见 `00-风格参考.md` §6.20 R4′）。
  ⑥ **粘连**：两个散文段之间**缺空行**（上一行以 。！？" 收尾、下一行以汉字或 `**` 起头、
     中间无空行、上一行不以 `：` 收尾）——这一段装了两件事，该拆没拆。
     **注意**：并段必须**合成一行**；只删空行、留内部换行的并段与粘连在源码上同形，本尺会
     当场把它报成新病（2026-10-29 批一首跑撞出 6 处假阳性）。

口径留痕与判法、目标值、待裁见 `00-碎段优化台账.md` §一～§六。

用法（在本目录下）：
    python 00-碎段-量尺.py                  # 全书底账：① 短段与体例件 ② 上端 ③ 连排三分
    python 00-碎段-量尺.py --ch 08          # 单章逐段明细（短段逐条带五类定性）＋连排（带 ok/block/cross）
    python 00-碎段-量尺.py --stuck          # ⑥ 粘连检查（全书，给行号与两段首句）
    python 00-碎段-量尺.py --ch 后          # 后记（'后'／'后记'／'20' 三种写法都认）

口径变更必须先改本文件，并在 `00-碎段优化台账.md` 留痕（量法本身就是判据）。
"""
import os
import re
import sys
import glob

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BOOK = os.path.dirname(os.path.abspath(__file__))
HAN = re.compile(r'[\u4e00-\u9fff]')
LEAD = re.compile(r'^\*\*([^*]{1,40})\*\*')

SHORT = 20          # 短段阈值（汉字）
SKIP = ['参考文献', '版本变更记录']


def han(s):
    return len(HAN.findall(s))


def pc(v, d):
    return 100.0 * v / d if d else 0.0


# ── 切块与归类：与 00-风格参考-量尺.py 同一套（口径 v3），本尺只借归类 ──────────
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
    """→ [(段文本, 语体, 块标题, 紧随其后的第一非空行)]；与 00-冗余-量尺.py 逐字同一切法。"""
    out, buf = [], []
    heading, in_code = '', False
    head_txt = open(path, encoding='utf-8').read()
    inline = ('**误解现场。**' in head_txt) or ('**误解现场**。' in head_txt)

    def flush(nxt=''):
        if not buf:
            return
        p = ' '.join(buf)
        label = ''
        m = LEAD.match(p)
        if m:
            label = m.group(1)
        k = kind(label) if (inline and label and kind(label) != 'argue') else kind(heading)
        out.append((p, k, heading, nxt))
        del buf[:]

    lines = head_txt.split('\n')
    for i, line in enumerate(lines):
        if line.strip().startswith('```'):
            in_code = not in_code
            flush()
            continue
        if in_code:
            continue
        if re.match(r'^#{2,4} ', line):
            flush()
            heading = re.sub(r'^#+\s*', '', line).strip()
            if any(s in heading for s in SKIP):
                heading = '【跳过】' + heading
            continue
        if not line.strip():
            flush(next((x.strip() for x in lines[i + 1:] if x.strip()), ''))
            continue
        if is_prose(line):
            if heading.startswith('【跳过】'):
                continue
            buf.append(line.strip())
        else:
            flush(line.strip())
    flush()
    return out


def classify(t, nxt):
    """短段五类定性（见文件头 ②）。只对 ≤SHORT 汉字的段调用。"""
    tt = t.strip()
    if tt.startswith('**'):
        return 'K0'
    if tt.endswith('：') and (nxt.startswith('>') or nxt.startswith('"') or nxt.startswith('“')):
        return 'K1'
    # v3 补丁：本书各章引号体例不一——弯引号（ch7／17 等）与直引号（ch9 等）并存，
    # 旧判据只认 `：“` 与引号起头，直引号「：\"…\"」夹在句中时报不出，把对白算成 K4。
    if '：“' in tt or '："' in tt or tt.startswith('"') or tt.startswith('“'):
        return 'K2'
    if '——' in tt and han(tt) <= 14:
        return 'K3'
    return 'K4'


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


def norm(arg):
    a = (arg or '').strip()
    return '后' if a in ('后', '后记', '20') else a.zfill(2)


BLOCKERS = ('#', '|', '>', '- ', '* ', '+ ', '```', '---')


def between(a_nxt):
    """两段之间夹着什么？空＝真相邻；返回夹着的那一行。"""
    return '' if not a_nxt else a_nxt


def pair_kind(a, b):
    """相邻两段能不能并：'ok' 真相邻可并｜'cross' 跨节（节题插在中间）｜'block' 夹着件（表/清单/引文/术语注）。
    a[3] ＝紧随其后的第一行非空原文：只有在它就是 b 的首行时，两段才真相邻。"""
    nxt = (a[3] or '').strip()
    if not nxt:
        return 'ok'                       # 块末：a 后面没有东西，b 必在别的块——不该出现
    if nxt.startswith('#'):
        return 'cross'
    if nxt.startswith(BLOCKERS) or re.match(r'^\d+[.、)]\s', nxt):
        return 'block'
    n = re.sub(r'\s+', '', nxt)
    m = re.sub(r'\s+', '', b[0])
    if m.startswith(n[:20]) or n.startswith(m[:20]):
        return 'ok'
    return 'block'


def chapter_stats(ch, path):
    ps = paragraphs(path)
    short = [p for p in ps if han(p[0]) <= SHORT]
    cnt = {k: 0 for k in ('K0', 'K1', 'K2', 'K3', 'K4')}
    for p in short:
        cnt[classify(p[0], p[3])] += 1
    arg = [p for p in ps if p[1] == 'argue']
    ak = [p for p in arg if han(p[0]) <= SHORT and classify(p[0], p[3]) == 'K4']
    # 连排：按"相邻对"的真相邻性切成 ok／cross／block 三类
    runs = []          # 每项 dict(kind, texts, pairs)
    cur, kinds = [], []
    for p in arg + [None]:
        ok = (p is not None and han(p[0]) <= SHORT and classify(p[0], p[3]) == 'K4')
        if ok:
            cur.append(p)
            continue
        if len(cur) >= 2:
            ks = [pair_kind(cur[i], cur[i + 1]) for i in range(len(cur) - 1)]
            kind = 'ok' if all(k == 'ok' for k in ks) else ('cross' if 'cross' in ks else 'block')
            runs.append(dict(kind=kind, texts=[x[0] for x in cur], pairs=ks))
        cur = []
    # 上端指标（论证段）
    AL = sorted(han(p[0]) for p in arg)
    q = lambda t: AL[min(len(AL) - 1, int(round(t * (len(AL) - 1))))] if AL else 0
    return dict(ch=ch, n=len(ps), short=short, cnt=cnt, arg=arg, ak=ak, runs=runs,
                mean=(sum(AL) / len(AL)) if AL else 0, p50=q(.5), p75=q(.75), p90=q(.90),
                mx=max(AL) if AL else 0,
                over100=sum(1 for v in AL if v >= 100),
                over130=sum(1 for v in AL if v >= 130))


# ── ⑤ 粘连检查（两段之间缺空行）────────────────────────────────────────────
def stuck_hits(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    out, infence = [], False
    for i in range(len(lines) - 1):
        a, b = lines[i], lines[i + 1]
        if a.strip().startswith('```'):
            infence = not infence
            continue
        if infence:
            continue
        if not a.strip() or not b.strip():
            continue
        if not is_prose(a) or not is_prose(b):
            continue
        if not re.search(r'[。！？"]$', a.strip()):
            continue
        if a.strip().endswith('：'):
            continue
        if not re.match(r'^[\u4e00-\u9fff*]', b.strip()):
            continue
        out.append((i + 1, i + 2, a.strip()[:46], b.strip()[:46]))
    return out


def main():
    argv = sys.argv[1:]
    if '--stuck' in argv:
        print('=== ⑤ 粘连检查（两个散文段之间缺空行；段该拆而未拆） ===')
        total = 0
        for ch, path in items():
            hits = stuck_hits(path)
            total += len(hits)
            if hits:
                print('  ch%s  %d 处' % (ch, len(hits)))
                for l1, l2, x, y in hits:
                    print('     L%d／L%d  %s… ／／ %s…' % (l1, l2, x, y))
        print('  合计 %d 处' % total)
        return

    if '--ch' in argv:
        i = argv.index('--ch')
        want = norm(argv[i + 1] if len(argv) > i + 1 else '')
        hit = [(c, p) for c, p in items() if c == want]
        if not hit:
            print('--ch 用法：--ch 08（两位章号）／--ch 后；未找到该章。')
            return
        ch, path = hit[0]
        st = chapter_stats(ch, path)
        n, s = st['n'], len(st['short'])
        print('=== ch%s 短段明细（段汉字 ≤%d）｜段 %d｜短段 %d（%.1f%%）｜论块短段 %d／%d（%.1f%%） ==='
              % (ch, SHORT, n, s, pc(s, n), len(st['ak']), len(st['arg']), pc(len(st['ak']), len(st['arg']))))
        print('   K0 小标 %d｜K1 引语引导 %d｜K2 对白 %d｜K3 体例短标 %d｜K4 可并 %d'
              % (st['cnt']['K0'], st['cnt']['K1'], st['cnt']['K2'], st['cnt']['K3'], st['cnt']['K4']))
        idx = {id(p): k for k, p in enumerate(st['short'])}
        for p in st['short']:
            print('   %s %3d [%s] %s' % (classify(p[0], p[3]), han(p[0]), p[2][:18], p[0][:56]))
        print('   ---- 短段连排（论块内连续 ≥2 段 K4；ok＝真相邻可并／block＝夹着件／cross＝跨节）----')
        if not st['runs']:
            print('   无')
        for r in st['runs']:
            print('    [%s] ×%d：%s' % (r['kind'], len(r['texts']),
                                     ' ／ '.join(x[:18] for x in r['texts'])))
        return

    # 全书底账
    print('=== 第三病·碎段底账（口径 v2；段池＝00-冗余-量尺.py，段号与 --sec 同源） ===')
    print()
    print('① 短段与体例件')
    print('章  段数 短段 短段%  K0 K1 K2 K3 K4可并  论块段 论块短段 论块短段%')
    rows = []
    T = dict(n=0, s=0, k0=0, k1=0, k2=0, k3=0, k4=0, an=0, ak=0,
             ok=0, okseg=0, block=0, cross=0, over100=0, over130=0)
    for ch, path in items():
        st = chapter_stats(ch, path)
        seg = sum(len(r['texts']) for r in st['runs'])
        for k, v in (('n', st['n']), ('s', len(st['short'])), ('k0', st['cnt']['K0']),
                     ('k1', st['cnt']['K1']), ('k2', st['cnt']['K2']), ('k3', st['cnt']['K3']),
                     ('k4', st['cnt']['K4']), ('an', len(st['arg'])), ('ak', len(st['ak'])),
                     ('ok', sum(1 for r in st['runs'] if r['kind'] == 'ok')),
                     ('okseg', sum(len(r['texts']) for r in st['runs'] if r['kind'] == 'ok')),
                     ('block', sum(1 for r in st['runs'] if r['kind'] == 'block')),
                     ('cross', sum(1 for r in st['runs'] if r['kind'] == 'cross')),
                     ('over100', st['over100']), ('over130', st['over130'])):
            T[k] += v
        rows.append((ch, st, seg))
    by_arg = sorted(rows, key=lambda x: -pc(len(x[1]['ak']), len(x[1]['arg'])))
    for ch, st, seg in by_arg:
        print('{} {:>5} {:>4} {:>5.1f}  {:>2} {:>2} {:>2} {:>2} {:>5}   {:>6} {:>7} {:>8.1f}'.format(
            ch, st['n'], len(st['short']), pc(len(st['short']), st['n']),
            st['cnt']['K0'], st['cnt']['K1'], st['cnt']['K2'], st['cnt']['K3'], st['cnt']['K4'],
            len(st['arg']), len(st['ak']), pc(len(st['ak']), len(st['arg']))))
    print('-' * 84)
    print('全书 段 {}｜短段 {}（{:.1f}%）＝K0 小标 {}＋K1 引语引导 {}＋K2 对白 {}＋K3 体例短标 {}＋K4 可并 {}'
          .format(T['n'], T['s'], pc(T['s'], T['n']), T['k0'], T['k1'], T['k2'], T['k3'], T['k4']))
    print('论块 段 {}｜论块短段 {}（{:.1f}%）'.format(T['an'], T['ak'], pc(T['ak'], T['an'])))
    print()
    print('② 上端（论证段；R4′ 的两条验线看这里）')
    print('章  论证段  均值  P50  P75  P90  最长  ≥100段  占比   ≥130段')
    for ch, st, seg in sorted(rows, key=lambda x: pc(x[1]['over100'], len(x[1]['arg']))):
        print('{} {:>6} {:>6.1f} {:>4} {:>4} {:>4} {:>4}  {:>6}  {:>5.1f}%  {:>6}'.format(
            ch, len(st['arg']), st['mean'], st['p50'], st['p75'], st['p90'], st['mx'],
            st['over100'], pc(st['over100'], len(st['arg'])), st['over130']))
    print('-' * 84)
    print('全书 论证段 {}｜均值 {:.1f}｜≥100 汉字 {}（{:.1f}%）｜≥130 {}'
          .format(T['an'], sum(st['mean'] * len(st['arg']) for _, st, _ in rows) / T['an'],
                  T['over100'], pc(T['over100'], T['an']), T['over130']))
    print()
    print('③ 短段连排（真相邻三分；只有 ok 类是本步的刀）')
    print('章   ok串  涉段   block串（夹着件）  cross串（跨节）')
    for ch, st, seg in by_arg:
        o = [r for r in st['runs'] if r['kind'] == 'ok']
        b = [r for r in st['runs'] if r['kind'] == 'block']
        c = [r for r in st['runs'] if r['kind'] == 'cross']
        print('{}  {:>5}  {:>4}  {:>14}  {:>14}'.format(
            ch, len(o), sum(len(r['texts']) for r in o), len(b), len(c)))
    print('-' * 84)
    print('全书 ok 串 {}（涉 {} 段）｜block 串 {}｜cross 串 {}｜最长 ok 串 {} 段'
          .format(T['ok'], T['okseg'], T['block'], T['cross'],
                  max([len(r['texts']) for _, st, _ in rows for r in st['runs']
                       if r['kind'] == 'ok'], default=0)))
    print()
    print('注：①「短段%」裸读数含对白装置与加粗小标（后记 25.3%→扣体例 6.3% 即一例），')
    print('    判病看「论块短段%」与「ok 串」——成串才是碎，单发的短段多是落点句。')
    print('    ② 段长中位、段>200 红线不属本尺，见 `00-冗余-量尺.py`；粘连见 `--stuck`。')
    print('    ③ block 与 cross 两类不是刀口：前者两段之间夹着表／清单／引文／术语注，')
    print('    后者夹着节题——并了会拆散件或跨节，判留。')


if __name__ == '__main__':
    main()
