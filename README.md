# Celestis

> 纯文本规范体系：让任意 AI 助手读懂项目、改动代码、留下可追溯的设计。

Celestis 不是 CLI，也不是需要安装的工具链。它由一组 Markdown 技能、模板和目录约定组成。把项目的 `.spec` 目录交给任意 AI 助手，它就能按 `spec.md` 的协议完成查找、设计、实现、归档和对外文档生成。

---

## 1. 设计目标

- **单一事实源**：`.spec` 是项目文档的唯一来源，代码位置、业务规则、接口契约、设计结论都从这里查。
- **当前事实与历史分离**：`feature.spec.md` 只写“现在是什么”，`.archive` 保存“当时为什么这样设计”。
- **分层加载**：先读小索引，再按需加载领域、功能卡、契约、主题细节，避免一次读完整仓库。
- **对外/内部分离**：开发信息（代码地图、验收标准、变更历史）留在内部；对外只暴露调用契约和必要的设计说明。
- **旧版本可迁移**：技能启动时能识别旧目录、旧文件名、旧章节，并自动迁移到新结构。
- **零工具依赖**：不新增命令、不依赖脚本、不依赖 CI；任何支持 Markdown 的 AI 助手都能使用。

---

## 2. 核心原则

1. `.spec` 是唯一事实源。
2. `feature.spec.md` 是当前事实：只写当前最终结论，就地更新，不追加历史，不使用 `-------------`。
3. `feature.{主题}.md` 是当前设计的细节主题，不是历史；同样就地更新。
4. `design.md` / `changes/` / `fix.md` 是临时工作产物，`apply` / `fix` 结束时归档。
5. `.archive/{version}/` 是只读历史，写入后不修改。
6. 跨文件引用只指向 `spec.md`、`domain.spec.md`、`feature.spec.md`；`feature.spec.md` 可以引用自己的 `feature.api.md` 和主题文件。
7. 代码是行为事实，spec 是意图；两者冲突时以代码为准，并更新 spec。
8. `dist/spec-docs/` 是生成物，只读，不提交。
9. 默认不写 `status`；只有弃用才写 `status: deprecated`。
10. 不预标 `audience`；主题是否对外由父功能卡 §4 的“（内部）”链接标记决定。

---

## 3. 目录结构

### 3.1 项目内的 `.spec`

```text
.spec/
├── spec.md                         # 唯一入口：项目地图 + 索引 + AI 使用协议
├── rules.md                        # 工程约束
└── {domain}/
    ├── domain.spec.md              # 领域字典：边界、共享模型、feature 清单
    └── {feature}/
        ├── feature.spec.md         # 必填：当前完整设计的结论层
        ├── feature.api.md          # 有对外接口则必填：对外契约
        ├── feature.api.{资源}.md   # 可选：接口过多时按资源拆分
        ├── feature.{主题}.md       # 可选：当前设计的细节主题
        ├── design.md               # 临时：本次设计（归档前）
        ├── changes/                # 临时：任务与变更（归档前）
        │   ├── tasks.md
        │   └── ...
        └── .archive/               # 历史：只追加，不修改
            └── {version}/
                ├── manifest.md     # 归档记录（纯 Markdown）
                ├── design.md       # 历史设计过程
                ├── changes/
                │   ├── tasks.md
                │   └── ...
                └── fix.md          # 历史修复记录（如有）
```

### 3.2 对外生成物

```text
dist/spec-docs/                     # 一次性生成；不提交、不手工修改
├── README.md                       # 下游阅读顺序
├── llms.txt                        # AI 入口
├── api-index.md                    # 所有 API 总表
├── feature-index.md                # 所有功能总表
└── {domain}/{feature}/
    ├── feature.api.md
    ├── feature.api.{资源}.md       # 可选：API 拆分文件
    ├── feature.spec.md             # 可选：过滤后的对外版
    └── feature.{对外主题}.md       # 可选：父功能卡 §4 未标“（内部）”的主题
```

### 3.3 本仓库

```text
.
├── README.md                       # 本文件：Celestis 的设计说明（不参与技能渲染）
├── render.py                       # 将 @Template 占位符渲染为 skills/{name}/SKILL.md
├── init.md                         # init 技能源文件
├── create.md                       # create 技能源文件
├── apply.md                        # apply 技能源文件
├── fix.md                          # fix 技能源文件
├── Template/                       # 技能共享模板
│   ├── base.md
│   ├── base_root.md
│   ├── file_spec.md
│   ├── spec.md
│   ├── rules.md
│   ├── domain_spec.md
│   ├── feature_spec.md
│   ├── feature_api_spec.md
│   ├── feature_topic_spec.md
│   ├── archive.md
│   ├── export.md
│   ├── drift.md
│   ├── vars.json
│   └── task.md
└── skills/                         # 渲染产物，不手工编辑
    ├── init/SKILL.md
    ├── create/SKILL.md
    ├── apply/SKILL.md
    └── fix/SKILL.md
```

