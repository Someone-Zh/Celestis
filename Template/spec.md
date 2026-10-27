---
spec: project
id: {{项目标识}}
version: {{项目版本}}
updated: {{YYYY-MM-DD}}
---

# 项目规范（唯一入口）

> 本文件是项目唯一入口：项目地图 + 功能索引 + AI 使用协议。
> 只在这里维护索引；领域和功能的细节在各自文件中。
> 索引变化时更新 frontmatter 的 `updated`；项目 `version` 由发布流程维护。

## 0. 使用协议（给所有 AI）

### 阅读顺序
1. 本文件：项目地图、领域/功能索引、维护入口。
2. `.spec/rules.md`：技术栈、命名、安全、配置位置。
3. `.spec/{domain}/domain.spec.md`：领域边界、共享模型、feature 清单。
4. `.spec/{domain}/{feature}/feature.spec.md`：该功能的当前事实。
5. 需要精确契约时才读 `feature.api.md`；需要深水区时才读 `feature.{主题}.md`。
6. **永不读 `.archive/**`**，除非用户明确要求审计历史。

### 不变量
- `feature.spec.md` 是当前事实：只写当前最终结论，就地更新，不追加历史。
- `feature.{主题}.md` 是当前设计的细节主题，不是历史。
- `design.md` / `changes/` / `fix.md` 是临时工作产物，apply/fix 结束时归档。
- 只有 `feature.spec.md` 是跨 feature 的引用单元。
- 代码是行为事实，spec 是意图；冲突以代码为准，并更新 spec。
- `dist/spec-docs/` 是生成物，只读，不提交。

### 版本规则速查
- feature：设计阶段 `0.1.0`；首次完整实现 `1.0.0`；行为变更 minor；修复 patch；设计文档指定版本优先；归档冲突 patch+1。
- domain：新建 `1.0.0`；新增 feature minor；修正 patch。
- `feature.api.md` / 拆分文件 / 主题文件跟随 feature 版本。
- 内容变化刷新 `updated`；`spec.md` 索引变化刷新其 `updated`。
- 默认不写 `status`；只有弃用写 `status: deprecated`。

### 引用与索引规则速查
- `spec.md` §6 是唯一项目索引；`domain.spec.md` §5 是领域 feature 索引。
- `spec.md` 索引可链接 `domain.spec.md` 和 `feature.spec.md`。
- `domain.spec.md` 索引只链接 `feature.spec.md`。
- 其他跨文件引用只链接 `feature.spec.md`；不得链接 `feature.api.md`、主题文件或 `.archive`。
- `feature.spec.md` 可以链接自己的 `feature.api.md` 和主题文件；`feature.api.md` 可以链接回自己的 `feature.spec.md`。
- 新功能、摘要/版本变化或弃用标记变化时更新；同步 domain 的 `version` / `updated` 和 `spec.md` 的 `updated`。
- 已弃用的 feature 在名称后标注“（已弃用）”。

### 维护入口
| 场景 | 入口 | 说明 |
| :--- | :--- | :--- |
| 初始化 / 旧规范迁移 | `init` | 扫描项目，生成或修正 `spec.md` / `rules.md`，并迁移旧结构 |
| 新功能 / 大改 | `create` → `apply` | create 出设计与任务；apply 实现并收尾 |
| 小修 / Bug 修复 | `fix` | 轻量通道，允许先改代码后补规范 |
| 归档 | apply/fix 结束自动；也可说“归档 {feature}” | 幂等，可补归档 |
| 对外文档 | 说“生成对外文档” | 输出到 `dist/spec-docs/`，一次性生成，不提交 |
| 漂移审计 | 说“检查 {feature} 漂移” | 按需审计，不强制门禁 |

## 1. 整体目录结构
> 本节由初始化脚手架扫描生成；调整核心骨架时必须同步更新。

```text
{{项目/服务根目录}}/
├── .spec/                          # 规范根目录
├── {{核心源代码目录}}/               # 业务代码主目录
│   ├── {{全局共享/公共模块}}/         # 共享工具、常量、异常定义
│   └── {{领域/业务模块}}/             # 业务核心实现
└── {{配置及部署目录}}/               # 配置文件、脚本、Dockerfile 等
```

## 2. 模块职责矩阵
| 模块/目录路径 | 核心职责 | 允许引入的依赖 | 严禁包含的内容 |
| :--- | :--- | :--- | :--- |
| `{{模块路径1}}` | `{{核心职责描述}}` | `{{允许依赖的库/模块}}` | `{{反模式/禁带内容}}` |
| `{{模块路径2}}` | `{{核心职责描述}}` | `{{允许依赖的库/模块}}` | `{{反模式/禁带内容}}` |

