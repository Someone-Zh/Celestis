---
name: "{{@skills.create.name}}"
description: 用于创建新的功能需求设计方案，从用户意图到完整设计文档的规划工具。当用户提到"创建需求"、"新建功能"、"规划需求"、"设计新功能"、"create requirement"、"需求设计"、"功能规划"、"新需求"时自主唤醒。适用于从零开始规划功能的场景，核心职责包括需求收集、架构探索、设计文档编写、规范文件补齐与验收标准制定。
version: "{{@skills.create.version}}"
triggers:
  - type: command
    name: create
globs:
  - ".spec/**/*"
disable-model-invocation: false
user-invocable: true
argument-hint: "{{@skills.create.argument_hint}}"
compatibility: "{{@skills.create.compatibility}}"
---
@Template/file_spec.md

@Template/base_root.md

@Template/base.md

## 1. 前置与兼容
- 如果 `.spec/spec.md` 或 `.spec/rules.md` 不存在，停止并提示用户先执行 `init`。
- 先按本文档中的“旧版本兼容与自动迁移”小节执行迁移；本文件不重复迁移规则。
- 本技能额外检查：
  - 目标领域/功能目录是否有不属于本次的 `design.md` / `changes/` / `fix.md`；有则提示用户先归档或确认继续。
  - `feature.spec.md` / `feature.api.md` 是否存在；`create` 负责补齐。

## 2. 从输入信息中分析领域与功能
- 如果输入是标准需求目录 `.spec/{{领域}}/{{功能}}/design.md`，直接提取需求内容和初步设计。
- 如果输入不完整（只有领域或功能目录），根据已有信息追问。
- 如果输入是设计方案（文件或直接提供），自动划分或新建到相应领域与功能；允许同时操作多个领域/功能。
- 如果完全没有上下文，必须进一步提问。
- **只有完整获取领域、功能、设计三要素后，才允许执行后续流程。**

## 3. 索引校验与补齐
- 在 `.spec/spec.md` §6 的唯一索引表中查找领域与功能。
- 不存在则新增；存在则校验 Feature ID、版本和路径是否准确。
- 在 `.spec/{{领域}}/domain.spec.md` §5 的 feature 索引中同步新增或修正。
- 索引规则按本文档中的“引用与索引规则”。

## 4. 创建或补齐规范文件
- 确保功能目录存在。
- **`design.md`**：写入本次设计的完整方案，必须做到仅凭它就能完成开发。
- **`changes/tasks.md`**：按附录模板生成原子任务清单，任务可关联 AC-ID。
- **`feature.spec.md`**：
  - 不存在则按附录模板创建，写入当前已知的 §0 摘要、§2 API 摘要（有对外接口时）、§3 代码地图（规划）、§4 设计结论、§5 验收标准、§6 变更历史首行；默认不写 `status`。
  - 已存在则只更新当前事实相关章节；**禁止追加历史段**，禁止使用 `-------------`。
- **`feature.api.md`**：
  - 有对外接口则创建或更新；不存在对外接口则不创建。
  - 文件名只能是 `feature.api.md`；如果发现 `feature.spec.api.md`，按兼容规则重命名。
  - 内容只写怎么调用：协议、入参、出参、错误码、示例；不写内部实现。
- **`feature.{主题}.md`**：
  - 仅当某个设计主题独立且复杂时创建；一个文件只讲一个主题。
  - 在 `feature.spec.md` §4 中链接，并注明“何时读”；含内部实现细节时，在链接旁标“（内部）”。
- **`domain.spec.md`**：
  - 不存在则按附录模板创建；已存在则补齐边界、共享模型、公共规则和 feature 索引。
- **`spec.md`**：
  - 更新 §6 唯一索引表；不要创建第二张领域表。
  - 索引变化时同步 `spec.md` frontmatter 的 `updated`；项目 `version` 由发布流程维护。

## 5. 版本与 ID 规则
- 版本规则按本文档中的“版本规则”；`create` 额外：
  - 新功能设计阶段用 `0.1.0`；首次完整实现由 `apply` 升为 `1.0.0`。
  - 新建 `domain.spec.md` 用 `1.0.0`。
  - 版本号写入 `design.md`、`feature.spec.md`、`feature.api.md`、拆分文件和主题文件（如有）的 frontmatter，以及 `feature.spec.md` §6 首行。
