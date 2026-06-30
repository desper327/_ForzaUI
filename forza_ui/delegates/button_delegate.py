# -*- coding: utf-8 -*-
"""Action button column delegate; emits clicked(index) without writing the model."""

from __future__ import annotations

from Qt import QtCore, QtGui, QtWidgets

from forza_ui.delegates.base import DelegateRole, FItemDelegateBase
from forza_ui.input.push_button import FPushButton


class FButtonDelegate(FItemDelegateBase):
    """Read-only action column that paints FPushButton and emits clicked(index)."""

    clicked = QtCore.Signal(QtCore.QModelIndex)

    def __init__(
        self,
        button_type_role: int = DelegateRole.ButtonTypeRole,
        default_fui_type: str = FPushButton.DefaultType,
        fui_size: int | None = None,
        cell_margin: int = 4,
        parent=None,
    ):
        super().__init__(
            fui_size=fui_size,
            cell_margin=cell_margin,
            single_click_edit=False,
            parent=parent,
        )
        self._button_type_role = button_type_role
        self._default_fui_type = default_fui_type

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> None:
        self.paint_selection_background(painter, option)
        text = index.data(QtCore.Qt.DisplayRole) or ""
        fui_type = index.data(self._button_type_role) or self._default_fui_type
        FPushButton.paint_appearance(
            painter,
            self.content_rect(option),
            str(text),
            fui_size=self.resolved_fui_size(),
            enabled=self.is_enabled(option),
            fui_type=fui_type,
        )

    def editorEvent(
        self,
        event: QtCore.QEvent,
        model: QtCore.QAbstractItemModel,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> bool:
        if not self.is_enabled(option):
            return False
        if (
            event.type() == QtCore.QEvent.MouseButtonRelease
            and event.button() == QtCore.Qt.LeftButton
        ):
            self.clicked.emit(index)
            return True
        return super().editorEvent(event, model, option, index)
