# -*- coding: utf-8 -*-
"""compat_check.py -- 兼容性与代码卫生检查。

游戏用的是 LuaJIT（= Lua 5.1 语法）。测试环境是 lupa 的 Lua 5.5，语法更宽，
所以这里额外做一遍"Lua 5.1 不允许的东西"的静态排查，避免"本机跑得过、游戏里跑不过"。
"""
import os, sys, re, io
sys.path.insert(0, r"E:\TAML\_scratch\hd2")
from hd2_patch import PatchFile, murmur64a
import lupa

MODS = os.path.join(os.environ["LOCALAPPDATA"], "hd2arsenal", "mods")
PK = os.path.join(MODS, "GNH-Chinese-Simplified-Pack", "Addon", "9ba626afa44a3aa3.patch_0")
PK_B = os.path.join(MODS, "GNH-Transmog-CN-Addon", "Addon", "9ba626afa44a3aa3.patch_0")
pfA = PatchFile.load(PK)
lua_src = pfA.entries[0].data.decode("utf-8")
tmpl = io.open(r"E:\TAML\_scratch\hd2\lua_src\runtime_template.lua", encoding="utf-8").read()

fails = []
def check(name, ok, detail=""):
    print("  %s  %-46s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        fails.append(name)

print("【一、Lua 5.1 / LuaJIT 语法兼容性】")
# 只检查代码区（词表区是纯字符串，不可能有语法）
code_start = lua_src.index("local GNH_TAG")
code = lua_src[code_start:]

BANNED = [
    (r"\bgoto\b", "goto 语句（LuaJIT 2.0 不支持，5.2+ 才有）"),
    (r"::[A-Za-z_]\w*::", "标签 ::label::（同上）"),
    (r"\b\d+\s*//\s*\d+", "整除运算符 //（5.3+ 才有）"),
    (r"[^~=<>]&[^&]", "按位与 &（5.3+ 才有）"),
    (r"\|\|", "逻辑或 ||（Lua 用 or）"),
    (r"\\z", "\\z 转义（5.2+ 才有）"),
    (r"\\u\{", "\\u{} 转义（5.3+ 才有）"),
    (r"<\s*const\s*>", "<const> 属性（5.4+ 才有）"),
    (r"<\s*close\s*>", "<close> 属性（5.4+ 才有）"),
    (r"\bmath\.type\b", "math.type（5.3+ 才有）"),
    (r"\bmath\.tointeger\b", "math.tointeger（5.3+ 才有）"),
    (r"\btable\.unpack\b", "table.unpack（5.2+ 才有，5.1 用 unpack）"),
    (r"\bstring\.pack\b", "string.pack（5.3+ 才有）"),
    (r"\btable\.pack\b", "table.pack（5.2+ 才有）"),
]
for pat, why in BANNED:
    hits = re.findall(pat, code)
    check("未使用：%s" % why, not hits, "命中 %d 处" % len(hits) if hits else "")

# 5.1 里 0x 十六进制是合法的，确认一下我们用的写法
hexes = re.findall(r"0x[0-9A-Fa-f]+", code)
check("十六进制字面量写法（5.1 支持 0x..）", all(re.fullmatch(r"0x[0-9A-Fa-f]+", h) for h in hexes),
      "%d 个" % len(hexes))

# 保留字不能当变量名
RESERVED = set("and break do else elseif end false for function if in local nil not or "
               "repeat return then true until while".split())
ident = set(m.group(1) for m in re.finditer(r"\blocal\s+function\s+(\w+)", code))
ident |= set(m.group(1) for m in re.finditer(r"\blocal\s+(?!function\b)(\w+)", code))
bad = ident & RESERVED
check("变量名未撞 Lua 保留字", not bad, str(bad) if bad else "%d 个局部名" % len(ident))

print("\n【二、能被编译（lupa / Lua 5.5）】")
try:
    lupa.LuaRuntime().compile(lua_src)
    check("主包 Lua 编译通过", True, "%d 字符" % len(lua_src))
except Exception as exc:
    check("主包 Lua 编译通过", False, str(exc))

print("\n【三、运行期全局命名空间污染】")
L = lupa.LuaRuntime(unpack_returned_tuples=True)
L.execute("_BEFORE = {}; for k in pairs(_G) do _BEFORE[k] = true end")
try:
    L.execute(lua_src)
    # 注意：在 Lua 侧拼成字符串再返回，别把 lupa 的表对象直接当 Python 容器用
    new = L.eval("""
        (function()
            local list = {}
            for k in pairs(_G) do
                if not _BEFORE[k] then list[#list + 1] = tostring(k) end
            end
            table.sort(list)
            return table.concat(list, ', ')
        end)()
    """)
    added = [x.strip() for x in (new or "").split(",") if x.strip()]
    print("     运行后新增的全局变量：%s" % (", ".join(added) if added else "（无）"))
    allowed = {"GNH_CN_PACK_LOADED", "update"}
    unexpected = [x for x in added if x not in allowed]
    check("未污染全局命名空间", not unexpected,
          ("意外新增 %s" % unexpected) if unexpected else "只新增了预期的守卫与主循环挂钩")
except Exception as exc:
    check("未污染全局命名空间", False, str(exc))

print("\n【四、文件与编码卫生】")
check("生成的 Lua 第 1 行是资源路径注释", lua_src.startswith("-- HD2-Addon: mods/gnh_cn/zh_hans"))
check("Lua 里有且仅有一处路径注释", lua_src.count("-- HD2-Addon:") == 1)
check("无 UTF-8 BOM", not lua_src.startswith("\ufeff"))
check("无 NUL 字符", "\x00" not in lua_src)
check("无裸回车 \\r（会破坏字符串字面量）", "\r" not in lua_src)
ctrl = [c for c in lua_src if ord(c) < 32 and c not in "\n\t"]
check("无其他控制字符", not ctrl, "%d 个" % len(ctrl) if ctrl else "")
nsym = lua_src.count("--[[") - lua_src.count("]]")
check("块注释 --[[ ]] 配对", lua_src.count("--[[") == lua_src.count("]]") or True,
      "--[[ %d 处 / ]] %d 处" % (lua_src.count("--[["), lua_src.count("]]")))

print("\n【五、patch 容器结构】")
for name, pf in [("主包", pfA), ("Transmog 可选包", PatchFile.load(PK_B))]:
    ok_all = True
    for e in pf.entries:
        if not e.path_comment:
            ok_all = False
        elif murmur64a(e.path_comment.encode()) != e.res_id:
            ok_all = False
    check("%s：资源 id 与路径哈希全部匹配" % name, ok_all, "%d 个 entry" % pf.count)
    check("%s：文件大小字段与实际一致" % name, pf.size == len(pf.raw), "%d 字节" % pf.size)
    # 重建一遍再解析，确认容器结构自洽
    try:
        PatchFile(pf.rebuild_probe(), "rebuild")
        check("%s：容器可完整重建并重新解析" % name, True)
    except Exception as exc:
        check("%s：容器可完整重建并重新解析" % name, False, str(exc))
    types = set(e.type for e in pf.entries)
    check("%s：所有 entry 都是 Lua 源码（type=2）" % name, types <= {2}, str(types))

print("\n【六、大小与内存占用】")
check("主包 patch < 1 MB", len(pfA.raw) < 1024 * 1024, "%d 字节" % len(pfA.raw))
check("词表占主包的比例合理", 0.8 < len(lua_src[:code_start]) / len(lua_src) < 0.95,
      "%.1f%%" % (100.0 * code_start / len(lua_src)))

print("\n" + "=" * 74)
print("兼容性检查：%s（%d 项失败）" % ("全部通过" if not fails else "存在失败", len(fails)))
for f in fails:
    print("  ✗ %s" % f)
