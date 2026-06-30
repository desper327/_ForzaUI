# -*- coding: utf-8 -*-
"""
FTableView + Delegate 的 MVC 学习示例（薄版）

使用 forza_ui.table 库组件，保留 MVC 两层 Model 教学要点。
完整能力演示见: examples/table_full/

运行:
    python examples/mvc_table_example.py
"""

from __future__ import annotations

from dataclasses import dataclass

import _bootstrap  # noqa: F401

from Qt import QtCore, QtGui, QtWidgets

from forza_ui import forza_theme
from forza_ui.basic.label import FLabel
from forza_ui.delegates.button_delegate import FButtonDelegate
from forza_ui.display.item_view import FTableView
from forza_ui.utils import application
from forza_ui.input.push_button import FPushButton
from forza_ui.table import (
    ColumnDef,
    FSchemaTableModel,
    parse_column_schema,
)
from forza_ui.delegates.registry import register_column_delegates

# =============================================================================
# 领域层 — 纯 Python
# =============================================================================


@dataclass
class AssetRow:
    name: str
    asset_type: str
    enabled: bool = True
    count: int = 1
    status: str = "待开始"
    due_date: QtCore.QDate | None = None

    def __post_init__(self) -> None:
        if self.due_date is None:
            self.due_date = QtCore.QDate.currentDate().addDays(7)


ASSET_TYPE_OPTIONS = ["相机", "角色", "场景", "特效", "灯光"]


@dataclass
class AssetTableState:
    rows: list[AssetRow]
    asset_type_options: list[str] | None = None
    project_name: str = "DemoProject"

    def __post_init__(self) -> None:
        if self.asset_type_options is None:
            self.asset_type_options = list(ASSET_TYPE_OPTIONS)


COLUMN_SCHEMA: list[ColumnDef] = parse_column_schema(
    [
        {"key": "name", "title": "名称", "cell_type": "text", "editable": True},
        {"key": "asset_type", "title": "类型", "cell_type": "combo", "editable": True, "options_from": "asset_type_options"},
        {"key": "enabled", "title": "启用", "cell_type": "check", "editable": True},
        {"key": "count", "title": "数量", "cell_type": "spin", "editable": True, "min": 0, "max": 999},
        {"key": "due_date", "title": "截止日期", "cell_type": "date", "editable": True},
        {"key": "status", "title": "状态", "cell_type": "badge", "editable": False, "badge_policy": "status"},
        {"key": "action", "title": "操作", "cell_type": "button", "editable": False, "button_label": "删除", "button_type": "danger"},
    ]
)


class StatusColorPolicy:
    _MAP = {
        "完成": ("#1a3d2e", "#52c41a"),
        "进行中": ("#3d2e1a", "#faad14"),
        "待开始": ("#2a2a2a", "#8c8c8c"),
    }
    _DEFAULT = ("#2a2a2a", "#d9d9d9")

    def colors_for(self, status: str) -> tuple[QtGui.QColor, QtGui.QColor]:
        bg_hex, fg_hex = self._MAP.get(status, self._DEFAULT)
        return QtGui.QColor(bg_hex), QtGui.QColor(fg_hex)


# =============================================================================
# MVC Model — GlobalModel + FSchemaTableModel（库提供 Qt 适配层）
# =============================================================================


class GlobalModel(QtCore.QObject):
    def __init__(self, state: AssetTableState | None = None, parent=None):
        super().__init__(parent)
        self._state = state or AssetTableState(
            rows=[
                AssetRow("Camera_A", "相机", True, 2, "完成"),
                AssetRow("Char_Hero", "角色", True, 1, "进行中"),
                AssetRow("Env_City", "场景", False, 5, "待开始"),
            ]
        )
        self._table_model = FSchemaTableModel(
            schema=COLUMN_SCHEMA,
            rows=lambda: self._state.rows,
            context=lambda: self._state,
            parent=self,
        )

    @property
    def state(self) -> AssetTableState:
        return self._state

    @property
    def table_model(self) -> FSchemaTableModel:
        return self._table_model

    def append_row(self, row: AssetRow) -> None:
        self._table_model.append_row(row)


# =============================================================================
# View — 被动面板
# =============================================================================


class AssetTablePanel(QtWidgets.QWidget):
    add_row_requested = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        hint = FLabel(
            "薄版 MVC 示例：FSchemaTableModel + configure_table_view。"
            "完整搜索/过滤/分页见 examples/table_full/"
        ).secondary()
        hint.setWordWrap(True)

        self._table = FTableView()
        self._table.setMinimumHeight(220)
        self._table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self._table.setEditTriggers(
            QtWidgets.QAbstractItemView.DoubleClicked
            | QtWidgets.QAbstractItemView.SelectedClicked
        )
        self._delegates = register_column_delegates(
        self._table,
        COLUMN_SCHEMA,
        badge_policies={"status": StatusColorPolicy()},
        )

        add_btn = FPushButton("添加一行").primary()
        add_btn.clicked.connect(self.add_row_requested.emit)
        self._status_label = FLabel("Ready").secondary()

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(hint)
        layout.addWidget(self._table)
        layout.addWidget(add_btn)
        layout.addWidget(self._status_label)

    def button_delegate(self) -> FButtonDelegate:
        return self._delegates["action"]

    def set_model(self, model: QtCore.QAbstractItemModel) -> None:
        self._table.setModel(model)

    def set_status(self, text: str) -> None:
        self._status_label.setText(text)


# =============================================================================
# Controller
# =============================================================================


class AssetTableController(QtCore.QObject):
    def __init__(self, panel: AssetTablePanel, model: GlobalModel, parent=None):
        super().__init__(parent)
        self._panel = panel
        self._model = model

        self._panel.set_model(model.table_model)
        self._panel.button_delegate().clicked.connect(self._on_delete_row)
        model.table_model.cell_edited.connect(self._on_cell_edited)
        panel.add_row_requested.connect(self._on_add_row)
        self._sync_status("已加载")

    def _sync_status(self, prefix: str) -> None:
        rows = self._model.state.rows
        summary = " | ".join(f"{r.name}/{r.status}" for r in rows)
        self._panel.set_status(f"{prefix} — [{self._model.state.project_name}] [{summary}]")

    def _on_cell_edited(self, row_index: int, field_key: str, new_value: object) -> None:
        if field_key == "asset_type":
            row = self._model.state.rows[row_index]
            if row.status == "待开始":
                row.status = "进行中"
                self._model.table_model.notify_row_changed(row_index, "status")
        self._sync_status(f"第 {row_index + 1} 行.{field_key} → {new_value!r}")

    def _on_delete_row(self, index: QtCore.QModelIndex) -> None:
        row_index = index.row()
        rows = self._model.state.rows
        if 0 <= row_index < len(rows):
            name = rows[row_index].name
            self._model.table_model.remove_row(row_index)
            self._sync_status(f"已删除 {name}")

    def _on_add_row(self) -> None:
        n = len(self._model.state.rows) + 1
        self._model.append_row(AssetRow(f"Asset_{n:02d}", "特效", True, 1, "待开始"))
        self._sync_status(f"已添加 Asset_{n:02d}")


class MvcTableExampleWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("forza_ui MVC Table Example (thin)")
        self.resize(960, 480)
        self._model = GlobalModel(parent=self)
        panel = AssetTablePanel()
        AssetTableController(panel, self._model, self)
        self.setCentralWidget(panel)


def main() -> None:
    with application() as app:
        window = MvcTableExampleWindow()
        forza_theme.apply(window)
        window.show()
        if QtWidgets.QApplication.instance() is app:
            app.exec()


if __name__ == "__main__":
    main()
