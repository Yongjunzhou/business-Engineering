---
name: meta-pipeline-spec-downgrade-plan
description: 元流水线规范降级为方法论说明+工程导航（已实施）；2026-10-20 删除 80-pl4pleos-2-pl4eosdata 九份空占位产品数据
metadata:
  type: project
---

# 元流水线规范降级计划

**提出日期**：2026-06-02
**状态**：已实施——`01-pl4pleos-spec-sysdev.md` 现为 239 行精简版（v1.0，2026-06-03）；2026-10-20 再删九份空占位产品数据（见文末）

## 问题

元流水线（A1）和 EOS 流水线（A2）同为"流水线类×AI SKILL"，套用同一套规范模板导致
`01-pl4pleos-spec-sysdev.md`（1178 行）实质上是 A2 规范的复制品，独立维护意义不大。

## 方案

将 `20-eos-engineering/10-pl4pleos/00-pl4pleos-spec/01-pl4pleos-spec-sysdev.md` 从"完整系统设计规范"
降级为一份简短的方法论说明 + 工程导航文档，包含：

1. 元流水线概念解释（三层构造链顶层）
2. A1→A2→A3→B 产品链关系
3. 工程阅读导航：通用规范 → A2 规范 → A3 规范
4. 当前建设状态

目录结构保留不变，但不把 A1 当作需要独立维护系统设计规范的产品。

## 2026-10-20 删空占位产品数据

用户令「删空的占位数据」。`80-pl4pleos-2-pl4eosdata/` 的九份文件（01~09）此前均为 3 行占位（"待重新生成—此前内容已过时"），已 `git rm`；目录保留，`README.md` 改为**槽位与层级说明**（九槽位名、五层图、`_inputs/` 说明），并标明当前无产品数据文件。

- **未删**：`_inputs/01-pl4eos-or-lifecycle.md`（输入登记表，真实内容）、`20-issues/ISSUE-20260529-001.md`、两个空的材料/归档子目录。
- **连带**：元流水线 sysdev 的 26 份任务仍按文件名引用九份数据（如 `01-pl4eos-original-requirements.md`）——那是**输出目标**，不是现存文件；下一次系统设计迭代按槽位生成后引用即恢复。
- **判据备忘**：本目录（元流水线）与 [[two-tier-isomorphic-structure]] 所述 `20-pl4eos` 同构，但其产品数据（EOS 流水线的设计成果）实际落在 `20-pl4eos/00-pl4eos-spec/01-pl4eos-spec-sysdev.md`，不在 `80-pl4pleos-2-pl4eosdata/`。

## 关联记忆

- [[two-tier-isomorphic-structure]]
- [[delivery-framework-two-types]]
