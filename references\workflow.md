# 《视频转教案》标准工作流（详细版）

本文件是 SKILL.md 的扩展，给出每一步的可执行细节。所有脚本均在 `references/` 下，运行环境为
WorkBuddy 托管的 Python（已装 python-docx）。运行前先 `cd` 到你的任务目录，脚本会把产物写到 `./output/`。

## 步骤 0　分析视频（拿元数据、判定科目年级）

- 调用 `references/fetch_bilibili.py <BV号或URL>` 取标题/时长/分区/UP主/播放数据。
- 结合标题与简介，判断科目（数学/语文/…）、年级、对应教材单元与课标归属。
- 重要：B 站优质课普遍无字幕、弹幕为压缩格式，**无法逐字还原课堂对话**。因此教案/逐字稿/说课稿的
  课堂语言是基于“视频课题 + 教材内容 + 新课标优质课范式”的合理重建，需在交付时向用户透明说明，
  并建议用户结合视频实际观课再微调提问语。

## 步骤 1　配套教案（DOCX）

- 专家/技能：**教师教案与课堂活动**（专家「教师教案与课堂活动」）。
- 生成：把分析得到的本课内容填入 `references/lesson_content.json`（或直接改默认示例），
  运行 `python references/gen_lesson_plan.py`。产物：`output/<课题>_优质课配套教案.docx`。
- 文档含：视频分析报告 + 课标/教材/学情 + 目标/重难点 + 教学过程三列表 + 板书 + 作业 + 教学反思留白
  + 配套 AI 视频提示词（导演思维、中英对照）。
- 视频生成提示词专家：其中“AI 视频提示词”部分遵循「视频生成提示词专家」的导演思维格式，
  若要真正生成讲解短视频，再调用该专家（需配置视频生成 API Key）。

## 步骤 2　教学逐字稿（DOCX）

- 专家/技能：**分层教学设计师**视角 + **教师教案与课堂活动**技能。
- 生成：沿用同一份 `lesson_content.json`（其 `process[].script` 已按角色分段），
  运行 `python references/gen_script.py`。产物：`output/<课题>_教学逐字稿.docx`。
- 文档含：〔教师〕〔生·预设〕〔板书〕〔课件〕〔提示〕〔分层〕标记 + 时间码 + 附录分层实施提示。

## 步骤 3　说课稿（DOCX）

- 专家/技能：**教师教案与课堂活动**（说课场景）。
- 生成：运行 `python references/gen_shuoke.py`。产物：`output/<课题>_说课稿.docx`。
- 文档八模块：说教材/学情/目标/重难点/教法学法/教学过程/板书/特色与反思，开场附“一句话结论”。

## 步骤 4　教学课件（HTML5，可课堂互动）

- 专家/技能：**互动课件设计师**。
- 生成：复制 `references/courseware.html` 为本课课件，替换标题、情境文案、比值示例、关系表文字。
  该模板是自包含单文件，离线可用，含 7 处课堂互动（国旗点击揭示比 / 比的各部位点击 / 比值实时计算器
  / 比÷分数关系高亮 / 后项≠0 辨析 / 分层测验即时反馈 / 三会小结）+ TTS 朗读 + AI 学伴面板。
- 交付：`本课_互动课件.html`，Chrome/Edge 双击打开即可，投影按 F11 全屏。

## 步骤 5　教学课件（PPTX，带导航互动）

- 专家/技能：**互动课件生成+转PPT（fmg-html-ppt / slidep）**。
- 生成：复制 `references/pages_lesson.json` 改文字，按 `references/ppt_pipeline.md` 走
  build_slides.py → validate → slidep start 编译出 PPTX，再补加页间跳转导航。产物：`本课_互动课件.pptx`。

## 步骤 6　说课课件（PPTX，陈述型）

- 专家/技能：**互动课件生成+转PPT（fmg-html-ppt / slidep）**。
- 生成：复制 `references/pages_shuke.json` 改文字，同上流水线。覆盖八模块说课结构。产物：`本课_说课课件.pptx`。

## 产物清单（典型）

```
output/
  <课题>_优质课配套教案.docx
  <课题>_教学逐字稿.docx
  <课题>_说课稿.docx
<课题>_互动课件.html
<课题>_互动课件.pptx
<课题>_说课课件.pptx
```

## 通用降级

- 视频无字幕：课堂对话为范式重建，已透明标注；用户提供真实转录后可回填 `lesson_content.json` 的 `script` 字段。
- PPT 流水线不可用：按 `ppt_pipeline.md` 第四节降级为纯 python-pptx 或 HTML5 交付。
- 换科目：只需改 `lesson_content.json` 的 `meta/process/board/...` 等字段，三套文档与课件同步更新。
