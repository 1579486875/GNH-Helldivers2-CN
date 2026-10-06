# -*- coding: utf-8 -*-
"""cn_pack9.py -- 2026-10-06 第三批修正。

1) 全角引号「」在「右侧大标题」这个渲染位置会显示成 ? ——
   该处的字体不含这两个字形（同一字符串在左侧选项行显示正常，说明两处字体不同）。
   因此凡是会被当作"选项名/标题"的短词条，一律去掉「」。
2) 超级体能的选项说明原先只登记了被截断的片段，与模组实际注册的完整句对不上，
   这里补上完整键。说明正文里的「」不受影响（实测该位置显示正常）。
3) 高度警戒的模组名带斜杠长名，收短。
"""

CN_PACK9 = {
    # 1) 去掉全角引号（右侧大标题字体不支持）
    "Require Muscle Enhancement": "需要肌肉强化加持",

    # 2) 补完整描述键（原键是截断片段，匹配不上）
    "Running with a heavy object only works when someone in the mission brought the Muscle Enhancement booster. Without it you carry at the normal speed.":
        "只有任务中有人带了「肌肉强化」增益时，负重奔跑才会生效；否则只能按正常速度搬运。",

    # 3) 缩短带斜杠的模组名
    "高度警戒 / High Alert": "高度警戒",
    "High Alert": "高度警戒",
}
