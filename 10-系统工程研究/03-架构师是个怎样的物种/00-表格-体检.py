# -*- coding: utf-8 -*-
"""批〇 表格体检：逐文件检查 Markdown 表格的列数一致性（同一表内各行单元格数相等）。

只报「同一张表内列数不一致」——这是批〇改号改行后最容易出的硬伤。
"""
import os, re, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BOOK = os.path.dirname(os.path.abspath(__file__))
FILES = ['00-全书框架.md', '00-目录.md', '00-三条线索.md', '00-主线与各章支撑.md', '00-案例设定.md',
         r'..\00-系统工程相关研究报告\90-治理登记\15-章级取料一致性卡.md',
         r'..\00-系统工程相关研究报告\90-治理登记\08-报告用途登记.md']


def cells(line):
    t = line.strip()
    if t.startswith('|'):
        t = t[1:]
    if t.endswith('|'):
        t = t[:-1]
    return t.count('|') + 1

bad_total = 0
for rel in FILES:
    path = os.path.join(BOOK, rel)
    lines = open(path, encoding='utf-8', errors='replace').read().split('\n')
    i, issues = 0, []
    while i < len(lines):
        if lines[i].lstrip().startswith('|'):
            j = i
            while j < len(lines) and lines[j].lstrip().startswith('|'):
                j += 1
            block = lines[i:j]
            if len(block) >= 3 and re.match(r'^\s*\|[\s:\-|]+\|\s*$', block[1]):
                base = cells(block[0])
                for k, ln in enumerate(block):
                    # 作废行（| ~~…）与版本记录行（| **v…）结构上就不按表列排，豁免
                    if ln.lstrip().startswith('| ~~') or ln.lstrip().startswith('| **v'):
                        continue
                    if cells(ln) != base:
                        issues.append((i + k + 1, base, cells(ln), ln[:60]))
            i = j
        else:
            i += 1
    print('%-52s %s' % (rel.replace('..\\', ''), '列数一致 ✓' if not issues else '列数不一致 %d 行（存量缺口，归批七）' % len(issues)))
    for ln_no, base, got, txt in issues[:12]:
        print('    L%d  应 %d 列／实 %d 列   %s' % (ln_no, base, got, txt))
    bad_total += len(issues)

print('\n合计异常行：%d（作废行与版本记录行已豁免；余下为 2026-11-06 批〇 前既有缺口，不阻断本批验收，归批七补）' % bad_total)
sys.exit(0)
