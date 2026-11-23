# -*- coding: utf-8 -*-
"""sync_fix.py -- 只取编号最大的 GNH 包同步回 Arsenal（并清理残留 66）。"""
import os, io, re, shutil, json, sys
sys.path.insert(0, r"E:\TAML\_scratch\hd2")
from hd2_patch import PatchFile
LA = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal")
DATA = r"C:\SteamLibrary\steamapps\common\Helldivers 2\data"
BK = r"E:\TAML\_scratch\hd2\stale-patches-backup"
os.makedirs(BK, exist_ok=True)

# 1) 找出每个包"编号最大"的那份
best = {"A": None, "B": None}
for f in sorted(os.listdir(DATA)):
    m = re.match(r"^9ba626afa44a3aa3\.patch_(\d+)$", f)
    if not m:
        continue
    n = int(m.group(1)); p = os.path.join(DATA, f)
    try:
        head = open(p, "rb").read(300000)
    except Exception:
        continue
    tag = None
    if b"GNH_CN" in head:
        tag = "A"
    elif b"hd2transmog/foundation" in head and os.path.getsize(p) > 2000000:
        tag = "B"
    if tag and (best[tag] is None or n > best[tag][0]):
        best[tag] = (n, p)
print("1) 每个包取编号最大的：")
for tag, v in best.items():
    print("   %s 包 -> patch_%d (%d 字节)" % (tag, v[0], os.path.getsize(v[1])) if v else "   %s 包 -> 缺失" % tag)

# 2) 同步
st = json.load(io.open(os.path.join(LA, "hd2a_data.json"), encoding="utf-8"))
for m in st["modsList"]["default"]["mods"]:
    lab = str(m.get("label")); d = m.get("path")
    if "GNH" not in lab or not d:
        continue
    tag = "A" if "简体" in lab else "B"
    if not best[tag]:
        continue
    src = best[tag][1]
    dst_dir = os.path.join(d, "Addon"); os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, "9ba626afa44a3aa3.patch_0")
    shutil.copy2(src, dst)
    print("2) ✅ %s 包 patch_%d (%d 字节) -> %s" % (tag, best[tag][0], os.path.getsize(src), os.path.basename(d)))

# 3) 清理非最大的重复包（备份后删除）
for tag in ("A", "B"):
    for f in sorted(os.listdir(DATA)):
        m = re.match(r"^9ba626afa44a3aa3\.patch_(\d+)$", f)
        if not m:
            continue
        n = int(m.group(1)); p = os.path.join(DATA, f)
        if best[tag] is None or n == best[tag][0] or n in (137, 138):
            continue
        try:
            head = open(p, "rb").read(300000)
        except Exception:
            continue
        is_t = (b"GNH_CN" in head and tag == "A") or (b"hd2transmog/foundation" in head
                and os.path.getsize(p) > 2000000 and tag == "B")
        if is_t:
            shutil.copy2(p, os.path.join(BK, f)); os.remove(p)
            print("3) 🗑️ 清理重复的 %s 包 %s (%d 字节，已备份)" % (tag, f, os.path.getsize(os.path.join(BK, f))))
