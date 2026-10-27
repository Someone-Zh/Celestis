### 漂移审计

> 本小节是漂移审计规则的唯一来源；其他文件只引用，不复制步骤。

1. 读 `feature.spec.md` 的 `updated` 和 §3 代码地图锚点。
2. 检查每个 `路径#符号` 是否存在；不存在即硬漂移。
3. 若有 shell，执行 `git log --since=<updated> -- <代码范围>`；有改动即软漂移。
4. 只做重构：更新代码地图，并刷新 `feature.spec.md` 的 `updated`。
5. 行为/契约变化：更新 spec/api/AC，按 `.spec/spec.md` §0 的“版本规则速查”递增，归档，并刷新 `updated`。
6. 说不清：报告用户，不自动改写；**不要刷新 `updated`**，保留待确认状态。
