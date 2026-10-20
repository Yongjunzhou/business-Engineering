---
name: two-tier-isomorphic-structure
description: 20-eos-engineering/10-pl4pl/ 和 20-eos-engineering/20-pl4eos/ 目录结构同构，均含 00-spec/10-subpd-sysdev/20-subpd-comdev/30-subpd-sysint/40-subpd-sysops/80-X-2-Ydata
metadata:
  type: project
---

# 两层目录结构同构化

**日期**：2026-06-02
**2026-10-20**：元流水线的目录与内部前缀由 `pl4pleos` 改名为 `pl4pl`（见 [[meta-pipeline-rename-2026-10-20]]）。

## 结构

```
20-eos-engineering/10-pl4pl/（元流水线, A1）        20-eos-engineering/20-pl4eos/（EOS 流水线, A2）
00-pl4pl-spec/                  00-pl4eos-spec/
10-pl4pl-subpd-sysdev/          10-pl4eos-subpd-sysdev/
20-pl4pl-subpd-comdev/          20-pl4eos-subpd-comdev/
30-pl4pl-subpd-sysint/          30-pl4eos-subpd-sysint/
40-pl4pl-subpd-sysops/          40-pl4eos-subpd-sysops/
50-* (A2 特有：bizcfg)            50-pl4eos-subpd-bizcfg/
80-pl4pl-2-pl4eosdata/          80-pl4eos-2-eosdata/
```

## 命名规律

`{层级号}-{产品前缀}-subpd-{子线名称}`

- `pl4pl` = Pipeline for Pipelines（元流水线；原 `pl4pleos`，2026-10-20 改名）
- `pl4eos` = Pipeline for EOS（EOS 流水线）

## 清理操作

- 移除了 `20-eos-engineering/10-pl4pl/10-pl4eos-sysdev/`（内容重复，移入 90-hold/）
- 移除了 `20-eos-engineering/20-pl4eos/10-eos-sysdev/`（内容重复，移入 90-hold/）
- 统一命名：`pl4eos`/`pl4pleos` 前缀对齐（后者于 2026-10-20 改名 `pl4pl`）

## 产品链关系

A1（元流水线, 流水线类×AI SKILL）→ A2（EOS 流水线, 流水线类×AI SKILL）→ A3（EOS, 非流水线类×软件产品）→ B（输出产品）

## 相关记忆

- [[delivery-framework-two-types]]
