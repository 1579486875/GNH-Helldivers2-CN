# -*- coding: utf-8 -*-
"""hud_cn2.py -- HD2 抬头显示+ (HUD+) 0.2.2 字符串池汉化（可重复运行）。

原理与安全边界（务必先读）：
  * HUD+ 的界面文本不在 Lua 里，而在 patch 的一串「多语言字符串池」中：
    英文段 → 波兰语段 → 西班牙语段 …… 每个字符串以 NUL 分隔。
  * 文件里存在一张**指向字符串内部的偏移表**（实测 25 处 32 位小端值落在英文段内），
    所以**绝不能改变任何字符串的长度** —— 中文一律不许比英文长，不够就用 NUL 补齐。
    文件总长度、字符串起止偏移完全不动，因此结构风险为零。
  * 定位方式：找 b"\\0" + 英文 + b"\\0"。0.2.2 里每个待替字符串都**只出现一次**（已逐个核验），
    所以不必写死偏移，模组下次更新只要文案不变就还能命中。
  * 长度上限的取舍：短槽位（Size=4 / Hide=4 / Dim=3 / Opacity=7 字节）放不下常规译名，
    只能取单字或近似词；实在放不下的（Size）保留英文，宁可混一个英文词也不动结构。
"""
import os, io, json, re, shutil, datetime, sys
LA = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal")
BK = r"E:\TAML\_scratch\hd2\hud-backup"
os.makedirs(BK, exist_ok=True)

# (英文原文, 中文) —— 中文的 UTF-8 字节数必须 <= 英文字节数
REPL = [
    # ── 选项名 ──
    ("Death Marker", "死亡标记"),
    ("Fire Mode Icon", "射击模式"),
    ("Brackets", "括号"),
    ("Ammo Count", "弹药数"),
    ("Magazines", "弹匣"),
    ("Trajectory Reticle", "弹道准星"),
    ("Ring", "环"),
    ("Trajectory + Blast Radius", "弹道+爆炸范围"),
    ("Reticle + Blast Radius", "准星+爆炸范围"),
    ("Time Shown After Firing", "开火后显示时长"),
    ("Opacity", "透明"),          # 槽位仅 7 字节，"不透明度"(9) 放不下
    ("Hide", "隐"),               # 槽位仅 4 字节，"隐藏"(6) 放不下
    ("Dim", "暗"),                # 槽位仅 3 字节，只够一个字
    ("Always", "始终"),
    ("Weapon HUD", "武器 HUD"),
    ("Trajectory Preview", "弹道预览"),
    ("When Idle", "闲置时"),
    ("Zeroing Icon", "归零图标"),
    ("Stratagems", "战备"),
    ("Vanilla HUD", "原版 HUD"),
    ("Gauges", "仪表"),
    ("Weapon Function Icons", "武器功能图标"),
    ("Pin to Screen", "固定屏幕"),
    ("Squad Status", "小队状态"),
    ("Game Reticle (AMR, Backpack-Fed)", "游戏准星(AMR,背包)"),
    ("Trajectory Only", "仅弹道"),
    # ── 选项说明 ──
    ("While aiming an explosive round, or holding the throw button with a grenade or stratagem beacon, draws its path and marks where it hits. The blast radius paints the full-damage area and the outer edge of the blast on the ground, and turns the game's warning colour while you stand inside it.",
     "瞄准爆炸类弹药，或手持手雷、战备信标按住投掷键时，画出其飞行轨迹并标出落点。爆炸范围会在地面画出满伤区域与爆炸外沿，你站在其中时会变成游戏的警告色。"),
    ("While you enter a stratagem code or hold a stratagem beacon, shows the game's stratagem list in the 3D HUD instead of the screen.",
     "输入战备指令或手持战备信标时，把游戏的战备列表显示在 3D HUD 上，而不是屏幕上。"),
    ("How many seconds the 3D HUD stays after you fire. The game itself keeps weapon info up for 15 seconds; this can only shorten it.",
     "开火后 3D HUD 保持显示的秒数。游戏本身让武器信息显示 15 秒；这里只能缩短。"),
    ("Lets the game draw its own reticle for the Anti-Materiel Rifle in third person, and in first person for backpack-fed weapons without sights (Maxigun, Belt-Fed Grenade Launcher, Cremator). It follows the game's Reticle Visibility setting and applies to weapons that spawn after the change.",
     "让游戏为反器材步枪在第三人称下绘制自带准星，并为没有瞄具的背包供弹武器（Maxigun、弹链榴弹发射器、焚化者）在第一人称下绘制。遵循游戏的准星可见性设置，对该改动之后生成的武器生效。"),
    ("Shows skulls, recent map pings, boosters and each squadmate's stratagem calls. Calls sit beside the gear; your own status attaches to the weapon or health display.",
     "显示骷髅、地图标记、增益，以及队友的战备呼叫。呼叫显示在装备旁；你自己的状态挂在武器或血量显示上。"),
    ("Marks the spot where you died with a skull. After your reinforcement lands it stays 15 seconds, or until you reach it.",
     "用骷髅标记你阵亡的位置。增援落地后它会保留 15 秒，或直到你抵达该处。"),
    ("In third person, holds the 3D HUD to the right of the reticle instead of beside the weapon. First person always uses this position.",
     "第三人称下，把 3D HUD 固定在准星右侧，而不是紧贴武器。第一人称始终使用该位置。"),
    ("What the 3D HUD does once the game stops showing weapon info (it shows it while you aim, shoot, reload, switch or open the map). Hide fades it out, Dim keeps it at 30% and Always keeps it fully visible.",
     "游戏停止显示武器信息后 3D HUD 的表现（瞄准、射击、换弹、切换或打开地图时游戏会显示它）。隐：淡出；暗：保持 30%；始终：完全可见。"),
    ("Opacity of the weapon panel. The stratagem list always stays fully visible.",
     "武器面板的透明度。战备列表始终完全可见。"),
]

