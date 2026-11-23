# -*- coding: utf-8 -*-
"""cn_mod_desc.py -- 把 Arsenal 里模组的**简介（description）**换成简体中文。可重复运行。

为什么需要它：
  Arsenal 的模组简介是从各模组自带的 manifest.json 读进来的。用户每次「更新/重新导入」
  模组，Arsenal 就会用 manifest 里的英文原文把我们之前汉化好的简介**覆盖掉**。
  2026-10-11 就是这么被打回 12 条纯英文的。所以简介汉化和 HUD+ 的字符串池一样，
  属于「上游一变就要重跑」的一次性工序。

只改显示层，三处都不动文件本身：
  * hd2a_data.json  -> modsList.default.mods[].description（列表页显示的就是它）
  * hd2a_data.json  -> modsLibrary[].description（模组库）
  * mod_headers.db  -> 若存在描述字段，一并更新
  **故意不改 manifest.json**：那是模组自带文件，改了会让 Arsenal 算出的 contentHash
  与磁盘不一致，下次启动可能把模组标记成「已更改」。收益不值这个风险。

前提：Arsenal 必须完全退出（它退出时会把内存里的状态写回，开着改会被冲掉）。
"""
import os, io, json, re, sys, shutil, sqlite3, subprocess, datetime

LA = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal")
ST = os.path.join(LA, "hd2a_data.json")
BK = r"E:\TAML\_scratch\hd2\arsenal-backup"
os.makedirs(BK, exist_ok=True)
DRY = "--dry" in sys.argv


def running():
    try:
        out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq HD2Arsenal.exe"],
                             capture_output=True, text=True, timeout=15).stdout
        return "HD2Arsenal" in out
    except Exception:
        return False


if running():
    print("❌ Arsenal 正在运行 —— 请先完全退出，否则改动会被它覆盖")
    raise SystemExit(1)

# ── 按「英文简介原文」精确匹配 ──────────────────────────────────────────────
BY_TEXT = {
    "Choose any of the twenty-one bundled mods in this pack's Options menu in Arsenal or HD2MM. "
    "Requires the separate Bingus Shared Loader v18. Disable standalone copies of features you want "
    "turned off. Close the game, select your options, then Purge / Deploy. With default Arsenal "
    "priority put the loader last.":
        "在 Arsenal 或 HD2MM 的「选项」菜单里挑选本合集的 21 个内置模组。需要单独安装 Bingus 共享加载器 v18。"
        "想关掉某项功能，就同时禁用它的独立版本。关掉游戏 → 选好选项 → Purge / Deploy。"
        "Arsenal 默认优先级下，请把加载器放在列表最后。",

    "Bastion, Maelstrom and FRV upgrades, each its own option: tank top speed, engine torque, grip, "
    "steering, throttle response, suspension and stability; 360-degree MBT turrets with traverse, "
    "elevation and aim range; an autoloader; driving from the gunner seat; gunner camera distance; "
    "FRV stability; a vehicle indicator; and more than one vehicle in your loadout. With the Mod "
    "Options Menu, the options can be changed in game. Requires Bingus Shared Loader v19 or newer.":
        "堡垒、漩涡与快速侦察车的全面强化，每一项都是独立选项：坦克极速、发动机扭矩、履带抓地力、转向、"
        "油门响应、悬挂与稳定性；主战坦克炮塔可 360 度旋转，转向速度、俯仰速度与瞄准范围均可调；自动装弹机；"
        "从炮手位驾驶；炮手视角距离；侦察车稳定性；载具指示器；以及战备配置里带多辆载具。"
        "装「模组选项菜单」后可在游戏内随时调整。需要 Bingus 共享加载器 v19 或更高。",

    "Smarter, safer aiming for your guard dog (Guard Dog, Rover, K-9), your sentries and the resupply "
    "pod and Supply FRV guns. They never shoot through you or your teammates, skip the dead, cover and "
    "armor they can't hurt, and pick the right targets. The Tesla Tower stops zapping you. Optional "
    "targeting laser. Each part can be turned on or off in the options (also in game with Mod Options "
    "Menu). Requires Bingus Shared Loader v15 or newer.":
        "让你的护卫犬（护卫犬、漫游者、K-9）、哨戒炮，以及补给舱与补给侦察车的机枪打得更聪明、更安全："
        "绝不穿过你或队友开火，跳过尸体、掩体与打不穿的装甲，并自动挑选合适的目标；特斯拉塔不再电你。"
        "可选目标激光。每一项都能在选项里单独开关（装「模组选项菜单」后游戏内也能改）。"
        "需要 Bingus 共享加载器 v15 或更高。",

    "(v3.0.7) Redesigned, clear and precise map markers.":
        "（v3.0.7）重新设计的地图标记：清晰、精确。",

    "Beside the compass: enemies near you, searching for you, targeting you, and targeting your "
    "teammates. Requires Bingus Shared Loader v15 or newer / API 1.":
        "显示在罗盘旁：附近、正在搜索你、正在锁定你，以及正在锁定队友的敌人。"
        "需要 Bingus 共享加载器 v15 或更高 / API 1。",

    "v1.9.3 test build: copies fresh unit coordinates and logs warning sources for diagnosis. "
    "Preserves visuals, settings, EXO and host/client support. Requires Mod Options Menu v1.1+ and "
    "Bingus Shared Loader v18+.":
        "v1.9.3 测试版：复制最新的单位坐标并记录警报来源，便于诊断。视觉效果、各项设置、机甲支持与"
        "主客机兼容均保持不变。需要「模组选项菜单」v1.1+ 与 Bingus 共享加载器 v18+。",

    "Adds what the vanilla HUD leaves out - a 3D weapon panel, ammo count and weapon icons on the "
    "weapon row, trajectory preview and squad status - built from the game's own HUD and set in the "
    "game's Options menu.":
        "补齐原版 HUD 缺少的内容：3D 武器面板、弹药数与武器栏图标、弹道预览、小队状态 —— "
        "全部基于游戏自身的 HUD 实现，在游戏的选项菜单里设置。",

    "Longer-range vanilla pickup icons for samples, supplies and equipment. Set each distance "
    "(default to 100) and switch in game on the Escape menu's MODS tab. Needs Bingus Shared Loader "
    "v15+; Mod Options Menu recommended.":
        "拉长原版拾取图标（样本、补给、装备）的可见距离。三类距离可分别设置（默认 100），"
        "游戏内按 Esc → MODS 标签页切换。需要 Bingus 共享加载器 v15+；建议搭配「模组选项菜单」。",

    "All-In-One Pack":
        "整合包（All-In-One）",

    "Removes the smoke from firing a weapon while keeping the muzzle flash.":
        "移除开火时的硝烟，同时保留枪口火光。",

    "All-in-one file; choose which weapon sounds you want to use.":
        "整合包；可自行挑选要使用的武器音效。",

    "Shared HD2Runtime API 1. Requires Bingus Shared Loader v15+ / API 1. Install once; no gameplay "
    "changes until a dependent mod requests them.":
        "共享 HD2Runtime API 1。需要 Bingus 共享加载器 v15+ / API 1。安装一次即可；"
        "在依赖它的模组来请求之前，它不会改动任何玩法。",
}

