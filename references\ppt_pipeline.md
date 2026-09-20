# PPT 课件流水线（教学课件 / 说课课件）

本 Skill 的 PPT 产出走「互动课件生成+转PPT（fmg-html-ppt / slidep）」技能的标准流水线：
把每页逻辑写成 `pages.json` → `build_slides.py` 生成 `.slide`（JSX DSL）→ `validate_slides.py` 校验 → `slidep start` 编译出真实 `.pptx`，最后用 python-pptx 补加页间跳转导航。

> 路径说明：`fmg-html-ppt` 技能的安装目录因机器而异，运行时请用该技能自带说明或 `Skill` 工具定位其 `scripts/` 目录；本文件只用逻辑描述，不写死绝对路径。

## 一、pages.json 版式清单（12 种）

cover / tree / intro / cards / text / compare / claims / quote / sort / flow / homework / read。
本课常用：cover（封面）、tree（知识地图）、intro（情境导入）、cards（概念卡/小结）、text（公式）、compare（比÷分数对比）、claims（辨析/反思）、homework（作业）。

字段示例（cards）：
```json
{
  "type": "cards",
  "title": "探究一：比由哪些“零件”组成",
  "subtitle": "15 ∶ 10 = 1.5",
  "hint": "比号前面的叫前项，后面的叫后项。",
  "items": [
    {"zi": "前项", "py": "15", "ci": "比号前面的数"},
    {"zi": "比号", "py": "∶", "ci": "读作“比”"},
    {"zi": "后项", "py": "10", "ci": "比号后面的数"},
    {"zi": "比值", "py": "1.5", "ci": "前项÷后项的结果"}
  ]
}
```

实例参考：`pages_lesson.json`（教学课件）、`pages_shuke.json`（说课课件）已随本 Skill 提供。

## 二、生成步骤

1. 按本课内容改写 `pages.json`（复制 `pages_lesson.json` 或 `pages_shuke.json` 再改文字）。
2. 运行 `build_slides.py pages.json --out slides` 生成 `.slide` 文件。
3. 运行 `validate_slides.py slides` 校验（应全通过；常见警告为字体渲染，不影响）。
4. 后台运行 `slidep start --project <工程目录> --filename <名称>.pptx`，等待约 10–15 秒生成 pptx。
5. 停止 daemon（非必需，进程会自动退出）。

## 三、补加 PPT 原生互动（页间跳转导航）

PPTX 无法承载 HTML 那种实时计算/即时判分。用 python-pptx 在每页底部加
「⏹封面 / ◀上一页 / 下一页▶」按钮，放映时点按即可跳页（非线性播放，方便课堂灵活调度）。
跳转用 `slide.part.relate_to(目标slide.part, RT.SLIDE)` 建立关系，并写 `a:hlinkClick` 的 `r:id`。
答案页用颜色标注（绿=对、粉=错），便于点击讲解；若想要“点一下才弹出答案”，在 WPS/PowerPoint 里给答案框加「出现」动画（触发=单击）即可。

## 四、降级说明

- 若 `slidep` 不可用（未安装/后端未起）：可改用纯 `python-pptx` 直接排版（牺牲 slidep 的精美 DSL，但能出可打开的 PPTX）。降级时明确告知用户“非 slidep 渲染，排版为功能版”。
- 若 `fmg-html-ppt` 技能不在环境内：PPT 环节退化为“先生成 HTML5 课件（courseware.html），由用户自行用浏览器打印/导出”，并说明限制。
