# -*- coding: utf-8 -*-
"""dump_runtime.py -- 把主包里真正的代码部分（词表之后的逻辑）单独打印出来，便于逐行审查。"""
import sys, os
sys.path.insert(0, r"E:\TAML\_scratch\hd2")
from hd2_patch import PatchFile
MODS = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal", "mods")
PK = os.path.join(MODS, "GNH-Chinese-Simplified-Pack", "Addon", "9ba626afa44a3aa3.patch_0")
src = PatchFile.load(PK).entries[0].data.decode("utf-8")
i = src.find("local GNH_TAG")
print("总字符 %d；词表部分 %d 字符；代码部分从第 %d 行开始"
      % (len(src), i, src[:i].count("\n") + 1))
code = src[i:]
lines = code.split("\n")
print("代码行数（含注释）%d，字符 %d" % (len(lines), len(code)))
print("=" * 78)
for n, l in enumerate(lines, 1):
    print("%4d| %s" % (n, l))
