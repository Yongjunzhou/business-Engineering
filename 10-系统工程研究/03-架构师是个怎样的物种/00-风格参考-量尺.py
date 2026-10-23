#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""《架构师是个怎样的物种？》章级配比量尺（口径 v3）

用途：章级语体配比与红线自查。**这是本书配比数字的单一量尺**——写作方与审查方共用，
     口径变更必须先改本文件并在 `00-风格参考.md` §3.3 留痕（"量法本身就是判据"）。

口径 v3（2026-09-26 定；块边界与归类规则自 v2 起未变）
- 计量单位：汉字 `[\\u4e00-\\u9fff]`；**分母＝章主体**（剔除「参考文献」「版本变更记录」；
  自查＋练习外移附录 E 落地后，同步从分母剔除）。
- 块边界：**下一个任意级标题**（`##` 或 `###`）——案例进展块常插在幕中间，只认 `##` 会把
  紧随的论证节误并进"叙事"（v1 曾因此虚高 ch2 22.1／ch8 23.8／ch11 33 个百分点）。
- 归类：章首（标题含"误解现场"）／案例进展（含"案例进展"）／论证（其余正文块）／
  章末核心件（概念总图＋认知反转＋本章判据）／章末可压件（概念总图＋认知反转＋自查＋练习＋小结）。
- 三口径：A＝判据＋可压件（旧表）／B＝判据移出红线（**v1.3 起为红线口径**）／
  C＝再外移"自查＋练习"（拟迁附录 E，落地后可复算）。
- 红线（v1.3）：章首 ≤4%／案例进展合计 ≤12% 且单块 ≤700 汉字／论证 ≥60%／
  可压件 ≤22%／认知反转 硬线 ≤1000、提示线 ≤800；硬门＝同一概念点不得两处各讲一遍（人工判读）。

