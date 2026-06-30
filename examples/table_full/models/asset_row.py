# -*- coding: utf-8 -*-
"""Domain row and state — pure Python, no Qt dependency except QDate on rows."""

from __future__ import annotations

from dataclasses import dataclass

from Qt import QtCore

ASSET_TYPE_OPTIONS = ["相机", "角色", "场景", "特效", "灯光"]


@dataclass
class AssetRow:
    name: str
    asset_type: str
    enabled: bool = True
    count: int = 1
    status: str = "待开始"
    due_date: QtCore.QDate | None = None
    progress: int = 0
    task_state: str = "idle"
    task_action: str = "开始"
    task_btn_type: str = "primary"
    task_status: str | None = None

    def __post_init__(self) -> None:
        if self.due_date is None:
            self.due_date = QtCore.QDate.currentDate().addDays(7)


@dataclass
class AssetTableState:
    rows: list[AssetRow]
    asset_type_options: list[str] | None = None
    project_name: str = "DemoProject"
    default_page_size: int = 10

    def __post_init__(self) -> None:
        if self.asset_type_options is None:
            self.asset_type_options = list(ASSET_TYPE_OPTIONS)
