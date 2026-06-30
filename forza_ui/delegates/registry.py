# -*- coding: utf-8 -*-
"""Register column delegates on FTableView from a schema map."""

from __future__ import annotations

from typing import Any

from forza_ui.delegates.badge_delegate import BadgeColorPolicy, FBadgeDelegate
from forza_ui.delegates.base import DelegateRole
from forza_ui.delegates.button_delegate import FButtonDelegate
from forza_ui.delegates.check_delegate import FCheckDelegate
from forza_ui.delegates.combo_delegate import FComboDelegate
from forza_ui.delegates.date_delegate import FDateDelegate
from forza_ui.delegates.line_edit_delegate import FLineEditDelegate
from forza_ui.delegates.progress_delegate import FProgressDelegate
from forza_ui.delegates.spin_delegate import FSpinDelegate
from forza_ui.delegates.switch_delegate import FSwitchDelegate
from forza_ui.display.item_view import FTableView


def _cell_type_value(column: Any) -> str:
    cell_type = column.cell_type if hasattr(column, "cell_type") else column.get("cell_type", "text")
    if hasattr(cell_type, "value"):
        return cell_type.value
    return str(cell_type)


def _column_key(column: Any, col_index: int) -> str:
    if hasattr(column, "key"):
        return column.key
    return column.get("key", str(col_index))


def _badge_policy_for_column(
    column: Any,
    badge_policies: dict[str, BadgeColorPolicy] | None,
    fallback: BadgeColorPolicy | None,
) -> BadgeColorPolicy | None:
    name = column.badge_policy if hasattr(column, "badge_policy") else column.get("badge_policy")
    if name and badge_policies and name in badge_policies:
        return badge_policies[name]
    return fallback


def register_column_delegates(
    table: FTableView,
    schema: list[Any],
    *,
    options_role: int = DelegateRole.OptionsRole,
    badge_policy: BadgeColorPolicy | None = None,
    badge_policies: dict[str, BadgeColorPolicy] | None = None,
    button_delegate: FButtonDelegate | None = None,
) -> dict[str, Any]:
    """
    Register delegates from a schema list.

    Supported cell_type values:
        text, combo, spin, double, check, switch, date, datetime, time, badge, button, progress
    """
    instances: dict[str, Any] = {}

    for col_index, column in enumerate(schema):
        cell_type = _cell_type_value(column)
        key = _column_key(column, col_index)

        delegate = None
        if cell_type == "text":
            delegate = FLineEditDelegate(parent=table)
        elif cell_type == "combo":
            delegate = FComboDelegate(options_role=options_role, parent=table)
        elif cell_type == "spin":
            delegate = FSpinDelegate(spin_type="int", parent=table)
        elif cell_type == "double":
            delegate = FSpinDelegate(spin_type="double", parent=table)
        elif cell_type == "check":
            delegate = FCheckDelegate(parent=table)
        elif cell_type == "switch":
            delegate = FSwitchDelegate(parent=table)
        elif cell_type == "date":
            delegate = FDateDelegate(date_type="date", parent=table)
        elif cell_type == "datetime":
            delegate = FDateDelegate(date_type="datetime", parent=table)
        elif cell_type == "time":
            delegate = FDateDelegate(date_type="time", parent=table)
        elif cell_type == "badge":
            policy = _badge_policy_for_column(column, badge_policies, badge_policy)
            delegate = FBadgeDelegate(policy=policy, parent=table)
        elif cell_type == "progress":
            delegate = FProgressDelegate(parent=table)
        elif cell_type == "button":
            delegate = button_delegate or FButtonDelegate(parent=table)
            instances.setdefault("button", delegate)

        if delegate is not None:
            table.setItemDelegateForColumn(col_index, delegate)
            instances[key] = delegate

    return instances
