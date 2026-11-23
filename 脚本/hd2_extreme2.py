# -*- coding: utf-8 -*-
"""hd2_extreme2.py -- 极端场景测试（动态发现路径，不再写死目录名）。"""
import os, sys, io, re
from hd2_patch import PatchFile
from lupa import LuaRuntime
MODS = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal", "mods")
buf = io.StringIO(); W = lambda *a: print(*a, file=buf)
def find_pack(*kw):
    for n in sorted(os.listdir(MODS)):
        p = os.path.join(MODS, n)
        if os.path.isdir(p) and all(k in n for k in kw):
            pp = os.path.join(p, "Addon", "9ba626afa44a3aa3.patch_0")
            if os.path.exists(pp): return p
    return None
MAIN = find_pack("GNH", "Helldivers2"); OPT = find_pack("GNH", "Transmog")
pm = PatchFile.load(os.path.join(MAIN, "Addon", "9ba626afa44a3aa3.patch_0"))
po = PatchFile.load(os.path.join(OPT, "Addon", "9ba626afa44a3aa3.patch_0"))
FRAG = pm.entries[0].data.decode("utf-8", "replace").replace("\x00", "")
W("主包: %s | 可选包: %s" % (os.path.basename(MAIN), os.path.basename(OPT)))
W("")
W("=== 主包：极端场景（真实 Lua 执行）===")
def scen(label, body, keys, pre_extra="", host="immediate", update=True, loader=True):
    L = LuaRuntime(unpack_returned_tuples=True)
    pre = "local RC, LOG = {}, {}\n_G.print = function(...) local t={...}; LOG[#LOG+1]=tostring(t[1]) end\n"
    if update: pre += "_G.update = function() end\n"
    if loader: pre += "_G.CowboyBingusModLoader = { open_log = function(n) return nil end }\n"
    pre += pre_extra
    if host == "immediate":
        pre += "_G.MOM = { api = 1, register_option = function(id, spec) RC[#RC+1] = {id=id, spec=spec}; return true end }\n_G.ModOptionsMenu = _G.MOM\n"
    else:
        pre += "_G.ModOptionsMenu = nil\n"
    w = "local C = assert(load([===[%s]===], 'gnh'))\nC()\n" % FRAG
    if host == "delayed":
        w += "_G.MOM = { api = 1, register_option = function(id, spec) RC[#RC+1] = {id=id, spec=spec}; return true end }\n_G.ModOptionsMenu = _G.MOM\n_G.update()\n"
    try:
        L.execute(pre + w + body)
        g = L.globals().RET
        W("  %-38s -> %s" % (label, {k: g[k] for k in keys}))
    except Exception as exc:
        W("  %-38s -> EXC: %s" % (label, str(exc)[:110]))

scen("1 正常（host 已就绪）", """
_G.MOM.register_option('a', {type='toggle', label='Show Badge'})
RET = { label = RC[1].spec.label, hooked = (table.concat(LOG,'|')):find('已接管') ~= nil }
""", ["label", "hooked"])
scen("2 host 延迟（走 update 轮询）", """
_G.MOM.register_option('b', {type='toggle', label='Tank Power'})
RET = { label = RC[1] and RC[1].spec.label, hooked = (table.concat(LOG,'|')):find('已接管') ~= nil }
""", ["label", "hooked"], host="delayed")
scen("3 无 host 也无 update", """
RET = { loaded = tostring(_G.GNH_CN_PACK_LOADED) }
""", ["loaded"], host="delayed", update=False)
scen("4 无 Bingus loader", """
_G.MOM.register_option('c', {type='toggle', label='Show Badge'})
RET = { label = RC[1].spec.label }
""", ["label"], loader=False)
scen("5 print 抛错", """
_G.MOM.register_option('d', {type='toggle', label='Show Badge'})
RET = { label = RC[1].spec.label }
""", ["label"], pre_extra="_G.print = function() error('print broken') end\n")
scen("6 _G 带元表", """
_G.MOM.register_option('e', {type='toggle', label='Show Badge'})
RET = { label = RC[1].spec.label }
""", ["label"], pre_extra="setmetatable(_G, {__index=function() return nil end, __newindex=function(t,k,v) rawset(t,k,v) end})\n")
scen("7 register_option 被别人先包装", """
_G.MOM.register_option('f', {type='toggle', label='Show Badge'})
RET = { label = RC[1].spec.label, flag = RC[1].spec.outer == true }
""", ["label", "flag"],
    pre_extra="_G.ModOptionsMenu = { api = 1, register_option = function(id, spec) spec.outer = true; RC[#RC+1] = {id=id, spec=spec}; return true end }\n")
scen("8 choices 只读表", """
local ch = setmetatable({'Off','Strong (x1.25)'}, {__newindex = function() error('ro') end})
local ok = pcall(_G.MOM.register_option, 'g', {type='choice', label='Tank Power', choices=ch})
RET = { call_ok = ok, c2 = RC[1] and RC[1].spec.choices[2], untouched = ch[2] == 'Strong (x1.25)' }
""", ["call_ok", "c2", "untouched"])
scen("9 label 靠元表提供（浅拷贝会丢）", """
local spec = setmetatable({type='toggle'}, {__index=function(_,k) if k=='label' then return 'Show Badge' end end})
local ok = pcall(_G.MOM.register_option, 'h', spec)
RET = { call_ok = ok, passthrough = RC[1] and RC[1].spec == spec }
""", ["call_ok", "passthrough"])
scen("10 非字符串/特殊字符/超长文本", """
_G.MOM.register_option('i', {type='toggle', label=12345})
_G.MOM.register_option('j', {type='toggle', label='quote\\' and "dq"'})
_G.MOM.register_option('k', {type='toggle', label=string.rep('X',300)})
RET = { num = RC[1].spec.label, weird_ok = type(RC[2].spec.label)=='string', long_kept = RC[3].spec.label == string.rep('X',300) }
""", ["num", "weird_ok", "long_kept"])
scen("11 已是中文的文本不二次处理", """
_G.MOM.register_option('l', {type='toggle', label='更多的汉化文本'})
RET = { kept = RC[1].spec.label == '更多的汉化文本' }
""", ["kept"])
scen("12 重复加载（两个 chunk）", """
_G.MOM.register_option('m', {type='toggle', label='Show Badge'})
RET = { label = RC[1].spec.label, skipped = (table.concat(LOG,'|')):find('重复加载') ~= nil }
""", ["label", "skipped"])

W("")
W("=== 可选包：结构与内容 ===")
L = LuaRuntime(unpack_returned_tuples=True)
loader = L.eval("function(c,n) local f,e = load(c,n); return f ~= nil, e end")
for e in po.entries:
    code = e.data.decode("utf-8", "replace").replace("\x00", "")
    ok, err = loader(code, "tm")
    W("  Lua 编译: %s" % ("成功" if ok else ("失败 " + str(err)[:80])))
tm = po.entries[0].data.decode("utf-8", "replace")
for k in ("不含被动加成", "已装备", "保存变体", "创建变体", "移除变体", "外观", "被动", "基础属性", "合计"):
    W("    %-10s 已汉化=%s" % (k, k in tm))
pat = re.compile(r"(==|~=)\s*'([^']{1,80})'|'([^']{1,80})'\s*(==|~=)")
zh = [m.group(0) for m in pat.finditer(tm) if any("\u4e00" <= c <= "\u9fff" for c in (m.group(2) or m.group(3) or ""))]
W("  比较表达式含中文: %d（应 0）" % len(zh))
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes", "hd2_extreme2.txt"),"w",encoding="utf-8").write(buf.getvalue())
print("ok")
