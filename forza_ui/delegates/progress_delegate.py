# -*- coding: utf-8 -*-
"""Read-only progress bar column delegate."""

from __future__ import annotations

from Qt import QtCore, QtGui, QtWidgets

from forza_ui import forza_theme
from forza_ui.delegates.base import DelegateRole, FItemDelegateBase
from forza_ui.feedback.progress_bar import FProgressBar


class FProgressDelegate(FItemDelegateBase):
    """Table cell delegate that paints FProgressBar via paint_appearance."""

    def __init__(
        self,
        min_role: int = DelegateRole.MinRole,
        max_role: int = DelegateRole.MaxRole,
        status_role: int = DelegateRole.ProgressStatusRole,
        fui_size: int | None = None,
        cell_margin: int = 4,
        parent=None,
    ):
        super().__init__(
            fui_size=fui_size,
            cell_margin=cell_margin,
            single_click_edit=False,
            parent=parent,
        )
        self._min_role = min_role
        self._max_role = max_role
        self._status_role = status_role

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> None:
        self.paint_selection_background(painter, option)
        raw_value = index.data(QtCore.Qt.EditRole)
        try:
            value = int(raw_value or 0)
        except (TypeError, ValueError):
            value = 0
        minimum = index.data(self._min_role)
        maximum = index.data(self._max_role)
        minimum = int(minimum) if minimum is not None else 0
        maximum = int(maximum) if maximum is not None else 100
        status = index.data(self._status_role) or FProgressBar.NormalStatus
        content = self.content_rect(option)
        bar_h = forza_theme.progress_bar_size
        bar_rect = QtCore.QRect(
            content.left(),
            content.top() + max(0, (content.height() - bar_h) // 2),
            content.width(),
            bar_h,
        )
        FProgressBar.paint_appearance(
            painter,
            bar_rect,
            value=value,
            minimum=minimum,
            maximum=maximum,
            fui_status=str(status),
            enabled=self.is_enabled(option),
        )

    def sizeHint(
        self,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> QtCore.QSize:
        base = super().sizeHint(option, index)
        bar_h = forza_theme.progress_bar_size + self._cell_margin * 2
        return QtCore.QSize(base.width(), max(base.height(), bar_h))
