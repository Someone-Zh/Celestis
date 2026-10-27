## 执行前必须遵守

> 本小节是旧版本迁移规则的唯一来源；其他技能只引用，不复制迁移清单。

### 1. 阅读顺序（所有 AI 必须遵守）
1. `.spec/spec.md`：项目地图、功能索引、使用协议。
2. `.spec/rules.md`：工程约束。
3. `.spec/{domain}/domain.spec.md`：领域边界、共享模型、feature 清单。
4. `.spec/{domain}/{feature}/feature.spec.md`：该功能的当前事实。
5. 需要精确契约时才读 `feature.api.md`；需要深水区时才读 `feature.{主题}.md`。
6. **永不读 `.archive/**`**，除非用户明确要求审计历史。

### 2. 不变量
- `feature.spec.md` 是当前事实：只写当前最终结论，就地更新，不追加历史，不使用 `-------------`。
- `feature.{主题}.md` 是当前设计的细节主题，不是历史；同样就地更新。
- `design.md` / `changes/` / `fix.md` 是临时工作产物，apply/fix 结束时归档。
- `.archive/{version}/` 是只读历史，写入后不修改。
- 跨文件引用只指向 `spec.md`、`domain.spec.md`、`feature.spec.md`；`feature.spec.md` 可以引用自己的 `feature.api.md` 和主题文件。
- 代码是行为事实，spec 是意图；两者冲突时以代码为准，并更新 spec。
- `dist/spec-docs/` 是生成物，只读，不提交。

### 3. 旧版本兼容与自动迁移
发现旧结构时，先迁移再执行。迁移原则：**只改名、补元数据、修链接、搬历史；不删除、不改写业务内容**。

| 旧结构 | 新结构 | 处理 |
| :--- | :--- | :--- |
| `feature.spec.api.md` | `feature.api.md` | 重命名并更新所有引用；两者都存在时保留 `feature.api.md`，旧文件移入 `.archive/legacy-{日期}/` |
| 领域目录下的 `spec.md` | `domain.spec.md` | 重命名并更新引用 |
| 功能目录下的 `spec.md` | `feature.spec.md` | 重命名并更新引用；根 `.spec/spec.md` 不动 |
| `domain.spec.md` / `spec.md` 中的 `features/...` 链接 | 相对链接 | 去掉不存在的 `features/` 层 |
| 跨文件链接指向 `feature.api.md` / 主题文件 / `.archive` | 只链 `feature.spec.md` | 改写为 `feature.spec.md`；archive 链接只保留在变更历史并标注“历史快照” |
| `feature.spec.md` 无 frontmatter | 最小 frontmatter | 补 `spec: feature` / `id` / `domain` / `version` / `updated` / `code` |
| `spec.md` / `domain.spec.md` 无 frontmatter | 最小 frontmatter | 补 `spec` / `id` / `version` / `updated` |
| `feature.api.md` 无 frontmatter | 最小 frontmatter | 补 `spec: api` / `id` / `version` / `updated` |
| `feature.api.md` 内容过薄（只有示例） | 按新模板补齐 | 补功能说明、通用约定、错误码、典型调用；缺什么补什么，不虚构 |
| 主题文件无 frontmatter | 最小 frontmatter | 补 `id` / `parent` / `version` / `updated` |
| 旧 `status: draft` / `stable` | 删除 | 默认视为可用；`deprecated` 保留 |
| 旧 `audience: external` / `internal` | 删除 | 对外/内部改由父功能卡 §4 的“（内部）”链接标记决定 |
| 标题无 `[对外]` / `[内部]` | 有标记 | 按默认映射补齐：0/1/2/4/7 对外，3/5/6 内部 |
| `feature.spec.md` 含 `-------------` 历史段 | 当前事实 + archive | 历史段移入 `.archive/legacy-{日期}/history-from-feature-spec.md`，正文只留当前结论，变更历史加一行说明 |
| `feature.spec.md` 过大且 §4 含多个独立主题 | 功能卡 + 主题文件 | 不自动拆分；标记并在迁移报告中建议拆分 |
| `feature.spec.md` 缺 §0/§3/§4/§6（有接口时加 §2） | 按新模板补齐 | 补缺失章节；缺什么补什么，不虚构 |
| `feature.api.md` 过大（>300 行） | 按资源拆分 | 拆为 `feature.api.{资源}.md`，`feature.api.md` 保留索引；不丢内容 |
| 旧主题文件 `feature.{旧名}.md` | `feature.{主题}.md` | 保留内容；名称过于笼统时按主题重命名，否则保留原名；重命名时同步更新 `feature.spec.md` §4 的链接；含内部细节的标“（内部）” |
| feature 目录缺少 `feature.spec.md` | 最小骨架 | 从旧 `design.md` 和现有代码生成 frontmatter + §0/§3/§6 骨架；默认不写 `status`，标记待补充 |
| domain 目录缺少 `domain.spec.md` | 最小骨架 | 生成 frontmatter + 边界/共享模型/feature 索引占位；不虚构 |
| `spec.md` / `domain.spec.md` 有重复索引 | 单一索引 | 合并为一张表，保留全部信息 |
| `spec.md` / `domain.spec.md` 索引含状态列 | 按新模板重建 | 去掉状态列；已弃用的 feature 在名称后标注“（已弃用）” |
| `domain.spec.md` 缺少边界/公共规则 | 按新模板补齐 | 补负责/不负责、共享模型、公共规则、feature 索引；不虚构 |
| feature 根目录有 `design.md` / `changes/` / `fix.md` | `.archive/{version}/` | **提示用户归档**；用户同意后按归档流程移动，不自动删除 |
| `.archive` 被当前文档引用 | 仅变更历史可引用 | 其他位置改写为 `feature.spec.md`，或删除链接 |

