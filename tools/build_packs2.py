# -*- coding: utf-8 -*-
"""build_packs2.py -- 重构为两个包：
   A) GNH-Chinese-Simplified-Pack   —— 零冲突：只提供全新资源 mods/gnh_cn/*，运行时接管 ModOptionsMenu
   B) GNH-Transmog-CN-Addon         —— 可选：覆盖式汉化 Transmog 界面（与 HD2 Transmog 有覆盖关系）
"""
import os, sys, io, json, uuid, shutil, hashlib
sys.path.insert(0, r"E:\TAML\_scratch\hd2")
from cn_strings import CN
from hd2_patch import PatchFile, murmur64a, p32, p64, align8

MODS = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal", "mods")
BACKUP = r"E:\TAML\_scratch\hd2\backup"
DATA = r"C:\SteamLibrary\steamapps\common\Helldivers 2\data"
LOG = r"E:\TAML\_scratch\hd2\notes\build_packs2.txt"
PACK_A = os.path.join(MODS, "GNH-Chinese-Simplified-Pack")
PACK_B = os.path.join(MODS, "GNH-Transmog-CN-Addon")
TEMPLATE = os.path.join(MODS, "Vanilla Plus Megapack Rows V36 zh-Hans zh-Hant CN 16627 36 2026-10-01T05-16Z UR0syXwpP_AR640294",
                        "options", "ChineseTranslation", "9ba626afa44a3aa3.patch_0")
import glob as _glob
_tm = sorted(_glob.glob(os.path.join(MODS, "HD2 Transmog*", "Addon", "9ba626afa44a3aa3.patch_0")),
             key=os.path.getmtime)
TM_PATCH = _tm[-1] if _tm else os.path.join(MODS, "HD2 Transmog (Foundation) 16633 0.1.5 2026-09-28T20-24Z 8MtblTk5q_AR931809", "Addon", "9ba626afa44a3aa3.patch_0")
buf = io.StringIO(); W = lambda *a: print(*a, file=buf)

def lua_str(s):
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n") + "'"

def build_runtime_lua():
    L = []
    L += ["-- HD2-Addon: mods/gnh_cn/zh_hans",
          "-- GNH 简体中文汉化包 —— 零冲突实现：只提供本模组自己的资源，",
          "-- 不覆盖任何其他模组的文件；用运行时接管的方式把 ModOptionsMenu 里的英文界面文本换成中文。",
          "-- 制作：大赢经直插白皮赢道 (GNH-CN-CYS)", ""]
    L += ["local GNH_CN = {"]
    for en, zh in CN.items():
        L.append("    [%s] = %s," % (lua_str(en), lua_str(zh)))
    L += ["}", "",
          "local GNH_TAG = 'GNH-CN-PACK'",
          "local log_file",
          "do",
          "    local loader = rawget(_G, 'CowboyBingusModLoader')",
          "    if loader and type(loader.open_log) == 'function' then",
          "        local ok, f = pcall(loader.open_log, 'GNHChinesePack.log')",
          "        if ok then log_file = f end",
          "    end",
          "end",
          "local function log(msg)",
          "    pcall(print, '[' .. GNH_TAG .. '] ' .. msg)",
          "    if log_file then pcall(function() log_file:write(msg .. '\\n'); log_file:flush() end) end",
          "end", "",
          "-- 只做浅拷贝再翻译：绝不改动调用方传入的表（对方可能是只读表或共用表）",
          "local function translate_spec(spec)",
          "    if type(spec) ~= 'table' then return spec end",
          "    local out = {}",
          "    for k, v in pairs(spec) do out[k] = v end",
          "    if out.type == nil or out.label == nil then return spec end",
          "    if type(out.label) == 'string' then out.label = GNH_CN[out.label] or out.label end",
          "    if type(out.description) == 'string' then out.description = GNH_CN[out.description] or out.description end",
          "    if type(out.mod) == 'string' then out.mod = GNH_CN[out.mod] or out.mod end",
          "    local choices = out.choices",
          "    if type(choices) == 'table' then",
          "        local replaced = {}",
          "        for i = 1, #choices do",
          "            local c = choices[i]",
          "            replaced[i] = (type(c) == 'string' and GNH_CN[c]) or c",
          "        end",
          "        out.choices = replaced",
          "    end",
          "    return out",
          "end", "",
          "local hooked, hits = false, 0",
          "local function try_hook()",
          "    if hooked then return true end",
          "    local host = rawget(_G, 'ModOptionsMenu')",
          "    if type(host) ~= 'table' or type(host.register_option) ~= 'function' then return false end",
          "    local real_register = host.register_option",
          "    host.register_option = function(id, spec)",
          "        local ok, translated = pcall(translate_spec, spec)",
          "        if not ok or type(translated) ~= 'table' then translated = spec end",
          "        hits = hits + 1",
          "        if hits <= 8 then log('汉化命中 #' .. hits .. ': ' .. tostring(id)) end",
          "        return real_register(id, translated)",
          "    end",
          "    hooked = true",
          "    log('已接管 ModOptionsMenu.register_option（词表 ' .. tostring(#GNH_CN) .. ' 条）')",
          "    return true",
          "end", "",
          "if rawget(_G, 'GNH_CN_PACK_LOADED') then log('重复加载，本次跳过'); return end",
          "rawset(_G, 'GNH_CN_PACK_LOADED', true)", "",
          "if try_hook() then",
          "    log('ModOptionsMenu 已就绪，直接接管完成')",
          "else",
          "    -- 兜底：与各模组同样的做法，接管主循环，在 ModOptionsMenu 出现的那一帧抢先接管",
          "    local base_update = rawget(_G, 'update')",
          "    local waited = 0",
          "    rawset(_G, 'update', function(...)",
          "        if not hooked then",
          "            if not try_hook() then",
          "                waited = waited + 1",
          "                if waited == 1 or waited % 900 == 0 then log('等待 ModOptionsMenu 就绪…（已等 ' .. waited .. ' 帧）') end",
          "            end",
          "        end",
          "        if type(base_update) == 'function' then return base_update(...) end",
          "    end)",
          "end"]
    return "\n".join(L) + "\n"

