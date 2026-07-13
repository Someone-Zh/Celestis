---
name: init
description: 用于初始化项目规范体系，深度扫描代码库并生成企业级规范文档。当用户提到"初始化项目"、"init project"、"生成规范"、"创建规范文档"、"项目初始化"、"建立规范体系"、"扫描项目结构"、"初始化规范"时自主唤醒。适用于新项目或未规范化项目的首次配置，核心职责包括代码库深度扫描、架构分析、规范文档生成与规则配置。
version: 1.0.0
triggers:
  - type: command
    name: init
globs:
  - "**/*"
disable-model-invocation: false
user-invocable: true
argument-hint: "[项目根目录]"
compatibility: "network: none"
---

@Template/file_spec.md

# 你作为一名资深架构师，请深度扫描项目并生成附录中的企业级规范文档。并严格遵循以下要求：
## 要求：
* 体现企业级项目的严谨性和规范性
   
@Template/base.md

## 附录
* .spec/rules.md
```.spec/rules.md
@Template/rules.md
````
* .spec/spec.md
```.spec/spec.md
@Template/spec.md
```