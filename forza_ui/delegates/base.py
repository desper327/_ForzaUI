# -*- coding: utf-8 -*-
"""Shared base class and ItemDataRole constants for forza_ui delegates."""

from __future__ import annotations

from Qt import QtCore, QtGui, QtWidgets

from forza_ui import forza_theme


class DelegateRole:
    """Shared roles between QAbstractItemModel and F* delegates."""

    OptionsRole = QtCore.Qt.UserRole + 2
    MinRole = QtCore.Qt.UserRole + 3
    MaxRole = QtCore.Qt.UserRole + 4
    StepRole = QtCore.Qt.UserRole + 5
    DisplayFormatRole = QtCore.Qt.UserRole + 6
    ButtonTypeRole = QtCore.Qt.UserRole + 7
    ProgressStatusRole = QtCore.Qt.UserRole + 8


class FItemDelegateBase(QtWidgets.QStyledItemDelegate):
    """Common margin, fui_size, selection paint, and editor geometry."""

    def __init__(
        self,
        fui_size: int | None = None,
        cell_margin: int = 3,
        single_click_edit: bool = False,
        parent=None,
    ):
        super().__init__(parent)
        self._fui_size = fui_size
        self._cell_margin = cell_margin
        self._single_click_edit = single_click_edit

    def resolved_fui_size(self) -> int:
        return self._fui_size if self._fui_size is not None else forza_theme.medium

    def content_rect(self, option: QtWidgets.QStyleOptionViewItem) -> QtCore.QRect:
        m = self._cell_margin
        return option.rect.adjusted(m, m, -m, -m)

    def paint_selection_background(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionViewItem,
    ) -> None:
        if option.state & QtWidgets.QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())

    def is_enabled(self, option: QtWidgets.QStyleOptionViewItem) -> bool:
        return bool(option.state & QtWidgets.QStyle.State_Enabled)

    def open_editor_on_click(
        self,
        event: QtCore.QEvent,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> bool:
        if not self._single_click_edit:
            return False
        if (
            event.type() == QtCore.QEvent.MouseButtonRelease
            and event.button() == QtCore.Qt.LeftButton
            and option.widget is not None
        ):
            view = option.widget
            if not view.isPersistentEditorOpen(index):
                view.edit(index)
            return True
        return False

    def updateEditorGeometry(
        self,
        editor: QtWidgets.QWidget,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> None:
        editor.setGeometry(option.rect)