def build_transmog_lua():
    # 优先用模组库里的"当前版本"（更新后自动跟随）；备份仅作兜底
    bk = os.path.join(BACKUP, os.path.relpath(TM_PATCH, MODS))
    src = TM_PATCH if os.path.exists(TM_PATCH) else bk
    lua = PatchFile.load(src).text(-1)
    REPL = [("'CREATE VARIANT  '", "'创建变体  '"), ("'Choose a look'", "'选择外观'"),
        ("'Choose base stats'", "'选择基础属性'"), ("'Choose stats'", "'选择属性'"),
        ("'Choose a passive'", "'选择被动'"), ("'CUSTOM VARIANT'", "'自订变体'"),
        ("'Saved variant'", "'已保存变体'"), ("'ARMOR RATING'", "'护甲值'"), ("'STAMINA REGEN'", "'耐力回复'"),
        ("'BASE STATS'", "'基础属性'"), ("'Not selected'", "'未选择'"),
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
        # —— 第二轮补齐：扫描原始文件后发现的漏项 ——
        ("'Saved look'", "'已保存外观'"),
        ("'Select to review the full passive.'", "'选择可查看完整被动说明。'"),
        ("'A Select   B Back   Y Cancel'", "'A 选择   B 返回   Y 取消'"),
        ("'D-pad / stick Move    LB / RB Page'", "'方向键/摇杆 移动    LB / RB 翻页'"),
        ("'Passive bonuses are excluded.'", "'不含被动加成。'"),
        ("'Equipped'", "'已装备'"),
        ("'Save variant'", "'保存变体'"),
        ("'Remove variant'", "'移除变体'"),
        ("'Reload'", "'重新加载'"),
        ("'Reset'", "'重置'"),
        ("'Duplicate'", "'复制'"),
        ("'Discard'", "'放弃'"),
        ("'Base stats'", "'基础属性'"),
        ("'Saved'", "'已保存'"),
        ("'Close'", "'关闭'"),
        ("'Look'", "'外观'"),
        ("'Perk'", "'被动'"),
        ("'New'", "'新建'"),
        ("'BASE'", "'基础'"),
        ("'PERK'", "'被动'"),
        ("'TOTAL'", "'合计'")]
    n = 0
    for a, b in REPL:
        c = lua.count(a)
        if c: lua = lua.replace(a, b); n += c
    return lua, n

def write_patch(entries, dest):
    tmpl = PatchFile.load(TEMPLATE)
    head_len = 0xC8 + 80 * (len(entries) - 1)
    blob = bytearray(tmpl.raw[:head_len])
    for i, (path, text) in enumerate(entries):
        payload = text.encode("utf-8")
        rec = len(blob)
        blob += p32(len(payload)) + p32(2) + payload
        blob += b"\x00" * (align8(len(payload)) - len(payload))
        blob[0x68 + 80 * i:0x70 + 80 * i] = p64(murmur64a(path.encode()))
        blob[0x78 + 80 * i:0x80 + 80 * i] = p64(rec)
        blob[0xA0 + 80 * i:0xA8 + 80 * i] = p64(len(payload) + 8)
    blob[0x20:0x24] = p32(len(blob))
    blob[0x08:0x0C] = p32(len(entries))      # entry 计数（u32）
    blob[0x58:0x60] = p64(len(entries))      # entry 计数（u64）
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as fh: fh.write(blob)
    return PatchFile.load(dest)

# ---------------- 包 A：零冲突 ----------------
runtime = build_runtime_lua()
readme = ("-- HD2-Addon: mods/gnh_cn/readme\n"
          "-- GNH 简体中文汉化包（零冲突版）\n"
          "-- 只提供本模组自己的资源，不覆盖任何其他模组的文件。\n"
          "-- 作用：把 ModOptionsMenu 里未自带翻译键的模组界面文本换成简体中文\n"
          "--       （Aggro Counter / Armored Overhaul / Smarter Guard Dogs & Sentries）。\n"
          "-- 建议放在模组列表末尾加载。删除本模组即可完全还原。\n"
          "-- 制作：大赢经直插白皮赢道 (GNH-CN-CYS)\n")
