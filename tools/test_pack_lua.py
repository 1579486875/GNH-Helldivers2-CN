# -*- coding: utf-8 -*-
"""test_pack_lua.py -- 用真实 Lua 运行环境验证包 A 的运行时接管 + 补翻逻辑。

构造一个与 ModOptionsMenu 内部结构一致的替身（state.options / state.mods / revision），
先注册几个"比汉化包更早注册"的选项，再加载汉化包的 Lua，检查：
  * 语法能编译、执行不报错
  * 先注册的选项被就地补翻（label / description / choices / 模组名）
  * 之后注册的选项被实时翻译
"""
import sys, os
sys.path.insert(0, r"E:\TAML\_scratch\hd2")
from hd2_patch import PatchFile
import lupa

MODS = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal", "mods")
PK = os.path.join(MODS, "GNH-Chinese-Simplified-Pack", "Addon", "9ba626afa44a3aa3.patch_0")
src = PatchFile.load(PK).text(0)
print("包 A Lua %d 字符" % len(src))

PRELUDE = r"""
local state = {options = {}, mods = {}, revision = 0, view = nil}
local function new_option(id, spec)
    local o = {id = id, kind = spec.type, label = spec.label,
               description = spec.description,
               choices = spec.choices and {} or nil, labels = {}}
    if spec.choices then
        for i, c in ipairs(spec.choices) do
            o.choices[i] = string.upper(c)
            o.labels[i] = 7
        end
    end
    return o
end
local api = {}
function api.register_option(id, spec)
    if state.options[id] then return false, 'option already registered differently' end
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
-- 模拟"比汉化包更早注册"的模组（Objective Tracker 的全部 17 个选项里抽几个）
api.register_option('codex.objective_tracker.enabled',
    {type = 'toggle', label = 'Show objective tracker', mod = 'Objective Tracker', default = true})
api.register_option('codex.objective_tracker.theme',
    {type = 'choice', label = 'Icon and distance colors', mod = 'Objective Tracker', default = 1,
     choices = {'Objective colors', 'Helldiver gold', 'Ice white'}})
api.register_option('codex.objective_tracker.rows',
    {type = 'slider', label = 'Maximum visible targets', mod = 'Objective Tracker', default = 5,
     min = 3, max = 8, step = 1,
     description = 'Show the nearest targets, sorted by distance. Panel height also limits how many rows fit.'})
-- 模拟另一个也要汉化的模组（HD2 Transmog）
api.register_option('hd2tm.preview.style',
    {type = 'choice', label = 'Preview style', mod = 'HD2 Transmog', default = 1,
     choices = {"Mod author's choice", 'Force HD2', 'Force Studio'}})
STATE_BEFORE = state
"""

CHECK = r"""
local st = STATE_BEFORE
local out = {}
out.revision = st.revision
out.n_options = 0
for _ in pairs(st.options) do out.n_options = out.n_options + 1 end
out.enabled_label = st.options['codex.objective_tracker.enabled'].label
out.theme_label = st.options['codex.objective_tracker.theme'].label
out.theme_c1 = st.options['codex.objective_tracker.theme'].choices[1]
out.theme_c2 = st.options['codex.objective_tracker.theme'].choices[2]
out.theme_c3 = st.options['codex.objective_tracker.theme'].choices[3]
out.rows_desc = st.options['codex.objective_tracker.rows'].description
out.tm_label = st.options['hd2tm.preview.style'].label
out.tm_c1 = st.options['hd2tm.preview.style'].choices[1]
out.mod_title = st.mods['OBJECTIVE TRACKER'] and st.mods['OBJECTIVE TRACKER'].title or '<nil>'
return out
"""

REGISTER_LATE = r"""
local api = _G.ModOptionsMenu
api.register_option('late.option.one',
    {type = 'toggle', label = 'Show Badge', mod = 'Aggro Counter', default = true})
return api and 'ok' or 'no-api'
"""

LATE_CHECK = r"""
local st = STATE_BEFORE
return st.options['late.option.one'] and st.options['late.option.one'].label or '<nil>'
"""

L = lupa.LuaRuntime(unpack_returned_tuples=True)
L.execute(PRELUDE)
L.execute(src)
res = L.execute(CHECK)
print("\n=== 加载汉化包后的状态 ===")
for k, v in sorted(res.items()):
    print("  %-14s = %s" % (k, v))
L.execute(REGISTER_LATE)
late = L.execute(LATE_CHECK)
print("\n=== 之后再注册的选项 ===")
print("  late.option.one.label = %s" % late)
print("\n=== 判定 ===")
ok = True
def chk(name, got, want):
    global ok
    good = (str(got) == str(want))
    ok = ok and good
    print("  %s %-46s %s" % ("PASS" if good else "FAIL", name, got))
chk("补翻 toggle label", res["enabled_label"], "显示任务目标追踪")
chk("补翻 choice label", res["theme_label"], "图标与距离颜色")
chk("补翻 choice 值 1", res["theme_c1"], "目标配色")
chk("补翻 choice 值 2", res["theme_c2"], "绝地潜兵金")
chk("补翻 choice 值 3", res["theme_c3"], "冰白")
chk("补翻 description", res["rows_desc"], "显示最近的目标，按距离排序。面板高度也会限制可容纳的行数。")
chk("补翻 Transmog 选项名", res["tm_label"], "预览风格")
chk("补翻 Transmog 选项值", res["tm_c1"], "作者指定")
chk("补翻模组名", res["mod_title"], "目标追踪器")
chk("实时翻译后注册的选项", late, "显示徽章")
print("  revision = %s（注册 5 次后应 > 5）" % res["revision"])
print("\n结论：%s" % ("全部通过" if ok else "存在失败项"))
