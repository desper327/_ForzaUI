# -*- coding: utf-8 -*-
"""Application settings tab — passive view."""

from __future__ import annotations

from Qt import QtCore, QtWidgets

from forza_ui.basic.label import FLabel
from forza_ui.input.line_edit import FLineEdit
from forza_ui.input.spin_box import FSpinBox


class SettingsPage(QtWidgets.QWidget):
    project_name_changed = QtCore.Signal(str)
    default_page_size_changed = QtCore.Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._project_edit = FLineEdit()
        self._project_edit.setPlaceholderText("项目名称")

        self._page_size_spin = FSpinBox()
        self._page_size_spin.setRange(5, 100)

        form = QtWidgets.QFormLayout()
        form.setContentsMargins(16, 16, 16, 16)
        form.setSpacing(12)
        form.addRow(FLabel("项目名称").secondary(), self._project_edit)
        form.addRow(FLabel("默认每页行数").secondary(), self._page_size_spin)

        hint = FLabel(
            "修改后由 Controller 写入业务 Model.state；分页默认值在下次切换页大小时生效。"
        ).secondary()
        hint.setWordWrap(True)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(hint)
        layout.addStretch()

        self._project_edit.editingFinished.connect(self._emit_project_name)
        self._page_size_spin.valueChanged.connect(self._emit_page_size)

    def set_project_name(self, name: str) -> None:
        self._project_edit.blockSignals(True)
        self._project_edit.setText(name)
        self._project_edit.blockSignals(False)

    def set_default_page_size(self, page_size: int) -> None:
        self._page_size_spin.blockSignals(True)
        self._page_size_spin.setValue(page_size)
        self._page_size_spin.blockSignals(False)

    def _emit_project_name(self) -> None:
        text = self._project_edit.text().strip() or "DemoProject"
        self.project_name_changed.emit(text)

    def _emit_page_size(self, value: int) -> None:
        self.default_page_size_changed.emit(int(value))
