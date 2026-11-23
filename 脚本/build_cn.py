# -*- coding: utf-8 -*-
"""build_cn.py -- 统一构建 HD2 汉化：从备份还原原始 patch -> 应用汉化 -> 校验 -> 写回 mods 与游戏 data。

汉化 A（ModOptionsMenu）：在 mod_options_menu 的 Lua 末尾追加中文词表 + 包装 translation.resolve
    - 上游结构保护：translation / translation.resolve / note 任一缺失都安静退出
    - 语言判断：游戏语言是中文才替换（语言读不到时按中文处理）
汉化 B（HD2 Transmog）：仅替换纯显示用字面量，保留用于比较的字符串
"""
import os, sys, io, shutil, hashlib
from cn_strings import CN
from hd2_patch import PatchFile, rewrite_last_entry, murmur64a
from luaparser import ast

MODS = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal", "mods")
BACKUP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backup")
GAMEDATA = os.environ.get("HD2_DATA", r"C:\SteamLibrary\steamapps\common\Helldivers 2\data")
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes", "build_cn.txt")
MARK = "GNH_CN_TEXT_PACK"

PACK = os.path.join(MODS, "Vanilla Plus Megapack Rows V36 zh-Hans zh-Hant CN 16627 36 2026-10-01T05-16Z UR0syXwpP_AR640294")
MENU_PATCH = os.path.join(PACK, "options", "ModOptionsMenu", "9ba626afa44a3aa3.patch_0")
TM_PATCH = os.path.join(MODS, "HD2 Transmog (Foundation) 16633 0.1.5 2026-09-28T20-24Z 8MtblTk5q_AR931809", "Addon", "9ba626afa44a3aa3.patch_0")

# Transmog 显示文本替换（长串在前，避免子串误伤）
TM_REPL = [
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
    ("'Remove variant'", "'移除变体'"),
    ("section={title='Custom Variant'", "section={title='自订变体'"),
]

buf = io.StringIO()


def lua_str(s):
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n") + "'"


def restore(patch, backup):
    """把 mods 里的 patch 还原为备份中的原始内容。"""
    if os.path.exists(backup):
        shutil.copy2(backup, patch)
        return True
    return False


def build_menu_lua(lua):
    """生成注入代码。整段包在一个立即执行函数里：主 chunk 的 local 数已达上限（200），
    顶层绝不能再新增 local —— 否则整块 Lua 编译失败（已实测）。"""
    lines = ["",
             "-- ============================================================================",
             "-- " + MARK + " / 简体中文界面文本包（GNH-CN-CYS）",
             "-- 为未自带翻译键的模组（Aggro Counter、Armored Overhaul、Smarter Guard Dogs",
             "-- & Sentries 等）按英文原文匹配汉化。",
             "-- 结构保护：translation.resolve 不存在时安静退出；",
             "-- 本地化定位：本包是简体中文汉化包，命中词表即替换，不做语言判断。",
             "-- 整段用立即执行函数包裹：主 chunk 的 local 数已接近 200 上限，",
             "-- 顶层不再新增任何 local（否则整块 Lua 编译失败）。",
             "-- 删除本段即可还原英文。",
             "-- ============================================================================",
             "-- 下一行以分号开头是必需的：Lua 的换行不结束语句，若上一条语句是 note(...) 这类",
             "-- 函数调用，紧跟其后的 (function() 会被当成调用后缀，运行时报 attempt to call a nil value。",
             ";(function()",
             "    if rawget(_G, 'GNH_CN_TEXT_PACK') then return end",
             "    rawset(_G, 'GNH_CN_TEXT_PACK', true)",
             "    local GNH_CN = {"]
    for en, zh in CN.items():
        lines.append("        [%s] = %s," % (lua_str(en), lua_str(zh)))
    lines += [
        "    }",
        "    if type(translation) ~= 'table' or type(translation.resolve) ~= 'function' then return end",
        "    -- 不再做语言判断：ModOptionsMenu 的语言观测发生在各模组注册选项之后，",
        "    -- 注册那一刻只能读到默认/Steam 语言，中文界面会被误判成英文而漏翻。",
        "    -- 本包定位是简体中文汉化包，因此无条件把命中的界面文本替换为中文。",
        "    local gnh_calls, gnh_hits = 0, 0",
        "    local base_resolve = translation.resolve",
        "    translation.resolve = function(value, limit)",
        "        gnh_calls = gnh_calls + 1",
        "        local text = base_resolve(value, limit)",
        "        if text == nil then return nil end",
        "        local cn = GNH_CN[text]",
        "        if cn ~= nil then",
        "            gnh_hits = gnh_hits + 1",
        "            if type(note) == 'function' and gnh_hits <= 8 then",
        "                note('GNH-CN 汉化命中: ' .. text .. ' -> ' .. cn)",
        "            end",
        "            return cn",
        "        end",
        "        return text",
        "    end",
        "    if type(note) == 'function' then",
        "        note('GNH-CN: 已接管文本解析入口 translation.resolve')",
        "    end",
        "    -- 第二道保险：chunk 末尾时 _G.ModOptionsMenu 已就绪，直接把注册进来的 spec",
        "    -- 就地换成中文。这样即便某个版本不再经过 translation.resolve，选项名与说明仍是中文。",
        "    local host = rawget(_G, 'ModOptionsMenu')",
        "    if type(host) == 'table' and type(host.register_option) == 'function' then",
        "        local real_register = host.register_option",
        "        -- 关键：只做浅拷贝，绝不就地改写调用方传入的表。",
        "        -- 对方可能给 spec 加只读元表，或让多个选项共用同一个表；就地赋值会抛错或污染。",
        "        local function translate_spec(spec)",
        "            if type(spec) ~= 'table' then return spec end",
        "            local out = {}",
        "            for k, v in pairs(spec) do out[k] = v end",
        "            if out.type == nil or out.label == nil then return spec end",
        "            if type(out.label) == 'string' then out.label = GNH_CN[out.label] or out.label end",
        "            if type(out.description) == 'string' then out.description = GNH_CN[out.description] or out.description end",
        "            if type(out.mod) == 'string' then out.mod = GNH_CN[out.mod] or out.mod end",
        "            local choices = out.choices",
        "            if type(choices) == 'table' then",
        "                local replaced = {}",
        "                for i = 1, #choices do",
        "                    local c = choices[i]",
        "                    replaced[i] = (type(c) == 'string' and GNH_CN[c]) or c",
        "                end",
        "                out.choices = replaced",
        "            end",
        "            return out",
        "        end",
        "        host.register_option = function(id, spec)",
        "            local ok, translated = pcall(translate_spec, spec)",
        "            if not ok or type(translated) ~= 'table' then translated = spec end",
        "            return real_register(id, translated)",
        "        end",
        "        if type(note) == 'function' then note('GNH-CN: 已接管 ModOptionsMenu.register_option（只读浅拷贝，不改动调用方的表）') end",
        "    else",
        "        if type(note) == 'function' then note('GNH-CN: 未找到 ModOptionsMenu API，仅使用文本解析入口') end",
        "    end",
        "    if type(note) == 'function' then",
        "        local count = 0",
        "        for _ in pairs(GNH_CN) do count = count + 1 end",
        "        note('GNH-CN: 简体中文界面文本包已载入 (' .. count .. ' 条)')",
        "    end",
        "end)()",
    ]
    return "\n".join(lines) + "\n"