pfA = write_patch([("mods/gnh_cn/zh_hans", runtime), ("mods/gnh_cn/readme", readme)],
                  os.path.join(PACK_A, "Addon", "9ba626afa44a3aa3.patch_0"))
W("### 包 A：%s" % os.path.basename(PACK_A))
W("  patch %d 字节, %d entry" % (len(pfA.raw), pfA.count))
for e in pfA.entries:
    W("    entry%d len=%-7d id匹配=%s %s" % (e.index, e.length, murmur64a(e.path_comment.encode()) == e.res_id, e.path_comment))
json.dump({"Version": 1, "Guid": str(uuid.uuid4()), "Name": "GNH 简体中文汉化包",
    "Description": ("把 ModOptionsMenu 中未自带翻译键的模组界面文本换成简体中文（Aggro Counter 仇恨计数、"
                    "Armored Overhaul 装甲大修、Smarter Guard Dogs & Sentries 更聪明的护卫犬与哨戒炮，共 110 条）。"
                    "本模组只提供自己的资源、不覆盖任何其他模组的文件，因此不会与任何模组产生文件冲突；"
                    "采用运行时接管的方式生效，停用或删除即可完全还原。建议放在模组列表末尾。"),
    "Options": [{"Name": "简体中文汉化", "Description": "运行时接管界面文本并替换为中文", "Include": ["Addon"]}]},
    open(os.path.join(PACK_A, "manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
W("  manifest.json 已更新（零冲突说明）")

# ---------------- 包 B：Transmog 增强（覆盖式，可选） ----------------
tmlua, tmn = build_transmog_lua()
pfB = write_patch([("mods/hd2transmog/foundation", tmlua)],
                  os.path.join(PACK_B, "Addon", "9ba626afa44a3aa3.patch_0"))
W("")
W("### 包 B：%s" % os.path.basename(PACK_B))
W("  patch %d 字节, %d entry（替换 %d 处）" % (len(pfB.raw), pfB.count, tmn))
for e in pfB.entries:
    W("    entry%d len=%-8d id匹配=%s %s" % (e.index, e.length, murmur64a(e.path_comment.encode()) == e.res_id, e.path_comment))
json.dump({"Version": 1, "Guid": str(uuid.uuid4()), "Name": "GNH Transmog 界面汉化（可选）",
    "Description": ("把 HD2 Transmog 的装甲变体界面换成简体中文。"
                    "\n\n⚠ 在模组管理器里可能会显示冲突，这是正常现象：本包通过覆盖 "
                    "mods/hd2transmog/foundation 这一个游戏资源来汉化界面文本，因此会与 HD2 Transmog 显示 1 处文件冲突。"
                    "\n\n部署时请让本包排在 HD2 Transmog 之后（Arsenal 默认会把它放在末尾）。"
                    "如果只需要零冲突的汉化，请只启用「GNH 简体中文汉化包」。"),
    "Options": [{"Name": "Transmog 界面汉化", "Description": "覆盖式汉化，与 HD2 Transmog 有 1 处资源覆盖关系", "Include": ["Addon"]}]},
    open(os.path.join(PACK_B, "manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
W("  manifest.json 已写入（含冲突说明）")

# ---------------- 同步到游戏 data ----------------
W("")
W("### 部署到 data")
for n in sorted(os.listdir(DATA)):
    if n.startswith("9ba626afa44a3aa3.patch_"):
        p = os.path.join(DATA, n)
        if not os.path.isfile(p): continue
        try: dpf = PatchFile.load(p)
        except Exception: continue
        if any((e.path_comment or "").startswith("mods/gnh_cn") or e.path_comment == "mods/hd2transmog/foundation" and os.path.getsize(p) > 2090000 for e in dpf.entries):
            for suffix in ("", ".gpu_resources", ".stream"):
                q = p + suffix
                if os.path.exists(q): os.remove(q)
            W("  移除旧部署: %s（含伴生文件）" % n)
nums = [int(n.split("_")[-1]) for n in os.listdir(DATA) if n.startswith("9ba626afa44a3aa3.patch_") and n.split("_")[-1].isdigit()]
nxt = max(nums) + 1
dst = os.path.join(DATA, "9ba626afa44a3aa3.patch_%d" % nxt)
shutil.copy2(os.path.join(PACK_A, "Addon", "9ba626afa44a3aa3.patch_0"), dst)
for suffix in (".gpu_resources", ".stream"): open(dst + suffix, "wb").close()
W("  包 A 部署为 patch_%d (%d 字节)" % (nxt, os.path.getsize(dst)))
W("  包 B 未部署（可选，用户需要时另行启用）")
open(LOG, "w", encoding="utf-8").write(buf.getvalue())
print("ok")