def translate(path, tag, dry=False):
    raw = bytearray(open(path, "rb").read())
    orig = len(raw)
    if not dry:
        shutil.copy2(path, os.path.join(BK, "%s_%s" % (
            tag, datetime.datetime.now().strftime("%m%d_%H%M%S"))))
    ok = skip = 0
    problems = []
    for en, zh in REPL:
        eb = en.encode(); zb = zh.encode()
        needle = b"\x00" + eb + b"\x00"
        cnt = raw.count(needle)
        if cnt != 1:
            problems.append("   ⚠️ %-46s 命中 %d 次（需恰好 1 次）" % (en[:46], cnt))
            skip += 1
            continue
        pos = raw.find(needle)
        start, ln = pos + 1, len(eb)
        if len(zb) > ln:
            problems.append("   ❌ %-46s 超长 %d > %d" % (zh, len(zb), ln))
            skip += 1
            continue
        if not dry:
            raw[start:start + ln] = zb + b"\x00" * (ln - len(zb))
        ok += 1
    assert len(raw) == orig, "文件长度被改变了！"
    if not dry:
        open(path, "wb").write(bytes(raw))
    print("   %s：替换 %d 条，跳过 %d 条，长度 %d 不变" % (tag, ok, skip, len(raw)))
    for p in problems:
        print(p)
    return ok, skip

print("=== HUD+ 0.2.2 字符串池汉化 ===")
DRY = "--dry" in sys.argv
if DRY:
    print("（dry-run：只检查，不写文件）")
st = json.load(io.open(os.path.join(LA, "hd2a_data.json"), encoding="utf-8"))
hit = [x for x in st["modsList"]["default"]["mods"] if "抬头显示" in str(x.get("label"))]
if not hit:
    print("找不到 HUD+ 模组，中止"); sys.exit(1)
p = hit[0]["path"]
print("模组目录：%s" % p)
pfs = [os.path.join(dp, f) for dp, dn, fs in os.walk(p) for f in fs
       if ".patch_" in f and not f.endswith((".stream", ".gpu_resources"))]
print("patch 文件：%s" % [os.path.basename(x) for x in pfs])
assert len(pfs) == 1, "预期只有一个 patch 文件"
ok, skip = translate(pfs[0], "hudplus_0.2.2", dry=DRY)
print("\n完成：%d 条已汉化，%d 条跳过" % (ok, skip))