def do_menu():
    backup = os.path.join(BACKUP, os.path.relpath(MENU_PATCH, MODS))
    print("=== A. ModOptionsMenu ===", file=buf)
    print("备份存在:", os.path.exists(backup), file=buf)
    restore(MENU_PATCH, backup)
    pf = PatchFile.load(MENU_PATCH)
    lua = pf.text(-1)
    assert MARK not in lua
    ast.parse(lua.replace("\x00", ""))
    new = lua.rstrip("\x00") + build_menu_lua(lua)
    ast.parse(new.replace("\x00", ""))
    out = rewrite_last_entry(pf.raw, new.encode("utf-8"))
    PatchFile(out, "new")
    with open(MENU_PATCH, "wb") as fh:
        fh.write(out)
    print("原始 %d -> 汉化 %d 字符；文件 %d -> %d 字节" % (len(lua), len(new), len(pf.raw), len(out)), file=buf)
    return MENU_PATCH, out


def do_transmog():
    backup = os.path.join(BACKUP, os.path.relpath(TM_PATCH, MODS))
    print("\n=== B. HD2 Transmog ===", file=buf)
    print("备份存在:", os.path.exists(backup), file=buf)
    restore(TM_PATCH, backup)
    pf = PatchFile.load(TM_PATCH)
    lua = pf.text(-1)
    ast.parse(lua.replace("\x00", ""))
    new, total, skipped = lua, 0, []
    for old, zh in TM_REPL:
        n = new.count(old)
        if n == 0:
            skipped.append(old); continue
        new = new.replace(old, zh)
        total += n
        print("  替换 %-72s x%d" % (old, n), file=buf)
    if skipped:
        print("  未匹配(已跳过):", skipped, file=buf)
    ast.parse(new.replace("\x00", ""))
    out = rewrite_last_entry(pf.raw, new.encode("utf-8"))
    PatchFile(out, "new")
    with open(TM_PATCH, "wb") as fh:
        fh.write(out)
    print("替换 %d 处；%d -> %d 字符；文件 %d -> %d 字节" % (total, len(lua), len(new), len(pf.raw), len(out)), file=buf)
    return TM_PATCH, out


def sync_data(mods_patch, path_marker):
    """把汉化后的 patch 同步到游戏 data 目录里的部署副本。"""
    for n in sorted(os.listdir(GAMEDATA)):
        if not n.startswith("9ba626afa44a3aa3.patch_") or ".gpu" in n or ".stream" in n:
            continue
        p = os.path.join(GAMEDATA, n)
        try:
            pf = PatchFile.load(p)
        except Exception:
            continue
        if any(e.path_comment == path_marker for e in pf.entries):
            shutil.copy2(mods_patch, p)
            print("  同步 data: %s (%d 字节)" % (n, os.path.getsize(p)), file=buf)
            return n
    print("  !! data 未找到对应副本:", path_marker, file=buf)
    return None


m1, _ = do_menu()
m2, _ = do_transmog()
print("\n=== 同步到游戏 data ===", file=buf)
sync_data(m1, "mods/cowboybingus/mod_options_menu")
sync_data(m2, "mods/hd2transmog/foundation")
open(LOG, "w", encoding="utf-8").write(buf.getvalue())
print("BUILD DONE")
