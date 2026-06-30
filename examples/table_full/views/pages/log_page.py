# -*- coding: utf-8 -*-
"""Runtime log tab."""

from __future__ import annotations

from Qt import QtCore, QtWidgets

from forza_ui.basic.label import FLabel
from forza_ui.input.push_button import FPushButton
from forza_ui.input.text_edit import FTextEdit


class LogPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._log = FTextEdit()
        self._log.setReadOnly(True)

        clear_btn = FPushButton("清空日志")
        clear_btn.clicked.connect(self._log.clear)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.addWidget(FLabel("运行记录").h4())
        layout.addWidget(self._log, 1)
        layout.addWidget(clear_btn)

    def append_line(self, message: str) -> None:
        stamp = QtCore.QDateTime.currentDateTime().toString("HH:mm:ss")
        self._log.append(f"[{stamp}] {message}")
