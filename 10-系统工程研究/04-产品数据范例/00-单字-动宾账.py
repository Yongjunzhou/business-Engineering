# -*- coding: utf-8 -*-
"""单字动词分区账 v2：把每个动字按后接字分成五桶，五桶之和＝该字全文出现总数。
一 孤立：后接句读或空格，形式关已报。
二 词素：后接字与该字合成一个两字词（写出／判定／取值域的可入此桶者单列待裁）。
三 补语：后接的是可能补语、趋向补语、结果补语（写不出、判不过、改完），不成动宾，不在此轮。
四 动宾：后接的是宾语或宾语的数量（改一处、写户口表、判真假、标级别）——禁令第二条明写要写全的那种。
五 待裁：全线术语里含这个动字开头的（取值、判留、判改、列名、取名法），改名须人点头。
"""
import io, re, sys, collections

CI = {
    '取': '用决舍消而缔',
    '写': '法成明在出进到完清齐全死满下上回作字人户活去',
    '看': '到完得作图起见上过做',
    '改': '动法成到完后版称排序用并点空参装虚描结替',
    '记': '录忆进各写状到在按成处为行',
    '标': '题准对志注明出待示签级识是了记给或分字当不唯改汉疑档示',
    '挂': '靠上着解由在',
    '判': '定据例法断否词决',
    '核': '对到心后查见与表性并',
    '拆': '成分开解回',
    '列': '名清出齐全明在入',
    '填': '毕满进齐',
    '查': '法表见无来与',
}
DAI = {'取': '值', '判': '留改', '列': '标', '改': '名'}
BU = set('不得出进到完上下来去成回着了过起死歪掉满')   # 补语／体标记
NUM = set('一二三四五六七八九十两几多')                  # 数量宾语
PRON = set('什谁哪这那某各')                             # 代词宾语

out = []
for p in sys.argv[1:]:
    t = io.open(p, encoding='utf-8').read()
    name = p.replace('\\', '/').split('/')[-1]
    print('=' * 74)
    print(name, '　汉字', len(re.findall(r'[\u4e00-\u9fff]', t)))
    tot_all = collections.Counter()
    for v, ci in CI.items():
        occ = [m.start() for m in re.finditer(v, t)]
        if not occ:
            continue
        c = collections.Counter()
        for a in occ:
            nx = t[a + 1] if a + 1 < len(t) else ''
            if not nx or not re.match(r'[\u4e00-\u9fff]', nx):
                c['孤立'] += 1
            elif nx in DAI.get(v, ''):
                c['待裁'] += 1
            elif nx in BU:
                c['补语'] += 1
            elif nx in ci:
                c['词素'] += 1
            else:
                c['动宾'] += 1
                ln = t.count('\n', 0, a) + 1
                out.append((name, v, ln, t[max(0, a-14):a+16].replace('\n', '')))
        tot_all.update(c)
        print('  %-2s 共 %3d：孤立 %2d・词素 %3d・补语 %3d・动宾 %3d・待裁 %2d'
              % (v, sum(c.values()), c['孤立'], c['词素'], c['补语'], c['动宾'], c['待裁']))
    print('  合计：孤立 %d・词素 %d・补语 %d・动宾 %d・待裁 %d＝%d'
          % (tot_all['孤立'], tot_all['词素'], tot_all['补语'], tot_all['动宾'], tot_all['待裁'], sum(tot_all.values())))
print('=' * 74)
print('动宾逐处共 %d 处' % len(out))
for name, v, ln, ctx in out:
    print('%s L%-5d %s  %s' % (name[:6], ln, v, ctx))
