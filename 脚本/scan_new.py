# -*- coding: utf-8 -*-
"""scan_new.py -- 列出模组库全部模组，标出 manifest 里仍有英文文本的（= 待汉化）。"""
import json, os, re, sqlite3
D = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal")
con = sqlite3.connect("file:%s?mode=ro" % os.path.join(D, "mod_headers.db").replace("\\", "/"), uri=True)
rows = con.execute("SELECT uuid, label, path FROM mods").fetchall()
con.close()
zh = re.compile(r"[\u4e00-\u9fff]")
state = json.load(open(os.path.join(D, "hd2a_data.json"), encoding="utf-8"))
enabled = {m["path"]: bool(m.get("enabled")) for m in state["modsList"]["default"]["mods"]}
print("模组库 %d 条记录\n" % len(rows))
todo = []
for uuid, label, path in sorted(rows, key=lambda r: r[1] or ""):
    mp = os.path.join(path, "manifest.json")
    if not os.path.isfile(mp):
        print("  [?] %-38s 无 manifest：%s" % ((label or "")[:38], path[-55:])); continue
    j = json.load(open(mp, encoding="utf-8"))
    miss = []
    for k in ("Name", "Description"):
        s = j.get(k) or ""
        if s.strip() and not zh.search(s): miss.append((k, s))
    def w(o):
        for x in o or []:
            for k in ("Name", "Description"):
                s = x.get(k) or ""
                if s.strip() and not zh.search(s): miss.append((k, s))
            w(x.get("SubOptions"))
    w(j.get("Options"))
    tag = "启用" if enabled.get(path) else "未启用"
    flag = "★待汉化" if miss else "  已汉化"
    print("  %s [%s] %-36s 待译 %d 条" % (flag, tag, (label or "")[:36], len(miss)))
    if miss: todo.append({"label": label, "path": path, "miss": miss})
print("\n需要汉化的模组：%d 个" % len(todo))
json.dump(todo, open("_todo.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print()
for m in todo:
    print("=== %s ===" % m["label"][:50])
    for k, s in m["miss"]:
        print("   [%s] %s" % (k, s.replace("\n", " ⏎ ")[:150]))
