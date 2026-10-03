# -*- coding: utf-8 -*-
"""cn_strings.py —— 英文原文 -> 简体中文 词表（用于 Mod Options Menu 选项文本汉化）。

键必须与模组注册时传入的字符串逐字符一致（多行 .. 拼接的按拼接后的完整文本为键）。
'Off' 故意不翻译：Mod Options Menu 会用游戏自带的原生词（关）。
"""

CN = {
    # ---------------- Aggro Counter ----------------
    'Aggro Counter': '仇恨计数',
    'Show Badge': '显示徽章',
    'Show the badge beside the compass. Same as Ctrl+Shift+O.': '在罗盘旁显示徽章。同 Ctrl+Shift+O。',
    'Position': '位置',
    'Where the badge sits. Beside the compass it grows away from it when enlarged.':
        '徽章所在位置。放大时会向背离罗盘的方向扩展。',
    'Left of Compass': '罗盘左侧',
    'Right of Compass': '罗盘右侧',
    'Under Warning Banners': '警告横幅下方',
    'Size': '大小',
    'Badge size. It shrinks by itself if it does not fit beside the compass.':
        '徽章尺寸。若罗盘旁放不下会自动缩小。',
    'Move Right': '向右移动',
    'Nudge the badge sideways, in 1440p pixels (negative = left). Same as Ctrl+Shift+J / L.':
        '左右微调徽章，单位 1440p 像素（负值 = 向左）。同 Ctrl+Shift+J / L。',
    'Move Down': '向下移动',
    'Nudge the badge up or down, in 1440p pixels (negative = up). Same as Ctrl+Shift+I / K.':
        '上下微调徽章，单位 1440p 像素（负值 = 向上）。同 Ctrl+Shift+I / K。',
    'Nearby Cell': '附近计数',
    'Radar: every live enemy within the nearby radius of you, whatever it is doing.':
        '雷达：附近半径内所有存活敌人，无论它在做什么。',
    'Searching Cell': '搜索计数',
    'Eye: enemies searching for you (lost sight of you, alerted, dropping in, emerging).':
        '眼睛：正在搜索你的敌人（跟丢你、进入警戒、空降、钻出地面）。',
    'On You Cell': '锁定你',
    'Reticle: enemies fighting you, or the vehicle you are in.':
        '准星：正在攻击你或你所乘载具的敌人。',
    'Teammates Cell': '锁定队友',
    'People: enemies fighting your teammates.': '人物：正在攻击你队友的敌人。',
    'When Nothing Is Counted': '计数全为零时',
    'What the badge does while every shown number is 0.': '所有显示数字均为 0 时，徽章的表现。',
    'Dim': '变暗',
    'Hide': '隐藏',
    'Show': '显示',
    'Background Opacity': '背景不透明度',
    'Red From': '变红阈值',
    'Enemies on you from which the on-you number and bar turn red.':
        '锁定你的敌人达到该数量时，「锁定你」的数字与进度条变红。',
    'Nearby Radius (m)': '附近半径（米）',
    'How far the nearby cell counts enemies.': '附近计数统计敌人的最远距离。',
    'Ctrl+Shift Keys': 'Ctrl+Shift 快捷键',
    'The Ctrl+Shift keys that show, resize and move the badge.':
        '用于显示、缩放和移动徽章的 Ctrl+Shift 快捷键。',
    'Let HUD Mods Replace It': '允许 HUD 模组接管',
    'Another HUD mod may hide this badge while it shows the same numbers itself.':
        '其他 HUD 模组可隐藏此徽章，改由它自己显示相同数字。',
    'Diagnostic Log': '诊断日志',
    'Detailed log (Logs/AggroCounter.log) for bug reports; F8 then marks the moment. Leave it off otherwise.':
        '用于反馈问题的详细日志（Logs/AggroCounter.log）；F8 可标记当前时刻。平时请保持关闭。',

    # ---------------- Armored Overhaul ----------------
    'ARMORED OVERHAUL': '装甲大修',
    'Tank Power': '坦克动力',
    'More pulling power for the Bastion and Maelstrom: quicker off the line and up slopes. Top speed is unchanged.':
        '提升堡垒与漩涡的牵引力：起步与爬坡更快。最高速度不变。',
    'Strong (x1.25)': '强劲 (x1.25)',
    'Stronger (x1.5)': '更强 (x1.5)',
    'Strongest (x2)': '极强 (x2)',
    'Tank Grip': '坦克抓地',
    'More track grip for the Bastion and Maelstrom: less sliding on slopes and in turns.':
        '提升堡垒与漩涡的履带抓地力：减少在斜坡和转弯时的打滑。',
    'Moderate (x1.25)': '适度 (x1.25)',
    'Maximum (x2)': '最大 (x2)',
    'Tank Steering': '坦克转向',
    'Quicker steering for the Bastion and Maelstrom: they start and stop turning sooner.':
        '堡垒与漩涡转向更灵敏：起转与停转都更早。',
    'Responsive (x1.25)': '灵敏 (x1.25)',
    'Quick (x1.5)': '迅捷 (x1.5)',
    'Sharp (x2)': '锐利 (x2)',
    'Tank MBT Turrets': '坦克主战炮塔',
    "The Bastion and Maelstrom turrets turn all the way round like a main battle tank. The Maelstrom's missile pods and smoke launchers turn with it. Only you see the new turrets, and their armor always looks undamaged.":
        '堡垒与漩涡的炮塔可像主战坦克一样整圈旋转，漩涡的导弹发射巢与烟雾发射器会随之转动。新炮塔只有你能看到，且其装甲始终显示为未受损。',
    'Tank Turret Traverse': '炮塔回旋速度',
    'How fast the Bastion and Maelstrom turrets turn (the game: 25 degrees a second). Works with or without MBT Turrets.':
        '堡垒与漩涡炮塔的旋转速度（游戏原版：每秒 25 度）。无论是否启用主战炮塔均有效。',
    'Quick (x1.25)': '快捷 (x1.25)',
    'Fast (x1.5)': '快速 (x1.5)',
    'Very fast (x2)': '极快 (x2)',
    'Tank Turret Elevation': '炮塔俯仰速度',
    'How fast the Bastion and Maelstrom guns move up and down (the game: 35 degrees a second).':
        '堡垒与漩涡火炮上下俯仰的速度（游戏原版：每秒 35 度）。',
    'Tank Turret Aim Range': '炮塔俯仰范围',
    'How far down and up the Bastion and Maelstrom guns aim (the game: 3 below to 25 above).':
        '堡垒与漩涡火炮的俯仰角度范围（游戏原版：向下 3 度至向上 25 度）。',
    'Wide (-6..+30 deg)': '宽 (-6..+30 度)',
    'Wider (-10..+35 deg)': '更宽 (-10..+35 度)',
    'Widest (-15..+45 deg)': '最宽 (-15..+45 度)',
    'Tank Autoloader': '坦克自动装填',
    'The Bastion and Maelstrom main gun reloads by itself when it runs dry, at the normal reload speed (perks count). You can still reload by hand.':
        '堡垒与漩涡的主炮打空后会自动装填，速度为正常装填速度（受加成影响）。仍可手动装填。',
    'Gunner Drive': '炮手驾驶',
    "Drive from the gunner seat when the driver seat is empty: your movement keys drive and a driver panel shows gear, rpm, speed and fuel. F sounds the horn; Mouse 3 pops the Maelstrom's smoke. Controller: the left stick drives, its click is the horn, the right stick click pops smoke. Set your own keys with the Mod Bindings Menu. A teammate who takes the wheel drives. Pick which vehicles.":
        '驾驶座无人时可从炮手座驾驶：用移动键开车，并显示档位、转速、速度与燃料的驾驶面板。F 鸣笛；鼠标中键释放漩涡的烟雾。手柄：左摇杆驾驶，按下左摇杆鸣笛，按下右摇杆放烟。可用 Mod Bindings Menu 自定义按键。队友上车驾驶时由队友操控。可选择适用载具。',
    'Tanks and FRV': '坦克与 FRV',
    'Tanks': '坦克',
    'FRV': 'FRV',
    'Tank Gunner Camera': '坦克炮手视角',
    'Puts the Bastion and Maelstrom gunner camera lower and further back so you see more around the tank. It stays behind the turret as it turns.':
        '把堡垒与漩涡的炮手视角放低并后移，让你看到坦克周围更多区域。炮塔转动时视角保持在炮塔后方。',
    'Close (1 m behind)': '近（身后 1 米）',
    'Far (3.5 m behind)': '远（身后 3.5 米）',
    'Farther (5.4 m behind)': '更远（身后 5.4 米）',
    'Farthest (7.4 m behind)': '最远（身后 7.4 米）',
    'Vehicle Indicator': '载具指示器',
    "A small outline of your vehicle shows where the gun points compared to the hull, colored by health (blue to red). Works in the Bastion, the Maelstrom, the M-102 FRV and the M-103 Supply FRV, in any seat; the FRVs' tires each show their own health and go clear when popped. Only you see it.":
        '用小型轮廓显示载具火炮相对车体的指向，并按血量着色（蓝到红）。适用于堡垒、漩涡、M-102 FRV 与 M-103 补给 FRV 的任意座位；FRV 的每个轮胎单独显示血量，爆胎后变透明。只有你能看到。',

    # ---------------- Smarter Guard Dogs & Sentries ----------------
    'SMARTER GUARD DOGS & SENTRIES': '更聪明的护卫犬与哨戒炮',
    'Guard Dogs': '护卫犬',
    'The mod handles your guard dog (Guard Dog, Rover, K-9). Turn off to leave your dog to the game; your sentries and the rest of the mod keep working.':
        '本模组接管你的护卫犬（护卫犬、漫游者、K-9）。关闭后护卫犬交还给游戏，哨戒炮及本模组其余功能仍然生效。',
    'Sentries': '哨戒炮',
    'The mod handles your sentries (Machine Gun, Gatling, Autocannon, Rocket, Laser, Flame, Mortar, EMS Mortar and the Tesla Tower), plus the guns on armed resupply pods and the Supply FRV. Turn off to leave your sentries to the game; your guard dog and the rest of the mod keep working.':
        '本模组接管你的哨戒炮（机枪、加特林、自动炮、火箭、激光、火焰、迫击炮、EMS 迫击炮与特斯拉塔），以及武装补给舱和补给 FRV 上的机枪。关闭后哨戒炮交还给游戏，护卫犬及本模组其余功能仍然生效。',
    'All sentries': '全部哨戒炮',
    'All but the Tesla Tower': '除特斯拉塔外的全部',
    'Intelligence': '智能决策',
    "How your dogs and sentries choose what to shoot. Armor Intelligence: they leave alone armor they can't hurt, fire only short bursts at Heavy Devastators, and no sentry wastes ammo on dropships. Target Prioritization: your dog goes for the closest threat to you first; your sentries deal with enemies at their feet, Gunships and the armor that suits the gun first. Turn off to leave both to the game.":
        '你的护卫犬与哨戒炮如何选择射击目标。装甲识别：放过打不穿的装甲目标，对重型毁灭者只做短点射，哨戒炮不会把弹药浪费在运输舰上。目标优先：护卫犬优先攻击离你最近的威胁；哨戒炮优先处理脚下的敌人、炮艇以及适合其火力的装甲。关闭后两项都交还给游戏。',
    'Armor Intelligence and Target Prioritization': '装甲识别 + 目标优先',
    'Only Armor Intelligence': '仅装甲识别',
    'Only Target Prioritization': '仅目标优先',
    'Safety': '安全防护',
    "Who your dog and your sentries never fire through: they hold fire while that helldiver is in their line of fire, don't swing their fire across them, mortars and the rocket sentry leave enemies next to them alone, and the Tesla Tower doesn't zap them or arc into them. Turn off at your own risk: they will fire through anyone. Everything else keeps working.":
        '你的护卫犬与哨戒炮绝不误伤的对象：当该潜兵位于射线上时它们会停火，不会把火力扫过对方，迫击炮与火箭哨戒炮会放过紧挨着对方的敌人，特斯拉塔也不会电到或电弧到对方。关闭后果自负：它们会朝任何人开火。其余功能不受影响。',
    'You and your teammates': '你与队友',
    'Only you': '仅你',
    'Only your teammates': '仅队友',
    'Targeting Laser': '瞄准激光',
    "Laser out of the barrel of your guard dog and your sentries (not the mortars) toward their targets, shown only on your screen: green while they fire, flashing red when the safety stops a shot, flashing yellow when the dog's target goes out of sight. The Tesla Tower shows its reach as a yellow ring. Line: thin, hidden by walls. Glow: a soft beam that shows through walls.":
        '从护卫犬与哨戒炮（迫击炮除外）炮口射向目标的激光，仅你可见：开火时为绿色，被安全防护拦下时闪红，护卫犬丢失目标时闪黄。特斯拉塔以黄圈显示其作用范围。细线：纤细，会被墙挡住。辉光：柔和光束，可透过墙壁看到。',
    'Line': '细线',
    'Glow': '辉光',
    'Laser Brightness': '激光亮度',
    'How bright the targeting laser is: its beams and rings, line or glow.':
        '瞄准激光的亮度：光束与光圈，细线或辉光均适用。',
    'Dim (50%)': '暗 (50%)',
    'Softer (75%)': '较柔 (75%)',
    'Normal (100%)': '正常 (100%)',
    'Bright (150%)': '亮 (150%)',
    'Brightest (200%)': '最亮 (200%)',
}
