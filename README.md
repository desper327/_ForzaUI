# forza_ui

纯 **View 层** Qt 控件库，基于 [dayu_widgets](https://github.com/phenom-films/dayu_widgets) 改造而来。  
采用 Ant Design 风格，内置图标资源，不包含 `FieldMixin`，也不内置数据模型。

面向 [Forza_Tray](../../Forza_Tray) 等 MVC 应用：View 发出语义化信号，Controller 通过 setter 推送状态。

## 安装 / 路径

需要把 Forza 的 **Qt 兼容层**（`Qt.py`）和本包根目录加入 `sys.path`：

```python
import sys
sys.path.insert(0, r".../ForzaPipeline/Forza_Lib/vendor")
sys.path.insert(0, r".../ForzaPipeline/Forza_Lib/forza_ui")
```

## 快速开始

```python
from forza_ui import forza_theme, FPushButton, FLineEdit
from Qt.QtWidgets import QApplication, QWidget, QVBoxLayout
import sys

app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout(window)
layout.addWidget(FPushButton("Launch").primary())
layout.addWidget(FLineEdit().medium())
forza_theme.apply(window)
window.show()
app.exec()
```

## 目录结构

组件按用途放在不同文件夹，在 IDE 里展开 `forza_ui/` 即可浏览：

```
forza_ui/
├── theme.py          # 主题
├── icons.py          # 图标
├── mixin.py          # 装饰器 mixin
├── utils.py          # 工具函数
├── static/           # QSS、SVG 资源
│
├── basic/            # 基础展示
│   ├── label.py          FLabel
│   ├── divider.py        FDivider
│   ├── avatar.py         FAvatar
│   └── badge.py          FBadge
│
├── input/            # 输入与操作
│   ├── push_button.py    FPushButton
│   ├── tool_button.py    FToolButton
│   ├── line_edit.py      FLineEdit
│   ├── text_edit.py      FTextEdit
│   ├── combo_box.py      FComboBox
│   ├── check_box.py      FCheckBox
│   ├── radio_button.py   FRadioButton
│   ├── switch.py         FSwitch
│   ├── slider.py         FSlider
│   ├── spin_box.py       FSpinBox / FDateEdit / …
│   ├── button_group.py   FPushButtonGroup / FRadioButtonGroup / …
│   └── completer.py      FCompleter
│
├── display/          # 数据展示（需自备 Model）
│   ├── item_view.py      FTableView / FTreeView / FListView / FBigView
│   ├── card.py           FCard / FMeta
│   ├── carousel.py       FCarousel
│   └── header_view.py    FHeaderView
│
├── delegates/        # 表格/树形列 Delegate（独立于 display）
│   ├── base.py               FItemDelegateBase, DelegateRole
│   ├── combo_delegate.py     FComboDelegate
│   ├── line_edit_delegate.py FLineEditDelegate
│   ├── spin_delegate.py      FSpinDelegate
│   ├── check_delegate.py     FCheckDelegate
│   ├── switch_delegate.py    FSwitchDelegate
│   ├── date_delegate.py      FDateDelegate
│   ├── badge_delegate.py     FBadgeDelegate (+ BadgeColorPolicy)
│   ├── button_delegate.py    FButtonDelegate
│   └── registry.py           register_column_delegates
│
├── table/            # 表格 MVC 数据管道（Qt 适配层，非业务 Model）
│   ├── schema.py               列配置 load_column_schema
│   ├── schema_table_model.py   FSchemaTableModel
│   ├── search_page.py          FSearchProxyModel / FPageSliceProxyModel
│   └── table_set.py            FTableViewSet / configure_table_view
│
├── navigation/       # 导航与结构
│   ├── tab_widget.py         FTabWidget
│   ├── line_tab_widget.py    FLineTabWidget
│   ├── menu_tab_widget.py    FMenuTabWidget
│   ├── collapse.py           FCollapse
│   ├── menu.py               FMenu
│   ├── page.py               FPage（分页条 UI）
│   └── drawer.py             FDrawer
│
├── feedback/         # 反馈与状态
│   ├── alert.py            FAlert
│   ├── message.py          FMessage
│   ├── toast.py            FToast
│   ├── loading.py          FLoading / FLoadingWrapper
│   ├── progress_bar.py     FProgressBar
│   └── progress_circle.py  FProgressCircle
│
└── layout/           # 布局与容器
    ├── flow_layout.py      FFlowLayout
    ├── splitter.py         FSplitter
    ├── dock_widget.py      FDockWidget
    ├── stacked_widget.py   FStackedWidget
    └── popup.py            FPopup
```

### 导入方式

```python
# 方式 1：从根包导入（常用控件已汇总）
from forza_ui import FPushButton, FLineEdit, FAlert

# 方式 2：从分类文件夹导入（更明确）
from forza_ui.input.line_edit import FLineEdit
from forza_ui.feedback.alert import FAlert
from forza_ui.display.card import FCard
```

### 场景速查

| 我想做… | 去哪个文件夹 | 推荐控件 |
|---------|-------------|----------|
| 设置/偏好面板 | `input/` + `basic/` | `FLabel` `FLineEdit` `FComboBox` `FCheckBox` `FSwitch` `FPushButton` |
| 表单提交 | `input/` | `FLineEdit` `FComboBox` `FRadioButtonGroup` `FPushButton` |
| 工具栏 | `input/` + `navigation/` | `FToolButton` `FToolButtonGroup` `FMenu` |
| 表格浏览数据 | `table/` + `display/` | `FTableViewSet` 或 `FSchemaTableModel` + `configure_table_view` |
| 树形目录 | `display/` | `FTreeView` + 自备 Model |
| 卡片信息流 | `display/` + `basic/` | `FCard` `FMeta` `FAvatar` `FBadge` |
| 多面板切换 | `navigation/` | `FTabWidget` / `FLineTabWidget` / `FCollapse` |
| 操作结果提示 | `feedback/` | `FAlert`（页内） / `FMessage`（顶部） / `FToast`（居中） |
| 异步等待 | `feedback/` | `FLoading` `FLoadingWrapper` `FProgressBar` |

## MVC 约定

| 层级 | 职责 |
|------|------|
| **forza_ui `F*` 控件** | 带样式的控件；使用标准 Qt 信号（`clicked`、`textChanged` 等） |
| **你的 View 面板** | 组合控件；暴露 `*_requested` 信号；提供 `set_*` / `update_*` 方法 |
| **Controller** | `SignalBinder.bind(view.signal, slot)`；读写 Model；调用 View 的 setter |

完整示例见 `examples/mvc_panel_example.py`（被动 View + Controller）。

表格薄版示例见 `examples/mvc_table_example.py`（`FSchemaTableModel` + 两层 MVC）。

完整表格（YAML + 搜索/过滤/分页）见 `examples/table_full/main.py`。

### 表格 `forza_ui/table/`（5 文件）

| 文件 | API |
|------|-----|
| `schema.py` | `load_column_schema`, `ColumnDef` |
| `schema_table_model.py` | `FSchemaTableModel` |
| `search_page.py` | `FSearchProxyModel`, `FPageSliceProxyModel` |
| `table_set.py` | `FTableViewSet`, `configure_table_view` |

```python
from forza_ui import FTableViewSet, FSchemaTableModel, load_column_schema

schema = load_column_schema("assets_table.yaml")
model = FSchemaTableModel(schema, rows=lambda: state.rows, context=lambda: state)
view_set = FTableViewSet(schema).searchable().paginated()
view_set.set_source_model(model)
```

### 表格 Delegate 套件（`forza_ui/delegates/`）

所有 Delegate 与对应 `F*` 控件样式一致（显示态 `paint_appearance`，编辑态真实控件）：

| Delegate | 列类型 | 对应控件 |
|----------|--------|----------|
| `FLineEditDelegate` | text | FLineEdit |
| `FComboDelegate` | combo | FComboBox |
| `FSpinDelegate` | spin / double | FSpinBox / FDoubleSpinBox |
| `FCheckDelegate` | check | FCheckBox |
| `FSwitchDelegate` | switch | FSwitch |
| `FDateDelegate` | date / datetime / time | FDateEdit 等 |
| `FBadgeDelegate` | badge | 只读徽章（可注入 ColorPolicy） |
| `FButtonDelegate` | button | FPushButton（emit clicked） |

```python
from forza_ui import FTableView, register_column_delegates, DelegateRole

register_column_delegates(
    table,
    schema=[
        {"key": "name", "cell_type": "text", "editable": True},
        {"key": "type", "cell_type": "combo", "editable": True},
    ],
    options_role=DelegateRole.OptionsRole,
)
```

完整演示见 `examples/mvc_table_example.py` 与 `examples/table_full/main.py`。

## 不包含内容

- `MFieldMixin` / 表单自动绑定
- dayu 的 `MTableModel`、浏览器/序列/db_path 等业务控件
- 替代应用层领域 Model 的「万能表格 Model」

## 示例

```bash
# 全组件学习示例（推荐先看这个，含详细中文注释）
python examples/demo.py

# MVC 模式示例（Forza_Tray 风格）
python examples/mvc_panel_example.py

# 表格薄版 MVC 示例
python examples/mvc_table_example.py

# 表格全面能力演示（YAML + 搜索/过滤/分页）
python examples/table_full/main.py
```

## 命名约定

- 控件类使用 `F*` 前缀，例如 `FPushButton`、`FLabel`
- QSS 动态属性使用 `fui_*` 前缀，例如 `fui_type`、`fui_size`、`fui_level`
- 对应 Python API 同样为 `fui_*`，例如：

```python
button.set_fui_type("primary")
button.set_fui_size(forza_theme.large)
label.set_fui_level(FLabel.H1Level)
```

## 可选：接入 Forza_Tray

在 `config/settings.py` 中添加：

```python
sys.path.append(os.path.join(FORZA_ROOT, "Forza_Lib", "forza_ui"))
```

然后将 View 中的原生 `QPushButton` / `QComboBox` 替换为 `FPushButton` / `FComboBox`，并在托盘窗口上调用 `forza_theme.apply()`。
