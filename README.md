# GNH · Helldivers 2 界面汉化包

> **📦 下载**：[最新版本（Release）](https://github.com/1579486875/GNH-Helldivers2-CN/releases/latest) —— 主包（零冲突）与 Transmog 可选包都在 Release 页，在 HD2 Arsenal 里导入即可。

> 把未自带中文的 HD2 模组界面（游戏内 MODS 选项菜单、Transmog 装甲变体界面）改成简体中文。
> 采用**运行时接管**方案：只提供全新资源路径，**不覆盖、不修改任何上游模组文件**，因此主包**零冲突**。

**作者**：大赢经直插白皮赢道（GNH-CN-CYS）　·　**许可**：MIT（见 [LICENSE](LICENSE)）

---

## 仓库内容

| 路径 | 说明 |
| --- | --- |
| [`dist/GNH简体中文汉化包-Helldivers2.zip`](dist) | **主包**：零冲突，直接分发/自用 |
| [`dist/GNH-Transmog界面汉化-可选包.zip`](dist) | 可选包：汉化 Transmog 界面，与 HD2 Transmog 有 1 处预期覆盖 |
| [`tools/`](tools) | 构建与校验脚本（Python），见 [tools/README.md](tools/README.md) |
| 本文件 | 完整说明、技术原理、历次极端场景验证记录 |

**安装**：在 HD2 Arsenal 里「导入」对应 zip → 启用 → Deploy。建议放在模组列表靠后位置。

> 下文出现的 `tools\...` 是开发时的原始路径；在本仓库中对应 `tools/` 目录。
> 脚本已改为相对路径，并支持用环境变量 `HD2_DATA` 指定游戏 data 目录。

---

## 汉化说明

> 制作：大赢经直插白皮赢道（GNH-CN-CYS）　日期：2026-10-03
> 目标：把未自带中文的 HD2 模组界面（游戏内 MODS 选项目录、Transmog 装甲变体界面）改成简体中文。

### 一、这次汉化了什么

| 目标 | 位置 | 汉化内容 |
| --- | --- | --- |
| **MODS 选项目录**（ESC → 模组） | 运行时接管 `ModOptionsMenu`（主包资源 `mods/gnh_cn/zh_hans`） | **541 组词表（含大写形式共 1026 条）**：选项名、选项值、选项说明、模组名 —— 覆盖 Aggro Counter 仇恨计数、Armored Overhaul 装甲大修、Smarter Guard Dogs & Sentries 更聪明的护卫犬与哨戒炮、Objective Tracker 任务目标追踪、HD2 Transmog 幻化、Better Lobby Management 大厅管理等 |
| **装甲变体界面**（军械库 → 防具 → 自订变体） | `HD2 Transmog (Foundation)` 的 patch | 35 处界面文本：`CREATE VARIANT`、`Choose a look / base stats / passive`、`Back / Cancel / Create`、`LOOK / PASSIVE / BASE STATS`、`ARMOR RATING / SPEED / STAMINA REGEN`、`Not selected`、底部说明等 |

**已汉化**（原本就是中文，未改动）：更好的大厅管理、浅水区飞扑、Mod 键位菜单、敌方模板预测、舰内站点快捷键 —— 这些模组自带 Bingus Text 翻译键，由整合包里的 `ChineseTranslation` 补丁翻译。

**本次未包含**（可作为下一版）：HD2 Arsenal 管理器列表里的模组名称与描述（`manifest.json`）、`Mod Bindings Menu` 按键绑定名（`MOVE BADGE UP` 等 7 条）。

### 二、已改动的文件

改动前**全部已备份**，见 `tools\backup\`（保留原目录结构）。

| 文件 | 说明 |
| --- | --- |
| `%LOCALAPPDATA%\hd2arsenal\mods\Vanilla Plus Megapack …\options\ModOptionsMenu\9ba626afa44a3aa3.patch_0` | 94208 → 107880 字节，在 `mod_options_menu` 的 Lua 末尾追加中文词表 |
| `C:\SteamLibrary\steamapps\common\Helldivers 2\data\9ba626afa44a3aa3.patch_14` | 上者的游戏部署副本，已同步（同一内容） |
| `%LOCALAPPDATA%\hd2arsenal\mods\HD2 Transmog (Foundation) …\Addon\9ba626afa44a3aa3.patch_0` | 2082560 → 2082568 字节，界面字面量替换为中文 |
| `C:\SteamLibrary\steamapps\common\Helldivers 2\data\9ba626afa44a3aa3.patch_20` | 上者的游戏部署副本，已同步 |

### 三、怎么生效

1. **完全退出游戏**（以及 HD2 Arsenal，如果它开着）。
2. 直接用 Steam 启动游戏即可 —— `data` 目录里的部署副本已经是汉化版；
   也可以先开 HD2 Arsenal，**若它提示重新部署（Deploy），点同意**（此时它会把 mod 库里已汉化的文件重新复制过去，结果一致）。
3. 进游戏后：
   - `ESC → 模组`：AGGRO COUNTER / ARMORED OVERHAUL / SMARTER GUARD DOGS & SENTRIES 三个面板应为中文。
   - 军械库 → 防具 → 自建变体：标题、按钮、字段名应为中文。

### 四、怎么还原成英文

```powershell
python tools\restore_hd2_cn.py
```

脚本会把备份还原到 mod 库并同步回游戏 `data` 目录；之后在 HD2 Arsenal 里再点一次 Deploy 也可以。

### 五、技术要点（便于以后维护）

- HD2 的模组 patch 文件（`9ba626afa44a3aa3.patch_N`）是 Stingray bundle patch：头部 + 若干 entry；每个 entry 有 `(u32 长度, u32 类型)` 记录，`type = 2` 就是**明文 Lua**。
- 每个 entry 的资源 ID = `murmur_hash_64A("mods/…路径")`，与内容无关 —— 所以**替换 Lua 内容不影响资源定位**，只要更新「文件总大小 / entry 长度 / 长度+8」三个字段即可。
- 工具与脚本（可重复使用）：
  - `tools\hd2_patch.py` —— patch 读写、校验（自检覆盖全部 108 个 Lua entry，资源 ID 全部匹配）
  - `tools\cn_strings.py` —— 541 组英文→中文词表（合并自 `cn_add.py` / `cn_desc.py` / `cn_fix.py` /
    `cn_mods.py` / `cn_mods2.py` / `cn_new.py` / `cn_ui3.py`）；运行时还会自动补一份全大写键，共 1026 条
  - `tools\apply_cn_menu.py` / `apply_cn_transmog.py` —— 一键重新应用汉化（**幂等保护**，已应用过会拒绝重复执行）
- 每一步都用 `luaparser` 做了 **Lua 语法校验**（改前、改后各一次），并用 `hd2_patch.PatchFile` 复核了 patch 结构。

### 六、注意

- **模组更新会覆盖汉化**：以后在 HD2 Arsenal 里更新 Vanilla Plus Megapack 或 HD2 Transmog，汉化会丢失；重跑上面两个 `apply_cn_*.py` 即可（若模组文本有改动，脚本会提示哪条没匹配到）。
- 汉化只改**显示文本**，不触碰任何数值、逻辑判断（Transmog 里用于识别游戏原生分类的 `'CUSTOM VARIANTS'` 等比较字符串刻意保留原样）。


---

## 附录一：兼容性复盘与极端场景验证（2026-10-03 第二轮）

> 本轮按「大胆假设、小心验证」重做了汉化的兼容性审查，**抓到并修复了两个会让游戏内 MODS 面板直接失效的致命缺陷**。
> 验证手段：安装 lupa（内置 Lua 运行时）与 luaparser，对汉化后的 Lua 做**真实编译与执行**，而不是只做静态检查。

### 一、抓到并修复的两个致命问题

### 问题 1：主 chunk 的 local 数量超限（编译期失败）
- **假设**：ModOptionsMenu 的源码自己注释过「本 chunk 的 local 数接近 200 上限」，而我在文件末尾追加了代码。
- **实测**：load() 报错 —— too many local variables (limit is 200) in main function near 'for'。
- **后果**：整块 Lua **无法编译**，MODS 面板会完全失效（不是「汉化不生效」而是「功能消失」）。
- **修复**：把整段汉化代码包进**立即执行函数**，顶层不再新增任何 local（闭包只捕获 translation / note 两个 upvalue）。
- **复验**：原始版与汉化版现在都能编译通过。

### 问题 2：Lua「换行不结束语句」陷阱（运行期必崩）
- **假设**：注入代码紧跟在原文件最后一行的 note('Mod Options Menu initialized.') 之后。
- **实测**：Lua 会把换行后的 (function() ... end)() 解析成**上一条语句的调用后缀**，即 note('...')(function() ... end)()；而 note() 返回 nil，于是运行时抛 attempt to call a nil value。
- **后果**：MODS 面板一打开就报 Lua 错误。
- **修复**：在 (function() 前加一个**前置分号**，让 Lua 认为上一条语句已结束（代码里已写明原因注释）。
- **复验**：构造与真实文件完全相同的上下文（note(...) 后紧跟注入代码）执行，运行正常。

### 二、另外三项加固

| 加固 | 说明 |
| --- | --- |
| 语言保护 | 只在游戏语言为中文时替换，**英文环境下界面保持英文**；语言读不到或读取异常时兜底按中文处理 |
| 上游结构保护 | translation / translation.resolve / note / translation.T 任一缺失都**安静退出**，不会因为上游更新而报错 |
| 全局幂等标记 | _G.GNH_CN_TEXT_PACK，即使 chunk 被重复加载也不会二次包装 |

### 三、极端场景单元测试结果（真实 Lua 执行）

| 场景 | 预期 | 实测 |
| --- | --- | --- |
| 1 游戏语言 zh-Hans | 显示中文 | OK：Show Badge 到 显示徽章 |
| 2 游戏语言 en | 保持英文 | OK：原文返回 |
| 3 游戏语言 zh-Hant | 按中文处理 | OK：显示中文 |
| 4 language() 抛异常 | 兜底翻译 | OK：显示中文，无报错 |
| 5 T.language 缺失 | 兜底翻译 | OK：显示中文 |
| 6 T 整体缺失 | 兜底翻译 | OK：显示中文 |
| 7 translation.resolve 缺失 | 安静退出 | OK：不修改任何东西 |
| 8 translation 整体缺失 | 安静退出 | OK：不报错 |
| 9 note 缺失 | 不报错 | OK：正常翻译 |
| 10 注入代码被执行两次 | 幂等 | OK：仅生效一次 |
| 11 真实上下文（note(...) 之后） | 正常运行 | OK：日志与翻译都正确 |

### 四、横向验证

| 项目 | 结果 |
| --- | --- |
| patch 容器结构 | ModOptionsMenu（2 entry）、Transmog（1 entry）全部解析通过，**资源 ID 与路径哈希 101/101 全匹配** |
| UTF-8 合法性 | 两个 patch 的文本载荷均为合法 UTF-8，正文无 NUL |
| 词表跨模组冲突 | **0 条** 词表被两个以上模组当作界面文本使用，无误译面 |
| Transmog 逻辑安全 | 汉化后 Lua 中，**比较表达式里出现中文的数量 = 0**（用于识别游戏原生分类的 CUSTOM VARIANTS 等刻意保留英文） |
| 文本宽度 | 110 条里仅 3 条比英文略宽（最多 +2 列），最长条目 241 列（上限 400 字符），无溢出风险 |
| M.upper() 兼容性 | 该函数只处理 ASCII / Latin-1 / 希腊 / 西里尔，**CJK 原样保留**（源码注释亦如此声明），中文不会被破坏 |
| 数据一致性 | 模组库与游戏 data 目录的部署副本 SHA-256 完全一致（patch_14 / patch_20） |

### 五、仍然存在的已知限制（诚实告知）

1. **Transmog 的汉化是字面量替换，不随语言切换**：如果把游戏语言改成英文，Transmog 的按钮与标签仍会是中文（ModOptionsMenu 的汉化则有语言保护，会自动回到英文）。
2. **模组更新会覆盖汉化**：Arsenal 更新 Vanilla Plus Megapack 或 HD2 Transmog 后，重跑 `build_cn.py` 即可（脚本自带幂等保护与语法校验，失败会直接报错而不会写入坏文件）。
3. **上游大改版时**：若 ModOptionsMenu 内部结构变化（例如 translation.resolve 消失），汉化会**安静地不生效**（不会报错、不会影响原功能），此时重跑脚本会提示未匹配项。
4. **尚未汉化**：Arsenal 管理器里的模组名称与描述（manifest.json）、Mod Bindings Menu 的按键绑定名。

---

## 附录二：第三轮修复 —— MODS 面板仍显示英文的真正原因（2026-10-03）

### 现象与排查

用户反馈「模组设置界面还是没有翻译」。我读取游戏自身日志与文件系统后确认：

| 检查 | 结果 |
| --- | --- |
| 游戏进程创建时间（取自 ArmoryPreviewCache.log 的 `process_created_filetime_hex`） | **09:59:40** |
| 我的修复写入游戏 data 的时刻 | **09:57:14** |
| 结论 | 游戏进程**确实晚于修复启动**，加载的是修复版 —— 问题不在「没重启」 |
| `ModOptionsMenu.log` 行序 | 第 2 行「GNH-CN 已载入」→ 第 4~40 行「Registered option …」→ 第 41 行「Text language: zh-Hans」 |

### 真正的根因

`Bingus Text` 的 `M.observe()` 会**每次调用都覆盖** `registry.game_language`：

- **启动早期**：各模组注册选项时，游戏的语言设置对象尚未就绪，观测到的是**默认语言（英文）**；
- **打开菜单时**：观测才拿到真正的 `zh-Hans`（日志第 41 行）；
- 而字符串型界面文本**在注册那一刻就被解析并缓存**，之后不会再重新解析。

于是我的「语言保护」在注册阶段读到 `en`，判定为非中文 → 整批选项不翻译。这个判断逻辑本身没错，但**评估时机不可靠**。

### 修复（双保险）

1. **去掉语言判断**：本包定位就是简体中文汉化包，命中词表即替换，不再猜测语言。
2. **第一道保险 —— 包装文本解析入口** `translation.resolve`。
3. **第二道保险 —— 包装公开 API** `ModOptionsMenu.register_option`：在调用真实注册函数前，就地替换 `spec.label / description / mod / choices`。这样即使某个版本不再经过 `translation.resolve`，界面依然是中文。
4. **加入诊断日志**：每次启动会写入
   - `GNH-CN: 已接管文本解析入口 translation.resolve`
   - `GNH-CN: 已接管 ModOptionsMenu.register_option`
   - `<文本> -> <中文>`（前 8 条命中）

   以后若再出现「没汉化」，看一眼 `%LOCALAPPDATA%\CowboyBingus\Helldivers2\Logs\ModOptionsMenu.log` 就能定位。

### 验证方式（离线端到端模拟）

用 lupa 加载**真实 patch 文件里的完整 Lua**，并模拟两个真实模组的注册调用：

| 模拟项 | 修复前 | 修复后 |
| --- | --- | --- |
| `Show Badge` | 英文 | **显示徽章** |
| 该选项的描述 | 英文 | **在罗盘旁显示徽章。同 Ctrl+Shift+O。** |
| `mod = 'Aggro Counter'` | 英文 | **仇恨计数** |
| `Tank Power` | 英文 | **坦克动力** |
| 选项值 `Strong (x1.25)` | 英文 | **强劲 (x1.25)** |
| 选项值 `Off` | — | 保持 `Off`（交给游戏原生「关」） |

> 注：必须**完全退出游戏再启动**才会生效——选项文本是游戏启动时注册并缓存的。

---

## 附录三：第四轮 —— 极端场景验证与加固（2026-10-03）

### 一、先说结论：汉化已经生效

`ModOptionsMenu.log` 里可以直接看到（这是游戏自己写的日志）：

```
2: GNH-CN: 已接管文本解析入口 translation.resolve
3: GNH-CN: 已接管 ModOptionsMenu.register_option
4: GNH-CN: 简体中文界面文本包已载入 (110 条)
9: Registered option smarter_guard_dogs.dogs.on ... under 更聪明的护卫犬与哨戒炮.
14: Registered option armored_overhaul.power.strong ... under 装甲大修.
24: GNH-CN 汉化命中: FRV -> FRV
```

模组名与选项文本都已按词表替换为中文（`BETTER LOBBY MANAGEMENT`、`SHALLOW WATER DIVING` 仍显英文是**正确的**——它们自带 Bingus 翻译键，由整合包的中文包负责）。

### 二、本轮主动发现并加固的一个真实缺陷

**风险场景**：若某个模组传入的 `spec` 表带只读元表（`__newindex` 保护），上一版直接 `spec.label = ...` 赋值会**抛错**，从而破坏该模组的选项注册。

**加固措施**：包装函数改为**浅拷贝一个副本**再翻译，**绝不改动调用方传入的表**，并用 `pcall` 兜底：

```lua
host.register_option = function(id, spec)
    local ok, translated = pcall(translate_spec, spec)   -- translate_spec 内部是 pairs 浅拷贝
    if not ok or type(translated) ~= 'table' then translated = spec end
    return real_register(id, translated)
end
```

### 三、极端场景测试（12 项，全部真实 Lua 执行）

| # | 极端场景 | 结果 |
| --- | --- | --- |
| 1 | **spec 带只读元表**（`__newindex` 抛错） | 调用成功、翻译生效（显示徽章）、原表未被触碰 ✅（**加固前会抛错**） |
| 2 | **多个选项共用同一个 spec 表** | 两次都翻译，原表**未被污染** ✅ |
| 3 | label 是**函数**（API v2） | 不报错，函数原样传递给菜单（由文本入口翻译）✅ |
| 4 | choices 带元表 | 正确翻译 `强劲 (x1.25)`，长度正确 ✅ |
| 5 | `_G.ModOptionsMenu` 缺失 | 不报错，仅打印提示，只用文本入口 ✅ |
| 6 | 真实注册函数自身抛错 | 错误**原样传播**，不被吞掉 ✅ |
| 7 | spec 是 nil / 字符串 | 安全透传 ✅ |
| 8 | 非法 spec（缺 label） | 原样交给菜单自己报错 ✅ |
| 9 | 注入代码被执行两次 | 幂等，仅生效一次 ✅ |
| 10 | **与其他模组的包装叠加** | 翻译生效，对方的标记保留 ✅ |
| 11 | 文本入口收 nil / 未知文本 | nil→nil，未知原样返回 ✅ |
| 12 | 超长字符串 / 空串 | 安全 ✅ |

### 四、RimWorld 三工程复检（同日）

| 工程 | XML | 翻译 | Def 引用 | 代码质量 | 部署 |
| --- | --- | --- | --- | --- | --- |
| GNH-LocalFixes | 2/2 通过 | 无 Keyed（代码无 Translate 调用，无需翻译） | — | TODO/空 catch/硬编码 均 0；Harmony 2 处、幂等守卫 15 处 | 0 差异 |
| 米莉拉关键物品制作补丁 | 21/21 通过 | Keyed 6×3 一致；DefInjected 63×3 无差异、字段越界 0 | 21 个 defName 全部就位 | 同上，均 0 | 0 差异 |
| 床铺增益建筑通用兼容 | 8/8 通过 | Keyed 36×3 一致；DefInjected 2×3 一致；代码引用 36 键**全部有定义** | defName 1 个 | 同上，均 0 | 0 差异 |

- 三个工程 `dotnet build -c Release` 全部 **0 错误 0 警告**；
- `csproj` 的 `Version` 与 `About.xml` 的 `modVersion` **全部一致**（上轮修正后未回退）。

> 注：`GNH.LocalFixes.csproj` 不出现在 RimWorld 部署目录，是该模组的发布结构决定的（只发布 `About/`、`Patches/`、`Assemblies/`），不是缺失。

---

## 附录四：改为独立汉化包（2026-10-03 晚间）

### 一、为什么要改

此前汉化是**直接改写原模组文件**的（Vanilla Plus Megapack 内的 `ModOptionsMenu`、以及 HD2 Transmog）。代价是：模组一更新汉化就没了，而且动了作者的文件。现已改为**完全独立的汉化 mod**，一个原模组文件都没碰。

### 二、独立包长什么样

```
%LOCALAPPDATA%\hd2arsenal\mods\GNH-Chinese-Simplified-Pack\
├── manifest.json                      Arsenal 识别用（名称/GUID/说明/选项）
└── Addon\9ba626afa44a3aa3.patch_0     单个 patch，内含 3 个资源
    ├── mods/gnh_cn/zh_hans            运行时接管 Lua（444 条词表 + 两道保险）
    ├── mods/hd2transmog/foundation    Transmog 的汉化副本（覆盖式）
    └── mods/gnh_cn/readme             说明文本
```

### 三、它是怎么生效的（不修改任何原文件）

**关键机制**：HD2 的模组都是通过包装全局 `_G.update` 拿到每帧回调的（`rawset(_G, 'update', ...)`），我用了同一套机制：

1. **加载时**若 `_G.ModOptionsMenu` 已就绪 → **当场接管**它的公开 API `register_option`；
2. **若还没就绪** → 包装 `_G.update`，每帧检查，在它出现的那一帧**抢先接管**（早于各模组的注册）；
3. 接管后只做**浅拷贝再翻译**，绝不改动调用方传入的表，外层 `pcall` 兜底。

**加载顺序保证**：独立包被部署为 `patch_84`，是当前 **最大编号**（0~84）→ 最后加载 → ModOptionsMenu（patch_14）早已就绪 → 走第 1 条路径。

### 四、原模组文件已完全还原

| 文件 | 状态 |
| --- | --- |
| Vanilla Plus Megapack 的 `ModOptionsMenu` patch | 哈希 `7ad2b96b3ac5504c`，与原始备份**逐字节一致** |
| HD2 Transmog 的 `Addon` patch | 哈希 `7e636c0b787a256d`，与原始备份**逐字节一致** |
| 游戏 `data\patch_14` / `patch_20` | 同样已还原为原版 |

### 五、极端场景测试（11 项，真实 Lua 执行）

| # | 场景 | 结果 |
| --- | --- | --- |
| 1 | host 已就绪（正常路径） | 翻译生效，日志含"已接管" ✅ |
| 2 | **host 尚未就绪（走 `update` 轮询）** | 同样接管成功、翻译生效 ✅ |
| 3 | 没有 `update` 函数（极端环境） | 不报错 ✅ |
| 4 | spec 带**只读元表** | 调用成功、翻译生效、原表未被触碰 ✅ |
| 5 | spec 是 nil / 字符串 / 缺字段 | 安全透传 ✅ |
| 6 | 真实注册函数抛错 | 错误原样传播，不被吞 ✅ |
| 7 | 与其他模组的 `update` 包装叠加 | 调用链完好 ✅ |
| 8 | 重复加载 | 幂等，只接管一次 ✅ |
| 9 | 未知文本 | 原样返回 ✅ |
| 10 | mod 名与长描述 | 正确汉化（如 `SMARTER GUARD DOGS & SENTRIES` → 更聪明的护卫犬与哨戒炮）✅ |
| 11 | 选项值 `Off` | 保持 `Off`，交给游戏原生显示"关" ✅ |

### 六、五遍复核结果

1. **独立包自身**：manifest 合法；patch 3 entry、资源 ID 全匹配；
2. **Lua 编译**：三个 entry 在真实 Lua 运行时下**全部编译通过**；
3. **原模组文件**：与备份哈希一致，确认已还原；
4. **游戏 data**：独立包位于 `patch_84`（最大编号，最后加载），与模组库哈希一致；
5. **汉化覆盖**：注册 API 接管 ✓、每帧轮询兜底 ✓、幂等标记 ✓；Transmog 界面串已汉化，**用于识别游戏原生分类的 `CUSTOM VARIANTS` 等英文比较串刻意保留**（比较表达式里出现中文的数量 = 0）。

### 七、维护与回退

- **模组更新后**：独立包**不会**被上游覆盖（它有自己的文件）；但 `mods/hd2transmog/foundation` 是副本，Transmog 大版本更新后应重跑 `build_pack.py` 重新生成副本，否则可能用旧版覆盖新版（脚本会基于备份里的**原版**重新替换，不会累积污染）。
- **停用汉化**：在 HD2 Arsenal 里关掉「GNH 简体中文汉化包」，或直接删除 游戏 `data\9ba626afa44a3aa3.patch_84`（及其 `.gpu_resources`/`.stream`）。
- **彻底清除**：删除模组库里的 `GNH-Chinese-Simplified-Pack` 目录。
- 原模组文件始终是作者原版，无需还原。

---

## 附录五：零冲突重构（可分发给别人）

### 一、为什么要重构

原来的独立包里有 Transmog 的**覆盖式**副本（`mods/hd2transmog/foundation`），因此模组管理器必定显示「与 HD2 Transmog 冲突」。要让**别人用也不冲突**，只有一条路：**只提供全新的资源路径，不覆盖任何已有资源**。

### 二、现在的两个包

| 包 | 内容 | 冲突 | 用途 |
| --- | --- | --- | --- |
| **GNH 简体中文汉化包**（主包） | 只含 `mods/gnh_cn/zh_hans` + `mods/gnh_cn/readme`，运行时接管 ModOptionsMenu | **零冲突** | 分发/日常使用 |
| GNH Transmog 界面汉化（可选包） | 覆盖 `mods/hd2transmog/foundation` | 与 HD2 Transmog 冲突 1 处（预期） | 想要 Transmog 界面中文时单独启用 |

主包 zip：`dist\GNH简体中文汉化包-Helldivers2.zip`（约 8 KB）
可选包 zip：`dist\GNH-Transmog界面汉化-可选包.zip`

### 三、为什么主包零冲突

Arsenal 的冲突检测比的是「两个模组是否提供同一个游戏资源」。主包提供的两个资源路径是本模组**独有**的：

- `mods/gnh_cn/zh_hans`（运行时接管代码 + 473 条词表）
- `mods/gnh_cn/readme`

用资源 ID 校验过：这两个 ID 在模组库里**只有本模组提供**。汉化通过**运行时接管** `ModOptionsMenu.register_option` 实现，不触碰任何其他模组的文件。

### 四、如果已经把旧版导入过 Arsenal

Arsenal 会把每个模组的文件清单缓存进 `mod_headers` 表。旧版缓存里有 **3 条**资源（含 Transmog 那条），这就是冲突提示仍然出现的原因（已用资源哈希逐一比对确认）。

**解决办法（两步，最干净）**：

1. 在 HD2 Arsenal 里**删除**「GNH 简体中文汉化包」；
2. 用新的 `GNH简体中文汉化包-Helldivers2.zip` **重新导入**，再点 Deploy。

导入后清单变成 2 条，冲突提示消失。

### 五、分发说明

直接把 `GNH简体中文汉化包-Helldivers2.zip` 给别人：对方在 Arsenal 里导入 → 启用 → Deploy 即可，**不会看到任何冲突**。

注意事项（可一并转告）：

- 建议把本模组放在**模组列表靠后**的位置（Arsenal 默认把新导入的模组追加到末尾，通常已经是这样）；
- 它依赖 `_G.update` 主循环与 `ModOptionsMenu` 的公开 API，两者都是 HD2 模组生态的标准做法；
- 只汉化**界面文本**（选项名/说明/模组名/选项值），不触碰任何数值与逻辑；
- 不装 Vanilla Plus Megapack（没有 ModOptionsMenu）时，本模组只会记一条日志、不报错、不影响其他模组。

---

## 附录六：两个汉化包的极端场景与六维度复检（2026-10-03 深夜）

### 一、极端场景（12 项，真实 Lua 执行，全部通过）

| # | 极端假设 | 结果 |
| --- | --- | --- |
| 1 | ModOptionsMenu 已就绪 | 当场接管，翻译生效 ✅ |
| 2 | ModOptionsMenu 延迟出现 | 走 `_G.update` 轮询，照样接管 ✅ |
| 3 | **既没有 host 也没有 update** | 不报错，只记一条日志 ✅ |
| 4 | **没有 Bingus loader**（日志文件打不开） | 不报错 ✅ |
| 5 | **`print` 被别的模组改坏** | 不报错（pcall 包住）✅ |
| 6 | **`_G` 被设了元表** | 正常工作（全部走 rawset）✅ |
| 7 | **别的模组先把 `register_option` 包装好** | 两层包装正确叠加，对方标记保留 ✅ |
| 8 | **choices 是只读表** | 调用成功、翻译生效、原表未被触碰 ✅ |
| 9 | **label 靠元表提供**（浅拷贝会丢字段） | 检测到字段缺失，原样透传、不报错 ✅ |
| 10 | label 是数字 / 含引号换行 / 300 字符超长 | 全部安全 ✅ |
| 11 | 已经是中文的文本 | 不二次处理 ✅ |
| 12 | **同一个包被加载两次** | 幂等，第二次跳过 ✅ |

### 二、六维度复检（对应你要求的编译 / XML / 翻译 / Def 引用 / 构建配置）

| 维度 | 对应到 HD2 | 结果 |
| --- | --- | --- |
| **编译** | Lua 编译（真实 Lua 运行时） | 两个包共 3 个 entry **全部编译成功** |
| **XML** | patch 容器格式 | 头部字段自洽、每条 entry 的记录偏移/长度校验、**资源 ID 全部匹配** |
| **翻译** | 词表完整性 | 473 条，无空键/空值/占位符；**全部就位**于主包 Lua（Lua 编译校验通过） |
| **Def 引用** | 资源 ID ↔ 路径映射 | ID 与 murmur64(路径) 一一对应；两包资源**互不重叠**；**主包在模组库内提供者数 = 1（零冲突）** |
| **构建配置** | manifest.json | JSON 合法、Guid/Version/Options 齐全、Include 目录存在 |
| **代码与注释** | Lua 代码与注释一致性 | 4 项声明逐条核对通过：浅拷贝 ✓ 每帧轮询 ✓ 幂等标记 ✓ 不直接改调用方的表 ✓ |

### 三、本轮修正的自身缺陷

1. **脚本写死目录名**：Arsenal 每次重新导入会给目录换 `_ARxxxxxx` 后缀，导致脚本找不到包 → 已全部改为**按关键词动态发现**目录。
2. **两处测试设计错误**（场景 7 的包装顺序、场景 12 只加载一次）→ 已修正并复跑通过。
3. **一次误操作**：清理 Arsenal 数据库时按 `uuid` 删除，误删了主包记录 → **已从备份完整恢复**，并决定**不再改动 Arsenal 数据库**，改由用户在界面里处理（见下）。

### 四、需要你在 Arsenal 里做的一步

当前数据库里有 **4 条**汉化包记录，其中 2 条指向已被删除的旧目录（就是冲突提示的来源）：

| 记录 | 状态 |
| --- | --- |
| GNH 简体中文汉化包 → `…_AR707121` | ❌ 目录已不存在 |
| GNH Transmog 界面汉化（可选）→ `…_AR146312` | ❌ 目录已不存在 |
| GNH 简体中文汉化包 → `…_AR626100` | ✅ 当前（清单 2 条 = 零冲突） |
| GNH Transmog 界面汉化（可选）→ `…_AR369945` | ✅ 当前 |

**最干净的做法**：在 Arsenal 里把 4 条 GNH 条目**全部删除**，再用最新的两个 zip 重新导入一次 —— 这样库里只会剩 2 条正确记录，冲突提示随之消失。

zip 位置：
- `dist\GNH简体中文汉化包-Helldivers2.zip`（零冲突主包）
- `dist\GNH-Transmog界面汉化-可选包.zip`（覆盖式，会显示 1 处冲突，属正常）


---

## 许可与第三方声明

本仓库的汉化词表、构建脚本与文档由 **大赢经直插白皮赢道（GNH-CN-CYS）** 制作，以 [MIT](LICENSE) 许可发布。

发布包中**不含**任何上游模组的文件副本（主包只提供 `mods/gnh_cn/*` 两个全新资源路径）；
用户需自行安装 [HD2 Arsenal](https://www.nexusmods.com/helldivers2) 与相应上游模组（Vanilla Plus Megapack、HD2 Transmog 等）。
若选择启用 `dist/GNH-Transmog界面汉化-可选包.zip`，它会覆盖 `mods/hd2transmog/foundation` —— 这是该可选包的预期行为。

---

## 更新日志

### 2026-10-04　词表从 110 条扩展到 444 条

原先只覆盖 Aggro Counter、Armored Overhaul、Smarter Guard Dogs & Sentries 三个模组的选项文本。
本次把**当前启用的全部 20 个模组**纳入汉化：

| 范围 | 说明 |
| --- | --- |
| 游戏内「模组选项菜单」 | 选项名、选项值、选项说明 —— 由主包运行时接管替换 |
| HD2 Arsenal 管理器界面 | 模组名称、模组简介、选项名与说明 —— 写入各模组 `manifest.json`（不改动上游逻辑，仅本地化文本） |
| 新增模组 | HD2 HUD+、Better Map Markers、Enhanced Sentries Revamped、Menacing Heavy Weapons、Muzzle Flash Smoke Remover、Concept Mech |

**词表构成**：`cn_add.py`（选项名/值 261 条）、`cn_desc.py`（选项说明 105 条）、`cn_fix.py`（补漏 29 条）、
`cn_mods.py`（模组名 20 条），合并去重后共 **444 条**（`tools/cn_strings.py`）。

**未翻译项（刻意保留原文）**：武器/载具型号（`Flak36`、`Gau-19`、`M61`、`BAR`、`MG42`、`PKM`、`FRV` 等）、
护甲代号（`A9`、`DP8`、`RS67`）、模组专名（`Castle ODST`、`HD2 HUD+`）与梗名（`Meet The Medic`）。

**校验**：主包 Lua 经真实 Lua 运行时 `load()` 编译通过；词表 444 条全部就位于包内；
20 个模组的 manifest 文本仅剩上述刻意保留项。

### 2026-10-04（二次更新）　词表 444 → 473 条

- 新增模组：**HD2 SmoothBoot**、**HD2 C4 快捷操作**、**目标追踪器**、**机甲部位血量 HUD**
- 跟进更新：**更聪明的护卫犬与哨戒炮 4.6.3**、**HD2 Transmog 基础组件 0.2.1（实验版）**
- **重要修复**：`build_packs2.py` 原先把 Transmog 汉化包的基底路径写死为 0.1.5，
  在上游更新到 0.2.1 后会把版本**回退**。现已改为**动态取模组库中的当前版本**（备份仅作兜底）。
  同时给 `cn_strings.py` 的合并流程加上"只取指定词表变量"的约束，避免把 Python 内置名写进词表。
- 顺带清理了 Arsenal 模组库中 8 条失效记录，并修正 6 条指向 `temp_extract_*` 的错误路径。

---

﻿## 附录三：MODS 面板「先注册的模组漏翻」根因与修复（2026-10-05）

### 一、现象

游戏内 `ESC → 模组`：

| 面板 | 现象 |
| --- | --- |
| Aggro Counter（仇恨计数） | 全中文 ✅ |
| Smarter Guard Dogs & Sentries | 全中文 ✅（左侧列表已是「更聪明的护卫犬与哨戒炮」） |
| **Objective Tracker（任务目标追踪）** | **全英文 ❌** |
| **HD2 TRANSMOG（HD2 幻化）** | **全英文 ❌** |

### 二、定位（读游戏日志，不靠猜）

游戏为每个模组单独写日志，两个日志一对照就清楚了：

| 证据 | 说明 |
| --- | --- |
| `Logs\GNHChinesePack.log` 里有 `已接管 ModOptionsMenu.register_option（词表 897 条）` 与 `汉化: Show Badge -> 显示徽章` | 接管逻辑本身没问题，确实在翻译 |
| `Logs\ModOptionsMenu.log` 的注册顺序：`Mod Options Menu initialized.` → Objective Tracker 17 个选项 → Better Lobby Management 3 个 → **（汉化包在这里接管）** → Smarter Guard Dogs 6 个 → Shallow Water Diving 1 个 → Aggro Counter 15 个 → Armored Overhaul 11 个 → HD2 Transmog 3 个 | 汉化包的 Lua **比 Objective Tracker 晚执行** |
| `GNHChinesePack.log` 的前 3 条是 `[function] -> [function]`（Better Lobby Management 的三个函数型 label） | 与上一条互相印证：接管点确实落在 Objective Tracker 之后 |

**根因**：各模组的 Lua 由共享加载器按它自己的顺序执行，汉化包**无法保证排在最前面**。
只包装 `register_option` 只能影响「接管之后」发生的注册，**先注册进来的选项在寄存器里已经是英文**，
而字符串型界面文本是在注册那一刻被解析并缓存的，之后不会再解析。

### 三、修复：实时接管 + 就地补翻

1. **实时接管**（原有做法）：包装 `ModOptionsMenu.register_option`，翻译 `label / description / mod / choices`。
2. **就地补翻**（本次新增，关键）：
   - 用 `debug.getupvalue` 从 ModOptionsMenu 的导出函数（`register_option` / `get` / `set` / `ready` / `on_change`）里
     取出它的内部 `state` —— 判据是**该 upvalue 同时含 `options` 与 `mods` 两张表**；
   - 把**已经注册进来**的选项就地改成中文：`option.label`、`option.description`、`option.choices[i]`、`mod.title`；
   - **为什么改 `choices` 是安全的**：`choice` 的值是 1 基下标（存在 `state.values[id]`），与显示文本无关；
   - **为什么改完立刻生效**：ModOptionsMenu 每帧用 `shows_text(row + ROW_TEXT, option.label)` 校验行文本，
     label 一变就判定页面失效并重建，下一帧用新文本重绘；
   - 接管成功后**立刻补翻一次**，此后每 20 帧复查一次，连续 3 次没有新条目就停止（开销可忽略）。
3. **顺带覆盖 Mod Bindings Menu**：包装 `ModBindingsMenu.register_binding(id, label, slot, options)` 的**第 2 个参数**，
   并补翻 `state.registry` 里的 `text` / `label` / `category`，
   因此 `SHOW / HIDE BADGE`、`MOVE BADGE UP` 等按键名也变中文。
4. **兜底不写坏东西**：`debug` 取不到 `state` 时补翻静默失效（只写一条日志），实时接管照常工作；
   所有补翻都在 `pcall` 里执行，绝不因为补翻出错而影响菜单本身。

### 四、词表补充（473 → 541 组，含大写形式 1026 条）

新增 `tools/cn_ui3.py`，60 组词条**逐字符取自各模组的 Lua 源**（源文件已 dump 到 `tools/` 之外的 `lua_dump/` 便于复核）：

| 来源 | 内容 |
| --- | --- |
| Objective Tracker 0.4.12 | 17 个选项的全部 label / description / choices（32 条） |
| HD2 Transmog 0.2.1 | `Preview style`、`Armory 3D preview`、`Regenerate previews` 三个选项及其选项值、说明 |
| Aggro Counter 1.3 | Mod Bindings Menu 按键名：`SHOW / HIDE BADGE`、`BADGE BIGGER`、`MOVE BADGE UP` 等 7 条 |
| HD2 Transmog | 按键名：`Select Next Transmog Piece`、`Next / Previous Transmog Variant` 等 |
| 各模组 | MODS 页显示的模组名：`HD2 Transmog`、`Shallow Water Diving`、`Better Lobby Management` |

扫描工具 `tools/scan_ui.py`：遍历模组库里全部 206 个 Lua entry，提取注册到菜单的界面文本，列出**词表里缺失**的条目。
以后跟版本更新，只要重跑它就能知道还差哪些。

### 五、可选包（Transmog 界面）的三处修复

1. **修掉一处会让「自订变体」区块识别失败的替换**：上一版把 `section={title='Custom Variant'` 改成了中文，
   而判定处 `header.text=='Custom Variant'` 仍是英文 —— 这两者本应成对出现。现在**两者都保持英文**，
   只替换真正上屏的两处 `text('Custom Variant', ...)`。
2. **补齐遗漏**：`MODIFIED UNIQUE`、`Default: `、`Now (temporary): `、`Modded `、`Name and create`、
   `Set the look`、`D-pad / left stick: choose a look. A: select.`、`' saved'` / `' owned choices'`。
3. **新增校验脚本 `tools/verify_tm.py`**：把上游原始 `foundation` 与汉化版逐行 diff，
   并统计 `== '...'` / `~= '...'` / `['...']` 三类**比较 / 索引语境**里的字面量是否被改动。
   **本次结果：受影响字面量 0 个** —— 即只动了上屏文本，没有动任何判定逻辑。

### 六、验证（真实 Lua 运行时，而不是只看日志）

`tools/test_pack_lua.py` 用 `lupa` 起真实 Lua 运行时，构造一个与 ModOptionsMenu 内部结构一致的替身
（`state.options` / `state.mods` / `revision`），**先注册几个「比汉化包更早注册」的选项**，再加载主包的 Lua：

| 检查项 | 结果 |
| --- | --- |
| 主包 Lua 编译并执行 | 通过，无报错 |
| 补翻 toggle 选项名 | `Show objective tracker` → **显示任务目标追踪** |
| 补翻 choice 选项名 | `Icon and distance colors` → **图标与距离颜色** |
| 补翻 choice 选项值（大写形式） | `OBJECTIVE COLORS` → **目标配色**、`HELLDIVER GOLD` → **绝地潜兵金**、`ICE WHITE` → **冰白** |
| 补翻 description | 整句中文，与词表逐字符一致 |
| 补翻模组名 | `OBJECTIVE TRACKER` → **目标追踪器** |
| 接管之后注册的选项 | `Show Badge` → **显示徽章**（实时翻译仍然有效） |
| 补翻计数与 revision | 第 1 次扫描补翻 13 项，`revision` 正确自增，菜单会自动重绘 |

### 七、顺带清理（这些是「汉化时好时坏」的隐藏原因）

- Arsenal 包目录里残留三个**旧版散装 lua**：`cb78d3a9e61e5cd6.lua`（旧版 `mods/gnh_cn/zh_hans`）、
  `14f0960cccd5967c.lua`（旧版 readme）、`d42a76efa2beb2e3.lua`（**基于 Transmog 0.1.5 的旧汉化**）。
  它们是早期构建的遗留产物，留着会让 Arsenal 的部署结果不可预测。已备份到
  `_scratch/hd2/backup/leftover-lua/` 后**删除**，现在两个包目录里各自只剩 `Addon/9ba626afa44a3aa3.patch_0` 与 `manifest.json`。
- 部署脚本原先用「文件大小 > 2 MB」判断该删哪个 patch，**会误删上游原版的 Transmog Foundation**。
  现在改成按内容精确判定：
  - 包 A：该 patch 是否提供 `mods/gnh_cn/*` 资源；
  - 包 B：那份 `mods/hd2transmog/foundation` 里**有没有汉字**（上游原版一个汉字都没有，实测 zh 计数 = 0）。

---

﻿## 附录四：全面审计与加固（2026-10-05 第二轮）

> 本轮的目标不是"再加几条翻译"，而是把整套东西按"要发给别人、别人还要长期用"的标准重新过一遍：
> 兼容性、完整性、性能、代码整洁度、注释可读性，并**主动构造极端情况去撞**。

### 一、代码重构：从"拼字符串"改成"模板文件"

原先运行时代码是塞在 Python 里的一个大字符串列表，改一行注释都要数缩进。现在拆成：

| 文件 | 职责 |
| --- | --- |
| `tools/lua_src/runtime_template.lua` | 运行时代码本体，388 行，**独立可读、可单独做语法检查** |
| `tools/build_packs2.py` | 只负责把词表填进模板的 `--[[GNH_CN_TABLE]]` 占位符 |

构建脚本新增两道自检：模板里找不到占位符直接报错；生成后的 Lua **编译不通过就中止构建**，绝不把坏文件打进 patch。

### 二、性能实测（lupa / Lua 5.5 解释执行；游戏用 LuaJIT 会更快，下表是保守上界）

| 项目 | 实测 | 说明 |
| --- | --- | --- |
| 加载脚本 + 首次补翻（63 个选项，即用户实际规模） | **1.0 ms** | 启动时一次性 |
| 每帧开销 —— 初始化期间 | 低于测量精度（150 帧合计 < 1 ms） | 只在启动头几秒 |
| 每帧开销 —— **初始化完成之后** | **0.000047 ms/帧**（47 纳秒） | 折算 60fps 下 CPU 占用 **0.0003%** |
| 极端：5000 个选项的加载 + 一次性补翻 | **4 ms** | |
| 极端：连续注册 10000 次 | **46 ms**（0.0046 ms/次） | 任何真实模组都到不了这个量级 |
| 词表查找 | 0.08 微秒/次 | 哈希表 O(1) |
| 主包体积 | 146 KB | 其中 89% 是词表 |

**为性能做的具体改动**：

1. **收工即停摆**：初始化完成后 `done = true`，主循环里只剩 `if not done then tick() end` 一次真假判断。
   日志里会写一条"初始化完成（第 N 帧），主循环已交还"。
2. **按键菜单改为低频重试**：原先若用户没装 Mod Bindings Menu，会**每帧**白试一次；现在每 30 帧试一次，900 帧后彻底放弃。
3. **补翻自动收敛**：每 20 帧扫一次，连续 3 次扫不出新东西就永久停止。
4. 所有补翻都包在 `pcall` 里，出错也只是不翻译，不会中断游戏帧。

### 三、兼容性与健壮性（25 个极端场景，全部用真实 Lua 运行时跑）

| 分组 | 场景 | 结果 |
| --- | --- | --- |
| 加载环境 | ModOptionsMenu 完全不存在 / 没有 register_option / register_option 不是函数 / `_G.update` 不存在或不是函数 / 日志打不开 / 脚本被加载两次 | 7/7 通过：全部静默降级，不报错 |
| 菜单结构 | debug 库不存在 / getupvalue 报错 / 找不到内部 state（模拟上游改版）/ options 表混入字符串数字 nil / 选项缺字段 / choices 是字符串或空表 / 选项名是函数 / revision 不是数字 / mods 里混入非表 | 9/9 通过：**降级后实时翻译仍有效**，不会误伤函数型文本 |
| 注册行为 | 传入 nil / 字符串 / 缺 label / **只读表** / 补翻后重复注册 / 同名不同内容 / 上游自己抛异常 / 整个菜单是只读代理表 | 8/8 通过：只读表照样能翻译；**上游异常如实透传不被吞掉** |
| 按键菜单 | 正常接管+补翻 / 出现数字或 nil 标签 | 2/2 通过 |
| 重复加载 | 第二次加载不重复包装 | 1/1 通过 |

**本轮修掉的一个真实兼容性缺陷**：
补翻会把 `option.label` 从英文改成中文，而上游判断"同一个 id 是否重复注册"时比较的正是**当前显示文本**。
于是模组第二次用英文注册同一个选项时，会被上游判成"内容不一样"而拒绝，模组可能因此在日志里刷错误。
现在脚本会记住"哪些 id 是我们翻过的"，遇到这种情况按**重复注册**放行返回 true ——
只有当新注册的内容**翻译后与已存在的一致**时才放行，真正的冲突依旧照上游规则拒绝。

### 四、LuaJIT / Lua 5.1 兼容性

游戏用的是 LuaJIT（ModOptionsMenu 源码里有 55 处 `ffi`），而测试环境是 Lua 5.5，语法更宽。
所以额外做了一遍"5.1 不允许的东西"的静态排查：

- 未使用 `goto` / `::label::`（LuaJIT 2.0 不支持）
- 未使用 `//`、`&`、`|`、`<<`、`>>`（5.3+ 才有）
- 未使用 `\z`、`\u{}` 转义、`<const>`、`<close>`
- 未使用 `table.unpack` / `table.pack` / `string.pack` / `math.type` / `math.tointeger`
- 45 个局部变量名无保留字冲突；chunk 顶层局部变量 29 个，远低于 200 上限
- **运行后只新增了 2 个全局变量**：`GNH_CN_PACK_LOADED`（重复加载守卫）与 `update`（主循环挂钩），无命名空间污染

### 五、词表审计

用 `tools/audit_cn.py` 把 541 组词表整体过了一遍：

| 检查项 | 结果 |
| --- | --- |
| 控制字符（`\r`、`\0` 等会破坏 Lua 字面量） | 0 条 |
| 空键 / 空值 | 0 条 |
| 与游戏内置原生词冲突 | 5 条（`On`/`Off`/`Default`/`Balanced`），译文与游戏原生叫法一致，保留 |
| 译文超长 | 有，但已加**运行时长度保护**：超长自动回退英文，保证选项不会因超长被上游拒绝 |
| 纯英文"翻译"（键=值） | 28 条，全部是刻意保留的型号 / 代号 / 专名 |

### 六、覆盖率

`tools/scan_ui2.py`（改进版，能正确处理 `..` 跨行拼接）扫描 206 个 Lua entry：

- 识别出界面文本 **194 条**，词表已覆盖 **181 条（93.3%）**
- 剩余 13 条全部是**刻意保留**：测试版专用文本（作者标注 "Test build only"）、
  ModOptionsMenu 源码注释里的 API 示例（`Row text`、`Mod name`、`My Mod`）、
  开发者调试探针标识（`Probe A` / `Probe B`）

### 七、本轮同时修掉的工程问题

1. **构建脚本原先会误删上游原版文件**：旧逻辑用"文件大小 > 2 MB"判断该删哪个 patch，
   而上游原版的 Transmog Foundation 也是 2.87 MB —— 一旦执行就会把**官方原版**删掉。
   现在改为按内容精确判定（主包看是否提供 `mods/gnh_cn/*`；可选包看那份 foundation 里**有没有汉字**）。
2. **工具链约定的资源路径注释丢失**：模板化时漏了首行 `-- HD2-Addon: mods/gnh_cn/zh_hans`，
   导致构建中途崩溃。现在既补回了首行，也让校验遇到"缺注释"时给出提示而不是崩溃。
3. **UTF-8 BOM**：模板文件曾被写入 BOM，Lua 会把它当非法字符。已去除，并把"无 BOM"纳入自动检查。
4. **Arsenal 包目录里的旧版散装 lua**（含一个基于 Transmog 0.1.5 的旧汉化）已备份后删除。

### 八、两个"看起来像问题、查证后不是问题"的点（如实记录）

审计过程中出现两处告警，都追到了根：

1. **可选包在 Lua 5.5 下编译报错**（`attempt to assign to const variable 'line'`）。
   拿上游**原版** `patch_60` 做对照：**原版同样报错、报错行完全相同**，而那一行我们根本没动过。
   原因是可选包里跑的是上游 ModOptionsMenu 自己的代码，里面有 LuaJIT 专有写法，
   而测试环境是较新的 Lua 5.5 —— **属版本差异，与汉化无关**（游戏里用的是 LuaJIT）。
   检查脚本已改成"与上游原版对照"，不再单方面报警。

2. **"可选包判定语境里出现中文 18 处"**。这是最初用"整行里同时有 `==` 和汉字"做的**粗筛，属误报**：
   那 18 行里的中文都出现在 `text('...')` 这类**显示参数**里，判定用的字面量仍是英文。
   换成精确做法（只提取 `=='...'` / `~='...'` / `['...']` 里的字面量）后：
   **判定语境里的中文字面量 = 0**（上游原版 2170 个判定字面量同样全部为英文）。

### 九、最终交付状态

| 项目 | 状态 |
| --- | --- |
| 主包 / 可选包 Lua 结构 | 资源 ID 与路径哈希全部匹配、容器可完整重建 |
| 四处副本一致性 | 构建目录 = Arsenal 启用目录 = 游戏 data = 分发 zip（sha1 全同） |
| 词表 | 541 组 / 含大写 1026 条；覆盖率 181/194 |
| 极端场景 | 25/25 通过 |
| 兼容性检查 | 全部通过（0 项失败） |
| 性能 | 初始化后每帧 0.000047 ms（60fps 下 0.0003%） |
