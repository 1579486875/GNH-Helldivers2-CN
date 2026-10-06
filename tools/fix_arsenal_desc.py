# -*- coding: utf-8 -*-
"""desc_fix.py -- 把 HUD+ 的名字与描述写回 manifest 与 Arsenal 数据。"""
import os, io, json, re, shutil, datetime
LA = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal")
BK = r"E:\TAML\_scratch\hd2\arsenal-backup"
os.makedirs(BK, exist_ok=True)
stamp = datetime.datetime.now().strftime("%H%M%S")
NAME_ZH = "HD2 抬头显示+"
DESC_ZH = ("补齐原版 HUD 缺少的内容：3D 武器面板、弹药数与武器栏图标、弹道预览、小队状态 —— "
           "全部基于游戏自身的 HUD 实现，在游戏的选项菜单里设置。")
TARGET = "抬头显示"

# 1) manifest.json
p = [m for m in json.load(io.open(os.path.join(LA, "hd2a_data.json"), encoding="utf-8"))
     ["modsList"]["default"]["mods"] if TARGET in str(m.get("label"))][0]["path"]
mf = os.path.join(p, "manifest.json")
shutil.copy2(mf, os.path.join(BK, "manifest_%s.json" % stamp))
j = json.load(io.open(mf, encoding="utf-8-sig"))
print("1) manifest 原名: %s" % j.get("Name"))
j["Name"] = NAME_ZH
j["Description"] = DESC_ZH
io.open(mf, "w", encoding="utf-8").write(json.dumps(j, ensure_ascii=False, indent=2))
print("   ✅ manifest 已更新: %s" % NAME_ZH)

# 2) hd2a_data.json（modsList + modsLibrary）
dp = os.path.join(LA, "hd2a_data.json")
shutil.copy2(dp, os.path.join(BK, "hd2a_data_%s.json" % stamp))
st = json.load(io.open(dp, encoding="utf-8"))
n = 0
for m in st["modsList"]["default"]["mods"]:
    if TARGET in str(m.get("label")):
        m["description"] = DESC_ZH; n += 1
        print("2) modsList[%s] 描述已更新" % m.get("label"))
for m in (st.get("modsLibrary") or []):
    if TARGET in str(m.get("label") or m.get("name") or ""):
        m["description"] = DESC_ZH; n += 1
        print("2) modsLibrary[%s] 描述已更新" % m.get("label"))
io.open(dp, "w", encoding="utf-8").write(json.dumps(st, ensure_ascii=False, indent=1))
print("   ✅ hd2a_data.json 写入完成（%d 处）" % n)

# 3) mod_headers.db（SQLite，看有没有描述字段）
db = os.path.join(LA, "mod_headers.db")
if os.path.exists(db):
    shutil.copy2(db, os.path.join(BK, "mod_headers_%s.db" % stamp))
    import sqlite3
    con = sqlite3.connect(db); cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tabs = [r[0] for r in cur.fetchall()]
    for t in tabs:
        cur.execute("PRAGMA table_info(%s)" % t)
        cols = [r[1] for r in cur.fetchall()]
        if not any("desc" in c.lower() or "label" in c.lower() or "name" in c.lower() for c in cols):
            continue
        dcol = next((c for c in cols if "desc" in c.lower()), None)
        lcol = next((c for c in cols if c.lower() in ("label", "name")), None)
        if not dcol:
            continue
        q = "SELECT rowid, %s FROM %s WHERE %s LIKE ?" % (dcol, t, dcol)
        cur.execute(q, ("%vanilla HUD%",))
        rows = cur.fetchall()
        for rid, _ in rows:
            if lcol:
                cur.execute("UPDATE %s SET %s=?, %s=? WHERE rowid=?" % (t, dcol, lcol), (DESC_ZH, NAME_ZH, rid))
            else:
                cur.execute("UPDATE %s SET %s=? WHERE rowid=?" % (t, dcol), (DESC_ZH, rid))
            print("3) %s.rowid=%s 已更新（表 %s）" % (t, rid, t))
        con.commit()
    con.close()
    print("   ✅ mod_headers.db 处理完成（表: %s）" % tabs)
