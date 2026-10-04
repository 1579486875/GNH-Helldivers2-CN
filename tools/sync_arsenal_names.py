# -*- coding: utf-8 -*-
"""sync_arsenal_names.py -- 把词表同步进 Arsenal 的两处显示来源。

  * hd2a_data.json  —— 「配置」页显示的名称 / 简介 / 启用选项（导入时的快照）
  * mod_headers.db  —— 「模组库」页显示的 label
只改显示文本，绝不碰 path / include / enabled / uuid —— 那些是 Arsenal 用来找文件的。
"""
import os, io, json, re, sqlite3, shutil, sys
HD2 = r"E:\TAML\_scratch\hd2"
sys.path.insert(0, HD2)
from cn_strings import CN

LA = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal")
BK = os.path.join(HD2, "backup", "arsenal-db")
os.makedirs(BK, exist_ok=True)

def norm(s):
    return (s.replace("\u2019", "'").replace("\u2018", "'")
             .replace("\u201c", '"').replace("\u201d", '"').replace("\u2014", "-"))
NT = {norm(k): v for k, v in CN.items()}
def tr(s):
    if not isinstance(s, str) or not s.strip():
        return s
    if re.search(r"[\u4e00-\u9fff]", s):
        return s
    if s in CN:
        return CN[s]
    return NT.get(norm(s), s)

# ---------- 1) hd2a_data.json ----------
ST = os.path.join(LA, "hd2a_data.json")
shutil.copy2(ST, os.path.join(BK, "hd2a_data.json.before-newmods"))
d = json.load(io.open(ST, encoding="utf-8"))
hits = []
def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "mods" and isinstance(v, list):
                for m in v:
                    if not isinstance(m, dict):
                        continue
                    new_label, new_desc = tr(m.get("label")), tr(m.get("description"))
                    if new_label != m.get("label") or new_desc != m.get("description"):
                        hits.append((m.get("label"), new_label))
                        m["label"], m["description"] = new_label, new_desc
                    for op in m.get("options") or []:
                        if isinstance(op, dict):
                            for kk in ("name", "description"):
                                if kk in op:
                                    op[kk] = tr(op[kk])
                            for sub in op.get("suboptions") or []:
                                if isinstance(sub, dict):
                                    for kk in ("name", "description"):
                                        if kk in sub:
                                            sub[kk] = tr(sub[kk])
            else:
                walk(v)
    elif isinstance(o, list):
        for x in o:
            walk(x)
walk(d)
io.open(ST, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
json.load(io.open(ST, encoding="utf-8"))       # 复读校验
print("hd2a_data.json 更新 %d 条：" % len(hits))
for old, new in hits:
    print("   %-42r -> %r" % (old, new))

# ---------- 2) mod_headers.db ----------
DB = os.path.join(LA, "mod_headers.db")
for suffix in ("", "-wal", "-shm"):
    s = DB + suffix
    if os.path.exists(s):
        shutil.copy2(s, os.path.join(BK, "mod_headers.db" + suffix + ".before-newmods"))
con = sqlite3.connect(DB)
rows = con.execute("SELECT rowid, label FROM mods").fetchall()
n = 0
for rid, label in rows:
    new = tr(label)
    if new != label:
        con.execute("UPDATE mods SET label = ? WHERE rowid = ?", (new, rid))
        n += 1
        print("   数据库 label: %r -> %r" % (label, new))
con.commit()
left = con.execute("SELECT label FROM mods WHERE label GLOB '*[A-Za-z]*'").fetchall()
con.close()
print("mod_headers.db 更新 %d 条；仍含拉丁字母的 label 有 %d 个（专有名词属正常）" % (n, len(left)))