---

## 4. 文件职责

| 文件 | 角色 | 主要读者 | 是否必填 | 是否含历史 |
| :--- | :--- | :--- | :--- | :--- |
| `spec.md` | 项目地图 + 领域/功能索引 + AI 使用协议 | 所有人 / AI 第一站 | 是 | 否 |
| `rules.md` | 技术栈、命名、安全、配置位置 | 执行者 | 是 | 否 |
| `domain.spec.md` | 领域边界、共享模型、公共规则、feature 清单 | 进入领域时 | 是 | 否 |
| `feature.spec.md` | 当前完整设计的结论层 | 维护者 / AI | 是 | 否（只有变更索引） |
| `feature.api.md` | 对外契约：协议、入参、出参、错误码 | 下游 / 联调 | 有对外接口则必填 | 否 |
| `feature.api.{资源}.md` | API 按资源拆分文件 | 下游 / 联调 | 接口过多时 | 否 |
| `feature.{主题}.md` | 某个独立主题的当前细节 | 维护者 | 否 | 否 |
| `design.md` | 本次设计的完整过程与取舍 | 实施者 | apply 前需要 | 是（归档后） |
| `changes/` | 任务清单与外部变更记录 | 实施者 | apply 前需要 | 是（归档后） |
| `fix.md` | 本次修复的意图与影响范围 | 修复者 | 否（推荐） | 是（归档后） |
| `.archive/{version}/` | 历史设计、任务、修复记录 | 审计 | 自动产生 | 是（只读） |
| `dist/spec-docs/` | 对外文档投影 | 下游 / 下游 AI | 按需生成 | 否 |

---

## 5. AI 阅读协议

所有技能和任意 AI 助手都按同一顺序加载：

1. `.spec/spec.md`：项目地图、索引、使用协议。
2. `.spec/rules.md`：技术栈、命名、安全、配置位置。
3. `.spec/{domain}/domain.spec.md`：领域边界、共享模型、feature 清单。
4. `.spec/{domain}/{feature}/feature.spec.md`：该功能的当前事实。
5. 需要精确契约时才读 `feature.api.md`；需要深水区时才读 `feature.{主题}.md`。
6. **永不读 `.archive/**`**，除非用户明确要求审计历史。

这样做的目的：把 AI 的上下文预算花在“当前要改的功能”上，而不是一次性加载整个项目。

---

## 6. 内容分层与信息归属

| 信息 | 唯一归属 |
| :--- | :--- |
| 项目技术栈、目录、模块职责、数据流 | `spec.md` |
| 领域边界、共享实体、领域公共规则 | `domain.spec.md` |
| 功能行为、边界、业务规则、设计结论、验收 | `feature.spec.md` |
| 精确 API 契约（协议、入参、出参、错误码） | `feature.api.md` |
| 算法、状态机、时序、错误模型等细节 | `feature.{主题}.md` |
| 设计过程、备选方案、历史任务 | `.archive/{version}/` |

### 结论层与细节层

- `feature.spec.md` 是**结论层**：只读它，仍能回答“这个功能做什么、边界在哪、代码大概在哪、怎么验收”。
- 主题文件是**细节层**：只有需要状态机、时序、算法等深水区时才加载。
- 两者都是**当前设计**；历史过程只进 `.archive`。

---

## 7. `feature.spec.md` 的结构

保留 0-7 编号，但区分必填与可选，并设置内容上限，避免功能卡变成设计文档全集。

| 节 | 内容 | 标记 | 必填 | 上限 |
| :--- | :--- | :--- | :--- | :--- |
| 0 | 摘要与边界：做什么 / 不做什么 / 适用场景 | 对外 | 是 | 5 行 |
| 1 | 业务规则：只写代码里看不出来的规则 | 对外 | 否 | 10 条 |
| 2 | 对外接口摘要：API-ID 表 + 契约链接 | 对外 | 有对外接口则必填 | 10 行 |
| 3 | 代码地图：`路径#符号`，锚点唯一事实源 | 内部 | 是 | 8 行 |
| 4 | 设计结论：当前为什么这样设计 | 对外 | 是 | 15 行 + 主题链接 |
| 5 | 验收标准：外部可观察的 AC，关联测试 | 内部 | 否 | 10 条 |
| 6 | 变更历史：版本 / 日期 / 摘要 / 归档 | 内部 | 是 | 每版 1 行 |
| 7 | 已知限制 / 未覆盖 | 对外 | 否 | 5 条 |