- 必须分配稳定 ID：
  - Feature ID：`{{domain}}.{{feature}}`
  - API ID：`API-{{FEATURE}}-001`、`API-{{FEATURE}}-002`……
  - AC ID：`AC-{{FEATURE}}-001`、`AC-{{FEATURE}}-002`……
  - 规则 ID：`R-001`、`R-002`……

## 6. 设计工作流（核心）

### 必须遵守
1. **前置查阅**：读取所属领域 `domain.spec.md`，了解现有边界、共享模型和公共规则。
2. **充分收集**：收集准确文档、代码位置、现有业务逻辑，确保设计可落地。
3. **意图探索**：在正式实施前，深入探索真实意图、潜在需求和架构取舍。
4. **单点提问**：每次只提 1-3 个问题；宁可多轮沟通，不要一次压给用户。
5. **疑必确问**：任何模糊点必须确认后再写设计。
6. **选项优先**：优先多项选择题，降低沟通成本。
7. **渐进式验证**：展示设计 → 获得授权 → 继续推进。
8. **极简主义**：删除非必要、冗余的“镀金”功能。
9. **明确指标**：每个功能点都要有可验证的验收标准（AC-ID）。
10. **原子拆解**：任务拆到 2-5 分钟可完成/验证，写入 `changes/tasks.md`。
11. **外部变更记录**：涉及外部依赖或配置变更时，在 `changes/` 生成对应文件（如 SQL、配置样例）。
12. **只做设计**：本阶段只写设计文档和规范文件，不修改业务代码。
13. **规范约束**：设计必须满足 `.spec/spec.md` 和所属 `domain.spec.md` 的约束。

### 询问规范
- 不询问设计中已有答案的问题。
- 必须确认：未明确的技术选型、架构差异、需求盲区、隐藏的重构/破坏性变更、安全隐私、性能取舍、模糊数据结构。

### 核心理念
- **严禁盲目猜测**：显式陈述假设；有多种方案时列出对比；有更简单方案要主动提出；不合理需求要敢于 push back。
- **克制改动**：不重构没坏的代码；保持现有代码风格；只清理因本次改动产生的孤立残留。
- **可验证性**：把任务转化为可验证目标，定义成功指标。
- **内容归属**：功能行为写 `feature.spec.md`；精确契约写 `feature.api.md`；算法/状态机/时序写主题文件；设计过程写 `design.md`。

## 7. 产物交付
- `design.md`：本次完整设计，临时文件，`apply` 结束后归档。
- `changes/tasks.md`：原子任务清单。
- `feature.spec.md`：当前事实的功能卡；默认不写 `status`，只有弃用时写 `status: deprecated`。
- `feature.api.md`：有接口时的对外契约。
- `feature.{主题}.md`：按需的主题文件。
- `domain.spec.md`：领域字典与 feature 索引。
- `spec.md`：唯一项目索引。
- 后续对话继续迭代 `design.md`，保持设计先行；实现阶段再按 `apply` 收尾。
- 完成后输出：本次新增/修改的文件、版本号、下一步执行 `apply` 的路径。

## 8. 大文件拆分原则
- `feature.spec.md` 目标不超过约 180 行；某节超过约 15 行、含独立状态机/时序/多张表，或每次都被迫读它时，拆到 `feature.{主题}.md`。
- `feature.api.md` 目标不超过约 300 行；接口过多时按资源拆为 `feature.api.{资源}.md`，并在 `feature.api.md` 中保留索引与链接。
- 主题文件继续过大时，按子主题继续拆分；每个文件只讲一个主题。
- 拆分后必须在 `feature.spec.md` §4 或 `feature.api.md` 索引中保留入口和“何时读”。
- 含内部实现细节的主题链接标“（内部）”，导出时会被移除。

## 附录

### `changes/tasks.md`
````markdown
@Template/task.md
````

### `.spec/{{领域}}/domain.spec.md`
````markdown
@Template/domain_spec.md
````

### `.spec/{{领域}}/{{功能}}/feature.spec.md`
````markdown
@Template/feature_spec.md
````

### `.spec/{{领域}}/{{功能}}/feature.api.md`
````markdown
@Template/feature_api_spec.md
````

### `.spec/{{领域}}/{{功能}}/feature.{{主题}}.md`（可选）
````markdown
@Template/feature_topic_spec.md
````
