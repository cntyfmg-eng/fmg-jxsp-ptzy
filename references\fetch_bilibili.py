# -*- coding: utf-8 -*-
"""抓取 B 站优质课视频元数据，输出 JSON，供《视频转教案》Skill 分析阶段使用。

用法：
    python fetch_bilibili.py <BV号或视频URL> [--oid <弹幕oid>]

说明：
- 优先用 curl 调用公开 API（api.bilibili.com/x/web-interface/view），无需登录。
- 若环境无 curl，会尝试 urllib（部分沙箱禁用，fail 时会提示改用系统 Bash）。
- 输出 JSON 含标题/简介/时长/分区/UP主/播放数据等，便于后续判断科目、年级、课标归属。
- 注意：B 站视频普遍无字幕，弹幕为压缩格式，无法逐字还原课堂对话；本脚本只取元数据。
"""
import sys
import json
import re
import subprocess


def extract_bvid(text):
    m = re.search(r"BV[0-9A-Za-z]+", text)
    return m.group(0) if m else None


def fetch_view(bvid):
    url = "https://api.bilibili.com/x/web-interface/view?bvid=" + bvid
    # 优先 curl
    try:
        out = subprocess.check_output(
            ["curl", "-s", "--max-time", "30", url],
            stderr=subprocess.DEVNULL,
        ).decode("utf-8", "ignore")
        return json.loads(out)
    except Exception:
        pass
    # 回退 urllib
    try:
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8", "ignore"))
    except Exception as e:
        return {"error": "fetch_failed", "detail": str(e)}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "usage", "hint": "python fetch_bilibili.py <BV号或URL>"}, ensure_ascii=False))
        return
    arg = sys.argv[1]
    bvid = extract_bvid(arg)
    if not bvid:
        print(json.dumps({"error": "no_bvid", "hint": "未能从输入中解析 BV 号"}, ensure_ascii=False))
        return
    data = fetch_view(bvid)
    if data.get("code") != 0 and "data" not in data:
        print(json.dumps({"bvid": bvid, "raw": data}, ensure_ascii=False, indent=2))
        return
    d = data.get("data", data)
    out = {
        "bvid": bvid,
        "title": d.get("title"),
        "desc": (d.get("desc") or "")[:500],
        "duration_sec": d.get("duration"),
        "duration_text": ("%d 分 %d 秒" % (d.get("duration", 0) // 60, d.get("duration", 0) % 60)
                          if isinstance(d.get("duration"), int) else None),
        "uploader": (d.get("owner") or {}).get("name"),
        "pubdate": d.get("pubdate"),
        "tname": d.get("tname"),
        "quality": ("%dx%d" % (d.get("dimension", {}).get("width", 0),
                               d.get("dimension", {}).get("height", 0)) if d.get("dimension") else None),
        "stats": {
            "view": (d.get("stat") or {}).get("view"),
            "like": (d.get("stat") or {}).get("like"),
            "favorite": (d.get("stat") or {}).get("favorite"),
            "coin": (d.get("stat") or {}).get("coin"),
        },
        "pages": [p.get("part") for p in d.get("pages", [])],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
