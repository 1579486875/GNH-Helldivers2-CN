# -*- coding: utf-8 -*-
"""cn_pack10.py —— 2026-10-10 模组更新后的新一轮补充词表。

覆盖：
  * 高度警戒 / High Alert 1.9.2 —— 新增「分色 / 普通·重型·炮击 三套参数」共 49 条
  * 装甲大修 3.4.0 —— 新增炮手视角、引擎、转向、炮塔位置、载具配置等 43 条
  * 更聪明的护卫犬与哨戒炮 4.6.4 —— 三条重写的选项说明
  * C-Rig 骨骼运行时 v0.6 —— 新的 IK 模式说明与选项值
  * Vanilla Plus v40 —— 行文本标签

⚠ 键必须是「运行时字符串」：Lua 源码里写作 'Menu\\'s' 的，运行时是 "Menu's"，
   所以本表里的键一律是**去掉反斜杠的原文**。
"""

CN_PACK10 = {
    # ─────────────── 高度警戒 / High Alert 1.9.2 ───────────────
    # 选项名（新增的分色系统：普通 / 重型 / 炮击 三套参数）
    "Split Colors": "分色显示",
    "Normal Radius": "普通半径",
    "Normal Spread": "普通扩散",
    "Normal Color": "普通颜色",
    "Normal Brightness": "普通亮度",
    "Normal Tone": "普通色调",
    "Normal Opacity": "普通不透明度",
    "Normal Range": "普通探测范围",
    "Normal Boost": "普通增强",
    "Normal Rate": "普通闪烁频率",
    "Heavy Radius": "重型半径",
    "Heavy Spread": "重型扩散",
    "Heavy Color": "重型颜色",
    "Heavy Brightness": "重型亮度",
    "Heavy Tone": "重型色调",
    "Heavy Opacity": "重型不透明度",
    "Heavy Range": "重型探测范围",
    "Heavy Boost": "重型增强",
    "Heavy Rate": "重型闪烁频率",
    "Artillery On": "炮击警报",
    "Artillery Radius": "炮击半径",
    "Artillery Spread": "炮击扩散",
    "Artillery Color": "炮击颜色",
    "Artillery Brightness": "炮击亮度",
    "Artillery Tone": "炮击色调",
    "Artillery Opacity": "炮击不透明度",
    "Artillery Range": "炮击探测范围",
    "Artillery Boost": "炮击增强",
    "Artillery Rate": "炮击闪烁频率",
    # 选项说明
    "Heavy alerts take priority. Turn off to use Normal settings for all enemies.":
        "重型警报优先。关闭后所有敌人一律使用「普通」那套设置。",
    "Bloom depth: 1-30% of screen height; default 10.0%. Sets inward glow reach; highlight stays thin.":
        "光晕深入：屏幕高度的 1-30%，默认 10.0%。决定光晕能向内扩散多远；高亮描边始终保持细线。",
    "On: glow span and depth grow linearly to maximum at 3 m. Off: fixed radius.":
        "开启：光晕范围与深入随距离线性增长，3 米时达到最大。关闭：半径固定不变。",
    "Default: Yellow. Presets: Yellow, Orange, Red, Blue, White, Pink, Purple.":
        "默认：黄色。预设：黄、橙、红、蓝、白、粉、紫。",
    "Base brightness: 1-5x; default 3.0x; step 0.1. Original proximity response is preserved.":
        "基础亮度：1-5 倍，默认 3.0 倍，步进 0.1。保留原版的靠近响应曲线。",
    "Color tone: 0-1; default 0.8. 0 is black; 1 is full color. Original proximity response is preserved.":
        "颜色色调：0-1，默认 0.8。0 为黑色，1 为纯色。保留原版的靠近响应曲线。",
    "Opacity: 0-1; default 0.6. 0 is invisible; 1 is most visible. Original proximity response is preserved.":
        "不透明度：0-1，默认 0.6。0 为完全不可见，1 为最明显。保留原版的靠近响应曲线。",
    "Detection range: 5-30 m; default 12.1 m; step 0.1. Only living enemies targeting you trigger alerts.":
        "探测范围：5-30 米，默认 12.1 米，步进 0.1。只有正在锁定你的活体敌人才会触发警报。",
    "Master proximity boost. Rate and radius grow linearly to maximum at 3 m; brightness and opacity keep their original curves.":
        "靠近增强总开关。闪烁频率与半径随距离线性增长、3 米时达到最大；亮度与不透明度仍沿用原版曲线。",
    "Max flash rate: 1-5x; default 3.0x. Reaches maximum at 3 m. Set to 1 for base rate.":
        "最大闪烁频率：1-5 倍，默认 3.0 倍。3 米时达到最大。设为 1 则使用基础频率。",
    "Bloom depth: 1-30% of screen height; default 12.0%. Sets inward glow reach; highlight stays thin.":
        "光晕深入：屏幕高度的 1-30%，默认 12.0%。决定光晕能向内扩散多远；高亮描边始终保持细线。",
    "On: glow span and depth grow linearly to maximum at 6 m. Off: fixed radius.":
        "开启：光晕范围与深入随距离线性增长，6 米时达到最大。关闭：半径固定不变。",
    "Default: Red. Presets: Yellow, Orange, Red, Blue, White, Pink, Purple.":
        "默认：红色。预设：黄、橙、红、蓝、白、粉、紫。",
    "Detection range: 5-30 m; default 20.1 m; step 0.1. Only living enemies targeting you trigger alerts.":
        "探测范围：5-30 米，默认 20.1 米，步进 0.1。只有正在锁定你的活体敌人才会触发警报。",
    "Master proximity boost. Rate and radius grow linearly to maximum at 6 m; brightness and opacity keep their original curves.":
        "靠近增强总开关。闪烁频率与半径随距离线性增长、6 米时达到最大；亮度与不透明度仍沿用原版曲线。",
    "Max flash rate: 1-5x; default 2.0x. Reaches maximum at 6 m. Set to 1 for base rate.":
        "最大闪烁频率：1-5 倍，默认 2.0 倍。6 米时达到最大。设为 1 则使用基础频率。",
    "Cannon alerts; highest priority per direction. Includes cannon towers, small turrets, Factory Strider and Vox main cannons.":
        "炮击警报；在同一方向上优先级最高。涵盖加农炮塔、小型炮塔、工厂机兽与 Vox 主炮。",
    "Default: bright Red (tone 1.0). Presets: Yellow, Orange, Red, Blue, White, Pink, Purple.":
        "默认：亮红色（色调 1.0）。预设：黄、橙、红、蓝、白、粉、紫。",
    "Color tone: 0-1; default 1.0. 0 is black; 1 is full color. Original proximity response is preserved.":
        "颜色色调：0-1，默认 1.0。0 为黑色，1 为纯色。保留原版的靠近响应曲线。",
    "Detection range: 50-200 m; default 200.0 m; step 0.1. Only living cannons targeting you or your occupied mech trigger alerts.":
        "探测范围：50-200 米，默认 200.0 米，步进 0.1。只有正在锁定你、或锁定你所驾驶机甲的活体炮台才会触发警报。",

    # ─────────────── 装甲大修 3.4.0 ───────────────
    "Tank Turret Position": "坦克炮塔位置",
    "Vehicle Loadout": "载具配置",
    # 选项值
    # 颜色预设 —— 高度警戒的 COLOR_NAMES 是运行时从 PALETTES[i].name 拼出来的，
    # 源码里写作 name='Yellow' 而不是 choices={...}，所以扫描器抓不到，只能按名单手工补。
    # ⚠ 菜单会把选项值先转成大写再查表，所以译文里不要留小写拉丁字母（x1.1 会显示成 X1.1），
    #   倍数一律写成大写 X。
    "Yellow": "黄色",
    "Orange": "橙色",
    "Blue": "蓝色",
    "White": "白色",
    "Pink": "粉色",
    "Purple": "紫色",
    "Close (about 1.5 m back)": "近（后移约 1.5 米）",
    "Far (about 3.5 m back)": "远（后移约 3.5 米）",
    "Farther (about 5 m back)": "更远（后移约 5 米）",
    "Farthest (about 6.5 m back)": "最远（后移约 6.5 米）",
    "Fast (x1.1)": "快（X1.1）",
    "Faster (x1.15)": "更快（X1.15）",
    "Fastest (x1.3)": "最快（X1.3）",
    "Strong (x1.2)": "强（X1.2）",
    "Stronger (x1.35)": "更强（X1.35）",
    "Strongest (x1.5)": "最强（X1.5）",
    "Moderate (x1.2)": "适中（X1.2）",
    "Strong (x1.35)": "强（X1.35）",
    "Maximum (x1.5)": "最高（X1.5）",
    "Quick": "迅速",
    "Quicker": "更迅速",
    "Instant": "瞬时",
    "Steady": "平稳",
    "Original": "原版",
    "Centered": "居中",
    # 选项说明
    "Puts the Bastion and Maelstrom gunner camera lower and further back so you see more around the tank. It stays behind the turret as it turns. The pick is where the camera starts: the mouse wheel (or the Mod Bindings Menu's Zoom In / Zoom Out keys) moves it closer or further back, and from the closest point zooms in on the crosshair.":
        "把堡垒与漩涡的炮手视角放得更低、更靠后，让你能看到坦克周围更多东西。视角会随着炮塔转动、始终待在炮塔后方。所选项是视角的起始位置：用鼠标滚轮（或「模组按键菜单」里的放大 / 缩小键）可以让它靠近或后移，从最近处起则会朝准星拉近。",
    "While you drive from the gunner seat with Gunner Drive, a panel like the driver's own HUD shows the gear, rpm, speed, fuel and the Maelstrom's smoke rounds. It only shows while you are the one driving. Only you see it.":
        "当你用「炮手驾驶」从炮手位开车时，会显示一块类似驾驶员 HUD 的面板，标出挡位、转速、速度、燃料以及漩涡的烟雾弹余量。只有你亲自驾驶时才显示，且只有你能看到。",
    "A faster Bastion and Maelstrom: more engine speed and pulling power, forward and in reverse. Changes the tank you are in at once.":
        "让堡垒与漩涡更快：提升发动机转速与牵引力，前进与倒退都受益。对你当前所在的坦克立即生效。",
    "More engine torque for the Bastion and Maelstrom: quicker off the line and up slopes. Changes the tank you are in at once.":
        "提升堡垒与漩涡的发动机扭矩：起步更快、爬坡更轻松。对你当前所在的坦克立即生效。",
    "More track grip for the Bastion and Maelstrom: less sliding on slopes and in turns. Changes the tank you are in at once.":
        "提升堡垒与漩涡的履带抓地力：在斜坡与转弯时更不容易打滑。对你当前所在的坦克立即生效。",
    "Keeps the Bastion and Maelstrom on the ground: pressed down harder the faster they go, so they stay flat over crests and bumps instead of floating. Changes the tank you are in at once.":
        "把堡垒与漩涡牢牢压在地面上：速度越快下压力越大，越过坡顶与颠簸时不再飘起来。对你当前所在的坦克立即生效。",
    "Quicker steering for the Bastion and Maelstrom: they start and stop turning sooner. Changes every tank at once.":
        "让堡垒与漩涡转向更利落：开始与停止转向都更及时。对场上所有坦克立即生效。",
    "Snappier Bastion and Maelstrom: the throttle and brake let go sooner, and gear and direction changes wait less (Instant: no wait). Changes every tank at once.":
        "让堡垒与漩涡更跟手：松开油门与刹车后动力更快切断，换挡与换向的等待更短（「瞬时」= 完全不等）。对场上所有坦克立即生效。",
    "Drive from the gunner seat when the driver seat is empty: your movement keys drive, shift and CTRL change gear, Space is the handbrake. F sounds the horn; Mouse 3 pops the Maelstrom's smoke. Controller: the left stick drives, its click is the horn, the right stick click pops smoke. Keys set in the Mod Bindings Menu replace these. A teammate who takes the wheel drives. Pick which vehicles.":
        "驾驶位空着时可以直接从炮手位开车：移动键负责行驶，Shift 与 CTRL 换挡，空格是手刹。F 按喇叭；鼠标中键放出漩涡的烟雾。手柄：左摇杆行驶，按下左摇杆按喇叭，按下右摇杆放烟雾。「模组按键菜单」里设过的键会覆盖以上默认值。队友抢到方向盘时由队友驾驶。可选择对哪些载具生效。",
    "MBT Turrets: where the Bastion and Maelstrom turret sits. Original is the game's place. Centered puts it in the middle of the hull like a main battle tank: the gun reaches past the front deck, so it clips less when aimed low. Changes at once. The tank's hit areas stay the game's own.":
        "主战坦克炮塔：决定堡垒与漩涡的炮塔坐在哪。选「原版」就是游戏本来的位置；选「居中」会把炮塔移到车体正中间，像真正的主战坦克那样，炮管能越过前甲板，俯角瞄低时穿模更少。立即生效。坦克的受击判定仍沿用游戏原版。",
    "How fast the Bastion and Maelstrom turrets turn (the game: 25 degrees a second), and the gunner view left/right with them. Very fast is 75. Changes every tank at once; the view from the next time you sit in the gunner seat.":
        "堡垒与漩涡炮塔的转动速度（游戏原版：每秒 25 度），炮手视角的左右转动会同步跟随。「极快」为 75。对场上所有坦克立即生效；视角要等下次坐进炮手位时才刷新。",
    "How fast the Bastion and Maelstrom guns move up and down (the game: 35 degrees a second), and the gunner view up/down with them. Changes every tank at once; the view from the next time you sit in the gunner seat.":
        "堡垒与漩涡火炮的俯仰速度（游戏原版：每秒 35 度），炮手视角的上下转动会同步跟随。对场上所有坦克立即生效；视角要等下次坐进炮手位时才刷新。",
    "How far down and up the Bastion and Maelstrom guns aim (the game: 3 below to 25 above), and the gunner view up/down with them. Changes every tank at once; the view from the next time you sit in the gunner seat.":
        "堡垒与漩涡火炮的俯仰范围（游戏原版：向下 3 度、向上 25 度），炮手视角的上下活动范围会同步跟随。对场上所有坦克立即生效；视角要等下次坐进炮手位时才刷新。",
    "A small outline of your vehicle shows where the gun points compared to the hull, colored by health (blue to red). Works in the Bastion, the Maelstrom, the M-102 FRV and the M-103 Supply FRV, in any seat; the FRVs' tires each show their own health and go clear when popped. Only you see it.":
        "用一个小轮廓标出你的载具朝向、以及炮口相对车体指向何方，并按血量上色（蓝到红）。在堡垒、漩涡、M-102 快速侦察车与 M-103 补给侦察车里都能用，任何座位都行；侦察车的每条轮胎各自显示血量，爆胎后变透明。只有你能看到。",
    "Pick more than one tank, exosuit or FRV in your stratagem loadout (the game puts a second one in the first one's slot). Changes at once; turning it off puts the game's limit back.":
        "允许在战备配置里同时带多辆坦克、机甲或快速侦察车（游戏原本会把第二辆塞进第一辆的格子里）。立即生效；关闭后恢复游戏的原有上限。",

    # ─────────────── 更聪明的护卫犬与哨戒炮 4.6.4 ───────────────
    "How your dogs and sentries choose what to shoot. Armor Intelligence: they leave alone armor they can't hurt, fire only short bursts at Heavy Devastators, and no sentry wastes ammo on dropships. Target Prioritization: your dog goes for the closest threat to you first; your sentries deal with enemies at their feet, Gunships and the armor that suits the gun first. Turn off to leave both to the game.":
        "决定护卫犬与哨戒炮如何挑选射击目标。装甲智能：它们会放过自己打不穿的装甲，对重型毁灭者只打短点射，哨戒炮也不会再浪费弹药去打运输舰。目标优先级：护卫犬优先处理离你最近的威胁；哨戒炮优先处理脚边的敌人、炮艇，以及最适合当前武器对付的装甲。关闭后两者都交回游戏原版逻辑。",
    "Who your dog and your sentries never fire through: they hold fire while that helldiver is in their line of fire, don't swing their fire across them, mortars and the rocket sentry leave enemies next to them alone, and the Tesla Tower doesn't zap them or arc into them. Turn off at your own risk: they will fire through anyone. Everything else keeps working.":
        "设定护卫犬与哨戒炮不会向谁开火：当那名绝地潜兵处在射线上时它们会停火，扫射时也不会横扫过他；迫击炮与火箭哨戒炮会放过贴着他的敌人，特斯拉塔既不会电到他、也不会朝他拉弧。关闭风险自负：它们会直接穿过任何人开火。其余功能照常。",
    "Laser out of the barrel of your guard dog and your sentries (not the mortars) toward their targets, shown only on your screen: green while they fire, flashing red when the safety stops a shot, flashing yellow when the dog's target goes out of sight. The Tesla Tower shows its reach as a yellow ring. Line: thin, hidden by walls. Glow: a soft beam that shows through walls.":
        "从护卫犬与哨戒炮（不含迫击炮）的炮口朝目标画出一条激光，只显示在你的屏幕上：开火时为绿色，因安全限制停火时闪红，护卫犬的目标脱离视野时闪黄。特斯拉塔会用一个黄色圆环标出作用范围。细线：很细，会被墙挡住。光柱：柔和的光束，可以穿墙显示。",

    # ─────────────── C-Rig 骨骼运行时 v0.6 ───────────────
    "Requires this layout's Custom rig. Off: no IK. On: full IK. Auto: full IK with weapon contact. Partial: layout XYZ weights. Auto (Partial): full IK with contact, partial otherwise. Original hand orientation is retained.":
        "需要该布局带 Custom（自订）骨骼。关闭：不做 IK。开启：完整 IK。自动：完整 IK，并处理武器接触。部分：按布局的 XYZ 权重。自动（部分）：有接触时用完整 IK，其余情况用部分 IK。手部原始朝向保持不变。",
    "Partial": "部分",
    "Auto (Partial)": "自动（部分）",

    # ─────────────── Vanilla Plus v40 ───────────────
    "Row text": "行文本",
    "Shown beside the rows -- while the option is selected":
        "在行旁显示 —— 仅当该选项被选中时",
}
