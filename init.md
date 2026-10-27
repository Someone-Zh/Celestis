---
name: "{{@skills.init.name}}"
description: 用于初始化项目规范体系，深度扫描代码库并生成企业级规范文档。当用户提到"初始化项目"、"init project"、"生成规范"、"创建规范文档"、"项目初始化"、"建立规范体系"、"扫描项目结构"、"初始化规范"时自主唤醒。适用于新项目或未规范化项目的首次配置，核心职责包括代码库深度扫描、架构分析、规范文档生成、规则配置与旧版本规范迁移。
version: "{{@skills.init.version}}"
triggers:
  - type: command
    name: init
globs:
  - "**/*"
disable-model-invocation: false
user-invocable: true
argument-hint: "{{@skills.init.argument_hint}}"
compatibility: "{{@skills.init.compatibility}}"
---
@Template/file_spec.md

@Template/base_root.md

@Template/base.md

# 作为资深架构师，深度扫描项目并生成/修正企业级规范文件

## 1. 迁移与生成边界
- 先按本文档中的“旧版本兼容与自动迁移”小节执行迁移；本文件不复制迁移规则。
- `init` 额外负责：
  1. 生成或修正 `.spec/rules.md`。
  2. 生成或修正 `.spec/spec.md`，索引必须从文件系统实际目录生成。
  3. 为已存在的 domain / feature 目录补最小骨架（`domain.spec.md` / `feature.spec.md`）。
  4. 输出迁移报告。
- 不要虚构领域和功能业务内容；缺失文件只生成骨架并标记待补充。

## 2. 生成或修正 `.spec/rules.md`
- 如果不存在，按附录模板生成。
- 如果已存在，检查技术栈、架构模式、服务方式、涉及框架、配置管理是否与当前项目一致；缺失则补齐，过时则修正。
- 不虚构依赖或配置；无法确认时保留原内容并标注待确认。

## 3. 生成或修正 `.spec/spec.md`
- 如果不存在，按附录模板生成；如果已存在，按模板补齐结构并保留原有有效信息。
- 必须包含：
  - frontmatter：`spec: project`、`id`、`version`、`updated`。
  - §0 使用协议：阅读顺序、不变量、维护入口。
  - 项目目录结构、模块职责矩阵、核心要素速查表、数据流向、依赖拓扑。
  - **唯一的**业务领域与特性索引表；索引必须从文件系统实际目录生成，不能凭记忆。
- 索引规则按本文档中的“引用与索引规则”；索引从文件系统实际目录生成。
- 每个 feature 一行，包含 Feature ID、版本、`feature.spec.md` 路径；重复索引合并去重。
- 如果项目使用 Git，确保 `.gitignore` 包含 `dist/spec-docs/`。

## 4. domain / feature 最小骨架与校验
- domain 目录缺少 `domain.spec.md` → 生成最小骨架：frontmatter、边界/共享模型/feature 索引占位；`version` 取已有信息或 `1.0.0`；不要虚构业务内容。
- feature 目录缺少 `feature.spec.md` → 生成最小骨架：frontmatter、§0 摘要占位、§3 代码地图（从现有代码扫描）、§6 变更历史首行；`version` 取 `design.md` 或 `0.1.0`；默认不写 `status`。
- 已有 `domain.spec.md` / `feature.spec.md` / `feature.api.md` / 主题文件 → 按本文档中的“旧版本兼容与自动迁移”小节完成迁移和补齐。
- 迁移后额外检查：
  - `feature.spec.md` 仍过大（>180 行）→ 在报告中建议拆分到 `feature.{主题}.md`。
  - `feature.api.md` 超过约 300 行 → 建议按资源拆分到 `feature.api.{资源}.md`。
  - `feature.api.md` 只有请求/响应示例 → 建议按新模板补齐。

## 5. 输出迁移报告
完成后输出一份简短报告：
- 新增/修正了哪些文件。
- 重命名了哪些文件。
- 修复了哪些断链或重复索引。
- 哪些内容需要人工确认（例如待归档的 `design.md`、待拆分的巨型 `feature.spec.md`）。
- 下一步建议：执行 `create` 规划新功能，或执行 `apply` 推进已有设计。

## 附录

### `.spec/rules.md`
````markdown
@Template/rules.md
````

### `.spec/spec.md`
````markdown
@Template/spec.md
````

### `.spec/{{领域}}/domain.spec.md`
````markdown
@Template/domain_spec.md
````

### `.spec/{{领域}}/{{功能}}/feature.spec.md`
````markdown
@Template/feature_spec.md
````
