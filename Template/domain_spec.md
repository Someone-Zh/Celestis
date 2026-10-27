---
spec: domain
id: {{domain}}
version: {{版本}}
updated: {{YYYY-MM-DD}}
---

# {{Domain名称}} 领域规范

> 本文件是领域字典：边界、共享模型、公共规则和 feature 清单。
> 不要在这里重复全局 `spec.md` / `rules.md` 的内容，也不要展开单个 feature 的细节。
> 版本规则见 `.spec/spec.md` §0 的“版本规则速查”；本文件内容变化时同步 frontmatter 的 `version` / `updated`。

## 1. 领域边界
- **负责**：{{该领域负责的核心能力}}
- **不负责**：{{明确排除的能力，避免职责漂移}}
- **上游/下游**：{{依赖谁、被谁依赖}}

## 2. 共享模型与实体
| 实体描述 | 代码位置 | 核心表结构/缓存关联说明 |
| :--- | :--- | :--- |
| {{核心通用模型}} | `{{项目根路径的相对文件路径}}` | {{结构说明}} |

## 3. 领域公共依赖
- **内部领域依赖 (Domains)**：{{依赖领域的规范路径，如项目根路径 `.spec/{{依赖Domain}}/domain.spec.md`}}
- **三方外部服务 (Services)**：{{依赖的外部服务/三方 API 全路径或供应商描述}}

## 4. 领域公共规则与约束
> 本领域下所有 feature 必须无条件遵守的通用规则。

- {{架构规则、安全要求或通用开发规约 1}}
- {{架构规则、安全要求或通用开发规约 2}}

## 5. 下属特性索引
> 只链接 `feature.spec.md`；不要链接 `feature.api.md`、主题文件或 `.archive`。
> 链接相对于本文件（`domain.spec.md`）。

| Feature ID | 名称 | 版本 | 一句话说明 | 特性规范 |
| :--- | :--- | :--- | :--- | :--- |
| `{{domain.feature1}}` | `{{Feature1}}` | 1.0.0 | {{该功能做什么}} | [feature.spec.md]({{Feature1}}/feature.spec.md) |
| `{{domain.feature2}}` | `{{Feature2}}` | 0.1.0 | {{该功能做什么}} | [feature.spec.md]({{Feature2}}/feature.spec.md) |

> 默认不单列状态；已弃用的 feature 在名称后加“（已弃用）”，并在其 `feature.spec.md` frontmatter 写 `status: deprecated`。

## 6. 领域公共契约（可选）
- **公共错误码**：{{错误码与含义}}
- **公共鉴权/权限**：{{鉴权方式、角色模型}}
- **公共事件/消息**：{{领域内统一的事件或 Topic}}
