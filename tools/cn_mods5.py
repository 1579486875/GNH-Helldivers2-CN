# -*- coding: utf-8 -*-
"""cn_mods5.py -- C-Rig 骨骼运行时 的菜单选项词表（这部分由汉化包在运行时接管）。"""

CN_MODS5 = {
    # 选项分组名（会以大写显示）
    "Rigs & Physics": "骨骼与物理",

    # 五个开关
    "C-Rig runtime": "C-Rig 运行时",
    "OFF restores the current pose once, then suspends tracking, rigs, IK, animations, physics, statistics and profiling. Individual choices are preserved. ON binds the current scene again.":
        "关闭后会先恢复一次当前姿势，然后暂停追踪、骨骼、IK、动画、物理、统计与性能分析；各项独立选项都会保留。开启后重新绑定当前场景。",
    "Custom rigs": "自定义骨骼",
    "Enable authored armor retargeting for all matching pieces. Physics is controlled separately.":
        "为所有匹配的部件启用作者制作的盔甲骨骼替换。物理由单独的开关控制。",
    "Custom animations": "自定义动画",
    "Play baked bone Actions before physics. Matching mesh pieces share one clock. Turning this off restores their input pose.":
        "在物理运算之前播放预烘焙的骨骼动作。匹配的网格部件共用同一时钟。关闭后会恢复它们原本的输入姿势。",
    "All physics": "全部物理",
    "Master switch for physics only; custom Actions keep playing. Layout and individual system choices are preserved while this is OFF.":
        "只控制物理的总开关；自定义动作仍会继续播放。关闭期间，布局与各子系统的独立选项都会保留。",
    "Statistics overlay": "统计信息浮层",
    "Show per-layout animation groups and active pieces at the upper right. Counts refresh once per second. Does not change rigs or physics.":
        "在右上角显示各布局的动画分组与当前生效的部件。计数每秒刷新一次。不会改变骨骼或物理。",

    # 手部 IK（三选一）
    "Hand IK": "手部 IK",
    "OFF: no hand correction. ON: both hands follow original animation targets. AUTO: correct each hand only while weapon-bone contact is detected. Unconfirmed first-person right-hand contact stays OFF.":
        "关闭：不做手部修正。开启：双手跟随原动画目标。自动：仅在检测到武器与骨骼接触时修正对应的那只手；第一人称下未经确认的右手接触保持关闭。",
    "Auto": "自动",
}
