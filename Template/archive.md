### 归档流程（幂等，可手工补归档）

> 本小节是归档规则的唯一来源；其他文件只引用，不复制步骤。

#### 触发
- `apply` 正常结束时自动执行。
- `fix` 正常结束时自动执行。
- 用户说“归档 {feature}”时手工执行。

#### 前置条件
- 已实施完成：如果存在 `changes/tasks.md`，不能有未完成任务或失败任务；`fix` 流程以 `fix.md` 记录的修复完成和测试通过为准；有测试则运行并记录结果，无测试则记录原因。
- `feature.spec.md` 已更新为当前事实，§3 代码地图锚点存在（纯配置/文档功能记录对应文件锚点）。
- 版本号按 `.spec/spec.md` §0 的“版本规则速查”；仅当 frontmatter 缺失时：新功能 `1.0.0`；已有功能按 apply/fix 规则；没有可参照版本时用 `1.0.0`。
- **未实施、任务未完成或测试未通过时，拒绝归档并报告原因；不要用归档掩盖未完成。**

#### 步骤
1. 读取 `feature.spec.md` frontmatter 的 `version`。
2. 若 `.archive/{version}` 已存在：
   - 根目录仍有待归档文件 → 版本 patch+1 后使用新版本号；
   - 根目录已干净、`manifest.md` 存在且 §6 有当前版本行 → 直接结束（幂等），不重写；
   - 根目录已干净但 `manifest.md` 缺失 → 只补写 `manifest.md`，并确保 §6 有当前版本行后结束。
3. 确认 `feature.spec.md` §6 已有本次变更行；没有则先补。
4. 创建 `.archive/{version}/`。
5. 将存在的 `design.md`、`changes/`、`fix.md` 移入该目录；不存在的跳过；保留原内容，不删除。
6. 写入 `.archive/{version}/manifest.md`（纯 Markdown；已存在时不覆盖，只补充缺失信息）：
   - 版本、日期、触发方式（apply / fix / 手工补归档）
   - 变更文件清单
   - 测试结果
   - 覆盖的 AC
   - 关联需求或提交（可选）
7. 更新 `feature.spec.md` frontmatter 的 `version`（如版本被调整，同时更新 `updated`），同步 `feature.api.md` 及其拆分文件 / 主题文件 frontmatter 的 `version` / `updated`（如有），并更新 §6：版本 / 日期 / 摘要 / 归档路径（标注“历史快照”）。
8. 只有新功能、摘要/版本变化或弃用标记变化时，才按 `.spec/spec.md` §0 的“引用与索引规则速查”更新 `domain.spec.md` 和 `spec.md` 的索引。
9. 自检：
   - 功能根目录没有 `design.md`、`changes/`、`fix.md`
   - `.archive/{version}/manifest.md` 存在，包含版本、日期、触发方式、测试结果
   - 当前文档没有非变更历史位置的 `.archive` 链接
   - 所有相对链接可解析
   - frontmatter 的 `version` 与归档目录一致
   - `feature.spec.md` §6 有当前版本行，归档路径指向本目录

#### 中断恢复
- 已移动一部分：按 `manifest.md` 或目录内容补齐，不重复移动。
- 根目录已干净且归档完整：直接结束，不报错。
- 根目录有残留且归档已存在：视为第二批改动，版本 patch+1 后重新归档。
