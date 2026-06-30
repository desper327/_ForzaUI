# -*- coding: utf-8 -*-
"""Badge color policy registered by name from YAML schema."""

from __future__ import annotations

from Qt import QtGui


class StatusColorPolicy:
    _MAP = {
        "完成": ("#1a3d2e", "#52c41a"),
        "进行中": ("#3d2e1a", "#faad14"),
        "待开始": ("#2a2a2a", "#8c8c8c"),
    }
    _DEFAULT = ("#2a2a2a", "#d9d9d9")

    def colors_for(self, status: str) -> tuple[QtGui.QColor, QtGui.QColor]:
        bg_hex, fg_hex = self._MAP.get(status, self._DEFAULT)
        return QtGui.QColor(bg_hex), QtGui.QColor(fg_hex)


BADGE_POLICIES = {
    "status": StatusColorPolicy(),
}
