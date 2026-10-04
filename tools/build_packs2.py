# -*- coding: utf-8 -*-
"""build_packs2.py -- 重构为两个包：
   A) GNH-Chinese-Simplified-Pack   —— 零冲突：只提供全新资源 mods/gnh_cn/*，运行时接管 ModOptionsMenu
   B) GNH-Transmog-CN-Addon         —— 可选：覆盖式汉化 Transmog 界面（与 HD2 Transmog 有覆盖关系）
"""
import os, sys, io, json, uuid, shutil, hashlib, re
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
buf = io.StringIO()


def W(*a):
    """同一条信息同时写进构建日志和屏幕，出问题时不必去翻日志文件。"""
    line = " ".join(str(x) for x in a)
    print(line)
    print(line, file=buf)


def entry_id_ok(e):
    """校验 entry 的资源 id 是否真的等于其路径的 murmur 哈希。

    路径来自 Lua 开头的 -- HD2-Addon: 注释行（这是工具链的约定）。
    万一将来漏写这行，这里返回一句提示而不是让整个构建崩掉。
    """
    if not e.path_comment:
        return "?（缺 -- HD2-Addon: 注释）"
    return murmur64a(e.path_comment.encode()) == e.res_id

def lua_str(s):
    """把一段普通文本变成安全的 Lua 单引号字符串字面量（转义反斜杠、单引号、回车、换行）。"""
    return ("'" + s.replace("\\", "\\\\").replace("'", "\\'")
            .replace("\r", "\\r").replace("\n", "\\n") + "'")

TEMPLATE_LUA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lua_src", "runtime_template.lua")


def build_runtime_lua():
    """把中文词表填进 Lua 模板，得到最终要打进 patch 的那份 Lua。

    分工：
      * lua_src/runtime_template.lua —— 真正干活的代码，带完整中文注释，可单独用 Lua 语法工具检查；
      * cn_strings.py               —— 英文→中文词表（由 merge_cn_fixed.py 从各 cn_*.py 合并而来）。
    本函数只做一件事：把词表生成成 Lua 表字面量，替换掉模板里的 --[[GNH_CN_TABLE]] 占位符。

    另外会自动补一份**全大写**的键：菜单显示"选项值"和"模组名"时会先把文字转成大写，
    没有大写键就匹配不上（例如 Show Badge 是选项名不用转，而 GUARD DOGS 是选项值要转）。
    """
    lines, seen = [], set()
    for en, zh in CN.items():
        if en in seen:
            continue
        seen.add(en)
        lines.append("    [%s] = %s," % (lua_str(en), lua_str(zh)))
        up = en.upper()
        if up != en and up not in seen and up not in CN:
            seen.add(up)
            lines.append("    [%s] = %s," % (lua_str(up), lua_str(zh)))

    with io.open(TEMPLATE_LUA, encoding="utf-8-sig") as fh:
        tpl = fh.read()
    if "--[[GNH_CN_TABLE]]" not in tpl:
        raise RuntimeError("模板 %s 里找不到词表占位符 --[[GNH_CN_TABLE]]" % TEMPLATE_LUA)
    text = tpl.replace("--[[GNH_CN_TABLE]]", "\n".join(lines))

    # 生成后立刻做一次语法自检：能编译才允许继续，防止把坏文件打进 patch。
    # （游戏用的是 LuaJIT，这里用 lupa 内置的 Lua 编译；两者语法在本文用到的范围内一致。）
    try:
        import lupa
    except ImportError:
        pass
    else:
        try:
            lupa.LuaRuntime().compile(text)
        except Exception as exc:
            raise RuntimeError("生成的 Lua 编译失败，已中止构建：%s" % exc)
    return text


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
        ("section={title='Custom Variant'", "section={title='Custom Variant'"),  # 保留：与 header.text=='Custom Variant' 成对
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
        ("'TOTAL'", "'合计'"),
        # —— 第三轮补齐（2026-10-05）：补齐剩余上屏文本 ——
        # 说明：section.title 与 header.text=='Custom Variant' 是同一份判定依据（区块识别），
        # 只把标题改中文会让识别失败，所以两者都保持英文，只替换真正上屏的那两处 text(...)。
        ("text('Custom Variant'", "text('自订变体'"),
        ("text('MODIFIED UNIQUE'", "text('已改造的独特外观'"),
        ("text('Default: '", "text('默认：'"),
        ("text('Now (temporary): '", "text('当前（临时）：'"),
        ("text('Modded '", "text('已改造 '"),
        ("'Name and create'", "'命名并创建'"),
        ("'Set the look'", "'设置外观'"),
        ("'D-pad / left stick: choose a look. A: select.'", "'方向键/左摇杆：选择一个外观。A：选定。'"),
        ("' saved'", "' 个已保存'"),
        ("' owned choices'", "' 个可选'"),
        # —— 第四轮补齐：变体编辑器的空状态提示（纯赋值，不参与任何判定）——
        ("'No variant selected'", "'未选择任何变体'")]
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
          "-- 作用：把 ModOptionsMenu / Mod Bindings Menu 里未自带翻译键的模组界面文本\n"
          "--       换成简体中文（选项名、选项值、选项说明、模组名、按键名）。\n"
          "-- 覆盖：Aggro Counter / Armored Overhaul / Smarter Guard Dogs & Sentries /\n"
          "--       Objective Tracker / HD2 Transmog / Better Lobby Management 等。\n"
          "-- 说明：已注册的选项会在接管时统一补翻，所以不受模组加载顺序影响。\n"
          "-- 建议放在模组列表末尾加载。删除本模组即可完全还原。\n"
          "-- 制作：大赢经直插白皮赢道 (GNH-CN-CYS)\n")
