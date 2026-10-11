# -*- coding: utf-8 -*-
"""verify_desc_order.py -- 验证简介汉化与 Bingus 排序的结果。"""
import os, io, json, re, glob
LA = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal")
st = json.load(io.open(os.path.join(LA, "hd2a_data.json"), encoding="utf-8"))
mods = st["modsList"]["default"]["mods"]
CJK = re.compile(r"[\u4e00-\u9fff]")

print("=" * 78)
print("【1】启用列表顺序")
print("=" * 78)
for i, m in enumerate(mods):
    print("  %2d  %-46s %s" % (i + 1, str(m.get("label"))[:46],
                               "✅中文" if CJK.search(str(m.get("description") or "")) else "⚠️非中文"))

print("\n" + "=" * 78)
print("【2】简介语言统计")
print("=" * 78)
zh = [m for m in mods if CJK.search(str(m.get("description") or ""))]
en = [m for m in mods if not CJK.search(str(m.get("description") or ""))]
empty = [m for m in mods if not str(m.get("description") or "").strip()]
print("  中文 %d 条 / 非中文 %d 条 / 其中空 %d 条（共 %d）" % (len(zh), len(en), len(empty), len(mods)))
for m in en:
    print("     ⚠️ %-44s %s" % (str(m.get("label"))[:44], str(m.get("description"))[:70]))

print("\n" + "=" * 78)
print("【3】关键位置检查")
print("=" * 78)
last = str(mods[-1].get("label"))
second = str(mods[-2].get("label"))
print("  第 30 位（最末）= %s  %s" % (last, "✅ Bingus" if "Bingus" in last else "❌"))
print("  第 29 位        = %s" % second)
first = str(mods[0].get("label"))
print("  第 1 位         = %s" % first)
print("  汉化包 A 位置    = 第 %d 位" % ([i for i, m in enumerate(mods) if "GNH 简体中文汉化包" in str(m.get("label"))][0] + 1))
pb = [i for i, m in enumerate(mods) if "GNH Transmog 界面汉化" in str(m.get("label"))][0]
tb = [i for i, m in enumerate(mods) if "HD2 Transmog 基础组件" in str(m.get("label"))][0]
print("  汉化包 B / Transmog 本体 = 第 %d / %d 位  %s" % (pb + 1, tb + 1, "✅ B 在后面" if pb > tb else "❌ 顺序反了"))

print("\n" + "=" * 78)
print("【4】HD2Runtime 与 Bingus 的简介")
print("=" * 78)
for key in ["HD2Runtime", "Bingus"]:
    m = [x for x in mods if key in str(x.get("label"))][0]
    print("  %s\n     %s\n" % (m.get("label"), m.get("description")))

print("=" * 78)
print("【5】其他可能存描述的 Arsenal 文件")
print("=" * 78)
for f in ["deployment_snapshot.json", "mod_headers.db"]:
    p = os.path.join(LA, f)
    print("  %-28s %s" % (f, "存在 %d 字节" % os.path.getsize(p) if os.path.exists(p) else "不存在"))
    if f.endswith(".json") and os.path.exists(p):
        try:
            j = json.load(io.open(p, encoding="utf-8"))
            n = 0

            def walk(o):
                global n
                if isinstance(o, dict):
                    if "description" in o and isinstance(o["description"], str):
                        n += 1
                    for v in o.values():
                        walk(v)
                elif isinstance(o, list):
                    for x in o:
                        walk(x)
            walk(j)
            print("       含 description 字段 %d 处" % n)
        except Exception as e:
            print("       读取失败：%s" % e)
