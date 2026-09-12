---
name: init-celestis
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
* 如果已有则查看是否满足规则格式和内容验证与修正

@Template/base.md

# 扩展
1. 你不需要生成`domain.spec.md`和`feature.spec.md`,但是如果这两个已经存在则需要你查看是否满足规则格式和内容验证与修正。
2. 你的核心任务是准确并按要求的生成或修正 `.spec/rules.md` 和 `.spec/spec.md`

## 附录

* .spec/rules.md
```.spec/rules.md
@Template/rules.md
```

* .spec/spec.md
```.spec/spec.md
@Template/spec.md
```

* .spec/{{领域}}/domain.spec.md 文件格式
``` .spec/{{领域}}/domain.spec.md
@Template/domain_spec.md
```

* .spec/{{领域(Domain)}}/{{功能(Feature)}}/feature.spec.md 文件格式
``` .spec/{{领域(Domain)}}/{{功能(Feature)}}/feature.spec.md 文件格式
@Template/feature_spec.md
```

* .spec/{{领域(Domain)}}/{{功能(Feature)}}/feature.spec.api.md 文件格式
```
@Template/feature_api_spec.md
```