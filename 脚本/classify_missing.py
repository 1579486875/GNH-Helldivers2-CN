# -*- coding: utf-8 -*-
"""classify_missing.py -- 把缺失文本分成「纯英文待翻译」「模组自带中文」「翻译键」三类。"""
import os, io, json, re
HD2 = r"E:\TAML\_scratch\hd2"
d = json.load(io.open(os.path.join(HD2, "_missing.json"), encoding="utf-8"))
CJK = re.compile(r"[\u4e00-\u9fff]")
print("%-32s %6s %6s %6s %6s" % ("模组", "总缺", "纯英文", "含中文", "键名"))
print("-" * 66)
need = {}
for lab, items in sorted(d.items(), key=lambda x: -len(x[1])):
    pure, hascn, keys = [], [], []
    for s, kind in items.items():
        if re.match(r"^[a-z_]+(\.[a-z_]+)+$", s):
            keys.append((s, kind)); continue
        (hascn if CJK.search(s) else pure).append((s, kind))
    print("%-32s %6d %6d %6d %6d" % (lab[:30], len(items), len(pure), len(hascn), len(keys)))
    if pure: need[lab] = pure
print("\n=== 真正需要翻译的纯英文文本（共 %d 条 / %d 个模组）===" %
      (sum(len(v) for v in need.values()), len(need)))
for lab, items in need.items():
    labs = [(s, k) for s, k in items if k == "label"]
    descs = [(s, k) for s, k in items if k == "desc"]
    chs = [(s, k) for s, k in items if k == "choice"]
    print("\n【%s】label %d / desc %d / choice %d" % (lab, len(labs), len(descs), len(chs)))
    for s, k in labs + chs:
        print("   %-6s %s" % (k, s[:100]))
    for s, k in descs[:4]:
        print("   desc   %s" % s[:110])
    if len(descs) > 4: print("   ... 其余 %d 条描述" % (len(descs) - 4))
