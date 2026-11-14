# -*- coding: utf-8 -*-
"""落笔后自检：mermaid 块完整性 ＋ 46/48 号指针落点 ＋ 表格列数一致（只读）。"""
import os, re

LIB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(LIB, '35-架构定义与视图设计研究报告-从意义目的到产品数据与四案例.md')
txt = open(P, encoding='utf-8').read()
lines = txt.split('\n')

# 1. mermaid
blocks = re.findall(r'```mermaid\n(.*?)```', txt, re.S)
print('mermaid 块：%d' % len(blocks))
bad = 0
for i, b in enumerate(blocks, 1):
    if b.count('"') % 2 != 0:
        print('  块 %d：半角双引号数为奇数' % i); bad += 1
    if b.count('[') != b.count(']'):
        print('  块 %d：方括号不配对 [=%d ]=%d' % (i, b.count('['), b.count(']'))); bad += 1
    if b.count('{') != b.count('}'):
        print('  块 %d：花括号不配对' % i); bad += 1
print('  mermaid 异常：%d' % bad)

# 2. 46 号指针（本件正文）
secs_46 = {'1.3', '2.1', '2.2', '2.3', '2.4', '2.5', '2.6', '2.7', '2.8',
           '3.1', '3.2', '3.3', '3.4', '3.5', '3.6', '3.7', '3.8', '3.9',
           '4.1', '4.2', '4.3', '4.4', '4.5',
           '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.8', '5.9',
           '6.1', '6.2', '6.3', '6.4', '6.5', '6.6', '6.7', '6.8', '6.9', '6.10', '6.11',
           '7.1', '7.2', '7.3', '7.4', '7.5', '8.1', '8.2', '8.3', '8.4', '8.5', '8.6',
           '9.1', '9.2', '9.3', '9.4', '9.5', '9.6'}
hits = [(i, m.group(1)) for i, l in enumerate(lines, 1)
        for m in [re.search(r'46 号[^。\n]{0,24}?§(\d+\.\d+)', l)] if m]
print('\n46 号指针（正文）共 %d 处：' % len(hits))
for i, s in hits:
    mark = '' if s in secs_46 else '   ← 不在 46 号现行目录'
    print('   行 %-5d §%-4s%s' % (i, s, mark))

# 3. 48 号指针
hits48 = [(i, m.group(1)) for i, l in enumerate(lines, 1)
          for m in [re.search(r'48 号[^。\n]{0,26}?§(\d+\.\d+)', l)] if m]
print('\n48 号指针（正文）共 %d 处，节号：%s' % (len(hits48), ' '.join(sorted({s for _, s in hits48}))))

# 4. 表格列数（每块一致）
tbl = []
blocks2 = []
cur = []
for l in lines + ['']:
    if l.strip().startswith('|'):
        cur.append(l)
    else:
        if cur:
            blocks2.append(cur)
            cur = []
prob = 0
for b in blocks2:
    cols = set()
    for r in b:
        cells = [c for c in re.split(r'(?<!\\)\|', r.strip())[1:-1]]
        cols.add(len(cells))
    if len(cols) > 1:
        prob += 1
        print('  表块列数不一致：%s … 列数集合 %s' % (b[0][:40], sorted(cols)))
print('\n表块 %d 个，列数不一致 %d 个' % (len(blocks2), prob))
