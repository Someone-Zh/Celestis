## **必须**遵守下面的规范文件格式

```text
.spec/
├── spec.md                         # 唯一入口：项目地图 + 索引 + AI 使用协议
├── rules.md                        # 工程约束
└── {{对应Domain}}/
    ├── domain.spec.md              # 领域字典：边界、共享模型、feature 清单
    └── {{具体Feature名称}}/
        ├── feature.spec.md         # 必填：当前完整设计的结论层
        ├── feature.api.md          # 有对外接口则必填：对外契约
        ├── feature.api.{{资源}}.md # 可选：接口过多时按资源拆分
        ├── feature.{{主题}}.md     # 可选：当前设计的细节主题
        ├── design.md               # 临时：本次设计（归档前）
        ├── changes/                # 临时：任务与变更（归档前）
        │   ├── tasks.md
        │   └── ...
        └── .archive/               # 历史：只追加，不修改
            └── {{版本号}}/
                ├── manifest.md     # 归档记录（纯 Markdown）
                ├── design.md       # 历史设计过程
                ├── changes/
                │   ├── tasks.md
                │   └── ...
                └── fix.md          # 历史修复记录（如有）
```

```text
dist/spec-docs/                     # 对外生成物：不提交、不手工修改
├── README.md
├── llms.txt
├── api-index.md
├── feature-index.md
└── {{Domain}}/{{Feature}}/
    ├── feature.api.md
    ├── feature.api.{{资源}}.md     # 可选：API 拆分文件
    ├── feature.spec.md             # 过滤后的对外版
    └── feature.{{对外主题}}.md     # 父功能卡 §4 未标“（内部）”的主题
```

> 对外文档生成规则见 `.spec/spec.md` §8；本文件只定义文件布局。

### 引用规则
- 索引与跨文件引用规则见 `base.md` §8“引用与索引规则”；本文件只定义文件布局。

### 归并与残留
- `feature.spec.md` 必填；`feature.api.md` 在有对外接口时必填。
- 归档完成后，功能根目录不得残留 `design.md`、`changes/`、`fix.md`。
- 允许保留 `feature.spec.md`、`feature.api.md`、`feature.{主题}.md`。
