# -*- coding: utf-8 -*-
"""restore_hd2_cn.py -- 撤销本工作区对 HD2 模组做的汉化（从备份恢复 mods 目录并同步回游戏 data）。"""
import os, sys, shutil, hashlib, io
from hd2_patch import PatchFile

MODS = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal", "mods")
BACKUP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backup")
GAMEDATA = os.environ.get("HD2_DATA", r"C:\SteamLibrary\steamapps\common\Helldivers 2\data")
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes", "restore.txt")

buf = io.StringIO()
restored = []
for dirpath, _, names in os.walk(BACKUP):
    for n in names:
        if not (n.endswith(".patch_0") or n.endswith(".patch_1")):
            continue
        src = os.path.join(dirpath, n)
        rel = os.path.relpath(src, BACKUP)
        dst = os.path.join(MODS, rel)
        shutil.copy2(src, dst)
        restored.append((rel, os.path.getsize(src)))
        print("恢复:", rel, os.path.getsize(src), file=buf)

# 同步回游戏 data（按内容匹配：备份文件 == 某个 data patch 时，把备份写回去）
backup_blobs = {}
for dirpath, _, names in os.walk(BACKUP):
    for n in names:
        p = os.path.join(dirpath, n)
        backup_blobs[hashlib.sha256(open(p, "rb").read()).hexdigest()] = p
synced = 0
for n in os.listdir(GAMEDATA):
    if not n.startswith("9ba626afa44a3aa3.patch_"):
        continue
    p = os.path.join(GAMEDATA, n)
    if os.path.getsize(p) < 200:
        continue
    try:
        pf = PatchFile.load(p)
    except Exception:
        continue
    path = next((e.path_comment for e in pf.entries if e.path_comment), None)
    if path in ("mods/cowboybingus/mod_options_menu", "mods/hd2transmog/foundation"):
        for h, bp in backup_blobs.items():
            if os.path.basename(bp) == n or True:
                pass
        # 直接按 mod 路径找备份
        target = None
        for h, bp in backup_blobs.items():
            if "ModOptionsMenu" in bp and path == "mods/cowboybingus/mod_options_menu":
                target = bp
            if "Transmog" in bp and path == "mods/hd2transmog/foundation":
                target = bp
        if target:
            shutil.copy2(target, p)
            synced += 1
            print("同步回 data:", n, "<-", os.path.basename(os.path.dirname(target)), file=buf)

print("\n共恢复 %d 个模组文件，同步 %d 个游戏 data 文件。" % (len(restored), synced), file=buf)
print("提示：也可以在 HD2 Arsenal 里点一次 Deploy，让它按当前 mod 库重新部署。", file=buf)
open(LOG, "w", encoding="utf-8").write(buf.getvalue())
print(buf.getvalue())
