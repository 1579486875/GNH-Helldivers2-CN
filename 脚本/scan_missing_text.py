# -*- coding: utf-8 -*-
"""rescan2.py -- 修正版扫描：把 Lua 字面量里的转义还原成运行时字符串再查词表。

修正点（对比 rescan.py）：
  1. unq() 之后做一次 Lua 反转义：'Menu\\'s' -> "Menu's"。之前保留了反斜杠，
     导致这些条目被误报成"未翻译"（实测 6 条）。
  2. 空白压缩只作为**补充**判据，不再用压缩后的串当唯一 key。
"""
import os, io, json, re, sys
sys.path.insert(0, r"E:\TAML\_scratch\hd2")
from hd2_patch import PatchFile
HD2 = r"E:\TAML\_scratch\hd2"
SPEC = [("cn_add.py", "CN_ADD"), ("cn_desc.py", "CN_DESC"), ("cn_fix.py", "CN_FIX"),
        ("cn_mods.py", "CN_MODS"), ("cn_mods2.py", "CN_MODS2"), ("cn_new.py", "CN_NEW"),
        ("cn_strings.py", "CN"), ("cn_ui3.py", "CN_UI3"), ("cn_ui4.py", "CN_UI4"),
        ("cn_ui5.py", "CN_UI5"), ("cn_mods3.py", "CN_MODS3"), ("cn_mods4.py", "CN_MODS4"),
        ("cn_mods5.py", "CN_MODS5"), ("cn_batch1.py", "CN_BATCH"), ("cn_batch2.py", "CN_BATCH2"),
        ("cn_batch3.py", "CN_BATCH3"), ("cn_runtime.py", "CN_RUNTIME"),
        ("cn_pack6.py", "CN_PACK6"), ("cn_pack7.py", "CN_PACK7"),
        ("cn_pack8.py", "CN_PACK8"), ("cn_pack9.py", "CN_PACK9"), ("cn_pack10.py", "CN_PACK10")]
CN = {}
for f, key in SPEC:
    p = os.path.join(HD2, f)
    if not os.path.exists(p):
        continue
    ns = {}
    exec(open(p, encoding="utf-8-sig").read(), ns)
    for k, v in (ns.get(key) or {}).items():
        if isinstance(k, str) and isinstance(v, str) and k not in CN:
            CN[k] = v
print("词表 %d 条" % len(CN))

ESC = {'n': '\n', 'r': '\r', 't': '\t', '\\': '\\', "'": "'", '"': '"', 'a': '\a', 'b': '\b', 'f': '\f', 'v': '\v'}

def unesc(s):
    """把 Lua 字面量里的转义还原成运行时真正的字符。"""
    if '\\' not in s:
        return s
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 < len(s):
            out.append(ESC.get(s[i + 1], s[i + 1])); i += 2
        else:
            out.append(c); i += 1
    return ''.join(out)

def split_args(s):
    out, depth, buf, q, esc = [], 0, [], None, False
    for ch in s:
        if esc:
            buf.append(ch); esc = False; continue
        if ch == "\\":
            buf.append(ch); esc = True; continue
        if q:
            buf.append(ch)
            if ch == q: q = None
            continue
        if ch in "'\"":
            q = ch; buf.append(ch); continue
        if ch in "([{": depth += 1
        elif ch in ")]}": depth -= 1
        if ch == "," and depth == 0:
            out.append("".join(buf).strip()); buf = []
        else:
            buf.append(ch)
    if buf: out.append("".join(buf).strip())
    return out

def unq(x):
    x = x.strip()
    if len(x) >= 2 and x[0] in "'\"" and x[-1] == x[0]:
        return unesc(x[1:-1])
    return None

def scan_calls(t):
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
            if d: res.append(("desc", d))
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
        if u: res.append(("desc", u))
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

def known(s):
    """判定"已覆盖"：原样 / 压缩空白 / 全大写 三种写法任一命中即算已覆盖。"""
    if s in CN or s.upper() in CN:
        return True
    n = re.sub(r"\s+", " ", s)
    return n in CN or n.upper() in CN

LA = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal")
st = json.load(io.open(os.path.join(LA, "hd2a_data.json"), encoding="utf-8"))
mods = [m for m in st["modsList"]["default"]["mods"] if m.get("enabled")]
print("启用模组 %d 个\n" % len(mods))
missing, cov = {}, 0
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
                for kind, s in scan_calls(t) + scan_fields(t):
                    if s not in found: found[s] = kind
    miss = {s: k for s, k in found.items() if not known(s)}
    cov += len(found) - len(miss)
    if miss: missing[lab] = miss

tot = sum(len(v) for v in missing.values())
print("缺失 %d 个模组 / %d 条（已覆盖 %d 条）\n" % (len(missing), tot, cov))
for lab, d in sorted(missing.items(), key=lambda x: -len(x[1])):
    print("【%s】缺 %d 条" % (lab, len(d)))
    for s, k in d.items():
        print("   [%s] %s" % (k, s[:160]))
io.open(os.path.join(HD2, "_missing2.json"), "w", encoding="utf-8").write(
    json.dumps(missing, ensure_ascii=False, indent=1))
print("\n已写入 _missing2.json")
