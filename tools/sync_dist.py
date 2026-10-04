# -*- coding: utf-8 -*-
"""sync_dist.py -- 把 Arsenal 里构建好的两个包重新打成分发 zip，同步到所有分发位置。"""
import os, zipfile, hashlib, sys

MODS = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal", "mods")
PACKS = [
    ("GNH-Chinese-Simplified-Pack", [
        r"E:\TAML\GNH简体中文汉化包-Hellldivers2.zip",
        r"E:\TAML\GNH-Helldivers2-CN\dist\GNH简体中文汉化包-Hellldivers2.zip",
        r"E:\TAML\HD2模组打包-2026-10-04\GNH 简体中文汉化包.zip",
    ]),
    ("GNH-Transmog-CN-Addon", [
        r"E:\TAML\GNH-Transmog界面汉化-可选包.zip",
        r"E:\TAML\GNH-Helldivers2-CN\dist\GNH-Transmog界面汉化-可选包.zip",
        r"E:\TAML\HD2模组打包-2026-10-04\GNH Transmog 界面汉化（可选）.zip",
    ]),
]

def sha1(p):
    h = hashlib.sha1()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

for name, targets in PACKS:
    src = os.path.join(MODS, name)
    mf = os.path.join(src, "manifest.json")
    pdir = os.path.join(src, "Addon")
    patches = sorted(f for f in os.listdir(pdir) if ".patch_" in f)
    assert patches, "no patch in %s" % pdir
    pf = os.path.join(pdir, patches[0])
    print("=== %s" % name)
    print("    manifest %d 字节 / patch %s %d 字节 sha1=%s" % (os.path.getsize(mf), patches[0], os.path.getsize(pf), sha1(pf)[:12]))
    for dest in targets:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
            z.write(mf, "manifest.json")
            z.write(pf, "Addon/" + patches[0])
        print("   -> %-58s %8d 字节" % (dest, os.path.getsize(dest)))
        with zipfile.ZipFile(dest) as z:
            for i in z.infolist():
                print("        %-40s %9d" % (i.filename, i.file_size))
