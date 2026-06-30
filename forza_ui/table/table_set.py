# -*- coding: utf-8 -*-
"""
FTableViewSet — table widget kit: delegates, layout, search, pagination.

Typical usage::

    view_set = FTableViewSet(schema).searchable().paginated()
    view_set.set_source_model(global_model.table_model)
"""

from __future__ import annotations

from typing import Any

from Qt import QtCore, QtWidgets

from forza_ui.delegates.badge_delegate import BadgeColorPolicy
from forza_ui.delegates.base import DelegateRole
from forza_ui.display.item_view import FTableView
from forza_ui.icons import get_scale_factor
from forza_ui.input.line_edit import FLineEdit
from forza_ui.navigation.page import FPage
from forza_ui.table.load_schema import ColumnDef
from forza_ui.table.schema_table_model import FSchemaTableModel
from forza_ui.table.search_page_proxy_model import FPageSliceProxyModel, FSearchProxyModel

_HEADER_SORT_MAP = {
    "asc": QtCore.Qt.AscendingOrder,
    "desc": QtCore.Qt.DescendingOrder,
    "ascending": QtCore.Qt.AscendingOrder,
    "descending": QtCore.Qt.DescendingOrder,
}


def map_index_to_source(index: QtCore.QModelIndex) -> QtCore.QModelIndex:
    """Map any proxy index through the chain to the leaf source model index."""
    model = index.model()
    while isinstance(model, (QtCore.QSortFilterProxyModel, QtCore.QAbstractProxyModel)):
        index = model.mapToSource(index)
        if not index.isValid():
            return QtCore.QModelIndex()
        model = index.model()
    return index


def real_index(index: QtCore.QModelIndex) -> QtCore.QModelIndex:
    return map_index_to_source(index)


def real_model(model: QtCore.QAbstractItemModel | None) -> QtCore.QAbstractItemModel | None:
    while isinstance(model, QtCore.QSortFilterProxyModel):
        model = model.sourceModel()
    while isinstance(model, QtCore.QAbstractProxyModel):
        model = model.sourceModel()
    return model


def apply_column_layout(table: FTableView, schema: list[ColumnDef]) -> None:
    scale_x, _ = get_scale_factor()
    header = table.header_view
    for index, col in enumerate(schema):
        if header is not None:
            header.setSectionHidden(index, col.hide)
            if col.width is not None:
                header.resizeSection(index, int(col.width * scale_x))
            if col.order is not None:
                order = col.order
                if order in _HEADER_SORT_MAP:
                    header.setSortIndicator(index, _HEADER_SORT_MAP[order])
                elif order in (QtCore.Qt.AscendingOrder, QtCore.Qt.DescendingOrder):
                    header.setSortIndicator(index, order)