pfA = write_patch([("mods/gnh_cn/zh_hans", runtime), ("mods/gnh_cn/readme", readme)],
                  os.path.join(PACK_A, "Addon", "9ba626afa44a3aa3.patch_0"))
W("### 包 A：%s" % os.path.basename(PACK_A))
W("  patch %d 字节, %d entry" % (len(pfA.raw), pfA.count))
for e in pfA.entries:
    W("    entry%d len=%-7d id匹配=%s %s" % (e.index, e.length, entry_id_ok(e), e.path_comment))
json.dump({"Version": 1, "Guid": str(uuid.uuid4()), "Name": "GNH 简体中文汉化包",
    "Description": ("把 ModOptionsMenu 与 Mod Bindings Menu 里未自带翻译键的模组界面文本换成简体中文："
                    "选项名、选项值、选项说明、模组名、按键名。词表 565 组（含大写形式共 1074 条），"
                    "覆盖 Aggro Counter 仇恨计数、Armored Overhaul 装甲大修、"
                    "Smarter Guard Dogs & Sentries 更聪明的护卫犬与哨戒炮、Objective Tracker 任务目标追踪、"
                    "HD2 Transmog 幻化、Better Lobby Management 大厅管理等。"
                    "\n\n已注册的选项会在接管时统一补翻，因此不受模组加载顺序影响，也不会漏掉先于本包加载的模组。"
                    "\n\n本模组只提供自己的资源、不覆盖任何其他模组的文件，因此不会与任何模组产生文件冲突；"
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
    W("    entry%d len=%-8d id匹配=%s %s" % (e.index, e.length, entry_id_ok(e), e.path_comment))
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
zh_re = re.compile(r"[\u4e00-\u9fff]")

def our_kind(path):
    """只认本脚本自己的部署产物，绝不误删别人的 patch。

    包 A 的独有资源是 mods/gnh_cn/*；包 B 覆盖 mods/hd2transmog/foundation，
    而官方原版那份 foundation 里一个汉字都没有（实测 zh 计数 = 0），
    因此"含汉字"就能可靠地区分我们的汉化版与原版。
    """
    try:
        dpf = PatchFile.load(path)
    except Exception:
        return None
    for e in dpf.entries:
        pc = e.path_comment or ""
        if pc.startswith("mods/gnh_cn"):
            return "A"
        if pc == "mods/hd2transmog/foundation" and zh_re.search(e.data.decode("utf-8", "ignore")):
            return "B"
    return None

had_b = False
for n in sorted(os.listdir(DATA)):
    if not (n.startswith("9ba626afa44a3aa3.patch_") and n.split("_")[-1].isdigit()):
        continue
    p = os.path.join(DATA, n)
    if not os.path.isfile(p):
        continue
    kind = our_kind(p)
    if kind:
        for suffix in ("", ".gpu_resources", ".stream"):
            q = p + suffix
            if os.path.exists(q): os.remove(q)
        W("  移除本脚本的旧部署: %s（%s 包，含伴生文件）" % (n, kind))
        if kind == "B": had_b = True

nums = [int(n.split("_")[-1]) for n in os.listdir(DATA) if n.startswith("9ba626afa44a3aa3.patch_") and n.split("_")[-1].isdigit()]
nxt = max(nums) + 1
dst = os.path.join(DATA, "9ba626afa44a3aa3.patch_%d" % nxt)
shutil.copy2(os.path.join(PACK_A, "Addon", "9ba626afa44a3aa3.patch_0"), dst)
for suffix in (".gpu_resources", ".stream"): open(dst + suffix, "wb").close()
W("  包 A 部署为 patch_%d (%d 字节)" % (nxt, os.path.getsize(dst)))

if had_b:
    dstb = os.path.join(DATA, "9ba626afa44a3aa3.patch_%d" % (nxt + 1))
    shutil.copy2(os.path.join(PACK_B, "Addon", "9ba626afa44a3aa3.patch_0"), dstb)
    for suffix in (".gpu_resources", ".stream"): open(dstb + suffix, "wb").close()
    W("  包 B 部署为 patch_%d (%d 字节)" % (nxt + 1, os.path.getsize(dstb)))
else:
    W("  包 B 在 data 目录里没有旧部署，本次不新增（需要时在 Arsenal 里启用「GNH Transmog 界面汉化（可选）」）")
open(LOG, "w", encoding="utf-8").write(buf.getvalue())
print("ok")