### 写作规则

- **只写当前事实**：行为变化时就地重写相关章节，不追加“本次修正”段落。
- **不写历史过程**：备选方案、推演、历史任务进 `.archive/{version}/design.md`。
- **代码优先**：`feature.spec.md` 不是代码的镜像；它记录意图、边界、入口和契约。
- **超过约 180 行就拆**：某节超过约 15 行、含独立状态机/时序/多张表，或 AI 每次都被迫读它时，拆到 `feature.{主题}.md`。

---

## 8. 对外 / 内部标记

`feature.spec.md` 的标题使用 `[对外]` 或 `[内部]` 标记：

```markdown
## 0. 摘要与边界 [对外]
## 3. 代码地图 [内部]
## 4. 设计结论 [对外]
## 5. 验收标准 [内部]
## 6. 变更历史 [内部]
```

默认映射：

- 对外：§0、§1、§2、§4、§7
- 内部：§3、§5、§6

主题文件不再预标 `audience`；是否对外由父功能卡 §4 的链接标记决定：

- 链接旁标“（内部）” → 不导出；
- 未标 → 可导出。

对外章节不得出现内部文件路径、类名、表名、测试路径。需要写这些内容时，放 §3 或标“（内部）”的主题文件。

---

## 9. 主题文件 `feature.{主题}.md`

### 什么时候拆

满足任意一条即可拆：

1. `feature.spec.md` 的某一节超过约 15 行；
2. 该主题有独立的状态机、时序图、算法或多张表；
3. 该主题有多个边界条件，AI 每次读功能卡都被迫读它；
4. 该主题可以独立变化，且变化时不需要动功能卡其他部分。

### 命名

按主题命名，一个文件只讲一个主题：

- `feature.login-lockout.md`
- `feature.token-refresh.md`
- `feature.error-model.md`
- `feature.permission-matrix.md`

### 格式

```markdown
---
id: auth.login.lockout
parent: auth.login
version: 1.3.0
updated: 2026-10-20
---

# 登录 · 锁定策略（当前设计）

## 1. 结论
- 连续失败 5 次锁定 15 分钟；成功登录清零。

## 2. 详细设计
- 状态机、时序、边界条件、异常处理。

## 3. 与 API 的关系
- 对应错误码：423。

## 4. 何时读
- 修改锁定阈值或排查锁定时读。
```

主题文件是**当前细节**，不是历史；不写版本演进，不追加 `-------------`。父功能卡必须在 §4 里链接它，并注明“何时读”；含内部实现细节时标“（内部）”，导出时该链接会被移除。

---

## 10. 代码锚点

### 语法

```text
相对路径#符号
相对路径#符号:行号     # 行号可选，只是跳转提示
```

示例：

```text
src/api/auth/login.controller.ts#login
src/auth/login.service.ts#authenticate
src/auth/login.service.ts#lockAccount
src/auth/user.repo.ts#findByEmail
```

### 规则

- **符号**指函数、方法、类、导出的常量/组件；不是哈希，不是 commit。
- 重名或重载使用 `#Class.method`；仍不唯一时再加 `:行号`。
- 行号只是提示，行号变化不算漂移；符号不存在或改名才算。
- 路由写在 `feature.api.md`；代码地图用 handler 符号定位。
- `feature.spec.md` §3 代码地图是符号锚点的唯一事实源。
- frontmatter 的 `code` 只写范围目录/文件，不重复符号：

```yaml
code:
  - src/auth/login/
  - src/api/auth/login.controller.ts
```

不做 hash 指纹，不做 commit 绑定。用 `updated` 日期 + 符号存在性做按需审计即可。

---

## 11. 生命周期

> 详细规则由模板提供；本节只描述角色、顺序和前置条件。

### 11.1 `init`：初始化与迁移

- 执行 `Template/base_root.md` 的迁移；迁移规则只有这一份。
- 生成或修正 `.spec/rules.md` 和 `.spec/spec.md`；索引从文件系统实际目录生成。
- 为已存在的 domain / feature 目录补最小骨架。
- 输出迁移报告，列出自动修改项和待人工确认项。

### 11.2 `create`：设计与补齐规范

