# -*- coding: utf-8 -*-
"""列出 35 号现行全部标题与行号（建映射表用，只读）。"""
import os, re
LIB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(LIB, '35-架构定义与视图设计研究报告-从意义目的到产品数据与四案例.md')
lines = open(P, encoding='utf-8').read().split('\n')
for i, l in enumerate(lines, 1):
    if re.match(r'^#{1,5} ', l):
        print('%5d  %s' % (i, l[:80]))
print('---')
print('总行', len(lines))
