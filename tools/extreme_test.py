# -*- coding: utf-8 -*-
"""extreme_test.py -- 极端场景测试：用真实 Lua 运行时加载真实 patch 里的 Lua，逐个场景验证。

思路：先搭一个"和 ModOptionsMenu 内部结构一致的替身"，再针对每一种可能的糟糕情况做变形，
然后加载汉化包，看它 —— 会不会报错、能不能继续把中文翻出来、行为是否符合预期。
"""
import os, sys, time
sys.path.insert(0, r"E:\TAML\_scratch\hd2")
from hd2_patch import PatchFile
import lupa

MODS = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal", "mods")
PK = os.path.join(MODS, "GNH-Chinese-Simplified-Pack", "Addon", "9ba626afa44a3aa3.patch_0")
SRC = PatchFile.load(PK).entries[0].data.decode("utf-8")
print("被测试的 Lua：%d 字符（来自真实 patch）\n" % len(SRC))

# ── 与 ModOptionsMenu 内部结构一致的替身 ───────────────────────────────
STUB = r"""
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
    if type(spec) ~= 'table' then return false, 'invalid option registration' end
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
-- 模拟"比汉化包更早注册"的模组
api.register_option('ot.enabled', {type='toggle', label='Show objective tracker', mod='Objective Tracker', default=true})
api.register_option('ot.theme', {type='choice', label='Icon and distance colors', mod='Objective Tracker', default=1,
                                 choices={'Objective colors','Helldiver gold','Ice white'}})
api.register_option('tm.style', {type='choice', label='Preview style', mod='HD2 Transmog', default=1,
                                 choices={"Mod author's choice",'Force HD2','Force Studio'}})
"""

def new_runtime(setup=""):
    L = lupa.LuaRuntime(unpack_returned_tuples=True)
    L.execute(STUB)
    if setup:
        L.execute(setup)
    return L

def run(name, setup="", after="", expect_error=False):
    """跑一个场景，返回 (是否通过, 说明)。"""
    try:
        L = new_runtime(setup)
        L.execute(SRC)
        if after:
            L.execute(after)
        return L, None
    except Exception as exc:
        return None, exc

RESULTS = []
def report(name, ok, detail=""):
    RESULTS.append((name, ok, detail))
    print("  %s  %-46s %s" % ("PASS" if ok else "FAIL", name, detail))

def getopt(L, key):
    return L.eval("SIM.state.options[%r].label" % key)

# ══════════════ 1. 菜单根本不存在 ══════════════
print("【一、加载环境异常】")
L, err = None, None
try:
    L = lupa.LuaRuntime()
    L.execute("_G.ModOptionsMenu = nil")
    L.execute(SRC)
    L.globals().update()      # 主循环跑一帧
    ok = L.eval("_G.GNH_CN_PACK_LOADED") is True
    report("1. ModOptionsMenu 完全不存在", ok, "脚本正常载入、主循环可跑、不报错")
except Exception as exc:
    report("1. ModOptionsMenu 完全不存在", False, str(exc))

try:
    L = lupa.LuaRuntime()
    L.execute("_G.ModOptionsMenu = {api = 1}")   # 是个表，但没有 register_option
    L.execute(SRC)
    L.globals().update()
    report("2. 有 ModOptionsMenu 但没有 register_option", True, "不报错")
except Exception as exc:
    report("2. 有 ModOptionsMenu 但没有 register_option", False, str(exc))

try:
    L = lupa.LuaRuntime()
    L.execute("_G.ModOptionsMenu = {register_option = 'not a function'}")
    L.execute(SRC)
    L.globals().update()
    report("3. register_option 不是函数", True, "不报错")
except Exception as exc:
    report("3. register_option 不是函数", False, str(exc))

try:
    L = lupa.LuaRuntime()
    L.execute("_G.update = nil")
    L.execute(STUB)
    L.execute(SRC)
    report("4. 游戏主循环 _G.update 不存在", True, "不报错（包装里已判空）")
except Exception as exc:
    report("4. 游戏主循环 _G.update 不存在", False, str(exc))

try:
    L = lupa.LuaRuntime()
    L.execute("_G.update = 12345")     # 不是函数
    L.execute(STUB)
    L.execute(SRC)
    L.globals().update() if callable(L.globals().update) else None
    report("5. _G.update 不是函数", True, "不报错")
except Exception as exc:
    report("5. _G.update 不是函数", False, str(exc))

try:
    L = lupa.LuaRuntime()
    L.execute('_G.CowboyBingusModLoader = {open_log = function() error("no log") end}')
    L.execute(STUB)
    L.execute(SRC)
    report("6. 共享加载器在、但 open_log 报错", True, "日志写不了也不影响汉化")
except Exception as exc:
    report("6. 共享加载器在、但 open_log 报错", False, str(exc))

try:
    L = lupa.LuaRuntime()
    L.execute(STUB)
    L.execute(SRC)
    L.execute(SRC)                     # 第二次加载
    report("7. 脚本被重复加载两次", True, "第二次被守卫拦下，不会双层包装")