class FTableViewSet(QtWidgets.QWidget):
    """Composite table: FTableView + optional search and pagination."""

    sig_row_clicked = QtCore.Signal(QtCore.QModelIndex)
    sig_double_clicked = QtCore.Signal(QtCore.QModelIndex)
    cell_edited = QtCore.Signal(int, str, object)

    def __init__(self, schema: list[ColumnDef], parent=None):
        super().__init__(parent)
        self._schema = schema
        self._source_model: FSchemaTableModel | None = None
        self._pagination_enabled = False

        self._search_proxy = FSearchProxyModel(schema)
        self._page_slice = FPageSliceProxyModel()
        self._page_slice.setSourceModel(self._search_proxy)

        self._table = FTableView(show_row_count=True)
        self._table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self._table.setEditTriggers(
            QtWidgets.QAbstractItemView.DoubleClicked
            | QtWidgets.QAbstractItemView.SelectedClicked
        )
        self._table.setModel(self._search_proxy)#使用的是search_proxy，而不是source_model
        self._table.pressed.connect(self._on_row_pressed)
        self._table.doubleClicked.connect(self.sig_double_clicked)

        self._search_edit = FLineEdit().search().small()
        self._search_edit.setPlaceholderText("Search...")
        self._search_edit.setVisible(False)
        self._search_edit.textChanged.connect(self._search_proxy.set_search_pattern)

        self._toolbar = QtWidgets.QWidget()
        toolbar_layout = QtWidgets.QHBoxLayout(self._toolbar)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self._search_edit)

        self._page = FPage()
        self._page.setVisible(False)

        self._search_proxy.search_changed.connect(self._on_search_changed)
        self._page.page_changed.connect(self._on_page_changed)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(6)
        main_layout.addWidget(self._toolbar)
        main_layout.addWidget(self._table)
        main_layout.addWidget(self._page)

    @property
    def table(self) -> FTableView:
        return self._table

    @property
    def search_proxy_model(self) -> FSearchProxyModel:
        return self._search_proxy

    @property
    def page_slice_model(self) -> FPageSliceProxyModel:
        return self._page_slice

    @property
    def page(self) -> FPage:
        return self._page

    @property
    def schema(self) -> list[ColumnDef]:
        return self._schema

    def searchable(self) -> FTableViewSet:
        self._search_edit.setVisible(True)
        return self

    def paginated(self, page_sizes: list[int] | None = None) -> FTableViewSet:
        self._pagination_enabled = True
        self._page.setVisible(True)
        self._table.setModel(self._page_slice)
        if page_sizes:
            self._page.set_page_sizes(page_sizes)
        return self

    def configure_delegates(
        self,
        *,
        badge_policy: BadgeColorPolicy | None = None,
        badge_policies: dict[str, BadgeColorPolicy] | None = None,
        options_role: int = DelegateRole.OptionsRole,
    ) -> dict[str, Any]:
        from forza_ui.delegates.registry import register_column_delegates

        delegates = register_column_delegates(
            self._table,
            self._schema,
            options_role=options_role,
            badge_policy=badge_policy,
            badge_policies=badge_policies,
        )
        apply_column_layout(self._table, self._schema)
        return delegates

    def set_source_model(self, model: FSchemaTableModel) -> None:
        if self._source_model is not None:
            self._source_model.cell_edited.disconnect(self.cell_edited)
            self._source_model.modelReset.disconnect(self._update_page_total)
            self._source_model.rowsInserted.disconnect(self._update_page_total)
            self._source_model.rowsRemoved.disconnect(self._update_page_total)
        self._source_model = model
        self._search_proxy.setSourceModel(model)#这里给代理设置model，必须设置model，与mvc不冲突
        model.cell_edited.connect(self.cell_edited)
        model.modelReset.connect(self._update_page_total)
        model.rowsInserted.connect(self._update_page_total)
        model.rowsRemoved.connect(self._update_page_total)
        self._update_page_total()

    def map_to_source(self, index: QtCore.QModelIndex) -> QtCore.QModelIndex:
        return map_index_to_source(index)

    def source_row_for_index(self, index: QtCore.QModelIndex) -> int:
        source_index = self.map_to_source(index)
        return source_index.row() if source_index.isValid() else -1

    def _update_page_total(self) -> None:
        if self._pagination_enabled:
            self._page.set_total(self._search_proxy.rowCount(), reset_page=False)
            self._page_slice.set_page(
                self._page.current_page(),
                self._page.page_size(),
            )

    def _on_search_changed(self) -> None:
        if self._pagination_enabled:
            self._page.set_total(self._search_proxy.rowCount(), reset_page=True)
            self._page_slice.set_page(1, self._page.page_size())

    def _on_page_changed(self, page_size: int, current_page: int) -> None:
        self._page_slice.set_page(current_page, page_size)

    def _on_row_pressed(self, index: QtCore.QModelIndex) -> None:
        button = QtWidgets.QApplication.mouseButtons()
        if button == QtCore.Qt.LeftButton:
            self.sig_row_clicked.emit(self.map_to_source(index))
