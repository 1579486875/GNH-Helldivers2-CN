# tools —— 构建与校验工具链

HD2 汉化包的完整工具链，全部是 Python 3 标准库，没有第三方依赖（测试脚本需要 `lupa`）。

## 前置

- Python 3.8+
- HD2 Arsenal 已安装（脚本通过 `%LOCALAPPDATA%\hd2arsenal\mods` 定位模组库）
- 游戏 data 目录默认 `C:\SteamLibrary\steamapps\common\Helldivers 2\data`，在别处就设置环境变量：

```powershell
$env:HD2_DATA = "D:\Steam\steamapps\common\Helldivers 2\data"
```

## 目录结构

```
tools/
├── lua_src/runtime_template.lua   ← 运行时汉化脚本的模板（带完整中文注释，可单独编译检查）
├── cn_*.py                        ← 词表分册（按批次）
├── cn_strings.py                  ← 合并后的总词表（由 merge_cn_fixed.py 生成，不要手改）
├── build_packs2.py                ← 构建两个发布包
├── extreme_test.py / perf_test.py / compat_check.py / verify_tm.py   ← 测试与校验
└── hd2_patch.py                   ← patch 容器读写库
```

## 一、构建链

| 脚本 | 用途 |
| --- | --- |
| `hd2_patch.py` | **核心库**：HD2 Stingray patch 的读写与校验（头部、entry 记录、资源 ID 哈希） |
| `cn_add.py` / `cn_desc.py` / `cn_fix.py` / `cn_mods.py` / `cn_mods2.py` / `cn_new.py` / `cn_ui3.py` / `cn_ui4.py` / `cn_ui5.py` | 词表分册，按加入时间分批，便于回溯"这条是谁加的、为什么加" |
| `merge_cn_fixed.py` | 把上面的分册合并成 `cn_strings.py`（**只取指定的字典变量**，避免把 Python 内置名混进词表） |
| `lua_src/runtime_template.lua` | 运行时脚本本体。`build_packs2.py` 只负责把词表填进 `--[[GNH_CN_TABLE]]` 占位符 |
| `build_packs2.py` | **构建两个发布包**：零冲突主包 + Transmog 可选包；生成后立刻做 Lua 语法自检 |
| `sync_dist.py` | 从 Arsenal 模组库取最新产物，重新打成分发 zip 并同步到所有分发位置 |

**改词表的标准流程**：

```powershell
# 1) 改某一个 cn_*.py，或新增一个分册并加进 merge_cn_fixed.py 的 SPEC
# 2) 合并
python merge_cn_fixed.py
# 3) 构建（会顺带做 Lua 语法自检；部署到游戏 data 也在这一步）
python build_packs2.py
# 4) 校验
python compat_check.py
python extreme_test.py
```

## 二、测试与校验

| 脚本 | 检查什么 |
| --- | --- |
| `compat_check.py` | Lua 5.1/LuaJIT 语法兼容性（禁用 5.2+ 专有写法）、保留字冲突、全局命名空间污染、编码卫生、patch 容器结构 |
| `extreme_test.py` | **25 个极端场景**：菜单不存在 / 结构异常（模拟上游改版）/ 只读表 / 上游抛异常 / 重复注册 / 重复加载 …… 全部用真实 Lua 运行时执行 |
| `perf_test.py`、`perf_exact.py` | 性能实测：加载开销、每帧开销、5000 选项、10000 次注册、词表查找、超长翻译保护 |
| `verify_tm.py` | **可选包专用**：逐行 diff 上游原始文件与汉化版，并统计 `==` / `~=` / `[]` 三类**判定语境**里的字面量有没有被改动（必须为 0） |
| `scan_ui2.py` | 覆盖率扫描：遍历各模组 Lua 源，提取注册到菜单的界面文本，列出词表里缺失的（能正确处理 `..` 跨行拼接） |
| `audit_cn.py` | 词表质量审计：控制字符、长度上限、与游戏内置原生词冲突、空值、未翻译项 |
| `test_pack_lua.py` | 端到端逻辑验证（补翻 + 实时翻译） |
| `dump_lua_all.py`、`dump_runtime.py` | 辅助：把各模组 Lua 源 dump 出来；只看主包脚本的代码部分（跳过几千行词表） |

## 三、词表说明

- 词表是 `英文原文 → 简体中文` 的纯字符串映射，键必须与被汉化模组注册时传入的字符串**逐字符一致**。
- 构建时会自动补一份**全大写**的键：菜单显示"选项值"和"模组名"时会先转成大写。
- 目前规模：**565 组**（含大写形式共 1074 条）。
- 单条长度有上限（选项名 64 字 / 选项值 48 字 / 说明 400 字 / 模组名 40 字）。
  运行时脚本里有一道**长度保护**：中文超长就自动回退英文，避免整个选项被上游拒绝注册。

### 刻意保留英文的内容（不是漏翻）

| 类别 | 例子 | 原因 |
| --- | --- | --- |
| 武器 / 载具型号 | `Flak36`、`Gau-19`、`M61`、`MG42`、`PKM`、`FRV` | 型号是代号，中文圈也用原文 |
| 护甲代号 | `A9`、`DP8`、`RS67` | 同上 |
| 模组专名 | `Castle ODST`、`HD2 HUD+` | 作者的品牌名 |
| 游戏内原生词 | `OFF` / `ON` / `LOW` / `DEFAULT` | 游戏自己会翻译，我们译反而可能和原生叫法不一致 |
| 源码注释里的 API 示例 | `Row text`、`Mod name`、`My Mod` | 只存在于注释或默认值里，不会上屏 |
| 开发者调试项 | `Probe A` / `Probe B` | 开发者用来标记探针变体的标识 |
| 测试版专用文本 | `Test build only. ...` | 作者自己标注"仅测试版"，正式版不显示 |

## 四、常见维护任务

**模组更新后要重新汉化？**
先跑 `scan_ui2.py` 看有没有新文本 → 补进某个 `cn_*.py` → 按上面的标准流程重跑即可。

**上游 ModOptionsMenu 大改版导致补翻失效？**
日志里会看到"第 1 次扫描：暂时没有需要补翻的条目"，但实时接管仍然有效。
这是**安全降级**：脚本不会报错、不会影响游戏，只是"已经注册进去的旧选项"翻不了。

**想确认某个选项为什么没被翻译？**
看 `%LOCALAPPDATA%\CowboyBingus\Helldivers2\Logs\GNHChinesePack.log`：
它会打印接管时刻、每一次补翻的数量、以及前 12 条翻译明细。
