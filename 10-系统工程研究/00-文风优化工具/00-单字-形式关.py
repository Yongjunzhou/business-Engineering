# -*- coding: utf-8 -*-
"""单字关：查单字当名词、单字当动词。只报，不判。"""
import sys, re, io

NOUN = {'号': '编号', '件': '文档', '格': '数据项', '册': '规范', '栏': '字段', '卡': '48 号卡', '名': '名称'}
VERB = {'取': '取用', '写': '写出', '看': '查看', '改': '改动', '记': '记录', '标': '标注',
        '挂': '挂上', '判': '判定', '核': '核对', '拆': '拆开', '列': '列出', '画': '画出',
        '填': '填进', '查': '查得'}
KEEP_N = set('合资严规表价品性独人蛇风')   # 合格 资格 格式 …
KEEP_V = set()                               # 前后连汉字即词素，已由邻字判掉
# 单字站着的样子：卡上、栏与、名的、读的。后面那个字是虚词或方位词，就不算复合词。
# 名词把方位词算进来（卡上、栏里）；动词不算，否则挂上、判过、写到会被误报（2026-11-28 用户指「栏与不成立判定照卡写」）。
NOUN_AFTER = set('的了与和及是不都上里中前后这那')
VERB_AFTER = set('的了与和及是不都这那')
PREV_FUNC = set('的了与和及是把被由对为从按照向于将并之其各每这那')
MEASURE = '列行条份项处种位页章节约次件张个'

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
            after = NOUN_AFTER if ch in NOUN else VERB_AFTER
            if (cjk(prev) and prev not in PREV_FUNC) or (cjk(nxt) and nxt not in after):
                continue
            if prev in '0123456789一二三四五六七八九十百千两几这那每各半多' and ch in MEASURE:
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
