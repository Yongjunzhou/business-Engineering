# 元流水线
**Meta-Pipeline — Pipeline for Pipelines**

**文档版本**：v3.0
**最后更新**：2026-10-20

---

## 产品定位

元流水线是**开发流水线的流水线**：以通用系统设计方法论为方法来源，产出流水线类产品。当前输出产品是 **EOS 流水线（pl4eos）**——由元流水线设计出 EOS 流水线，再由 EOS 流水线设计 EOS 本体。

```
pl4pl ──开发──→ pl4eos ──使用──→ eos
```

---

## 目录结构

```
10-pl4pl/
├── 00-pl4pl-spec/                      # 设计描述文档
│   ├── 01-pl4pl-spec-sysdev.md         #   系统设计规范
│   ├── 02-pl4pl-spec-comdev.md         #   构件开发规范（待编写）
│   ├── 03-pl4pl-spec-sysint.md         #   集成交付规范（待编写）
│   ├── 04-pl4pl-spec-sysops.md         #   系统运维规范（待编写）
│   └── 06-pl4pl-glossary.md            #   术语对照
├── 10-pl4pl-subpd-sysdev/              # 系统设计子线
│   ├── 00-presysdev-4-pl4eos/         #   OR 预处理
│   ├── 10-wfsysdev-4-pl4eos/          #   瀑布（6 任务）
│   ├── 20-resysdev-4-pl4eos/          #   逆向工程（8 任务）
│   ├── 30-agsysdev-4-pl4eos/          #   敏捷（8 任务）
│   ├── 40-opsysdev-4-pl4eos/          #   DevOps（4 任务）
│   └── README.md
├── 20-pl4pl-subpd-comdev/              # 构件开发子线（待扩展）
├── 30-pl4pl-subpd-sysint/              # 集成交付子线（待扩展）
├── 40-pl4pl-subpd-sysops/              # 系统运维子线（待扩展）
└── 80-pl4pl-2-pl4eosdata/              # 运行数据—元流水线到 pl4eos 的产品数据
```

---

## 各子目录说明

| 目录 | 内容 | 状态 |
|------|------|------|
| `00-pl4pl-spec/` | 元流水线的设计描述：系统设计规范（精简版）、构件开发／集成／运维规范、术语对照 | 系统设计规范已写；02~04 待编写 |
| `10-pl4pl-subpd-sysdev/` | 系统设计子线——为 pl4eos 做系统设计的操作规程：预处理 ＋ 瀑布／逆向／敏捷／DevOps 四模式任务 | 已建齐 |
| `20-pl4pl-subpd-comdev/` | 构件开发子线 | 待扩展 |
| `30-pl4pl-subpd-sysint/` | 集成交付子线 | 待扩展 |
| `40-pl4pl-subpd-sysops/` | 系统运维子线 | 待扩展 |
| `80-pl4pl-2-pl4eosdata/` | 输出产品（pl4eos）的产品数据槽位与输入登记 | 暂无正式产品数据 |

---

## 相关文档

- [元流水线系统设计规范](00-pl4pl-spec/01-pl4pl-spec-sysdev.md)
- [系统设计子线操作规程](10-pl4pl-subpd-sysdev/README.md)
- [产品数据槽位说明](80-pl4pl-2-pl4eosdata/README.md)
