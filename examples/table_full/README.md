# Table Full Demo

全面展示 `forza_ui/table` 模块能力。

## 运行

```bash
cd ForzaPipeline/Forza_Lib/forza_ui
python examples/table_full/main.py
```

**深入阅读**（Model 链 / 搜索分页 / 排序 / 进度条）：

- [docs/table_full_model_chain解释.md](../../docs/table_full_model_chain解释.md)
- [docs/row_column_cell_index解释.md](../../docs/row_column_cell_index解释.md)

薄版 MVC 教学示例（无搜索/分页）：

```bash
python examples/mvc_table_example.py
```

## `forza_ui/table/` 模块结构（5 个文件）

| 文件 | 职责 | 常用 API |
|------|------|----------|
| `schema.py` | 列配置（YAML/JSON/TOML） | `load_column_schema`, `ColumnDef` |
| `schema_table_model.py` | Qt 适配 Model | `FSchemaTableModel` |
| `search_page.py` | 搜索 + 分页 Proxy | `FSearchProxyModel`, `FPageSliceProxyModel` |
| `table_set.py` | 表格组合件 + Delegate 配置 | `FTableViewSet`, `configure_table_view` |

分页 UI 控件 `FPage` 在 `forza_ui/navigation/page.py`，由 `FTableViewSet.paginated()` 自动组装。

## 心智模型（4 层 MVC）

```
1. 配置层   assets_table.yaml  →  load_column_schema()
2. 领域层   GlobalModel.state    （你的 MVC Model，唯一数据源）
3. 适配层   FSchemaTableModel    （库提供，投影 state.rows）
4. 视图层   AssetTableWindow     （被动 View：Tab + 抽屉，不含 Model）
           FTableViewSet         （由 Controller 创建并注入）
```

**MVC 接线（本示例）**：

```python
# main.py — 只创建 Model 与 Controller
model = GlobalModel()
controller = AssetTableController(model)
controller.window.show()

# Controller 内 — View 不 import GlobalModel
view_set = FTableViewSet(model.schema).searchable().paginated()
window = AssetTableWindow(view_set)
view_set.set_source_model(model.table_model)
settings.set_project_name(model.state.project_name)  # setter 灌数据
settings.project_name_changed.connect(controller._on_project_name_changed)  # 信号上报
```

**Model 链（本示例）**：

```
FSchemaTableModel → FSearchProxyModel → FPageSliceProxyModel → FTableView
```

## 我该 import 什么？

| 场景 | import |
|------|--------|
| 完整表格（搜索/分页） | `FTableViewSet`, `load_column_schema` |
| 简单 MVC 表格 | `FSchemaTableModel`, `configure_table_view` |
| 手动拼 Proxy 链 | `FSearchProxyModel`, `FPageSliceProxyModel` |
| 业务 Model | 自己写 `GlobalModel`（应用层，见 `models/`） |

## 能力清单

| 能力 | 实现 |
|------|------|
| 配置驱动 | `config/assets_table.yaml` + `load_column_schema` |
| MVC 两层 Model | `GlobalModel` + `FSchemaTableModel` |
| 全部 cell 类型 | text / combo / check / spin / date / badge / button / **progress** |
| 进度列 + 多线程 | `FProgressDelegate` + `RowTaskManager`（节流单格刷新） |
| 行详情抽屉 | 选中行 → `FDrawer` + `RowDetailPanel` |
| 应用 Tab 壳 | `FMenuTabWidget` + `FStackedWidget`（任务总览 / 设置 / 日志） |
| 搜索 | `FTableViewSet.searchable()` |
| 分页 | `FPage` + `FPageSliceProxyModel` |
| Badge 策略 | `policies/status_color.py` 注册表 |
| 业务规则 | Controller 监听 `cell_edited` / 任务信号 |

## 快速上手（核心代码）

```python
from forza_ui.table import FTableViewSet, load_column_schema

schema = load_column_schema("config/assets_table.yaml")
view_set = FTableViewSet(schema).searchable().paginated()
view_set.set_source_model(model.table_model)   # FSchemaTableModel
view_set.configure_delegates(badge_policies=BADGE_POLICIES)
view_set.cell_edited.connect(controller._on_cell_edited)
```

## 目录

```
table_full/
├── config/assets_table.yaml   # 列配置（Layer 1）
├── models/                    # 领域 Model + GlobalModel（Layer 2）
│   ├── asset_row.py           # AssetRow, AssetTableState
│   └── asset_model.py         # GlobalModel → FSchemaTableModel
├── policies/                  # Badge 配色策略（运行时注册表）
├── views/                     # 被动 View（FTableViewSet 组装）
├── controllers/               # Controller（业务规则）
└── main.py
```

## 与整个库的分工

| 包 | 职责 |
|----|------|
| `display/` | 纯样式 View（`FTableView`） |
| `delegates/` | 单元格渲染/编辑（`F*Delegate`） |
| `table/` | 数据管道（配置 → Model → Proxy → ViewSet） |
| `navigation/` | `FPage` 分页条 UI |

## 数据流说明

1. 用户编辑 cell → Delegate → `FSchemaTableModel.setData()` → 写入 `state.rows`
2. `FSchemaTableModel` emit `cell_edited` → Controller 执行业务规则
3. 搜索/分页只影响 View 可见行，**不修改** `state.rows`
4. Controller 删除行时：先用 `view_set.map_to_source(index)` 映射到 source row，再删 `state.rows`
5. 后台任务更新进度：子线程 emit → Controller 写 `row.progress` → `table_model.notify_row_changed(row, "progress")`
6. 任务控制列用 **button** Delegate（开始/取消），进度列用只读 **FProgressDelegate**

## 进度列 MVC 路径

```
QThread/Worker → RowTaskManager（节流）→ Controller
  → state.rows[i].progress = N
  → table_model.notify_row_changed(i, "progress")
  → FProgressDelegate.paint()
```

## Tab 与抽屉

- **任务总览**：`FTableViewSet`
- **设置**：`project_name`、`default_page_size`
- **日志**：`LogPage.append_line()`
- **行详情**：点击「详情」按钮 → `FDrawer` + `RowDetailPanel`

## 目录

```
table_full/
├── config/assets_table.yaml
├── models/
├── policies/
├── services/row_task_manager.py
├── views/
│   ├── asset_table_window.py
│   ├── row_detail_panel.py
│   └── pages/
├── controllers/
└── main.py
```