用法：在本目录下 `python 00-风格参考-量尺.py`。
"""
import os
import re
import glob
import statistics
import sys

if hasattr(sys.stdout, 'reconfigure'):      # Windows 控制台按 UTF-8 输出，防乱码
    sys.stdout.reconfigure(encoding='utf-8')

BOOK = os.path.dirname(os.path.abspath(__file__))
HAN = re.compile(r'[\u4e00-\u9fff]')
SKIP = ['参考文献', '版本变更记录']
KEYS = ['open', 'case', 'argue', 'map', 'reversal', 'criteria', 'selfcheck', 'exercise', 'summary']


def han(s):
    return len(HAN.findall(s))


def kind(h):
    """按标题归类；顺序即优先级。"""
    if any(k in h for k in SKIP):
        return 'skip'
    if '误解现场' in h:
        return 'open'
    if '案例进展' in h or '案例回场' in h:
        return 'case'          # 2026-09-27：第1章（双线章）的案例块用「案例回场」，与「案例进展」同类计量
    if '概念总图' in h or '能力级' in h:
        return 'map'          # 2026-09-26：「本章的能力级」升为独立节（### B），与总图同归 map 类
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


def chapters(root):
    for f in sorted(glob.glob(os.path.join(root, '*.md'))):
        n = os.path.basename(f)
        if re.match(r'\d\d-第\d+章', n) and '从教材到问题分析' not in n:
            yield n[:2], f


LEAD = re.compile(r'^\*\*([^*]{1,40})\*\*')   # 段首小标：`**小标。**正文`／独立行 `**A 概念总图**`


def blocks(path):
    """按任意级标题切块，返回 [(标题, 正文)]。

    **2026-10-21 增「段首小标」也作块边界**（半长化改定：章内三级标题压到 1/3，改用
    `**小标。**正文` 承接）；不认它，章首「误解现场」与「案例进展」就统计不到，
    配比口径会整体失真（当日 ch10 首测即误报 论证 94.7%）。
    **跳过态**：进了「参考文献」块之后，块内的粗体小标（标准／经典文献）不再切块——
    否则参考文献会被拆成一堆 argue 块、混进分母（首测全书各章虚高 200~500 汉字）。
    """
    out, cur_h, cur, in_skip = [], None, [], False
    txt = open(path, encoding='utf-8').read()
    # 过渡期开关（2026-10-21）：章内已改用「段首小标」的章才认小标为块边界；
    # 尚未迁移的章仍按标题切块——保证同一把尺在迁移前后对**未改的章**读数一字不变。
    # 2026-10-23 补：加粗收尾规则改后（句读移出加粗），小标写作 `**误解现场**。`
    # 两种形态都认，否则 inline_mode 判否、整章退化成"论证 100%"。判例 4：锚点一动，全库脚本同批改。
    inline_mode = ('**误解现场。**' in txt) or ('**误解现场**。' in txt)

    def flush():
        if cur_h is not None:
            out.append((cur_h, '\n'.join(cur)))

    for ln in txt.split('\n'):
        if re.match(r'^#{2,3} ', ln):
            flush()
            cur_h, cur = re.sub(r'^#+\s*', '', ln).strip(), []
            in_skip = '参考文献' in cur_h
            continue
        m = LEAD.match(ln) if inline_mode else None
        if m and not in_skip:
            flush()
            cur_h = m.group(1).strip().rstrip('。｜ ')
            rest = ln[m.end():].lstrip('。｜ ').strip()
            cur = [rest] if rest else []
            in_skip = '参考文献' in cur_h
            continue
        cur.append(ln)
    flush()
    return out


pc = lambda v, d: 100.0 * v / d if d else 0.0

rows = []
for ch, path in chapters(BOOK):
    a = dict.fromkeys(KEYS, 0)
    big = []
    case_sizes = []
    for h, body in blocks(path):
        k = kind(h)
        if k == 'skip':
            continue
        v = han(body)
        a[k] += v
        if k == 'case':
            case_sizes.append(v)
        if k == 'case' and v > 700:
            big.append(v)
    # 2026-10-23 改：半长化判定按**章长**，不再认「段首小标」锚点。
    # 起因＝第1章重排把 `**误解现场。**` 改成 `### 1.1.1 误解现场`，锚点判否 → 被当成 v3 章
    # （章首线 4%）而误报红线；第3章同日改法，早已同此病。口径见 00-风格参考.md §6.1
    # 「占比线必须随章长缩放」——半长化章 8,370~10,230 汉字，其余章 ≥14,598，阈值 11,000 分得干净。
    tot = sum(a.values())
    rows.append(dict(ch=ch, tot=tot, big=big, case_n=len(case_sizes),
                     case_max=max(case_sizes) if case_sizes else 0,
                     half=(tot <= 11000), **a))

print('=== ① 逐章语体配比（口径 v3） ===')
print('章   总汉字  章首%  案例%  叙事%  论证%  核心尾%  可压件%(B)  认知反转  案例块>700')
for r in rows:
    core = r['map'] + r['reversal'] + r['criteria']
    press = r['map'] + r['reversal'] + r['selfcheck'] + r['exercise'] + r['summary']
    narr = r['open'] + r['case']
    print('{}  {:>6}  {:>5.1f}  {:>5.1f}  {:>5.1f}  {:>5.1f}  {:>7.1f}  {:>10.1f}  {:>8}  {}'.format(
        r['ch'], r['tot'], pc(r['open'], r['tot']), pc(r['case'], r['tot']), pc(narr, r['tot']),
        pc(r['argue'], r['tot']), pc(core, r['tot']), pc(press, r['tot']), r['reversal'],
        '、'.join(str(v) for v in r['big']) or '—'))

med = lambda k: round(statistics.median([pc(r[k], r['tot']) for r in rows]), 1)
print('—' * 96)
print('中位：章首 {}%  案例 {}%  叙事 {}%  论证 {}%  核心尾件 {}%  可压件%(B) {}%  认知反转 {} 汉字'.format(
    med('open'), med('case'), med('open') and round(statistics.median(
        [pc(r['open'] + r['case'], r['tot']) for r in rows]), 1), med('argue'),
    round(statistics.median([pc(r['map'] + r['reversal'] + r['criteria'], r['tot']) for r in rows]), 1),
    round(statistics.median([pc(r['map'] + r['reversal'] + r['selfcheck'] + r['exercise'] + r['summary'],
                                r['tot']) for r in rows]), 1),
    int(statistics.median([r['reversal'] for r in rows]))))

print()
print('=== ② 三口径下的「章末件占比」 ===')
print('口径 A＝判据＋可压件（旧）｜B＝判据移出红线（v1.3 红线口径）｜C＝再外移自查＋练习（拟迁附录 E）')
print('章    A(旧)     B(现)     C(外移后)')
over_b, over_c = [], []
for r in rows:
    moved = r['selfcheck'] + r['exercise']
    newtot = r['tot'] - moved
    a = pc(r['map'] + r['reversal'] + r['criteria'] + r['selfcheck'] + r['exercise'] + r['summary'], r['tot'])
    b = pc(r['map'] + r['reversal'] + r['selfcheck'] + r['exercise'] + r['summary'], r['tot'])
    c = pc(r['map'] + r['reversal'] + r['summary'], newtot)
    if b > 22:
        over_b.append('ch%s %.1f%%' % (r['ch'], b))
    if c > 22:
        over_c.append('ch%s %.1f%%' % (r['ch'], c))
    print('{}  {:>6.1f}%  {:>7.1f}%  {:>9.1f}%{}'.format(r['ch'], a, b, c, '  ←B 超线' if b > 22 else ''))
print('口径B 超 22%：', '、'.join(over_b) if over_b else '无')
print('口径C 超 22%：', '、'.join(over_c) if over_c else '无')

print()
print('=== ③ 红线自查（超线项汇总） ===')
print('口径：未半长化章按 v3（章首 4／案例 12／论证 60／可压件 22／反转 800·1000）；'
      '已半长化章（每章 9,300 汉字级）按 v4（章首 8／案例 15／论证 55／可压件 25／反转 500·600）'
      '——**占比线必须随章长缩放**：同一段 600 字的开场，在 1.8 万的章里是 3.3%、在 9,300 的章里是 6.5%，'
      '不缩放就会把“成书后的正常章”误报成退步（2026-10-21 半长化改定，见 00-风格参考.md §6.1）')
th = lambda r: (8, 15, 55, 25, 500, 600) if r.get('half') else (4, 12, 60, 22, 800, 1000)
print('章首 >口径：', '、'.join('ch%s %.1f%%（线 %d）' % (r['ch'], pc(r['open'], r['tot']), th(r)[0])
                            for r in rows if pc(r['open'], r['tot']) > th(r)[0]) or '无')
print('案例合计 >口径：', '、'.join('ch%s %.1f%%（线 %d）' % (r['ch'], pc(r['case'], r['tot']), th(r)[1])
                              for r in rows if pc(r['case'], r['tot']) > th(r)[1]) or '无')
print('论证 <口径：', '、'.join('ch%s %.1f%%（线 %d）' % (r['ch'], pc(r['argue'], r['tot']), th(r)[2])
                            for r in rows if pc(r['argue'], r['tot']) < th(r)[2]) or '无')
press = lambda r: pc(r['map'] + r['reversal'] + r['selfcheck'] + r['exercise'] + r['summary'], r['tot'])
print('可压件 >口径（口径B）：', '、'.join('ch%s %.1f%%（线 %d）' % (r['ch'], press(r), th(r)[3])
                                     for r in rows if press(r) > th(r)[3]) or '无')
print('认知反转 >硬线：', '、'.join('ch%s %d（线 %d）' % (r['ch'], r['reversal'], th(r)[5]) for r in rows
                              if r['reversal'] > th(r)[5]) or '无')
print('认知反转 >提示线：', '、'.join('ch%s %d（线 %d）' % (r['ch'], r['reversal'], th(r)[4]) for r in rows
                               if r['reversal'] > th(r)[4]) or '无')
print('案例单块 >700：', '、'.join('ch%s %s' % (r['ch'], '／'.join(str(v) for v in r['big']))
                              for r in rows if r['big']) or '无')
print()
print('注：硬门「同一概念点不得两处各讲一遍」为人工判读，本脚本不判；')
print('    处置顺序＝改口径 → 外移自查＋练习 → 压认知反转 → 去重复 → 才轮到叙事（见 00-风格参考.md §6.1）。')

print()
print('=== ④ §3.3 表行（口径 v3；可直接粘贴进 00-风格参考.md §3.3） ===')
print('| 章 | 总汉字 | 章首% | 案例% | 叙事合计% | 论证% | 核心尾件% | 附属尾件% | 案例块数 | 案例单块最大 |')
print('|---|---|---|---|---|---|---|---|---|---|')
for r in rows:
    core = r['map'] + r['reversal'] + r['criteria']
    tail = r['selfcheck'] + r['exercise'] + r['summary']
    print('| {} | {} | {:.1f} | {:.1f} | {:.1f} | {:.1f} | {:.1f} | {:.1f} | {} | {} |'.format(
        r['ch'], r['tot'], pc(r['open'], r['tot']), pc(r['case'], r['tot']),
        pc(r['open'] + r['case'], r['tot']), pc(r['argue'], r['tot']), pc(core, r['tot']),
        pc(tail, r['tot']), r['case_n'], r['case_max'] or '—'))

# ─────────────────────────────────────────────────────────────────────
# ⑤ 酣畅三查（断点代理；2026-10-23 立，判据见 00-风格参考.md §6.17）
#    性质＝只报不判——断点是读者的事，脚本只把"可能停下来的地方"点出来。
# ─────────────────────────────────────────────────────────────────────


def prose_paras(body):
    """把块正文切成散文段：剔代码块／表格／引用块／列表项（与量尺其余各项同口径）。"""
    out, buf, infence = [], [], False
    for ln in body.split('\n'):
        s = ln.strip()
        if s.startswith('```'):
            infence = not infence
            if buf:
                out.append(' '.join(buf))
                buf = []
            continue
        if infence:
            continue
        head = (not s or s.startswith('|') or s.startswith('>') or s.startswith('- ')
                or s.startswith('* ') or re.match(r'^\d+[.、] ', s))
        if head:
            if buf:
                out.append(' '.join(buf))
                buf = []
            continue
        buf.append(s)
    if buf:
        out.append(' '.join(buf))
    return out


def sentences(p):
    return [x for x in re.split(r'(?<=[。！？])', p) if han(x)]


print()
print('=== ⑤ 酣畅三查（断点代理；只报不判，判据见 00-风格参考.md §6.17） ===')
print('章  跨块重复句  最长长段连排(>100汉字)  短段%(≤20汉字)')
dup_detail = []
for ch, path in chapters(BOOK):
    blks = [(h, prose_paras(b)) for h, b in blocks(path)]
    seen, dups = {}, []
    for bi, (h, ps) in enumerate(blks):
        for p in ps:
            for s in sentences(p):
                key = re.sub(r'[^\u4e00-\u9fff]', '', s)
                if len(key) < 8:
                    continue
                if key in seen and seen[key][0] != bi:
                    dups.append((key, seen[key][1], h))
                seen.setdefault(key, (bi, h))
    cnt = {}
    for key, _, _ in dups:
        cnt[key] = cnt.get(key, 0) + 1
    # 只留"恰好两次"的：出现三次及以上，多是清单里逐条重复的同一问句（结构性，不属重读）
    dups = [d for d in dups if cnt[d[0]] == 1]
    lens = [han(p) for _, ps in blks for p in ps]
    run = best = 0
    for v in lens:
        run = run + 1 if v > 100 else 0
        best = max(best, run)
    short = pc(sum(1 for v in lens if v <= 20), len(lens))
    print('{}  {:>10}  {:>18}  {:>14.1f}'.format(ch, len(dups), best, short))
    dup_detail.append((ch, dups))

print()
print('跨块重复句（同一句 ≥8 汉字、恰好出现两次、分属两块）——改法＝删一处，或让它升级为递进：')
found = False
for ch, dups in dup_detail:
    if not dups:
        continue
    found = True
    print('  ch{}'.format(ch))
    for key, a, b in dups[:6]:
        print('    「{}」  {} ↔ {}'.format(key[:28], a[:24], b[:24]))
    if len(dups) > 6:
        print('    ……另有 {} 条'.format(len(dups) - 6))
if not found:
    print('  无')
print()
print('注：长段连排与短段占比只报不判（各章语体不同）；断点五型的诊断与处方见 §6.17，')
print('    本脚本只覆盖其中两型（重读的跨块重复、断线的节奏）。')
