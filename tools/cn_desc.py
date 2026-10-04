# -*- coding: utf-8 -*-
"""cn_desc.py -- 选项说明 / 模组简介 的中文词表。"""

CN_DESC = {
    # ---------- Aggro Counter ----------
    'Badge size. Fine-tune in game with Ctrl+Shift+= / -.': '徽章尺寸。游戏内可用 Ctrl+Shift+= / - 微调。',
    'Beside the compass, on its right (less room: up to about 150%).': '罗盘右侧（空间较小：最大约 150%）。',
    'Default. Beside the compass, on its left (room up to about 185%).': '默认。罗盘左侧（空间较大：最大约 185%）。',
    'Centred below the compass and the game warning banners.': '居中显示在罗盘与游戏警告横幅下方。',
    'Shrinks to fit beside the compass (about 185% on the left).': '会自动缩小以贴合罗盘（左侧约 185%）。',
    'Just the radar number: every live enemy within 60m of you.': '只显示雷达数字：你周围 60 米内的所有存活敌人。',
    'Default. Nearby, searching, on you and on teammates.': '默认。附近、搜索中、锁定你、锁定队友。',
    'Only appears when an enemy targets or searches for you or a teammate.': '仅当有敌人锁定或搜索你/队友时才出现。',
    'What the badge does while every count is 0.': '所有计数为 0 时徽章的表现。',
    'Where the badge sits. It grows away from the compass when enlarged.':
        '徽章所在位置。放大时会朝背离罗盘的方向扩展。',
    'Which numbers the badge shows. Other combinations: cells in the settings file.':
        '徽章显示哪些数字。其它组合：见设置文件中的 cells。',
    'Beside the compass: enemies near you, searching for you, targeting you, and targeting your teammates. Requires Bingus Shared Loader v18 or newer.':
        '在罗盘旁显示：附近的敌人、正在搜索你的敌人、锁定你的敌人，以及锁定队友的敌人。需要 Bingus Shared Loader v18 或更新版本。',

    # ---------- Smarter Guard Dogs & Sentries ----------
    'The guard dog and sentry improvements (safety, closest threat first, no shooting the dead, no shooting into cover, Guard Dog range, Rover fire spreading; sentries that do not fire through you or swing their fire across you, stop firing into walls, deal with enemies at their feet first, a Laser Sentry that sets enemies alight and moves on like the Rover and cools down before it burns out, and a Tesla Tower that leaves helldivers and enemies next to them alone). Keep this on.':
        '护卫犬与哨戒炮的整体改进（安全保护、优先最近的威胁、不射击尸体、不朝掩体开火、护卫犬射程、漫游者火焰蔓延；哨戒炮不会穿过你开火或把弹道扫过你、不会对着墙射击、优先处理脚下的敌人；激光哨戒炮能点燃敌人并像漫游者那样转移目标、过热前会先冷却；特斯拉塔不再电击绝地潜兵及其旁边的敌人）。请保持开启。',
    'The mod handles your guard dog (Guard Dog, Rover, K-9). Turn off to leave your dog to the game; your sentries and the rest of the mod keep working.':
        '由本模组接管你的护卫犬（护卫犬、漫游者、K-9）。关闭则护卫犬交回游戏处理，哨戒炮与本模组其它功能照常工作。',
    'The mod handles your sentries (Machine Gun, Gatling, Autocannon, Rocket, Laser, Flame, Mortar, EMS Mortar and the Tesla Tower), plus the guns on armed resupply pods and the Supply FRV. Turn off to leave your sentries to the game; your guard dog and the rest of the mod keep working.':
        '由本模组接管你的哨戒炮（机枪、加特林、机炮、火箭、激光、火焰、迫击炮、电磁迫击炮与特斯拉塔），以及武装补给舱和补给 FRV 上的机枪。关闭则哨戒炮交回游戏处理，护卫犬与本模组其它功能照常工作。',
    'Every sentry except the Tesla Tower, which is left to the game.': '除特斯拉塔外的所有哨戒炮（特斯拉塔交回游戏处理）。',
    'How your dogs and sentries choose what to shoot. Armor Intelligence: they leave alone armor they cannot get through (Hulks, Chargers, Tanks and similar; the Rover also Scout Striders; the Laser Sentry only what is above Heavy), fire only short bursts at Heavy Devastators, and no sentry wastes ammo on dropships (only the Rocket and Autocannon sentries shoot enemies still aboard one). Target Prioritization: your dog goes for the closest threat to you first; your sentries deal with enemies at their feet first, go for Gunships and Stingrays first (the Rocket Sentry only while one hovers), then the armor that suits the gun (Heavy for the Rocket and Autocannon, lighter for the Machine Gun, Gatling and Laser; the closest first for the Flame Sentry). Turn off to leave both to the game. Everything else keeps working.':
        '决定护卫犬与哨戒炮如何选择目标。装甲判断：跳过打不穿的装甲（浩克、冲锋虫、坦克等；漫游者还会跳过侦察追猎者；激光哨戒炮只打重型以上），对重型破坏者只点射，且没有哨戒炮会把弹药浪费在运输艇上（只有火箭与机炮哨戒炮会射击仍在艇上的敌人）。目标优先级：护卫犬优先攻击离你最近的威胁；哨戒炮优先处理脚下的敌人，其次优先炮艇与黄貂鱼（火箭哨戒炮只在悬停时），再按武器特性选择装甲（火箭与机炮打重型、机枪/加特林/激光打轻型；火焰哨戒炮优先最近）。关闭则两者都交回游戏，其余功能照常。',
    'Skip armor they cannot hurt and dropships; the game decides the order.': '跳过打不动的装甲和运输艇；攻击顺序由游戏决定。',
    'The right target first; they may shoot armor they cannot hurt.': '优先攻击正确的目标；可能对打不动的装甲开火。',
    'Who your dog and your sentries never fire through: they hold fire while that helldiver is in their line of fire, do not swing their fire across them, mortars and the rocket sentry leave enemies next to them alone, and the Tesla Tower does not zap them or arc into them. Turn off at your own risk: they will fire through anyone. Everything else keeps working.':
        '决定护卫犬与哨戒炮绝不穿过谁开火：当该绝地潜兵处于弹道上时停火、不把弹道扫过他们、迫击炮与火箭哨戒炮不攻击其身边的敌人、特斯拉塔不电击也不对其电弧。关闭需自行承担风险：它们会穿过任何人开火。其余功能照常。',
    'Protects the other players; they may fire through you.': '保护其他玩家；可能穿过你开火。',
    'Protects you; they may fire through other players.': '保护你；可能穿过其他玩家开火。',
    'Laser out of the barrel of your guard dog and your sentries (not the mortars) toward their targets, shown only on your screen: green while they fire, flashing red when the safety stops a shot (and a red ring around the rocket sentry while an enemy is too close for it to fire), flashing yellow when the dog target goes out of sight (cover or smoke), off while the dog reloads. The Tesla Tower shows its reach as a yellow ring instead. Turn off to hide it.':
        '从护卫犬与哨戒炮（迫击炮除外）枪口射向目标的激光，只在你屏幕上显示：开火时为绿色，安全保护拦下射击时闪红（敌人离火箭哨戒炮太近时它会显示红圈），护卫犬目标被掩体或烟雾遮挡时闪黄，装填时熄灭。特斯拉塔改以黄色圆环显示作用范围。关闭即隐藏。',
    'A thin, plain line with a small cross where it hits. Simple to look at, but walls and objects hide it.':
        '细直线，命中处有小十字。观感简洁，但会被墙壁和物体遮挡。',
    'A soft glowing beam with a bright spot on the target. It looks much better than the line, but it shows through walls and objects (the game draws it on top of the world).':
        '柔和光晕光束，命中点亮起光斑。比细线好看得多，但会穿透墙壁与物体（游戏把它绘制在世界之上）。',
    'How bright the targeting laser is: its beams and rings, line or glow.':
        '瞄准激光的亮度：包括光束与圆环、线状或光晕。',
    'The laser as it has always been.': '与原版一致的激光。',
    'The laser at 50% of its normal brightness.': '亮度为正常值 50% 的激光。',
    'The laser at 75% of its normal brightness.': '亮度为正常值 75% 的激光。',
    'The laser at 150% of its normal brightness.': '亮度为正常值 150% 的激光。',
    'The laser at 200% of its normal brightness.': '亮度为正常值 200% 的激光。',

    # ---------- Helmet Headlamp ----------
    'Short-range helmet task light, about 20-25 m.': '近距离头盔作业灯，约 20-25 米。',
    'Gameplay-first flood, about 35-40 m.': '偏游戏性的泛光照明，约 35-40 米。',
    'Initial mode; the mode key still switches it.': '初始模式；模式键仍可切换。',

    # ---------- Better Map Markers ----------
    'Customise the appearance of the map marker.': '自定义地图标记的外观。',
    'Customise the appearance of the enemy blips (the solid red circles on the map which show enemy unit positions).':
        '自定义敌人光点的外观（地图上表示敌军位置的红色实心圆）。',
    'Customise the appearance of Helldiver view cones on the minimap.': '自定义小地图上绝地潜兵视野扇形的外观。',
    'Customise the appearance of the Super Destroyer compass indicator.\n(NOTE: This is only enabled in megacity missions.)':
        '自定义超级驱逐舰罗盘指示器的外观。\n（注意：仅在巨型城市任务中启用。）',

    # ---------- HD2 Transmog ----------
    'Body-armor creation process. Helmet/cape and icon settings are independent.':
        '护甲创建流程。头盔/披风与图标设置相互独立。',
    'Choose look, base stats, then passive.': '依次选择外观、基础属性，再选被动。',
    'Choose look and passive; the look supplies base stats.': '选择外观与被动；基础属性由外观决定。',
    'Shared variant creator for detected helmet/cape passives. On by default.':
        '为识别到的头盔/披风被动提供共享的变体创建器。默认开启。',
    'Use the same + creator for helmets and capes with detected gameplay changes.':
        '对检测到玩法变化的头盔与披风，使用同一个「+」创建器。',
    'Disable helmet and cape variants.': '禁用头盔与披风变体。',
    'Show or hide passive badges on armor thumbnails. On by default.': '在护甲缩略图上显示或隐藏被动徽章。默认开启。',
    'Show passive badges on armor thumbnails.': '在护甲缩略图上显示被动徽章。',
    'Hide thumbnail badges; passive-selection and detail-panel icons stay visible.':
        '隐藏缩略图上的徽章；被动选择界面与详情面板的图标仍然显示。',

    # ---------- Armored Overhaul ----------
    'More pulling power for the Bastion and Maelstrom: quicker off the line and up slopes. Top speed is unchanged.':
        '提升堡垒与漩涡的牵引力：起步与爬坡更快。最高速度不变。',
    'More track grip for the Bastion and Maelstrom: less sliding on slopes and in turns.':
        '提升堡垒与漩涡的履带抓地力：在斜坡与转弯时更少打滑。',
    'Quicker steering for the Bastion and Maelstrom: they start and stop turning sooner.':
        '提升堡垒与漩涡的转向响应：起转与停转都更快。',
    'Road wheels that work like a tank: the game tanks rest on their bump stops, so the wheels cannot move. Here each wheel rests part-way down a longer travel and follows the ground, keeping its track down, well damped; the hull is no longer thrown sideways when one track unloads. The tanks ride a little higher than in the game.':
        '像真实坦克那样工作的负重轮：原版坦克压在缓冲块上，轮子无法活动。本模组让每个轮子在更长的行程中半悬并贴合地面，履带始终压地、阻尼充分；单侧履带卸载时车体不再被甩向一侧。车体会比原版略高一点。',
    'Half a metre of wheel travel, each wheel resting half-way: soaks up rough ground; the hull resists being rolled and the grip is shared between the tracks.':
        '轮行程半米、每个轮子停在中间位置：能吸收崎岖地面；车体不易被翻覆，抓地力由两侧履带共同承担。',
    'Stiffer, more damped wheels with a little less travel; the hull is very hard to roll and the tracks share almost all the grip.':
        '轮子更硬、阻尼更强、行程略短；车体极难翻覆，几乎全部抓地力由履带承担。',
    'The Bastion and Maelstrom turrets turn all the way round like a main battle tank. The Maelstrom missile pods and smoke launchers turn with it. Only you see the new turrets, and their armor always looks undamaged.':
        '堡垒与漩涡的炮塔可像主战坦克那样 360 度旋转。漩涡的导弹发射巢与烟雾发射器随之转动。新炮塔只有你自己能看到，且其装甲始终显示为完好。',
    'How fast the Bastion and Maelstrom turrets turn (the game: 25 degrees a second). Works with or without MBT Turrets.':
        '堡垒与漩涡炮塔的转速（原版：每秒 25 度）。无论是否开启「炮塔全向旋转」都有效。',
    'How fast the Bastion and Maelstrom guns move up and down (the game: 35 degrees a second).':
        '堡垒与漩涡火炮的俯仰速度（原版：每秒 35 度）。',
    'How far down and up the Bastion and Maelstrom guns aim (the game: 3 below to 25 above).':
        '堡垒与漩涡火炮的俯仰范围（原版：下 3 度至上 25 度）。',
    'The Bastion and Maelstrom main gun reloads by itself when it runs dry, at the normal reload speed (perks count). You can still reload by hand.':
        '堡垒与漩涡的主炮打空后会自动装填，速度为正常装填速度（受相关加成影响）。仍可手动装填。',
    'Drive from the gunner seat when the driver seat is empty: your movement keys drive, the gun works as normal, and a driver panel shows gear, rpm, speed and fuel. F sounds the horn; in the Maelstrom, Mouse 3 pops smoke. On a controller the left stick drives, its click sounds the horn and the right stick click pops smoke. A teammate who takes the wheel drives as normal, and getting out while it rolls brakes it to a stop. With the Mod Bindings Menu you can set your own keys (controls, tab MODS). Pick which vehicles.':
        '驾驶位空置时可在炮手座驾驶：移动键控制行驶，武器照常工作，并显示档位、转速、速度与燃料面板。按 F 鸣笛；漩涡上鼠标中键释放烟雾。手柄用左摇杆驾驶、按下鸣笛、右摇杆按下放烟雾。队友接方向盘后按正常方式驾驶；行驶中下车会自动刹停。配合「模组按键菜单」可自定义按键（控制设置里的 MODS 分页）。可选择适用于哪些载具。',
    'Tanks and FRV': '坦克与 FRV',
    'Puts the Bastion and Maelstrom gunner camera lower and further back so you see more around the tank. It stays behind the turret as it turns.':
        '把堡垒与漩涡的炮手视角放得更低更靠后，便于观察坦克周围。视角会始终跟随炮塔后方。',
    'The game distance, 1.4 m up (the game: 2 m).': '与原版一致的距离，高度 1.4 米（原版为 2 米）。',
    'Far (3.5 m behind)': '远（后方 3.5 米）',
    'Keeps the M-102, M-103 and M-104 FRVs on their wheels over rough ground, jumps and hard turns: a firmer front, longer suspension travel, a lower center of mass, more grip and weight, and a little more ground clearance. Engine and steering stay the game own.':
        '让 M-102、M-103、M-104 FRV 在崎岖地面、跳跃与急转弯时保持四轮着地：前悬更硬、悬挂行程更长、重心更低、抓地与重量更高，离地间隙略增。引擎与转向保持原版。',
    'Half the change: still lively, far less likely to roll.': '改动一半：依然灵活，但翻车概率大幅降低。',
    'Stays upright over rough ground, jumps and hard turns; a quarter heavier.':
        '在崎岖地面、跳跃与急转弯时保持直立；重量增加四分之一。',
    'Lower, grippier, stiffer and 40% heavier, and the chassis resists rolling: very hard to tip, slower to turn.':
        '更低、更抓地、更硬且重量 +40%，车架抗翻覆：极难翻车，但转向变慢。',
    'A small outline of your vehicle shows where the gun points compared to the hull, colored by health (blue to red). Works in the Bastion, the Maelstrom, the M-102 FRV and the M-103 Supply FRV, in any seat; the FRVs tires each show their own health and go clear when popped. Only you see it.':
        '屏幕上的载具小轮廓显示炮口相对车体的朝向，颜色随耐久变化（蓝到红）。堡垒、漩涡、M-102 FRV、M-103 补给 FRV 的任意座位均可用；FRV 的每个轮胎单独显示耐久，爆胎后变透明。只有你自己能看到。',

    # ---------- HD2 HUD+ ----------
    'Required for the HUD to work. Keep this enabled and use the options below to choose what is displayed.':
        'HUD 运行所必需。请保持启用，并在下面选择要显示的内容。',
    'Enabled by default. Choose one: Integrated / Rings / Simple.': '默认开启。三选一：一体化 / 圆环 / 简洁。',
    'Under the crosshair: a charge, reload, heat or rounds arc, ammo, reserve ammo, health/stamina bars, stims, throwables, backpack. Best with game HUD on Map only.':
        '准星下方：充能/装填/热量/弹数弧线、弹药、备弹、生命与耐力条、兴奋剂、投掷物、背包。建议把游戏 HUD 设为「仅地图」。',
    'A ring by the crosshair shows charge, reload, heat or rounds; another shows a backpack own resource. Plus ammo, reserve ammo and weapon setting icons.':
        '准星旁的一个圆环显示充能、装填、热量或弹数；另一个圆环显示背包资源。另含弹药、备弹与武器状态图标。',
    'Weapon setting icons only - fire mode, function, scope zoom - beside the game weapon panel. Fixed brightness, and they hide when that panel hides.':
        '只显示武器状态图标（射击模式、功能、倍镜）在游戏武器面板旁。亮度固定，随该面板一同隐藏。',
    'Enabled by default. Choose one: Faint / Full brightness.': '默认开启。二选一：微弱 / 全亮。',
    'Dims the crosshair HUD to 30% brightness when idle. Does not affect Simple or squad icons.':
        '待机时把准星 HUD 亮度降到 30%。不影响「简洁」模式与小队图标。',
    'Keeps the crosshair HUD at full brightness when idle. Does not affect Simple or squad icons.':
        '待机时保持准星 HUD 全亮。不影响「简洁」模式与小队图标。',
    'Each squad row shows that player booster, yours last - a skull while that player is dead, or what they just pinged. Stratagems they call stack along the row. All hide with it.':
        '小队每行显示该玩家的增益（你自己在最后）——该玩家阵亡时显示骷髅，或显示他刚标记的内容。他们呼叫的战略配备会沿该行堆叠。整块显示可一并隐藏。',
    'The stratagems you chose, on a row at the bottom center: each drains on the way in, fills back as it cools, shows uses left while ready, carries a soft tint of its in-game colour while ready that turns full and enlarges while its beacon is out, and goes grey when the game blocks it.':
        '你选择的战略配备，排列在屏幕底部中央：呼叫时逐渐消耗、冷却时回填、就绪时显示剩余次数；就绪时带有其游戏内颜色的淡色标记，信标投放期间变为实色并放大；被游戏禁用时变灰。',
    'Lets the game draw its own crosshair for the Anti-Materiel Rifle in third person and the Maxigun in first person. It follows the game crosshair setting.':
        '让游戏为第三人称的反器材步枪与第一人称的转轮机枪绘制自带准星。跟随游戏的准星设置。',

    # ---------- Muzzle Flash / Sentries ----------
    'No Muzzle Flash Smoke': '枪口无烟',
    'Removes the smoke from firing a weapon while keeping the muzzle flash.':
        '移除开火时的硝烟，同时保留枪口火光。',
    'Enhances the sounds of the Sentries': '强化哨戒炮的音效',
    'Changes firing, shell eject, and shell impact sounds.': '替换开火、抛壳与炮弹命中音效。',
    'Changes charge-up, firing, and overheat alarm sounds.': '替换充能、开火与过热警报音效。',
    'Changes charge-up, firing, cooldown, and ready-state sounds.': '替换充能、开火、冷却与就绪状态音效。',
    'Changes firing, reload (with ping), and gun open/close sounds.': '替换开火、装填（含提示音）与炮闩开合音效。',
    'A subtle, low-volume ping heard while shooting.': '射击时能听到的轻微、低音量提示音。',
    'A distinct, much louder ping heard while shooting.': '射击时能听到的明显、音量更大的提示音。',
    'Changes firing, reload, and charge-up sounds, including safety mode alerts.':
        '替换开火、装填与充能音效，并包含安全模式提示音。',
    'Includes an alarm to warn you when you are about to explode.': '包含即将过载爆炸时的警报音。',
    'Includes a sound cue for reaching maximum safe charge.': '包含达到最大安全充能时的提示音。',
    'Combines Unsafe and Safe sounds. Note: Slightly less immersive due to overlapping cues.':
        '同时包含「不安全」与「安全」音效。注意：提示音重叠，代入感略降。',
    'Changes firing, charge-up, and reload sounds; adds a warning as you near max charge.':
        '替换开火、充能与装填音效；接近最大充能时增加警告音。',
    'Changes firing, idle, and repel sounds.': '替换开火、待机与驱离音效。',
    'Changes firing, lock-on, and target-locked sounds.': '替换开火、锁定与锁定完成音效。',
    'Changes enter/exit, movement, engine, and stomp sounds for Patriot and Emancipator.':
        '替换爱国者与解放者的进出舱、移动、引擎与踏步音效。',
    'The default menacing horn sound for the Exosuit.': '外骨骼默认的威压号角声。',
    'The iconic mechanical roar of the MvM Tank from Team Fortress 2.': '《军团要塞 2》中 MvM 坦克标志性的机械咆哮。',
    'The iconic Warlord Titan Warhorn from the 40K universe.': '40K 世界观中战将泰坦标志性的战争号角。',
    'Doctor! Are you sure this will work? Ha ha ha, I have no idea!': '医生！你确定这能行？哈哈哈，我完全不知道！',
    'Changes firing, wind-up/down and spin-loop audio.': '替换开火、加速/减速与旋转循环音效。',
    'Changes the firing sound (more updates planned).': '替换开火音效（后续还会继续更新）。',
    'This is the default mod, no added music.': '这是默认版本，没有附加音乐。',

    # ---------- Bingus / GL-52 ----------
    'ARSENAL: place this loader LAST (bottom of the list) with default priority, or FIRST if first-mod priority is enabled. Required by Armory Preview Cache, Know Your Constellation, Controllable Hover Pack, Vehicle Stability, Enemy Collision Synchronized, Vanilla Plus Megapack or the separate Better Stratagem Bounce, Hellpod Steering Unlocked, Reinforcement Beacons Fixed, Consistent Vaulting, Shallow Water Diving and Sentry Aim Retention mods. Import this ZIP through Arsenal or HD2MM, enable it alongside the megapack or your chosen mods, then Deploy. Also supports HUD Ballistic Trajectory Overlay v2.':
        'Arsenal 用法：把本加载器放在列表最后（默认优先级），或在使用「首个模组优先」时放在最前。以下模组需要它：军械库预览缓存、敌情预测、悬浮背包可控下降、载具稳定性、敌人碰撞同步修正、Vanilla Plus 合集，或单独的「战备球弹射优化」「地狱舱转向解锁」「增援信标修正」「翻越判定稳定化」「浅水区飞扑」「哨戒炮瞄准保持」。请用 Arsenal 或 HD2MM 导入本 ZIP，与合集或你选的模组一起启用，然后 Deploy。同时支持「HUD 弹道轨迹叠加 v2」。',
    'Builds 25327279, 25480438 only. GL-52 owner exclusion; damage and range unchanged. Unknown game modules stop safely. Requires Bingus Shared Loader v15+ / API 1 and discovery.':
        '仅支持 25327279、25480438 版本。GL-52 排除发射者自身；伤害与射程不变。遇到未知游戏模块会安全停止。需要 Bingus Shared Loader v15+ / API 1 与 discovery。',
}
