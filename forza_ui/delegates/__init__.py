# -*- coding: utf-8 -*-
"""
Table/tree item delegates for forza_ui.

Each delegate pairs with an F* widget: display via paint_appearance, edit via real widget.
"""

from __future__ import annotations

from forza_ui.delegates.badge_delegate import (
    BadgeColorPolicy,
    DefaultBadgeColorPolicy,
    FBadgeDelegate,
)
from forza_ui.delegates.base import DelegateRole, FItemDelegateBase
from forza_ui.delegates.button_delegate import FButtonDelegate
from forza_ui.delegates.check_delegate import FCheckDelegate
from forza_ui.delegates.combo_delegate import FComboDelegate
from forza_ui.delegates.date_delegate import FDateDelegate
from forza_ui.delegates.line_edit_delegate import FLineEditDelegate
from forza_ui.delegates.progress_delegate import FProgressDelegate
from forza_ui.delegates.registry import register_column_delegates
from forza_ui.delegates.spin_delegate import FSpinDelegate
from forza_ui.delegates.switch_delegate import FSwitchDelegate

__all__ = [
    "BadgeColorPolicy",
    "DefaultBadgeColorPolicy",
    "DelegateRole",
    "FBadgeDelegate",
    "FButtonDelegate",
    "FCheckDelegate",
    "FComboDelegate",
    "FDateDelegate",
    "FItemDelegateBase",
    "FLineEditDelegate",
    "FProgressDelegate",
    "FSpinDelegate",
    "FSwitchDelegate",
    "register_column_delegates",
]

