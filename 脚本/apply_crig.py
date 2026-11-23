# -*- coding: utf-8 -*-
"""apply_crig.py -- 给 C-Rig 写描述 + 汉化名称与选项 + 同步 Arsenal。"""
import os, io, json, re, sys, shutil, time, subprocess, sqlite3
HD2 = r"E:\TAML\_scratch\hd2"
sys.path.insert(0, HD2)
MODS = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal", "mods")
LA = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal")

# 描述（按代码里的实际功能写，不夸大）
DESC = (
    "骨骼替换运行时（前置库）。为使用自定义骨架、带骨骼物理（晃动）的盔甲模组提供运行时支持。"
    "\n\n必须同时安装并启用「Bingus 共享加载器」与「Mod 选项菜单」（ModOptionsMenu），否则本模组不会启动。"
    "\n\n本模组自身不改变任何游戏内容，只是让依赖它的盔甲类模组能正常工作；安装后请保持启用。"
    "\n\n▸ 下面的「运行时」选项请务必勾选（作者原话 MUST SELECT）。"
)

d = [n for n in os.listdir(MODS) if n.startswith("Runtime(ShareLoader)")][0]
root = os.path.join(MODS, d)
mp = os.path.join(root, "manifest.json")

# 备份
BK = os.path.join(HD2, "backup", "manifests-all", re.sub(r'[\\/:*?"<>|]', "_", d)[:60])
os.makedirs(BK, exist_ok=True)
if not os.path.exists(os.path.join(BK, "manifest.json")):
    shutil.copy2(mp, os.path.join(BK, "manifest.json"))

j = json.load(io.open(mp, encoding="utf-8-sig"))
print("原 Name        : %r" % j.get("Name"))
print("原 Description : %r" % j.get("Description"))
j["Name"] = "C-Rig 骨骼运行时（共享加载器）"
j["Description"] = DESC
for o in j.get("Options") or []:
    if o.get("Name") == "Runtime":
        o["Name"] = "运行时"
    if o.get("Description") == "MUST SELECT":
        o["Description"] = "必须选中"
io.open(mp, "w", encoding="utf-8").write(json.dumps(j, ensure_ascii=False, indent=2))
print("\n新 Name        : %r" % j["Name"])
print("新 Description : %s" % DESC.replace("\n", " ")[:110] + "…")
for o in j.get("Options") or []:
    print("新 Option      : %r / %r  Include=%s（目录名，未动）" % (o.get("Name"), o.get("Description"), o.get("Include")))

# 同步 Arsenal（若未运行）
def running():
    try:
        out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq HD2Arsenal.exe"],
                             capture_output=True, text=True, timeout=15).stdout
        return "HD2Arsenal" in out
    except Exception:
        return True

print("\n=== 同步 Arsenal ===")
if running():
    print("   Arsenal 正在运行 —— 挂后台任务，等它退出后再同步")
else:
    ST = os.path.join(LA, "hd2a_data.json")
    shutil.copy2(ST, os.path.join(HD2, "backup", "arsenal-db", "hd2a_data.json.before-crig"))
    s = json.load(io.open(ST, encoding="utf-8"))
    n = 0
    for m in s["modsList"]["default"]["mods"]:
        if os.path.basename(m.get("path") or "") == d:
            m["label"] = j["Name"]; m["description"] = DESC
            for op in m.get("options") or []:
                if op.get("name") == "Runtime": op["name"] = "运行时"
                if op.get("description") == "MUST SELECT": op["description"] = "必须选中"
            n += 1
    for m in s.get("modsLibrary") or []:
        if os.path.basename(m.get("path") or "") == d:
            m["label"] = j["Name"]; m["description"] = DESC
            for op in m.get("options") or []:
                if op.get("name") == "Runtime": op["name"] = "运行时"
                if op.get("description") == "MUST SELECT": op["description"] = "必须选中"
            n += 1
    io.open(ST, "w", encoding="utf-8").write(json.dumps(s, ensure_ascii=False, indent=2))
    json.load(io.open(ST, encoding="utf-8"))
    print("   配置更新 %d 处" % n)
    con = sqlite3.connect(os.path.join(LA, "mod_headers.db"))
    cur = con.execute("UPDATE mods SET label = ? WHERE path LIKE ?", (j["Name"], "%" + d + "%"))
    con.commit()
    print("   数据库更新 %d 行" % cur.rowcount)
    con.close()
