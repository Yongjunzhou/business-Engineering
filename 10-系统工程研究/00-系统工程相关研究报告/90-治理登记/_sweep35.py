# -*- coding: utf-8 -*-
"""35 号 v2.0：库外活指针换算（只换他件里写的「35 号 §x.y」）。

    python 90-治理登记/_sweep35.py           # 预演：只列，不写
    python 90-治理登记/_sweep35.py --apply   # 写入

范围：报告库（00-系统工程相关研究报告/，含子目录）＋教材书＋训侧；**不含** 90-治理登记（走追注）、
      claude-memory（记忆不换算）、.ai-agent/.work-*（现场与备份）。
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # 00-系统工程相关研究报告
PROJ = os.path.dirname(ROOT)                                        # 10-系统工程研究
SKIP_DIR = ('90-治理登记', 'claude-memory', 'node_modules', '.git', '成书', 'build')

def skip(d):
    return d in SKIP_DIR or d.startswith('.')

MAP = {'2.1':'2.1','2.2':'2.2','2.3':'2.3','2.4':'2.4','2.4.1':'2.4.1','2.5':'2.5','2.6':'10.1',
       '3.1':'2.6','3.2':'2.7','3.3':'2.8','3.4':'2.9','3.5':'2.10',
       '4.1':'5.1','4.2':'5.2','4.3':'5.3','4.4':'5.4','4.5':'5.5',
       '5.1':'5.6','5.2':'5.7','5.3':'5.8',
       '6.1':'3.1','6.2':'3.2','6.3':'3.3','6.4':'3.4','6.5':'3.5',
       '7.1':'4.1','7.2':'4.2','7.3':'4.3','7.4':'4.4','7.5':'4.5',
       '12.1':'9.1','12.2':'9.2','12.3':'9.3','12.4':'9.4',
       '13.1':'6.1','13.2':'6.2','13.2.1':'6.2.1','13.2.2':'6.2.2',
       '13.3':'6.3','13.4':'6.4','13.5':'6.5','13.6':'6.6',
       '16.1':'6.7','16.2':'7.1','16.2.1':'7.2','16.2.2':'7.3','16.2.3':'7.4',
       '16.3':'8.1','16.3.1':'8.1.1','16.3.2':'8.1.2','16.4':'8.2',
       '16.5':'8.3','16.5.1':'8.3.1','16.5.2':'8.3.2','16.5.3':'8.3.3',
       '16.5.4':'8.3.4','16.5.5':'8.3.5','16.5.6':'8.3.6','16.6':'8.4','16.7':'8.5'}
CHAP = {'一':'1.6','二':'二','三':'二','四':'五','五':'五','六':'三','七':'四',
        '八':'11.1','九':'11.2','十':'11.3','十一':'11.4','十二':'九','十三':'六',
        '十四':'附录 C','十五':'10.2','十六':'六~八'}
PAT = re.compile(r'35\s*号\s*(?:研究报告)?\s*§(\d+(?:\.\d+)*|十[一二三四五六]|[一二三四五六七八九])')

# 合并型引用：原 §二 与 §三 并为一章，链条要收成一处
PRE = [('35 号 §二·§三', '35 号 §二'), ('35 号 §二、§三', '35 号 §二'),
       ('35 号 §二~§三', '35 号 §二')]

def conv(m):
    k = m.group(1)
    if k in MAP:
        return '35 号 §' + MAP[k]
    if k in CHAP:
        return '35 号 ' + ('附录 C' if CHAP[k].startswith('附录') else '§' + CHAP[k])
    return m.group(0)

def files():
    for base in (ROOT, PROJ):
        for dp, dns, fns in os.walk(base):
            dns[:] = [d for d in dns if not skip(d)]
            for fn in fns:
                if not fn.endswith('.md'):
                    continue
                if fn.startswith('35-架构定义与视图设计研究报告'):
                    continue
                yield os.path.join(dp, fn)

def main():
    apply = '--apply' in sys.argv
    total, hits = 0, {}
    for p in files():
        try:
            t = open(p, encoding='utf-8').read()
        except Exception:
            continue
        n = len(PAT.findall(t))
        if not n:
            continue
        t2 = t
        for a, b in PRE:
            t2 = t2.replace(a, b)
        new = PAT.sub(conv, t2)
        hits[os.path.relpath(p, PROJ)] = n
        total += n
        if apply and new != t:
            open(p, 'w', encoding='utf-8', newline='\n').write(new)
    print('%s：%d 件、%d 处' % ('已换算' if apply else '预演', len(hits), total))
    for k, v in sorted(hits.items(), key=lambda x: -x[1]):
        print('   %-72s %d' % (k, v))

main()
