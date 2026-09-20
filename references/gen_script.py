# -*- coding: utf-8 -*-
"""生成《教学逐字稿》DOCX（可直接上课使用，含教师口述/学生预设/板书/课件/分层提示）。

对应 Skill 步骤：调用「教师教案与课堂活动」（分层视角）后产出逐字稿。
用法：
    python gen_script.py [lesson_content.json]
输出：./output/<课题>_教学逐字稿.docx
"""
import sys
import os
import json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from docx_common import (new_doc, add_title, add_subtitle, add_para, add_h2,
                         NAVY, BLUE, GREY, DARK, ORANGE, PURPLE)

DEFAULT = os.path.join(HERE, "lesson_content.json")

ROLE_TAG = {
    "teacher": ("〔教师〕", NAVY, DARK),
    "student": ("〔生·预设〕", GREY, __import__("docx").shared.RGBColor(0x40, 0x40, 0x40)),
    "board":   ("〔板书〕", BLUE, BLUE),
    "ppt":     ("〔课件〕", ORANGE, __import__("docx").shared.RGBColor(0x70, 0x40, 0x00)),
    "note":    ("〔提示〕", GREY, GREY),
    "tier":    ("〔分层〕", PURPLE, __import__("docx").shared.RGBColor(0x40, 0x10, 0x60)),
}


def hexc(s):
    if isinstance(s, str) and s.startswith("#"):
        return __import__("docx").shared.RGBColor(int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16))
    return s


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def line(doc, role, text):
    tag, tcol, bcol = ROLE_TAG.get(role, ("〔注〕", GREY, GREY))
    p = doc.add_paragraph()
    p.paragraph_format.space_after = __import__("docx").shared.Pt(3)
    from docx_common import set_cjk
    r1 = p.add_run(tag)
    set_cjk(r1, "宋体", size=11, bold=True, color=hexc(tcol))
    r2 = p.add_run(text)
    italic = (role == "student")
    set_cjk(r2, "宋体", size=11, color=hexc(bcol), italic=italic)
    return p


def timing(doc, text):
    from docx_common import set_cjk
    p = doc.add_paragraph()
    p.paragraph_format.space_before = __import__("docx").shared.Pt(8)
    p.paragraph_format.space_after = __import__("docx").shared.Pt(4)
    r = p.add_run(text)
    set_cjk(r, "黑体", size=12.5, bold=True, color=NAVY)
    return p


def build(c, out_path):
    doc = new_doc()
    m = c["meta"]
    add_title(doc, "《%s》%s · 教学逐字稿" % (m["title"], m["grade"]))
    add_subtitle(doc, "可直接上课使用　｜　%s　｜　时长约 45 分钟" % m["textbook"])
    add_subtitle(doc, "对应《义务教育数学课程标准（2022 年版）》")
    doc.add_paragraph()
    add_para(doc, "使用说明：〔教师〕为上课口述语言；〔生·预设〕为预计学生回答，供参考、可按课堂实际调整；"
                  "〔板书〕〔课件〕为课堂操作提示；〔分层〕为差异化教学提示（不公开贴标签、可流动）。",
              color=GREY, italic=True)

    for p in c.get("process", []):
        timing(doc, "▶ %s（约 0 分钟起，%d 分钟）" % (p["name"], p.get("minutes", 0)))
        for step in p.get("script", []):
            line(doc, step.get("role", "note"), step.get("text", ""))
        if p.get("tier"):
            line(doc, "tier", p["tier"])

    # 附录：分层教学实施提示
    doc.add_page_break()
    add_h2(doc, "附：分层教学实施提示（供教师参考，不公开贴标签）")
    add_para(doc, "依据《义务教育数学课程标准（2022 年版）》及教材编修建议。本课时锚点目标不变："
                  "理解比的意义、会求比值、能沟通比与除法分数的关系。差异只设在任务复杂度、支架量与成果形式上。",
              color=GREY)
    tiers = [
        ("①号任务卡（基础层·保底达标）", "比值计算若卡住，提供示例支架（完整示范并标注每步）+步骤卡（写比→前项÷后项→写比值）。支架第1次全套，第2次撤视觉支架，第3次独立，避免长期依赖。"),
        ("②号任务卡（中等层·能力进阶）", "在基础层加变量：不同类量比、带单位比值的实际意义（如100:2的比值50表示速度）；变式判断“3:2与2:3是否相同”。"),
        ("③号任务卡（拔尖层·拓展挑战）", "开放任务：用比解释“为什么1份蜜+8份水 与 2份蜜+16份水一样甜（1:8=2:16）”；或探究“黄金比为什么好看”，鼓励画图与表达。"),
        ("分组方式", "弹性流动分组：同课堂内不同颜色任务卡，默认推荐。教师巡课时间向①②号倾斜（约70%），③号学生当“小导师”互教。允许完成本层后申请升级、遇困申请支援。"),
        ("评价标尺", "统一用一条核心标尺衡量：能理解比的意义、会求比值、能沟通比与除法分数关系；证据形式可多样（口头/书面/操作），只分级深度，不换标准。"),
    ]
    for k, val in tiers:
        p = doc.add_paragraph(style='List Bullet')
        from docx_common import set_cjk
        r = p.add_run(k + "：")
        set_cjk(r, "宋体", size=10.5, bold=True, color=NAVY)
        r2 = p.add_run(val)
        set_cjk(r2, "宋体", size=10.5)

    doc.save(out_path)
    print("SAVED:", out_path)


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    c = load(src)
    out_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "%s_教学逐字稿.docx" % c["meta"]["title"])
    build(c, out)


if __name__ == "__main__":
    main()
