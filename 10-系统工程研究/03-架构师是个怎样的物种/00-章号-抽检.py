# -*- coding: utf-8 -*-
"""批〇 验收第 4 项：全库「旧章号」抽检。

扫教材书目录下全部 .md（不含 旧版正文归档/、不含 *-从教材到问题分析.md），
按文件统计「第N章」（N>=12）与「旧号引用」出现数，并抽样打印上下文，
供与新号对表逐条判「属正常历史留痕／属待改/属已改」。
"""
import os, re, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BOOK = os.path.dirname(os.path.abspath(__file__))
PAT = re.compile(r'第(1[2-9]|2[0-9])章')
rows = []
for name in sorted(os.listdir(BOOK)):
    if not name.endswith('.md'):
        continue
    if '从教材到问题分析' in name:
        continue
    path = os.path.join(BOOK, name)
    txt = open(path, encoding='utf-8', errors='replace').read()
    hits = PAT.findall(txt)
    if hits:
        rows.append((name, len(hits), sorted({int(h) for h in hits})))

print('=== 批〇 验收④ 旧章号抽检（教材书顶层 .md，不含归档与派生件） ===')
print('命中文件 %d 个｜命中总数 %d 处\n' % (len(rows), sum(r[1] for r in rows)))
for name, n, ns in sorted(rows, key=lambda r: -r[1]):
    print('  %-52s %4d 处   章号 %s' % (name, n, ','.join(str(x) for x in ns)))

print('\n--- 逐文件抽样（每文件最多 4 条，前 60 字上下文） ---')
for name, n, ns in sorted(rows, key=lambda r: -r[1]):
    txt = open(os.path.join(BOOK, name), encoding='utf-8', errors='replace').read()
    print('\n[%s] %d 处' % (name, n))
    for k, m in enumerate(PAT.finditer(txt)):
        if k >= 4:
            print('   …（余 %d 处略）' % (n - 4))
            break
        s = txt[max(0, m.start() - 34):m.start() + 24].replace('\n', ' ')
        print('   · …%s…' % s)
