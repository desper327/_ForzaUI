# -*- coding: utf-8 -*-
"""Read-only row detail form shown inside FDrawer."""

from __future__ import annotations

from Qt import QtCore, QtWidgets

from forza_ui.basic.label import FLabel

from models.asset_row import AssetRow


class RowDetailPanel(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._fields: dict[str, FLabel] = {}
        form = QtWidgets.QFormLayout(self)
        form.setContentsMargins(12, 8, 12, 8)
        form.setSpacing(10)
        for key, title in (
            ("name", "名称"),
            ("asset_type", "类型"),
            ("enabled", "启用"),
            ("count", "数量"),
            ("status", "状态"),
            ("progress", "进度"),
            ("task_state", "任务状态"),
            ("due_date", "截止日期"),
        ):
            value_label = FLabel("—")
            value_label.setWordWrap(True)
            self._fields[key] = value_label
            form.addRow(FLabel(title).secondary(), value_label)
        self.clear()

    def clear(self) -> None:
        for label in self._fields.values():
            label.setText("—")

    def set_row(self, row: AssetRow | None) -> None:
        if row is None:
            self.clear()
            return
        self._fields["name"].setText(row.name)
        self._fields["asset_type"].setText(row.asset_type)
        self._fields["enabled"].setText("是" if row.enabled else "否")
        self._fields["count"].setText(str(row.count))
        self._fields["status"].setText(row.status)
        self._fields["progress"].setText(f"{row.progress}%")
        self._fields["task_state"].setText(row.task_state)
        if row.due_date is not None:
            self._fields["due_date"].setText(row.due_date.toString("yyyy-MM-dd"))
        else:
            self._fields["due_date"].setText("—")
