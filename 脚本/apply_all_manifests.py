# -*- coding: utf-8 -*-
"""apply_all_manifests.py -- 把词表应用到"模组库"里全部 mod 的 manifest（不只启用的）。"""
import os, json, re, shutil, sqlite3, sys
HD2 = r"E:\TAML\_scratch\hd2"
BAK = os.path.join(HD2, "backup", "manifests-all")
os.makedirs(BAK, exist_ok=True)

T = {}
for f in ("cn_strings.py", "cn_add.py", "cn_desc.py", "cn_fix.py", "cn_mods.py", "cn_mods2.py", "cn_new.py"):
    ns = {}
    exec(open(os.path.join(HD2, f), encoding="utf-8-sig").read(), ns)
    for k, v in ns.items():
        if isinstance(v, dict): T.update(v)
def norm(s):
    return s.replace("\u2019","'").replace("\u2018","'").replace("\u201c",'"').replace("\u201d",'"').replace("\u2014","-")
NT = {norm(k): v for k, v in T.items()}
def tr(s):
    if not isinstance(s, str) or not s.strip(): return s
    if re.search(r"[\u4e00-\u9fff]", s): return s
    if s in T: return T[s]
    return NT.get(norm(s), s)

D = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal")
con = sqlite3.connect("file:%s?mode=ro" % os.path.join(D, "mod_headers.db").replace("\\", "/"), uri=True)
rows = con.execute("SELECT DISTINCT path FROM mods").fetchall()
con.close()

done = miss_mod = 0
for (path,) in rows:
    mp = os.path.join(path, "manifest.json")
    if not os.path.isfile(mp):
        miss_mod += 1; continue
    j = json.load(open(mp, encoding="utf-8"))
    before = json.dumps(j, ensure_ascii=False)
    bdir = os.path.join(BAK, re.sub(r'[\\/:*?"<>|]', "_", os.path.basename(path))[:50])
    try:
        os.makedirs(bdir, exist_ok=True)
        if not os.path.exists(os.path.join(bdir, "manifest.json")):
            shutil.copy2(mp, os.path.join(bdir, "manifest.json"))
    except OSError as e:
        print("  [跳过备份] %s: %s" % (os.path.basename(path)[:40], e))
    j["Name"] = tr(j.get("Name", ""))
    j["Description"] = tr(j.get("Description", ""))
    def w(o):
        for x in o or []:
            for k in ("Name", "Description"):
                if k in x: x[k] = tr(x[k])
            w(x.get("SubOptions"))
    w(j.get("Options"))
    if json.dumps(j, ensure_ascii=False) != before:
        json.dump(j, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        done += 1
        print("  已汉化:", os.path.basename(path)[:60])
print("\n共更新 %d 个 manifest；%d 个目录缺少 manifest.json（导入不完整或已失效）" % (done, miss_mod))
