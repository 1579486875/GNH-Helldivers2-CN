# -*- coding: utf-8 -*-
"""sync_arsenal_from_manifest.py -- 用各模组 manifest 的最新内容覆盖 Arsenal 的 label / description。

与 sync_arsenal_names.py 的区别：
  那个是"翻译"（已含中文的会跳过，所以版本号永远不更新）；
  这个是"以 manifest 为准同步"，能跟上模组更新后的新版本号与新描述。
"""
import os, io, json, shutil, sqlite3, subprocess

LA = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal")
MODS = os.path.join(LA, "mods")
BK = r"E:\TAML\_scratch\hd2\backup\arsenal-db"
os.makedirs(BK, exist_ok=True)

def running():
    try:
        out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq HD2Arsenal.exe"],
                             capture_output=True, text=True, timeout=15).stdout
        return "HD2Arsenal" in out
    except Exception:
        return True
if running():
    print("Arsenal 正在运行 —— 请先完全退出（否则改动会被它覆盖）")
    raise SystemExit(1)

# 建索引：目录名 -> (Name, Description, options)
facts = {}
for d in os.listdir(MODS):
    mf = os.path.join(MODS, d, "manifest.json")
    if not os.path.isfile(mf):
        continue
    j = json.load(io.open(mf, encoding="utf-8-sig"))
    facts[d] = j

ST = os.path.join(LA, "hd2a_data.json")
shutil.copy2(ST, os.path.join(BK, "hd2a_data.json.before-manifest-sync"))
s = json.load(io.open(ST, encoding="utf-8"))
changed = []

def apply(m, where):
    d = os.path.basename(m.get("path") or "")
    j = facts.get(d)
    if not j:
        return
    newlabel = j.get("Name")
    newdesc = j.get("Description")
    if newlabel and m.get("label") != newlabel:
        changed.append("%s: %r -> %r" % (where, m.get("label"), newlabel))
        m["label"] = newlabel
    if isinstance(newdesc, str) and newdesc.strip() and m.get("description") != newdesc:
        m["description"] = newdesc
    # 选项名同步
    opts = {o.get("Name"): o for o in (j.get("Options") or [])}
    for op in m.get("options") or []:
        src = opts.get(op.get("name"))
        if not src:
            # 名字已被翻译过，用 include 匹配
            for cand in (j.get("Options") or []):
                if cand.get("Include") == op.get("include"):
                    src = cand
                    break
        if src:
            if src.get("Name"):
                op["name"] = src["Name"]
            if src.get("Description"):
                op["description"] = src["Description"]

for m in s["modsList"]["default"]["mods"]:
    apply(m, "配置")
for m in s.get("modsLibrary") or []:
    apply(m, "模组库")

io.open(ST, "w", encoding="utf-8").write(json.dumps(s, ensure_ascii=False, indent=2))
json.load(io.open(ST, encoding="utf-8"))
print("按 manifest 同步完成，%d 处名称被更新：" % len(changed))
for c in changed:
    print("   %s" % c)

con = sqlite3.connect(os.path.join(LA, "mod_headers.db"))
n = 0
for rid, label, path in con.execute("SELECT rowid, label, path FROM mods").fetchall():
    d = os.path.basename(path or "")
    j = facts.get(d)
    if j and j.get("Name") and j["Name"] != label:
        con.execute("UPDATE mods SET label = ? WHERE rowid = ?", (j["Name"], rid))
        n += 1
con.commit()
con.close()
print("数据库更新 %d 行" % n)
