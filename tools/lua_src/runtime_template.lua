-- HD2-Addon: mods/gnh_cn/zh_hans
-- ══════════════════════════════════════════════════════════════════════════════
--  GNH 简体中文汉化包 —— 运行时汉化脚本
--  资源路径：mods/gnh_cn/zh_hans
--  制作：大赢经直插白皮赢道（GNH-CN-CYS）
--
--  【这份脚本在干什么】
--  游戏里 ESC → 模组 那个界面（"模组选项目录"）是共享加载器提供的一套菜单框架，
--  各个模组把自己的选项注册进去。问题是不少模组的选项文字是写死的英文。
--  本脚本不修改任何别人的文件，而是在游戏运行时"接管"菜单的注册入口，把英文换成中文。
--
--  【先认识三个词，看懂这三个就能看懂全文】
--    词表 GNH_CN ...... 下面那张大表：左边英文、右边中文，相当于一本翻译词典。
--    接管（hook）...... 把菜单原本用的函数换成一个包装版：先把文字翻一遍，再交给原函数。
--                       好比在门口加了个前台，进门的东西都要先过一遍手。
--    补翻（sweep）..... 把菜单内部"已经存好的"选项文字就地翻一遍。
--                       因为共享加载器按它自己的顺序运行各个模组，我们不一定排在第一个；
--                       等我们运行时，前面的模组早就把选项注册完了 —— 接管只对新注册有效，
--                       已经进去的那些就靠补翻补上。
--
--  【对性能的影响】
--  只在游戏刚启动的一小段时间里做事，全部完成后会写一条"主循环已交还"的日志；
--  之后每帧只剩一次真假判断，对帧率的影响可以忽略不计。
-- ══════════════════════════════════════════════════════════════════════════════

-- ─────────────────────────────── 一、词表 ───────────────────────────────
-- 格式：[英文原文] = 中文译文
-- 键必须与被汉化模组注册时传入的字符串**逐字符一致**，差一个空格就匹配不上。
-- 生成时会额外补一份全大写版本：菜单显示"选项值"和"模组名"时会先转成大写。
local GNH_CN = {
--[[GNH_CN_TABLE]]
}

-- 【跨小节使用的变量，先在这里声明】
-- Lua 的 local 变量只对自己"下面"的代码可见，下面这两项会被好几个小节用到，
-- 所以统一提到最前面声明 —— 否则后面小节里读到的其实是"全局变量"（那就是 nil 了）。
local real_register = nil   -- 菜单原本的注册函数（接管成功后才有值）
local GNH_COUNT = 0         -- 词表条目数，只用于日志

-- ─────────────────────────────── 二、日志 ───────────────────────────────
-- 运行情况写进 %LOCALAPPDATA%\CowboyBingus\Helldivers2\Logs\GNHChinesePack.log
-- 出问题时看这个文件就知道脚本走到了哪一步。
local GNH_TAG = 'GNH-CN-PACK'
local log_file
do
    local loader = rawget(_G, 'CowboyBingusModLoader')
    if loader and type(loader.open_log) == 'function' then
        local ok, f = pcall(loader.open_log, 'GNHChinesePack.log')
        if ok then log_file = f end
    end
end
local function log(msg)
    pcall(print, '[' .. GNH_TAG .. '] ' .. msg)
    if log_file then
        pcall(function() log_file:write(msg .. '\n'); log_file:flush() end)
    end
end

-- ─────────────────────────── 三、文本工具 ───────────────────────────
-- 数一个字符串里有几个"字"（字符），而不是几个字节。
-- 为什么要自己数：Lua 的 # 运算符数的是**字节**，一个汉字占 3 个字节，
-- 所以 #'中文' == 6，但它其实只有 2 个字。菜单限制的是"字数"。
local function utf8_len(s)
    local n, i, len = 0, 1, #s
    while i <= len do
        local c = s:byte(i)
        if c < 0x80 then i = i + 1          -- 0xxxxxxx：1 字节，ASCII
        elseif c < 0xE0 then i = i + 2      -- 110xxxxx：2 字节
        elseif c < 0xF0 then i = i + 3      -- 1110xxxx：3 字节，汉字在这里
        else i = i + 4 end                  -- 11110xxx：4 字节，表情符号等
        n = n + 1
    end
    return n
