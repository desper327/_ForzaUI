# -*- coding: utf-8 -*-
"""
FSchemaTableModel — schema-driven Qt table model (MVC adapter layer).

Projects domain ``rows`` onto QAbstractTableModel for FTableView / delegates.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from Qt import QtCore, QtGui

from forza_ui.delegates.base import DelegateRole
from forza_ui.input.push_button import FPushButton
from forza_ui.table.load_schema import CellType, ColumnDef


def _get_row_value(row: Any, key: str) -> Any:
    if isinstance(row, dict):
        return row.get(key)
    return getattr(row, key, None)


def _set_row_value(row: Any, key: str, value: Any) -> None:
    if isinstance(row, dict):
        row[key] = value
    else:
        setattr(row, key, value)


def _resolve_context_value(context: Any, attr_path: str) -> Any:
    if context is None or not attr_path:
        return None
    obj = context
    for part in attr_path.split("."):
        if isinstance(obj, dict):
            obj = obj.get(part)
        else:
            obj = getattr(obj, part, None)
        if obj is None:
            break
    return obj


_BUTTON_TYPE_MAP = {
    "default": FPushButton.DefaultType,
    "primary": FPushButton.PrimaryType,
    "success": FPushButton.SuccessType,
    "warning": FPushButton.WarningType,
    "danger": FPushButton.DangerType,
}


class TableRole:
    """Role constants shared between model and delegates."""

    CellTypeRole = QtCore.Qt.UserRole + 1
    OptionsRole = DelegateRole.OptionsRole
    MinRole = DelegateRole.MinRole
    MaxRole = DelegateRole.MaxRole
    StepRole = DelegateRole.StepRole
    ButtonTypeRole = DelegateRole.ButtonTypeRole
    DisplayFormatRole = DelegateRole.DisplayFormatRole
    ProgressStatusRole = DelegateRole.ProgressStatusRole


class FSchemaTableModel(QtCore.QAbstractTableModel):
    """
    Generic QAbstractTableModel driven by column schema.

    Reads/writes row data via ``rows`` callable; resolves combo options from
    ``context`` when ``options_from`` is set on a column.
    """

    cell_edited = QtCore.Signal(int, str, object)

    def __init__(
        self,
        schema: list[ColumnDef],
        rows: Callable[[], list],
        context: Callable[[], Any] | None = None,
        parent=None,
    ):
        super().__init__(parent)
        self._schema = schema
        self._rows = rows
        self._context = context or (lambda: None)
        self._key_to_col = {col.key: index for index, col in enumerate(schema)}

    @property
    def schema(self) -> list[ColumnDef]:
        return self._schema

    def column_index(self, key: str) -> int:
        return self._key_to_col[key]

    def rowCount(self, parent=QtCore.QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self._rows())

    def columnCount(self, parent=QtCore.QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self._schema)

    def _column(self, col_index: int) -> ColumnDef:
        return self._schema[col_index]

    def _display_value(self, col: ColumnDef, value: Any) -> Any:
        if col.cell_type == CellType.CHECK:
            return col.check_true_label if value else col.check_false_label
        if col.cell_type == CellType.DATE and isinstance(value, QtCore.QDate):
            fmt = col.display_format or "yyyy-MM-dd"
            return value.toString(fmt)
        if col.cell_type == CellType.DATETIME and isinstance(value, QtCore.QDateTime):
            fmt = col.display_format or "yyyy-MM-dd HH:mm:ss"
            return value.toString(fmt)
        if col.cell_type == CellType.TIME and isinstance(value, QtCore.QTime):
            fmt = col.display_format or "HH:mm:ss"
            return value.toString(fmt)
        if col.cell_type == CellType.BUTTON:
            return col.button_label or str(value or "")
        return value

    def _resolve_options(self, col: ColumnDef) -> list[Any] | None:
        if col.options is not None:
            return col.options
        if col.options_from:
            value = _resolve_context_value(self._context(), col.options_from)
            return list(value) if value is not None else []
        return None

    def _button_type(self, col: ColumnDef, row: Any = None) -> str:
        if row is not None:
            row_type = _get_row_value(row, "task_btn_type")
            if row_type:
                return _BUTTON_TYPE_MAP.get(row_type, row_type)
        if col.button_type:
            return _BUTTON_TYPE_MAP.get(col.button_type, col.button_type)
        return FPushButton.DefaultType

    def _progress_status(self, row: Any, col: ColumnDef, value: Any) -> str:
        from forza_ui.feedback.progress_bar import FProgressBar

        row_status = _get_row_value(row, "task_status")
        if row_status in (
            FProgressBar.ErrorStatus,
            FProgressBar.SuccessStatus,
            FProgressBar.NormalStatus,
        ):
            return row_status
        try:
            numeric = int(value or 0)
        except (TypeError, ValueError):
            numeric = 0
        minimum = col.min_value if col.min_value is not None else 0
        maximum = col.max_value if col.max_value is not None else 100
        if numeric >= maximum:
            return FProgressBar.SuccessStatus
        task_state = _get_row_value(row, "task_state")
        if task_state == "cancelled":
            return FProgressBar.ErrorStatus
        return FProgressBar.NormalStatus

    def data(self, index: QtCore.QModelIndex, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None

        row = self._rows()[index.row()]
        col = self._column(index.column())
        value = _get_row_value(row, col.key)

        if role == QtCore.Qt.DisplayRole:
            return self._display_value(col, value)

        if role == QtCore.Qt.EditRole:
            return value

        if role == QtCore.Qt.CheckStateRole and col.cell_type == CellType.CHECK:
            return QtCore.Qt.Checked if value else QtCore.Qt.Unchecked

        if role == TableRole.CellTypeRole:
            return col.cell_type.value

        if role == TableRole.OptionsRole and col.cell_type == CellType.COMBO:
            return self._resolve_options(col)

        if role == TableRole.MinRole and col.cell_type in (
            CellType.SPIN,
            CellType.DOUBLE,
            CellType.PROGRESS,
        ):
            return col.min_value if col.min_value is not None else 0

        if role == TableRole.MaxRole and col.cell_type in (
            CellType.SPIN,
            CellType.DOUBLE,
            CellType.PROGRESS,
        ):
            return col.max_value if col.max_value is not None else (
                100 if col.cell_type == CellType.PROGRESS else 999
            )

        if role == TableRole.StepRole and col.cell_type in (CellType.SPIN, CellType.DOUBLE):
            return col.step if col.step is not None else 1

        if role == TableRole.DisplayFormatRole and col.cell_type in (
            CellType.DATE,
            CellType.DATETIME,
            CellType.TIME,
        ):
            return col.display_format or "yyyy-MM-dd"

        if role == TableRole.ButtonTypeRole and col.cell_type == CellType.BUTTON:
            return self._button_type(col, row)

        if role == TableRole.ProgressStatusRole and col.cell_type == CellType.PROGRESS:
            return self._progress_status(row, col, value)

        return None

    def setData(self, index: QtCore.QModelIndex, value, role=QtCore.Qt.EditRole) -> bool:
        if not index.isValid():
            return False

        col = self._column(index.column())
        if not col.editable and role not in (QtCore.Qt.CheckStateRole,):
            return False

        rows = self._rows()
        row_obj = rows[index.row()]
        old_value = _get_row_value(row_obj, col.key)
        new_value = value

        if role == QtCore.Qt.CheckStateRole and col.cell_type == CellType.CHECK:
            new_value = value == QtCore.Qt.Checked
            if old_value == new_value:
                return False
            _set_row_value(row_obj, col.key, new_value)
            self.dataChanged.emit(
                index,
                index,
                [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole, QtCore.Qt.CheckStateRole],
            )
            self.cell_edited.emit(index.row(), col.key, new_value)
            return True

        if role != QtCore.Qt.EditRole:
            return False

        if isinstance(new_value, str):
            new_value = new_value.strip()

        if old_value == new_value:
            return False

        _set_row_value(row_obj, col.key, new_value)
        self.dataChanged.emit(index, index, [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole])
        self.cell_edited.emit(index.row(), col.key, new_value)
        return True

    def flags(self, index: QtCore.QModelIndex):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        col = self._column(index.column())
        base = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
        if col.editable:
            base |= QtCore.Qt.ItemIsEditable
        if col.cell_type == CellType.CHECK:
            base |= QtCore.Qt.ItemIsUserCheckable
        return base

    def headerData(self, section: int, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            return self._schema[section].title
        return str(section + 1)

    def append_row(self, row: Any) -> None:
        insert_at = len(self._rows())
        self.beginInsertRows(QtCore.QModelIndex(), insert_at, insert_at)
        self._rows().append(row)
        self.endInsertRows()

    def remove_row(self, row_index: int) -> None:
        rows = self._rows()
        if row_index < 0 or row_index >= len(rows):
            return
        self.beginRemoveRows(QtCore.QModelIndex(), row_index, row_index)
        del rows[row_index]
        self.endRemoveRows()

    def notify_row_changed(self, row_index: int, field_key: str) -> None:
        col_index = self.column_index(field_key)
        col = self._column(col_index)
        idx = self.index(row_index, col_index)
        roles = [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole]
        if col.cell_type == CellType.PROGRESS:
            roles.append(TableRole.ProgressStatusRole)
        if col.cell_type == CellType.BUTTON:
            roles.append(TableRole.ButtonTypeRole)
        self.dataChanged.emit(idx, idx, roles)
