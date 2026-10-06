# -*- coding: utf-8 -*-
"""cn_pack6.py —— 2026-10-06 新增词条。

来源：对当前 34 个启用模组做全量界面文本扫描，与既有 678 条词表比对后
剩余的「纯英文」条目。覆盖此前完全没做过汉化的模组：

  * 战术战斗大修 v1.7.9（Tactical Combat Overhaul）—— 31 个选项名 + 32 条说明
  * 边跑边打 v1.0.4（Run-N-Gun）—— 5 个选项名 + 5 条说明
  * 装甲大修 3.2.0（Armored Overhaul）—— 10 条说明
  * 其它零散：护卫犬 3 条、仇恨计数 5 条、C4 2 个按键名、C-Rig / 超级体能 等

键必须与模组注册时传入的字符串逐字符一致（含冒号后的空格、' 符号等）。
说明文本一律控制在 400 字以内（ModOptionsMenu 的说明上限），
选项名 64 字以内 —— 超限会被整个拒绝注册，比显示英文更糟。

有几条原文是 Lua 里用 .. 拼起来的片段（如 'Native: ... in line with '），
本表只翻译其中出现的字面量部分，拼接逻辑不受影响。
"""

CN_PACK6 = {
    # ═══════════════ 战术战斗大修 v1.7.9 ═══════════════
    # ── 力竭 ──
    "Winded Sway": "气喘晃动",
    "EXHAUSTION: Uses the game's own exertion levels, the heavy-breathing state that builds while sprinting and peaks when stamina runs out. ON makes aim sway grow more at those levels. Rested aim is unchanged.":
        "力竭：沿用游戏自身的用力等级（冲刺时逐渐加重、耐力见底时达到峰值）。开启后这些等级会让瞄准晃动更明显；不喘时的瞄准不受影响。",
    "Winded Sway Strength": "气喘晃动强度",
    "EXHAUSTION (% of normal): Scales the EXTRA sway each exertion level adds. Normally the most winded level sways 1.6x; 250 makes it 2.5x, 500 makes it 4x. Levels with no extra sway stay unchanged. 100 = normal.":
        "力竭（正常值的百分比）：调整各用力等级额外增加的晃动。原本喘得最厉害时晃动为 1.6 倍；设为 250 变成 2.5 倍，500 变成 4 倍。本身没有额外晃动的等级不受影响。100 = 正常。",

    # ── 姿态回复 ──
    "Stance Recovery": "姿态回复",
    "RECOVERY: Changes how fast stamina refills in each stance. Normal full refill takes 7 s standing, 6 s crouched and 5 s prone. The wait before refilling starts is the Delay group below.":
        "回复：调整各姿态下耐力条的回充速度。原本站满需 7 秒、蹲下 6 秒、趴下 5 秒。开始回充前的等待时间见下方「延迟」组。",
    "Recovery Speed: Standing": "回复速度：站立",
    "RECOVERY (% of normal): Stamina refill speed while standing. 70 = a full refill takes 10 s instead of 7 s. Lower values push you to take a knee to catch your breath. 100 = normal.":
        "回复（正常值的百分比）：站立时的耐力回充速度。70 表示回满需要 10 秒（原本 7 秒）。数值越低越需要蹲下来喘口气。100 = 正常。",
    "Recovery Speed: Crouched": "回复速度：蹲下",
    "RECOVERY: Stamina refill speed while crouched. 150 = a full refill takes 4 s instead of 6 s. 100 = normal.":
        "回复：蹲下时的耐力回充速度。150 表示回满需要 4 秒（原本 6 秒）。100 = 正常。",
    "Recovery Speed: Prone": "回复速度：趴下",
    "RECOVERY: Stamina refill speed while prone. 150 = a full refill takes about 3.3 s instead of 5 s. 100 = normal.":
        "回复：趴下时的耐力回充速度。150 表示回满约需 3.3 秒（原本 5 秒）。100 = 正常。",

    # ── 延迟 ──
    "Recovery Delay": "回复延迟",
    "DELAY (seconds): The wait after using stamina (running, sliding, melee weapons, anything) before it refills. Game: 1.5 s in every stance. Your current stance sets the wait, and changing stance mid-wait counts once live stamina is confirmed (a moment of sprinting each mission).":
        "延迟（秒）：消耗耐力后（奔跑、滑铲、近战武器等）到开始回充之间的等待时间。原版各姿态均为 1.5 秒。等待时间由当前姿态决定；确认实时耐力后（每局先冲刺一下），等待中途换姿态也会立即生效。",
    "Delay: Standing": "延迟：站立",
    "DELAY: Seconds before stamina starts refilling while standing. Game default 1.5.":
        "延迟：站立时耐力开始回充前等待的秒数。原版默认 1.5。",
    "Delay: Crouched": "延迟：蹲下",
    "DELAY: Seconds before stamina starts refilling while crouched. Game default 1.5. Switching stance changes the wait right away.":
        "延迟：蹲下时耐力开始回充前等待的秒数。原版默认 1.5。换姿态会立即改变等待时间。",
    "Delay: Prone": "延迟：趴下",
    "DELAY: Seconds before stamina starts refilling while prone. Game default 1.5. Switching stance changes the wait right away.":
        "延迟：趴下时耐力开始回充前等待的秒数。原版默认 1.5。换姿态会立即改变等待时间。",

    # ── 坡度 ──
    "Slopes": "坡度",
    "SLOPES: Running uphill is slower and drains sprint stamina faster; running downhill is quicker and drains less. Speed uses the game's own slope settings; the stamina effect follows the slope you are actually running on.":
        "坡度：上坡更慢、冲刺耐力消耗更快；下坡更快、消耗更少。速度沿用游戏自身的坡度设置；耐力效果按你实际跑的坡度计算。",
    "Uphill Speed Penalty": "上坡减速",
    "SLOPES (% of normal): How hard slopes slow you going up. The game normally starts slowing you at 10 degrees and nearly stops you at 55. 175 reaches the same slowdown at a much shallower angle. 0 removes uphill slowdown. 100 = normal.":
        "坡度（正常值的百分比）：上坡减速的强度。原版从 10 度开始减速、55 度几乎走不动。设为 175 时很缓的坡就会达到同样减速。0 = 取消上坡减速。100 = 正常。",
    "Downhill Speed Bonus": "下坡加速",
    "SLOPES (EXPERIMENTAL, % bonus): Extra running speed downhill, rising from 5 to 25 degrees of slope. Also replaces the game's slowdown on steep descents. If the game caps speed at normal, this has no effect. 0 = normal game behavior.":
        "坡度（实验性，加速百分比）：下坡时的额外奔跑速度，从 5 度坡开始提升、到 25 度达到最大。同时取代原版在陡下坡的减速。若游戏本身把速度限制在正常值，则本项无效。0 = 原版行为。",
    "Uphill Stamina Drain": "上坡耐力消耗",
    "SLOPES (% of normal at 20 degrees): Sprint stamina drain while running up a 20-degree slope. 200 = twice as fast. Scales with steepness and is capped at 40 degrees. Flat ground is unchanged. 100 = normal.":
        "坡度（20 度坡时的正常值百分比）：上 20 度坡的冲刺耐力消耗。200 = 消耗快一倍。随坡度提高，40 度封顶。平地不受影响。100 = 正常。",
    "Downhill Stamina Drain": "下坡耐力消耗",
    "SLOPES (% of normal at 20 degrees): Sprint stamina drain while running down a 20-degree slope. 50 = half the drain. Scales with steepness and is capped at 40 degrees. 100 = normal.":
        "坡度（20 度坡时的正常值百分比）：下 20 度坡的冲刺耐力消耗。50 = 消耗减半。随坡度提高，40 度封顶。100 = 正常。",

    # ── 近战 ──
    "Melee": "近战",
    "MELEE: Momentum damage and the stamina cost per swing below. Momentum: your default melee hits harder the faster you were moving just before the swing (standard diver melee only, not melee weapons).":
        "近战：下方为冲量伤害与每次挥击的耐力消耗。冲量：挥击前移动越快，默认近战伤害越高（仅限潜兵默认近战，不含近战武器）。",
    "Momentum Damage": "冲量伤害",
    "MELEE (% bonus): Extra damage at full sprint speed. 100 = double damage (75 becomes 150). The bonus rises smoothly from jogging to sprinting and lingers briefly so a sprint-into-swing counts. 0 = normal.":
        "近战（加成百分比）：全速冲刺时的额外伤害。100 = 伤害翻倍（75 变成 150）。加成从小跑平滑增长到冲刺，并会短暂保留，所以「冲刺接挥击」也算数。0 = 正常。",
    "Momentum Stagger and Push": "冲量硬直与推撞",
    "MELEE: ON applies the same momentum bonus to stagger and push force, so a charging hit knocks enemies around harder. Armor penetration never changes.":
        "近战：开启后冲量加成同样作用于硬直与推力，冲锋一击能把敌人打得更飞。穿甲值不受影响。",
    "Momentum Armor Pen": "冲量穿甲",
    "MELEE: ON gives your default melee +1 armor penetration while you are moving at sprint speed or faster (sprinting, sliding, diving), so a charging hit can crack armor it normally bounces off. Standard diver melee only.":
        "近战：处于冲刺速度或更快时（冲刺、滑铲、飞扑），默认近战获得 +1 穿甲，冲锋一击能破开原本会被弹开的装甲。仅限潜兵默认近战。",
    "Momentum on Melee Weapons": "近战武器也享冲量",
    "MELEE: ON applies momentum damage, stagger/push and armor pen to melee weapons (machete, axes, hammers and the rest) as well as the default melee. Their damage values are shared by every diver using them.":
        "近战：开启后，近战武器（砍刀、斧头、锤子等）与默认近战一样享受冲量伤害、硬直/推力与穿甲。这些武器的伤害数值为所有使用者共用。",
    "Melee Stamina Cost": "近战耐力消耗",
    "MELEE (% of a full bar): Stamina each melee swing takes, as a share of a full bar. 10 = ten swings empty a full bar. Starts working once the mod has confirmed your live stamina, which takes a moment of sprinting in each mission. 0 = no cost.":
        "近战（占满条的百分比）：每次挥击消耗的耐力，按整条耐力的比例计。10 = 挥十下耗尽一整条。需先确认实时耐力才会生效（每局先冲刺一下）。0 = 不消耗。",
    "No Melee When Exhausted": "力竭时禁止近战",
    "MELEE: ON prevents default melee and melee-weapon attacks while the confirmed live stamina bar is empty. Melee becomes available again as soon as stamina begins recovering.":
        "近战：开启后，确认实时耐力见底时禁止默认近战与近战武器攻击。耐力一开始回充就恢复可用。",

    # ── 翻越攀爬 ──
    "Mantling": "翻越攀爬",
    "MANTLING: Stamina for vaulting and climbing ledges, and whether you can do it on an empty bar. The game normally charges nothing for either.":
        "翻越攀爬：翻越与攀爬崖边消耗的耐力，以及耐力见底时能否继续。原版这两项都不消耗耐力。",
    "Mantle Stamina Cost": "翻越耐力消耗",
    "MANTLING (% of a full bar): Stamina each successful vault or ledge climb takes. The cost is charged only when the game actually enters its climbing movement state, not when you press the button. 10 = a tenth of a bar. Starts once live stamina is confirmed. 0 = free, as in the base game.":
        "翻越攀爬（占满条的百分比）：每次成功翻越或攀爬崖边消耗的耐力。只有游戏真正进入攀爬移动状态时才扣，不是按下按键就扣。10 = 消耗十分之一条。需先确认实时耐力才会生效。0 = 免费，与原版相同。",
    "No Mantling When Exhausted": "力竭时禁止翻越",
    "MANTLING: ON stops vaults and ledge climbs while your stamina bar is empty; small steps still work. Needs live stamina confirmed (a moment of sprinting each mission).":
        "翻越攀爬：开启后耐力见底时无法翻越与攀爬崖边；矮台阶仍可通过。需先确认实时耐力（每局先冲刺一下）。",

    # ── 边跑边打（战术战斗大修内的一段）──
    "Run and Gun": "边跑边打",
    "RUN AND GUN: Sprint into firing and you keep running: same speed as your sprint, same stamina drain, and on an empty bar the same tired pace. It lasts as long as you keep shooting and moving. The price is heavy aim sway on the move. Firing from a walk or standing works as normal.":
        "边跑边打：冲刺中开火可以继续奔跑——速度与冲刺一致、耐力消耗也一致，耐力见底时同样保持力竭时的慢速。只要持续开火并移动就一直有效。代价是移动中瞄准晃动很大。走路或站立时开火则一切如常。",
    "Hipfire Linger": "腰射残留",
    "RUN AND GUN (% of normal): How long you stay in the shooting stance after your last shot before the game lets you sprint again. 50 = half as long. 100 = normal.":
        "边跑边打（正常值的百分比）：最后一枪之后、游戏允许重新冲刺之前的腰射停留时长。50 = 缩短一半。100 = 正常。",
    "Run and Gun Stamina Drain": "边跑边打耐力消耗",
    "RUN AND GUN (% of sprint drain): Stamina used while firing at a run, compared with sprinting. 100 = the same as sprinting (slopes included). Needs live stamina confirmed (a moment of sprinting each mission). 0 = free.":
        "边跑边打（占冲刺消耗的百分比）：边跑边开火时的耐力消耗，与冲刺相比。100 = 与冲刺相同（含坡度影响）。需先确认实时耐力（每局先冲刺一下）。0 = 不消耗。",
    "Run and Gun Sway": "边跑边打晃动",
    "RUN AND GUN (% extra): Extra aim sway and recoil sway while firing or aiming on the move, full at jogging speed and above. 200 = three times the sway. Stacks with winded sway. 0 = no penalty.":
        "边跑边打（额外百分比）：移动中开火或瞄准时的额外瞄准晃动与后坐晃动，达到小跑速度及以上时取满值。200 = 晃动变为三倍。与气喘晃动叠加。0 = 无额外惩罚。",

    # ── 诊断与预设 ──
    "Diagnostics Probe": "诊断探针",
    "DIAGNOSTICS: For developing melee stamina cost. ON + APPLY in a mission records 90 seconds of your diver's state (reads only, changes nothing), then writes TacticalCombatProbe.log. Records once per switch-on. Follow the steps in README.txt.":
        "诊断：用于开发近战耐力消耗功能。在任务中开启并点「应用」，会记录 90 秒的潜兵状态（仅读取、不做任何修改），然后写入 TacticalCombatProbe.log。每次开启只记录一次。请按 README.txt 的步骤操作。",
    "Preset": "预设",
    "Your own applied settings.": "你自己应用的设置。",
    "PRESETS: Select one, then APPLY to replace every setting below. Editing a setting afterwards switches this to Custom. Vanilla: no changes. Light: a gentle nudge. Tactical: the intended experience. Hardcore: hills hurt, winded aim is rough, crouching is how you recover.":
        "预设：选一个再点「应用」，即可替换下方所有设置；之后手动改任意一项会切回「自定义」。原版 = 不做改动。轻度 = 轻微调整。战术 = 作者推荐的体验。硬核 = 上坡要命、喘气时瞄准难受、靠蹲下来回气。",

    # ═══════════════ 边跑边打 v1.0.4（独立模组）═══════════════
    "Run-N-Gun": "边跑边打",
    "Sprint into firing to keep your running speed while shooting. Turning sideways reduces the benefit when Directional Run-N-Gun is enabled.":
        "冲刺中开火可保持奔跑速度。开启「定向边跑边打」后，侧向移动会降低效果。",
    "Directional Run-N-Gun": "定向边跑边打",
    "Limits the movement-speed benefit to roughly forward movement. Full benefit within 30 degrees, tapering to zero by 55 degrees.":
        "把移动速度加成限制在接近正前方的方向。30 度内为满效果，到 55 度时衰减为零。",
    "One-Handed Direction Bypass": "单手武器忽略方向限制",
    "One-handed weapons ignore the directional angle restriction. All secondaries and recognized one-handed primaries keep full Run-N-Gun speed in any movement direction.":
        "单手武器不受方向角度限制。所有副武器以及可识别为单手持的主武器，在任何移动方向上都能保持完整的边跑边打速度。",
    "Percent of the normal post-shot hipfire linger. Lower values let sprinting resume sooner after the last shot. 100 = vanilla.":
        "正常「开火后腰射停留」时长的百分比。数值越低，最后一枪之后越早能重新冲刺。100 = 原版。",
    "Run-N-Gun Sway": "边跑边打晃动",
    "Extra aim/recoil sway while firing on the move. 200 = roughly triple the affected sway. 0 = no extra sway.":
        "移动中开火时的额外瞄准/后坐晃动。200 = 受影响的晃动约为三倍。0 = 无额外晃动。",

    # ═══════════════ 装甲大修 3.2.0 ═══════════════
    "Puts the Bastion and Maelstrom gunner camera lower and further back so you see more around the tank. It stays behind the turret as it turns. The pick is where the camera starts: the mouse wheel (or the Mod Bindings Menu's Zoom In / Zoom Out keys) moves it closer or further back, and from the closest point zooms in on the crosshair.":
        "把堡垒与漩涡的炮手视角放低、后移，让你能看清坦克周围的更多情况；炮塔转动时视角始终跟在炮塔后方。此项选择的是视角的起始距离：滚轮（或「模组按键菜单」里的放大/缩小键）可以拉近拉远；从最近处再继续就是向准星变焦。",
    "While you drive from the gunner seat with Gunner Drive, a panel like the driver's own HUD shows the gear, rpm, speed, fuel and the Maelstrom's smoke rounds. It only shows while you are the one driving. Only you see it.":
        "当你用「炮手座驾驶」在炮手位开车时，会显示一块与驾驶员 HUD 类似的面板，内容有挡位、转速、速度、燃料以及漩涡的烟雾弹存量。只有你本人在驾驶时才显示，也只有你自己能看到。",
    "More track grip for the Bastion and Maelstrom: less sliding on slopes and in turns. Tanks called in after a change use it.":
        "提升堡垒与漩涡的履带抓地力：在斜坡与转弯时更不容易打滑。改动后新召唤的坦克才会生效。",
    "More pulling power for the Bastion and Maelstrom: quicker off the line and up slopes. Top speed is unchanged. Tanks called in after a change use it.":
        "提升堡垒与漩涡的牵引力：起步与爬坡更快。最高速度不变。改动后新召唤的坦克才会生效。",
    "Quicker steering for the Bastion and Maelstrom: they start and stop turning sooner. Tanks called in after a change use it.":
        "提升堡垒与漩涡的转向响应：开始与停止转向都更干脆。改动后新召唤的坦克才会生效。",
    "Drive from the gunner seat when the driver seat is empty: your movement keys drive, shift and CTRL change gear, Space is the handbrake. F sounds the horn; Mouse 3 pops the Maelstrom's smoke. Controller: the left stick drives, its click is the horn, the right stick click pops smoke. Set your own keys with the Mod Bindings Menu. A teammate who takes the wheel drives. Pick which vehicles.":
        "驾驶位空着时可以从炮手位开车：方向键即驾驶，Shift 与 Ctrl 换挡，空格是手刹；F 按喇叭，鼠标中键放漩涡的烟雾。手柄：左摇杆驾驶、按下是喇叭，右摇杆按下放烟雾。可用「模组按键菜单」自定义按键。队友坐上驾驶位时由他开。可勾选适用于哪些载具。",
    "How fast the Bastion and Maelstrom turrets turn (the game: 25 degrees a second), and the gunner view left/right with them. Very fast is 75. With MBT Turrets all the way round a change applies at once; otherwise tanks called in after a change use it. The view: from the next time you sit in the gunner seat.":
        "堡垒与漩涡炮塔的转速（原版为每秒 25 度），以及炮手视角随之左右转动的速度。最快档为 75。若已启用「360 度主战坦克炮塔」，改动立即生效；否则改动后新召唤的坦克才生效。视角则从你下次坐上炮手位时生效。",
    "How fast the Bastion and Maelstrom guns move up and down (the game: 35 degrees a second), and the gunner view up/down with them. Tanks called in after a change use it.":
        "堡垒与漩涡火炮的俯仰速度（原版为每秒 35 度），以及炮手视角随之上下转动的速度。改动后新召唤的坦克才会生效。",
    "How far down and up the Bastion and Maelstrom guns aim (the game: 3 below to 25 above). Tanks called in after a change use it.":
        "堡垒与漩涡火炮的俯仰范围（原版为下 3 度至上 25 度）。改动后新召唤的坦克才会生效。",
    "A small outline of your vehicle shows where the gun points compared to the hull, colored by health (blue to red). Works in the Bastion, the Maelstrom, the M-102 FRV and the M-103 Supply FRV, in any seat; the FRVs' tires each show their own health and go clear when popped. Only you see it.":
        "用一个小轮廓显示炮口相对于车体的朝向，颜色随血量变化（蓝到红）。适用于堡垒、漩涡、M-102 FRV 与 M-103 补给 FRV，任何座位都能看到；FRV 的每个轮胎各自显示血量，被打爆就变透明。只有你自己能看到。",

    # ═══════════════ 更聪明的护卫犬与哨戒炮 4.6.3 ═══════════════
    "How your dogs and sentries choose what to shoot. Armor Intelligence: they leave alone armor they can't hurt, fire only short bursts at Heavy Devastators, and no sentry wastes ammo on dropships. Target Prioritization: your dog goes for the closest threat to you first; your sentries deal with enemies at their feet, Gunships and the armor that suits the gun first. Turn off to leave both to the game.":
        "决定护卫犬与哨戒炮如何挑选射击目标。装甲智能：打不动的装甲就不打，对重型破坏者只点短射，哨戒炮不会浪费弹药打运输船。目标优先级：护卫犬优先扑向离你最近的威胁；哨戒炮优先处理脚边的敌人、炮艇，以及最适合当前火炮的装甲。关闭后两项都交还给游戏原版处理。",
    "Who your dog and your sentries never fire through: they hold fire while that helldiver is in their line of fire, don't swing their fire across them, mortars and the rocket sentry leave enemies next to them alone, and the Tesla Tower doesn't zap them or arc into them. Turn off at your own risk: they will fire through anyone. Everything else keeps working.":
        "设定护卫犬与哨戒炮绝不误伤的对象：当该潜兵处于射线上时暂停射击、不把火力横扫过去，迫击炮与火箭哨戒炮不打击紧贴他们的敌人，特斯拉塔也不会电到或电弧到他们。关闭风险自负：它们会直接穿过任何人开火。其余功能照常。",
    "Laser out of the barrel of your guard dog and your sentries (not the mortars) toward their targets, shown only on your screen: green while they fire, flashing red when the safety stops a shot, flashing yellow when the dog's target goes out of sight. The Tesla Tower shows its reach as a yellow ring. Line: thin, hidden by walls. Glow: a soft beam that shows through walls.":
        "从护卫犬与哨戒炮（不含迫击炮）的炮口射向目标的激光，只显示在你的屏幕上：开火时为绿色，因安全机制停火时闪红，犬的目标脱离视野时闪黄。特斯拉塔用黄圈表示作用范围。细线：纤细、会被墙挡住。光晕：柔和光束，可以透墙看到。",

    # ═══════════════ 仇恨计数 v1.4 ═══════════════
    "Native: the game font and smooth icons, in line with ":
        "原生：使用游戏字体与平滑图标，风格与 ",
    "Nudge the badge sideways, in 1440p pixels (negative = left). ":
        "把标记左右微调，单位是 1440p 像素（负数 = 向左）。",
    "Nudge the badge up or down, in 1440p pixels (negative = up). ":
        "把标记上下微调，单位是 1440p 像素（负数 = 向上）。",
    "Another HUD mod may ":
        "其它 HUD 模组可能",
    "Detailed log (Logs/AggroCounter.log) for bug reports; F8 then marks the moment. ":
        "在 Logs/AggroCounter.log 输出详细日志以便反馈问题；按 F8 会在日志里标记当前时刻。",

    # ═══════════════ HD2 C4 快捷操作 1.13.1 ═══════════════
    "Throw C4": "投掷 C4",
    "Detonate C4": "引爆 C4",

    # ═══════════════ 超级体能 ═══════════════
    "Require Muscle Enhancement": "需要「肌肉强化」加持",
    "Running with a heavy object only works when someone in the mission brought the Muscle ":
        "只有任务中有人带了「肌肉强化」，负重奔跑才会生效",

    # ═══════════════ C-Rig 骨骼运行时 ═══════════════
    "Enable every physics system for layout ":
        "为以下骨架启用全部物理系统：",
    "auto": "自动",
}