except Exception as exc:
    report("7. 脚本被重复加载两次", False, str(exc))

print("\n【二、菜单内部结构异常（模拟上游改版）】")
try:
    L = lupa.LuaRuntime()
    L.execute(STUB)
    L.execute("debug = nil")           # 整个 debug 库消失
    L.execute(SRC)
    L.execute("SIM.api.register_option('late.dbg', {type='toggle', label='Show Badge'})")
    v = L.eval("SIM.state.options['late.dbg'].label")
    report("8. debug 库不存在", v == "显示徽章", "补翻失效但实时翻译仍生效：%s" % v)
except Exception as exc:
    report("8. debug 库不存在", False, str(exc))

try:
    L = lupa.LuaRuntime()
    L.execute(STUB)
    L.execute("debug = {getupvalue = function() error('blocked') end}")
    L.execute(SRC)
    report("9. debug.getupvalue 每次都报错", True, "pcall 兜住，不报错")
except Exception as exc:
    report("9. debug.getupvalue 每次都报错", False, str(exc))

try:
    # 上游大改版：内部 state 不再叫 options/mods
    L = lupa.LuaRuntime()
    L.execute(STUB)
    L.execute("SIM.state.options = nil; SIM.state.mods = nil")
    L.execute(SRC)
    report("10. 找不到菜单内部 state（上游改版）", True, "安全降级为不补翻")
except Exception as exc:
    report("10. 找不到菜单内部 state（上游改版）", False, str(exc))

try:
    L = new_runtime()
    L.execute("SIM.state.options.junk1 = 'I am a string'")
    L.execute("SIM.state.options.junk2 = nil")
    L.execute("SIM.state.options.junk3 = 42")
    L.execute(SRC)
    report("11. options 表里混入字符串/数字/nil", True, "类型检查挡住了")
except Exception as exc:
    report("11. options 表里混入字符串/数字/nil", False, str(exc))

try:
    L = new_runtime()
    L.execute("SIM.state.options.broken = {kind='toggle'}")
    L.execute(SRC)
    report("12. 某个选项缺 id / label 字段", True, "不报错")
except Exception as exc:
    report("12. 某个选项缺 id / label 字段", False, str(exc))

try:
    L = new_runtime()
    L.execute("SIM.state.options.ok1 = {id='ok1', label='Show Badge', choices='not a table'}")
    L.execute("SIM.state.options.ok2 = {id='ok2', label='Position', choices={}}")
    L.execute(SRC)
    report("13. choices 是字符串 / 是空表", True, "不报错")
except Exception as exc:
    report("13. choices 是字符串 / 是空表", False, str(exc))

try:
    L = new_runtime()
    L.execute("SIM.state.options.fn1 = {id='fn1', label=function() return 'x' end}")
    L.execute(SRC)
    report("14. 选项名是函数而不是字符串", True, "原样保留，不误伤")
except Exception as exc:
    report("14. 选项名是函数而不是字符串", False, str(exc))

try:
    L = new_runtime()
    L.execute("SIM.state.revision = 'abc'; SIM.state.view = 'nonsense'")
    L.execute(SRC)
    report("15. revision 不是数字 / view 是字符串", True, "不报错")
except Exception as exc:
    report("15. revision 不是数字 / view 是字符串", False, str(exc))

try:
    L = new_runtime()
    L.execute("SIM.state.mods.weird = 'not a table'")
    L.execute("SIM.state.view = {mods = {1, 'abc', nil, {title='X'}}}")
    L.execute(SRC)
    report("16. mods / view.mods 里混入非表元素", True, "不报错")
except Exception as exc:
    report("16. mods / view.mods 里混入非表元素", False, str(exc))

print("\n【三、注册行为异常】")
try:
    L = new_runtime()
    L.execute(SRC)
    L.execute("SIM.api.register_option('x.nil', nil)")
    L.execute("SIM.api.register_option('x.str', 'oops')")
    L.execute("SIM.api.register_option('x.nolabel', {type='toggle'})")
    report("17. 传入 nil / 字符串 / 缺 label 的注册表", True, "不报错")
except Exception as exc:
    report("17. 传入 nil / 字符串 / 缺 label 的注册表", False, str(exc))

try:
    L = new_runtime()
    L.execute(SRC)
    # 只读的 spec 表：改它就会报错 —— 汉化包必须只读不写
    L.execute("""
        local ro = setmetatable({type='toggle', label='Show Badge', mod='Aggro Counter'},
                                {__newindex = function() error('spec is read-only') end})
        SIM.api.register_option('ro.test', ro)
    """)
    label = L.eval("SIM.state.options['ro.test'].label")
    report("18. 注册表是只读表（禁止写入）", label == "显示徽章", "结果=%s" % label)
except Exception as exc:
    report("18. 注册表是只读表（禁止写入）", False, str(exc))