迁移完成后输出一份简短报告：改了哪些文件、补了哪些元数据、哪些需要人工确认。

### 4. 迁移执行细则
1. **命名**：`feature.spec.api.md` → `feature.api.md`，并更新 `feature.spec.md`、`domain.spec.md`、`spec.md` 中的链接。两者都存在时，保留 `feature.api.md`，旧文件移入 `.archive/legacy-{日期}/`。
2. **frontmatter**：
   - `spec: feature`：固定值。
   - `id`：由目录推导为 `{domain}.{feature}`。
   - `domain`：由目录推导。
   - `version`：优先取旧标题下的版本/日期行、变更记录或 `design.md` 中的版本；旧式 `V1` 归一为 `1.0.0`；没有则用 `1.0.0`（内容完整且无 `design.md` / `changes`）或 `0.1.0`（仍有 `design.md` / `changes` 或内容不完整）。
   - `status`：删除旧 `draft` / `stable`；保留 `deprecated`。默认不写 `status`，表示可用。
   - `audience`：删除；对外/内部由父功能卡 §4 的“（内部）”链接标记决定。
   - `updated`：当天日期。
   - `code`：从旧“代码位置”“实现原理”等章节提取目录/文件；提取不到就留空，不虚构。
   - `feature.api.md` 与主题文件同样补最小 frontmatter：api 用 `spec: api/id/version/updated`，主题用 `id/parent/version/updated`。
3. **标题标记**：按默认映射给 §0-§7 补 `[对外]` / `[内部]`；没有编号的标题按关键词判断：概述/接口/设计/限制 → 对外，代码位置/验收/变更 → 内部。
4. **历史搬迁**：把 `-------------` 之后的内容、旧的“变更记录/历史版本”段落移入 `.archive/legacy-{日期}/history-from-feature-spec.md`；正文删除这些段落，只在 §6 加一行“legacy 历史快照”说明。不要改写历史内容。
5. **链接修正**：按 `base.md` §8“引用与索引规则”修正链接；删除不存在的 `features/` 层；`.archive` 链接只保留在 §6 并标注“历史快照”。
6. **索引合并**：`spec.md` 只保留一张领域/feature 表；合并时保留所有行和最新版本/信息。
7. **不自动做的事**：不自动拆分巨型 §4；不自动归档 `design.md` / `changes/` / `fix.md`；不自动改写业务规则。把这些问题写进迁移报告，等待用户确认。
8. **章节映射**：旧标题按内容映射到新编号：功能业务概述 → §0，对外接口与规范 → §2，最新实现原理与代码位置 → §3，当前功能详细设计逻辑 → §4，核心验收标准 → §5；补 §6 变更历史、§7 已知限制。无法映射的内容保留并标记“待整理”。

归档细则见 `.spec/spec.md` §8；`apply` / `fix` 技能内也包含完整归档流程。
