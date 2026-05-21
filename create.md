---
description: 创建功能需求
---
@Template/file_spec.md

@Template/base_root.md

@Template/base.md

## 从给定信息中分析功能和需求信息
* 如果给定的是需求目录`.spec/{{功能}}/{{需求}}/design.md`（比如：`.spec/auth/.archive/login/design.md`）则从中直接获取需求和需求以及初步的设计需求信息
* 如果给丁的目录不全比如 `.spec/{{功能}}/{{需求}}` `.spec/{{功能}}` 则根据已经获取的信息进行进一步询问
* 如果完全没有信息或者信息无法确定则需要进一步询问
* 只有获取到了完整的功能、需求、设计信息后在**必须**按照下面的`创建功能需求`执行处理


## 从输入信息中分析并判断在`.spec/spec.md` 尾部查找`项目下功能 `下是否有对应的功能.
* 没有则根据当前功能创建
* 仅包含 `{{功能规范文件}}` 如 `.spec/{{功能}}/spec.md ` 不要有下级目录和下级目录的文件

## 创建功能需求
### 必须遵守的工作流程
1. 读取需求所属功能的规范文件(`.spec/{{功能}}/spec.md`)了解功能目前涉及的信息，不存在则根据附录中 .spec/{{功能}}/spec.md 文件格式 创建
2. 先尽最大可能收集信息包括但不限于涉及的准确文档、当前代码位置和逻辑等信息保证准确的创建需求
3. 在实施前探索用户意图、需求和设计
4. 一次问一个问题 ——不要用太多问题让自己感到压力
5. 任何有疑问的位置都必须询问确认具体意图在继续
6. 多项选择题优先 ——比开放式回答更容易回答
7. 渐进式验证 ——展示设计，获得批准后再继续
8. 保持灵活 ——当有不合理的地方时，随时澄清
9. 毫不留情地 ——移除所有设计中的多余功能
10. 明确每个功能点的验收标准

### 必须坚持的核心理念
* 必须通过提问完善粗略的想法，探索替代方案，并将设计分成章节进行验证。保存设计文档。
* 把工作分成小任务（每份 2-5 分钟）。每个任务都有精确的文件路径、完整的代码和验证步骤。
* 不要怕询问次数过多，必须要确定所有疑惑和问题点。
* 需要先评估本次需求对所属功能的规范文件(`.spec/{{功能}}/spec.md`)中的 `当前功能详细信息` 的设计文档按需求读取了解之前的设计
* Don't assume. Don't hide confusion. Surface tradeoffs.Before implementing:
  1. State your assumptions explicitly. If uncertain, ask.
  2. If multiple interpretations exist, present them - don't pick silently.
  3. If a simpler approach exists, say so. Push back when warranted.
  4. If something is unclear, stop. Name what's confusing. Ask.
* Touch only what you must. Clean up only your own mess.
  * When editing existing things:
     1. Don't refactor things that aren't broken.
     2. Don't refactor things that aren't broken. 
     3. Match existing style, even if you'd do it differently. 
 * When your changes create orphans:
     1. Remove imports/variables/functions that YOUR changes made unused.
     2. Don't remove pre-existing dead code unless asked.
 * The test: Every changed line should trace directly to the user's request.
* Define success criteria. Loop until verified.
  * Transform tasks into verifiable goals:
    1. "Add validation" → "Write tests for invalid inputs, then make them pass"
    2. "Fix the bug" → "Write a test that reproduces it, then make it pass"
    3. "Refactor X" → "Ensure tests pass before and after"

* 
### 将最终的功能需求规划设计写入到需求设计文件(`.spec/{{功能}}/{{需求}}/design.md`)中
### 后续的对话也必须按照当前规范来执行并根据输入持续修改需求设计文件(`.spec/{{功能}}/{{需求}}/design.md`)

## 附录
* .spec/{{功能}}/spec.md 文件格式
``` .spec/{{功能}}/spec.md
@Template/function_spec.md
```