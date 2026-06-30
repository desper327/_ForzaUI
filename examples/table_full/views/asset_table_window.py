# -*- coding: utf-8 -*-
"""Main window — passive View shell (tabs + drawer). No domain Model dependency."""

from __future__ import annotations

from Qt import QtCore, QtWidgets

from forza_ui.icons import get_scale_factor
from forza_ui.layout.stacked_widget import FStackedWidget
from forza_ui.navigation.drawer import FDrawer
from forza_ui.navigation.menu_tab_widget import FMenuTabWidget
from forza_ui.table import FTableViewSet

from views.pages.log_page import LogPage
from views.pages.settings_page import SettingsPage
from views.pages.task_overview_page import TaskOverviewPage
from views.row_detail_panel import RowDetailPanel


class AssetTableWindow(QtWidgets.QMainWindow):
    """Passive View: emits user intent, exposes setters; does not import GlobalModel."""

    add_row_requested = QtCore.Signal()

    def __init__(self, view_set: FTableViewSet, parent=None):
        super().__init__(parent)
        self.setWindowTitle("forza_ui Table Full Demo")
        self.resize(1100, 720)

        self._view_set = view_set
        self._overview_page = TaskOverviewPage(view_set)
        self._overview_page.add_button.clicked.connect(self.add_row_requested.emit)

        self._settings_page = SettingsPage()
        self._log_page = LogPage()

        self._stack = FStackedWidget()
        self._stack.addWidget(self._overview_page)
        self._stack.addWidget(self._settings_page)
        self._stack.addWidget(self._log_page)

        self._menu_tab = FMenuTabWidget()
        self._menu_tab.add_menu({"text": "任务总览", "svg": "home_line.svg"}, index=0)
        self._menu_tab.add_menu({"text": "设置", "svg": "edit_line.svg"}, index=1)
        self._menu_tab.add_menu({"text": "日志", "svg": "detail_line.svg"}, index=2)
        self._menu_tab.tool_button_group.sig_checked_changed.connect(
            self._stack.setCurrentIndex
        )
        self._menu_tab.tool_button_group.set_fui_checked(0)

        central = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        layout.addWidget(self._menu_tab)
        layout.addWidget(self._stack, 1)
        self.setCentralWidget(central)

        self._detail_panel = RowDetailPanel()
        scale_x, _ = get_scale_factor()
        self._drawer = FDrawer("资产详情", parent=self).right()
        self._drawer.setFixedWidth(int(280 * scale_x))
        self._drawer.set_widget(self._detail_panel)

    @property
    def view_set(self) -> FTableViewSet:
        return self._view_set

    @property
    def drawer(self) -> FDrawer:
        return self._drawer

    @property
    def detail_panel(self) -> RowDetailPanel:
        return self._detail_panel

    @property
    def settings_page(self) -> SettingsPage:
        return self._settings_page

    @property
    def log_page(self) -> LogPage:
        return self._log_page

    def set_status(self, text: str) -> None:
        self._overview_page.set_status(text)

    def closeEvent(self, event) -> None:
        self._drawer.close()
        super().closeEvent(event)
