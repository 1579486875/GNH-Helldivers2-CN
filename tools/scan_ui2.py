# -*- coding: utf-8 -*-
"""scan_ui2.py -- 改进版覆盖率扫描。

和第一版的区别：能正确处理 Lua 里的**跨行字符串拼接**，例如
    description = '第一段。 '
                  .. '第二段。'
运行时送进菜单的是拼好的整句，所以扫描器也必须拼好再比对，
否则会把"其实已经翻译好的"误报成漏翻（第一版就踩了这个坑）。
"""
import os, re, sys, json
HD2 = r"E:\TAML\_scratch\hd2"
sys.path.insert(0, HD2)
from cn_strings import CN

DUMP = os.path.join(HD2, "lua_dump")
ZH = re.compile(r"[\u4e00-\u9fff]")
STR = r"(?:'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\")"
FIELD = re.compile(r"\b(label|description|mod|title)\s*=\s*" + STR + r"((?:\s*\.\.\s*" + STR + r")*)", re.S)
CHOICES = re.compile(r"\bchoices\s*=\s*\{(.*?)\}\s*,\s*(?:default|description|gap|label|$)", re.S)
LIT = re.compile(STR)

def unesc(s):
    return (s.replace("\\'", "'").replace('\\"', '"')
             .replace("\\n", "\n").replace("\\t", "\t").replace("\\\\", "\\"))

def pieces(m):
    """把一个字段的所有字符串片段按 Lua 的 .. 语义原样拼起来。"""
    out = []
    for g in (2, 3):
        if m.group(g) is not None:
            out.append(unesc(m.group(g)))
    rest = m.group(4) or ""
    for mm in LIT.finditer(rest):
        s = mm.group(1) if mm.group(1) is not None else mm.group(2)
        if s is not None:
            out.append(unesc(s))
    return "".join(out)

found = {}          # 完整文本 -> 出现的字段类型集合
for root, _, names in os.walk(DUMP):
    for n in sorted(names):
        if not n.endswith(".lua"):
            continue
        t = open(os.path.join(root, n), encoding="utf-8", errors="replace").read()
        if "register_option" not in t and "register_binding" not in t:
            continue
        for m in FIELD.finditer(t):
            s = pieces(m)
            if s and len(s) >= 2:
                found.setdefault(s, set()).add(m.group(1))
        for m in CHOICES.finditer(t):
            for mm in LIT.finditer(m.group(1)):
                s = unesc(mm.group(1) if mm.group(1) is not None else mm.group(2))
                if s and len(s) >= 2:
                    found.setdefault(s, set()).add("choice")

# 只保留"看起来像界面文本"的：排除纯键名、路径、代码片段
def looks_like_text(s):
    if ZH.search(s):
        return False                       # 已经是中文，不用管
    if re.fullmatch(r"[a-z_][\w.]*", s):
        return False                       # 翻译键 / 变量名，如 option.region.label
    if "/" in s and " " not in s:
        return False                       # 资源路径
    if s.startswith("..") or s.endswith("or ") or s.startswith("@"):
        return False
    return True

pending = {s: sorted(v) for s, v in found.items() if looks_like_text(s) and s not in CN}
print("扫描到界面文本 %d 条；其中【词表里没有】的 %d 条\n" % (len(found), len(pending)))
for s in sorted(pending, key=lambda x: (pending[x], x)):
    print("  [%-11s] %s" % (",".join(pending[s]), s[:170]))
json.dump(pending, open(os.path.join(HD2, "notes", "_pending_ui.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print("\n--- 抽查：多行拼接的说明是否被正确识别为已翻译 ---")
for probe in ["Nudge the badge sideways", "Another HUD mod may", "Detailed log (Logs"]:
    matched = [s for s in found if s.startswith(probe)]
    for s in matched[:1]:
        print("  %s  %s" % ("已在词表" if s in CN else "词表缺失", s[:100]))
