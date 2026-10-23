#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""阶段七「四项对表」的随库量具：段长中位／句长中位／带人带例段占比／破折号密度。

**为什么单列一件**：手册 §1.7 的四项对表里，**段长中位**与**带人带例占比**这两项，
`00-风格参考-量尺.py` 不报（它报配比、红线与⑤酣畅三查），`00-表达-量尺.py` 也不报
（它报段数、段>150、句长、破折、白话、括号）——过去每章都要现写一段一次性脚本。
2026-10-23 第2章那轮把它固定下来，收进库里，供后面各章直接跑。

用法：
    python 00-四项对表.py "02-第2章-工程-让产品开发可重复.md"
    python 00-四项对表.py              # 不给文件名则 01~18 章逐章报

**口径与 `00-表达-量尺.py` 逐字一致**（同一把尺）：散文段的拼装、散文行的豁免
（标题／表格／引用块／清单／围栏）、句子的切分（只按「。」、≥2 个汉字）、中位取法
（`lens[len//2]`）、破折号计数（`——`）全部照抄；**本件只新增两项**：段长中位、
带人带例占比。改动口径必须两处同改，否则两只脚本会给出两套数。

判定线（手册 §1.7／风格参考 §6.12）：
    段长中位  叙事与判据体 34~40，论证体 45 起，**一律 ≤45**
    段>150    **0**（红线）
    句长中位  ≤24（19~20 最好）
    带人带例  ≥15%（自查线）
    破折号    ≤10‰（书级红线）
"""
import re
import sys
import os
import glob

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

HAN = re.compile(r'[\u4e00-\u9fff]')
BOOK = os.path.dirname(os.path.abspath(__file__))

# 案例人物与两个案例主体（同 00-案例设定.md §二 团队表；改一处两处同改）
NAMES = ['罗建', '顾言', '曹峰', '王默', '郑亮', '苏婷',
         '石军', '小周', '小张', '林涛', '赵刚', '吴浩', '季昭',
         '恒信', '冰链']


def han(s):
    return len(HAN.findall(s))


def is_prose(line):
    """逐字照抄 `00-表达-量尺.py`：散文行的豁免清单。"""
    t = line.strip()
    if not t:
        return False
    for pre in ('#', '|', '>', '```', '---', '- ', '* ', '+ ', '　'):
        if t.startswith(pre):
            return False
    if re.match(r'^\d+[.、)]\s', t):
        return False
    if re.match(r'^\*\*[^*]+：\*\*', t):      # 章前件标签行
        return False
    return True


def chapter_files():
    out = {}
    for name in sorted(os.listdir(BOOK)):
        m = re.match(r'^(\d\d)-第(\d+)章-(.+)\.md$', name)
        if m and '分析' not in name:
            out[int(m.group(2))] = os.path.join(BOOK, name)
    return out


def analyse(path):
    """逐字照抄 `00-表达-量尺.py` 的 analyse 前半段（散文段的拼装与切句）。"""
    paras, para = [], []
    in_code = False
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.strip().startswith('```'):
                in_code = not in_code
                continue
            if in_code:
                continue
            if not line.strip():
                if para:
                    paras.append(' '.join(para))
                    para = []
                continue
            if is_prose(line):
                para.append(line.strip())
            else:
                if para:
                    paras.append(' '.join(para))
                    para = []
    if para:
        paras.append(' '.join(para))

    text = '\n'.join(paras)
    total = han(text)

    plens = sorted(han(p) for p in paras)
    p_med = plens[len(plens) // 2] if plens else 0
    over150 = sum(1 for p in paras if han(p) > 150)
    p_max = plens[-1] if plens else 0

    sents = sorted(han(s) for s in re.split(r'。', text) if han(s) >= 2)
    s_med = sents[len(sents) // 2] if sents else 0
    s_max = sents[-1] if sents else 0

    hit = [p for p in paras if any(n in p for n in NAMES)]

    dash = text.count('——')

    return dict(total=total, n=len(paras), p_med=p_med, over150=over150, p_max=p_max,
                s_med=s_med, s_max=s_max, hit=len(hit), dash=dash)


def report(path, title=None):
    r = analyse(path)
    print('【%s】' % (title or os.path.basename(path)))
    print('  散文 %d 汉字／%d 段' % (r['total'], r['n']))
    print('  ① 段长中位 %d（线 ≤45）｜段>150 %d 段（须 0）｜最长 %d'
          % (r['p_med'], r['over150'], r['p_max']))
    print('  ② 句长中位 %d（线 ≤24）｜最长句 %d' % (r['s_med'], r['s_max']))
    print('  ③ 带人带例 %d/%d = %.0f%%（线 ≥15%%）'
          % (r['hit'], r['n'], 100.0 * r['hit'] / max(1, r['n'])))
    print('  ④ 破折号 %d 处 = %.2f‰（线 ≤10‰）' % (r['dash'], 1000.0 * r['dash'] / max(1, r['total'])))
    flag = []
    if r['p_med'] > 45:
        flag.append('段长中位超线')
    if r['over150']:
        flag.append('段>150 超红线')
    if r['s_med'] > 24:
        flag.append('句长中位超线')
    if 100.0 * r['hit'] / max(1, r['n']) < 15:
        flag.append('带人带例低于自查线')
    if 1000.0 * r['dash'] / max(1, r['total']) > 10:
        flag.append('破折号超线')
    print('  超线：%s' % ('、'.join(flag) if flag else '无'))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    if args:
        for a in args:
            report(a)
        return
    files = chapter_files()
    for ch in sorted(files):
        report(files[ch], 'ch%02d' % ch)


if __name__ == '__main__':
    main()
