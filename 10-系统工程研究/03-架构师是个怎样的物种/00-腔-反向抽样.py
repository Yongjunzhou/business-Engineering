#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""《架构师是个怎样的物种？》反向抽样复核器（第四病·收口批立）

**它测的是「冤改」**——`00-腔-判留抽样.py` 测的是"该改而没改"（漏），它测不了
"不该改却改了"（冤）。做法相反：从**判改一侧**取，把同一处的**改前／改后两版**
遮掉来路、随机编成 A／B，交第二只眼睛只答一句"哪一版更像人写的、为什么"，
再由父代理核一致率：**判"改后更好"的比例低到某族不过半，就是该族有冤改**。

用法（本目录下）：
    python 00-腔-反向抽样.py 2eaee5a3            # 取该提交对上一提交的正文改动
    python 00-腔-反向抽样.py 2eaee5a3 --seed 7
    python 00-腔-反向抽样.py HEAD~1 HEAD         # 指定范围

产出（`.work-p6/` 下，不入库）：
    rev-items.md   题面——只有 A／B 两版与三问，不给章号段号、不给原判
    rev-key.tsv    底稿——编号／章／段序／哪一版是改后，父代理核一致率用

**一条纪律**：复核者不得读 `00-腔-判读单-*`、`00-腔优化台账.md`、`00-风格参考.md` §6.21。
"""
import os
import re
import sys
import difflib
import random
import subprocess
import glob

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BOOK = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BOOK, '.work-p6')


def chapters():
    out = []
    for f in sorted(glob.glob(os.path.join(BOOK, '*.md'))):
        n = os.path.basename(f)
        m = re.match(r'^(\d\d)-第(\d+)章-', n)
        if m and '从教材到问题分析' not in n:
            out.append((m.group(2).zfill(2), n))
    if os.path.exists(os.path.join(BOOK, '20-后记.md')):
        out.append(('后', '20-后记.md'))
    return out


def get(ref, name):
    r = subprocess.run(['git', 'show', '%s:./%s' % (ref, name)], cwd=BOOK, capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout.decode('utf-8')


def blocks(txt):
    txt = txt.replace('\r\n', '\n')
    out = [b.strip() for b in re.split(r'\n[ \t]*\n', txt)]
    return [b for b in out if b]


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return
    ref_new = a[0]
    ref_old = a[1] if len(a) > 1 and not a[1].startswith('--') else a[0] + '^'
    seed = 20261030
    if '--seed' in a:
        seed = int(a[a.index('--seed') + 1])

    pairs = []
    for lbl, name in chapters():
        old = get(ref_old, name)
        new = get(ref_new, name)
        if old is None or new is None or old == new:
            continue
        ob, nb = blocks(old), blocks(new)
        sm = difflib.SequenceMatcher(None, ob, nb, autojunk=False)
        k = 0
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag != 'replace':
                continue
            for x, y in zip(ob[i1:i2], nb[j1:j2]):
                k += 1
                pairs.append(dict(ch=lbl, idx=k, old=x, new=y))

    random.seed(seed)
    order = list(range(len(pairs)))
    random.shuffle(order)
    lines = ['# 反向抽样复核（同一处的两版文字，遮掉来路）', '',
             '> 每题给出同一段落的两个版本 A／B，问三件：① 哪一版更像人写的（A／B／两版一样）'
             '② 一句话理由 ③ 另一版有没有丢内容（有就说丢了什么，没有就写"无"）。',
             '> 逐题独立作答，不要互相参照，不要猜改动方向。', '']
    key = ['编号\t章\t段序\t改后是哪一版']
    for n, i in enumerate(order, 1):
        it = pairs[i]
        code = 'R%02d' % n
        # 随机决定 A／B 谁是改后
        a_is_new = random.random() < 0.5
        va, vb = (it['new'], it['old']) if a_is_new else (it['old'], it['new'])
        lines += ['## 【%s】' % code, '', '**A**：' + va, '', '**B**：' + vb, '',
                  '作答：① ＿＿ ② ＿＿ ③ ＿＿', '']
        key.append('%s\tch%s\t%d\t%s' % (code, it['ch'], it['idx'], 'A' if a_is_new else 'B'))

    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, 'rev-items.md'), 'w', encoding='utf-8', newline='').write('\n'.join(lines))
    open(os.path.join(OUT, 'rev-key.tsv'), 'w', encoding='utf-8', newline='').write('\n'.join(key))
    print('改动处 %d 处 → 题面 .work-p6/rev-items.md｜底稿 .work-p6/rev-key.tsv' % len(pairs))


if __name__ == '__main__':
    main()
