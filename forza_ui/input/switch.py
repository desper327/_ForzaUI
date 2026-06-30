"""
FSwitch
"""

# Import third-party modules
from Qt import QtCore, QtWidgets

# Import local modules
from forza_ui import forza_theme
from forza_ui.mixin import cursor_mixin


@cursor_mixin
class FSwitch(QtWidgets.QRadioButton):
    """
    Switching Selector.

    Property:
        fui_size: the size of switch widget. int
    """

    _paint_proxies: dict[int, "FSwitch"] = {}

    def __init__(self, parent=None):
        self._fui_size = forza_theme.default_size
        super(FSwitch, self).__init__(parent)
        self.setAutoExclusive(False)

    def minimumSizeHint(self):
        """
        Override the QRadioButton minimum size hint. We don't need the text space.
        :return:
        """
        height = self._fui_size * 1.2
        return QtCore.QSize(int(height), int(height / 2))

    def get_fui_size(self):
        """
        Get the switch size.
        :return: int
        """
        return getattr(self, "_fui_size", forza_theme.default_size)

    def set_fui_size(self, value):
        """
        Set the switch size.
        :param value: int
        :return: None
        """
        self._fui_size = value
        self.style().polish(self)

    fui_size = QtCore.Property(int, get_fui_size, set_fui_size)

    def huge(self):
        """Set FSwitch to huge size"""
        self.set_fui_size(forza_theme.huge)
        return self

    def large(self):
        """Set FSwitch to large size"""
        self.set_fui_size(forza_theme.large)
        return self

    def medium(self):
        """Set FSwitch to medium size"""
        self.set_fui_size(forza_theme.medium)
        return self

    def small(self):
        """Set FSwitch to small size"""
        self.set_fui_size(forza_theme.small)
        return self

    def tiny(self):
        """Set FSwitch to tiny size"""
        self.set_fui_size(forza_theme.tiny)
        return self

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
        from forza_ui.input.paint_utils import paint_switch_indicator_appearance

        paint_switch_indicator_appearance(
            cls._paint_proxies,
            painter,
            rect,
            checked,
            fui_size=fui_size,
            enabled=enabled,
        )
