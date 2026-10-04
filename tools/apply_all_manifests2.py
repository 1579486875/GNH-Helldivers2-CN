# -*- coding: utf-8 -*-
"""apply_all_manifests2.py -- 把词表应用到模组库里**全部** manifest（不只启用的）。

和第一版的区别：
  1. 词表直接从合并好的 cn_strings.py 读，不再硬编码分册清单，新增词表自动生效；
  2. 直接遍历 mods 目录（而不是从数据库读路径），避免库里路径过时导致漏掉；
  3. 明确只改 Name / Description —— manifest 里的 Include 是**目录名**，翻译了会找不到文件。
"""
import os, io, json, re, shutil, sys
HD2 = r"E:\TAML\_scratch\hd2"
sys.path.insert(0, HD2)
from cn_strings import CN

MODS = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal", "mods")
BAK = os.path.join(HD2, "backup", "manifests-all")

def norm(s):
    return (s.replace("\u2019", "'").replace("\u2018", "'")
             .replace("\u201c", '"').replace("\u201d", '"').replace("\u2014", "-"))

NT = {norm(k): v for k, v in CN.items()}
def tr(s):
    """查词表。已经是中文的、或查不到的，原样返回。"""
    if not isinstance(s, str) or not s.strip():
        return s
    if re.search(r"[\u4e00-\u9fff]", s):
        return s
    if s in CN:
        return CN[s]
    return NT.get(norm(s), s)

changed, seen_mod, no_manifest = 0, 0, 0
for name in sorted(os.listdir(MODS)):
    root = os.path.join(MODS, name)
    if not os.path.isdir(root):
        continue
    mp = os.path.join(root, "manifest.json")
    if not os.path.isfile(mp):
        no_manifest += 1
        continue
    seen_mod += 1
    j = json.load(io.open(mp, encoding="utf-8-sig"))
    before = json.dumps(j, ensure_ascii=False, sort_keys=True)

    j["Name"] = tr(j.get("Name", ""))
    j["Description"] = tr(j.get("Description", ""))
    def w(opts):
        for x in opts or []:
            if not isinstance(x, dict):
                continue
            for k in ("Name", "Description"):
                if k in x:
                    x[k] = tr(x[k])
            w(x.get("SubOptions"))
    w(j.get("Options"))

    if json.dumps(j, ensure_ascii=False, sort_keys=True) != before:
        try:
            bdir = os.path.join(BAK, re.sub(r'[\\/:*?"<>|]', "_", name)[:60])
            os.makedirs(bdir, exist_ok=True)
            if not os.path.exists(os.path.join(bdir, "manifest.json")):
                shutil.copy2(mp, os.path.join(bdir, "manifest.json"))
        except OSError as exc:
            print("  [备份跳过] %s: %s" % (name[:36], exc))
        json.dump(j, io.open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        changed += 1
        print("  已汉化: %-58s -> %s" % (name[:58], j["Name"]))

print("\n扫描 %d 个 manifest，更新 %d 个；%d 个目录没有 manifest.json" % (seen_mod, changed, no_manifest))
