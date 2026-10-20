---
name: pending-30-eos-link-fixes
description: 30-eos 待办：01 号规范 22 处链接深度多退一层、00 号 README 为旧稿；另 20-pl4eos 规范 README 是错放副本（2026-10-20 查出，未处理）
metadata:
  type: project
---

2026-10-20 清点 `30-eos/` 时查出，当日未动（用户「收工」）：

- **`20-eos-engineering/30-eos/00-eos-product-spec/01-eos-spec-sysdev.md`**：22 处 `[通用设计规范](../../../00-generalspec/01-generalspec-sysdev.md)` 深度多退一层——2026-10-19 目录下沉后未修，正确应为 `../../00-generalspec/…`；另有 1 处 `../10-pl4eos-subpd-sysdev/README.md` 指向不存在的目录（实际在 `20-pl4eos/10-pl4eos-subpd-sysdev/`）。
- **`20-eos-engineering/30-eos/00-eos-product-spec/README.md`**：旧稿——两条链接指向 `01-eos-system-design-specification.md`、`04-eos-system-design-terminology-glossary.md`（均已不存在），并引用迁移前 `00-general/…` 路径；未列出实际存在的 `10`~`15` 六份文档。
- **`20-eos-engineering/20-pl4eos/00-pl4eos-spec/README.md`**：是元流水线规范 README 的**错放副本**——内容描述 `01-pl4pl-spec-*`，而该目录实际是 `01-pl4eos-spec-sysdev.md`（2,249 行）、`05-pl4eos-spec-bizcfg.md`、`06-pl4eos-glossary.md`、`07-pl4eos-spec-sr-refactor-summary-2026-06-16.md` 等八份。

**Why**：都是 2026-10-19 目录重排前遗留的引用失效与旧稿，非 2026-10-20 改名造成。

**How to apply**：处理 `30-eos` 或 `20-pl4eos` 规范目录时一并收口——链接只改深度或指向，README 按目录实际文件重写，不动规范内容结论。相关：[[meta-pipeline-rename-2026-10-20]]、[[project-directory-migration-2026-10-19]]。
