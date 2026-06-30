# -*- coding: utf-8 -*-
"""
Table MVC helpers — 5 modules, 4 layers:

1. schema.py           — column config (YAML/JSON/TOML)
2. schema_table_model  — FSchemaTableModel (Qt adapter for domain rows)
3. search_page         — FSearchProxyModel + FPageSliceProxyModel
4. table_set           — FTableViewSet + configure_table_view

Domain models stay in application code; this package provides Qt adapters only.
"""

from __future__ import annotations

from forza_ui.table.load_schema import CellType, ColumnDef, load_column_schema, parse_column_schema
from forza_ui.table.schema_table_model import FSchemaTableModel, TableRole
from forza_ui.table.search_page_proxy_model import FPageSliceProxyModel, FSearchProxyModel
from forza_ui.table.table_set import (
    FTableViewSet,
    apply_column_layout,
    map_index_to_source,
    real_index,
    real_model,
)

__all__ = [
    "CellType",
    "ColumnDef",
    "FPageSliceProxyModel",
    "FSchemaTableModel",
    "FSearchProxyModel",
    "FTableViewSet",
    "TableRole",
    "apply_column_layout",
    "load_column_schema",
    "map_index_to_source",
    "parse_column_schema",
    "real_index",
    "real_model",
]
