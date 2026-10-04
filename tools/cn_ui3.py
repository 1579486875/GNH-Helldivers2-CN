# -*- coding: utf-8 -*-
"""cn_ui3.py -- 第三批词表：ModOptionsMenu / ModBindingsMenu 注册的界面文本。

来源（逐字符取自各模组 Lua 源，见 _scratch/hd2/lua_dump/）：
  * Objective Tracker 0.4.12        -- 17 个选项的 label / description / choices
  * HD2 Transmog Foundation 0.2.1   -- 3 个选项及其 choices / description
  * Aggro Counter 1.3               -- Mod Bindings Menu 的按键标签
  * HD2 Transmog                    -- Mod Bindings Menu 的按键标签
  * 各模组在 MODS 页里显示的模组名（会被 ModOptionsMenu 转成大写后显示）
"""

CN_UI3 = {
    # ---------- Objective Tracker 0.4.12：17 个选项 ----------
    "Objective Tracker": "任务目标追踪",
    "Show objective tracker": "显示任务目标追踪",
    "Show only while map is open": "仅在打开地图时显示",
    "Display the tracker with the tactical map. The panel also appears in ESC for positioning and resizing.":
        "与战术地图一同显示追踪面板。该面板也会出现在 ESC 菜单中，供你调整位置与大小。",
    "Maximum visible targets": "最多显示目标数",
    "Show the nearest targets, sorted by distance. Panel height also limits how many rows fit.":
        "显示最近的目标，按距离排序。面板高度也会限制可容纳的行数。",
    "Maximum distance (meters)": "最大距离（米）",
    "Direct distance from your Helldiver to loaded objectives.": "从你的绝地潜兵到已加载目标的直线距离。",
    "Text and icon size (%)": "文字与图标大小（%）",
    "Set the text and icon size. Resizing the panel keeps this size and changes how many targets fit.":
        "设置文字与图标大小。调整面板尺寸会保留该字号，并改变可容纳的目标数量。",
    "Background opacity (%)": "背景不透明度（%）",
    "Icon and distance colors": "图标与距离颜色",
    "Objective colors": "目标配色",
    "Helldiver gold": "绝地潜兵金",
    "Ice white": "冰白",
    "Row spacing": "行间距",
    "Compact": "紧凑",
    "Comfortable": "宽松",
    "Support and retrieval objectives": "支援与回收类目标",
    "Radar stations, SEAF artillery, SAM sites, escape pod data and mutant larvae.":
        "雷达站、SEAF 火炮、防空导弹阵地、逃生舱数据与变异幼虫。",
    "Hostile nests and installations": "敌方巢穴与设施",
    "Research objective sites": "研究类目标地点",
    "Specimen pickups": "样本拾取物",
    "Show Automaton heads and mutated eggs with distance and direction.":
        "显示自动人形头颅与变异卵的距离和方向。",
    "Show item carrier": "显示物品携带者",
    "Show the carrier squad tag for Automaton heads, mutated eggs and mutant larvae.":
        "为自动人形头颅、变异卵与变异幼虫显示携带者的小队标签。",
    "Hide completed objectives": "隐藏已完成目标",
    "Hide objectives after the game reports completion. Completion affects only your HUD.":
        "当游戏报告目标完成后将其隐藏。该完成状态只影响你自己的 HUD。",
    "Hide destroyed sites": "隐藏已被摧毁的地点",
    "For sites without a readable objective state, hide the entry when every observed structure is dead or removed. Native objective state takes priority when available.":
        "对于无法读取任务状态的地点，当观察到的所有结构均已被摧毁或移除时隐藏该条目。若可读取原生任务状态，则以原生状态为准。",
    "Show panel aboard ship": "在飞船上也显示面板",
    "Detailed logging": "详细日志",
    "Write objective state details to the local log for troubleshooting.":
        "将任务状态详情写入本地日志，便于排查问题。",

    # ---------- HD2 Transmog Foundation 0.2.1：3 个选项 ----------
    "HD2 Transmog": "HD2 幻化",
    "Preview style": "预览风格",
    "Choose the lighting for generated previews. HD2 uses the approved rim lighting; Studio emphasizes front detail. Both styles stay cached. Items without an author choice use HD2.":
        "选择生成预览所用的光照。HD2 使用官方认可的轮廓光；Studio 更强调正面细节。两种风格的缓存都会保留。作者未指定时使用 HD2。",
    "Mod author's choice": "作者指定",
    "Force HD2": "强制 HD2",
    "Force Studio": "强制 Studio",
    "Armory 3D preview": "军械库 3D 预览",
    "Full render": "完整渲染",
    "Game default": "游戏默认",
    "Full render draws the large Armory model through the game's full pipeline, with hair and the lighting of the generated previews. It needs temporal anti-aliasing; without it, and with Game default, the game draws the model itself.":
        "完整渲染会通过游戏的完整渲染管线绘制大型军械库模型，包含头发以及生成预览所用的光照。它需要开启时间抗锯齿；若未开启，或者选择「游戏默认」，则由游戏自行绘制模型。",
    "Regenerate previews": "重新生成预览",
    "Keep cached images": "保留缓存图像",
    "Regenerate now": "立即重新生成",
    "Apply Regenerate now to refresh generated previews for the selected style. Requires a working renderer and an open Armory item list. Cached images remain available if rendering is unavailable.":
        "选择「立即重新生成」可用当前风格刷新已生成的预览。需要渲染器可用且军械库物品列表已打开。若渲染不可用，仍会保留缓存图像。",

    # ---------- Aggro Counter 1.3：Mod Bindings Menu 按键标签 ----------
    "SHOW / HIDE BADGE": "显示/隐藏徽章",
    "BADGE BIGGER": "放大徽章",
    "BADGE SMALLER": "缩小徽章",
    "MOVE BADGE UP": "上移徽章",
    "MOVE BADGE DOWN": "下移徽章",
    "MOVE BADGE LEFT": "左移徽章",
    "MOVE BADGE RIGHT": "右移徽章",

    # ---------- HD2 Transmog：Mod Bindings Menu 按键标签 ----------
    "Select Next Transmog Piece": "选择下一件幻化部件",
    "Next Transmog Variant": "下一个幻化变体",
    "Previous Transmog Variant": "上一个幻化变体",
    "Refresh Transmog Look": "刷新幻化外观",
    "Custom Variant": "自订变体",

    # ---------- MODS 页里的模组名 ----------
    "Shallow Water Diving": "浅水潜行",
    "Better Lobby Management": "大厅管理",
}
