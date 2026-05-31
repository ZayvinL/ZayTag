# ZayTag — Nuke Path Label System / Nuke 路径标签系统

> A production-ready file browser and path management tool for [Nuke](https://www.foundry.com/products/nuke). — 面向 Nuke 的生产级文件浏览器与路径管理工具。

Tag your project paths with tokens, browse renders with sequence-aware views, and drag files directly into the node graph.
用令牌标记项目路径，以序列感知视图浏览渲染文件，拖拽即可导入节点图。

Compatible with **Nuke 13 – 16+** and both **PySide2 & PySide6**. / 兼容 Nuke 13–16+，同时支持 PySide2 和 PySide6。

---

## Screenshot / 截图

![screenshot](screenshot.png)

---

## Features / 功能特性

- **Path Templating / 路径模板** — Use `{0} {1} {2} ...` placeholders in path templates. Sample tokens from Read nodes or the script path via sampling rules. 使用 `{0}{1}{2}` 占位符，通过采样规则从 Read 节点或工程路径提取令牌。
- **Path Packs / 路径设定包** — JSON-based per-project path configurations. Create multiple preset groups per pack. 基于 JSON 的按项目路径配置，每个包可创建多个预设组。
- **Three View Modes / 三种浏览模式**
  - *Tree / 树* — Traditional folder tree with green-dot markers on directories containing files. 传统文件夹树，含文件的目录带绿色圆点标记。
  - *All Files / 所有文件* — Flat recursive file list. 扁平递归文件列表。
  - *Sequences / 序列整理* — Auto-group frame sequences into single entries with frame range and missing-frame detection. 自动合并帧序列，显示帧范围与缺失帧。
- **Drag & Drop / 拖拽导入** — Drag files/sequences from any view into the Nuke Node Graph to create Read nodes. 从任意视图拖拽文件到 Nuke 节点图创建 Read。
- **Right-Click Menu / 右键菜单** — Copy path, open in explorer, import as Read, expand/collapse folders, expand-to-files. 复制路径、在资源管理器打开、作为 Read 导入、展开/闭合文件夹、展开到文件。
- **Keyboard Shortcuts / 快捷键**
  - `Alt+1` — Sample from selected Read node / 从选中 Read 节点获取
  - `Alt+2` — Sample from script path / 从工程路径获取
  - `C` — Copy selected path / 复制选中路径
  - `F` — Expand to files (tree) / Open folder (flat) / 展开到文件 / 打开目录
- **Dark UI / 暗色界面** — Warm amber theme matching Nuke's native style. 暖琥珀色调，匹配 Nuke 原生风格。
- **Built-in Help Page / 内置帮助页面** — Bilingual (Chinese/English). 中英双语。

---

## Installation / 安装

```bash
# Clone into your .nuke directory / 克隆到 .nuke 目录
cd ~/.nuke
git clone https://github.com/ZayvinL/ZayTag.git ZaneTpack/pipline_FolderPath
```

Add to `~/.nuke/init.py` or `~/.nuke/ZaneTpack/init.py` / 添加到 Nuke 启动脚本：

```python
import nuke
nuke.pluginAddPath("./ZaneTpack/pipline_FolderPath")
```

Restart Nuke. Find **ZayTag > 路径标签系统** in the Nodes toolbar menu.
重启 Nuke，在节点工具栏菜单中找到 **ZayTag > 路径标签系统**。

---

## Usage / 使用指南

### 1. Sample Path Tokens / 采样路径令牌
Select a Read node and press `Alt+1` (or click **从Read获取**). The sampling rule extracts path layers — e.g. `ProjA,EP01,SH001`.
选中 Read 节点按 `Alt+1`（或点击从Read获取），采样规则提取路径层级。

### 2. Set Up Path Templates / 设置路径模板
In the **路径集合** tab, add search paths using `{0}{1}{2}` placeholders:
在路径集合页面添加查找路径：

```
E:/projects/{0}/{1}/{2}/renders/
```

### 3. Open File Browser / 打开文件浏览器
Check the paths you need and click a preset in the left panel. File browser tabs are generated automatically.
勾选需要的路径，点击左侧预设即可生成文件浏览器标签页。

### 4. Browse & Import / 浏览与导入
Switch between Tree / All Files / Sequences via the dropdown. Right-click or use shortcuts. Drag files directly into the Node Graph.
通过下拉菜单切换浏览模式，右键或快捷键操作，拖拽文件到节点图。

### Sampling Rule Format / 采样规则格式
Rules define how a file path is split into tokens. 规则定义如何拆分路径：

```
*/*-1*_*0,*/*-1*_*1,*/*-1*_*2
```

| Symbol / 符号 | Meaning / 含义 |
|---|---|
| `*` | Separator between operations / 操作分隔符 |
| `symbol*N` | Split by symbol, take position N / 按符号拆分，取第 N 位 |
| `@` | Special: take characters by position / 特殊：按字符位取值 |

---

## Project Structure / 项目结构

```
pipline_FolderPath/
├── ZayTagPath.py         # Backward-compat entry point / 向后兼容入口
├── ZayWPanel.py          # Main window: path packs, sampling, tabs / 主窗口
├── tree_widgets.py       # Tree view, flat list, folder delegate, drag / 树与列表控件
├── ZaySplit.py           # String splitting for path parsing / 字符串拆分工具
├── _qt.py                # PySide2 / PySide6 compatibility layer / Qt 兼容层
├── CurrentPath.py        # Path resolution helpers / 路径解析辅助
├── RWJson.py             # JSON read/write with Nuke version handling / JSON 读写
├── menu.py               # Nuke menu registration / Nuke 菜单注册
├── SampleRuler.json      # Sample ruler configuration / 采样规则配置
├── PathPackSet/          # Runtime JSON data store for path packs / 路径包数据
└── README.md
```

---

## Requirements / 运行环境

- Nuke 13.0+
- PySide2 or PySide6（bundled with Nuke / 随 Nuke 自带）

No external Python packages required. / 无需额外 Python 包。

---

## Credits / 致谢

- **Author / 作者：** Zayvin (Lenden)
- **Original concept / 原始概念：** Mr.Cheese

## License / 许可

MIT
