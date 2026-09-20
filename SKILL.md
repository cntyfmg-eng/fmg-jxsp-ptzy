---
name: fmg-jxsp-ptzy
slug: fmg-jxsp-ptzy
version: "1.0.0"
displayName: 优质课视频转教案课件生成器
description: 把一节优质课视频（B站等公开平台）一键转化为成套备课物料：配套教案、教学逐字稿、说课稿、教学互动课件（HTML5 与 PPTX 两种格式）、说课课件（PPTX）。每一步明确标注所调用的专家与技能，并附可运行脚本与示例数据，确保按流水线能稳定产出全部文件。适用于教师备课、磨课、公开课与教研说课。
agent_created: true
---

# 优质课视频转教案课件生成器

> 沉淀自“视频转教案”真实产出流程：输入一个优质课视频链接，稳定产出 6 类备课物料，
> 且**每一种文件都对应明确的专家与技能**。

## 一、适用场景

- 手头有一节优质课视频（公开课/B站/国家中小学智慧教育平台等），想快速沉淀为可二次编辑的备课包。
- 需要配套产出：教案、逐字稿、说课稿、课堂互动课件（HTML + PPT）、说课 PPT。
- 希望清楚知道每一步该请哪位专家、调哪个技能，避免反复试错。

## 二、触发词

视频转教案、优质课视频、生成教案、生成逐字稿、生成说课稿、说课课件、教学课件、
视频转课件、公开课备课、一课三件套、视频生成 PPT 课件。

## 三、专家 / 技能映射总表（核心）

| 步骤 | 交付物 | 调用的专家 | 调用的技能 | 本 Skill 内工具 |
|---|---|---|---|---|
| 0 分析 | 视频元数据 + 科目/年级判定 | （通用分析，无需特定专家） | — | `references/fetch_bilibili.py` |
| 1 教案 | 《配套教案》DOCX | 教师教案与课堂活动 | 教师教案与课堂活动 | `references/gen_lesson_plan.py` |
| 2 逐字稿 | 《教学逐字稿》DOCX | 分层教学设计师（企鹅教师助手） | 教师教案与课堂活动 | `references/gen_script.py` |
| 3 说课稿 | 《说课稿》DOCX | （说课场景） | 教师教案与课堂活动 | `references/gen_shuoke.py` |
| 4 教学课件 | 互动 HTML5 课件 | 互动课件设计师 | 互动课件设计师 | `references/courseware.html` |
| 5 教学课件 | 互动 PPTX 课件 | 互动课件生成+转PPT | 互动课件生成+转PPT（fmg-html-ppt / slidep） | `references/pages_lesson.json` + `references/ppt_pipeline.md` |
| 6 说课课件 | 说课 PPTX | 互动课件生成+转PPT | 互动课件生成+转PPT（fmg-html-ppt / slidep） | `references/pages_shuke.json` + `references/ppt_pipeline.md` |

> 备注：「视频生成提示词专家」用于步骤 1 中的“AI 视频提示词”小节（导演思维、中英对照）；
> 若要真正生成讲解短视频，再单独调用该专家（需视频生成 API Key）。

## 四、标准工作流

### 步骤 0　分析视频
1. 提取 BV 号/链接，运行 `python references/fetch_bilibili.py <BV号或URL>` 取元数据。
2. 依据标题、简介、分区判定科目、年级、教材单元与课标归属。
3. 透明告知用户：优质课视频普遍无字幕、弹幕压缩，**课堂对话无法逐字还原**，文档语言为
   “课题 + 教材 + 新课标优质课范式”的合理重建，建议结合观课微调。

### 步骤 1　配套教案（调用「教师教案与课堂活动」）
- 把本课内容填入 `references/lesson_content.json`（或直接改默认示例），运行
  `python references/gen_lesson_plan.py` → `output/<课题>_优质课配套教案.docx`。
- 含视频分析报告、课标/教材/学情、目标重难点、教学过程三列表、板书、作业、反思留白、
  及 AI 视频提示词（导演思维、中英对照）。

### 步骤 2　教学逐字稿（调用「教师教案与课堂活动」+ 分层视角）
- 沿用同一份 `lesson_content.json`，运行 `python references/gen_script.py`
  → `output/<课题>_教学逐字稿.docx`。
- 含〔教师〕〔生·预设〕〔板书〕〔课件〕〔提示〕〔分层〕标记、时间码与分层实施提示附录。

### 步骤 3　说课稿（调用「教师教案与课堂活动」）
- 运行 `python references/gen_shuoke.py` → `output/<课题>_说课稿.docx`。
- 八模块完整：说教材/学情/目标/重难点/教法学法/教学过程/板书/特色与反思，附“一句话结论”。

### 步骤 4　教学课件 HTML5（调用「互动课件设计师」）
- 复制 `references/courseware.html` 改文案，离线可用、含 7 处课堂互动 + TTS 朗读 + AI 学伴面板。
- 交付 `<课题>_互动课件.html`，Chrome/Edge 双击打开，F11 全屏投影。

### 步骤 5　教学课件 PPTX（调用「互动课件生成+转PPT」）
- 复制 `references/pages_lesson.json` 改文字，按 `references/ppt_pipeline.md` 走
  build_slides.py → validate → slidep start 编译，再补页间跳转导航 → `<课题>_互动课件.pptx`。

### 步骤 6　说课课件 PPTX（调用「互动课件生成+转PPT」）
- 复制 `references/pages_shuke.json` 改文字，同上流水线 → `<课题>_说课课件.pptx`（八模块说课结构）。

详步见 @references/workflow.md，PPT 编译细节见 @references/ppt_pipeline.md。

## 五、内容数据模型（一处改、三处同步）

三套 DOCX 与课件均读 `references/lesson_content.json`。换科目只改该 JSON 的
`meta / process / board / shuoke / ai_prompts` 等字段，文档与课件自动同步更新。
运行生成器时可传自定义 JSON：`python references/gen_lesson_plan.py 我的课.json`。

## 六、关键约束与降级

- **无字幕**：课堂对话为范式重建，已透明标注；用户提供真实转录后回填 `lesson_content.json` 的 `script` 字段即可。
- **PPT 互动边界**：PPTX 无法承载 HTML 的实时计算/即时判分；用页间跳转导航 + 答案色标 + 「出现」动画替代。
  若 slidep 不可用，按 `ppt_pipeline.md` 降级为纯 python-pptx 或 HTML5 交付，并说明限制。
- **运行环境**：DOCX 生成依赖 python-docx（托管 Python 已装）；slidep 依赖 fmg-html-ppt 技能。
- **输出位置**：脚本产物写到当前目录的 `./output/`，不写死任何用户绝对路径。

## 七、产物清单（典型）

```
output/<课题>_优质课配套教案.docx
output/<课题>_教学逐字稿.docx
output/<课题>_说课稿.docx
<课题>_互动课件.html
<课题>_互动课件.pptx
<课题>_说课课件.pptx
```

## 八、绝不做什么

- 不谎称“已逐字转录视频”：无字幕时明确说明是范式重建。
- 不写死用户本机绝对路径；不把示例数据（比的认识）当作唯一正确模板硬套到其它科目。
- 不跳过专家/技能映射：每一步都按第三节表格调用对应专家与技能。
- 不把 PPT 的静态排版说成“等价 HTML 实时互动”；互动能力差异如实告知。
