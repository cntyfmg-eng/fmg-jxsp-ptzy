# 优质课视频转教案课件生成器

把一节优质课视频（B站等公开平台）一键转化为成套备课物料：配套教案、教学逐字稿、说课稿、教学互动课件（HTML5 与 PPTX 两种格式）、说课课件（PPTX）。每一步明确标注所调用的专家与技能，并附可运行脚本与示例数据，确保按流水线能稳定产出全部文件。适用于教师备课、磨课、公开课与教研说课。

一个 WorkBuddy Skill，把可复用的工作流固化下来，供随时调用。

## 文件结构

```
fmg-jxsp-ptzy/
├── SKILL.md            # Skill 定义(入口, 含 front matter)
├── icon.png            # 图标
├── references/         # 参考模板 / 资料 / 数据
├── scripts/            # 自动化脚本(若有)
├── README.md
├── LICENSE
└── .gitignore
```

## 安装

将本仓库内容放入 WorkBuddy 的 skills 目录(`~/.workbuddy/skills/fmg-jxsp-ptzy/`), 重启或刷新即可。

## License

MIT © cntyfmg-eng
