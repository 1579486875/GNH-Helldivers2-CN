# -*- coding: utf-8 -*-
"""cn_pack8.py -- 过长的模组名缩短，避免 MODS 列表里挤出边界、压住相邻行。

背景：ModOptionsMenu 给左侧"分类"（模组名）预留的宽度是固定的，
它自己只校验模组名不超过 40 个字（超了直接拒绝注册），但没校验渲染宽度。
Battlefield V Kill Feedback 交上去的是双语长名（36 字），渲染时溢出到列表右边缘，
盖住了旁边的选项行。这里把它换成短名即可 —— 因为它走的是 spec.mod 这条路径，
本汉化包的钩子正好拦得到。
"""

CN_PACK8 = {
    # 战地V击杀反馈：双语长名 -> 短名
    "BATTLEFIELD V KILL FEEDBACK / 战地V击杀反馈": "战地V击杀反馈",
    "Battlefield V Kill Feedback / 战地V击杀反馈": "战地V击杀反馈",
    "Battlefield V Kill Feedback/战地V击杀反馈": "战地V击杀反馈",
    # 顺带把几个较长的模组名统一收短，减少同类溢出
    "TACTICAL COMBAT OVERHAUL": "战术战斗大修",
    "Tactical Combat Overhaul": "战术战斗大修",
    "SHALLOW WATER DIVING": "浅水潜行",
    "Shallow Water Diving": "浅水潜行",
    "HD2 TRANSMOG": "HD2 幻化",
}
