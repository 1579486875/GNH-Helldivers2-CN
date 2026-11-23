# -*- coding: utf-8 -*-
"""apply_cn_menu.py -- 把简体中文词表注入 Mod Options Menu 的 Lua（patch 最后一个 entry）。"""
import os, sys, io, shutil
from cn_strings import CN
from hd2_patch import PatchFile, rewrite_last_entry, murmur64a
from luaparser import ast

MODS = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal", "mods")
PACK = os.path.join(MODS, "Vanilla Plus Megapack Rows V36 zh-Hans zh-Hant CN 16627 36 2026-10-01T05-16Z UR0syXwpP_AR640294")
MENU_PATCH = os.path.join(PACK, "options", "ModOptionsMenu", "9ba626afa44a3aa3.patch_0")
BACKUP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backup")
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes", "apply_cn_menu.txt")
MARK = "GNH_CN_TEXT_PACK"   # 幂等标记

buf = io.StringIO()

def lua_str(s):
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n") + "'"

pf = PatchFile.load(MENU_PATCH)
print("patch:", MENU_PATCH, file=buf)
for e in pf.entries:
    print("  ", e, file=buf)

lua = pf.text(-1)
assert MARK not in lua, "已经注入过，先回滚"
ast.parse(lua.replace("\x00", ""))
print("原始 Lua 语法校验: OK (%d 字符)" % len(lua), file=buf)

lines = []
lines.append("")
lines.append("-- ============================================================================")
lines.append("-- " + MARK + " / 简体中文界面文本包")
lines.append("-- 为未自带翻译键的模组（Aggro Counter、Armored Overhaul、Smarter Guard Dogs")
lines.append("-- & Sentries 等）按英文原文匹配汉化；删除本段即可还原英文。")
lines.append("-- 制作：大赢经直插白皮赢道 (GNH-CN-CYS)")
lines.append("-- ============================================================================")
lines.append("do")
lines.append("    local GNH_CN = {")
for en, zh in CN.items():
    lines.append("        [%s] = %s," % (lua_str(en), lua_str(zh)))
lines.append("    }")
lines.append("    local gnh_base_resolve = translation.resolve")
lines.append("    translation.resolve = function(value, limit)")
lines.append("        local text = gnh_base_resolve(value, limit)")
lines.append("        if text ~= nil then")
lines.append("            local cn = GNH_CN[text]")
lines.append("            if cn ~= nil then return cn end")
lines.append("        end")
lines.append("        return text")
lines.append("    end")
lines.append("    local gnh_count = 0")
lines.append("    for _ in pairs(GNH_CN) do gnh_count = gnh_count + 1 end")
lines.append("    note('GNH-CN 汉化: 已载入 ' .. gnh_count .. ' 条界面文本')")
lines.append("end")
inject = "\n".join(lines) + "\n"

new_lua = lua.rstrip("\x00") + inject
ast.parse(new_lua.replace("\x00", ""))
print("注入后 Lua 语法校验: OK (%d 字符, 新增 %d)" % (len(new_lua), len(new_lua) - len(lua)), file=buf)

payload = new_lua.encode("utf-8")
out = rewrite_last_entry(pf.raw, payload)
pf2 = PatchFile(out, MENU_PATCH + " (new)")
print("新 patch 结构校验: OK, %d 字节" % len(out), file=buf)
for e in pf2.entries:
    ok = "id OK" if (not e.path_comment or murmur64a(e.path_comment.encode()) == e.res_id) else "ID MISMATCH"
    print("  ", e, ok, file=buf)

# 备份（保留相对路径）
rel = os.path.relpath(MENU_PATCH, MODS)
dst = os.path.join(BACKUP, rel)
os.makedirs(os.path.dirname(dst), exist_ok=True)
if not os.path.exists(dst):
    shutil.copy2(MENU_PATCH, dst)
    print("已备份到:", dst, file=buf)
else:
    print("备份已存在:", dst, file=buf)

with open(MENU_PATCH, "wb") as fh:
    fh.write(out)
print("已写入:", MENU_PATCH, file=buf)

open(LOG, "w", encoding="utf-8").write(buf.getvalue())
print("DONE")
