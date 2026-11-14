# -*- coding: utf-8 -*-
"""撞号普查：把 35 号里 §2.x~§8.x 的每一处引用逐条列出，供逐处判"本件自引 or 标准条款"。

    python 90-治理登记/_census35.py > _census.txt

判定辅助列：
  IN_APP   ：该行在附录 A/B（条款索引）内 → 一律标准条款
  EXEMPT   ：存史行（版本行/修订记录/勘误） → 一律不动
  STD_NEAR ：紧邻 16 字内有标准名 → 标准条款
  PREEV    ：本行前面 40 字内有件名（46/48/42/34 号） → 他件引用
  其余     ：待判（候选：本件自引）
"""
import os, re, sys

LIB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(LIB, '35-架构定义与视图设计研究报告-从意义目的到产品数据与四案例.md')
lines = open(P, encoding='utf-8').read().split('\n')

STD = ('42010', '42020', '15288', '42030', 'ISO 9000', 'ISO/IEC', 'ISO_IEC')
EXEMPT = ('文档版本', '修订记录', '勘误记录', '勘误（', '→ v', '> **v')

# 附录 A/B 行区间（现行 v1.10）
appA = next(i for i, l in enumerate(lines, 1) if l.startswith('## 附录 A'))
appB = next(i for i, l in enumerate(lines, 1) if l.startswith('## 附录 B'))

PAT = re.compile(r'§(\d+(?:\.\d+)*)')
cnt = {'STD': 0, 'APP': 0, 'EXEMPT': 0, 'PREEV': 0, 'CAND': 0}
cand = []
for i, l in enumerate(lines, 1):
    if not PAT.search(l):
        continue
    if any(k in l for k in EXEMPT):
        cnt['EXEMPT'] += len(PAT.findall(l)); continue
    if appA <= i <= 99999 and (appA <= i):
        if i >= appA:
            cnt['APP'] += len(PAT.findall(l)); continue
    near_std = False
    for mm in PAT.finditer(l):
        k = mm.group(1)
        if not re.match(r'^[2-8]\.\d', k):
            continue
        pre16 = l[max(0, mm.start() - 16):mm.start()]
        pre40 = l[max(0, mm.start() - 40):mm.start()]
        if any(s in pre16 for s in STD):
            cnt['STD'] += 1; continue
        if any(o in pre40 for o in ('46 号', '48 号', '42 号', '34 号')):
            cnt['PREEV'] += 1; continue
        cnt['CAND'] += 1
        cand.append((i, k, l[max(0, mm.start() - 34):mm.start() + 16].replace('\n', ' ')))

print('统计：标准条款(紧邻) %d｜附录内 %d｜存史 %d｜他件 %d｜待判 %d'
      % (cnt['STD'], cnt['APP'], cnt['EXEMPT'], cnt['PREEV'], cnt['CAND']))
print('-' * 100)
for i, k, ctx in cand:
    print('%5d  §%-7s …%s…' % (i, k, ctx))
