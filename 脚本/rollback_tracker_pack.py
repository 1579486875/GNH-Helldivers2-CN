# -*- coding: utf-8 -*-
"""rollback_tracker_pack.py -- 立即撤销目标追踪器汉化包（字体不支持中文）。"""
import os, sys, io, json, shutil, subprocess, sqlite3
sys.path.insert(0, r"E:\TAML\_scratch\hd2")
from hd2_patch import PatchFile

LA = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal")
MODS = os.path.join(LA, "mods")
D = r"C:\SteamLibrary\steamapps\common\Helldivers 2\data"
TARGET = "mods/codex/private_objective_tracker"
PACK = "GNH-ObjectiveTracker-CN-Addon"

def arsenal_running():
    try:
        out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq HD2Arsenal.exe"],
                             capture_output=True, text=True, timeout=15).stdout
        return "HD2Arsenal" in out
    except Exception:
        return False

print("=== 1) 从游戏 data 删除汉化版 patch ===")
removed = []
for n in sorted(os.listdir(D)):
    if not (n.startswith("9ba626afa44a3aa3.patch_") and n.split("_")[-1].isdigit()):
        continue
    p = os.path.join(D, n)
    if not os.path.isfile(p):
        continue
    try:
        pf = PatchFile.load(p)
    except Exception:
        continue
    for e in pf.entries:
        if (e.path_comment or "") == TARGET:
            t = e.data.decode("utf-8", "ignore")
            if "任务目标追踪" in t:          # 只删我们那个汉化版
                for s in ("", ".gpu_resources", ".stream"):
                    q = p + s
                    if os.path.exists(q):
                        os.remove(q)
                removed.append(n)
                print("   已删除 %s（汉化版）" % n)
            else:
                print("   保留 %s（原始版，含 OBJECTIVE TRACKER）" % n)
print("   共删除 %d 个" % len(removed))

print("\n=== 2) 从 Arsenal 配置移除这个包 ===")
if arsenal_running():
    print("   ⚠️ Arsenal 正在运行 —— 配置改动会被它退出时覆盖，稍后补做")
else:
    ST = os.path.join(LA, "hd2a_data.json")
    shutil.copy2(ST, os.path.join(r"E:\TAML\_scratch\hd2\backup\arsenal-db", "hd2a_data.json.before-rollback"))
    d = json.load(io.open(ST, encoding="utf-8"))
    n = 0
    mods = d["modsList"]["default"]["mods"]
    before = len(mods)
    d["modsList"]["default"]["mods"] = [m for m in mods if os.path.basename(m.get("path") or "") != PACK]
    n += before - len(d["modsList"]["default"]["mods"])
    lib = d.get("modsLibrary") or []
    b2 = len(lib)
    d["modsLibrary"] = [m for m in lib if os.path.basename(m.get("path") or "") != PACK]
    n += b2 - len(d["modsLibrary"])
    io.open(ST, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
    json.load(io.open(ST, encoding="utf-8"))
    print("   已从 %d 处移除" % n)
    DB = os.path.join(LA, "mod_headers.db")
    con = sqlite3.connect(DB)
    cur = con.execute("DELETE FROM mods WHERE path LIKE ?", ("%" + PACK,))
    con.commit()
    print("   数据库删除 %d 行" % cur.rowcount)
    con.close()

print("\n=== 3) 把汉化包挪出模组库（避免误启用） ===")
src = os.path.join(MODS, PACK)
dst = r"E:\TAML\_scratch\hd2\disabled-packs"
os.makedirs(dst, exist_ok=True)
if os.path.isdir(src):
    if os.path.isdir(os.path.join(dst, PACK)):
        shutil.rmtree(os.path.join(dst, PACK))
    shutil.move(src, os.path.join(dst, PACK))
    print("   已移到 %s" % os.path.join(dst, PACK))
else:
    print("   （已不在模组库）")

print("\n=== 4) 复查游戏 data ===")
for n in sorted(os.listdir(D)):
    if not (n.startswith("9ba626afa44a3aa3.patch_") and n.split("_")[-1].isdigit()):
        continue
    p = os.path.join(D, n)
    if not os.path.isfile(p):
        continue
    try:
        pf = PatchFile.load(p)
    except Exception:
        continue
    for e in pf.entries:
        pc = e.path_comment or ""
        if pc == TARGET:
            t = e.data.decode("utf-8", "ignore")
            print("   %-30s 目标追踪器资源：%s" % (n, "汉化版（不该有！）" if "任务目标追踪" in t else "原始英文版 ✅"))
        elif pc.startswith("mods/gnh_cn"):
            print("   %-30s GNH 主包 ✅" % n)
            break
        elif pc == "mods/hd2transmog/foundation":
            print("   %-30s Transmog %s" % (n, "汉化版 ✅" if "自订变体" in e.data.decode("utf-8", "ignore") else "原始版"))
