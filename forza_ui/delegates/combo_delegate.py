# -*- coding: utf-8 -*-
"""QStyledItemDelegate that displays and edits cells with FComboBox."""

from __future__ import annotations

from Qt import QtCore, QtGui, QtWidgets

from forza_ui.delegates.base import DelegateRole, FItemDelegateBase
from forza_ui.input.combo_box import FComboBox


class FComboDelegate(FItemDelegateBase):
    """Table/tree cell delegate for combo columns."""

    DEFAULT_OPTIONS_ROLE = DelegateRole.OptionsRole

    def __init__(
        self,
        options_role: int = DEFAULT_OPTIONS_ROLE,
        fui_size: int | None = None,
        cell_margin: int = 3,
        parent=None,
    ):
        super().__init__(
            fui_size=fui_size,
            cell_margin=cell_margin,
            single_click_edit=True,
            parent=parent,
        )
        self._options_role = options_role

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> None:
        self.paint_selection_background(painter, option)
        text = index.data(QtCore.Qt.DisplayRole) or ""
        FComboBox.paint_appearance(
            painter,
            self.content_rect(option),
            str(text),
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
        if self.open_editor_on_click(event, option, index):
            return True
        return super().editorEvent(event, model, option, index)

    def createEditor(
        self,
        parent: QtWidgets.QWidget,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> QtWidgets.QWidget:
        combo = FComboBox(parent)
        combo.set_fui_size(self.resolved_fui_size())
        options = index.model().data(index, self._options_role) or []
        combo.addItems(options)
        return combo

    def setEditorData(self, editor: FComboBox, index: QtCore.QModelIndex) -> None:
        current = index.model().data(index, QtCore.Qt.EditRole)
        idx = editor.findText(current or "")
        editor.setCurrentIndex(idx if idx >= 0 else 0)

    def setModelData(
        self,
        editor: FComboBox,
        model: QtCore.QAbstractItemModel,
        index: QtCore.QModelIndex,
    ) -> None:
        model.setData(index, editor.currentText(), QtCore.Qt.EditRole)
