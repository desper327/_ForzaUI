# -*- coding: utf-8 -*-
"""Column schema definitions and config file loading."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from enum import Enum
from typing import Any


class CellType(str, Enum):
    TEXT = "text"
    COMBO = "combo"
    CHECK = "check"
    SWITCH = "switch"
    SPIN = "spin"
    DOUBLE = "double"
    DATE = "date"
    DATETIME = "datetime"
    TIME = "time"
    BADGE = "badge"
    BUTTON = "button"
    PROGRESS = "progress"


@dataclass
class ColumnDef:
    key: str
    title: str
    cell_type: CellType = CellType.TEXT
    editable: bool = False
    searchable: bool = False
    hide: bool = False
    width: int | None = None
    order: str | None = None
    options: list[Any] | None = None
    options_from: str | None = None
    min_value: int | float | None = None
    max_value: int | float | None = None
    step: int | float | None = None
    display_format: str | None = None
    badge_policy: str | None = None
    button_label: str | None = None
    button_type: str | None = None
    check_true_label: str = "是"
    check_false_label: str = "否"


def _parse_cell_type(value: Any) -> CellType:
    if isinstance(value, CellType):
        return value
    if isinstance(value, str):
        return CellType(value)
    raise ValueError(f"Invalid cell_type: {value!r}")


def column_def_from_dict(data: dict[str, Any]) -> ColumnDef:
    raw_type = data.get("cell_type", "text")
    return ColumnDef(
        key=str(data["key"]),
        title=str(data.get("title", data.get("label", data["key"]))),
        cell_type=_parse_cell_type(raw_type),
        editable=bool(data.get("editable", False)),
        searchable=bool(data.get("searchable", False)),
        hide=bool(data.get("hide", False)),
        width=data.get("width"),
        order=data.get("order"),
        options=data.get("options"),
        options_from=data.get("options_from"),
        min_value=data.get("min", data.get("min_value")),
        max_value=data.get("max", data.get("max_value")),
        step=data.get("step"),
        display_format=data.get("display_format"),
        badge_policy=data.get("badge_policy"),
        button_label=data.get("button_label"),
        button_type=data.get("button_type"),
        check_true_label=str(data.get("check_true_label", "是")),
        check_false_label=str(data.get("check_false_label", "否")),
    )


def parse_column_schema(raw: Any) -> list[ColumnDef]:
    if isinstance(raw, list):
        columns = raw
    elif isinstance(raw, dict) and "columns" in raw:
        columns = raw["columns"]
    else:
        raise ValueError("Schema must be a list or dict with 'columns' key")
    return [column_def_from_dict(item) for item in columns]


def schema_as_dicts(schema: list[ColumnDef]) -> list[dict[str, Any]]:
    result = []
    for col in schema:
        item: dict[str, Any] = {
            "key": col.key,
            "title": col.title,
            "cell_type": col.cell_type.value,
            "editable": col.editable,
            "searchable": col.searchable,
            "hide": col.hide,
        }
        if col.width is not None:
            item["width"] = col.width
        if col.order is not None:
            item["order"] = col.order
        if col.options is not None:
            item["options"] = col.options
        if col.options_from is not None:
            item["options_from"] = col.options_from
        if col.min_value is not None:
            item["min"] = col.min_value
        if col.max_value is not None:
            item["max"] = col.max_value
        if col.step is not None:
            item["step"] = col.step
        if col.display_format is not None:
            item["display_format"] = col.display_format
        if col.badge_policy is not None:
            item["badge_policy"] = col.badge_policy
        if col.button_label is not None:
            item["button_label"] = col.button_label
        if col.button_type is not None:
            item["button_type"] = col.button_type
        result.append(item)
    return result


def _load_raw_config(path: str) -> Any:
    ext = os.path.splitext(path)[1].lower()
    with open(path, encoding="utf-8") as handle:
        text = handle.read()

    if ext == ".json":
        return json.loads(text)

    if ext in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError as exc:
            raise ImportError(
                "YAML schema requires PyYAML: pip install pyyaml"
            ) from exc
        return yaml.safe_load(text)

    if ext == ".toml":
        try:
            import tomllib
        except ImportError:
            try:
                import tomli as tomllib
            except ImportError as exc:
                raise ImportError(
                    "TOML schema requires Python 3.11+ tomllib or: pip install tomli"
                ) from exc
        return tomllib.loads(text)

    raise ValueError(f"Unsupported schema file extension: {ext}")


def load_column_schema(path: str) -> list[ColumnDef]:
    """Load column schema from JSON, YAML, or TOML file."""
    return parse_column_schema(_load_raw_config(path))
