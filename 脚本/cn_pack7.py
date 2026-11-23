# -*- coding: utf-8 -*-
"""cn_pack7.py -- 浅水潜行（Shallow Water Diving）词条。

该模组把 LuaJIT 字节码用 loadstring 的十进制转义形式嵌在补丁里，
明文搜索搜不到，因此第一轮全量扫描漏掉了它。
这里通过解码字节码取到了准确原文。
"""

CN_PACK7 = {
    "Max Dive Water Depth": "最大入水深度",
    "Deepest water, measured up from your feet, that a dive can start in: from 0.20 (lower shin, the original limit) up to 1.30, where your Helldiver starts swimming. Deeper water always keeps the game's normal behavior.":
        "潜水的最大入水深度，从脚底往上量：0.20（小腿下段，原版上限）到 1.30（此时潜兵会开始游泳）。更深的水域始终沿用游戏原本的行为。",
}
