#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""SOSA 中英文对照版 · 机械关（四关）

用法：
    python 00-对照核对.py            # 核本目录全部已译分册
    python 00-对照核对.py 01-introduction.md
退出码 0 为过；1 为有 FAIL。

四关（口径见 SOSA-术语对照表.md §十一）：
  1 段数对齐——英文段与中文段一一交替，不漏、不并、不多
  2 禁译串——译前译后的多重集完全一致（型号码／标准号／引脚号／电压值／链接）
  3 术语一致性——术语表的直译词条，其英文在原册出现 ≥3 次而中文一次未见的，报 WARN
  4 规范动词——每个含 shall/should/must 的英文段，其配对中文段须含 应／宜／必须
另核：页锚、图引用、表题三者多重集一致；表格列数一致；中文段里出现「译注」以外的英文夹注漏译迹象。
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
    (u'SLT 型号码', re.compile(r'SLT[0-9A-Za-z][\w\.\-]*')),
    (u'MOD 型号码', re.compile(r'MOD[0-9A-Za-z][\w\.\-]*')),
    (u'J 连接器号', re.compile(r'\bJ(?:10|[1-9])\b')),
    (u'MIL 标准号', re.compile(r'MIL-(?:STD|DTL|PRF|HDBK)-[0-9A-Za-z/\-\.]+')),
    (u'SAE 标准号', re.compile(r'\bAS\d{3,}(?:/\d+)?')),
    (u'电压电流值', re.compile(r'\b\d+V\s?DC@\d+A\b')),
    (u'Excel 文件名', re.compile(r'SOSA_[\w\-\.]+\.xlsx')),
    (u'链接', re.compile(r'https?://[^\s\)\]]+')),
    (u'信号名', re.compile(r'\b(?:PWR_EN(?:_RTN)?|MASTER_ARM(?:_RET)?|D[ABCD][+-]|TX[1-4][+-]|RX[1-4][+-])\b')),
]

HEAD = re.compile(r'^#{1,6}\s')
ANCHOR = re.compile(u'^<!--.*-->$', re.S)
IMG = re.compile(r'^!\[.*\]\(.*\)$', re.S)
TABLE = re.compile(r'^\|')
LABEL = re.compile(r'^(\*[^*]|\*\*Table)')
RULE = re.compile(r'^(---|\*\*\*)$')
TPL = re.compile(u'^(Rule|Recommendation|Suggestion|Permission|Observation|规则|推荐|建议|许可|观察)\\s*<[a-z]+>-<[a-z]+>$')
PAGEQ = re.compile(u'^>\\s*原书\\s*p\\.')
NOTEQ = re.compile(u'^>\\s*\\*\\*译注\\*\\*')
URLONLY = re.compile(r'^https?://\S+$')

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
    for b in out:
        s = b.strip()
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
        elif TPL.match(s) or PAGEQ.match(s) or NOTEQ.match(s) or URLONLY.match(s):
            res.append(('label', b))
        elif RULE.match(s):
            res.append(('rule', b))
        else:
            res.append(('para', b))
    return res


def lang(body):
    """判语言。判据以"有没有汉字"为主：本书英文侧不含汉字，
    故含汉字的块几乎必是译文（哪怕它夹着大段文件名、URL、型号码）。"""
    s = body
    if s.startswith('>'):
        s = s.lstrip('> ').strip()
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    c = len(CJK.findall(s))
    l = len(re.findall(r'[A-Za-z]', s))
    if c == 0 and l == 0:
        return 'NONE'
    if c >= 6:
        return 'ZH'
    if c >= 1 and l <= 8:
        return 'ZH'
    if c >= 1:
        return 'MIX'
    return 'EN'


def norm_anchor(b):
    return re.sub(r'\s+', ' ', b.strip())


def norm_img(b):
    m = re.search(r'\(([^)]+)\)', b)
    return os.path.basename(m.group(1)) if m else b


def parse_glossary():
    """返回 [(英文, 中文, 档)]，只取含 档 列的表行。"""
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
        zh = re.sub(r'（.*?）', '', zh).strip()
        if not zh:
            continue
        rows.append((en, zh, grade))
    return rows


def table_check(txt):
    """表格列数：GFM 按分隔行定列数，少一格则该列静默消失。"""
    fails = []
    lines = txt.split('\n')
    i = 0
    while i < len(lines):
        if lines[i].startswith('|'):
            j = i
            while j < len(lines) and lines[j].startswith('|'):
                j += 1
            rows = lines[i:j]
            cols = [len(r.strip().strip('|').split('|')) for r in rows]
            if len(set(cols)) != 1:
                fails.append(u'表格列数不齐（第 %d 行起）：%s' % (i + 1, cols))
            i = j
        else:
            i += 1
    return fails


