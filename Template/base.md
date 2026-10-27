## 通用约束

> 本节是全局不变量的唯一来源；其他文件只引用，不复制规则。

### 1. 文件与命名
- 唯一契约文件名：`feature.api.md`；禁止再使用 `feature.spec.api.md`。
- 接口过多时按资源拆为 `feature.api.{资源}.md`，由 `feature.api.md` 保留索引与链接。
- 唯一对外引用单元：`feature.spec.md`。
- 主题文件：`feature.{主题}.md`，一个文件只讲一个主题，例如 `feature.login-lockout.md`。
- 临时文件：`design.md`、`changes/`、`fix.md`，归档后不得残留。
- 生成物：`dist/spec-docs/`，只读，不提交。

### 2. frontmatter 最小字段
- `spec.md`：`spec: project`、`id`、`version`、`updated`。
- `domain.spec.md`：`spec: domain`、`id`、`version`、`updated`。
- `feature.spec.md`：`spec: feature`、`id`、`domain`、`version`、`updated`、`code`；`status` 可选，仅用于 `deprecated`，缺省表示可用。
- `feature.api.md`：`spec: api`、`id`、`version`、`updated`；拆分的 `feature.api.{资源}.md` 沿用同一组字段。
- 主题文件：`id`、`parent`、`version`、`updated`。
- `code` 只写范围（目录或文件）；精确符号写在 `feature.spec.md` §3 代码地图中。
- `feature.api.md` 只放需要被下游调用的对外契约；纯内部契约放主题文件或代码注释。

### 3. 对外 / 内部标记
- `feature.spec.md` 的标题使用 `[对外]` 或 `[内部]` 标记。
- 默认映射：§0/§1/§2/§4/§7 为对外；§3/§5/§6 为内部。
- 对外章节不得出现内部文件路径、类名、表名、测试路径；这些内容放 §3 或父功能卡 §4 中标“（内部）”的主题文件。
- 主题文件的对外/内部由父功能卡 §4 的链接标记决定：标“（内部）”的不导出；未标可导出。
- 导出流程、默认包、链接清理和排除项见 `.spec/spec.md` §8；本文件只定义标记规则。

### 4. 历史规则
- `feature.spec.md` 和主题文件只保留当前事实，就地更新；禁止追加历史段落，禁止使用 `-------------`。
- 变更历史只在 `feature.spec.md` §6 保留索引：每版本一行（版本 / 日期 / 摘要 / 归档路径，标注“历史快照”）。
- 设计过程、备选方案、历史任务放 `.archive/{version}/`；写入后不再修改。
- 同一版本内的 `design.md` 可以继续追加；一旦归档，后续改动必须产生新版本。

### 5. 版本规则
- feature：新功能设计阶段 `0.1.0`；首次完整实现 `1.0.0`；行为变更 minor；修复 patch；设计文档指定版本优先；归档目录冲突 patch+1。
- domain：新建 `1.0.0`；新增 feature 用 minor；修正用 patch。
- `feature.api.md`、拆分文件和主题文件跟随 feature 版本。
- 内容变化刷新 `feature.spec.md` 的 `updated`；`spec.md` 索引变化刷新其 `updated`；`domain.spec.md` 内容变化刷新其 `version` / `updated`。
- 默认不写 `status`；只有弃用时写 `status: deprecated`。

### 6. 代码锚点
- 语法：`相对路径#符号`，可选 `相对路径#符号:行号`。
- 符号指函数、方法、类、导出的常量/组件；不是哈希，不是 commit。
- 重名或重载使用 `#Class.method`；仍不唯一时再加 `:行号`。
- 行号只是跳转提示，行号变化不算漂移；符号不存在或改名才算漂移。
- 路由写在 `feature.api.md`；代码地图用 handler 符号定位。
- `feature.spec.md` §3 代码地图是符号锚点的唯一事实源。

### 7. 内容归属
| 信息 | 唯一归属 |
| :--- | :--- |
| 项目技术栈、目录、模块职责、数据流 | `spec.md` |
| 领域边界、共享实体、领域公共规则 | `domain.spec.md` |
| 功能行为、边界、业务规则、设计结论、验收 | `feature.spec.md` |
| 对外 API 契约（协议、入参、出参、错误码，只放需要被下游调用的） | `feature.api.md` |
| 算法、状态机、时序、错误模型等细节 | `feature.{主题}.md` |
| 设计过程、历史任务 | `.archive/{version}/` |

### 8. 引用与索引规则
- `spec.md` §6 是唯一项目索引；`domain.spec.md` §5 是领域 feature 索引。
- `spec.md` 索引可链接 `domain.spec.md` 和 `feature.spec.md`。
- `domain.spec.md` 索引只链接 `feature.spec.md`。
- 其他跨文件引用只链接 `feature.spec.md`；不得链接 `feature.api.md`、主题文件或 `.archive`。
- `feature.spec.md` 可以链接自己的 `feature.api.md` 和主题文件。
- `feature.api.md` 可以链接回自己的 `feature.spec.md`。
- 所有链接使用相对路径，必须能从所在文件解析。
- 新功能、摘要/版本变化或弃用标记变化时更新索引；同步 `domain.spec.md` 的 `version` / `updated` 和 `spec.md` 的 `updated`。
- 已弃用的 feature 在名称后标注“（已弃用）”，不单列状态列。

### 9. 禁止行为
- 不得虚构不存在的接口、参数、错误码或代码位置。
- 不得把历史设计写回 `feature.spec.md`。
- 不得让当前文档链接 `.archive`（变更历史中的“历史快照”除外）。
- 不得手工修改 `dist/spec-docs/`。
