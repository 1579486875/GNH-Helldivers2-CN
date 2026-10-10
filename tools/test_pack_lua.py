# -*- coding: utf-8 -*-
"""test_pack10_lua.py -- 用真实 Lua 运行环境验证 2026-10-10 这一轮的新词条。

做法与 test_pack_lua.py 一致：搭一个 ModOptionsMenu 替身（state.options / state.mods），
然后把**刚更新过的模组的真实选项**注册进去，看汉化包能不能把它们变成中文。
重点验证四件事：
  1. 高度警戒 1.9.2 新增的「分色」系列（普通 / 重型 / 炮击）
  2. 装甲大修 3.4.0 新增的选项名、选项值与长说明
  3. C-Rig v0.6 的 IK 说明
  4. 超长文本会被主动放行（宁可显示英文，也不能让选项注册失败）
"""
import sys, os, io, json
sys.path.insert(0, r"E:\TAML\_scratch\hd2")
from hd2_patch import PatchFile
import lupa

LA = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal")
st = json.load(io.open(os.path.join(LA, "hd2a_data.json"), encoding="utf-8"))
PK = [m["path"] for m in st["modsList"]["default"]["mods"]
      if "GNH 简体中文汉化包" in str(m.get("label"))][0]
p = os.path.join(PK, "Addon", "9ba626afa44a3aa3.patch_0")
src = PatchFile.load(p).text(0)
print("包 A：%s" % PK)
print("Lua %d 字符\n" % len(src))

# 真实原文（从模组 patch 里扫出来的，逐字符照抄）
HA_DESC = ("Detection range: 5-30 m; default 12.1 m; step 0.1. "
           "Only living enemies targeting you trigger alerts.")
HA_DESC_LONG = ("Master proximity boost. Rate and radius grow linearly to maximum at 3 m; "
                "brightness and opacity keep their original curves.")
AO_DESC = ("MBT Turrets: where the Bastion and Maelstrom turret sits. Original is the game's place. "
           "Centered puts it in the middle of the hull like a main battle tank: the gun reaches past "
           "the front deck, so it clips less when aimed low. Changes at once. The tank's hit areas "
           "stay the game's own.")
AO_DESC2 = ("Drive from the gunner seat when the driver seat is empty: your movement keys drive, "
            "shift and CTRL change gear, Space is the handbrake. F sounds the horn; Mouse 3 pops the "
            "Maelstrom's smoke. Controller: the left stick drives, its click is the horn, the right "
            "stick click pops smoke. Keys set in the Mod Bindings Menu replace these. A teammate who "
            "takes the wheel drives. Pick which vehicles.")
CRIG_DESC = ("Requires this layout's Custom rig. Off: no IK. On: full IK. Auto: full IK with weapon "
             "contact. Partial: layout XYZ weights. Auto (Partial): full IK with contact, partial "
             "otherwise. Original hand orientation is retained.")

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
    if state.options[id] then return false, 'dup' end
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
STATE = state
"""

REG = r"""
local api = _G.ModOptionsMenu
api.register_option('ha.split', {type = 'toggle', label = 'Split Colors', mod = 'High Alert', default = false})
api.register_option('ha.nradius', {type = 'slider', label = 'Normal Radius', mod = 'High Alert',
    default = 12.1, min = 5, max = 30, step = 0.1, description = DETECT})
api.register_option('ha.ncolor', {type = 'choice', label = 'Normal Color', mod = 'High Alert', default = 1,
    choices = {'Yellow', 'Orange', 'Red', 'Blue', 'White', 'Pink', 'Purple'}})
api.register_option('ha.nboost', {type = 'toggle', label = 'Normal Boost', mod = 'High Alert',
    default = true, description = BOOST})
api.register_option('ha.art', {type = 'toggle', label = 'Artillery On', mod = 'High Alert', default = true,
    description = 'Cannon alerts; highest priority per direction. Includes cannon towers, small turrets, Factory Strider and Vox main cannons.'})
api.register_option('ao.turretpos', {type = 'choice', label = 'Tank Turret Position', mod = 'Armored Overhaul',
    default = 1, choices = {'Original', 'Centered'}, description = TURRET})
api.register_option('ao.loadout', {type = 'toggle', label = 'Vehicle Loadout', mod = 'Armored Overhaul',
    default = false, description = 'Pick more than one tank, exosuit or FRV in your stratagem loadout (the game puts a second one in the first one' .. string.char(39) .. 's slot). Changes at once; turning it off puts the game' .. string.char(39) .. 's limit back.'})
api.register_option('ao.cam', {type = 'choice', label = 'Gunner Camera', mod = 'Armored Overhaul', default = 2,
    choices = {'Close (about 1.5 m back)', 'Far (about 3.5 m back)', 'Farther (about 5 m back)',
               'Farthest (about 6.5 m back)'}, description = GUNNER})
api.register_option('ao.speed', {type = 'choice', label = 'Engine Speed', mod = 'Armored Overhaul', default = 2,
    choices = {'Fast (x1.1)', 'Faster (x1.15)', 'Fastest (x1.3)'}})
api.register_option('ao.steer', {type = 'choice', label = 'Steering Response', mod = 'Armored Overhaul', default = 1,
    choices = {'Quick', 'Quicker', 'Instant'}})