## 3. 核心要素速查表
| 分类 | 关键要素描述 | 物理路径/位置 | 备注/负责人 |
| :--- | :--- | :--- | :--- |
| **服务入口** | {{应用启动类、Main 函数、CLI 入口}} | `{{具体文件路径}}` | |
| **对外 API** | {{HTTP Router、RPC 服务定义、GraphQL Schema}} | `{{具体文件/目录路径}}` | |
| **配置文件** | {{环境配置、应用参数、日志配置}} | `{{具体文件路径}}` | |
| **三方集成** | {{消息队列监听器、定时任务、第三方 SDK 初始化}} | `{{具体文件/目录路径}}` | |
| {{其他重要功能}} | {{功能描述}} | {{功能所在位置}} | {{备注/负责人}} |

## 4. 标准数据流向
```mermaid
graph TD
{{    Client[用户/客户端请求] --> Controller[Controller/Entry 层: 入口校验与路由]
    Controller --> Service[Service/Domain 层: 核心业务逻辑]
    Service --> Infra[Infra/Repository 层: 基础设施与持久化]
    Infra --> DB[(数据库/外部存储)]

    DB -.->|Return Entity| Infra
    Infra -.->|Return DTO/Model| Service
    Service -.->|Return VO/Result| Controller
    Controller -.->|HTTP/RPC Response| Client
    }}
```
> **流向约束**：
> 1. {{例：禁止从 Controller 层直接绕过 Service 层调用 Infra 层。}}
> 2. {{例：Entity 严禁穿透到 Controller 层，必须在 Service 层完成向 VO/DTO 的转换。}}

## 5. 模块依赖拓扑
- **{{上层依赖下层}}**：`{{模块A}}` -> `{{模块B}}` -> `{{模块C}}`
- **{{单向依赖原则}}**：严禁在 `{{模块X}}` 与 `{{模块Y}}` 之间引入循环依赖。
- **{{三方依赖合规}}**：所有新增三方依赖必须在 `.spec/rules.md` 中报备。
- **{{模块依赖原则}}**：{{具体规则}}

## 6. 业务领域与特性索引
> 本表是项目唯一的领域/功能索引；不要在其他文件维护重复索引。
> `spec.md` 索引可链接 `domain.spec.md` 和 `feature.spec.md`；不要链接 `feature.api.md`、主题文件或 `.archive`。
> 链接相对于本文件（`.spec/spec.md`）。

| 业务领域 (Domain) | 领域规范 | 特性 (Feature) | Feature ID | 版本 | 特性规范 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `{{DomainName1}}` | [domain.spec.md]({{DomainName1}}/domain.spec.md) | `{{Feature1}}` | `{{domain.feature1}}` | 1.0.0 | [feature.spec.md]({{DomainName1}}/{{Feature1}}/feature.spec.md) |
| `{{DomainName2}}` | [domain.spec.md]({{DomainName2}}/domain.spec.md) | `{{Feature2}}` | `{{domain.feature2}}` | 0.1.0 | [feature.spec.md]({{DomainName2}}/{{Feature2}}/feature.spec.md) |

> 默认不单列状态；已弃用的 feature 在名称后加“（已弃用）”，并在其 `feature.spec.md` frontmatter 写 `status: deprecated`。

## 7. 文档分层与生成物
| 层 | 文件 | 主要读者 | 说明 |
| :--- | :--- | :--- | :--- |
| 入口 | `spec.md` | 所有人 / AI | 项目地图、索引、使用协议 |
| 规则 | `rules.md` | 执行者 | 技术栈、命名、安全、配置位置 |
| 领域 | `domain.spec.md` | 进入领域时 | 边界、共享模型、公共规则、feature 清单 |
| 功能卡 | `feature.spec.md` | 维护者 / AI | 当前完整设计的结论层 |
| 契约 | `feature.api.md` | 下游 / 联调 | 怎么调用：协议、入参、出参、错误码 |
| 深水区 | `feature.{主题}.md` | 维护者 | 算法、状态机、时序等细节 |
| 历史 | `.archive/{version}/` | 审计 | 只追加，不修改 |
| 对外生成物 | `dist/spec-docs/` | 下游 / 下游 AI | 由 `.spec` 生成，只读，不提交 |

## 8. 维护流程

> 以下流程由模板提供，其他文件只引用，不复制步骤。

@Template/archive.md

@Template/export.md

@Template/drift.md
