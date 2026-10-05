# -*- coding: utf-8 -*-
"""wait_and_sync_arsenal.py -- 等 Arsenal 完全退出后，自动同步名称（含新版本号）与描述。"""
import os, io, json, time, subprocess, shutil, sqlite3, sys

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

print("等待 Arsenal 退出…（最长 60 分钟）", flush=True)
deadline = time.time() + 3600
while time.time() < deadline:
    if not running():
        time.sleep(3)
        if not running():
            break
    time.sleep(2)
else:
    print("超时：Arsenal 一直开着，未同步")
    raise SystemExit(0)
print("Arsenal 已退出，开始同步…\n", flush=True)

# 建 manifest 索引
facts = {}
for d in os.listdir(MODS):
    mf = os.path.join(MODS, d, "manifest.json")
    if os.path.isfile(mf):
        try:
            facts[d] = json.load(io.open(mf, encoding="utf-8-sig"))
        except Exception:
            pass

ST = os.path.join(LA, "hd2a_data.json")
shutil.copy2(ST, os.path.join(BK, "hd2a_data.json.before-final-sync"))
s = json.load(io.open(ST, encoding="utf-8"))
changed = []

def apply(m):
    d = os.path.basename(m.get("path") or "")
    j = facts.get(d)
    if not j:
        return
    nl, nd = j.get("Name"), j.get("Description")
    if nl and m.get("label") != nl:
        changed.append((m.get("label"), nl))
        m["label"] = nl
    if isinstance(nd, str) and nd.strip():
        m["description"] = nd
    for op in m.get("options") or []:
        for cand in (j.get("Options") or []):
            if cand.get("Include") == op.get("include") or cand.get("Name") == op.get("name"):
                if cand.get("Name"):
                    op["name"] = cand["Name"]
                if cand.get("Description"):
                    op["description"] = cand["Description"]
                break

for m in s["modsList"]["default"]["mods"]:
    apply(m)
for m in s.get("modsLibrary") or []:
    apply(m)

io.open(ST, "w", encoding="utf-8").write(json.dumps(s, ensure_ascii=False, indent=2))
json.load(io.open(ST, encoding="utf-8"))
print("配置页更新 %d 处：" % len(changed))
for a, b in changed:
    print("   %r -> %r" % (a, b))

con = sqlite3.connect(os.path.join(LA, "mod_headers.db"))
n = 0
for rid, label, path in con.execute("SELECT rowid, label, path FROM mods").fetchall():
    j = facts.get(os.path.basename(path or ""))
    if j and j.get("Name") and j["Name"] != label:
        con.execute("UPDATE mods SET label = ? WHERE rowid = ?", (j["Name"], rid))
        n += 1
con.commit()
con.close()
print("模组库页更新 %d 行" % n)

# 复核
s2 = json.load(io.open(ST, encoding="utf-8"))
print("\n=== 复核（前 12 个）===")
for m in s2["modsList"]["default"]["mods"][:12]:
    print("   %s" % m.get("label"))
print("\n完成 —— 可以重新打开 Arsenal 了。")