def check_one(name, verbose=True):
    src_path = os.path.join(SRC, name)
    dst_path = os.path.join(HERE, name)
    fails, warns = [], []
    if not os.path.exists(dst_path):
        warns.append(u'尚未译：%s' % name)
        return fails, warns
    d_txt = read(dst_path)
    if not os.path.exists(src_path):
        # 样张类：无英文侧对应件，只核表列数与空段
        fails += table_check(d_txt)
        if verbose:
            print(u'—— %s ｜ 无英文侧对应件，仅核表列数' % name)
            for f in fails:
                print(u'  FAIL ' + f)
        return fails, warns

    s_txt, d_txt = read(src_path), read(dst_path)
    sb, db = blocks(s_txt), blocks(d_txt)
    # ---- 关 1 段数对齐 ----
    seq = []
    for kind, body in db:
        if kind != 'para':
            continue
        lg = lang(body)
        seq.append((lg, body))
    n_en = sum(1 for lg, _ in seq if lg == 'EN')
    n_zh = sum(1 for lg, _ in seq if lg == 'ZH')
    if n_en != n_zh:
        fails.append(u'段数不齐：英文段 %d／中文段 %d' % (n_en, n_zh))
    for i, (lg, body) in enumerate(seq):
        prev = seq[i - 1][0] if i else None
        if lg == 'EN':
            if i + 1 >= len(seq) or seq[i + 1][0] != 'ZH':
                fails.append(u'英文段其后不是中文段：%s…' % body[:40].replace('\n', ' '))
        elif lg == 'ZH':
            if prev != 'EN':
                fails.append(u'中文段其前不是英文段：%s…' % body[:40].replace('\n', ' '))
        elif lg == 'MIX':
            warns.append(u'段语言混杂（需人看）：%s…' % body[:50].replace('\n', ' '))
    # 英文原册的段落须与对照册的英文段逐一相同（防改字、并段、拆段、丢段）
    s_para = [b.strip() for k, b in sb if k == 'para']
    d_en = [b.strip() for lg, b in seq if lg == 'EN']
    if len(s_para) != len(d_en):
        fails.append(u'英文段数变了：原册 %d 段／对照册英文段 %d 段' % (len(s_para), len(d_en)))
    for i, (a, b) in enumerate(zip(s_para, d_en)):
        if a != b:
            fails.append(u'英文第 %d 段与原文不一致（并段／拆段／改字）：原文「%s…」／本册「%s…」' % (
                i + 1, a[:40].replace('\n', ' '), b[:40].replace('\n', ' ')))
            break

    # ---- 页锚／图／表题 ----
    sa = Counter(norm_anchor(b) for k, b in sb if k == 'anchor')
    da = Counter(norm_anchor(b) for k, b in db if k == 'anchor')
    if sa != da:
        miss = sa - da
        extra = da - sa
        fails.append(u'页锚不一致：缺 %d／多 %d（缺例：%s）' % (
            sum(miss.values()), sum(extra.values()),
            list(miss)[0] if miss else '-'))
    sa_seq = [norm_anchor(b) for k, b in sb if k == 'anchor']
    da_seq = [norm_anchor(b) for k, b in db if k == 'anchor']
    if sa != da or sa_seq != da_seq:
        if sa == da:
            fails.append(u'页锚位置次序变了（首处差异：%s）' % next(
                (x for x, y in zip(sa_seq, da_seq) if x != y), '-'))
    si = Counter(norm_img(b) for k, b in sb if k == 'image')
    di = Counter(norm_img(b) for k, b in db if k == 'image')
    if si != di:
        miss = si - di
        extra = di - si
        fails.append(u'图引用不一致：缺 %s／多 %s' % (dict(miss) or '-', dict(extra) or '-'))

    # 表题：英文侧 `**Table N:` ；对照侧同块内并置，取 Table 号比对
    st = Counter(re.findall(r'Table\s+(\d+)\s*:', s_txt))
    dt = Counter(re.findall(r'Table\s+(\d+)\s*:', d_txt))
    if st != dt:
        fails.append(u'表题号不一致：原册 %s／对照册 %s' % (sorted(st), sorted(dt)))

    # ---- 关 2 禁译串 ----
    s_all = ''.join(b + '\n' for k, b in sb if k not in ('anchor',))
    d_all = ''.join(b + '\n' for k, b in db if k not in ('anchor',))
    # 对照册的中文侧可能重复英文串（如术语并置），故按"集合"比，不看次数
    for label, pat in PATTERNS:
        a = set(pat.findall(s_all))
        b = set(pat.findall(d_all))
        miss = a - b
        if miss:
            fails.append(u'禁译串丢失（%s）：%s' % (label, u'、'.join(sorted(miss)[:6])))

    # ---- 关 5 表格列数 ----
    fails += table_check(d_txt)

    # ---- 关 3 术语一致性（WARN）----
    for en, zh, grade in parse_glossary():
        cnt = len(re.findall(r'\b%s\b' % re.escape(en), s_txt, re.I))
        if cnt >= 3 and zh not in d_txt:
            warns.append(u'术语疑漏译：%s（%s）英文 %d 次，中文「%s」0 次' % (en, grade, cnt, zh))

    # ---- 关 4 规范动词 ----
    pairs = []
    i = 0
    while i < len(seq):
        if seq[i][0] == 'EN' and i + 1 < len(seq) and seq[i + 1][0] == 'ZH':
            pairs.append((seq[i][1], seq[i + 1][1]))
        i += 1
    for en_body, zh_body in pairs:
        for word, cw in VERB_EN:
            if re.search(r'\b%s\b' % word, en_body, re.I) and cw not in zh_body:
                fails.append(u'规范动词缺中文：%s 段含 %s，中文段无「%s」：%s…' % (
                    word, word, cw, en_body[:36].replace('\n', ' ')))

    if verbose:
        print(u'—— %s ｜ 段 %d/%d ｜ 页锚 %d ｜ 图 %d ｜ 表题 %d' % (
            name, n_en, n_zh, sum(da.values()), sum(di.values()), sum(dt.values())))
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
                       and not n.startswith('00-'))
    total_f, total_w, done = 0, 0, 0
    for name in names:
        f, w = check_one(name)
        total_f += len(f)
        total_w += len(w)
        if os.path.exists(os.path.join(HERE, name)):
            done += 1
    print(u'\n已译分册 %d／%d ｜ FAIL %d ｜ WARN %d' % (
        done, len(names), total_f, total_w))
    return 1 if total_f else 0


if __name__ == '__main__':
    sys.exit(main())
