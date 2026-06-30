# -*- coding: utf-8 -*-
"""
forza_ui - Pure View layer Qt widget library.

Styled Ant Design-inspired widgets for MVC applications.
No FieldMixin, no built-in data models.

组件按文件夹分类：basic / input / display / navigation / feedback / layout
详见 README.md「目录结构」。
"""

from __future__ import annotations

import os
import sys

DEFAULT_STATIC_FOLDER = os.path.join(sys.modules[__name__].__path__[0], "static")
CUSTOM_STATIC_FOLDERS: list[str] = []

from forza_ui.theme import FTheme

forza_theme = FTheme("dark", primary_color=FTheme.orange)

from forza_ui.feedback.alert import FAlert
from forza_ui.basic.avatar import FAvatar
from forza_ui.basic.badge import FBadge
from forza_ui.input.button_group import FCheckBoxGroup
from forza_ui.input.button_group import FPushButtonGroup
from forza_ui.input.button_group import FRadioButtonGroup
from forza_ui.input.button_group import FToolButtonGroup
from forza_ui.display.card import FCard
from forza_ui.display.card import FMeta
from forza_ui.display.carousel import FCarousel
from forza_ui.delegates import (
    FBadgeDelegate,
    FButtonDelegate,
    FCheckDelegate,
    FComboDelegate,
    FDateDelegate,
    FLineEditDelegate,
    FSpinDelegate,
    FSwitchDelegate,
    DelegateRole,
    register_column_delegates,
)
from forza_ui.input.check_box import FCheckBox
from forza_ui.navigation.collapse import FCollapse
from forza_ui.input.combo_box import FComboBox
from forza_ui.basic.divider import FDivider
from forza_ui.layout.flow_layout import FFlowLayout
from forza_ui.display.item_view import FBigView
from forza_ui.display.item_view import FListView
from forza_ui.display.item_view import FTableView
from forza_ui.display.item_view import FTreeView
from forza_ui.basic.label import FLabel
from forza_ui.input.line_edit import FLineEdit
from forza_ui.navigation.line_tab_widget import FLineTabWidget
from forza_ui.feedback.loading import FLoading
from forza_ui.feedback.loading import FLoadingWrapper
from forza_ui.navigation.menu import FMenu
from forza_ui.navigation.menu_tab_widget import FMenuTabWidget
from forza_ui.navigation.page import FPage
from forza_ui.feedback.message import FMessage
from forza_ui.feedback.progress_bar import FProgressBar
from forza_ui.feedback.progress_circle import FProgressCircle
from forza_ui.input.push_button import FPushButton
from forza_ui.input.radio_button import FRadioButton
from forza_ui.input.slider import FSlider
from forza_ui.input.spin_box import FDateEdit
from forza_ui.input.spin_box import FDateTimeEdit
from forza_ui.input.spin_box import FDoubleSpinBox
from forza_ui.input.spin_box import FSpinBox
from forza_ui.input.spin_box import FTimeEdit
from forza_ui.input.switch import FSwitch
from forza_ui.navigation.tab_widget import FTabWidget
from forza_ui.input.text_edit import FTextEdit
from forza_ui.feedback.toast import FToast
from forza_ui.input.tool_button import FToolButton
from forza_ui.icons import FIcon
from forza_ui.icons import FPixmap
from forza_ui.utils import application
from forza_ui.icons import get_scale_factor
from forza_ui.table import (
    CellType,
    ColumnDef,
    FPageSliceProxyModel,
    FSchemaTableModel,
    FSearchProxyModel,
    FTableViewSet,
    TableRole,
    load_column_schema,
)

__all__ = [
    "FAlert",
    "FAvatar",
    "FBadge",
    "FCheckBoxGroup",
    "FPushButtonGroup",
    "FRadioButtonGroup",
    "FToolButtonGroup",
    "FCard",
    "FMeta",
    "FCarousel",
    "FBadgeDelegate",
    "FButtonDelegate",
    "FCheckDelegate",
    "FComboDelegate",
    "FDateDelegate",
    "FLineEditDelegate",
    "FSpinDelegate",
    "FSwitchDelegate",
    "DelegateRole",
    "FCheckBox",
    "FCollapse",
    "FComboBox",
    "FDivider",
    "FFlowLayout",
    "FBigView",
    "FListView",
    "FTableView",
    "FTreeView",
    "FLabel",
    "FLineEdit",
    "FLineTabWidget",
    "FLoading",
    "FLoadingWrapper",
    "FMenu",
    "FMenuTabWidget",
    "FPage",
    "FMessage",
    "FProgressBar",
    "FProgressCircle",
    "FPushButton",
    "FRadioButton",
    "FSlider",
    "FDateEdit",
    "FDateTimeEdit",
    "FDoubleSpinBox",
    "FSpinBox",
    "FTimeEdit",
    "FSwitch",
    "FTabWidget",
    "FTextEdit",
    "FToast",
    "FToolButton",
    "FIcon",
    "FPixmap",
    "FTheme",
    "application",
    "forza_theme",
    "get_scale_factor",
    "CellType",
    "ColumnDef",
    "FPageSliceProxyModel",
    "FSchemaTableModel",
    "FSearchProxyModel",
    "FTableViewSet",
    "TableRole",
    "load_column_schema",
    "register_column_delegates",
]

__version__ = "0.1.0"
