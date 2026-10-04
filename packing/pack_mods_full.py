# -*- coding: utf-8 -*-
"""pack_mods_1005.py -- 完整打包当前启用的 26 个模组（整个目录，含全部选项）。

与旧版唯一的区别：输出目录换成今天的日期，并打印磁盘余量。
"""
import json, os, re, zipfile, time, shutil

DATA = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal", "hd2a_data.json")
mods = json.load(open(DATA, encoding="utf-8"))["modsList"]["default"]["mods"]
OUT = r"E:\TAML\HD2模组打包-2026-10-05"
os.makedirs(OUT, exist_ok=True)

def human(n):
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024 or u == "GB":
            return "%.1f %s" % (n, u)
        n /= 1024.0

def safe(name):
    return re.sub(r'[\\/:*?"<>|]', "_", name).strip()

for z in os.listdir(OUT):
    if z.endswith(".zip"):
        os.remove(os.path.join(OUT, z))

enabled = sorted([x for x in mods if x.get("enabled")], key=lambda x: x.get("label", ""))
print("启用模组 %d 个，开始打包到 %s\n" % (len(enabled), OUT))

report, t0 = [], time.time()
for m in enabled:
    label, root = m["label"], m["path"]
    if not os.path.isdir(root):
        report.append((label, "目录不存在", 0))
        print("  ✗ %-34s 目录不存在" % label[:34])
        continue
    zip_path = os.path.join(OUT, safe(label) + ".zip")
    n_files = n_bytes = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=1) as z:
        for dirpath, dirnames, filenames in os.walk(root):
            for f in filenames:
                src = os.path.join(dirpath, f)
                rel = os.path.relpath(src, root).replace("\\", "/")
                z.write(src, rel)
                n_files += 1
                n_bytes += os.path.getsize(src)
    report.append((label, "%d 个文件" % n_files, os.path.getsize(zip_path)))
    print("  ✔ %-32s %-9s 原始 %9s -> zip %9s" % (label[:32], "%d 文件" % n_files, human(n_bytes), human(os.path.getsize(zip_path))))

tot = sum(r[2] for r in report)
print("\n共 %d 个包，合计 %s，用时 %.0f 秒" % (len(report), human(tot), time.time() - t0))
json.dump([[r[0], r[1], r[2]] for r in report],
          open(os.path.join(OUT, "_打包清单.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
free = shutil.disk_usage("E:\\").free
print("E 盘剩余空间：%s" % human(free))
print("完成 -> %s" % OUT)
