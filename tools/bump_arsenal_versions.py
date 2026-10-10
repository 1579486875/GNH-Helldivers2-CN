# -*- coding: utf-8 -*-
"""bump_arsenal_versions.py -- 模组更新后，把 Arsenal 里中文 label 的**版本号**跟进到新版。

为什么不用现成的 sync_arsenal_from_manifest.py：
  那个脚本是"以 manifest 为准整体覆盖 label"，manifest 里的名字是英文
  （Armored Overhaul 3.4.0），一覆盖就把我们做的中文名（装甲大修 3.2.0）冲成英文了。
  这里只做一件事：把 label 里的**版本号片段**换成新版，中文名原样保留。

版本号来源优先级：模组 manifest 的 Name  →  目录名。
  例：装甲大修 3.2.0  +  manifest "Armored Overhaul 3.4.0"  ->  装甲大修 3.4.0
      HD2 抬头显示+   +  manifest 无版本号、目录名 "HD2 HUD Plus 0.2.2 ..."  ->  追加 " 0.2.2"

Arsenal 必须完全退出（它退出时会把内存里的状态写回 hd2a_data.json，会把改动冲掉）。
"""
import os, io, json, re, shutil, sqlite3, subprocess, datetime, sys

LA = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal")
MODS = os.path.join(LA, "mods")
ST = os.path.join(LA, "hd2a_data.json")
BK = r"E:\TAML\_scratch\hd2\arsenal-backup"
os.makedirs(BK, exist_ok=True)


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


def ver_of(s):
    """从一段文字里取出最像版本号的那一段。

    先找 `1.2` / `3.4.0` 这种带小数点的；找不到才退回 `v40` 这种纯整数编号。
    顺序不能反：ODST 的目录名是 "Devoid-Of-Liberty-7.0.0-V4"，
    先找 vN 会把末尾的修订号 V4 当成版本（7.0.0 才是主版本）。
    """
    if not s:
        return None
    # 注意：这里**故意不用 \b 词边界**。目录名里版本号常常紧跟在字母后面
    # （V1.9.2 / v0.6 / v40_AR499748），而字母与数字之间不构成 \b，
    # 用 \b 会从中间截出 "9.2"、"v0" 这种半个版本号。
    m = re.search(r"\d+\.\d+(?:\.\d+)*", s)
    if m:
        return m.group(0)
    m = re.search(r"(?<![A-Za-z0-9])[vV]\d+", s)
    if m:
        return m.group(0)
    return None


def ver_tuple(v):
    """把版本号化成可比较的数字元组：v1.2 -> (1, 2)。"""
    if not v:
        return None
    n = re.findall(r"\d+", v)
    return tuple(int(x) for x in n) if n else None


# 目录名 -> manifest Name
facts = {}
for d in os.listdir(MODS):
    mf = os.path.join(MODS, d, "manifest.json")
    if os.path.isfile(mf):
        try:
            facts[d] = json.load(io.open(mf, encoding="utf-8-sig")).get("Name") or ""
        except Exception:
            facts[d] = ""

stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(ST, os.path.join(BK, "hd2a_data.json.before-version-bump_%s" % stamp))
s = json.load(io.open(ST, encoding="utf-8"))

changed, unchanged = [], 0
DRY = "--dry" in sys.argv


def fix(m, where):
    global unchanged
    p = m.get("path") or ""
    d = os.path.basename(p)
    if not os.path.isdir(p):
        return
    label = str(m.get("label") or "")
    if not label:
        return
    new_v = ver_of(facts.get(d)) or ver_of(d)
    if not new_v:
        unchanged += 1
        return
    old_v = ver_of(label)
    if old_v == new_v:
        unchanged += 1
        return
    if old_v:
        # 只在"新版本确实比旧版本大"时才改。
        # 反例：BFV Kill Feedback 的 manifest 里写的是 v1，而 label 是 v1.2 ——
        # 不比大小直接覆盖会把版本号改小，看起来像被降级了。
        to, tn = ver_tuple(old_v), ver_tuple(new_v)
        if to is not None and tn is not None and tn <= to:
            unchanged += 1
            return
        newlabel = label.replace(old_v, new_v)
    else:
        newlabel = label + " " + new_v
    if newlabel == label:
        unchanged += 1
        return
    changed.append("%-6s %-40s -> %s" % (where, label, newlabel))
    if not DRY:
        m["label"] = newlabel


for m in s["modsList"]["default"]["mods"]:
    fix(m, "配置")
for m in s.get("modsLibrary") or []:
    fix(m, "模组库")

print("label 版本号跟进 %d 处（未变 %d）：" % (len(changed), unchanged))
for c in changed:
    print("   " + c)

if DRY:
    print("\n（dry-run，未写入）")
    raise SystemExit(0)

io.open(ST, "w", encoding="utf-8").write(json.dumps(s, ensure_ascii=False, indent=2))
json.load(io.open(ST, encoding="utf-8"))
print("hd2a_data.json 已写入（两处：配置 + 模组库）")

# deployment_snapshot.json（Arsenal 的部署快照，也带 label）
snap = os.path.join(LA, "deployment_snapshot.json")
if os.path.isfile(snap):
    shutil.copy2(snap, os.path.join(BK, "deployment_snapshot.json.before-version-bump_%s" % stamp))
    sj = json.load(io.open(snap, encoding="utf-8"))
    n = 0

    def fix_snap(lst):
        global n
        for m in lst or []:
            p = m.get("path") or m.get("Path") or ""
            d = os.path.basename(p)
            lab = str(m.get("label") or m.get("Label") or "")
            if not lab or not os.path.isdir(p):
                continue
            nv = ver_of(facts.get(d)) or ver_of(d)
            ov = ver_of(lab)
            if nv and ov != nv:
                nl = lab.replace(ov, nv) if ov else (lab + " " + nv)
                if "label" in m:
                    m["label"] = nl
                else:
                    m["Label"] = nl
                n += 1

    for k, v in sj.items():
        if isinstance(v, list):
            fix_snap(v)
    io.open(snap, "w", encoding="utf-8").write(json.dumps(sj, ensure_ascii=False, indent=2))
    print("deployment_snapshot.json 更新 %d 处" % n)

# mod_headers.db
db = os.path.join(LA, "mod_headers.db")
shutil.copy2(db, os.path.join(BK, "mod_headers.db.before-version-bump_%s" % stamp))
con = sqlite3.connect(db)
rows = con.execute("SELECT rowid, label, path FROM mods").fetchall()
n = 0
for rid, label, path in rows:
    d = os.path.basename(path or "")
    nv = ver_of(facts.get(d)) or ver_of(d)
    ov = ver_of(label or "")
    if nv and ov != nv:
        nl = (label or "").replace(ov, nv) if ov else ((label or "") + " " + nv)
        con.execute("UPDATE mods SET label = ? WHERE rowid = ?", (nl, rid))
        n += 1
        print("   DB  %-40s -> %s" % (label, nl))
con.commit()
con.close()
print("mod_headers.db 更新 %d 行" % n)
print("\n完成。备份在 %s" % BK)