end

-- 查词表的统一入口：查到中文、而且不超长，才用中文；否则原样返回英文。
-- 上限是菜单自己规定的：选项名 64、选项值 48、说明 400、模组名 40（单位是"字"）。
-- 为什么非查长度不可：超长的文本会让**整个选项注册失败、直接从菜单里消失**，
-- 那比显示英文还糟。多这一道检查，最坏情况也只是回到英文。
local function pick(en, limit)
    if type(en) ~= 'string' then return en end
    local zh = GNH_CN[en]
    if type(zh) ~= 'string' then return en end
    -- 快速判断：字节数都没超上限的，字数一定也没超，不必真去数。
    if #zh > limit and utf8_len(zh) > limit then return en end
    return zh
end

-- ─────────────────────── 四、翻译"选项注册表" ───────────────────────
-- 模组注册一个选项时会递进来一张表，长这样：
--     { type = 'toggle', label = 'Show Badge', description = '……', choices = {……} }
-- 我们**复制一份**再改，绝不动对方原来那张表 —— 对方的表可能是只读的，
-- 也可能注册完自己还要接着用。复制是"浅拷贝"：把每个格子搬过去，值本身不动。
local function translate_spec(spec)
    if type(spec) ~= 'table' then return spec end
    local out = {}
    for k, v in pairs(spec) do out[k] = v end
    if out.label == nil then return spec end   -- 没有选项名：上游本来就会拒绝，不必多事
    out.label = pick(out.label, 64)
    out.description = pick(out.description, 400)
    out.mod = pick(out.mod, 40)
    local choices = out.choices
    if type(choices) == 'table' then
        local replaced = {}
        for i = 1, #choices do replaced[i] = pick(choices[i], 48) end
        out.choices = replaced
    end
    return out
end

-- ───────────────────── 五、借用菜单内部的"小本子" ─────────────────────
-- Lua 里，函数能看见它外面定义的局部变量，这些变量叫 upvalue，
-- 可以理解成函数的"随身小本子"。菜单把玩家注册过的所有选项记在它自己的小本子里，
-- 但这个本子不对外开放。好在 Lua 提供了 debug.getupvalue，可以把本子借出来看一眼：
-- 只要某本子里同时有 options 和 mods 两张表，那就是我们要找的 state。
--
-- 说明：菜单自己就用 debug.getinfo 找调用方，所以 debug 库一定是可用的。
-- 万一以后上游改了内部结构、找不到了，也只是"补翻"失效，
-- 接管照常工作、也不会报错 —— 属于安全的降级。
local getupvalue = type(debug) == 'table' and debug.getupvalue or nil

local function find_upvalue(probes, count, field_a, field_b)
    if not getupvalue then return nil end
    for i = 1, count do
        local f = probes[i]
        if type(f) == 'function' then
            local k = 1
            while k <= 96 do          -- Lua 函数最多 60 个 upvalue，96 已经绰绰有余
                local ok, name, v = pcall(getupvalue, f, k)
                if not ok or name == nil then break end
                if type(v) == 'table' and type(v[field_a]) == 'table' and type(v[field_b]) == 'table' then
                    return v
                end
                k = k + 1
            end
        end
    end
    return nil
end

-- 把若干"可能拿着小本子"的函数收进一个数组。
-- 用计数器 n 而不是 #p：数组中间一旦有空位，# 就不准了。
local function collect(...)
    local p, n = {}, 0
    for i = 1, select('#', ...) do
        local f = select(i, ...)
        if type(f) == 'function' then n = n + 1; p[n] = f end
    end
    return p, n
end

local function options_state(host)
    local p, n = collect(real_register, host.register_option, host.get,
                         host.set, host.ready, host.on_change)
    return find_upvalue(p, n, 'options', 'mods')
end

-- ──────────────────────────── 六、补翻 ────────────────────────────
-- 把菜单里"已经注册好的"选项文字就地改成中文。
--
-- 【为什么改选项值是安全的】
-- 菜单内部记的是"玩家选了第几个"（1、2、3……），不是文字本身，文字只用来显示。
-- 所以把显示文字换成中文，不会影响玩家实际选中的值。
--
-- 【为什么改完马上就能看见】
-- 菜单每一帧都会核对行上的文字是否还等于 option.label；
-- 我们一改，它下一帧就发现对不上，于是用新文字重画一遍。
--
-- 顺带记下"哪些 id 被我们翻过"（见下面的 swept_ids），重复注册时要靠它。
local swept_ids = {}   -- [选项 id] = 我们写进去的中文选项名

