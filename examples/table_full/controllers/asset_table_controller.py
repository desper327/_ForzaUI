# -*- coding: utf-8 -*-
"""Controller — connects GlobalModel, FTableViewSet, tasks, and drawer."""

from __future__ import annotations

from Qt import QtCore

from forza_ui.feedback.progress_bar import FProgressBar
from forza_ui.input.push_button import FPushButton
from forza_ui.table import FTableViewSet

from models.asset_row import AssetRow
from models.asset_model import GlobalModel
from policies.status_color import BADGE_POLICIES
from services.row_task_manager import RowTaskManager
from views.asset_table_window import AssetTableWindow


class AssetTableController(QtCore.QObject):
    def __init__(self, model: GlobalModel, parent=None):
        super().__init__(parent)
        self._model = model
        self._view_set = (
            FTableViewSet(model.schema)
            .searchable()
            .paginated([10, 25, 50])
        )
        self._window = AssetTableWindow(self._view_set)
        self._task_manager = RowTaskManager(self)
        self._drawer_row_index = -1

        self._view_set.set_source_model(model.table_model)
        self._view_set.cell_edited.connect(self._on_cell_edited)

        delegates = self._view_set.configure_delegates(badge_policies=BADGE_POLICIES)
        delete_delegate = delegates.get("action")
        if delete_delegate is not None:
            delete_delegate.clicked.connect(self._on_delete_clicked)

        task_delegate = delegates.get("task_action")
        if task_delegate is not None:
            task_delegate.clicked.connect(self._on_task_action_clicked)

        detail_delegate = delegates.get("detail_action")
        if detail_delegate is not None:
            detail_delegate.clicked.connect(self._on_detail_clicked)

        self._window.add_row_requested.connect(self._on_add_row)

        settings = self._window.settings_page
        settings.set_project_name(model.state.project_name)
        settings.set_default_page_size(model.state.default_page_size)
        settings.project_name_changed.connect(self._on_project_name_changed)
        settings.default_page_size_changed.connect(self._on_default_page_size_changed)

        self._task_manager.progress_updated.connect(self._on_task_progress)
        self._task_manager.task_finished.connect(self._on_task_finished)
        self._task_manager.task_cancelled.connect(self._on_task_cancelled)

        self._sync_status("已加载 YAML 配置驱动的表格")
        self._log("应用已启动")

    @property
    def window(self) -> AssetTableWindow:
        return self._window

    def _log(self, message: str) -> None:
        self._window.log_page.append_line(message)

    def _row_index_by_name(self, name: str) -> int:
        for index, row in enumerate(self._model.state.rows):
            if row.name == name:
                return index
        return -1

    def _sync_status(self, prefix: str) -> None:
        rows = self._model.state.rows
        summary = " | ".join(
            f"{r.name}/{r.asset_type}/{'Y' if r.enabled else 'N'}/{r.status}"
            for r in rows[:5]
        )
        extra = f" ... (+{len(rows) - 5})" if len(rows) > 5 else ""
        project = self._model.state.project_name
        self._window.set_status(f"{prefix} — [{project}] [{summary}{extra}]")

    def _sync_task_button(self, row: AssetRow) -> None:
        if row.task_state == "running":
            row.task_action = "取消"
            row.task_btn_type = FPushButton.DangerType
        else:
            row.task_action = "开始"
            row.task_btn_type = FPushButton.PrimaryType

    def _refresh_task_columns(self, row_index: int) -> None:
        table_model = self._model.table_model
        for field in ("progress", "task_action", "status"):
            table_model.notify_row_changed(row_index, field)

    def _sync_detail_if_open(self, row_index: int) -> None:
        if row_index != self._drawer_row_index:
            return
        if not self._window.drawer.isVisible():
            return
        rows = self._model.state.rows
        if 0 <= row_index < len(rows):
            self._window.detail_panel.set_row(rows[row_index])

    def _on_project_name_changed(self, name: str) -> None:
        self._model.state.project_name = name
        self._sync_status("项目名称已更新")
        self._log(f"项目名称 → {name}")

    def _on_default_page_size_changed(self, page_size: int) -> None:
        self._model.state.default_page_size = page_size
        self._view_set.page._on_page_size_changed(page_size)
        self._log(f"默认每页行数 → {page_size}")

    def _on_detail_clicked(self, index: QtCore.QModelIndex) -> None:
        source_index = self._view_set.map_to_source(index)
        row_index = source_index.row()
        rows = self._model.state.rows
        if row_index < 0 or row_index >= len(rows):
            return
        row = rows[row_index]
        self._drawer_row_index = row_index
        self._window.detail_panel.set_row(row)
        self._window.drawer.open()
        self._log(f"查看详情: {row.name}")

    def _on_cell_edited(self, row_index: int, field_key: str, new_value: object) -> None:
        if field_key == "asset_type":
            row = self._model.state.rows[row_index]
            if row.status == "待开始":
                row.status = "进行中"
                self._model.table_model.notify_row_changed(row_index, "status")
        self._sync_status(f"第 {row_index + 1} 行.{field_key} → {new_value!r}")
        self._log(f"编辑 行{row_index + 1}.{field_key} = {new_value!r}")
        self._sync_detail_if_open(row_index)

    def _on_task_action_clicked(self, index: QtCore.QModelIndex) -> None:
        source_index = self._view_set.map_to_source(index)
        row_index = source_index.row()
        rows = self._model.state.rows
        if row_index < 0 or row_index >= len(rows):
            return
        row = rows[row_index]
        if row.task_state == "running":
            self._task_manager.cancel(row.name)
            self._log(f"请求取消任务: {row.name}")
            return
        if row.task_state in ("done", "cancelled"):
            row.progress = 0
            row.task_status = None
        row.task_state = "running"
        row.status = "进行中"
        self._sync_task_button(row)
        self._refresh_task_columns(row_index)
        self._task_manager.start(row.name)
        self._log(f"启动任务: {row.name}")
        self._sync_detail_if_open(row_index)

    def _on_task_progress(self, row_name: str, value: int) -> None:
        row_index = self._row_index_by_name(row_name)
        if row_index < 0:
            return
        row = self._model.state.rows[row_index]
        if row.progress == value:
            return
        row.progress = value
        self._model.table_model.notify_row_changed(row_index, "progress")
        self._sync_detail_if_open(row_index)

    def _on_task_finished(self, row_name: str) -> None:
        row_index = self._row_index_by_name(row_name)
        if row_index < 0:
            return
        row = self._model.state.rows[row_index]
        row.task_state = "done"
        row.status = "完成"
        row.progress = 100
        row.task_status = FProgressBar.SuccessStatus
        self._sync_task_button(row)
        self._refresh_task_columns(row_index)
        self._log(f"任务完成: {row_name}")
        self._sync_detail_if_open(row_index)

    def _on_task_cancelled(self, row_name: str) -> None:
        row_index = self._row_index_by_name(row_name)
        if row_index < 0:
            return
        row = self._model.state.rows[row_index]
        row.task_state = "cancelled"
        row.task_status = FProgressBar.ErrorStatus
        self._sync_task_button(row)
        self._refresh_task_columns(row_index)
        self._log(f"任务已取消: {row_name}")
        self._sync_detail_if_open(row_index)

    def _on_delete_clicked(self, index: QtCore.QModelIndex) -> None:
        source_index = self._view_set.map_to_source(index)
        row_index = source_index.row()
        rows = self._model.state.rows
        if row_index < 0 or row_index >= len(rows):
            return
        name = rows[row_index].name
        self._task_manager.stop(name)
        self._model.remove_row(row_index)
        if self._drawer_row_index == row_index:
            self._drawer_row_index = -1
            self._window.detail_panel.clear()
            self._window.drawer.close()
        elif self._drawer_row_index > row_index:
            self._drawer_row_index -= 1
        self._sync_status(f"已删除 {name}")
        self._log(f"删除行: {name}")

    def _on_add_row(self) -> None:
        rows = self._model.state.rows
        n = len(rows) + 1
        row = AssetRow(f"Asset_{n:02d}", "特效", True, 1, "待开始")
        self._sync_task_button(row)
        self._model.append_row(row)
        self._sync_status(f"已添加 Asset_{n:02d}")
        self._log(f"添加行: Asset_{n:02d}")

    def shutdown(self) -> None:
        self._task_manager.stop_all()
