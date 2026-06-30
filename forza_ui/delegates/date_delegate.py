# -*- coding: utf-8 -*-
"""QStyledItemDelegate for FDateEdit / FDateTimeEdit / FTimeEdit columns."""

from __future__ import annotations

from Qt import QtCore, QtGui, QtWidgets

from forza_ui.delegates.base import DelegateRole, FItemDelegateBase
from forza_ui.input.spin_box import FDateEdit, FDateTimeEdit, FTimeEdit


class FDateDelegate(FItemDelegateBase):
    """Date/time column delegate backed by QAbstractSpinBox family widgets."""

    _WIDGET_MAP = {
        "date": FDateEdit,
        "datetime": FDateTimeEdit,
        "time": FTimeEdit,
    }

    def __init__(
        self,
        date_type: str = "date",
        display_format_role: int = DelegateRole.DisplayFormatRole,
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
        self._date_type = date_type
        self._display_format_role = display_format_role
        self._widget_cls = self._WIDGET_MAP.get(date_type, FDateEdit)

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> None:
        self.paint_selection_background(painter, option)
        text = self._display_text(index)
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

    def _display_text(self, index: QtCore.QModelIndex) -> str:
        value = index.data(QtCore.Qt.DisplayRole)
        if value is None:
            return ""
        if isinstance(value, (QtCore.QDate, QtCore.QDateTime, QtCore.QTime)):
            fmt = index.data(self._display_format_role)
            if fmt:
                return value.toString(fmt)
            return value.toString()
        return str(value)

    def createEditor(
        self,
        parent: QtWidgets.QWidget,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> QtWidgets.QWidget:
        editor = self._widget_cls(parent=parent)
        editor.set_fui_size(self.resolved_fui_size())
        fmt = index.data(self._display_format_role)
        if fmt:
            editor.setDisplayFormat(fmt)
        return editor

    def setEditorData(self, editor, index: QtCore.QModelIndex) -> None:
        value = index.model().data(index, QtCore.Qt.EditRole)
        if value is None:
            return
        if isinstance(value, QtCore.QDate):
            editor.setDate(value)
        elif isinstance(value, QtCore.QDateTime):
            editor.setDateTime(value)
        elif isinstance(value, QtCore.QTime):
            editor.setTime(value)
        elif isinstance(value, str) and value:
            if self._date_type == "datetime":
                editor.setDateTime(QtCore.QDateTime.fromString(value, QtCore.Qt.ISODate))
            elif self._date_type == "time":
                editor.setTime(QtCore.QTime.fromString(value, QtCore.Qt.ISODate))
            else:
                editor.setDate(QtCore.QDate.fromString(value, QtCore.Qt.ISODate))

    def setModelData(
        self,
        editor,
        model: QtCore.QAbstractItemModel,
        index: QtCore.QModelIndex,
    ) -> None:
        if self._date_type == "datetime":
            model.setData(index, editor.dateTime(), QtCore.Qt.EditRole)
        elif self._date_type == "time":
            model.setData(index, editor.time(), QtCore.Qt.EditRole)
        else:
            model.setData(index, editor.date(), QtCore.Qt.EditRole)
