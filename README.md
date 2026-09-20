# 优质课视频转教案课件生成器

把一节优质课视频（B站等公开平台）一键转化为成套备课物料：配套教案、教学逐字稿、说课稿、教学互动课件（HTML5 与 PPTX 两种格式）、说课课件（PPTX）。每一步明确标注所调用的专家与技能，并附可运行脚本与示例数据，确保按流水线能稳定产出全部文件。适用于教师备课、磨课、公开课与教研说课。

一个把**优质课视频**（B站、国家中小学智慧教育平台等公开平台）一键转化为成套备课物料的 WorkBuddy 技能。视频链接丢进去，出来的就是可二次编辑的完整备课包。

## 功能一览

输入一个优质课视频链接，自动产出以下六份资料：

| 交付物 | 格式 | 调用的专家 / 技能 |
| --- | --- | --- |
| 配套教案 | DOCX | 教师教案与课堂活动 + 视频生成提示词专家 |
| 教学逐字稿 | DOCX | 教师教案与课堂活动（分层教学设计师视角） |
| 说课稿 | DOCX | 教师教案与课堂活动 |
| 教学互动课件 | HTML5 单文件 | 互动课件设计师 |
| 教学课件 | PPTX | 互动课件生成+转PPT（fmg-html-ppt / slidep） |
| 说课课件 | PPTX | 同上（12 页覆盖说课八模块） |

每份资料都明确标注了生成它时所调用的专家与技能，便于追溯与迭代。

## 用法

在 WorkBuddy 对话中输入：

```
@skill:fmg-jxsp-ptzy https://www.bilibili.com/video/BVxxxxxxxx
```

技能会自动：① 抓取视频元数据 → ② 判断科目年级 → ③ 生成三份 DOCX → ④ 生成 HTML5 互动课件与两份 PPTX。产物存放在当前工作目录。

换科目只需修改 `references/lesson_content.json` 一处，三套文档与课件自动同步。

## 文件结构

```
fmg-jxsp-ptzy/
├── SKILL.md              # 技能说明 + 专家/技能映射总表
├── references/
│   ├── docx_common.py    # 共享 DOCX 排版助手（中文字体/表格/卡片）
│   ├── fetch_bilibili.py # B站视频元数据抓取
│   ├── gen_lesson_plan.py# 教案生成器
│   ├── gen_script.py     # 逐字稿生成器
│   ├── gen_shuoke.py     # 说课稿生成器
│   ├── lesson_content.json # 统一数据模型（改一处驱动全部）
│   ├── courseware.html   # 单文件 HTML5 互动课件模板
│   ├── pages_lesson.json # 教学 PPT 版式示例
│   ├── pages_shuke.json  # 说课 PPT 版式示例
│   ├── ppt_pipeline.md   # PPTX 流水线说明
│   └── workflow.md       # 完整工作流文档
├── README.md
├── LICENSE
└── .gitignore
```

## 安装

将本仓库克隆或解压到 WorkBuddy 用户级技能目录：

```
~/.workbuddy/skills/fmg-jxsp-ptzy/
```

重启 WorkBuddy 后，技能即可在「专家 / 技能」中心被调用。

## 许可证

MIT © 2026 cntyfmg-eng
