# -*- coding: utf-8 -*-
"""merge_cn_fixed.py -- 只取指定的词表变量，重新生成干净的 cn_strings.py。"""
import os
HD2 = r"E:\TAML\_scratch\hd2"
SPEC = [("cn_add.py", "CN_ADD"), ("cn_desc.py", "CN_DESC"), ("cn_fix.py", "CN_FIX"),
        ("cn_mods.py", "CN_MODS"), ("cn_mods2.py", "CN_MODS2"), ("cn_new.py", "CN_NEW"),
        ("cn_strings.py", "CN"),
        ("cn_ui3.py", "CN_UI3"), ("cn_ui4.py", "CN_UI4"), ("cn_ui5.py", "CN_UI5")]

CN = {}
for f, key in SPEC:
    ns = {}
    exec(open(os.path.join(HD2, f), encoding="utf-8-sig").read(), ns)
    d = ns.get(key)
    assert isinstance(d, dict), "%s 里没有 %s" % (f, key)
    for k, v in d.items():
        if not isinstance(k, str) or not isinstance(v, str): continue
        if k not in CN: CN[k] = v
bad = [k for k in CN if not isinstance(k, str)]
print("合并 %d 条（过滤掉非字符串键 %d 个）" % (len(CN), len(bad)))
src = os.path.join(HD2, "cn_strings.py")
with open(src, "w", encoding="utf-8") as fh:
    fh.write("# -*- coding: utf-8 -*-\n")
    fh.write('"""cn_strings.py —— 英文原文 -> 简体中文 词表（Mod Options Menu 选项文本 / 模组名 / 选项说明）。\n\n')
    fh.write("合并自 cn_add / cn_desc / cn_fix / cn_mods / cn_mods2 / cn_new，共 %d 条；\n" % len(CN))
    fh.write("键必须与模组注册时传入的字符串逐字符一致。\n\"\"\"\n\n")
    fh.write("CN = {\n")
    for k, v in CN.items():
        fh.write("    %r: %r,\n" % (k, v))
    fh.write("}\n")
# 语法自检
ns = {}
exec(open(src, encoding="utf-8-sig").read(), ns)
print("自检：重新加载成功，CN = %d 条" % len(ns["CN"]))
