# -*- coding: utf-8 -*-
"""01 数据形式关：列作名词的改字段，三处动词写全。"""
import io, sys

P = '04-产品数据范例/01-问题与机会清单.md'
T = [
    ('「来源」列', '「来源」字段', 0),      # 0 = 允许多处
    ('文档6「为谁」列', '文档6「为谁」字段', 0),
    ('按 15288 §3.26 判。', '按 15288 §3.26 判定。', 1),
    ('问题5 写「无」', '问题5 写出「无」', 1),
    ('机会3 写「无」', '机会3 写出「无」', 1),
]

t = io.open(P, encoding='utf-8').read()
bad = 0
for old, new, want in T:
    n = t.count(old)
    if n == 0 or (want and n != want):
        print('✗ %d 处（期望 %s）：%s' % (n, want or '多', old[:30]))
        bad += 1
        continue
    print('  落 %d 处：%s' % (n, old[:24]))
    t = t.replace(old, new)
if bad:
    print('没落 %d 行，未写回。' % bad)
    sys.exit(1)
io.open(P, 'w', encoding='utf-8').write(t)
print('已写回。')
