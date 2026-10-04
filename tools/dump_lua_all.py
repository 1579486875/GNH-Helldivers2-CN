# -*- coding: utf-8 -*-
"""dump_lua_all.py -- 把模组库里所有 patch 的 Lua 源 dump 到 _scratch/hd2/lua_dump/，供静态核对。"""
import os, json, sys
sys.path.insert(0, r"E:\TAML\_scratch\hd2")
from hd2_patch import PatchFile

MODS = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal", "mods")
OUT = r"E:\TAML\_scratch\hd2\lua_dump"
SKIP = {"GNH-Chinese-Simplified-Pack", "GNH-Transmog-CN-Addon",
        "GNH-Transmog\u754c\u9762\u6c49\u5316-\u53ef\u9009\u5305_AR971368", "GNH\u7b80\u4f53\u4e2d\u6587\u6c49\u5316\u5305-Hellldivers2_AR395600"}

index = []
n_lua = n_patch = 0
for mod in sorted(os.listdir(MODS)):
    mdir = os.path.join(MODS, mod)
    if not os.path.isdir(mdir) or mod in SKIP:
        continue
    for dirpath, _, names in os.walk(mdir):
        for name in sorted(names):
            if ".patch_" not in name:
                continue
            p = os.path.join(dirpath, name)
            try:
                pf = PatchFile.load(p)
            except Exception as exc:
                index.append({"mod": mod, "file": p, "error": str(exc)})
                continue
            n_patch += 1
            for e in pf.entries:
                if e.type != 2:
                    continue
                n_lua += 1
                try:
                    text = e.data.decode("utf-8")
                except UnicodeDecodeError:
                    continue
                sub = os.path.join(OUT, mod)
                os.makedirs(sub, exist_ok=True)
                fn = "%s__e%02d.lua" % (os.path.relpath(dirpath, mdir).replace(os.sep, "_"), e.index)
                fn = "".join(ch for ch in fn if ch.isalnum() or ch in "._-") or "lua"
                if len(fn) > 140:
                    fn = fn[:120] + "__e%02d.lua" % e.index
                with open(os.path.join(sub, fn), "w", encoding="utf-8") as fh:
                    fh.write(text)
                index.append({"mod": mod, "rel": os.path.relpath(os.path.join(sub, fn), OUT),
                              "src": os.path.relpath(p, MODS), "entry": e.index,
                              "path_comment": e.path_comment, "chars": len(text),
                              "has_register": "register_option" in text})
os.makedirs(OUT, exist_ok=True)
json.dump(index, open(os.path.join(OUT, "_index.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("patch %d \u4e2a, lua %d \u4e2a; \u5176\u4e2d\u542b register_option \u7684 %d \u4e2a"
      % (n_patch, n_lua, sum(1 for i in index if i.get("has_register"))))
for i in index:
    if i.get("has_register"):
        print("  %-32s %s" % (i["mod"][:32], i["rel"]))
