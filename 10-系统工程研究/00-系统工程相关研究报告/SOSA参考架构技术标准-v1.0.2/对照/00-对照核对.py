#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""SOSA 中英文对照版 · 机械关（六关）

用法：
    python 00-对照核对.py            # 核本目录全部已译分册
    python 00-对照核对.py 03-xxx.md   # 核一册
退出码 0 为过；1 为有 FAIL。

六关：
  1 段对齐（按原文逐段文本匹配，不靠语言判别）：原文每段都要出现一次、次序不变，
    且每段英文后紧跟且只跟一段中文（非原文段即视为译文）；纯代码段与中文行不参与比对
  2 禁译串：译前译后集合一致（型号码／标准号／引脚号／电压值／链接／信号名）
  3 术语一致性：术语表直译词条英文正文 ≥3 次而中文一次未见的，报 WARN
  4 规范动词：含 shall/should/must 的英文段，其配对中文段须含 应／宜／必须
  5 表列数：同一张表内各行格数一致（横幅行按表头宽度补齐后放过）
  6 表内英文格照录：每格须为原格本身或「原格＋并置中文」（格内多行允许逐行交错）
另核：页锚、图引用、表题三者多重集一致。
"""
import io
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, '..'))
GLOSSARY = os.path.join(HERE, 'SOSA-术语对照表.md')

CJK = re.compile(u'[\u4e00-\u9fff]')

PATTERNS = [
    (u'SLT 型号码', re.compile(r'SLT[0-9A-Za-z][\w.\-]*')),
    (u'MOD 型号码', re.compile(r'MOD[0-9A-Za-z][\w.\-]*')),
    (u'J 连接器号', re.compile(r'\bJ(?:10|[1-9])\b')),
    (u'MIL 标准号', re.compile(r'MIL-(?:STD|DTL|PRF|HDBK)-[0-9A-Za-z/\-.]+')),
    (u'SAE 标准号', re.compile(r'\bAS\d{3,}(?:/\d+)?')),
    (u'电压电流值', re.compile(r'\b\d+V\s?DC@\d+A\b')),
    (u'Excel 文件名', re.compile(r'SOSA_[\w.\-]+\.xlsx')),
    (u'链接', re.compile(r'https?://\S+')),
    (u'信号名', re.compile(r'\b(?:PWR_EN(?:_RTN)?|MASTER_ARM(?:_RET)?|D[ABCD][+-]|TX[1-4][+-]|RX[1-4][+-])\b')),
]

HEAD = re.compile(r'^#{1,6}\s')
ANCHOR = re.compile(u'^<!--.*-->$', re.S)
IMG = re.compile(r'^!\[.*\]\(.*\)$', re.S)
TABLE = re.compile(r'^\|')
LABEL = re.compile(r'^(\*[^*]|\*\*Table)')
RULE = re.compile(r'^(---|\*\*\*)$')
TPL = re.compile(u'^(Rule|Recommendation|Suggestion|Permission|Observation|规则|推荐|建议|许可|观察)\s*<[a-z]+>-<[a-z]+>$')
PAGEQ = re.compile(u'^>\s*原书\s*p\.')
NOTEQ = re.compile(u'^>\s*\*\*译注\*\*')
READQ = re.compile(u'^>\s*\*\*本表读法\*\*')
TRANSNOTE = re.compile(u'^>\s*转写说明')
SUMQ = re.compile(u'^>\s*\*\*小结\*\*')
BOLDLABEL = re.compile(u'^\\*\\*(?:Rule|Recommendation|Suggestion|Permission|Observation|Note|注|小结)[^*]*\\*\\*$'
                       u'|^\\*\\*#\\d+ [^*]*\\*\\*$'
                       u'|^\\*\\*[^*]*｜[^*]*\\*\\*$')   # 加粗标目／原则题名／含「｜」的分组标题：都是装置块
URLONLY = re.compile(r'^https?://\S+$')
NOTEONLY = re.compile(u'^(NOTE|注)\\s*\\d+$')

VERB_EN = [('shall', u'应'), ('should', u'宜'), ('must', u'必须')]


def read(path):
    return io.open(path, encoding='utf-8').read()


def blocks(text):
    """按空行切块；代码围栏内整块跳过。返回 [(kind, body)]。"""
    out, buf, fence = [], [], False
    for line in text.split('\n'):
        if line.startswith('```'):
            fence = not fence
            buf.append(line)
            continue
        if fence:
            buf.append(line)
            continue
        if line.strip() == '':
            if buf:
                out.append('\n'.join(buf))
                buf = []
            continue
        buf.append(line)
    if buf:
        out.append('\n'.join(buf))

    res = []
    skip = False
    for b in out:
        s = b.strip()
        if s.startswith(u'<!-- 未译') or s.startswith(u'<!-- 装置'):
            skip = True
            res.append(('mark', b))
            continue
        if s.startswith(u'<!-- /未译') or s.startswith(u'<!-- /装置'):
            skip = False
            res.append(('mark', b))
            continue
        if skip:
            if HEAD.match(s):
                res.append(('head', b))
            elif ANCHOR.match(s):
                res.append(('anchor', b))
            elif IMG.match(s):
                res.append(('image', b))
            elif TABLE.match(s):
                res.append(('table', b))
            else:
                res.append(('skip', b))
            continue
        if HEAD.match(s):
            res.append(('head', b))
        elif ANCHOR.match(s):
            res.append(('anchor', b))
        elif IMG.match(s):
            res.append(('image', b))
        elif TABLE.match(s):
            res.append(('table', b))
        elif LABEL.match(s) and s.endswith('*'):
            res.append(('label', b))
        elif RULE.match(s):
            res.append(('rule', b))
        elif TPL.match(s) or PAGEQ.match(s) or NOTEQ.match(s) or URLONLY.match(s) \
                or READQ.match(s) or TRANSNOTE.match(s) or SUMQ.match(s) \
                or NOTEONLY.match(s) \
                or BOLDLABEL.match(s):
            res.append(('label', b))
        else:
            res.append(('para', b))
    return res


def lang(body):
    """只用于报「语言混杂」提示，不参与配对判定。"""
    s = body
    if s.startswith('>'):
        s = s.lstrip('> ').strip()
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    c = len(CJK.findall(s))
    l = len(re.findall(r'[A-Za-z]', s))
    if c == 0:
        return 'EN'
    if l == 0:
        return 'ZH'
    if c >= 6:
        return 'ZH'
    if l >= 20 and c <= 3:
        return 'EN'
    if c >= 1 and l <= 8:
        return 'ZH'
    return 'MIX'


def rows_of(txt):
    """把 txt 里的每张表切成 [[cells,...], ...]。"""
    out, lines, i = [], txt.split('\n'), 0
    while i < len(lines):
        if lines[i].startswith('|'):
            j = i
            while j < len(lines) and lines[j].startswith('|'):
                j += 1
            out.append([[c.strip() for c in r.strip().strip('|').split('|')]
                        for r in lines[i:j]])
            i = j
        else:
            i += 1
    return out


def table_check(txt):
    """同一张表内各行格数须一致；横幅行（只有一个非空格）按表头宽度补齐后放过。"""
    fails = []
    for n, rows in enumerate(rows_of(txt), 1):
        target = len(rows[1]) if len(rows) > 1 else len(rows[0])
        bad = []
        for i, r in enumerate(rows, 1):
            if len(r) == target:
                continue
            if sum(1 for c in r if c.strip()) <= 1 and len(r) < target:
                continue
            bad.append((i, len(r)))
        if bad:
            fails.append(u'第 %d 张表列数不齐（目标 %d 格）：%s' % (n, target, bad))
    return fails


def frag_ok(ca, cb):
    """格内多行并置：英文各片须在对照格里按序出现（允许逐行交错）。"""
    frags = [f.strip() for f in ca.split('<br>') if f.strip()]
    if len(frags) <= 1:
        return False
    pos = 0
    for f in frags:
        k = cb.find(f, pos)
        if k < 0:
            return False
        pos = k + len(f)
    return True


def cell_check(src_txt, dst_txt):
    """表内英文格照录：对照册每格须为原格本身，或「原格＋并置中文」。

    表 5 特办（一张巨表按模块切成多张、组标题行改作加粗小标题、每组重复表头）
    走另一支：要求原文每一数据行都在对照册里按序出现（只比英文），不要求逐表对齐。
    """
    fails = []
    st, dt = rows_of(src_txt), rows_of(dst_txt)
    if len(st) == 1 and len(dt) > 1:
        expect = [r for r in st[0][2:] if sum(1 for c in r if c.strip()) > 1]
        flat = [r for t in dt for r in t]
        k = 0
        for r in flat:
            if k >= len(expect):
                break
            e = [c.replace('**', '').strip() for c in expect[k]]
            g = [c.replace('**', '').strip() for c in r]
            ok = True
            for ci, ce in enumerate(e):
                if not ce:
                    continue
                cg = g[ci] if ci < len(g) else ''
                if not (cg == ce or cg.startswith(ce) or frag_ok(ce, cg)):
                    ok = False
                    break
            if ok:
                k += 1
        if k < len(expect):
            fails.append(u'表 5 特办：原文数据行 %d 行，只按序匹配到 %d 行（第 %d 行起对不上）：%s'
                         % (len(expect), k, k + 1,
                            '｜'.join(c[:24] for c in expect[k] if c.strip())))
        return fails

    if len(st) != len(dt):
        fails.append(u'表数不一致：原文 %d／对照 %d' % (len(st), len(dt)))
    for ti, (a, b) in enumerate(zip(st, dt), 1):
        if len(a) != len(b):
            fails.append(u'第 %d 张表行数不一致：原文 %d／对照 %d' % (ti, len(a), len(b)))
            continue
        for ri, (ra, rb) in enumerate(zip(a, b), 1):
            if ri == 2:
                continue
            n = max(len(ra), len(rb))
            for ci in range(n):
                ca = ra[ci] if ci < len(ra) else ''
                cb = rb[ci] if ci < len(rb) else ''
                ca = ca.replace('**', '').strip()
                cb = cb.replace('**', '').strip()
                if not ca or ca == cb:
                    continue
                if frag_ok(ca, cb):
                    continue
                if not cb.startswith(ca):
                    fails.append(u'第 %d 表 行 %d 列 %d 英文被改：原「%s」→ 对照「%s」'
                                 % (ti, ri, ci + 1, ca[:36], cb[:36]))
    return fails


def norm_para(b):
    """段落比对前的归一。

    1 按行丢掉「中文行」（≥6 个汉字）：源件里英文表注与中文转写说明常同处一块，
      对照册又在同一块里插了中文注；这些都属装置文字，不参与英文比对。
    2 再剥引用记号、剥源件给英文 NOTE 冠上的「注：」，压空白。
    """
    keep = []
    for line in b.strip().split('\n'):
        if len(CJK.findall(line)) >= 6:
            continue
        if re.match(r'^>\s*$', line.strip()):   # 引用块里的空引用行，不参与比对
            continue
        keep.append(line)
    s = '\n'.join(keep).strip()
    s = re.sub(u'^>\s*', '', s)
    s = re.sub(u'^注\s*[：:]\s*', '', s)
    s = re.sub(u'^NOTE\s*\d*\s*[：:]?\s*', '', s, flags=re.I)
    s = re.sub(r'\s+', ' ', s).strip()
    if not s:
        # 整段都是中文（转换件自带的说明）时，退回原文，供下面按文本识别「中文注」
        s = re.sub(r'\s+', ' ', b.strip())
    return s


def norm_anchor(b):
    return re.sub(r'\s+', ' ', b.strip())


def norm_img(b):
    m = re.search(r'\(([^)]+)\)', b)
    return os.path.basename(m.group(1)) if m else b


def parse_glossary():
    rows = []
    if not os.path.exists(GLOSSARY):
        return rows
    for line in read(GLOSSARY).split('\n'):
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 3:
            continue
        if set(cells[0]) <= set('-: '):
            continue
        en, zh, grade = cells[0], cells[1], cells[2]
        if grade not in (u'直译', u'存原词', u'自拟'):
            continue
        if not re.match(r'^[A-Za-z]', en):
            continue
        zh = re.sub(u'（.*?）', '', zh).strip()
        if not zh:
            continue
        rows.append((en, zh, grade))
    return rows


def pair_units(src_paras, dst_paras):
    """按原文逐段文本匹配，返回 (配对列表, 失败列表)。"""
    fails = []
    src_n = [norm_para(x) for x in src_paras]
    dst_n = [norm_para(x) for x in dst_paras]
    pairs, k, i = [], 0, 0
    while i < len(dst_paras):
        b = dst_paras[i].strip()
        if k < len(src_paras) and dst_n[i] == src_n[k]:
            zh = []
            j = i + 1
            while j < len(dst_paras) and (k + 1 >= len(src_paras)
                                          or dst_n[j] != src_n[k + 1]):
                if dst_n[j] == src_n[k]:
                    break
                zh.append(dst_paras[j])
                j += 1
            pairs.append((b, zh))
            inline = len(CJK.findall(b)) >= 6      # 块内自带中文（如英文表注里插了中文注）
            if not zh and not inline and re.search(r'[A-Za-z]', b):
                fails.append(u'英文段其后无中文：%s…' % b[:40].replace('\n', ' '))
            if len(zh) > 1:
                fails.append(u'英文段其后中文段不止一段（%d 段）：%s…'
                             % (len(zh), b[:34].replace('\n', ' ')))
            k += 1
            i = j
        else:
            fails.append(u'多出来的非原文段（前面不是待配英文段）：%s…'
                         % b[:40].replace('\n', ' '))
            i += 1
    if k < len(src_paras):
        fails.append(u'原文有 %d 段未出现在对照册（自第 %d 段起）：%s…'
                     % (len(src_paras) - k, k + 1, src_paras[k][:40].replace('\n', ' ')))
    return pairs, fails


def check_one(name, verbose=True):
    src_path = os.path.join(SRC, name)
    dst_path = os.path.join(HERE, name)
    fails, warns = [], []
    if not os.path.exists(dst_path):
        warns.append(u'尚未译：%s' % name)
        return fails, warns
    d_txt = read(dst_path)
    if not os.path.exists(src_path):
        fails += table_check(d_txt)
        if verbose:
            print(u'—— %s ｜ 无英文侧对应件，仅核表列数' % name)
            for f in fails:
                print(u'  FAIL ' + f)
        return fails, warns

    s_txt = read(src_path)
    sb, db = blocks(s_txt), blocks(d_txt)

    src_paras = [b.strip() for k, b in sb if k == 'para']
    dst_paras = [b for k, b in db if k == 'para']
    # 「未译区」（如前置册的印刷式目录与图表清单）内的段落不在对照册里成段，
    # 只要原文逐字出现在未译区里，就不再要求它配对。
    skip_set = set()
    for k, b in db:
        if k == 'skip':
            for line in b.split('\n'):
                n = norm_para(line)
                if n:
                    skip_set.add(n)
    if skip_set:
        dst_norms = set(norm_para(p) for p in dst_paras)
        src_paras = [p for p in src_paras
                     if norm_para(p) not in skip_set or norm_para(p) in dst_norms]
    pairs, p_fails = pair_units(src_paras, dst_paras)
    fails += p_fails
    n_en, n_zh = len(pairs), sum(len(z) for _, z in pairs)

    for en, zh in pairs:
        if zh and lang(zh[0]) == 'MIX':
            warns.append(u'中文段语言混杂（需人看）：%s…' % zh[0][:44].replace('\n', ' '))
        if not zh:
            continue
        en_s = len(re.findall(r'[.!?](?:\s|$)', en))
        zh_s = len(re.findall(u'[。！？]', zh[0]))
        if en_s >= 4 and zh_s * 2 < en_s:
            warns.append(u'段内句数疑偏少（英 %d 句／中 %d 句，查有无删译）：%s…'
                         % (en_s, zh_s, en[:36].replace('\n', ' ')))

    def _is_page(x):
        return x.strip().startswith(u'<!-- 原书 p.') or x.strip().startswith(u'<!--原书 p.')
    sa = Counter(norm_anchor(b) for k, b in sb if k == 'anchor' and _is_page(b))
    da = Counter(norm_anchor(b) for k, b in db if k == 'anchor' and _is_page(b))
    if sa != da:
        fails.append(u'页锚不一致：原文 %d／对照 %d（缺 %d／多 %d）'
                     % (sum(sa.values()), sum(da.values()),
                        sum((sa - da).values()), sum((da - sa).values())))
    si = Counter(norm_img(b) for k, b in sb if k == 'image')
    di = Counter(norm_img(b) for k, b in db if k == 'image')
    if si != di:
        fails.append(u'图引用不一致：原文 %s／对照 %s' % (dict(si) or '-', dict(di) or '-'))
    st = Counter(re.findall(r'^\*\*Table\s+(\d+)\s*:', s_txt, re.M))
    dt = Counter(re.findall(r'^\*\*Table\s+(\d+)\s*:', d_txt, re.M))
    if st != dt:
        fails.append(u'表题号不一致：原文 %s／对照 %s' % (sorted(st), sorted(dt)))

    s_all = '\n'.join(b for k, b in sb if k != 'anchor')
    d_all = '\n'.join(b for k, b in db if k != 'anchor')
    for label, pat in PATTERNS:
        a, b = set(pat.findall(s_all)), set(pat.findall(d_all))
        miss = a - b
        if miss:
            fails.append(u'禁译串丢失（%s）：%s' % (label, u'、'.join(sorted(miss)[:6])))

    fails += table_check(d_txt)
    fails += cell_check(s_txt, d_txt)

    s_para_txt = '\n'.join(src_paras)
    for en, zh, grade in parse_glossary():
        cnt = len(re.findall(r'\b%s\b' % re.escape(en), s_para_txt, re.I))
        if cnt >= 3 and zh not in d_txt:
            warns.append(u'术语疑漏译：%s（%s）英文正文 %d 次，中文「%s」0 次'
                         % (en, grade, cnt, zh))

    for en, zh in pairs:
        if not zh:
            continue
        # 惯用 should（「It should be noted that…」「Should any viewer…」）不是规范动词，先抹掉
        en_chk = re.sub(r'(?i)\b(?:it should be noted|should be noted|should any)\b', ' ', en)
        for word, cw in VERB_EN:
            if re.search(r'\b%s\b' % word, en_chk, re.I) and cw not in zh[0]:
                fails.append(u'规范动词缺中文：%s 段含 %s，中文段无「%s」：%s…'
                             % (word, word, cw, en[:34].replace('\n', ' ')))

    if verbose:
        print(u'—— %s ｜ 段 %d/%d ｜ 页锚 %d ｜ 图 %d ｜ 表题 %d'
              % (name, n_en, n_zh, sum(da.values()), sum(di.values()), sum(dt.values())))
        for f in fails:
            print(u'  FAIL ' + f)
        for w in warns:
            print(u'  WARN ' + w)
    return fails, warns


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    if args:
        names = args
    else:
        names = sorted(n for n in os.listdir(HERE)
                       if n.endswith('.md') and re.match(r'^\d\d-', n)
                       and (n == '00-front-matter.md' or not n.startswith('00-')))
    total_f, total_w, done = 0, 0, 0
    for name in names:
        f, w = check_one(name)
        total_f += len(f)
        total_w += len(w)
        if os.path.exists(os.path.join(HERE, name)):
            done += 1
    print(u'\n已译分册 %d／%d ｜ FAIL %d ｜ WARN %d' % (done, len(names), total_f, total_w))
    return 1 if total_f else 0


if __name__ == '__main__':
    sys.exit(main())
