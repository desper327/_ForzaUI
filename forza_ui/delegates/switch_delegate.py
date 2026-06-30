# -*- coding: utf-8 -*-
"""QStyledItemDelegate for FSwitch boolean columns."""

from __future__ import annotations

from Qt import QtCore, QtGui, QtWidgets

from forza_ui.delegates.base import FItemDelegateBase
from forza_ui.input.switch import FSwitch


class FSwitchDelegate(FItemDelegateBase):
    """Boolean column rendered as FSwitch; click toggles value."""

    def createEditor(self, parent, option, index):
        """Bool EditRole would otherwise open Qt's default QComboBox on double-click."""
        return None

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> None:
        self.paint_selection_background(painter, option)
        checked = self._is_checked(index)
        FSwitch.paint_appearance(
            painter,
            option.rect,
            checked,
            fui_size=self.resolved_fui_size(),
            enabled=self.is_enabled(option),
        )

    def editorEvent(
        self,
        event: QtCore.QEvent,
        model: QtCore.QAbstractItemModel,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> bool:
        if not (self.is_enabled(option) and index.flags() & QtCore.Qt.ItemIsEditable):
            return False
        if (
            event.type() == QtCore.QEvent.MouseButtonRelease
            and event.button() == QtCore.Qt.LeftButton
        ):
            new_value = not self._is_checked(index)
            model.setData(index, new_value, QtCore.Qt.EditRole)
            model.setData(
                index,
                QtCore.Qt.Checked if new_value else QtCore.Qt.Unchecked,
                QtCore.Qt.CheckStateRole,
            )
            return True
        return super().editorEvent(event, model, option, index)

    @staticmethod
    def _is_checked(index: QtCore.QModelIndex) -> bool:
        state = index.data(QtCore.Qt.CheckStateRole)
        if state is not None:
            return state == QtCore.Qt.Checked
        value = index.data(QtCore.Qt.DisplayRole)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("1", "true", "yes", "on")
        return bool(value)