local function sweep_options()
    local host = rawget(_G, 'ModOptionsMenu')
    if type(host) ~= 'table' then return 0 end
    local st = options_state(host)
    if not st then return 0 end

    local n = 0
    for _, option in pairs(st.options) do
        if type(option) == 'table' then
            local before = n
            local zh = pick(option.label, 64)
            if zh ~= option.label then option.label = zh; n = n + 1 end
            zh = pick(option.description, 400)
            if zh ~= option.description then option.description = zh; n = n + 1 end
            local ch = option.choices
            if type(ch) == 'table' then
                for i = 1, #ch do
                    local c = pick(ch[i], 48)
                    if c ~= ch[i] then ch[i] = c; n = n + 1 end
                end
            end
            if n > before and option.id then swept_ids[option.id] = option.label end
        end
    end

    -- 模组名（左侧列表的分组标题）
    for _, mod in pairs(st.mods) do
        if type(mod) == 'table' then
            local zh = pick(mod.title, 40)
            if zh ~= mod.title then mod.title = zh; n = n + 1 end
        end
    end
    -- 左侧列表是另一份数组，元素通常与上面是同一个表，但为稳妥再扫一遍
    local view = st.view
    if type(view) == 'table' and type(view.mods) == 'table' then
        for _, mod in ipairs(view.mods) do
            if type(mod) == 'table' then
                local zh = pick(mod.title, 40)
                if zh ~= mod.title then mod.title = zh; n = n + 1 end
            end
        end
    end

    -- 通知菜单"内容变了，重画"
    if n > 0 and type(st.revision) == 'number' then st.revision = st.revision + 1 end
    return n
end

-- ─────────────────────── 七、按键绑定菜单 ───────────────────────
-- 同一个作者的另一个菜单 ModBindingsMenu（改按键用的）。
-- 它的注册函数是 register_binding(id, 显示名, 槽位, 附加设置)，第二个参数就是要显示的名字。
-- 我们只把第二个参数换成中文，其余参数原样转交。
local bindings_hooked = false
local real_binding_register = nil

local function try_hook_bindings()
    if bindings_hooked then return true end
    local host = rawget(_G, 'ModBindingsMenu')
    if type(host) ~= 'table' or type(host.register_binding) ~= 'function' then return false end
    local real = host.register_binding

    local function wrapped(id, label, ...)
        local ok, text = pcall(pick, label, 127)
        if not ok then text = label end
        return real(id, text, ...)
    end

    local ok = pcall(function() host.register_binding = wrapped end)
    if not ok then
        log('ModBindingsMenu.register_binding 无法替换（可能是只读表），改用补翻方式')
        bindings_hooked = true
        return true
    end
    real_binding_register = real
    bindings_hooked = true
    log('已接管 ModBindingsMenu.register_binding')
    return true
end

local function sweep_bindings()
    local host = rawget(_G, 'ModBindingsMenu')
    if type(host) ~= 'table' then return 0 end
    local p, np = collect(real_binding_register, host.register_binding, host.is_down, host.ready)
    local st = find_upvalue(p, np, 'registry', 'order')
    if not st then return 0 end
    local n = 0
    for _, record in pairs(st.registry) do
        if type(record) == 'table' then
            -- record.label 可能是数字（游戏自己的本地化编号），pick 对非字符串原样返回
            local zh = pick(record.text, 127)
            if zh ~= record.text then record.text = zh; n = n + 1 end
            zh = pick(record.label, 127)
            if zh ~= record.label then record.label = zh end
            zh = pick(record.category, 64)
            if zh ~= record.category then record.category = zh; n = n + 1 end
        end
    end
    return n
end

-- ─────────────────────── 八、接管选项注册 ───────────────────────
local hooked = false        -- 是否已经处理过（含"确认无法接管"的情况，避免反复尝试）
local hits = 0

