# -*- coding: utf-8 -*-
"""missing_scan.py -- 全量扫描 34 个模组的界面文本，比对现有词表，列出缺失。"""
import os, io, json, re, sys
sys.path.insert(0, r"E:\TAML\_scratch\hd2")
from hd2_patch import PatchFile
HD2 = r"E:\TAML\_scratch\hd2"
SPEC = [("cn_add.py","CN_ADD"),("cn_desc.py","CN_DESC"),("cn_fix.py","CN_FIX"),("cn_mods.py","CN_MODS"),
        ("cn_mods2.py","CN_MODS2"),("cn_new.py","CN_NEW"),("cn_strings.py","CN"),("cn_ui3.py","CN_UI3"),
        ("cn_ui4.py","CN_UI4"),("cn_ui5.py","CN_UI5"),("cn_mods3.py","CN_MODS3"),("cn_mods4.py","CN_MODS4"),
        ("cn_mods5.py","CN_MODS5"),("cn_batch1.py","CN_BATCH"),("cn_batch2.py","CN_BATCH2"),
        ("cn_batch3.py","CN_BATCH3"),("cn_runtime.py","CN_RUNTIME")]
CN = {}
for f, key in SPEC:
    ns = {}
    exec(open(os.path.join(HD2, f), encoding="utf-8-sig").read(), ns)
    for k, v in (ns.get(key) or {}).items():
        if isinstance(k, str) and isinstance(v, str) and k not in CN:
            CN[k] = v
print("现有词表 %d 条" % len(CN))

def split_args(s):
    out, depth, buf, q, esc = [], 0, [], None, False
    for ch in s:
        if esc: buf.append(ch); esc = False; continue
        if ch == "\\": buf.append(ch); esc = True; continue
        if q:
            buf.append(ch)
            if ch == q: q = None
            continue
        if ch in "'\"": q = ch; buf.append(ch); continue
        if ch in "([{": depth += 1
        elif ch in ")]}": depth -= 1
        if ch == "," and depth == 0: out.append("".join(buf).strip()); buf = []
        else: buf.append(ch)
    if buf: out.append("".join(buf).strip())
    return out

def unq(x):
    x = x.strip()
    if len(x) >= 2 and x[0] in "'\"" and x[-1] == x[0]:
        return x[1:-1]
    return None

def scan_calls(t, fname):
    """提取 option(...) / register_option(...) 里的 label / description / choices"""
    res = []
    for m in re.finditer(r"(?<![\w.])option\s*\(", t):
        i = m.end(); depth = 1; j = i
        while j < len(t) and depth:
            c = t[j]
            if c == "(": depth += 1
            elif c == ")": depth -= 1
            j += 1
        args = split_args(t[i:j-1])
        if len(args) >= 3:
            lab = unq(args[2])
            if lab: res.append(("label", lab))
        if len(args) >= 8:
            d = unq(args[7])
            if d: res.append(("desc", re.sub(r"\s+", " ", d)))
        for a in args:
            if a.strip().startswith("{"):
                for c in split_args(a.strip()[1:-1] if a.strip().endswith("}") else a.strip()[1:]):
                    u = unq(c)
                    if u and len(u) > 2: res.append(("choice", u))
    return res

def scan_fields(t):
    res = []
    for m in re.finditer(r"\blabel\s*=\s*('(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\")", t):
        u = unq(m.group(1))
        if u and "/" not in u: res.append(("label", u))
    for m in re.finditer(r"\bdescription\s*=\s*('(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\")", t):
        u = unq(m.group(1))
        if u: res.append(("desc", re.sub(r"\s+", " ", u)))
    for m in re.finditer(r"\bchoices?\s*=\s*\{", t):
        i = m.end(); depth = 1; j = i
        while j < len(t) and depth:
            if t[j] == "{": depth += 1
            elif t[j] == "}": depth -= 1
            j += 1
        for c in split_args(t[i:j-1]):
            u = unq(c)
            if u and len(u) > 2: res.append(("choice", u))
    return res

LA = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal")
st = json.load(io.open(os.path.join(LA, "hd2a_data.json"), encoding="utf-8"))
mods = [m for m in st["modsList"]["default"]["mods"] if m.get("enabled")]
missing = {}
for m in mods:
    lab = str(m.get("label")); root = m.get("path") or ""
    if not root or not os.path.isdir(root): continue
    found = {}
    for dp, dn, fs in os.walk(root):
        for f in sorted(fs):
            if ".patch_" not in f or f.endswith((".gpu_resources", ".stream")): continue
            try: pf = PatchFile.load(os.path.join(dp, f))
            except Exception: continue
            for e in pf.entries:
                if e.type != 2: continue
                t = e.data.decode("utf-8", "ignore")
                for kind, s in scan_calls(t, f) + scan_fields(t):
                    if s not in found: found[s] = kind
    miss = {s: k for s, k in found.items() if s not in CN and s.upper() not in CN}
    if miss: missing[lab] = miss

tot = sum(len(v) for v in missing.values())
print("缺失文本覆盖 %d 个模组，共 %d 条\n" % (len(missing), tot))
for lab, d in sorted(missing.items(), key=lambda x: -len(x[1])):
    print("=" * 74)
    print("【%s】缺 %d 条" % (lab, len(d)))
    for s, k in list(d.items())[:60]:
        print("   [%s] %s" % (k, s[:130]))
io.open(os.path.join(HD2, "_missing.json"), "w", encoding="utf-8").write(
    json.dumps({k: {s: t for s, t in v.items()} for k, v in missing.items()}, ensure_ascii=False, indent=1))
print("\n已写入 _missing.json")
