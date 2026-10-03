# -*- coding: utf-8 -*-
"""build_pack.py -- 生成「独立汉化包」：不修改任何原模组文件。

独立包内容（一个 patch 文件的 3 个 entry）：
  entry0: mods/gnh_cn/zh_hans      -> 运行时包装 ModOptionsMenu 的注册 API（含 110 条词表）
  entry1: mods/hd2transmog/foundation -> Transmog 的汉化副本（覆盖式，需随上游更新重跑）
  entry2: mods/gnh_cn/readme       -> 说明文本
"""
import os, sys, io, shutil, hashlib, datetime
from cn_strings import CN
from hd2_patch import PatchFile, murmur64a, p32, p64, align8, u32, u64

MODS = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal", "mods")
BACKUP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backup")
PACK_NAME = "GNH-Chinese-Simplified-Pack"
PACK_DIR = os.path.join(MODS, PACK_NAME)
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes", "build_pack.txt")
TEMPLATE = os.path.join(MODS, "Vanilla Plus Megapack Rows V36 zh-Hans zh-Hant CN 16627 36 2026-10-01T05-16Z UR0syXwpP_AR640294",
                        "options", "ChineseTranslation", "9ba626afa44a3aa3.patch_0")
TM_PATCH = os.path.join(MODS, "HD2 Transmog (Foundation) 16633 0.1.5 2026-09-28T20-24Z 8MtblTk5q_AR931809", "Addon", "9ba626afa44a3aa3.patch_0")
MENU_PATCH = os.path.join(MODS, "Vanilla Plus Megapack Rows V36 zh-Hans zh-Hant CN 16627 36 2026-10-01T05-16Z UR0syXwpP_AR640294",
                          "options", "ModOptionsMenu", "9ba626afa44a3aa3.patch_0")
buf = io.StringIO(); W = lambda *a: print(*a, file=buf)

def lua_str(s):
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n") + "'"

# ---------- entry0: 运行时包装 ----------
lines = []
lines.append("-- HD2-Addon: mods/gnh_cn/zh_hans")
lines.append("-- GNH 简体中文汉化包（独立 mod，不修改任何原模组文件）")
lines.append("-- 原理：在 ModOptionsMenu 就绪的那一帧接管它的公开注册 API，把各模组注册进来的")
lines.append("-- 英文界面文本（选项名/说明/模组名/选项值）换成简体中文。")
lines.append("-- 只做浅拷贝，绝不改动调用方传入的表；带 pcall 兜底，任何异常都不影响原模组。")
lines.append("-- 制作：大赢经直插白皮赢道 (GNH-CN-CYS)")
lines.append("")
lines.append("local GNH_CN = {")
for en, zh in CN.items():
    lines.append("    [%s] = %s," % (lua_str(en), lua_str(zh)))
