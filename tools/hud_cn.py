# -*- coding: utf-8 -*-
"""hud_cn.py -- HUD+ 汉化（按原文自动定位，可重复运行）。

模组更新后 patch 的偏移会全部改变，所以这里不写死偏移：
先按 "\\0 + 英文原文 + \\0" 在整个文件里定位字符串池里的那条，再等长替换。
中文一律不比英文长，差额用 \\0 补齐 —— 文件长度与偏移表完全不动。
"""
import os, io, json, re, shutil, datetime, sys
LA = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal")
DATA = r"C:\SteamLibrary\steamapps\common\Helldivers 2\data"
BK = r"E:\TAML\_scratch\hd2\hud-backup"
os.makedirs(BK, exist_ok=True)

REPL = [
    # 选项名 / 标签
    ("Death Marker", "死亡标记"),
    ("Fire Mode Icon", "射击模式"),
    ("Ammo Count", "弹药数"),
    ("Magazines", "弹匣"),
    ("Trajectory + Blast Radius", "弹道+爆炸范围"),
    ("Weapon HUD", "武器 HUD"),
    ("Trajectory Preview", "弹道预览"),
    ("Zeroing Icon", "归零图标"),
    ("Stratagems", "战备"),
    ("Vanilla HUD", "原版 HUD"),
    ("Gauges", "仪表"),
    ("Weapon Function Icons", "武器功能图标"),
    ("Squad Status", "小队状态"),
    ("Game Reticle (AMR, Backpack-Fed)", "游戏准星(AMR,背包供弹)"),
    ("Trajectory Only", "仅弹道"),
    # 描述
    ("While aiming an explosive round, or holding the throw button with a grenade or stratagem beacon, draws its path and marks where it hits. The blast radius paints the full-damage area and the outer edge of the blast on the ground, and turns the game's warning colour while you stand inside it.",
     "瞄准爆炸类弹药，或手持手雷、战备信标按住投掷键时，画出其飞行轨迹并标出落点。爆炸范围会在地面画出满伤区域与爆炸外沿，你站在其中时会变成游戏的警告色。"),
    ("Lets the game draw its own reticle for the Anti-Materiel Rifle in third person, and in first person for backpack-fed weapons without sights (Maxigun, Belt-Fed Grenade Launcher, Cremator). It follows the game's Reticle Visibility setting and applies to weapons that spawn after the change.",
     "让游戏为反器材步枪在第三人称下绘制自带准星，并为没有瞄具的背包供弹武器（Maxigun、弹链榴弹发射器、焚化者）在第一人称下绘制。遵循游戏的准星可见性设置，对该改动之后生成的武器生效。"),
    ("Shows skulls, recent map pings, boosters and each squadmate's stratagem calls. Calls sit beside the gear; your own status attaches to the weapon or health display.",
     "显示骷髅、地图标记、增益，以及队友的战备呼叫。呼叫显示在装备旁；你自己的状态挂在武器或血量显示上。"),
    ("Marks the spot where you died with a skull. After your reinforcement lands it stays 15 seconds, or until you reach it.",
     "用骷髅标记你阵亡的位置。增援落地后它会保留 15 秒，或直到你抵达该处。"),
    ("While you enter a stratagem code or hold a stratagem beacon, shows the game's stratagem list on the 3D panel instead of the screen.",
     "输入战备指令或手持战备信标时，把游戏的战备列表显示在 3D 面板上，而不是屏幕上。"),
    # 0.2.1 新增
    ("Pin 3D HUD to Screen", "固定 3D HUD"),
    ("3D Weapon Panel Opacity", "3D 面板不透明"),
    ("In third person, holds the 3D weapon panel to the right of the reticle instead of beside the weapon. First person always uses this position.",
     "第三人称下，把 3D 武器面板固定在准星右侧，而不是紧贴武器。第一人称始终使用该位置。"),
]

def translate(path, tag):
    raw = bytearray(open(path, "rb").read()); orig = len(raw)
    shutil.copy2(path, os.path.join(BK, "%s_%s" % (tag, datetime.datetime.now().strftime("%H%M%S"))))
    ok = skip = 0
    for en, zh in REPL:
        needle = b"\x00" + en.encode() + b"\x00"
        pos = raw.find(needle)
        if pos < 0:
            # 兜底：字符串池第一条前面可能不是 \0
            needle2 = en.encode() + b"\x00"
            pos2 = raw.find(needle2)
            if pos2 < 0:
                print("   ⚠️ 找不到: %s" % en[:42]); skip += 1; continue
            start, ln = pos2, len(needle2) - 1
        else:
            start, ln = pos + 1, len(needle) - 2
        b = zh.encode("utf-8")
        if len(b) > ln:
            print("   ❌ 超长 %d > %d: %s" % (len(b), ln, zh[:22])); skip += 1; continue
        raw[start:start+ln] = b + b"\x00" * (ln - len(b))
        ok += 1
    assert len(raw) == orig, "文件长度被改变了！"
    open(path, "wb").write(bytes(raw))
    print("   %s：替换 %d 条，跳过 %d 条，长度 %d 不变" % (tag, ok, skip, len(raw)))
    return ok

print("=== A) 模组目录 ===")
p = [m for m in json.load(io.open(os.path.join(LA, "hd2a_data.json"), encoding="utf-8"))
     ["modsList"]["default"]["mods"] if "抬头显示" in str(m.get("label"))][0]["path"]
pf = [os.path.join(dp, f) for dp, dn, fs in os.walk(p) for f in fs
      if f.endswith(".patch_0") and not f.endswith((".stream", ".gpu_resources"))][0]
size = os.path.getsize(pf)
n1 = translate(pf, "mod")
print("\n=== B) data 目录里同尺寸的 patch ===")
n2 = 0
for f in sorted(os.listdir(DATA)):
    m = re.match(r"^9ba626afa44a3aa3\.patch_(\d+)$", f)
    if not m:
        continue
    fp = os.path.join(DATA, f)
    if os.path.getsize(fp) != size:
        continue
    head = open(fp, "rb").read(0x4000)
    if b"Trajectory Preview" in head or b"Death Marker" in head:
        print("   找到 %s (%d 字节)" % (f, size))
        n2 += translate(fp, "data_" + m.group(1))
print("\n模组目录 %d 条 / data %d 个文件" % (n1, 1 if n2 else 0))
