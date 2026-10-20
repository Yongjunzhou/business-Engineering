---
name: meta-pipeline-rename-2026-10-20
description: 元流水线目录与内部前缀 pl4pleos → pl4pl（2026-10-20），名字表达"开发流水线的流水线"
metadata:
  type: project
---

**2026-10-20 用户定并执行。** 元流水线的目录名与内部前缀由 `pl4pleos` 改为 `pl4pl`。

## 为什么

原名 `pl4pleos` = Pipeline for (Pipeline of EOS)，把元流水线的身份绑死在"造 EOS 流水线"上；其本职是**开发流水线的流水线**，EOS 流水线只是当前第一个产出实例。改名后三层链读作：

```
pl4pl ──开发──→ pl4eos ──使用──→ eos
```

## 映射

| 旧 | 新 |
|---|---|
| `20-eos-engineering/10-pl4pleos/` | `20-eos-engineering/10-pl4pl/` |
| `00-pl4pleos-spec/`、`01/02/03/04/06-pl4pleos-spec-*`、`06-pl4pleos-glossary.md` | `00-pl4pl-spec/`、`NN-pl4pl-spec-*`、`06-pl4pl-glossary.md` |
| `10/20/30/40-pl4pleos-subpd-*` | `10/20/30/40-pl4pl-subpd-*` |
| `80-pl4pleos-2-pl4eosdata/` | `80-pl4pl-2-pl4eosdata/` |

`2-pl4eosdata` 不动——元流水线的输出产品仍是 pl4eos，`2` 表示产出流向。

## 范围与不改

- **活引用全改**：根 `CLAUDE.md`、`README.md`、`AGENTS.md`、`20-eos-engineering/CLAUDE.md`、`00-generalspec/README.md`、`20-pl4eos`／`30-eos` 规范与 README、`10-pl4pl` 内全部文档、`90-治理登记/01-例外与治理机构登记.md`、相关记忆。目录与文件名用 `git mv`，正文用批量替换。
- **不改**（历史事实快照）：`chain-layer-name-rename-2026-08-28`、`directory-restructure-direction`、`pending-subpd-subpl-naming`、`project-directory-migration-2026-10-19`、`skill-guide-renaming-2026-09-15`、`90-治理登记/06-根规范术语改名-逐文件计划差异`。

## 关联

- [[two-tier-isomorphic-structure]]
- [[meta-pipeline-spec-downgrade-plan]]
