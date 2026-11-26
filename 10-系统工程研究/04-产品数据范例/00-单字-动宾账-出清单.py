# -*- coding: utf-8 -*-
"""把五桶账写成 markdown 清单：口径一篇、逐处一篇。"""
import io, re, collections

src = io.open('04-产品数据范例/00-单字-动宾账.py', encoding='utf-8').read()
exec(src.split('out = []')[0])

FILES = ['04-产品数据范例/00-产品数据规范编制规范.md',
         '04-产品数据范例/00-产品数据范例编制规程.md']

rows, secs = [], []
for p in FILES:
    t = io.open(p, encoding='utf-8').read()
    name = p.replace('\\', '/').split('/')[-1]
    tot = collections.Counter()
    hits, dai = [], []
    for v, ci in CI.items():
        for m in re.finditer(v, t):
            a = m.start()
            nx = t[a + 1] if a + 1 < len(t) else ''
            ln = t.count('\n', 0, a) + 1
            if not nx or not re.match(r'[\u4e00-\u9fff]', nx):
                tot['孤立'] += 1
            elif nx in DAI.get(v, ''):
                tot['待裁'] += 1
                dai.append((ln, v, nx, t[max(0, a - 14):a + 16].replace('\n', '')))
            elif nx in BU:
                tot['补语'] += 1
            elif nx in ci:
                tot['词素'] += 1
            else:
                tot['动宾'] += 1
                hits.append((ln, v, t[max(0, a - 14):a + 14].replace('\n', '')))
    rows.append((name, tot))
    secs.append((name, sorted(hits), sorted(dai)))

o = ['# 单字动词清账：两个文档的五桶账', '',
     '口径写在 `00-单字-动宾账.py` 头：孤立、词素、补语、动宾、待裁五桶，五桶之和等于该动字在全文出现总数，没有落在桶外的处。逐处清单在第三节，按行号排。', '',
     '## 一 五桶合计', '',
     '| 文件 | 孤立 | 词素 | 补语 | 动宾 | 待裁 | 合计 |',
     '|---|---|---|---|---|---|---|']
for name, tot in rows:
    o.append('| %s | %d | %d | %d | %d | %d | %d |'
             % (name, tot['孤立'], tot['词素'], tot['补语'], tot['动宾'], tot['待裁'], sum(tot.values())))
o += ['', '## 二 待裁：术语碰撞，改名须人点头', '',
      '| 文件 | 行 | 字 | 原文', '|---|---|---|---|']
for name, _, dai in secs:
    for ln, v, nx, ctx in dai:
        o.append('| %s | L%d | %s%s | %s |' % (name[:6], ln, v, nx, ctx.replace('|', '丨')))
o += ['', '## 三 动宾逐处']
for name, hits, _ in secs:
    o += ['', '### %s（%d 处）' % (name, len(hits)), '', '| 行 | 字 | 原文', '|---|---|---|']
    for ln, v, ctx in hits:
        o.append('| L%d | %s | %s |' % (ln, v, ctx.replace('|', '丨')))

io.open('04-产品数据范例/00-单字-动宾清单.md', 'w', encoding='utf-8').write('\n'.join(o) + '\n')
print('写出 %d 行' % len(o))
for name, tot in rows:
    print(name, dict(tot))
