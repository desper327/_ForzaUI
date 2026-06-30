# -*- coding: utf-8 -*-
"""Task overview tab — table + toolbar."""

from __future__ import annotations

from Qt import QtWidgets

from forza_ui.basic.label import FLabel
from forza_ui.input.push_button import FPushButton
from forza_ui.table import FTableViewSet


class TaskOverviewPage(QtWidgets.QWidget):
    def __init__(self, view_set: FTableViewSet, parent=None):
        super().__init__(parent)
        self._view_set = view_set

        hint = FLabel(
            "YAML 配置驱动列 | 进度 Delegate | 点击「详情」打开抽屉 | "
            "搜索 + 客户端分页"
        ).secondary()
        hint.setWordWrap(True)

        self._add_btn = FPushButton("添加一行").primary()
        self._status_label = FLabel("Ready").secondary()

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(hint)
        layout.addWidget(view_set, 1)
        layout.addWidget(self._add_btn)
        layout.addWidget(self._status_label)

    @property
    def view_set(self) -> FTableViewSet:
        return self._view_set

    @property
    def add_button(self) -> FPushButton:
        return self._add_btn

    def set_status(self, text: str) -> None:
        self._status_label.setText(text)