- 前置：`.spec/spec.md` 和 `.spec/rules.md` 必须存在；先执行 `base_root` 迁移。
- 明确领域、功能、设计三要素；创建 `design.md` 和 `changes/tasks.md`。
- 补齐 `feature.spec.md`、`feature.api.md`（有对外接口时）、主题文件、`domain.spec.md`、`spec.md` 索引。
- 分配稳定 ID：Feature ID、API-ID、AC-ID、规则 ID。
- 版本规则见 `.spec/spec.md` §0（完整规则见 `Template/base.md` §5）；`create` 额外：新功能 `0.1.0`，新 domain `1.0.0`。
- 只做设计，不改业务代码。

### 11.3 `apply`：实现与收尾

- 前置：`design.md`、`changes/tasks.md`、`domain.spec.md`、`feature.spec.md` 必须存在；涉及对外接口时 `feature.api.md` 必须存在。缺失时停止并提示 `create` / `init`。
- 按 TDD 实现，原子任务推进，维护任务状态。
- 收尾更新 `feature.spec.md`、`feature.api.md`、主题文件、索引和 frontmatter。
- 版本规则见 `.spec/spec.md` §0（完整规则见 `Template/base.md` §5）；首次完整实现为 `1.0.0`。
- 按 `Template/archive.md` 归档；未完成、测试未通过不得归档。

### 11.4 `fix`：轻量通道

- 适用于 Bug 修复、小范围行为调整、文案/校验/日志小修，以及“先改代码、最后补规范”。
- 前置：`domain.spec.md` 和 `feature.spec.md` 必须存在。
- 超过阈值时转 `create + apply`：新增功能/对外接口、修改对外契约、数据表/缓存/配置结构变更、超过 5 个文件或跨模块。
- 收尾更新 `feature.spec.md` / `feature.api.md` / 主题文件 / 索引；按 `Template/archive.md` 归档；`fix.md` 归档不删除。

### 11.5 归档 / 对外文档 / 漂移审计

- 归档：见 `Template/archive.md`。
- 对外文档：见 `Template/export.md`。
- 漂移审计：见 `Template/drift.md`。
- `.spec/spec.md` §8 通过 include 引用这三个模板，生成后的 spec.md 自带完整流程。

---

## 12. 归档模型

```text
.archive/
└── {version}/
    ├── manifest.md     # 版本、日期、触发方式、变更文件、测试结果、覆盖的 AC
    ├── design.md       # 历史设计过程
    ├── changes/        # 历史任务与变更
    └── fix.md          # 历史修复记录（如有）
```

关键原则：

- 归档是“提交”，不是“开工”；`apply` 开工时不归档。
- 归档只追加，不修改历史版本。
- 功能根目录归档后不得残留 `design.md` / `changes/` / `fix.md`。
- 当前文档不链接 `.archive`；只有 `feature.spec.md` §6 变更历史可以出现归档路径，并标注“历史快照”。

完整步骤、幂等规则和 manifest 字段见 `Template/archive.md`。

---

## 13. 对外文档

默认 API 优先：

```text
dist/spec-docs/
├── README.md
├── llms.txt
├── api-index.md
├── feature-index.md
└── {domain}/{feature}/
    ├── feature.api.md
    └── feature.api.{资源}.md
```

需要解释设计原理时，再附带：

- 过滤后的 `feature.spec.md`（只保留 `[对外]` 节）；
- 父功能卡 §4 未标“（内部）”的主题文件。

阅读路径：

```text
api-index.md
  → feature.api.md（或拆分文件）（怎么调）
    → feature.spec.md §0/§1/§4/§7（功能边界、设计原理）
      → feature.{对外主题}.md（状态机、时序、错误模型）
```

对外文档一次性生成到 `dist/spec-docs/`，不提交、不接 CI。完整步骤、索引字段和链接清理规则见 `Template/export.md`。

---

## 14. 旧版本兼容

迁移原则：**只改名、补元数据、修链接、搬历史；不删除、不改写业务内容**。

常见迁移：

| 旧结构 | 新结构 |
| :--- | :--- |
| `feature.spec.api.md` | `feature.api.md` |
| 领域/功能目录下的 `spec.md` | `domain.spec.md` / `feature.spec.md` |
| `features/...` 链接 | 相对链接 |
| 旧 `status` / `audience` 字段 | 删除；`status: deprecated` 保留 |
| 缺失 `domain.spec.md` / `feature.spec.md` | 生成最小骨架 |
| `feature.api.md` 内容过薄或过大 | 按新模板补齐或按资源拆分 |

**完整迁移规则只有一份**：`Template/base_root.md`。`init` / `create` / `apply` / `fix` 只引用它，不复制迁移清单。

---

## 15. 技能生成、变量与单一事实源

### 15.1 技能生成

