# -*- coding: utf-8 -*-
"""apply_cn_transmog.py -- HD2 Transmog 界面文本汉化（仅替换纯显示用字面量）。"""
import os, sys, io, shutil, hashlib
from hd2_patch import PatchFile, rewrite_last_entry, murmur64a
from luaparser import ast

MODS = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal", "mods")
PATCH = os.path.join(MODS, "HD2 Transmog (Foundation) 16633 0.1.5 2026-09-28T20-24Z 8MtblTk5q_AR931809", "Addon", "9ba626afa44a3aa3.patch_0")
DATA = os.path.join(os.environ.get("HD2_DATA", r"C:\SteamLibrary\steamapps\common\Helldivers 2\data"), "9ba626afa44a3aa3.patch_20")
BACKUP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backup")
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes", "apply_cn_transmog.txt")

REPL = [
    ("'CREATE VARIANT  '", "'创建变体  '"),
    ("'Choose a look'", "'选择外观'"),
    ("'Choose base stats'", "'选择基础属性'"),
    ("'Choose stats'", "'选择属性'"),
    ("'Choose a passive'", "'选择被动'"),
    ("'CUSTOM VARIANT'", "'自订变体'"),
    ("'Saved variant'", "'已保存变体'"),
    ("'ARMOR RATING'", "'护甲值'"),
    ("'STAMINA REGEN'", "'耐力回复'"),
    ("'BASE STATS'", "'基础属性'"),
    ("'Not selected'", "'未选择'"),
    ("'Create saves this variant. Your equipped armor stays unchanged.'", "'创建即保存该变体；你当前装备的护甲不会改变。'"),
    ("'Choose an owned thumbnail to use its look.'", "'选择已拥有的缩略图以使用其外观。'"),
    ("'Choose owned armor to use its look and base stats.'", "'选择已拥有的护甲以使用其外观与基础属性。'"),
    ("'Choose a saved variant.'", "'选择已保存的变体。'"),
    ("'Choose another card or + to create a variant.'", "'选择其他卡片，或点 + 创建变体。'"),
    ("'Create variant'", "'创建变体'"),
    ("'Saving...'", "'保存中…'"),
    ("'New variant'", "'新变体'"),
    ("'Custom Variant '", "'自订变体 '"),
    ("'Variant'", "'变体'"),
    ("'STATS'", "'属性'"),
    ("'PASSIVE'", "'被动'"),
    ("'LOOK'", "'外观'"),
    ("'Back'", "'返回'"),
    ("'Cancel'", "'取消'"),
    ("'Create'", "'创建'"),
    ("'SPEED'", "'速度'"),
]

buf = io.StringIO()
pf = PatchFile.load(PATCH)
print("patch:", PATCH, file=buf)
for e in pf.entries:
    print("  ", e, file=buf)
assert pf.count == 1, "预期单 entry"
lua = pf.text(-1)
assert "创建变体" not in lua, "已经汉化过，先回滚"
ast.parse(lua.replace("\x00", ""))
print("原始 Lua 语法校验 OK (%d 字符)" % len(lua), file=buf)

new = lua
total = 0
for old, zh in REPL:
    n = new.count(old)
    if n == 0:
        print("  [跳过] 未找到: %s" % old, file=buf)
        continue
    new = new.replace(old, zh)
    total += n
    print("  替换 %-70s x%d" % (old, n), file=buf)
assert "\x00" not in new, "出现 NUL"
ast.parse(new.replace("\x00", ""))
print("汉化后 Lua 语法校验 OK (%d -> %d 字符, 共替换 %d 处)" % (len(lua), len(new), total), file=buf)

payload = new.encode("utf-8")
out = rewrite_last_entry(pf.raw, payload)
PatchFile(out, "new")
print("新 patch 结构校验 OK: %d 字节" % len(out), file=buf)

rel = os.path.relpath(PATCH, MODS)
dst = os.path.join(BACKUP, rel)
os.makedirs(os.path.dirname(dst), exist_ok=True)
if not os.path.exists(dst):
    shutil.copy2(PATCH, dst); print("已备份:", dst, file=buf)
with open(PATCH, "wb") as fh: fh.write(out)
print("已写入 mods:", PATCH, file=buf)

# 同步 data 副本
if os.path.exists(DATA):
    hb = hashlib.sha256(open(dst, "rb").read()).hexdigest()
    hd = hashlib.sha256(open(DATA, "rb").read()).hexdigest()
    print("data 副本与原文件一致:", hb == hd, file=buf)
    if hb == hd:
        shutil.copy2(PATCH, DATA)
        print("已同步:", DATA, os.path.getsize(DATA), file=buf)
    else:
        print("!! data 副本不一致，未同步", file=buf)
open(LOG, "w", encoding="utf-8").write(buf.getvalue())
print("DONE")
