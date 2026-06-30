# -*- coding: utf-8 -*-
"""Pagination UI widget (pure Qt signals, no FieldMixin)."""

from __future__ import annotations

import math

from Qt import QtCore, QtWidgets

from forza_ui import forza_theme
from forza_ui.basic.label import FLabel
from forza_ui.input.combo_box import FComboBox
from forza_ui.input.spin_box import FSpinBox
from forza_ui.input.tool_button import FToolButton
from forza_ui.navigation.menu import FMenu


def _total_pages(total: int, page_size: int) -> int:
    if page_size <= 0:
        return 0
    return max(1, int(math.ceil(total / page_size))) if total > 0 else 1


def _display_text(current: int, page_size: int, total: int) -> str:
    if total <= 0:
        return "0 - 0 of 0"
    start = (current - 1) * page_size + 1 if current else 0
    end = min(total, current * page_size)
    return f"{start} - {end} of {total}"


class FPage(QtWidgets.QWidget):
    """Pagination bar; emits page_changed(page_size, current_page)."""

    page_changed = QtCore.Signal(int, int)

    DEFAULT_PAGE_SIZES = [10, 25, 50, 100]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._total = 0
        self._page_size = 25
        self._current_page = 1

        self._display_label = FLabel()
        self._display_label.setAlignment(QtCore.Qt.AlignCenter)

        self._page_size_menu = FMenu(parent=self)
        self._page_size_combo = FComboBox().small()
        self._page_size_combo.set_menu(self._page_size_menu)
        self._page_size_combo.set_formatter(lambda value: f"{value} / page")

        self._prev_button = FToolButton().icon_only().svg("left_fill.svg").small()
        self._next_button = FToolButton().icon_only().svg("right_fill.svg").small()
        self._page_spin = FSpinBox()
        self._page_spin.setMinimum(1)
        self._page_spin.set_fui_size(forza_theme.small)
        self._total_page_label = FLabel("1")

        self._prev_button.clicked.connect(lambda: self._change_page(-1))
        self._next_button.clicked.connect(lambda: self._change_page(1))
        self._page_spin.valueChanged.connect(self._on_page_spin_changed)
        self._page_size_combo.sig_value_changed.connect(self._on_page_size_changed)

        self.set_page_sizes(self.DEFAULT_PAGE_SIZES)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.addStretch()
        layout.addWidget(self._display_label)
        layout.addStretch()
        layout.addWidget(FLabel("|").secondary())
        layout.addWidget(self._page_size_combo)
        layout.addWidget(FLabel("|").secondary())
        layout.addWidget(self._prev_button)
        layout.addWidget(FLabel("Page"))
        layout.addWidget(self._page_spin)
        layout.addWidget(FLabel("/"))
        layout.addWidget(self._total_page_label)
        layout.addWidget(self._next_button)

        self._refresh_ui()

    def set_page_sizes(self, sizes: list[int]) -> None:
        data = [{"label": str(size), "value": size} for size in sizes]
        self._page_size_menu.set_data(data)
        if self._page_size not in sizes:
            self._page_size = sizes[0] if sizes else 25
        self._page_size_combo.set_value(self._page_size)

    def set_total(self, total: int, *, reset_page: bool = True) -> None:
        self._total = max(0, total)
        if reset_page:
            self._current_page = 1
        self._refresh_ui()

    def current_page(self) -> int:
        return self._current_page

    def page_size(self) -> int:
        return self._page_size

    def _refresh_ui(self) -> None:
        total_page = _total_pages(self._total, self._page_size)
        if self._current_page > total_page:
            self._current_page = total_page
        if self._current_page < 1:
            self._current_page = 1

        self._display_label.setText(
            _display_text(self._current_page, self._page_size, self._total)
        )
        self._page_spin.blockSignals(True)
        self._page_spin.setMaximum(max(1, total_page))
        self._page_spin.setValue(self._current_page)
        self._page_spin.blockSignals(False)
        self._total_page_label.setText(str(total_page))
        self._prev_button.setEnabled(self._current_page > 1)
        self._next_button.setEnabled(self._current_page < total_page and self._total > 0)

    def _emit_page_changed(self) -> None:
        self.page_changed.emit(self._page_size, self._current_page)

    def _change_page(self, offset: int) -> None:
        self._current_page = max(1, self._current_page + offset)
        self._refresh_ui()
        self._emit_page_changed()

    def _on_page_spin_changed(self, value: int) -> None:
        if value != self._current_page:
            self._current_page = value
            self._refresh_ui()
            self._emit_page_changed()

    def _on_page_size_changed(self, value) -> None:
        self._page_size = int(value)
        self._current_page = 1
        self._refresh_ui()
        self._emit_page_changed()
