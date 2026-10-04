# -*- coding: utf-8 -*-
"""verify_tm.py -- 安全校验：pack B 只改上屏文本，不得改动任何「比较用」字符串。"""
import sys, os, re, difflib
sys.path.insert(0, r"E:\TAML\_scratch\hd2")
from hd2_patch import PatchFile

D = r"C:\SteamLibrary\steamapps\common\Helldivers 2\data"
old = PatchFile.load(os.path.join(D, "9ba626afa44a3aa3.patch_60")).entries[0].data.decode("utf-8", "replace")
new = PatchFile.load(os.path.join(D, "9ba626afa44a3aa3.patch_127")).entries[0].data.decode("utf-8", "replace")

PATS = [("equals", re.compile(r"==\s*'([^'\n]{1,120})'")),
        ("noteq", re.compile(r"~=\s*'([^'\n]{1,120})'")),
        ("index", re.compile(r"\[\s*'([^'\n]{1,120})'\s*\]"))]

print("=== 1) 比较/索引语境里的字符串是否被改动 ===")
bad = 0
for kind, rx in PATS:
    for s in sorted(set(rx.findall(old))):
        n_old = len(re.findall(r"[=~]?=\s*" + re.escape("'" + s + "'"), old)) if kind != "index" else old.count("['" + s + "']")
        n_new = len(re.findall(r"[=~]?=\s*" + re.escape("'" + s + "'"), new)) if kind != "index" else new.count("['" + s + "']")
        if n_new < n_old:
            # 该字面量在 pack B 里被替换掉了一部分
            bad += 1
            print("  [!] %-7s %-34s 原 %d -> 现 %d" % (kind, repr(s), n_old, n_new))
print("  受影响字面量 %d 个" % bad)

print("\n=== 2) 关键判定对：section.title 与 header.text 必须仍然一致 ===")
for s in ["section={title='Custom Variant'", "header.text=='Custom Variant'"]:
    print("  原 %-40s %d  /  现 %d" % (s, old.count(s), new.count(s)))

print("\n=== 3) 上屏文本的中文化情况 ===")
for s in ["text('Custom Variant'", "text('MODIFIED UNIQUE'", "text('Default: '",
          "text('Now (temporary): '", "text('Modded '", "'Name and create'", "'Set the look'",
          "'D-pad / left stick: choose a look. A: select.'", "' saved'", "' owned choices'"]:
    print("  %-52s 原 %d -> 现 %d" % (s, old.count(s), new.count(s)))

print("\n=== 4) 逐行 diff 概况 ===")
a, b = old.split("\n"), new.split("\n")
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
blocks = [op for op in sm.get_opcodes() if op[0] != "equal"]
print("  行数 %d -> %d；改动块 %d 个" % (len(a), len(b), len(blocks)))
for tag, i1, i2, j1, j2 in blocks:
    for l in a[i1:i2]:
        print("   -  %s" % l.strip()[:150])
    for l in b[j1:j2]:
        print("   +  %s" % l.strip()[:150])
