# academic-agent

一个本地学术材料处理 agent，用于读取论文、课程报告或文本材料，并结合自定义 skill 生成论文检查结果或课程汇报内容。

## 当前功能

- 读取 PDF、Word、txt、Markdown 文件
- 加载本地 SKILL.md 工作流规则
- 调用 Kimi API 生成结果
- 输出 Markdown 文件
- 支持两个任务：
  - 论文终稿检查
  - 课程汇报内容生成

## 项目结构

```text
academic-agent
├── main.py
├── llm_client.py
├── test_kimi.py
├── requirements.txt
├── .env.example
├── .gitignore
├── input
│   └── README.md
├── output
│   └── README.md
├── skills
│   ├── paper-final-check-skill
│   │   └── SKILL.md
│   └── course-ppt-content-skill
│       └── SKILL.md
└── tools
    ├── __init__.py
    ├── file_reader.py
    └── skill_loader.py
