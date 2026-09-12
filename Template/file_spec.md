## **必须**遵守下面的规范文件格式
.spec/
├── spec.md                         # 全局规范文件
├── rules.md                        # 全局规则约束文件
└── {{对应Domain}}/                     # 领域（模块）根目录（例如：auth）
    ├── domain.spec.md              # 领域规范（历史老文件如果叫 spec.md 需要为其更新命名并应用新的模版）
    └── {{具体Feature名称}}/         #  特性（功能）固定的功能特性目录（例如：login）
        ├── feature.spec.md         # 【全量最新】该 Feature 的最新全量逻辑与对外规范
        ├── feature.{{具体子功能}}.md # 【可选】当feature功能设计过于复杂时拆分的子Feature 由 feature.spec.md 引入按需加载
        ├── feature.api.md          # 【可选】当前featurede对外API（包括公开方法、对外端点等一切可供外部调用的） 由 feature.spec.md 引入按需加载,如果对外api过多可以多个名称为`feature.api.{{具体功能}}.md`
        ├── feature.api.{{具体功能}}.md  # 【可选】 当 feature.api.md 文件大于500行时拆分的
        ├── design.md               # 当前版本的设计文档
        └── changes/                # 当前需求的更改目录 
            ├── tasks.md            # 当前需求的实施任务清单
            └── ...                 # 其他产物
        └── .archive/               # 历史演进目录
            └── {{版本号}}
                ├── design.md        # 历史变更的只读补丁快照
                └── changes/         # 历史功能的更改目录 
                    ├── tasks.md     # 历史功能的实施任务清单
                    └── ...          # 其他产物
            ......
......