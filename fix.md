---
name: "{{@skills.fix.name}}"
description: 用于快速修正已完成功能的小问题或调整实现，基于 TDD 流程进行代码修复、规范同步与归档。当用户提到"修复bug"、"修正需求"、"fix bug"、"修复问题"、"调整实现"、"代码修复"、"缺陷修复"、"fix requirement"、"修改已完成的功能"时自主唤醒。适用于小范围、低风险的快速修正；涉及新功能、对外契约或大规模改动时应转 create + apply。
version: "{{@skills.fix.version}}"
triggers:
  - type: command
    name: fix
globs:
  - ".spec/**/*"
  - "**/fix.md"
  - "**/design.md"
disable-model-invocation: false
user-invocable: true
argument-hint: "{{@skills.fix.argument_hint}}"
compatibility: "{{@skills.fix.compatibility}}"
---
@Template/file_spec.md

@Template/base_root.md

@Template/base.md

## 1. 定位与前置校验
- 通过上下文明确修正内容及对应的 `.spec/{{领域(Domain)}}/{{功能(Feature)}}/` 目录。
- 无法精确定位时，必须向用户询问，严禁盲目执行。
- 读取 `feature.spec.md`，了解当前事实；读取 `feature.api.md`（如有），了解当前契约。
- 读取所属领域 `domain.spec.md`；不存在时停止并提示用户先执行 `init` 或 `create` 补齐。
- 如果 `feature.spec.md` 不存在，停止并提示用户先执行 `init`（迁移）或 `create`（补齐）；`fix` 不临时发明文件格式。

## 2. 旧版本兼容检查
- 先按本文档中的“旧版本兼容与自动迁移”小节执行迁移；本文件不重复迁移规则。
- 本技能额外检查：目标功能目录是否有残留的 `design.md` / `changes/`；有则提示归档或确认继续。

## 3. 适用范围与升级阈值
本技能是 **apply 的轻量通道**，适用于：
- Bug 修复；
- 小范围行为调整；
- 文案、校验、日志、配置的小修；
- 紧急问题先改代码、最后补规范。

出现以下任一情况，**停止 fix，转 create + apply**：
- 新增功能或新对外接口；
- 修改对外契约（路径、入参、出参、错误码、事件）；
- 涉及数据表结构、缓存结构、配置结构变更；
- 改动超过 5 个文件，或跨越多个模块；
- 需要多轮设计取舍才能确定方案。

## 4. 修正流水线（核心工作流）
1. **记录意图**：
   - 如果用户提供了修正描述或已有 `fix.md`，读取它。
   - 如果没有 `fix.md`，在功能目录创建一个简短的 `fix.md`，记录“修什么、为什么、影响范围”。
   - `fix.md` 是临时工作文件，结束时归档，不删除。
2. **先复现**：能写失败测试的，先写复现测试并观察失败。
3. **最小修复**：只改与修正直接相关的代码；不重构没坏的代码；保持现有风格。
4. **同步存量测试**：如果修正改变了既有行为，必须同步修改存量测试。
5. **允许先改代码、后补规范**：可以多次修改代码，但结束前必须完成下面的规范同步和归档。
6. **质量红线**：修改的代码必须有测试覆盖；编译与测试输出干净（零错误、零警告）。
7. **范围克制**：清理因本次修正产生的孤立 Import、变量、函数或类；不清理历史死代码。

## 5. 收尾：同步规范并归档
> fix 的收尾与 apply 使用同一套不变量，只是不写独立设计文档。

1. **更新 `feature.spec.md`（就地重写）**：
   - 更新受影响的 §0/§1/§2/§4/§7。
   - 更新 §3 代码地图中的 `路径#符号`。
   - 更新 §5 验收标准（如有变化）。
   - 在 §6 变更历史新增或更新一行（同一版本只保留一行）：版本 / 日期 / 摘要 / 归档路径。
   - frontmatter：按本文档中的“版本规则”patch+1，并更新 `updated` / `code`。
2. **更新 `feature.api.md`**：如果修正影响对外行为，必须同步更新协议、入参、出参、错误码或示例，以及 frontmatter 的 `version` / `updated`（含拆分文件）。
3. **更新主题文件**：如果修正涉及某个主题，就地更新对应 `feature.{{主题}}.md`，不追加历史；同步 frontmatter 的 `version` / `updated`。
4. **更新索引**：按本文档中的“引用与索引规则”更新 `domain.spec.md` / `spec.md`；只有摘要/版本/弃用标记变化时才改；版本按本文档中的“版本规则”。
5. **执行归档**：严格按下面的归档流程执行；归档只写入新版本目录，**禁止修改历史归档目录**。
6. **自检**：
   - 功能根目录没有 `fix.md`、`design.md`、`changes/`。
   - `feature.spec.md` 没有历史段和 `-------------`。
   - `feature.spec.md` / `feature.api.md` / 主题文件的版本与归档目录一致。
   - `feature.spec.md` §6 有当前版本行，归档路径指向该目录。
   - 代码地图锚点存在；API-ID 与契约文件一致。
   - 归档前 `fix.md` 记录的修复已完成，测试已通过（无测试则记录原因）；未完成不得归档。
   - 当前文档没有非变更历史位置的 `.archive` 链接。
   - 所有相对链接可解析。
   - `domain.spec.md` 和 `spec.md` 的索引与 `feature.spec.md` 一致。
   - 如果功能已弃用，`feature.spec.md` 已标 `status: deprecated`；否则不应出现 `status`。

@Template/archive.md

## 6. 大文件拆分
- 如果修正导致 `feature.spec.md` 或 `feature.api.md` 过大，按 `apply` 的拆分规则处理：拆到 `feature.{{主题}}.md` 或 `feature.api.{{资源}}.md`，并在主文件中保留入口和“何时读”。
- 拆分是当前设计的重组，不是历史归档。
- 主题文件格式：frontmatter（id / parent / version / updated）+ 结论 + 详细设计 + 与 API 的关系 + 何时读。
- 含内部实现细节时，在 `feature.spec.md` §4 的链接旁标“（内部）”。
