# -*- coding: utf-8 -*-
"""单字关：查单字当名词、单字当动词。只报，不判。"""
import sys, re, io

NOUN = {'号': '编号', '件': '文档', '格': '数据项', '册': '册名'}
VERB = {'取': '取用', '写': '写出', '看': '查看', '改': '改动', '记': '记录', '标': '标注',
        '挂': '挂上', '判': '判定', '核': '核对', '拆': '拆开', '列': '列出', '画': '画出',
        '填': '填进', '查': '查得'}
KEEP_N = set('合资严规表价品性独人蛇风')   # 合格 资格 格式 …
KEEP_V = set()                               # 前后连汉字即词素，已由邻字判掉

def cjk(c):
    return bool(re.match(r'[\u4e00-\u9fff]', c or ''))

def scan(path):
    hits = []
    for i, l in enumerate(io.open(path, encoding='utf-8'), 1):
        for m in re.finditer('[%s]' % ''.join(list(NOUN) + list(VERB)), l):
            a, b = m.start(), m.end()
            ch = l[a]
            prev = l[a-1] if a else ''
            nxt = l[b] if b < len(l) else ''
            if cjk(prev) or cjk(nxt):
                continue
            if ch in NOUN and (prev in KEEP_N or nxt in '式局外子言码段'):
                continue
            if ch == '号' and (prev.isdigit() or prev in 'N n ' or (prev == ' ' and a > 1 and l[a-2].isdigit())):
                continue  # 文档号：48 号 · 24 号，属名不属字段
            fix = NOUN.get(ch) or VERB.get(ch)
            hits.append((i, ch, fix, l.strip()[:40]))
    return hits

def main(argv):
    if not argv:
        print(__doc__); return 2
    bad = 0
    for p in argv:
        hits = scan(p)
        print('=' * 70)
        nn = [h for h in hits if h[1] in NOUN]
        vv = [h for h in hits if h[1] in VERB]
        print('%s　名词 %d 处、动词 %d 处' % (p.replace('\\', '/').split('/')[-1], len(nn), len(vv)))
        for title, group in (('单字的名词', nn), ('单字的动词', vv)):
            if not group:
                continue
            print('  —— %s' % title)
            for i, ch, fix, ctx in group:
                print('  L%-5d %s → %s   %s' % (i, ch, fix, ctx))
        bad += len(hits)
    return 0 if bad == 0 else 1

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
