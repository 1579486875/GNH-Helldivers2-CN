# -*- coding: utf-8 -*-
"""cn_mods3.py -- 第三批模组元数据词表：新加入的模组的名称 / 简介 / 启用选项。

来源：各模组自己的 manifest.json（逐字符照抄，差一个空格就匹配不上）。
注意：manifest 里的 Include 字段是**目录名**，绝对不能翻译，这里只收 Name / Description。
"""

CN_MODS3 = {
    # ---------------- Markers For MineField（雷区标记，AIO 整合包）----------------
    "Markers For MineField": "雷区标记",
    "All-In-One Pack": "整合包（一包包含全部标记）",
    "Simple Marker": "简易标记",
    'Add little cones above each mine\n\nCaution: Disable "Detailed Marker" if using this':
        '在每颗地雷上方显示小圆锥\n\n注意：使用本项时请关闭「详细标记」',
    "Detailed Marker": "详细标记",
    'Add detailed icons above each mine\n\nCaution: Disable "Simple Marker" if using this':
        '在每颗地雷上方显示详细图标\n\n注意：使用本项时请关闭「简易标记」',
    "Game Original Color": "游戏原版配色",
    "Custom Color": "自定义配色",
    "Marker For Automaton Mine": "自动人形地雷标记",
    "Add symbol icon above Automaton mine": "在自动人形地雷上方显示符号图标",
    "Lure Mine": "诱饵雷",
    "Add explosion icon above TM-1 Lure Mine": "在 TM-1 诱饵雷上方显示爆炸图标",
    "Damaged Hellbomb": "受损地狱火炸弹",
    "Add Hellbomb icon above Damaged Hellbomb \n(Randomly spawn in maps)\n\nAdd Emissive VFX on prong/top parts of Hellbomb\n(For clearer identification)":
        "在受损地狱火炸弹上方显示地狱火炸弹图标\n（在地图中随机刷新）\n\n为地狱火炸弹的支脚与顶部添加自发光特效\n（便于更清晰地辨认）",
    "G/40-K Meltamine": "G/40-K 熔融雷",
    "Add WH40K icon above G/40-K Meltamine\n\nAdd Emissive VFX on surface of Meltamine\n(For clearer identification)":
        "在 G/40-K 熔融雷上方显示 WH40K 图标\n\n为熔融雷表面添加自发光特效\n（便于更清晰地辨认）",

    # ---------------- Beacon Custom VFX（信标自定义特效）----------------
    "Beacon Custom VFX": "信标自定义特效",
    "Beacon beam replacment": "替换信标光柱特效",
    "Blue Beacon": "蓝色信标",
    "Blue V1": "蓝色 V1",
    "Blue V2 (Rock and Stone)": "蓝色 V2（Rock and Stone）",
    "Red Beacon": "红色信标",
    "Red V1": "红色 V1",
    "Red V2 (Vanilla plus)": "红色 V2（原版增强）",
}
