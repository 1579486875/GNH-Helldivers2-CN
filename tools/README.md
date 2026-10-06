# GNH Helldivers 2 汉化工具集

本目录是「HD2 模组简体中文汉化」的完整工具链。所有脚本都是**一次性/可重复运行**的，
不需要安装依赖（除 `lupa` 用于构建时的 Lua 语法自检）。

---

## 一、汉化体系：三条不同的路

HD2 的模组界面文本来自**三种完全不同的位置**，所以汉化也分三条路。
**理解这三条路是维护的关键** —— 它们「更新后会不会丢」的答案各不相同。

| # | 走的哪条路 | 适用于 | 机制 | 模组更新后 |
|---|---|---|---|---|
| 1 | **运行时翻译包** | 绝大多数模组（走 ModOptionsMenu 的） | 汉化包在运行时 hook `register_option` 改写文本，并向 `_G.BingusTranslations` 注册官方翻译包 | ✅ **自动保持** |
| 2 | **直接改文件** | 不走菜单系统的模组（目前只有 **HUD+**） | 等长替换二进制字符串池里的英文 | ❌ **会丢，需重跑** `hud_cn.py` |
| 3 | **改 Arsenal 数据** | Arsenal 模组列表显示的名字/描述 | 写 `manifest.json` + `hd2a_data.json` + `mod_headers.db` | ❌ 会丢，需重跑 |

### 路 1 的原理（为什么它能自动保持）

汉化包提供一个全新资源 `mods/gnh_cn/zh_hans`（**零冲突**，不覆盖任何原文件），
它在加载时做三件事：

1. **挂钩子**：包装 `ModOptionsMenu.register_option`，在注册那一刻把
   `spec.label` / `description` / `choices` / `mod` 换成中文（`translate_spec`）；
2. **补翻（sweep）**：对**已经注册完**的条目，直接改菜单内存里的 `option.label` 等字段
   —— 因为菜单用内部 ID 记值，改显示文字不影响玩家实际选中的值；
3. **注册 Bingus 官方翻译包**：往 `_G.BingusTranslations.packs` 里加一条
   `{language='zh-Hans', mods={模组标识={键=译文}}}`。这条路能治**钩子够不着**的情况
   （例如 Vanilla Plus 的 17 个子模组是在加载器的 `after_startup` 事件里一次性注册的，
   那时钩子还没装上）。

**词表**：`cn_strings.py`（由 `merge_cn_fixed.py` 从各 `cn_*.py` 合并而来，**先到先得**）。
构建时会为每条自动生成**全大写键**（菜单显示选项值和模组名时会转大写）。

### 路 2 的原理（为什么必须等长替换）

`HUD+` 把设置页直接塞进**游戏原生设置菜单**，文本存在一个**按语言分段的二进制字符串池**
（英文段后面紧跟韩文段，没有中文段 → 游戏回退到英文段）。

汉化的办法是**改英文段**，规则是：

```
原文  Trajectory Preview            (18 字节)
译文  弹道预览\0\0\0\0\0\0           (12 字节 + 6 个 \0 补齐)
```

**中文绝不允许比英文长，短的用 `\0` 补齐** —— 于是字符串池**总长度不变、偏移表一个字都不用动**。
这样既绕开了「重建容器结构」的风险（那曾把 Castle 模组搞崩），又因为字符串本来就以 `\0`
结尾而完全等价。**每次都校验文件长度不变**。

### 关键限制

- **字体**：某些渲染位置（如菜单右侧**大标题**）用的字体**不含全角引号 `「」`**，
  会显示成 `?`。所以**会被当作标题的短词条一律不用 `「」`**（`cn_pack9.py` 就是为此加的）。
  说明正文那个位置正常支持，可以保留。
- **长度上限**（超了会被整个拒绝注册，比显示英文更糟）：
  选项名 64 字、选项值 48 字、说明 400 字、**模组名 40 字**。

---

## 二、常用流程

### 首次 / 从零重建汉化包

```bash
python merge_cn_fixed.py     # 合并所有 cn_*.py → cn_strings.py
python build_packs2.py       # 构建 A 包（零冲突汉化）+ B 包（Transmog 汉化）并部署到游戏 data
python sync_to_arsenal.py    # 同步回 Arsenal 模组目录（关键！否则 Arsenal 一 Deploy 就打回）
```