lines.append("}")
lines.append("")
lines.append("local GNH_TAG = 'GNH-CN-PACK'")
lines.append("local log_file")
lines.append("do")
lines.append("    local loader = rawget(_G, 'CowboyBingusModLoader')")
lines.append("    if loader and type(loader.open_log) == 'function' then")
lines.append("        local ok, f = pcall(loader.open_log, 'GNHChinesePack.log')")
lines.append("        if ok then log_file = f end")
lines.append("    end")
lines.append("end")
lines.append("local function log(msg)")
lines.append("    -- 两个通道都写：游戏控制台 + 独立日志文件，便于用户与我排查")
lines.append("    pcall(print, '[' .. GNH_TAG .. '] ' .. msg)")
lines.append("    if log_file then pcall(function() log_file:write(msg .. '\\n'); log_file:flush() end) end")
lines.append("end")
lines.append("")
lines.append("-- 词表命中即替换；只做浅拷贝，不改动调用方传入的表（对方可能是只读表或共用表）")
lines.append("local function translate_spec(spec)")
lines.append("    if type(spec) ~= 'table' then return spec end")
lines.append("    local out = {}")
lines.append("    for k, v in pairs(spec) do out[k] = v end")
lines.append("    if out.type == nil or out.label == nil then return spec end")
lines.append("    if type(out.label) == 'string' then out.label = GNH_CN[out.label] or out.label end")
lines.append("    if type(out.description) == 'string' then out.description = GNH_CN[out.description] or out.description end")
lines.append("    if type(out.mod) == 'string' then out.mod = GNH_CN[out.mod] or out.mod end")
lines.append("    local choices = out.choices")
lines.append("    if type(choices) == 'table' then")
lines.append("        local replaced = {}")
lines.append("        for i = 1, #choices do")
lines.append("            local c = choices[i]")
lines.append("            replaced[i] = (type(c) == 'string' and GNH_CN[c]) or c")
lines.append("        end")
lines.append("        out.choices = replaced")
lines.append("    end")
lines.append("    return out")
lines.append("end")
lines.append("")
lines.append("local hooked, hits = false, 0")
lines.append("-- 幂等：无论被加载几次，只接管一次")
lines.append("local function try_hook()")
lines.append("    if hooked then return true end")
lines.append("    local host = rawget(_G, 'ModOptionsMenu')")
lines.append("    if type(host) ~= 'table' or type(host.register_option) ~= 'function' then return false end")
lines.append("    local real_register = host.register_option")
lines.append("    host.register_option = function(id, spec)")
lines.append("        local ok, translated = pcall(translate_spec, spec)")
lines.append("        if not ok or type(translated) ~= 'table' then translated = spec end")
lines.append("        hits = hits + 1")
lines.append("        if hits <= 8 then")
lines.append("            log('汉化命中 #' .. hits .. ': ' .. tostring(id))")
lines.append("        end")
lines.append("        return real_register(id, translated)")
lines.append("    end")
lines.append("    hooked = true")
lines.append("    log('已接管 ModOptionsMenu.register_option（词表 ' .. tostring(#GNH_CN) .. ' 条）')")
lines.append("    return true")
lines.append("end")
lines.append("")
lines.append("if rawget(_G, 'GNH_CN_PACK_LOADED') then")
lines.append("    log('检测到重复加载，本次跳过')")
lines.append("    return")
lines.append("end")
lines.append("rawset(_G, 'GNH_CN_PACK_LOADED', true)")
lines.append("")
lines.append("if try_hook() then")
lines.append("    -- 加载时 ModOptionsMenu 已就绪（本包排在它之后加载），无需每帧轮询")
lines.append("else")
lines.append("    -- 否则接管主循环，在 ModOptionsMenu 出现的那一帧抢先接管，")
lines.append("    -- 必须早于各模组的注册（它们也在 update 里检查 host）")
lines.append("    local base_update = rawget(_G, 'update')")
lines.append("    local skipped = 0")
lines.append("    rawset(_G, 'update', function(...)")
lines.append("        if not hooked then")
lines.append("            if not try_hook() then")
lines.append("                skipped = skipped + 1")
lines.append("                if skipped == 1 or skipped % 600 == 0 then")
lines.append("                    log('等待 ModOptionsMenu 就绪…（已等待 ' .. skipped .. ' 帧）')")
lines.append("                end")
lines.append("            end")
lines.append("        end")
lines.append("        if type(base_update) == 'function' then return base_update(...) end")
lines.append("    end)")
lines.append("end")
ENTRY0 = "\n".join(lines) + "\n"

