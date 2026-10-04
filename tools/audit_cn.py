# -*- coding: utf-8 -*-
"""audit_cn.py -- 词表静态质量审计。

检查项：
  1. 键/值里的控制字符（\r、\0、制表符等）—— 会破坏生成的 Lua 字面量或导致上游拒绝
  2. 翻译长度上限：选项名 label 64 / 选项值 choice 48 / 说明 description 400 / 模组名 mod 40（按字符数）
     超限会让上游 translation.resolve 返回 nil，**整个注册被拒绝、选项从菜单里消失**
  3. 与 ModOptionsMenu 内置的 NATIVE_WORDS（游戏会自己翻译的词）是否冲突
  4. 空键、空值、键值相同（等于没翻译）、值里仍是英文
  5. 键在哪些模组里作为什么字段出现（用于判断上面第 2 条的适用上限）
"""
import os, re, sys, json, unicodedata
HD2 = r"E:\TAML\_scratch\hd2"
sys.path.insert(0, HD2)
from cn_strings import CN

DUMP = os.path.join(HD2, "lua_dump")
ZH = re.compile(r"[\u4e00-\u9fff]")
CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")

# ---------- 1. 从各模组 Lua 源里收集字段类型 ----------
FIELD = re.compile(r"\b(label|description|mod|title)\s*=\s*(?:'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\")")
CHOICES = re.compile(r"\bchoices\s*=\s*\{([^}]*)\}", re.S)
LIT = re.compile(r"'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\"")

def unesc(s):
    return s.replace("\\'", "'").replace('\\"', '"').replace("\\n", "\n").replace("\\\\", "\\")

kinds = {}
for root, _, names in os.walk(DUMP):
    for n in sorted(names):
        if not n.endswith(".lua"):
            continue
        t = open(os.path.join(root, n), encoding="utf-8", errors="replace").read()
        if "register_option" not in t and "register_binding" not in t:
            continue
        for m in FIELD.finditer(t):
            s = unesc(m.group(2) if m.group(2) is not None else m.group(3))
            if s:
                kinds.setdefault(s, set()).add(m.group(1))
        for m in CHOICES.finditer(t):
            for mm in LIT.finditer(m.group(1)):
                s = unesc(mm.group(1) if mm.group(1) is not None else mm.group(2))
                if s:
                    kinds.setdefault(s, set()).add("choice")

# 上游长度上限（字符数）
LIMIT = {"label": 64, "choice": 48, "description": 400, "mod": 40, "title": 64}
NATIVE = set("""OFF ON NO YES LOW MEDIUM HIGH ULTRA DEFAULT CUSTOM NORMAL INVERTED WEAK STRONG
BASIC ADVANCED FULL PERFORMANCE BALANCED QUALITY GLOBAL ALWAYS DISABLED HIDDEN VISIBLE SMALL
LARGE SHORT DYNAMIC HOLD PRESS TAP""".split())

def clen(s):
    return len(s)

problems = {"ctrl": [], "toolong": [], "native": [], "empty": [], "same": [], "still_en": []}
for k, v in CN.items():
    ks = kinds.get(k, set())
    if CTRL.search(k) or CTRL.search(v) or "\r" in k or "\r" in v:
        problems["ctrl"].append((k, v, sorted(ks)))
    if not k.strip() or not v.strip():
        problems["empty"].append((k, v, sorted(ks)))
    if k == v:
        problems["same"].append((k, v, sorted(ks)))
    # 长度：按它可能出现的每一种字段逐个核
    for kind in (ks or {"label"}):
        lim = LIMIT.get(kind, 64)
        if clen(v) > lim:
            problems["toolong"].append((k, v, kind, clen(v), lim))
    # 与游戏原生词冲突
    if k.upper() in NATIVE:
        problems["native"].append((k, v, sorted(ks)))
    # 翻译后仍是纯英文（没翻到）
    if not ZH.search(v) and v.upper() == k.upper():
        problems["still_en"].append((k, v, sorted(ks)))

print("词表 %d 条；被识别的字段键 %d 个\n" % (len(CN), len(kinds)))
def show(title, rows, fmt):
    print("=== %s：%d ===" % (title, len(rows)))
    for r in rows[:40]:
        print("   " + fmt(r))
    if len(rows) > 40:
        print("   ...（其余 %d 条省略）" % (len(rows) - 40))
    print()

show("1) 含控制字符（\\r 等）", problems["ctrl"], lambda r: "%r -> %r  %s" % (r[0][:60], r[1][:60], r[2]))
show("2) 翻译超长（会导致上游拒绝注册）", problems["toolong"],
     lambda r: "%-16s %-58r 中文 %d 字 > 上限 %d" % (r[2], r[0][:56], r[3], r[4]))
show("3) 与游戏原生词 NATIVE_WORDS 冲突", problems["native"], lambda r: "%-14r -> %-14r 出现为 %s" % (r[0], r[1], r[2]))
show("4) 空键或空值", problems["empty"], lambda r: "%r -> %r" % (r[0], r[1]))
show("5) 键与值完全相同（等于没翻）", problems["same"], lambda r: "%r  %s" % (r[0], r[2]))
show("6) 译文仍是纯英文", problems["still_en"], lambda r: "%r -> %r" % (r[0], r[1]))

json.dump({k: [[x if not isinstance(x, set) else sorted(x) for x in r] for r in v] for k, v in problems.items()},
          open(os.path.join(HD2, "notes", "_audit_cn.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
