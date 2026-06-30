# -*- coding: utf-8 -*-
"""
MVC 集成示例（对齐 Forza_Tray 模式）

View：被动面板，发出语义化信号，只提供 setter
Controller：绑定信号，根据 Model 状态更新 View

全组件用法演示见：examples/demo.py
"""

from __future__ import annotations

from dataclasses import dataclass

import _bootstrap  # noqa: F401

from Qt import QtCore, QtWidgets

from forza_ui import forza_theme
from forza_ui.input.combo_box import FComboBox
from forza_ui.utils import application
from forza_ui.basic.label import FLabel
from forza_ui.input.line_edit import FLineEdit
from forza_ui.input.push_button import FPushButton


@dataclass
class PanelState:#model
    theme: str = "dark"
    nickname: str = "Artist"


class ThemePanel(QtWidgets.QWidget):#view
    """Passive view: emits user intent, exposes setters for controller."""

    theme_change_requested = QtCore.Signal(str)
    nickname_change_requested = QtCore.Signal(str)
    save_requested = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._theme_combo = FComboBox().medium()
        self._nickname_edit = FLineEdit().medium()
        self._status_label = FLabel("Ready")
        save_btn = FPushButton("Save").primary()

        self._theme_combo.currentTextChanged.connect(self.theme_change_requested.emit)
        self._nickname_edit.editingFinished.connect(
            lambda: self.nickname_change_requested.emit(self._nickname_edit.text())
        )
        save_btn.clicked.connect(self.save_requested.emit)

        form = QtWidgets.QFormLayout(self)
        form.addRow(FLabel("Theme"), self._theme_combo)
        form.addRow(FLabel("Nickname"), self._nickname_edit)
        form.addRow(save_btn)
        form.addRow(self._status_label)

    def set_theme_options(self, options: list[str], current: str) -> None:
        self._theme_combo.blockSignals(True)
        self._theme_combo.clear()
        self._theme_combo.addItems(options)
        index = self._theme_combo.findText(current)
        if index >= 0:
            self._theme_combo.setCurrentIndex(index)
        self._theme_combo.blockSignals(False)

    def set_nickname(self, nickname: str) -> None:
        self._nickname_edit.blockSignals(True)
        self._nickname_edit.setText(nickname)
        self._nickname_edit.blockSignals(False)

    def set_status(self, text: str) -> None:
        self._status_label.setText(text)


class PanelController(QtCore.QObject):#controller
    def __init__(self, panel: ThemePanel, parent=None):
        super().__init__(parent)
        self._panel = panel
        self._state = PanelState()
        self._themes = ["dark", "light"]

        panel.theme_change_requested.connect(self._on_theme_change)
        panel.nickname_change_requested.connect(self._on_nickname_change)
        panel.save_requested.connect(self._on_save)
        self._sync_view()

    def _sync_view(self) -> None:
        self._panel.set_theme_options(self._themes, self._state.theme)
        self._panel.set_nickname(self._state.nickname)
        self._panel.set_status(f"theme={self._state.theme}, nickname={self._state.nickname}")

    def _on_theme_change(self, theme: str) -> None:
        self._state.theme = theme
        forza_theme.set_theme(theme)
        root = self._panel.window()
        if root:
            forza_theme.apply(root)
        self._panel.set_status(f"theme={self._state.theme}, nickname={self._state.nickname}")

    def _on_nickname_change(self, nickname: str) -> None:
        self._state.nickname = nickname.strip() or "Artist"
        self._panel.set_nickname(self._state.nickname)
        self._panel.set_status(f"theme={self._state.theme}, nickname={self._state.nickname}")

    def _on_save(self) -> None:
        self._panel.set_status(f"Saved: {self._state.nickname} @ {self._state.theme}")


class MvcExampleWindow(QtWidgets.QMainWindow):#main
    def __init__(self):
        super().__init__()
        self.setWindowTitle("forza_ui MVC Example")
        self.resize(480, 260)
        panel = ThemePanel()
        self._controller = PanelController(panel, self)
        self.setCentralWidget(panel)


def main() -> None:
    with application() as app:
        window = MvcExampleWindow()
        forza_theme.apply(window)
        window.show()
        if QtWidgets.QApplication.instance() is app:
            app.exec()


if __name__ == "__main__":
    main()