# ---------- entry1: Transmog 汉化副本 ----------
TM_REPL = [
    ("'CREATE VARIANT  '", "'创建变体  '"), ("'Choose a look'", "'选择外观'"),
    ("'Choose base stats'", "'选择基础属性'"), ("'Choose stats'", "'选择属性'"),
    ("'Choose a passive'", "'选择被动'"), ("'CUSTOM VARIANT'", "'自订变体'"),
    ("'Saved variant'", "'已保存变体'"), ("'ARMOR RATING'", "'护甲值'"),
    ("'STAMINA REGEN'", "'耐力回复'"), ("'BASE STATS'", "'基础属性'"),
    ("'Not selected'", "'未选择'"),
    ("'Create saves this variant. Your equipped armor stays unchanged.'", "'创建即保存该变体；你当前装备的护甲不会改变。'"),
    ("'Choose an owned thumbnail to use its look.'", "'选择已拥有的缩略图以使用其外观。'"),
    ("'Choose owned armor to use its look and base stats.'", "'选择已拥有的护甲以使用其外观与基础属性。'"),
    ("'Choose a saved variant.'", "'选择已保存的变体。'"),
    ("'Choose another card or + to create a variant.'", "'选择其他卡片，或点 + 创建变体。'"),
    ("'Create variant'", "'创建变体'"), ("'Saving...'", "'保存中…'"), ("'New variant'", "'新变体'"),
    ("'Custom Variant '", "'自订变体 '"), ("'Variant'", "'变体'"), ("'STATS'", "'属性'"),
    ("'PASSIVE'", "'被动'"), ("'LOOK'", "'外观'"), ("'Back'", "'返回'"), ("'Cancel'", "'取消'"),
    ("'Create'", "'创建'"), ("'SPEED'", "'速度'"), ("'Remove variant'", "'移除变体'"),
    ("section={title='Custom Variant'", "section={title='自订变体'"),
]
def make_transmog():
    """从备份里的原版 Transmog Lua 生成汉化副本（始终基于原版，不会被反复替换污染）。"""
    bk = os.path.join(BACKUP, os.path.relpath(TM_PATCH, MODS))
    src = bk if os.path.exists(bk) else TM_PATCH
    pf = PatchFile.load(src)
    lua = pf.text(-1)
    total = 0
    for old, zh in TM_REPL:
        n = lua.count(old)
        if n: lua = lua.replace(old, zh); total += n
    W("  Transmog 副本：基于 %s 生成，替换 %d 处" % ("备份原版" if bk == src else "当前文件", total))
    return lua

ENTRY1 = make_transmog()
ENTRY2 = ("-- HD2-Addon: mods/gnh_cn/readme\n"
          "-- GNH 简体中文汉化包：把 ModOptionsMenu 里未自带翻译键的模组界面文本换成简体中文。\n"
          "-- 本包不修改任何原模组文件；删除本 mod 即可完全还原。\n"
          "-- 制作：大赢经直插白皮赢杠 (GNH-CN-CYS)\n".replace("白皮赢杠", "白皮赢道"))

# ---------- 用模板重建 patch ----------
pf = PatchFile.load(TEMPLATE)
W("模板: %s（%d entry, %d 字节）" % (os.path.basename(os.path.dirname(TEMPLATE)), pf.count, len(pf.raw)))
new_entries = [("mods/gnh_cn/zh_hans", ENTRY0), ("mods/hd2transmog/foundation", ENTRY1), ("mods/gnh_cn/readme", ENTRY2)]
head_len = 0xC8 + 80 * (len(new_entries) - 1)
blob = bytearray(pf.raw[:head_len])
for i, (path, text) in enumerate(new_entries):
    payload = text.encode("utf-8")
    rec = len(blob)
    blob += p32(len(payload)) + p32(2) + payload
    blob += b"\x00" * (align8(len(payload)) - len(payload))
    blob[0x68 + 80 * i:0x70 + 80 * i] = p64(murmur64a(path.encode()))
    blob[0x78 + 80 * i:0x80 + 80 * i] = p64(rec)
    blob[0xA0 + 80 * i:0xA8 + 80 * i] = p64(len(payload) + 8)
blob[0x20:0x24] = p32(len(blob))
out_path = os.path.join(PACK_DIR, "Addon", "9ba626afa44a3aa3.patch_0")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "wb") as fh: fh.write(blob)
check = PatchFile.load(out_path)
W("生成: %s (%d 字节, %d entry)" % (out_path, len(blob), check.count))
for e in check.entries:
    ok = murmur64a(e.path_comment.encode()) == e.res_id if e.path_comment else False
    W("   entry%d type=%d len=%-8d id匹配=%s path=%s" % (e.index, e.type, e.length, ok, e.path_comment))
open(LOG, "w", encoding="utf-8").write(buf.getvalue())
print("PACK BUILT")
