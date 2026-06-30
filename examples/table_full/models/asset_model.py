# -*- coding: utf-8 -*-
"""MVC Model — holds domain state and Qt table model."""

from __future__ import annotations

import os

from Qt import QtCore

from forza_ui.table import FSchemaTableModel, load_column_schema

from models.asset_row import AssetRow, AssetTableState

_SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "assets_table.yaml")


class GlobalModel(QtCore.QObject):
    def __init__(self, state: AssetTableState | None = None, schema_path: str | None = None, parent=None):
        super().__init__(parent)
        self._schema = load_column_schema(schema_path or _SCHEMA_PATH)
        self._state = state or AssetTableState(
            rows=[
                AssetRow("Camera_A", "相机", True, 2, "完成", progress=100, task_state="done"),
                AssetRow("Char_Hero", "角色", True, 1, "进行中", progress=35, task_state="idle"),
                AssetRow("Env_City", "场景", False, 5, "待开始"),
            ]
            * 12
        )
        self._table_model = FSchemaTableModel(
            schema=self._schema,
            rows=lambda: self._state.rows,
            context=lambda: self._state,
            parent=self,
        )

    @property
    def schema(self):
        return self._schema

    @property
    def state(self) -> AssetTableState:
        return self._state

    @property
    def table_model(self) -> FSchemaTableModel:
        return self._table_model

    def append_row(self, row: AssetRow) -> None:
        self._table_model.append_row(row)

    def remove_row(self, row_index: int) -> None:
        self._table_model.remove_row(row_index)