> ⚠️ **`build_packs2.py` 只写游戏 `data` 目录，不写 Arsenal 的模组目录**。
> 如果不同步，你在 Arsenal 里点一次 Deploy，Arsenal 就会拿它的旧 patch 覆盖掉新包。

### 新装了模组 / 想知道哪里还没汉化

```bash
python scan_missing_text.py    # 全量扫描所有模组的界面文本，与词表比对 → _missing.json
python classify_missing.py     # 分类：真缺翻译 / 模组自带中文 / 翻译键（未解析）
```

拿到清单后：写一个新词条文件 `cn_packN.py`（形如 `CN_PACKN = {"英文": "中文"}`），
把它加进 `merge_cn_fixed.py` 的 `SPEC` 列表**末尾**（追加在最后 = 优先级最低，不会覆盖旧词条），
然后跑上面「首次」那三步。

### 模组更新后

| 情况 | 要做的事 |
|---|---|
| 走**路 1** 的模组更新 | 一般不用管；若作者改了文案，重跑 `scan_missing_text.py` 补词条 |
| **HUD+** 更新 | 跑 `python hud_cn.py`（脚本按**原文**定位，不依赖偏移/编号，直接重跑即可） |
| Arsenal 列表描述变英文 | `python scan_arsenal_desc.py` 找出，再 `python fix_arsenal_desc.py` |

> **`fix_arsenal_desc.py` 必须在 Arsenal 完全关闭时运行** ——
> Arsenal 在退出时会用内存里的数据覆盖 `hd2a_data.json`。

### 打包发布

```bash
python pack_mods_full.py   # 打包全部模组为 zip 合集（目录自动按日期命名）
python make_readme5.py     # 生成 ★ 使用说明.txt
python sync_dist.py        # 重建 6 个分发 zip
```

---

## 三、脚本清单

### 核心构建链

| 脚本 | 作用 |
|---|---|
| `hd2_patch.py` | **容器格式库**：读写 `9ba626afa44a3aa3.patch_N`，含 `murmur64a` 资源 ID 计算 |
| `merge_cn_fixed.py` | 按 `SPEC` 顺序合并所有 `cn_*.py` → `cn_strings.py`（**先到先得**，改值要改最早的那个文件） |
| `cn_*.py` | 词表分片。`cn_add` → `cn_desc` → … → `cn_pack9` 顺序合并 |
| `cn_strings.py` | **合并产物**（不要手改，会被覆盖） |
| `build_packs2.py` | 构建并部署两个包：A=零冲突汉化包，B=Transmog 界面汉化 |
| `lua_src/runtime_template.lua` | 汉化包的 Lua 源码模板（`--[[GNH_CN_TABLE]]` 是词表占位符） |
| `sync_to_arsenal.py` | 把 data 里最新（按内容特征识别）的包同步回 Arsenal 模组目录 |

### HUD+ 专用（路 2）

| 脚本 | 作用 |
|---|---|
| `hud_cn.py` | **可重复运行**：按原文定位并等长替换 HUD+ 字符串池里的 23 条文本 |
| `hud_add_entry.py` | 往 `hud_cn.py` 追加新词条（模组更新加了新选项时用） |

### 审计

| 脚本 | 作用 |
|---|---|
| `scan_missing_text.py` | 全量扫描模组界面文本，与词表比对，输出 `_missing.json` |
| `classify_missing.py` | 把缺失分成「纯英文待翻译」「模组自带中文」「翻译键」 |
| `scan_arsenal_desc.py` | 找出 Arsenal 里还是英文的模组描述 |
| `fix_arsenal_desc.py` | 把中文名字/描述写回 manifest + Arsenal 数据（**需 Arsenal 关闭**） |
| `audit_cn.py` / `compat_check.py` | 汉化包与模组的兼容性/完整性检查 |
| `extreme_test.py` | 25 个极端场景测试 |
| `test_pack_lua.py` / `verify_tm.py` | Lua 语法与 Transmog 覆盖点校验 |

### 打包

| 脚本 | 作用 |
|---|---|
| `pack_mods_full.py` | 打包全部模组为合集 zip |
| `make_readme5.py` | 生成合集的使用说明 |
| `sync_dist.py` | 重建并同步 6 个分发 zip |

---

## 四、技术要点

### patch 容器格式

