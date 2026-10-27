### 对外文档生成

> 本小节是对外文档规则的唯一来源；其他文件只引用，不复制步骤。
> 一次性生成，输出到 `dist/spec-docs/`，不提交、不接 CI。

#### 默认包
- `README.md`（下游阅读顺序）
- `llms.txt`（AI 入口）
- `api-index.md`
- `feature-index.md`
- `feature.api.md`（含 `feature.api.{资源}.md` 拆分文件）

#### 需要设计原理时追加
- 过滤后的 `feature.spec.md`（只保留 `[对外]` 节）
- 父功能卡 §4 未标“（内部）”的主题文件

#### 步骤
1. 遍历 `spec.md` §6 索引中的所有 feature。
2. 对每个有 `feature.api.md` 的 feature，输出该文件及拆分文件；没有 API 文件的 feature 跳过 api 部分，只在 `feature-index.md` 登记。
3. 按需追加过滤后的 `feature.spec.md` 和未标“（内部）”的主题文件。
4. 生成 `api-index.md`、`feature-index.md`、`llms.txt`、`README.md`。
5. 排除 `design.md`、`changes/`、`fix.md`、`.archive/`、内部主题、代码地图、验收标准、变更历史。
6. 只导出 api 时，移除 `feature.api.md` 及其拆分文件中指向 `feature.spec.md` 的链接，避免断链。
7. 输出到 `dist/spec-docs/`，不提交。
8. 自检：不得有指向内部主题、未附带的 `feature.spec.md` 或 `.archive` 的链接；所有相对链接可解析。

#### 索引字段
- `api-index.md`：API-ID / Feature / 能力 / 协议-路径 / 鉴权 / 契约文件链接。
- `feature-index.md`：Feature ID / 领域 / 名称 / 版本 / 一句话说明 / 规范链接；已弃用的在名称后标注“（已弃用）”。

#### 阅读路径
```text
api-index.md
  → feature.api.md（或拆分文件）（怎么调）
    → feature.spec.md §0/§1/§4/§7（功能边界、设计原理）
      → feature.{对外主题}.md（状态机、时序、错误模型）
```