local function try_hook()
    if hooked then return true end
    local host = rawget(_G, 'ModOptionsMenu')
    if type(host) ~= 'table' or type(host.register_option) ~= 'function' then return false end
    local real = host.register_option

    local function wrapped(id, spec, ...)
        local ok, translated = pcall(translate_spec, spec)
        if not ok or type(translated) ~= 'table' then translated = spec end
        hits = hits + 1
        if hits <= 12 and translated ~= spec then
            log('汉化: ' .. tostring(spec.label) .. ' -> ' .. tostring(translated.label))
        end
        local a, b, c = real(id, translated, ...)
        -- 上游回答"这个 id 注册过了、而且内容不一样"。
        -- 如果差异正好是我们补翻造成的（swept_ids 里记着同样的中文名），
        -- 那就按"重复注册同一个选项"放行返回 true —— 否则模组会以为自己注册失败，
        -- 可能反复重试或者在它的日志里刷错误。
        if a == false and swept_ids[id] ~= nil and translated.label == swept_ids[id] then
            return true
        end
        return a, b, c
    end

    -- 有些表的字段是只读的，赋值会报错；用 pcall 兜住，失败也不影响游戏
    local ok = pcall(function() host.register_option = wrapped end)
    if not ok then
        log('ModOptionsMenu.register_option 无法替换（可能是只读表），改用补翻方式')
        hooked = true
        return true
    end
    real_register = real
    hooked = true
    log('已接管 ModOptionsMenu.register_option（词表 ' .. tostring(GNH_COUNT) .. ' 条）')
    return true
end

-- ────────────────────────── 九、主循环 ──────────────────────────
-- 加载本脚本时有两种可能：
--   A. 菜单已经就绪 → 立刻接管，并立刻补翻一次；
--   B. 菜单还没就绪（我们比它先加载）→ 挂到游戏主循环上，等它出现的那一帧抢先接管。
-- 之后每隔 20 帧补翻一次，直到连着 3 次都翻不出新东西为止。
-- 全部收工后 done = true，主循环里只剩一次真假判断。

-- ───────────────── 十、Bingus Text 官方翻译包 ─────────────────
-- 为什么要走这条路：Vanilla Plus 的十七个子模组（浅水潜行等）是在 Bingus 加载器
-- 的 after_startup 事件里"一次性"注册的，那一刻本脚本的钩子还没装上；而它们取
-- 文字走的是 Bingus Text 的翻译表（option_text -> translator），所以只能从官方
-- 翻译包这条正路进去，钩子和补翻都够不着。
--
-- 用法：全局表 _G.BingusTranslations 是各模组共用的一本"词典"，packs 是个数组。
-- 往里加一条 {language=..., name=..., mods={模组标识 = {键 = 译文}}} 即可；
-- 加完必须把 serial 加一 —— 各模组靠 serial 判断词典有没有更新，不加就不会重查。
local GNH_PACK_NAME = 'GNH Simplified Chinese Pack'

-- 浅水潜行的条目：键取自它字节码里的 option.depth.* （模组自己的英文文本表用的就是这两个键）
local GNH_SWD = {
    -- 模组名（左侧分类按钮上显示的名字）：键名取自 Vanilla Plus 里
    -- 'mod = option_text(tr, options_menu, "option.mod", 40)' 这一行。
    ['option.mod'] = '浅水潜行',
    ['option.depth.label'] = '最大入水深度',
    ['option.depth.description'] = '潜水的最大入水深度，从脚底往上量：0.20（小腿下段，原版上限）到 1.30（此时潜兵会开始游泳）。更深的水域始终沿用游戏原本的行为。',
}

-- Mod 选项菜单自身的界面文字。它的词典是 {mod = 'mod_options_menu', strings = {...}}，
-- 键名逐条抄自源码里的英文词典；{page} / {pages} 是它自己的占位符，必须原样保留，
-- 否则菜单会因"占位符与英文不符"而拒收这条译文。
local GNH_MOM = {
    ['tab.mods'] = '模组',
    ['category.none'] = '未安装任何模组选项',
    ['category.page'] = '第 {page} / {pages} 页',
    ['page.label'] = '模组分页',
    ['page.description'] = '分类按钮一次显示 7 个模组，翻页可查看其余。',
}