api.register_option('crig.ik', {type = 'choice', label = 'IK Mode', mod = 'Runtime(ShareLoader)', default = 1,
    choices = {'Partial', 'Auto (Partial)'}, description = IK})
api.register_option('long.desc', {type = 'toggle', label = 'Overlong', mod = 'Test', default = false,
    description = string.rep('x', 420)})
STATE = _G.ModOptionsMenu and STATE
"""

CHECK = r"""
local st = STATE
local o = function(id) return st.options[id] end
local out = {}
out.split     = o('ha.split').label
out.nradius   = o('ha.nradius').label
out.nradius_d = o('ha.nradius').description
out.ncolor    = o('ha.ncolor').label
out.ncolor_c  = o('ha.ncolor').choices[1] .. '|' .. o('ha.ncolor').choices[2] .. '|' .. o('ha.ncolor').choices[3] .. '|' .. o('ha.ncolor').choices[7]
out.nboost_d  = o('ha.nboost').description
out.art       = o('ha.art').label
out.art_d     = o('ha.art').description
out.turretpos = o('ao.turretpos').label
out.turret_c  = o('ao.turretpos').choices[1] .. '|' .. o('ao.turretpos').choices[2]
out.turret_d  = o('ao.turretpos').description
out.loadout   = o('ao.loadout').label
out.loadout_d = o('ao.loadout').description
out.cam       = o('ao.cam').label
out.cam_c     = o('ao.cam').choices[1] .. '|' .. o('ao.cam').choices[4]
out.gunner_d  = o('ao.cam').description
out.speed_c   = o('ao.speed').choices[1] .. '|' .. o('ao.speed').choices[3]
out.steer_c   = o('ao.steer').choices[1] .. '|' .. o('ao.steer').choices[3]
out.crig      = o('crig.ik').label
out.crig_c    = o('crig.ik').choices[1] .. '|' .. o('crig.ik').choices[2]
out.crig_d    = o('crig.ik').description
out.long_d    = o('long.desc').description
out.long_len  = #o('long.desc').description
out.mod_ha    = st.mods['HIGH ALERT'] and st.mods['HIGH ALERT'].title or '<nil>'
return out
"""

L = lupa.LuaRuntime(unpack_returned_tuples=True)
L.execute(PRELUDE)
L.execute(src)
L.globals()["DETECT"] = HA_DESC
L.globals()["BOOST"] = HA_DESC_LONG
L.globals()["TURRET"] = AO_DESC
L.globals()["GUNNER"] = AO_DESC2
L.globals()["IK"] = CRIG_DESC
L.execute(REG)
L.globals()["STATE"] = L.globals()["STATE"]
res = L.execute(CHECK)

print("=== 汉化结果 ===")
for k, v in sorted(res.items()):
    s = str(v)
    print("  %-12s = %s" % (k, s[:110] + ("…" if len(s) > 110 else "")))

ok = True
def chk(name, got, want):
    global ok
    good = str(got) == str(want)
    ok = ok and good
    print("  %s %-40s %s" % ("PASS" if good else "FAIL", name, str(got)[:70]))

print("\n=== 判定 ===")
chk("高度警戒·选项名", res["split"], "分色显示")
chk("高度警戒·普通半径", res["nradius"], "普通半径")
chk("高度警戒·探测范围说明", res["nradius_d"],
    "探测范围：5-30 米，默认 12.1 米，步进 0.1。只有正在锁定你的活体敌人才会触发警报。")
chk("高度警戒·选项值(颜色)", res["ncolor_c"], "黄色|橙色|红色|紫色")
chk("高度警戒·增强说明", res["nboost_d"],
    "靠近增强总开关。闪烁频率与半径随距离线性增长、3 米时达到最大；亮度与不透明度仍沿用原版曲线。")
chk("高度警戒·炮击警报", res["art"], "炮击警报")
chk("装甲大修·炮塔位置", res["turretpos"], "坦克炮塔位置")
chk("装甲大修·值 原版/居中", res["turret_c"], "原版|居中")
chk("装甲大修·炮塔说明", res["turret_d"][:11], "主战坦克炮塔：决定堡垒")
chk("装甲大修·载具配置", res["loadout"], "载具配置")
chk("装甲大修·载具配置说明", res["loadout_d"][:11], "允许在战备配置里同时带")
chk("装甲大修·视角值", res["cam_c"], "近（后移约 1.5 米）|最远（后移约 6.5 米）")
chk("装甲大修·驾驶说明", res["gunner_d"][:14], "驾驶位空着时可以直接从炮手位")
chk("装甲大修·速度值(菜单会转大写)", res["speed_c"], "快（X1.1）|最快（X1.3）")
chk("装甲大修·转向值", res["steer_c"], "迅速|瞬时")
chk("C-Rig·IK 说明", res["crig_d"][:13], "需要该布局带 Custom")
chk("C-Rig·值", res["crig_c"], "部分|自动（部分）")
print("  超长说明长度 = %s（420，应原样保留英文 x 而非被截断）" % res["long_len"])
print("\n结论：%s" % ("全部通过 ✅" if ok else "存在失败项 ❌"))