# ── 原文是空描述时，按模组目录名补一句（这两条模组自己没写简介）─────────────
BY_PATH = {
    "Runtime(ShareLoader)":
        "共享骨骼运行时（C-Rig）：为使用自订骨骼的模组提供 IK 与手部定位支持。"
        "安装一次即可，本身不改动玩法，由依赖它的模组调用。",
    "BFV Kill Feedback":
        "战地风格的击杀反馈：击杀图标、得分与连杀加分，以及四组随机得分音效；"
        "音效风格可在 BF1 / BF5 / BF6 之间切换，位置、大小、停留时间与音量均可调。"
        "装「模组选项菜单」后可在游戏内调整。",
}

stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
st = json.load(io.open(ST, encoding="utf-8"))
hits = []


def fix(m, where):
    p = str(m.get("path") or "")
    old = str(m.get("description") or "")
    new = BY_TEXT.get(old)
    if not new:
        for key, z in BY_PATH.items():
            if key in p and not old.strip():
                new = z
                break
    if new and new != old:
        hits.append((where, str(m.get("label"))[:40], old[:52], new[:52]))
        if not DRY:
            m["description"] = new


for m in st["modsList"]["default"]["mods"]:
    fix(m, "配置")
for m in st.get("modsLibrary") or []:
    fix(m, "模组库")

print("简介汉化 %d 处：" % len(hits))
for where, lab, old, new in hits:
    print("   [%s] %s" % (where, lab))
    print("        旧: %s" % old)
    print("        新: %s" % new)

if DRY:
    print("\n（dry-run，未写入）")
    raise SystemExit(0)

shutil.copy2(ST, os.path.join(BK, "hd2a_data.json.before-desc-cn_%s" % stamp))
io.open(ST, "w", encoding="utf-8").write(json.dumps(st, ensure_ascii=False, indent=2))
json.load(io.open(ST, encoding="utf-8"))
print("\nhd2a_data.json 已写入并通过 JSON 校验")

# mod_headers.db（若有描述字段）
db = os.path.join(LA, "mod_headers.db")
if os.path.isfile(db):
    shutil.copy2(db, os.path.join(BK, "mod_headers.db.before-desc-cn_%s" % stamp))
    con = sqlite3.connect(db)
    tabs = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    n = 0
    for t in tabs:
        cols = [r[1] for r in con.execute("PRAGMA table_info(%s)" % t).fetchall()]
        dcol = next((c for c in cols if "desc" in c.lower()), None)
        if not dcol:
            continue
        for rid, d in con.execute("SELECT rowid, %s FROM %s" % (dcol, t)).fetchall():
            new = BY_TEXT.get(str(d or ""))
            if new:
                con.execute("UPDATE %s SET %s=? WHERE rowid=?" % (t, dcol), (new, rid))
                n += 1
    con.commit()
    con.close()
    print("mod_headers.db 更新 %d 行（表：%s）" % (n, tabs))
print("\n完成。备份在 %s" % BK)
