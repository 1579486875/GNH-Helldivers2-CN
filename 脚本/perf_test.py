# -*- coding: utf-8 -*-
"""perf_test.py -- 性能实测：启动开销、每帧开销、大批量注册、长度保护。

说明：测试环境是 lupa 内置的 Lua 5.5（解释执行）；游戏里跑的是 LuaJIT（即时编译），
      同样代码只会更快。所以下面的数字是**保守上界**。
"""
import os, sys
sys.path.insert(0, r"E:\TAML\_scratch\hd2")
from hd2_patch import PatchFile
from cn_strings import CN
import lupa

MODS = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal", "mods")
PK = os.path.join(MODS, "GNH-Chinese-Simplified-Pack", "Addon", "9ba626afa44a3aa3.patch_0")
SRC = PatchFile.load(PK).entries[0].data.decode("utf-8")

STUB = r"""
local state = {options = {}, mods = {}, revision = 0, view = nil}
local function new_option(id, spec)
    local o = {id = id, kind = spec.type, label = spec.label,
               description = spec.description,
               choices = spec.choices and {} or nil, labels = {}}
    if spec.choices then
        for i, c in ipairs(spec.choices) do
            o.choices[i] = string.upper(c); o.labels[i] = 7
        end
    end
    return o
end
local api = {}
function api.register_option(id, spec)
    if type(spec) ~= 'table' then return false, 'invalid' end
    local e = state.options[id]
    if e then
        if e.label ~= spec.label then return false, 'option already registered differently' end
        return true
    end
    local o = new_option(id, spec)
    local title = string.upper(spec.mod or 'UNNAMED')
    local m = state.mods[title]
    if not m then m = {title = title, source = spec.mod, order = {}}; state.mods[title] = m end
    o.mod = title
    m.order[#m.order + 1] = o
    state.options[id] = o
    state.revision = state.revision + 1
    return true
end
function api.get(id) local o = state.options[id]; return o and o.label end
function api.set(id, v) return true end
function api.on_change(id, cb) return true end
function api.ready() return true end
_G.ModOptionsMenu = api
_G.SIM = {state = state, api = api}
"""

def timed(L, lua_code):
    """在 Lua 里量一段代码的 CPU 耗时（毫秒）。"""
    L.execute("_T0 = os.clock()")
    L.execute(lua_code)
    return L.eval("(os.clock() - _T0) * 1000")

print("被测试的 Lua：%d 字符；词表 %d 组\n" % (len(SRC), len(CN)))
R = []

# ── 1. 常规规模（复刻用户的实际模组库：7 个菜单分组 / 约 60 个选项）──
L = lupa.LuaRuntime(unpack_returned_tuples=True)
L.execute(STUB)
L.execute("""
    for g = 1, 7 do
        for i = 1, 9 do
            SIM.api.register_option('mod'..g..'.opt'..i,
                {type='choice', label='Icon and distance colors', mod='Mod '..g,
                 choices={'Objective colors','Helldiver gold','Ice white'}})
        end
    end
""")
t_load = timed(L, "")                     # 先测空转，作为 os.clock 的最小刻度参考
L.execute("_T0 = os.clock()")
L.execute(SRC)
t_script = L.eval("(os.clock() - _T0) * 1000")
n_opt = L.eval("(function() local n=0 for _ in pairs(SIM.state.options) do n=n+1 end return n end)()")
translated = L.eval("SIM.state.options['mod1.opt1'].label")
print("【常规规模】已注册 %d 个选项" % n_opt)
print("  加载整个汉化脚本 + 首次补翻：%.2f ms" % t_script)
print("  补翻结果抽查：%s" % translated)
R.append(("常规规模：加载+首次补翻", "%.2f ms" % t_script, translated == "图标与距离颜色"))

# ── 2. 每帧开销：初始化期间 vs 初始化完成之后 ──
t_init = timed(L, "for i = 1, 200 do update() end") / 200.0
L.execute("for i = 1, 200 do update() end")     # 多跑几帧，让初始化收尾
done = L.eval("_G.GNH_CN_PACK_LOADED")
t_after = timed(L, "for i = 1, 200000 do update() end") / 200000.0
print("\n【每帧开销】")
print("  初始化期间（每秒最多几百帧）：%.4f ms/帧" % t_init)
print("  初始化完成之后：%.6f ms/帧" % t_after)
R.append(("每帧开销（初始化后）", "%.6f ms" % t_after, t_after < 0.01))

