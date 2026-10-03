# tools —— 构建与校验脚本

这些脚本是 HD2 汉化包的构建工具链，全部为 Python 3，无第三方依赖（标准库 + 自带的 `cn_strings` 词表）。

## 前置

- Python 3.8+
- HD2 Arsenal 已安装（脚本通过 `%LOCALAPPDATA%\hd2arsenal\mods` 定位模组库）
- 游戏 data 目录默认 `C:\SteamLibrary\steamapps\common\Helldivers 2\data`；若在别处，设置环境变量：

```powershell
$env:HD2_DATA = "D:\Steam\steamapps\common\Helldivers 2\data"
```

## 核心脚本

| 脚本 | 用途 |
| --- | --- |
| `hd2_patch.py` | **核心库**：HD2 Stingray patch 文件的读写与校验（头部/entry 记录/资源 ID） |
| `cn_strings.py` | 110 条英文 → 中文词表 |
| `build_packs2.py` | **构建两个发布包**：零冲突主包 + Transmog 可选包（当前方案） |
| `build_pack.py` | 早期版本：构建含 Transmog 覆盖副本的单包 |
| `build_cn.py` | 早期版本：直接改写上游模组文件的汉化方案（已被独立包取代） |
| `apply_cn_menu.py` / `apply_cn_transmog.py` | 早期覆盖式方案的施加脚本（保留作历史参考） |
| `restore_hd2_cn.py` | 把备份还原回模组库与游戏 data 目录 |
| `hd2_extreme2.py` | 极端场景测试（真实 Lua 执行） |

> 日志默认写到脚本同级 `notes\` 目录，备份写到 `backup\` 目录。

## 说明

早期脚本（`build_cn.py`、`apply_cn_*.py`）对应的是「直接改写上游模组文件」的旧方案，
现已被**独立汉化包**取代 —— 见仓库根目录 `README.md` 的附录四、五。
