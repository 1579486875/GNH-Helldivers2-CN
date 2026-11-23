# -*- coding: utf-8 -*-
"""cn_ui4.py -- 第四批词表：多行拼接的说明文字 + 遗漏项。

为什么要单独一批：Lua 里这几条说明是这样写的 ——
    description = 'Nudge the badge sideways, in 1440p pixels (negative = left). '
                  .. 'Same as Ctrl+Shift+J / L.'
运行时送进菜单的是**拼接之后的完整句子**，所以词表的键也必须是拼好的整句，
只写第一段是匹配不上的（这也是之前扫描工具漏掉它们的原因）。
"""

CN_UI4 = {
    # ---------- Aggro Counter 1.3：四条跨行拼接的选项说明 ----------
    "Nudge the badge sideways, in 1440p pixels (negative = left). Same as Ctrl+Shift+J / L.":
        "左右微调徽章位置，单位为 1440p 像素（负值 = 左移）。等同于 Ctrl+Shift+J / L。",
    "Nudge the badge up or down, in 1440p pixels (negative = up). Same as Ctrl+Shift+I / K.":
        "上下微调徽章位置，单位为 1440p 像素（负值 = 上移）。等同于 Ctrl+Shift+I / K。",
    "Another HUD mod may hide this badge while it shows the same numbers itself.":
        "其他 HUD 模组在自行显示相同数字时，可以隐藏本徽章。",
    "Detailed log (Logs/AggroCounter.log) for bug reports; F8 then marks the moment. Leave it off otherwise.":
        "为反馈问题记录详细日志（Logs/AggroCounter.log）；按 F8 会标记当前时刻。平时建议关闭。",

    # ---------- HD2 Transmog：变体编辑器里的空状态提示 ----------
    "No variant selected": "未选择任何变体",
}
