# -*- coding: utf-8 -*-
"""desc_scan.py -- 扫描 Arsenal 里所有模组的描述，找出还是英文的。"""
import os, io, json, re
LA = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal")
CJK = re.compile(r"[\u4e00-\u9fff]")
st = json.load(io.open(os.path.join(LA, "hd2a_data.json"), encoding="utf-8"))
print("=== modsList 里的描述 ===")
need = []
for i, m in enumerate(st["modsList"]["default"]["mods"], 1):
    lab = str(m.get("label")); d = str(m.get("description") or "")
    if d and not CJK.search(d):
        need.append(("modsList", i, lab, d))
        print("   #%-3d %-30s %s" % (i, lab[:30], d[:88]))
print("   → 英文描述 %d 条" % len(need))
print("\n=== modsLibrary 里的描述 ===")
n2 = 0
for m in (st.get("modsLibrary") or []):
    lab = str(m.get("label") or m.get("name") or ""); d = str(m.get("description") or "")
    if d and not CJK.search(d):
        n2 += 1
        print("   %-30s %s" % (lab[:30], d[:88]))
print("   → 英文描述 %d 条" % n2)
print("\n=== 所有模组目录里的 manifest Description ===")
MODS = os.path.join(LA, "mods")
for name in sorted(os.listdir(MODS)):
    mf = os.path.join(MODS, name, "manifest.json")
    if not os.path.exists(mf):
        continue
    try:
        j = json.load(io.open(mf, encoding="utf-8-sig"))
    except Exception:
        continue
    d = str(j.get("Description") or "")
    if d and not CJK.search(d):
        print("   %-46s %s" % (name[:46], d[:76]))
