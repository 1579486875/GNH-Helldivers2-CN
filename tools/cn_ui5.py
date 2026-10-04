# -*- coding: utf-8 -*-
"""cn_ui5.py -- 第五批词表：从各模组 Lua 源里**直接读取**待补字符串，保证逐字符一致。

补的是：
  * HD2 Transmog 调试探针面板的 4 个标签（高级调试界面，普通玩家一般看不到，但补上更完整）
  * Mod Bindings Menu 里可能出现的模组名 Ship Station Hotkeys
  * Better Lobby Management 测试版专用的两个选项名
刻意**不补**的（见 tools/README 说明）：Probe A/B（开发者变体标识）、
ModOptionsMenu 源码注释里的 API 示例文本、代码注释里的示例名。
"""
import io, os, re, json

DUMP = r"E:\TAML\_scratch\hd2\lua_dump"
TM = os.path.join(DUMP, "HD2 Transmog Foundation 0.2.0 (Alpha) 16633 0.2.1 2026-10-04T14-37Z PjshZUxBj_AR829814", "Addon__e00.lua")
BL = os.path.join(DUMP, "Vanilla Plus Megapack Rows V36 zh-Hans zh-Hant CN 16627 36 2026-10-01T05-16Z UR0syXwpP_AR640294", "options_BetterLobbyManagement__e01.lua")

CN_UI5 = {}

# 1) Transmog 调试探针标签：形如 {key='direct_hash',label='1  Resource ID'},
t = io.open(TM, encoding="utf-8", errors="replace").read()
probe = re.findall(r"\{key='[a-z_0-9]+',\s*label='(\d\s+[A-Za-z][^']*)'\}", t)
MAPPING = {
    "1  Resource ID": "1  资源 ID",
    "2  Icon material": "2  图标材质",
    "3  Texture binding": "3  贴图绑定",
    "4  Configured icon": "4  已配置图标",
}
for lab in probe:
    if lab in MAPPING:
        CN_UI5[lab] = MAPPING[lab]
print("从 Transmog 源读到探针标签 %d 个：%s" % (len(probe), probe))

# 2) Better Lobby Management 测试版选项名（正式版不显示，补上以防有人用测试版）
t2 = io.open(BL, encoding="utf-8", errors="replace").read()
for en, zh in [("Kick Test", "踢人测试"), ("Promote Notice", "提升通知")]:
    if ("label='%s'" % en) in t2 or ("'%s'" % en) in t2:
        CN_UI5[en] = zh
        print("找到测试项：%s" % en)

# 3) 模组名（Mod Bindings Menu 的分组标题 / MODS 页的模组名）
CN_UI5["Ship Station Hotkeys"] = "舰内站点快捷键"

print("\n本批共 %d 条：" % len(CN_UI5))
for k, v in CN_UI5.items():
    print("   %r -> %r" % (k, v))
