# -*- coding: utf-8 -*-
"""
Search and client-side pagination proxy models.

Model chain: FSchemaTableModel → FSearchProxyModel → FPageSliceProxyModel → FTableView
"""

from __future__ import annotations

import re

from Qt import QtCore

from forza_ui.table.load_schema import ColumnDef


class FSearchProxyModel(QtCore.QSortFilterProxyModel):
    """Schema-driven global search across searchable columns."""

    search_changed = QtCore.Signal()

    def __init__(self, schema: list[ColumnDef] | None = None, parent=None):
        super().__init__(parent)
        if hasattr(self, "setRecursiveFilteringEnabled"):
            self.setRecursiveFilteringEnabled(True)
        self._schema = schema or []
        self._search_reg = None

    def set_schema(self, schema: list[ColumnDef]) -> None:
        self._schema = schema

    def set_search_pattern(self, pattern: str) -> None:
        if pattern:
            self._search_reg = re.compile(pattern, re.IGNORECASE)
        else:
            self._search_reg = None
        self.invalidateFilter()
        self.search_changed.emit()

    def filterAcceptsRow(self, source_row: int, source_parent: QtCore.QModelIndex) -> bool:
        source = self.sourceModel()
        if source is None:
            return False

        if not self._search_reg:
            return True

        for col_index, col in enumerate(self._schema):
            if not col.searchable:
                continue
            model_index = source.index(source_row, col_index, source_parent)
            value = source.data(model_index)
            if value is not None and self._search_reg.search(str(value)) is not None:
                return True
        return False


class FPageSliceProxyModel(QtCore.QAbstractProxyModel):
    """Client-side pagination: exposes one page slice of the source model."""

    page_changed = QtCore.Signal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._page = 1
        self._page_size = 25

    @property
    def current_page(self) -> int:
        return self._page

    @property
    def page_size(self) -> int:
        return self._page_size

    def setSourceModel(self, source: QtCore.QAbstractItemModel | None) -> None:
        old = self.sourceModel()
        if old is not None:
            old.modelReset.disconnect(self._on_source_layout_changed)
            old.rowsInserted.disconnect(self._on_source_rows_changed)
            old.rowsRemoved.disconnect(self._on_source_rows_changed)
            old.layoutChanged.disconnect(self._on_source_layout_changed)
            old.dataChanged.disconnect(self._on_source_data_changed)
        super().setSourceModel(source)
        if source is not None:
            source.modelReset.connect(self._on_source_layout_changed)
            source.rowsInserted.connect(self._on_source_rows_changed)
            source.rowsRemoved.connect(self._on_source_rows_changed)
            source.layoutChanged.connect(self._on_source_layout_changed)
            source.dataChanged.connect(self._on_source_data_changed)

    def set_page(self, page: int, page_size: int | None = None) -> None:
        if page_size is not None:
            self._page_size = max(1, page_size)
        self._page = max(1, page)
        self.layoutChanged.emit()
        self.page_changed.emit(self._page, self._page_size)

    def _offset(self) -> int:
        return (self._page - 1) * self._page_size

    def source_row_count(self) -> int:
        source = self.sourceModel()
        if source is None:
            return 0
        return source.rowCount()

    def rowCount(self, parent=QtCore.QModelIndex()) -> int:
        if parent.isValid():
            return 0
        remaining = max(0, self.source_row_count() - self._offset())
        return min(self._page_size, remaining)

    def columnCount(self, parent=QtCore.QModelIndex()) -> int:
        source = self.sourceModel()
        if source is None:
            return 0
        return source.columnCount(parent)

    def index(self, row: int, column: int, parent=QtCore.QModelIndex()) -> QtCore.QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
        return self.createIndex(row, column)

    def parent(self, index: QtCore.QModelIndex) -> QtCore.QModelIndex:
        return QtCore.QModelIndex()

    def mapFromSource(self, source_index: QtCore.QModelIndex) -> QtCore.QModelIndex:
        if not source_index.isValid():
            return QtCore.QModelIndex()
        row = source_index.row() - self._offset()
        if 0 <= row < self.rowCount():
            return self.index(row, source_index.column())
        return QtCore.QModelIndex()

    def mapToSource(self, proxy_index: QtCore.QModelIndex) -> QtCore.QModelIndex:
        if not proxy_index.isValid():
            return QtCore.QModelIndex()
        source = self.sourceModel()
        if source is None:
            return QtCore.QModelIndex()
        return source.index(proxy_index.row() + self._offset(), proxy_index.column())

    def data(self, index: QtCore.QModelIndex, role=QtCore.Qt.DisplayRole):
        source_index = self.mapToSource(index)
        if not source_index.isValid():
            return None
        return self.sourceModel().data(source_index, role)

    def flags(self, index: QtCore.QModelIndex):
        source_index = self.mapToSource(index)
        if not source_index.isValid():
            return QtCore.Qt.NoItemFlags
        return self.sourceModel().flags(source_index)

    def headerData(self, section: int, orientation, role=QtCore.Qt.DisplayRole):
        source = self.sourceModel()
        if source is None:
            return None
        return source.headerData(section, orientation, role)

    def sort(self, column: int, order=QtCore.Qt.AscendingOrder) -> None:
        """Forward header sort to source (FSearchProxyModel / QSortFilterProxyModel)."""
        source = self.sourceModel()
        if source is not None:
            source.sort(column, order)

    def _on_source_layout_changed(self, *args) -> None:
        self.layoutChanged.emit()

    def _on_source_rows_changed(self, *args) -> None:
        self.layoutChanged.emit()

    def _on_source_data_changed(
        self,
        top_left: QtCore.QModelIndex,
        bottom_right: QtCore.QModelIndex,
        roles=(),
    ) -> None:
        """Forward source dataChanged to visible page slice so views repaint."""
        source = self.sourceModel()
        if source is None or not top_left.isValid():
            return

        first_row = None
        first_col = None
        last_row = None
        last_col = None

        for row in range(top_left.row(), bottom_right.row() + 1):
            for col in range(top_left.column(), bottom_right.column() + 1):
                proxy_index = self.mapFromSource(source.index(row, col, top_left.parent()))
                if not proxy_index.isValid():
                    continue
                pr, pc = proxy_index.row(), proxy_index.column()
                if first_row is None:
                    first_row, first_col, last_row, last_col = pr, pc, pr, pc
                else:
                    first_row = min(first_row, pr)
                    first_col = min(first_col, pc)
                    last_row = max(last_row, pr)
                    last_col = max(last_col, pc)

        if first_row is None:
            return

        self.dataChanged.emit(
            self.index(first_row, first_col),
            self.index(last_row, last_col),
            roles,
        )
