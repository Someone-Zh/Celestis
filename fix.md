---
description: 修正需求
---
@Template/file_spec.md

@Template/base_root.md

@Template/base.md

## 必须指定 已存在的修正文件（`.spec/{{功能}}/{{需求}}/fix.md`） 或 给定的信息可以获取到需求信息以确定需求目录
* **必须**主动询问获取才能继续
  
## 修正需求
1. 先读取需求所属功能的规范文件(.spec/{{功能}}/spec.md)了解功能目前涉及的信息
2. 实现给定信息（fix.md文件内容或对话中提出）的需求
3. 执行完毕需要更新changes/tasks.md文件，内容格式**必须**要遵守附录中的changes/tasks.md 文件格式
4. 如果有涉及外部的变更需生成对应变更文件并写入`changes/{{变更的文件名.格式}}`
5. 将当前需求（如有fix.md则使用其内容，没有则采用对话输入）一字不差的使用`-------------`分隔符追加到design.md下（**不要修改历史信息**）
6. **必须**明确每个小功能的验收标准，并根据验收标准生成测试用例（对和当前功能无关的进行mock，位置根据项目规范或实际项目结构）
7. 确保每个新功能/方法都有测试，输出干净（无错误，警告）
8. 后续的持续对话修正都要**严格**遵守当前规范
9. 并将新的改动使用`-------------`分隔符追加到design.md下（**不要修改历史信息**）
10. 如给定的是修正文件（`.spec/{{功能}}/{{需求}}/fix.md`）则移除这个修正文件（`.spec/{{功能}}/{{需求}}/fix.md`）

### 必须坚持的核心理念
* 必须通过提问完善粗略的想法，探索替代方案，并将设计分成章节进行验证。保存设计文档。
* 把工作分成小任务（每份 2-5 分钟）。每个任务都有精确的文件路径、完整的代码和验证步骤。
* 强制执行 RED-GREEN-REFACTOR：写失败测试，观察它失败，写最小代码，观察它通过，提交。删除测试前编写的代码。
* 如果已有测试用例需同步修改已有的测试。
* 计划进行审查，按严重程度报告问题。关键问题阻碍了进展。
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

## 注意
* 当前一个设计文件过于庞大时（400行左右），需要按照在`design.md`同级目录下增加`{{功能点}}.md`来拆分设计文档,在`design.md`中描述引用对应的子功能点。
* 当`{{功能点}}.md`也过于庞大时同理，也同样拆分，也更贴合渐进式加载。

## 附录
* changes/tasks.md 文件格式
``` changes/tasks.md
@Template/task.md
```