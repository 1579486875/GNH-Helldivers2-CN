# -*- coding: utf-8 -*-
"""scan_ui.py -- scan mod Lua sources for ModOptionsMenu-registered UI text, report CN table coverage."""
import os, re, sys, json
HD2 = r"E:\TAML\_scratch\hd2"
sys.path.insert(0, HD2)
from cn_strings import CN
DUMP = os.path.join(HD2, "lua_dump")

FIELD = re.compile(r"\b(label|description|mod|title)\s*=\s*(?:'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\")")
CHOICES = re.compile(r"\bchoices\s*=\s*\{([^}]*)\}", re.S)
LIT = re.compile(r"'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\"")
ZH = re.compile(r"[\u4e00-\u9fff]")

def unesc(s):
    return s.replace("\\'", "'").replace('\\"', '"').replace("\\n", "\n")

files = []
for root, _, names in os.walk(DUMP):
    for n in sorted(names):
        if n.endswith(".lua"):
            p = os.path.join(root, n)
            t = open(p, encoding="utf-8").read()
            if "register_option" in t:
                files.append((p, t))

total_missing = 0
report = {}
for p, t in files:
    acc = {}
    for m in FIELD.finditer(t):
        fld = m.group(1)
        s = unesc(m.group(2) if m.group(2) is not None else m.group(3))
        if not s or len(s) < 2:
            continue
        acc.setdefault(s, fld)
    for m in CHOICES.finditer(t):
        for mm in LIT.finditer(m.group(1)):
            s = unesc(mm.group(1) if mm.group(1) is not None else mm.group(2))
            if not s or len(s) < 2:
                continue
            acc.setdefault(s, "choice")
    miss = {s: f for s, f in acc.items() if not ZH.search(s) and s not in CN}
    if miss:
        rel = os.path.relpath(p, DUMP)
        report[rel] = miss
        total_missing += len(miss)

print("含 register_option 的文件 %d 个；未覆盖字段 %d 条\n" % (len(files), total_missing))
for rel, miss in report.items():
    print("=== %s (%d) ===" % (rel.split(os.sep)[-1], len(miss)))
    for s, f in miss.items():
        print("   [%-11s] %s" % (f, s.replace("\n", " / ")[:170]))
json.dump(report, open(os.path.join(HD2, "notes", "_scan_ui_missing.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