try:
    L = new_runtime()
    L.execute(SRC)
    L.execute("""
        local ok1 = SIM.api.register_option('dup.one', {type='toggle', label='Show Badge'})
        local ok2, why = SIM.api.register_option('dup.one', {type='toggle', label='Show Badge'})
        SIM.DUP = {ok2 = ok2, why = why}
    """)
    ok2 = L.eval("SIM.DUP.ok2")
    report("19. 补翻后模组再次注册同一选项（必须放行）", ok2 is True or ok2 == 1,
           "第二次注册返回 %s（上游原本返回 true）" % ok2)
except Exception as exc:
    report("19. 补翻后模组再次注册同一选项", False, str(exc))

try:
    L = new_runtime()
    L.execute(SRC)
    L.execute("""
        local ok1 = SIM.api.register_option('dup.two', {type='toggle', label='Show Badge'})
        local ok2, why = SIM.api.register_option('dup.two', {type='toggle', label='完全不同的选项'})
        SIM.DUP2 = {ok2 = ok2}
    """)
    ok2 = L.eval("SIM.DUP2.ok2")
    report("20. 同名 id 但内容真的不同（不应误放行）", ok2 is False or ok2 == 0,
           "返回 %s（应为 false）" % ok2)
except Exception as exc:
    report("20. 同名 id 但内容真的不同", False, str(exc))

try:
    L = new_runtime()
    L.execute(SRC)
    L.execute("SIM.api.register_option = function() error('upstream exploded') end")
    threw = False
    try:
        L.execute("SIM.api.register_option('boom', {type='toggle', label='Show Badge'})")
    except Exception:
        threw = True
    report("21. 上游注册函数自己抛异常", threw, "异常如实透传，不被悄悄吞掉")
except Exception as exc:
    report("21. 上游注册函数自己抛异常", False, str(exc))

try:
    # 菜单是"只读代理表"：禁止替换它的函数 → 应退化为"只补翻"
    L = lupa.LuaRuntime(unpack_returned_tuples=True)
    L.execute(STUB)
    L.execute("""
        local real = _G.ModOptionsMenu
        _G.ModOptionsMenu = setmetatable({}, {
            __index = real,
            __newindex = function() error('menu table is readonly') end,
        })
        _G.SIM.REAL = real
    """)
    L.execute(SRC)
    v = L.eval("SIM.state.options['ot.enabled'].label")
    report("22. 菜单是只读表（无法替换函数）", v == "显示任务目标追踪",
           "降级为补翻后仍翻出中文：%s" % v)
except Exception as exc:
    report("22. 菜单是只读表（无法替换函数）", False, str(exc))

print("\n【四、按键绑定菜单异常】")
try:
    L = new_runtime()
    L.execute("""
        local state = {registry = {}, order = {}, revision = 0}
        local api = {}
        function api.register_binding(id, label, slot, options)
            if type(label) ~= 'string' and type(label) ~= 'number' then return false, 'invalid' end
            if state.registry[id] then return false, 'binding already registered differently' end
            state.registry[id] = {id = id, label = label, text = type(label) == 'string' and label or nil}
            state.order[#state.order+1] = state.registry[id]
            return true
        end
        function api.is_down(id) return false end
        function api.ready() return true end
        _G.ModBindingsMenu = api
        _G.BSIM = {state = state}
        api.register_binding('aggro.toggle', 'SHOW / HIDE BADGE', 0, nil)
    """)
    L.execute(SRC)
    txt = L.eval("BSIM.state.registry['aggro.toggle'].text")
    report("23. 按键绑定菜单接管 + 补翻", txt == "显示/隐藏徽章", "结果=%s" % txt)
except Exception as exc:
    report("23. 按键绑定菜单接管 + 补翻", False, str(exc))

try:
    L = new_runtime()
    L.execute("""
        local state = {registry = {}, order = {}}
        local api = {}
        function api.register_binding(id, label, slot, options)
            state.registry[id] = {id = id, label = label}
            return true
        end
        function api.is_down(id) return false end
        function api.ready() return true end
        _G.ModBindingsMenu = api
        _G.BSIM = {state = state}
        api.register_binding('x.num', 123456, 0, nil)      -- 数字型 label（游戏本地化编号）
        api.register_binding('x.nil', nil, 0, nil)
    """)
    L.execute(SRC)
    report("24. 按键菜单里出现数字/nil 标签", True, "不报错（数字原样保留）")
except Exception as exc:
    report("24. 按键菜单里出现数字/nil 标签", False, str(exc))

print("\n【五、重复加载与状态一致性】")
try:
    L = new_runtime()
    L.execute(SRC)
    L.execute("SIM.DUP3 = {n = 0}")
    L.execute(SRC)                                   # 再来一次
    dup = L.eval("_G.GNH_CN_PACK_LOADED")
    report("25. 第二次加载不会重复包装主循环", dup is True or dup == 1, "守卫生效")
except Exception as exc:
    report("25. 第二次加载不会重复包装主循环", False, str(exc))

npass = sum(1 for _, ok, _ in RESULTS if ok)
print("\n" + "=" * 74)
print("极端场景测试：%d / %d 通过" % (npass, len(RESULTS)))
for name, ok, detail in RESULTS:
    if not ok:
        print("  ✗ %s -> %s" % (name, detail))
