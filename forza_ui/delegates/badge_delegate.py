# -*- coding: utf-8 -*-
"""Read-only badge/status column delegate."""

from __future__ import annotations

from typing import Protocol

from Qt import QtCore, QtGui, QtWidgets


class BadgeColorPolicy(Protocol):
    def colors_for(self, text: str) -> tuple[QtGui.QColor, QtGui.QColor]:
        """Return (background, foreground) for the given display text."""


class DefaultBadgeColorPolicy:
    """Neutral badge colors when no semantic mapping is provided."""

    def colors_for(self, text: str) -> tuple[QtGui.QColor, QtGui.QColor]:
        return QtGui.QColor("#2a2a2a"), QtGui.QColor("#d9d9d9")


class FBadgeDelegate(QtWidgets.QStyledItemDelegate):
    """Read-only rounded badge column with injectable color policy."""

    _H_PADDING = 10
    _V_PADDING = 4
    _RADIUS = 4

    def __init__(self, policy: BadgeColorPolicy | None = None, parent=None):
        super().__init__(parent)
        self._policy = policy or DefaultBadgeColorPolicy()

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> None:
        text = index.data(QtCore.Qt.DisplayRole) or ""
        bg_color, fg_color = self._policy.colors_for(str(text))

        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        if option.state & QtWidgets.QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())

        badge_rect = option.rect.adjusted(
            self._H_PADDING,
            self._V_PADDING,
            -self._H_PADDING,
            -self._V_PADDING,
        )
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(badge_rect), self._RADIUS, self._RADIUS)
        painter.fillPath(path, bg_color)
        painter.setPen(fg_color)
        painter.drawText(badge_rect, QtCore.Qt.AlignCenter, str(text))
        painter.restore()

    def sizeHint(
        self,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> QtCore.QSize:
        base = super().sizeHint(option, index)
        return QtCore.QSize(base.width(), max(base.height(), 28))