-- 同一个模组在不同版本里可能用不同的标识，全部挂上；挂多余的没有副作用。
local function bingus_mods()
    local out = {}
    for _, name in ipairs({ 'shallow_water_diving', 'ShallowWaterDiving', 'Shallow Water Diving' }) do
        out[name] = GNH_SWD
    end
    out['mod_options_menu'] = GNH_MOM
    return out
end

local bingus_done = false

local function install_bingus_pack()
    if bingus_done then return true end
    local ok, done = pcall(function()
        local reg = rawget(_G, 'BingusTranslations')
        if type(reg) ~= 'table' or tonumber(reg.version) ~= 1 then return false end
        if type(reg.packs) ~= 'table' then reg.packs = {} end
        for _, p in ipairs(reg.packs) do
            if type(p) == 'table' and p.name == GNH_PACK_NAME then return true end
        end
        reg.packs[#reg.packs + 1] = { language = 'zh-Hans', name = GNH_PACK_NAME, mods = bingus_mods() }
        reg.serial = (tonumber(reg.serial) or 0) + 1
        return true
    end)
    if ok and done then
        bingus_done = true
        log('已注册 Bingus Text 翻译包（供 Vanilla Plus 子模组使用）')
    end
    return bingus_done
end

local sweep_calls, sweep_idle = 0, 0
local frame, wait_options, wait_bindings = 0, 0, 0
local done = false

local function sweep_tick()
    if sweep_idle >= 3 then return end
    sweep_calls = sweep_calls + 1
    local ok, n = pcall(sweep_options)
    if not ok or type(n) ~= 'number' then n = 0 end
    local b = 0
    pcall(function() b = sweep_bindings() or 0 end)
    if n > 0 or b > 0 then
        sweep_idle = 0
        log('补翻已注册条目 ' .. n .. ' 项 / 按键 ' .. b .. ' 条（第 ' .. sweep_calls .. ' 次扫描）')
    else
        sweep_idle = sweep_idle + 1
        if sweep_calls == 1 then log('第 1 次扫描：暂时没有需要补翻的条目') end
    end
end

local function tick()
    frame = frame + 1

    -- 1) 接管选项菜单。菜单一出现就要立刻接管，所以这里每帧都查一次
    --    （900 帧 ≈ 15 秒还没出现，就不再等了，不影响游戏）。
    if not hooked and wait_options < 900 then
        wait_options = wait_options + 1
        if try_hook() then log('已在第 ' .. frame .. ' 帧接管 ModOptionsMenu') end
    end

    -- 2) 接管按键菜单。它没那么急，每 30 帧试一次就够。
    if not bindings_hooked and wait_bindings < 900 then
        wait_bindings = wait_bindings + 1
        if wait_bindings % 30 == 1 then pcall(try_hook_bindings) end
    end

    -- 3) 周期性补翻
    if not bingus_done and frame % 10 == 0 then pcall(install_bingus_pack) end
    if sweep_idle < 3 and frame % 20 == 0 then pcall(sweep_tick) end

    -- 4) 该做的都做完了 → 交还主循环
    if (hooked or wait_options >= 900)
       and (bindings_hooked or wait_bindings >= 900)
       and sweep_idle >= 3 then
        done = true
        log('初始化完成（第 ' .. frame .. ' 帧），主循环已交还')
    end
end

-- ────────────────────── 十、启动与挂载 ──────────────────────
-- 重复加载保护：本脚本在极端情况下可能被执行两次（例如菜单被重新加载）。
-- 第二次直接退出，避免同一个函数被套两层包装。
if rawget(_G, 'GNH_CN_PACK_LOADED') then
    log('检测到重复加载，本次跳过')
    return
end
rawset(_G, 'GNH_CN_PACK_LOADED', true)

for _ in pairs(GNH_CN) do GNH_COUNT = GNH_COUNT + 1 end

pcall(install_bingus_pack)
try_hook()
pcall(try_hook_bindings)
if hooked or bindings_hooked then pcall(sweep_tick) end

local base_update = rawget(_G, 'update')
rawset(_G, 'update', function(...)
    if not done then tick() end
    if type(base_update) == 'function' then return base_update(...) end
end)

log('汉化包已载入，等待初始化')