- 技能源文件在仓库根目录：`init.md`、`create.md`、`apply.md`、`fix.md`。
- 共享规则在 `Template/`；技能通过 `@Template/xxx.md` 引入。
- `render.py` 将占位符替换为模板/变量内容，输出 `skills/{name}/SKILL.md`。
- 只渲染四个技能源文件；`README.md` 等其他文件跳过。
- 不要直接编辑 `skills/`；改源文件或模板后重新渲染。

```bash
python3 render.py --skill
```

### 15.2 变量渲染

变量定义在 `Template/vars.json`，使用 `{{@path.to.value}}` 引用：

```yaml
name: "{{@skills.apply.name}}"
version: "{{@skills.apply.version}}"
argument-hint: "{{@skills.apply.argument_hint}}"
```

- 变量按点号路径读取，例如 `skills.apply.name`。
- 变量缺失时渲染失败并报错，不会生成半成品。
- 适合放技能名、版本号、参数提示、兼容性等会变化的元数据。
- 不要把项目业务占位符（如 `{{Domain}}`）放进 `vars.json`；那些是生成文档时的内容占位。

### 15.3 单一事实源

| 规则 | 唯一归属 |
| :--- | :--- |
| 全局不变量、命名、frontmatter、状态、锚点、版本规则、引用与索引规则 | `Template/base.md` |
| 旧版本迁移 | `Template/base_root.md` |
| 归档流程 | `Template/archive.md` |
| 对外文档生成 | `Template/export.md` |
| 漂移审计 | `Template/drift.md` |
| 文件布局与引用规则 | `Template/file_spec.md` |
| 项目/领域/功能/API/主题格式 | 对应 `Template/*_spec.md` |
| 技能流程 | 各技能源文件 |
| 设计说明与高层视图 | `README.md` |

> 新规则只能写到唯一归属文件；其他文件只引用，不复制。否则会再次出现“改一处漏多处”。

### 15.4 渲染后检查

- `skills/*/SKILL.md` 无残留 `@Template/...` 或 `{{@...}}`；
- Markdown 代码围栏闭合；
- 表格列数一致；
- 旧文件名只出现在兼容表里；
- `README.md` 未生成技能。

---

## 16. 设计取舍

| 决策 | 原因 |
| :--- | :--- |
| 不接 OpenAPI / proto / GraphQL | 对个人项目太重；纯文本入参/出参/错误码已经够下游 AI 使用，也更好维护 |
| 不做 hash / commit 绑定 | 任何重构都会误报；符号锚点 + `updated` 日期已能覆盖常见漂移 |
| 不新增运行时 CLI / 脚本 | 学习成本和维护成本高；文本协议可被任意 AI 助手直接执行；`render.py` 仅是维护期工具 |
| 不接 CI 强制门禁 | 非高频需求；漂移审计先用按需流程，未来需要再加可选检查 |
| 对外文档不提交 | 一次性交付物，避免生成物与源文件产生第二事实源 |
| 不单独做 archive 技能 | 归档是 apply/fix 的收尾步骤 + 一个手工话术，独立技能反而增加认知负担 |
| 保留 `fix` | 小修和紧急修复需要轻量通道，否则所有改动都被迫走完整 create + apply |
| 保留 `feature.spec.md` 0-7 | 结构熟悉、稳定；通过必填/可选和上限控制复杂度 |
| 默认不写 `status` | draft 只存在于开发过程；用 `design.md` / `changes/` 的存在表示进行中；只有弃用才写 `status: deprecated` |
| 不预标 `audience` | 对外文档尚未有独立技能；生成时按 `feature.spec.md` §4 的“（内部）”链接标记决定，避免规范文件提前承担导出元数据 |

---

## 17. 使用示例

```text
初始化项目规范：
  init

为登录功能创建需求：
  create auth/login

执行登录功能设计：
  apply .spec/auth/login/design.md

快速修复登录锁定问题：
  fix auth.login 连续失败次数没有清零

补归档：
  归档 auth.login

生成对外文档：
  生成对外文档

检查文档与代码漂移：
  检查 auth.login 漂移

迁移旧规范：
  init
```

---

## 18. 心智模型

```text
spec.md          → 项目地图（去哪找）
domain.spec.md   → 领域字典（边界是什么）
feature.spec.md  → 功能卡（现在是什么、为什么）
feature.api.md   → 契约（怎么调用）
feature.{主题}.md → 深水区（细节怎么运作）
design.md        → 本次设计过程（临时）
.archive         → 历史快照（只读）
dist/spec-docs   → 对外投影（生成物）
```

一句话：

> **`.spec` 记录当前事实，`.archive` 记录历史原因；对外只发当前契约，内部保留完整脉络。**