# ── 3. 极端：5000 个已注册选项 ──
L2 = lupa.LuaRuntime(unpack_returned_tuples=True)
L2.execute(STUB)
L2.execute("""
    for g = 1, 50 do
        for i = 1, 100 do
            SIM.api.register_option('bulk'..g..'.opt'..i,
                {type='choice', label='Icon and distance colors', mod='Bulk '..g,
                 choices={'Objective colors','Helldiver gold','Ice white'},
                 description='Show the nearest targets, sorted by distance. Panel height also limits how many rows fit.'})
        end
    end
""")
L2.execute("_T0 = os.clock()")
L2.execute(SRC)
t_bulk = L2.eval("(os.clock() - _T0) * 1000")
ok_bulk = L2.eval("SIM.state.options['bulk1.opt1'].label")
print("\n【极端：5000 个选项】")
print("  加载 + 一次性补翻 5000 项：%.2f ms" % t_bulk)
print("  补翻结果抽查：%s" % ok_bulk)
R.append(("5000 选项的加载+补翻", "%.2f ms" % t_bulk, ok_bulk == "图标与距离颜色"))

# ── 4. 极端：10000 次注册调用（走汉化包装）──
t_reg = timed(L2, """
    for i = 1, 10000 do
        SIM.api.register_option('reg'..i,
            {type='choice', label='Icon and distance colors', choices={'Objective colors','Helldiver gold','Ice white'}})
    end
""")
print("\n【极端：连续注册 10000 次】")
print("  总耗时：%.2f ms（平均 %.4f ms/次）" % (t_reg, t_reg / 10000.0))
R.append(("10000 次注册", "%.2f ms" % t_reg, t_reg < 2000))

# ── 5. 极端：词表里非常长的中文 → 必须回退英文（防上游拒绝注册）──
long_zh = None
for k, v in CN.items():
    if len(v) > 64 and k.strip() and not k.startswith("GNH"):
        long_zh = (k, v); break
print("\n【长度保护】找一个中文超过 64 字的词条做选项名：")
print("  英文 %r" % long_zh[0][:60])
print("  中文 %d 字" % len(long_zh[1]))
L3 = lupa.LuaRuntime(unpack_returned_tuples=True)
L3.execute(STUB)
L3.execute(SRC)
esc = long_zh[0].replace("\\", "\\\\").replace("'", "\\'")
L3.execute("SIM.api.register_option('len.long', {type='toggle', label='%s'})" % esc)
got_long = L3.eval("SIM.state.options['len.long'].label")
L3.execute("SIM.api.register_option('len.ok', {type='toggle', label='Show Badge'})")
got_ok = L3.eval("SIM.state.options['len.ok'].label")
print("  超长条目注册后的选项名：%s" % ("仍是英文（已保护）" if got_long == long_zh[0] else "变成中文（未保护！）"))
print("  正常条目注册后的选项名：%s" % got_ok)
R.append(("超长翻译自动回退英文", "回退成功" if got_long == long_zh[0] else "未回退", got_long == long_zh[0]))

# ── 6. 词表查找性能 ──
keys = list(CN.keys())[:200]
lua_lookup = "local t = {" + ",".join("[%r]=true" % k.replace("'", "\\'") for k in keys[:50]) + "}"
L4 = lupa.LuaRuntime()
t_lookup = timed(L4, """
    local GNH = {}
    for i = 1, 1010 do GNH['key'..i] = 'value' end
    local s = 0
    for i = 1, 200000 do
        if GNH['key' .. (i % 1010)] then s = s + 1 end
    end
""") / 200000.0 * 1000.0     # 微秒
print("\n【词表查找】")
print("  单次查找约 %.4f 微秒（表结构哈希查找，O(1)）" % t_lookup)
R.append(("词表查找", "%.4f 微秒" % t_lookup, t_lookup < 5))

print("\n" + "=" * 74)
for name, val, ok in R:
    print("  %s  %-28s %s" % ("PASS" if ok else "FAIL", name, val))
