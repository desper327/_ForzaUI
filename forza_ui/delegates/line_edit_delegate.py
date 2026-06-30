# -*- coding: utf-8 -*-
"""QStyledItemDelegate for FLineEdit text columns."""

from __future__ import annotations

from Qt import QtCore, QtGui, QtWidgets

from forza_ui import forza_theme
from forza_ui.delegates.base import FItemDelegateBase
from forza_ui.input.line_edit import FLineEdit


class FLineEditDelegate(FItemDelegateBase):
    """Text column delegate using FLineEdit appearance."""

    def __init__(
        self,
        fui_size: int | None = None,
        cell_margin: int = 3,
        single_click_edit: bool = False,
        parent=None,
    ):
        super().__init__(
            fui_size=fui_size,
            cell_margin=cell_margin,
            single_click_edit=single_click_edit,
            parent=parent,
        )

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> None:
        self.paint_selection_background(painter, option)
        text = index.data(QtCore.Qt.DisplayRole) or ""
        FLineEdit.paint_appearance(
            painter,
            self.content_rect(option),
            str(text),
            fui_size=self.resolved_fui_size(),
            enabled=self.is_enabled(option),
        )

    def createEditor(
        self,
        parent: QtWidgets.QWidget,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> QtWidgets.QWidget:
        editor = FLineEdit(parent=parent)
        editor.set_fui_size(self.resolved_fui_size())
        forza_theme.apply(editor)
        return editor

    def setEditorData(self, editor: FLineEdit, index: QtCore.QModelIndex) -> None:
        editor.setText(str(index.model().data(index, QtCore.Qt.EditRole) or ""))

    def setModelData(
        self,
        editor: FLineEdit,
        model: QtCore.QAbstractItemModel,
        index: QtCore.QModelIndex,
    ) -> None:
        model.setData(index, editor.text(), QtCore.Qt.EditRole)
