# -*- coding: utf-8 -*-
"""QStyledItemDelegate for FSpinBox / FDoubleSpinBox numeric columns."""

from __future__ import annotations

from Qt import QtCore, QtGui, QtWidgets

from forza_ui.delegates.base import DelegateRole, FItemDelegateBase
from forza_ui.input.spin_box import FDoubleSpinBox, FSpinBox


class FSpinDelegate(FItemDelegateBase):
    """Integer or double spin column delegate."""

    def __init__(
        self,
        spin_type: str = "int",
        min_role: int = DelegateRole.MinRole,
        max_role: int = DelegateRole.MaxRole,
        step_role: int = DelegateRole.StepRole,
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
        self._spin_type = spin_type
        self._min_role = min_role
        self._max_role = max_role
        self._step_role = step_role
        self._widget_cls = FDoubleSpinBox if spin_type == "double" else FSpinBox

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> None:
        self.paint_selection_background(painter, option)
        value = index.data(QtCore.Qt.DisplayRole)
        text = "" if value is None else str(value)
        self._widget_cls.paint_appearance(
            painter,
            self.content_rect(option),
            text,
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

    def _apply_range(self, editor, index: QtCore.QModelIndex) -> None:
        model = index.model()
        min_val = model.data(index, self._min_role)
        max_val = model.data(index, self._max_role)
        step_val = model.data(index, self._step_role)
        if min_val is not None:
            editor.setMinimum(min_val)
        if max_val is not None:
            editor.setMaximum(max_val)
        if step_val is not None:
            editor.setSingleStep(step_val)

    def createEditor(
        self,
        parent: QtWidgets.QWidget,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> QtWidgets.QWidget:
        editor = self._widget_cls(parent)
        editor.set_fui_size(self.resolved_fui_size())
        self._apply_range(editor, index)
        return editor

    def setEditorData(self, editor, index: QtCore.QModelIndex) -> None:
        value = index.model().data(index, QtCore.Qt.EditRole)
        if value is None:
            return
        if self._spin_type == "double":
            editor.setValue(float(value))
        else:
            editor.setValue(int(value))

    def setModelData(
        self,
        editor,
        model: QtCore.QAbstractItemModel,
        index: QtCore.QModelIndex,
    ) -> None:
        model.setData(index, editor.value(), QtCore.Qt.EditRole)
