"""
FCheckBox
"""

# Import third-party modules
from Qt import QtWidgets

# Import local modules
from forza_ui.mixin import cursor_mixin


@cursor_mixin
class FCheckBox(QtWidgets.QCheckBox):
    """
    FCheckBox just use stylesheet and set cursor shape when hover. No more extend.
    """

    _paint_proxies: dict[int, "FCheckBox"] = {}

    def __init__(self, text="", parent=None):
        super(FCheckBox, self).__init__(text=text, parent=parent)

    @classmethod
    def clear_paint_proxies(cls) -> None:
        cls._paint_proxies.clear()

    @classmethod
    def paint_appearance(
        cls,
        painter,
        rect,
        checked: bool,
        *,
        fui_size: int | None = None,
        enabled: bool = True,
    ) -> None:
        from forza_ui.input.paint_utils import paint_check_indicator_appearance

        paint_check_indicator_appearance(
            cls._paint_proxies,
            painter,
            rect,
            checked,
            fui_size=fui_size,
            enabled=enabled,
        )