```
0x00  u32 magic = 0xF0000011
0x08  u32 entry 数量
0x20  u32 文件总字节数        ← 带外部资源(.gpu_resources)的包此值不是实际大小，需宽松解析
0x50  u64 bundle id (固定 0xe217d12cfa8d4ea1)
每个 entry i： 0x68+80i = 资源 id；0x78+80i = 记录偏移；0xA0+80i = 数据长度+8
数据区： (u32 长度, u32 类型) 后跟数据；type=2 表示 Lua
```

**资源 ID = `murmur_hash_64A(资源路径, seed=0)`** —— 这也是判断两个模组是否提供同一资源、
即「Arsenal 报的文件级冲突」的依据。

### Lua 的三种存放形态

排查时注意，补丁里的 Lua **不一定是明文**：

1. **明文源码** —— 如战术战斗大修、边跑边打，可直接读；
2. **LuaJIT 字节码**（以 `\x1bLJ` 开头）—— 如 Bingus 加载器；
3. **转义内嵌字节码** —— `return assert(loadstring("\027\076\074..."))`，
   **明文搜索搜不到**（浅水潜行就是这种，第一轮扫描漏掉了它，后来靠解码字节码才拿到准确原文）。

### Bingus Text 翻译包格式

```lua
_G.BingusTranslations = {
  version = 1,
  serial  = N,                -- 加包后必须 +1，否则各模组不会重查
  packs   = {
    { language = 'zh-Hans', name = '...', mods = { 模组标识 = { 键 = 译文 } } },
  },
}
```

`mods` 的键是模组的 `english.mod`（如 `mod_options_menu`、`shallow_water_diving`），
`键` 是该模组英文词典里的键（如 `tab.mods`、`page.label`、`option.depth.label`）。
**占位符（如 `{page}`）必须与英文一致**，否则会被拒收。

### 汉化包能覆盖什么、不能覆盖什么

| 位置 | 能否覆盖 | 靠什么 |
|---|---|---|
| ModOptionsMenu 里的选项名/说明/选项值 | ✅ | 钩子 + 补翻 |
| 模组自己的 `spec.mod`（模组名） | ✅ | 钩子改 `spec.mod` |
| 由 `caller_mod()` 推断出的模组名 | ⚠️ | 只能靠补翻改 `mod.title` |
| Vanilla Plus 子模组的文本 | ✅ | Bingus 翻译包 |
| ModOptionsMenu 自身的界面文字 | ✅ | Bingus 翻译包（`mod_options_menu`） |
| **游戏原生设置菜单里的自建标签页**（HUD+） | ❌ | 只能直接改文件（路 2） |
| 模组自绘 HUD 上的文字 | ❌ | 见下条字体限制 |

---

## 五、踩过的坑（重要）

1. **字体缺字是静态检查查不出来的**
   模组自绘 HUD 用的字体（如 `core/performance_hud/debug`）**没有中文字形**，
   中文会显示成一串 `?`。**改动后必须先在游戏里改一个字试**，别一次改完。
   同理，菜单右侧大标题的字体不含 `「」`。

2. **长度超限会被整个拒绝注册**
   超长文本比显示英文更糟 —— 菜单会直接不显示该项。所以所有译文都要过长度检查。

3. **Arsenal 会覆盖你的改动**
   - Arsenal **运行时**不要改 `hd2a_data.json`，它退出时会用内存数据写回；
   - 汉化包**必须同步进 Arsenal 的模组目录**，否则它一 Deploy 就用旧包覆盖游戏 data；
   - **Arsenal 每次 Deploy 都会重新分配 patch 编号** —— 所以脚本里**不要写死编号**，
     按内容特征（资源路径、特征字符串）去识别。

4. **不要在 Arsenal 的列表位置和实际加载顺序之间想当然**
   实测：列表从上到下**就是**加载顺序（patch 编号升序），个别模组例外（如手工部署的包）。

5. **`0x20` 字段不可尽信**
   带外部资源的包，该值是「逻辑大小」而非文件大小，解析器要能宽松处理。

6. **模组更新会重建整个 patch**
   HUD+ 从 0.2.0 到 0.2.1 时文件从 641228 变成 644999 字节，**所有偏移全变**。
   所以路 2 的脚本必须**按原文定位**，不能写死偏移。

---

## 六、相关文档

- 仓库根 `README.md` —— 汉化包的用户说明、安装方法、附录（含各技术专题）
- `packing/` —— 打包产物清单与使用说明
- 备份位置：`E:\TAML\_scratch\hd2\` 下的 `hud-backup/`、`stale-patches-backup/`、`arsenal-backup/`
