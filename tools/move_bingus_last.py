# -*- coding: utf-8 -*-
"""move_bingus_last.py -- 把 Bingus 共享加载器移到启用列表末尾（一次性整理）。

依据（两处独立的作者说明）：
  * Bingus 自己的简介：「Arsenal 用法：把本加载器放在列表最后（默认优先级），
    或在使用「首个模组优先」时放在最前。」
  * Vanilla Plus 的简介：「With default Arsenal priority put the loader last.」
本机 Arsenal 的 setTopPriority = False（即「默认优先级」），按说明应把加载器放最后，
但它当前排在第 1 位 —— 正好相反。

安全性（动手前已实测，见 _bingus_check.txt / _bingus2.txt）：
  * Bingus 的 patch 只含 1 个 entry，res_id = 8237644305030858762；
    在游戏 data 目录全部 137 个 patch 里**唯一**，没有任何别的模组提供同一资源。
    所以把它提升到最高优先级**不会覆盖任何人的文件**。
  * 全库唯一的资源重叠是 mods/hd2transmog/foundation（Transmog 本体 vs 我们的汉化包 B），
    与本操作无关。

只改 hd2a_data.json -> modsList.default.mods 的顺序；不动 modsLibrary。
Arsenal 必须完全退出。
"""
import os, io, json, re, sys, shutil, subprocess, datetime

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

st = json.load(io.open(ST, encoding="utf-8"))
mods = st["modsList"]["default"]["mods"]

bi = [i for i, m in enumerate(mods) if "Bingus" in str(m.get("label"))]
ri = [i for i, m in enumerate(mods) if "HD2Runtime" in str(m.get("label"))]
if not bi:
    print("找不到 Bingus 条目，中止"); raise SystemExit(1)
if len(mods) < 2:
    print("模组太少，中止"); raise SystemExit(1)

cur = bi[0]
# 目标位置：**绝对末尾**。
# Bingus 的作者说明写得很明确（「放在列表最后」），而 HD2Runtime 对自己的位置没有任何要求，
# 所以严格按作者说明把加载器放到最后一位。两者提供的资源 id 唯一、互不覆盖，谁前谁后都不影响功能。
dst = len(mods) - 1

print("当前顺序（前 6 + 末 4）：")
for i, m in enumerate(mods):
    mark = "  ← Bingus" if i == cur else ("  ← HD2Runtime" if ri and i == ri[0] else "")
    if i < 6 or i >= len(mods) - 4:
        print("  %2d  %s%s" % (i + 1, str(m.get("label"))[:52], mark))
print("\nBingus 现在第 %d 位，将移到第 %d 位（列表最末）" % (cur + 1, dst + 1))

if cur == dst:
    print("已经就位，无需改动。")
    raise SystemExit(0)

item = mods.pop(cur)
# 目标是「列表最末」，所以直接追加。
# 注意不要写成 insert(dst)：pop 之后列表短了一个，原末位索引已经过期，
# 用 dst = len(orig)-1 再 insert 会少插一位（实测会落到倒数第二）。
mods.append(item)

print("\n新顺序（前 6 + 末 6）：")
for i, m in enumerate(mods):
    if i < 6 or i >= len(mods) - 6:
        print("  %2d  %s" % (i + 1, str(m.get("label"))[:52]))

# 自检：集合必须完全一致，条数不变
src_labels = sorted(str(x.get("label")) for x in json.load(
    io.open(ST, encoding="utf-8"))["modsList"]["default"]["mods"])
new_labels = sorted(str(x.get("label")) for x in mods)
assert len(mods) == len(src_labels), "条数变了！"
assert src_labels == new_labels, "模组集合变了！"
print("\n自检：%d 条，集合与改动前完全一致 ✅" % len(mods))

if DRY:
    print("（dry-run，未写入）")
    raise SystemExit(0)

stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(ST, os.path.join(BK, "hd2a_data.json.before-bingus-last_%s" % stamp))
io.open(ST, "w", encoding="utf-8").write(json.dumps(st, ensure_ascii=False, indent=2))
json.load(io.open(ST, encoding="utf-8"))
print("hd2a_data.json 已写入并通过 JSON 校验")
print("\n⚠ 顺序变了 → patch 编号会整体重排，请回 Arsenal 再点一次 Deploy。")
