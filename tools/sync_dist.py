# -*- coding: utf-8 -*-
"""sync_dist.py -- 把 Arsenal 里构建好的两个汉化包重新打成分发 zip，同步到所有分发位置。

⚠ 2026-10-10 修正：源目录不再写死。
Arsenal 导入模组时会自己起一个带 `_AR<数字>` 后缀的目录，真正的路径只有 hd2a_data.json
里知道。之前这里写死 `GNH-Chinese-Simplified-Pack`，那是构建脚本早期误建的**孤儿目录**，
Arsenal 根本不看 —— 结果同步出去的分发 zip 一直是孤儿目录里的旧内容。
现在统一从 Arsenal 状态里现查，找不到就直接报错退出，绝不静默用错目录。
"""
import os, io, json, datetime, zipfile, hashlib, sys

LA = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal")
MODS = os.path.join(LA, "mods")
TODAY = datetime.date.today().strftime("%Y-%m-%d")
OUTDIR = r"E:\TAML\HD2-模组合集-GNH个人汉化-%s" % TODAY

st = json.load(io.open(os.path.join(LA, "hd2a_data.json"), encoding="utf-8"))


def our_dir(label_key):
    """从 Arsenal 状态里找出我们那个汉化包的实际目录。"""
    for m in st["modsList"]["default"]["mods"]:
        if label_key in str(m.get("label")) and m.get("path") and os.path.isdir(m["path"]):
            return m["path"]
    raise SystemExit("❌ 在 Arsenal 状态里找不到「%s」，请确认该模组已导入 Arsenal。" % label_key)


PACKS = [
    (our_dir("GNH 简体中文汉化包"), "GNH 简体中文汉化包.zip", [
        r"E:\TAML\GNH简体中文汉化包-Hellldivers2.zip",
        r"E:\TAML\GNH-Helldivers2-CN\dist\GNH简体中文汉化包-Hellldivers2.zip",
        os.path.join(OUTDIR, "GNH 简体中文汉化包.zip"),
    ]),
    (our_dir("GNH Transmog 界面汉化"), "GNH Transmog 界面汉化（可选）.zip", [
        r"E:\TAML\GNH-Transmog界面汉化-可选包.zip",
        r"E:\TAML\GNH-Helldivers2-CN\dist\GNH-Transmog界面汉化-可选包.zip",
        os.path.join(OUTDIR, "GNH Transmog 界面汉化（可选）.zip"),
    ]),
]


def sha1(p):
    h = hashlib.sha1()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


for src, _zipname, targets in PACKS:
    mf = os.path.join(src, "manifest.json")
    pdir = os.path.join(src, "Addon")
    patches = sorted(f for f in os.listdir(pdir) if ".patch_" in f)
    assert patches, "no patch in %s" % pdir
    pf = os.path.join(pdir, patches[0])
    print("=== %s" % src)
    print("    manifest %d 字节 / patch %s %d 字节 sha1=%s"
          % (os.path.getsize(mf), patches[0], os.path.getsize(pf), sha1(pf)[:12]))
    for dest in targets:
        d = os.path.dirname(dest)
        if not os.path.isdir(d):
            print("   -- 跳过（目录不存在）：%s" % dest)
            continue
        with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
            z.write(mf, "manifest.json")
            z.write(pf, "Addon/" + patches[0])
        print("   -> %-58s %8d 字节" % (dest, os.path.getsize(dest)))
        with zipfile.ZipFile(dest) as z:
            for i in z.infolist():
                print("        %-40s %9d" % (i.filename, i.file_size))
print("\n完成。分发目录：%s" % OUTDIR)
