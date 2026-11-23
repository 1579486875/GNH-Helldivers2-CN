# -*- coding: utf-8 -*-
"""perf_exact.py -- 精确测量：分开统计"初始化期间"和"初始化完成之后"的每帧开销。"""
import os, sys
sys.path.insert(0, r"E:\TAML\_scratch\hd2")
from hd2_patch import PatchFile
import lupa

PK = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal", "mods",
                  "GNH-Chinese-Simplified-Pack", "Addon", "9ba626afa44a3aa3.patch_0")
SRC = PatchFile.load(PK).entries[0].data.decode("utf-8")

STUB = r"""
local state = {options = {}, mods = {}, revision = 0, view = nil}
local function new_option(id, spec)
    local o = {id = id, kind = spec.type, label = spec.label, description = spec.description,
               choices = spec.choices and {} or nil, labels = {}}
    if spec.choices then
        for i, c in ipairs(spec.choices) do o.choices[i] = string.upper(c); o.labels[i] = 7 end
    end
    return o
end
local api = {}
function api.register_option(id, spec)
    if type(spec) ~= 'table' then return false, 'invalid' end
    local e = state.options[id]
    if e then if e.label ~= spec.label then return false, 'differ' end return true end
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
function api.get(id) return state.options[id] end
function api.set(id, v) return true end
function api.on_change(id, cb) return true end
function api.ready() return true end
_G.ModOptionsMenu = api
_G.SIM = {state = state}
for g = 1, 7 do
    for i = 1, 9 do
        api.register_option('m'..g..'.o'..i, {type='choice', label='Icon and distance colors', mod='Mod '..g,
            choices={'Objective colors','Helldiver gold','Ice white'}})
    end
end
"""

L = lupa.LuaRuntime(unpack_returned_tuples=True)
L.execute(STUB)
L.execute(SRC)

def ms(code):
    L.execute("_T = os.clock()")
    L.execute(code)
    return L.eval("(os.clock() - _T) * 1000")

# 初始化期间：还没收工的那几十帧
t_init = ms("for i = 1, 150 do update() end") / 150.0
print("初始化期间（尚未收工）：%.4f ms/帧" % t_init)

# 一口气跑到收工
ms("for i = 1, 1400 do update() end")

# 收工之后：大幅采样
t_after = ms("for i = 1, 300000 do update() end") / 300000.0
print("初始化完成之后：        %.6f ms/帧" % t_after)
print()
print("折算成 60fps 的 CPU 占用：初始化期间 %.4f%%，完成后 %.6f%%"
      % (t_init / (1000.0 / 60) * 100, t_after / (1000.0 / 60) * 100))
print("说明：这里跑的是 lupa 的 Lua 5.5 解释器；游戏里是 LuaJIT（即时编译），同一段代码只会更快，")
print("      所以上面的数字是保守上界。")
