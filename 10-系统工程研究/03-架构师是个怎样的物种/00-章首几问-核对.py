#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""《架构师是个怎样的物种？》章首几问核对器（`N.1.3 本章要回答什么`）

用途：一键核对全书 19 章的章首几问是否合式。**只认机械可查的项**——
      语义判断（问点是不是一件真事、是否目录的问答版、是否重问）仍须人工读。

判据户口：`00-风格参考.md` §6.15（六条写法）＋§6.15.1（本节形式九条，甲1~甲9）
          ＋§6.15.2（量五条，量1~量3）＋§6.15.3（反目录问答版）。
写法权威另见 `00-全书框架.md` §五 第 2 条。

用法（在本目录下运行）：
    python 00-章首几问-核对.py              # 全书，逐章一行＋违例明细
    python 00-章首几问-核对.py --chapter 18 # 只看某章
    python 00-章首几问-核对.py --quiet      # 只报违例章

退出码：0＝全过；1＝有违例。
"""
import os
import re
import sys
import glob
import statistics

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BOOK = os.path.dirname(os.path.abspath(__file__))
HAN = re.compile(r'[\u4e00-\u9fff]')

# ── 判据常量（改这里＝改判据，须与 00-风格参考.md §6.15 同批） ──────────────
OPENING = '读完本章，下面这几问，你应该答得出来。'
CLOSING_HEAD = '这几问合起来，问的是一件事：'
N_MIN, N_MAX = 4, 8                 # 甲4
CAP = 300                           # 甲6：本节汉字上限（例外章按 35×超出条数 放宽）
Q_MAX = 35                          # 量1：每问汉字上限
Q_RED = 40                          # 量1：硬红线
BAD_HEAD = tuple('这那他她它该此')     # 起头禁字
FACT_TAG = ('这一章', '本章的骨架')     # 甲8 禁语（章自称一律"本章"）

# 登记例外：章号 -> (条数, 理由)。只许登记，不许默默放过。
EXCEPT = {15: (9, '判据九项逐条覆盖（2026-10-26 该章按 §6.15 重写时定）')}

# 19 章主词表（§6.15.2 量2 的判据；多主词章按题归属）
MAIN = {
    1: ['概念', '概念体系'], 2: ['工程'], 3: ['需求', '设计开发', '质量'],
    4: ['需求工程', '需求'], 5: ['需求'], 6: ['设计开发', '需求', '方案'],
    7: ['产品数据', '数据'], 8: ['验证', '确认', '评审'], 9: ['工程师'],
    10: ['架构'], 11: ['架构定义', '架构'], 12: ['架构决策'], 13: ['架构描述'],
    14: ['架构', '设计'], 15: ['配置管理'], 16: ['架构治理', '治理'],
    17: ['架构过程', '架构'], 18: ['架构应用', '架构'], 19: ['架构师'],
}

ITEM = re.compile(r'^\s*(?:(\d+)[\.、]|([一二三四五六七八九十]+)、)\s*(.+)$')
HEAD3 = re.compile(r'^###\s*(\d+)\.1\.3\s*(.*)$')
HEAD = re.compile(r'^#{1,4}\s')
BLOCK = re.compile(r'^##\s*(\d+)\.(\d+)\s')


def han(s):
    return len(HAN.findall(s))


def chapters(want=None):
    out = []
    for f in sorted(glob.glob(os.path.join(BOOK, '*.md'))):
        n = os.path.basename(f)
        m = re.match(r'^(\d\d)-第(\d+)章', n)
        if not m or '从教材到问题分析' in n:
            continue
        ch = int(m.group(2))
        if want is None or ch == want:
            out.append((ch, f))
    return out


def parse(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    st = None
    for i, ln in enumerate(lines):
        if HEAD3.match(ln):
            st = i
            break
    if st is None:
        return None
    en = len(lines)
    for j in range(st + 1, len(lines)):
        if HEAD.match(lines[j]):
            en = j
            break
    body = lines[st + 1:en]
    # 分节线 `---` 属章级排版，不属本节；剔除后再分段
    body = [x for x in body if not re.match(r'^\s*---\s*$', x)]
    items, lead, tail = [], [], []
    idx = [k for k, ln in enumerate(body) if ITEM.match(ln.strip())]
    if idx:
        lead = [x for x in body[:idx[0]] if x.strip()]
        tail = [x for x in body[idx[-1] + 1:] if x.strip()]
        cur = None
        for ln in body[idx[0]:idx[-1] + 1]:
            m = ITEM.match(ln.strip())
            if m:
                if cur:
                    items.append(cur)
                cur = m.group(3).strip()
            elif cur and ln.strip():
                cur += ln.strip()
        if cur:
            items.append(cur)
    else:
        lead = [x for x in body if x.strip()]
    h2 = [m.group(0) for m in (BLOCK.match(x) for x in lines) if m and m.group(2) != '1']
    return dict(title=lines[st].strip(), lead=lead, items=items, tail=tail,
                text='\n'.join(body), nblocks=len(h2))


def check(ch, path):
    d = parse(path)
    bad, warn = [], []
    if not d:
        return ['甲0 找不到 `### N.1.3` 标题'], [], {}
    t = d['text']
    items = d['items']
    n = len(items)

    if not re.match(r'^###\s*%d\.1\.3\s+本章要回答什么$' % ch, d['title']):
        bad.append('甲1 标题不合式：%s' % d['title'])

    # 甲2 开场
    if len(d['lead']) != 1:
        bad.append('甲2 开场句应为 1 段，实为 %d 段' % len(d['lead']))
    elif d['lead'][0].strip() != OPENING:
        bad.append('甲2 开场句不合定句：%s' % d['lead'][0].strip()[:24])

    # 甲3 编号
    cn = re.findall(r'^\s*[一二三四五六七八九十]+、', '\n'.join(d['lead'] + d['items'] + d['tail']),
                    re.M)
    if cn:
        bad.append('甲3 用了汉字序数编号 %d 处' % len(cn))

    # 甲4 条数
    if not (N_MIN <= n <= N_MAX):
        if ch in EXCEPT and EXCEPT[ch][0] == n:
            warn.append('甲4 条数 %d 属登记例外（%s）' % (n, EXCEPT[ch][1]))
        else:
            bad.append('甲4 条数 %d 越界（%d~%d）' % (n, N_MIN, N_MAX))

    # 甲5 收尾
    if len(d['tail']) != 1:
        bad.append('甲5 收尾应为 1 段，实为 %d 段' % len(d['tail']))
    else:
        cl = d['tail'][0].strip()
        if not cl.startswith(CLOSING_HEAD):
            bad.append('甲5 收尾不合定句：%s' % cl[:24])
        if han(cl) > 40:
            bad.append('甲5 收尾 %d 汉字（≤40）' % han(cl))

    # 甲6 本节总量（超条数的例外章按 35×超出条数 放宽上限）
    cap = CAP + (35 * (n - N_MAX) if n > N_MAX else 0)
    size = han(t)
    if size > cap:
        bad.append('甲6 本节 %d 汉字（上限 %d）' % (size, cap))

    # 甲7 题区禁项
    zone = '\n'.join(items)
    for pat, name in ((r'\*\*', '加粗'), (r'^\s*>', '引文块'), (r'^\s*\|', '表格'),
                      (r'（', '括注'), (r'^\s*---\s*$', '分隔线')):
        c = len(re.findall(pat, zone, re.M))
        if c:
            bad.append('甲7 题区含%s %d 处' % (name, c))
    if '之外' in zone and '一问' in zone:
        bad.append('甲7 题区有"之外还有一问"式副册结构')

    # 甲8 自称与量词
    for w in FACT_TAG:
        if w in t:
            bad.append('甲8 本节出现「%s」' % w)
    if re.search(r'[一二三四五六七八九十\d]+\s*[句件条]：', '\n'.join(d['lead'])):
        bad.append('甲8 开场句用了"句／件／条"作量词')

    # 甲9 标点
    if '“' in t or '”' in t:
        bad.append('甲9 本节用弯引号（应直引号）')

    # 量1 题长
    lens = [han(x) for x in items]
    over40 = [i + 1 for i, L in enumerate(lens) if L > Q_RED]
    over35 = [i + 1 for i, L in enumerate(lens) if Q_MAX < L <= Q_RED]
    if over40:
        bad.append('量1 第 %s 问超硬红线 40 字' % over40)
    if over35:
        warn.append('量1 第 %s 问超 35 字' % over35)
    med = statistics.median(lens) if lens else 0
    if lens and not (18 <= med <= 28):
        warn.append('量1 题长中位 %s（18~28）' % med)

    # 量2 主词
    words = MAIN.get(ch, [])
    miss = [i + 1 for i, x in enumerate(items) if not any(w in x for w in words)]
    if len(miss) > 1:
        bad.append('量2 第 %s 问不带章题主词' % miss)
    elif miss:
        warn.append('量2 第 %s 问不带主词（至多 1 题例外）' % miss)

    # 起头（§6.15 ① 机械项）
    heads = [i + 1 for i, x in enumerate(items) if x[:1] in BAD_HEAD]
    if heads:
        bad.append('§6.15① 第 %s 问以「它／这／那」起头' % heads)

    # 问号数
    for i, x in enumerate(items):
        if x.count('？') > 2:
            bad.append('量5 第 %d 问 %d 个问号（≤2）' % (i + 1, x.count('？')))

    # 反目录问答版（§6.15.3 第 1 条）
    if items and d['nblocks'] and n == d['nblocks']:
        warn.append('§6.15.3 问数＝块数（%d），疑目录问答版，须人工核' % n)

    stat = dict(n=n, size=size, med=med, maxlen=max(lens) if lens else 0,
                nblocks=d['nblocks'], miss=len(miss))
    return bad, warn, stat


def main():
    want = None
    quiet = '--quiet' in sys.argv
    if '--chapter' in sys.argv:
        want = int(sys.argv[sys.argv.index('--chapter') + 1])

    total_q = total_bad = 0
    rows, notes = [], []
    for ch, path in chapters(want):
        bad, warn, stat = check(ch, path)
        total_q += stat.get('n', 0)
        total_bad += len(bad)
        rows.append((ch, stat, bad, warn))
        for b in bad:
            notes.append('  第%2d章 ✗ %s' % (ch, b))
        for w in warn:
            notes.append('  第%2d章 · %s' % (ch, w))

    if not quiet:
        print('章  条数  本节汉字  题长中位(最长)  块数  缺主词  结果')
        print('-' * 68)
        for ch, s, bad, warn in rows:
            flag = '✗ %d 项' % len(bad) if bad else ('· %d 提示' % len(warn) if warn else '✓')
            print('%2d  %4d  %7d  %8s(%-3s)  %4d  %5d  %s'
                  % (ch, s.get('n', 0), s.get('size', 0), s.get('med', 0),
                     s.get('maxlen', 0), s.get('nblocks', 0), s.get('miss', 0), flag))
        print()
    if notes:
        print('明细：')
        print('\n'.join(notes))
        print()
    print('合计：%d 章 / %d 问 / 违例 %d 项' % (len(rows), total_q, total_bad))
    return 1 if total_bad else 0


if __name__ == '__main__':
    sys.exit(main())
