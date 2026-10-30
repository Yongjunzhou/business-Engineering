#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""《架构师是个怎样的物种？》判留抽样复核器（第四病·批四立）

**为什么要有这一步**：盲读 8 段（手册 §4.7「漏率抽样」）测的是**漏**——"该改而没改"；
它测不出**冤**——"不该留却留了"。判读单里判留是判改的四五倍，若判留放水，量尺再准也白搭。
本脚本抽两族的判留各若干条，**只给原句与标的、不给任何先前判断**，交第二只眼睛盲判，
再由父代理核一致率：一致率低于八成的那一族，**该族全量复查**。

**池子口径**：用**改后的当前正文**（附录块已剔）扫命中处——改过的地方已经从文字里消失，
所以池子天然等于"判留"那一侧，不依赖判读单，也就不会把原判理由带进复核（防自我印证）。

用法（本目录下）：
    python 00-腔-判留抽样.py                 # 默认每族 10 条（破折／统称），种子固定
    python 00-腔-判留抽样.py --per 20        # 每族 20 条（样本小，20 条只能判方向）
    python 00-腔-判留抽样.py --seed 7        # 换一组抽样
    python 00-腔-判留抽样.py --ch 14 18      # 只在指定章里抽

产出（都在本目录 `.work-p6/` 下，不入库）：
    audit-items.md   题面——只有原句与标的，交给复核者
    audit-key.tsv    底稿——编号／章／段号／族／词／原判，父代理核一致率用

**一条纪律**：复核者不得打开 `00-腔-判读单-*` 与 `00-腔优化台账.md`，否则盲判失效。
"""
import os
import re
import sys
import random
import importlib.util
import io
import contextlib

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BOOK = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(BOOK, '00-冗余-量尺.py')
OUT = os.path.join(BOOK, '.work-p6')

_spec = importlib.util.spec_from_file_location('redund_ruler', BASE)
R = importlib.util.module_from_spec(_spec)
with contextlib.redirect_stdout(io.StringIO()):      # 屏蔽被 import 模块的自跑输出
    _spec.loader.exec_module(R)

# 与 00-腔-量尺.py 口径 v1.3 同一条正则（"这些年／那些年"不算统称；改口径两边一起改）
GENERIC = re.compile(r'(东西|这些(?!年|天|日子)|那些(?!年|天|日子)|这一套|这一类|这类|几件|几样|各地|各种|若干|同一样)')


def parse(path):
    """与 `00-冗余-量尺.py` 的 `paragraphs()` 同法切段，多记 block（最近一个二级标题）。"""
    out, buf = [], []
    block, sub, in_code = '', '', False
    with open(path, encoding='utf-8') as f:
        head = f.read()
    inline = ('**误解现场。**' in head) or ('**误解现场**。' in head)

    def flush():
        if not buf:
            return
        p = ' '.join(buf)
        m = R.LEAD.match(p)
        label = m.group(1) if m else ''
        k = R.kind(label) if (inline and label and R.kind(label) != 'argue') else R.kind(sub or block)
        out.append(dict(text=p, kind=k, block=block, sub=sub))
        del buf[:]

    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.strip().startswith('```'):
                in_code = not in_code
                flush()
                continue
            if in_code:
                continue
            if re.match(r'^## ', line):
                flush()
                block = re.sub(r'^#+\s*', '', line).strip()
                sub = ''
                continue
            if re.match(r'^### ', line):
                flush()
                sub = re.sub(r'^#+\s*', '', line).strip()
                continue
            if not line.strip():
                flush()
                continue
            if R.is_prose(line):
                if any(s in (sub or block) for s in R.SKIP):
                    continue
                buf.append(line.strip())
            else:
                flush()
    flush()
    for i, d in enumerate(out, 1):
        d['no'] = i
    return out


def pools(chapters):
    dash, gen = [], []
    for lbl, path in R.items():
        if chapters and lbl not in chapters:
            continue
        for p in parse(path):
            if '附录' in p['block']:
                continue                      # 与 00-腔-附录核查.py 同一口径
            t = p['text']
            for m in re.finditer('——', t):
                dash.append(dict(ch=lbl, no=p['no'],
                                 left=t[max(0, m.start() - 22):m.start()],
                                 right=t[m.end():m.end() + 22]))
            for m in GENERIC.finditer(t):
                gen.append(dict(ch=lbl, no=p['no'], word=m.group(1),
                                sent=t[max(0, m.start() - 26):min(len(t), m.end() + 26)]))
    return dash, gen


def main():
    a = sys.argv[1:]
    per, seed, chapters = 10, 20261029, None
    if '--per' in a:
        per = int(a[a.index('--per') + 1])
    if '--seed' in a:
        seed = int(a[a.index('--seed') + 1])
    if '--ch' in a:
        tail = []
        for x in a[a.index('--ch') + 1:]:
            if x.startswith('--'):
                break
            tail.append(x)
        chapters = set(x.zfill(2) for x in tail)

    dash, gen = pools(chapters)
    print(f'池子：破折 {len(dash)} 记｜统称 {len(gen)} 记（附录块已剔）')
    random.seed(seed)
    sd = random.sample(dash, min(per, len(dash)))
    sg = random.sample(gen, min(per, len(gen)))

    os.makedirs(OUT, exist_ok=True)
    lines = [f'# 判留抽样复核（破折 {len(sd)}＋统称 {len(sg)}，种子 {seed}）', '',
             '> 题面只给原句与标的，**不含任何先前判断**。逐题独立作答：判（留／撤／改）＋一句内容上的理由。', '']
    key = ['编号\t章\t段号\t族\t词\t原判']
    for i, it in enumerate(sd, 1):
        code = f'B{i:02d}'
        lines += [f'## 【{code}】ch{it["ch"]} 段{it["no"]}｜破折号', '',
                  f'原句（标的记作「—①—」）：{it["left"]}—①—{it["right"]}', '']
        key.append(f'{code}\tch{it["ch"]}\t{it["no"]}\t破折\t——\t判留')
    for i, it in enumerate(sg, 1):
        code = f'T{i:02d}'
        lines += [f'## 【{code}】ch{it["ch"]} 段{it["no"]}｜统称词「{it["word"]}」', '',
                  f'原句：{it["sent"]}', '']
        key.append(f'{code}\tch{it["ch"]}\t{it["no"]}\t统称\t{it["word"]}\t判留')

    open(os.path.join(OUT, 'audit-items.md'), 'w', encoding='utf-8', newline='').write('\n'.join(lines))
    open(os.path.join(OUT, 'audit-key.tsv'), 'w', encoding='utf-8', newline='').write('\n'.join(key))
    print('题面 → .work-p6/audit-items.md｜底稿 → .work-p6/audit-key.tsv')


if __name__ == '__main__':
    main()
