#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第13章：35 号 §十三（视图设计）＋§六（Step6~9）引用链逐条回正本核（量具）

用途：手册 §1.4.1「唯一不能后补的一步」——**引文回标准正本逐字核**。
      本脚本把 35 号 §十三 用到的每一条正本特征串，拿到库内正本里精确检索，
      输出「命中／未命中 ＋ 正本行号 ＋ 该行所属节号」。

口径
- 特征串取**英文原文**（不取中文译文）——手册 §1.4.1 核法第 1 条。
- 匹配＝**大小写敏感的纯子串**；命中多处时全部列出，人工判该引哪一处。
- **不含 markdown 强调符**：报告里为排版插进去的 `**` 必须剥掉——2026-10-13 实测，
  35 号 §13.5 的 `provides the **design solution**` 正是因此假未命中（正本无 `**`）。
- 只读库内正本三份：42010:2022 / 42020:2019 / 15288:2023（英文单行本用于精确串核）。

用法：python .work-ch13/verify_quotes13.py
"""
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                    '00-系统工程相关研究报告')
SRC = {
    '42010': os.path.join(ROOT, 'ISO_IEC_IEEE 42010 2023.md'),
    '42020': os.path.join(ROOT, 'ISO-IEC-IEEE 42020 2019.md'),
    '15288': os.path.join(ROOT, 'ISO IEC IEEE 15288 2023.md'),
}

# (正本, 声称条款, 特征串, 用途·落点)
CASES = [
    # —— 定性：四个东西分开（13.2 词条底座）——
    ('42010', '§3.3', 'work product used to express an *architecture* (3.2)', 'AD＝工作产品 → 13.2'),
    ('42010', '§3.7', 'comprising portion of an *architecture description* (3.3)', '视图＝信息部件 → 13.2'),
    ('42010', '§3.8', 'set of conventions for the creation, interpretation and use', '视角＝一组惯例 → 13.2'),
    ('42010', '§3.8 注2', 'frame of reference for the concerns', '视角是关切参照系（正本注2） → 13.2'),
    ('42010', '§3.8 注3', 'conventions of an architecture viewpoint are documented in a *specification* (3.16)',
     '惯例记载在规格里 → 13.2／T-152 户列依据'),
    ('42010', '§3.14', 'separately identifiable body of information that is produced, stored, and delivered for human and machine use',
     '信息部件定义 → 13.2'),
    ('42010', '§3.15', 'category of model distinguished by its key characteristics and modelling conventions',
     '模型种类定义 → 13.2／T-155'),
    ('42010', '§3.19 注1', 'a legend is an informal documentation of conventions', '图例＝非正式记录 → 13.2／T-154'),
    # —— 视图≠图（13.2 的承重论证）——
    ('42010', '§6.8 注2', 'does not prescribe the level of formality of view components', '不规定形式化程度 → 13.2'),
    ('42010', '§6.8 注2', 'non-model-based view components can also be used effectively',
     '非模型组件也能有效 → 13.2'),
    ('42010', '§5.2.8 EXAMPLE 2', 'The flow diagrams are model-based while the narrative is not',
     '叙述可作组件 → 13.2'),
    ('42010', '§3.19 EXAMPLE', 'can be used in several views of an *architecture description* (3.3)',
     '视图组件可跨视图复用 → 13.2'),
    # —— 视角是可以先订的合同（本章最反直觉的一句）——
    ('42010', '§6.6 注3', 'contract between architect and other stakeholders', '视角是合同 → 13.2'),
    ('42010', '§6.6 注3', 'can be made before any detailed architecting is undertaken', '合同可以先订 → 13.2'),
    # —— 有账可查：§6.6~§6.10 逐条 shall ——
    ('42010', '§6.6', 'An AD shall include or reference each architecture viewpoint used therein', '视角侧 shall 1'),
    ('42010', '§6.6', 'Each concern identified in accordance with 6.4 shall be framed by at least one architecture viewpoint',
     '每条关切被至少一个视角框定 → 13.4.3 + 四件账①'),
    ('42010', '§6.6', 'shall be associated with the architecture viewpoints which cover that perspective',
     '利益相关方角度须与视角关联 → 13.4.3'),
    ('42010', '§6.7', 'An AD shall include one or more architecture views for each architecture viewpoint used',
     '每个视角至少一张视图 → 13.4.3 + 四件账②'),
    ('42010', '§6.7', 'shall adhere to the conventions of its governing architecture viewpoint',
     '视图须遵循视角约定（37 号 §8.3 引） → 13.4.3'),
    ('42010', '§6.7', 'Each architecture view shall include version identification', '视图须有版本标识 → 13.4.4'),
    ('42010', '§6.7 d)', 'the recording of any known issues within a view with respect to its governing architecture',
     '已知问题须记 → 13.4.4 + 四件账④'),
    ('42010', '§6.8', 'Each view component shall identify its governing model kind, if any',
     '组件须标明模型种类 → 13.2'),
    ('42010', '§6.9.2', 'An AD shall include or reference a list of AD element correspondences',
     '对应关系清单 → 13.4.3 + 四件账③'),
    ('42010', '§6.9.3 注1', 'an AD shall record whether the method holds (is satisfied) or otherwise record all known violations',
     '对应方法须记成立／违反 → 13.4.3（★ 该 shall 在 NOTE 1 内，**不是正文段落**——引时须标"注 1"）'),
    ('42010', '§6.9.1', 'Consistency within an architecture description', '一致性节题 → 13.4.3'),
    # —— 标准不给固定清单（13.3.1 三处自我限制）——
    ('42010', '§6.6 注1', 'does not require the use of any particular architecture viewpoints', '自我限制一 → 13.3.1'),
    ('42010', '§8.1 注2', 'does not require any particular specifications of architecture viewpoints',
     '自我限制二 → 13.3.1'),
    ('42020', '§E.4.2.1', 'Some commonly used views', '自我限制三：是"常用"、且 42020 §E 是资料性 → 13.3.1'),
    # —— 七类视图定义句（13.3.2）——
    ('42020', '§E.4.2.2', 'contextual', '语境视图 → 13.3.2'),
    ('42020', '§E.4.2.3', 'main ideas or concepts', '概念视图 → 13.3.2'),
    ('42020', '§E.4.2.4', 'abstracted inputs are transformed into outputs', '功能视图 → 13.3.2'),
    ('42020', '§E.4.2.4 注', 'not a 42010 normative requirement', '功能视图非规范要求（引用警戒③） → 13.3.2'),
    ('42020', '§E.4.2.5', 'users rather than implementation', '逻辑视图 → 13.3.2'),
    ('42020', '§E.4.2.5 注', 'often somewhat subjective', '逻辑/物理之分主观（引用警戒②） → 13.3.2'),
    ('42020', '§E.4.2.6', 'provides the design solution for a product, service or enterprise',
     '物理视图＝设计解（引用警戒①·★ 须加限定注） → 13.3.2'),
    ('42020', '§E.4.2.7', 'implementable through technologies', '技术视图 → 13.3.2'),
    ('42020', '§E.4.2.8', 'responsibilities and authorities', '组织视图 → 13.3.2'),
    # —— 视角规格（13.4.1 / 13.5）——
    ('42010', '§8.1', 'The specification of an architecture viewpoint shall include or reference',
     '规格七项 shall 起句 → 13.4.1／13.5'),
    ('42010', '§8.1 a)', 'any stakeholder perspectives associated with this viewpoint', 'a) 相关方角度'),
    ('42010', '§8.1 b)', 'one or more concerns (per 6.4) framed by this architecture viewpoint', 'b) 框定的关切'),
    ('42010', '§8.1 c)', 'one or more aspects related to those concerns (per 6.5)', 'c) 方面体 ← 旧料"六项"漏掉的一项'),
    ('42010', '§8.1 d)', 'known typical stakeholders', 'd) 典型相关方'),
    ('42010', '§8.1 e)', 'model kinds (per 8.2) and legends for use when constructing views', 'e) 模型种类与图例'),
    ('42010', '§8.1 f)', 'correspondence methods capturing relations within resulting views and their view components (per 6.8)',
     'f) 对应方法'),
    ('42010', '§8.1 g)', 'references to any sources of information about this viewpoint', 'g) 信息来源'),
    ('42010', '§8.1 第二段（should）', 'A specification of an architecture viewpoint should identify view methods',
     '★ 视图方法是 **should、且在 §8.1 内**——**不是 §8.3 的 shall** → 13.4.1'),
    ('42010', '§8.2', 'Specification of a model kind', '模型种类规格节 → 13.4.1'),
    ('42010', '§8.3', 'View methods', '视图方法节题 → 13.4.1'),
    # —— 四步第一步的两个产出（★ 旧料整块缺）——
    ('42020', '§10.4.3 d)', 'd) Capture rationale for selection of framework(s), viewpoints, templates, metamodels and model kinds.',
     '★ 定型步含"选择理据"（V-O8 出处）——**旧料整块缺** → 13.4.1／13.5'),
    ('42020', '§10.4.3 e)', 'e) Define purpose and scope of each model and view to be developed.',
     '★ 定型步含"用途范围"（V-O9 出处）——**旧料整块缺** → 13.4.1／13.5'),
    ('42020', '§10.4.3 a)', 'a) Select, adapt or develop viewpoints and model kinds based on stakeholder concerns.',
     '★ 定型步第一动作（选/改/开发） → 13.4.1'),
    # —— 四步第二步（分配到实体与关系上）；§10.4.4 共十三项 a)~m) ——
    ('42020', '§10.4.4 e)', 'e) Allocate relevant concepts, properties, characteristics, behaviors, functions, features or constraints',
     '把内容分配到实体与关系上 → 13.4.2（**注意**：分配到"实体与关系"，不是 15288 §3.13 的系统元素）'),
    ('42020', '§10.4.4 f)', 'f) Identify relevant principles and precepts that will guide evolution of the architecture entity.',
     '识别管演化的原则 → 13.4.2'),
    ('42020', '§10.4.4 a)', 'a) For each viewpoint, define the architectural context and boundaries in terms of interfaces',
     '建模第一动作：定上下文与边界 → 13.4.2'),
    ('42020', '§10.4.4 j)', 'j) Harmonize the architecture models and views with each other.', '模型与视图相互调和 → 13.4.3'),
    ('42020', '§10.4.4 k)', 'k) Generate or modify the architecture description based on relevant models and views.',
     '★ 由模型与视图产出 AD → 13.4.4（成件）'),
    # —— §5.6 四句（对齐的理由）——
    ('42020', '§5.6', 'maximum flexibility in the design tradespace', '§5.6 四句之一 → 13.4.3'),
    # === V-I（输入账·13.5.1）：35 号 §13.3 十项逐项回正本 ===
    ('42010', '§6.3', 'An AD shall identify stakeholder perspectives considered relevant',
     'V-I1 相关方角度侧 → 13.5.1'),
    ('42010', '§6.4', 'An AD shall identify the concerns considered relevant to the architecture',
     'V-I1 关切清单 → 13.5.1'),
    ('42010', '§6.4 注3', 'Concerns expressed as interrogative questions', '关切写成问句更好沟通 → 13.2（视角"框定"的机理·可作白话桥）'),
    ('42010', '§6.4 注1', 'the association of concerns with stakeholders is many-to-many',
     '★ V-I2"多对多"的真正出处（**35 号原引 §6.4 NOTE 1 与 §6.2 NOTE 1——§6.2 无 NOTE 1**） → 13.5.1'),
    ('42010', '§6.1', 'An AD shall identify the entity of interest and the expected environment',
     'V-I3 实体与环境 → 13.5.1'),
    ('42010', '§6.1', 'An AD shall include a statement of its intended purpose', 'V-I3 预期用途 → 13.5.1'),
    ('42010', '§6.1 EXAMPLE', 'Date of issue and status; authors, reviewers, approving authority',
     'V-I3 辅助信息（标识信息） → 13.5.1'),
    ('42020', '§10.4.1 a)', 'Identify the intended users of the architecture description', 'V-I3 用者 → 13.5.1'),
    ('42020', '§10.4.1 b)', 'Identify the question(s) to be addressed', 'V-I9 要答哪些问 → 13.5.1'),
    ('42020', '§10.4.3 b)', 'Identify expected users of architecture elaboration information', '★ V-I9 的正本出处 → 13.5.1'),
    ('42020', '§10.4.3 a)', 'Select, adapt or develop viewpoints and model kinds based on stakeholder concerns.',
     'V-I5 可复用视角与模型种类 → 13.5.1'),
    ('42020', '§10.4.3 c)', 'Establish or identify potential architecture framework(s)', 'V-I6 ADF 与元模型 → 13.5.1'),
    ('42020', '§10.4.3 f)', 'Select, modify or develop supporting modeling methods and tools.', 'V-I7 模板与工具 → 13.5.1'),
    ('42020', '§10.4.3 g)', 'Select, develop or modify architecture frameworks, modeling templates and metamodels',
     'V-I7 模板与元模型 → 13.5.1'),
    ('42020', '§10.4.3 h)', 'Select, modify or develop relevant metamodel specifications and templates.',
     'V-I7 元模型规范 → 13.5.1'),
    ('42020', '§10.4.4 b)', 'identify the kinds of entities and their relationships to be modeled',
     'V-I8 待建模的实体与关系种类 → 13.5.1'),
    ('42010', '§6.2', 'shall include a statement of known resource limitations or other constraints',
     '★ 十一项自检第 11 条的正本出处（**35 号原引 §6.2 shall，对；但 V-I10"前轮遗留项 §6.2"缺具体条款**） → 13.5.3'),
    ('42010', '§6.2', 'Non-conformances shall be identified and explained with rationales',
     '★ 未处理项声明＝**未回应者／资源限制／不符合项及理据**（35 号 §十三 未收；O10 的正本依据） → 13.5.2'),
    # === V-O（输出账·13.5.2）：35 号 §13.4 十二项逐项回正本 ===
    ('42010', '§8.1', 'The specification of an architecture viewpoint shall include or reference', 'V-O1 视角规格 → 13.5.2'),
    ('42010', '§8.2', 'Specification of a model kind', 'V-O2 模型种类规格 → 13.5.2'),
    ('42010', '§6.7', 'An AD shall include one or more architecture views', 'V-O3 架构视图 → 13.5.2'),
    ('42010', '§6.7 a)', 'identification', 'V-O3 a) 标识与辅助信息 → 13.5.2'),
    ('42010', '§6.8', 'Each view component shall include version identification', 'V-O4 视图组件含版本 → 13.5.2'),
    ('42010', '§6.9.2', 'a list of AD element correspondences', 'V-O5 对应关系清单 → 13.5.2'),
    ('42010', '§6.9.3', 'a list of correspondence methods applying to itself', 'V-O6 对应方法清单 → 13.5.2'),
    ('42010', '§6.9.1', 'Consistency within an architecture description', 'V-O7 一致性分析 → 13.5.2'),
    ('42020', '§10.4.3 d)', 'Capture rationale for selection', 'V-O8 选择理据 → 13.5.2'),
    ('42020', '§10.4.3 e)', 'Define purpose and scope', 'V-O9 用途范围 → 13.5.2'),
    ('42010', '§6.7 d)', 'known issues within a view', 'V-O10 视图内已知问题 → 13.5.2'),
    ('42010', '§6.7 EXAMPLE 2', 'EXAMPLE 2', 'V-O11 AD 内非视图信息（EXAMPLE 2 的座标） → 13.5.2／13.2 末节'),
    ('42020', '§8.4.10', '8.4.10', 'V-O12 交付与使用记录 → 13.5.2'),
    ('42020', '§10.5', 'The following work products shall be produced', '★ §10 那一节的工作产品总账（本章只用到 §10.5） → 13.5.2'),
]


def load(p):
    with open(p, encoding='utf-8') as f:
        return f.read().split('\n')


def section_of(lines, idx):
    for i in range(idx, -1, -1):
        m = re.match(r'^#{3,5} (.+)$', lines[i])
        if m:
            return m.group(1)
    return '?'


def main():
    data = {k: load(v) for k, v in SRC.items()}
    hit = miss = 0
    print('=== 第13章 引文回正本核（量具 verify_quotes13.py） ===')
    print('口径：英文特征串 · 大小写敏感纯子串 · 三份库内英文正本 · 剥 markdown 强调符')
    print()
    for std, clause, needle, use in CASES:
        where = [i for i, ln in enumerate(data[std], 1) if needle in ln]
        if where:
            hit += 1
            sec = section_of(data[std], where[0] - 1)
            print('[HIT ] %-6s %-22s L%-6s %-46s %s'
                  % (std, clause, ','.join(map(str, where)), sec[:46], use))
        else:
            miss += 1
            print('[MISS] %-6s %-22s %-7s %s' % (std, clause, '', use))
            print('        特征串：%s' % needle)
    print()
    print('命中 %d／共 %d，未命中 %d' % (hit, len(CASES), miss))
    print('★ 未命中者不得写成"标准说……"，降为二手派生表述（手册 §1.4.1 核法第 3 条）。')


if __name__ == '__main__':
    main()
