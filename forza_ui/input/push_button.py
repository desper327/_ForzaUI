"""
FPushButton.
"""

# Import third-party modules
from Qt import QtCore, QtWidgets

# Import local modules
from forza_ui import forza_theme
from forza_ui.mixin import cursor_mixin
from forza_ui.mixin import focus_shadow_mixin


@cursor_mixin
@focus_shadow_mixin
class FPushButton(QtWidgets.QPushButton):
    """
    QPushButton.

    Property:
        fui_size: The size of push button
        fui_type: The type of push button.
    """

    DefaultType = "default"
    PrimaryType = "primary"
    SuccessType = "success"
    WarningType = "warning"
    DangerType = "danger"

    def __init__(self, text="", icon=None, parent=None):
        self._fui_type = FPushButton.DefaultType
        self._fui_size = forza_theme.default_size
        if icon is None:
            super(FPushButton, self).__init__(text=text, parent=parent)
        else:
            super(FPushButton, self).__init__(icon=icon, text=text, parent=parent)

    def get_fui_size(self):
        """
        Get the push button height
        :return: integer
        """
        return getattr(self, "_fui_size", forza_theme.default_size)

    def set_fui_size(self, value):
        """
        Set the avatar size.
        :param value: integer
        :return: None
        """
        self._fui_size = value
        self.style().polish(self)

    def get_fui_type(self):
        """
        Get the push button type.
        :return: string.
        """
        return self._fui_type

    def set_fui_type(self, value):
        """
        Set the push button type.
        :return: None
        """
        if value in [
            FPushButton.DefaultType,
            FPushButton.PrimaryType,
            FPushButton.SuccessType,
            FPushButton.WarningType,
            FPushButton.DangerType,
        ]:
            self._fui_type = value
        else:
            raise ValueError(
                "Input argument 'value' should be one of " "default/primary/success/warning/danger string."
            )
        self.style().polish(self)

    fui_type = QtCore.Property(str, get_fui_type, set_fui_type)
    fui_size = QtCore.Property(int, get_fui_size, set_fui_size)

    def primary(self):
        """Set FPushButton to PrimaryType"""
        self.set_fui_type(FPushButton.PrimaryType)
        return self

    def success(self):
        """Set FPushButton to SuccessType"""
        self.set_fui_type(FPushButton.SuccessType)
        return self

    def warning(self):
        """Set FPushButton to  WarningType"""
        self.set_fui_type(FPushButton.WarningType)
        return self

    def danger(self):
        """Set FPushButton to DangerType"""
        self.set_fui_type(FPushButton.DangerType)
        return self

    def huge(self):
        """Set FPushButton to huge size"""
        self.set_fui_size(forza_theme.huge)
        return self

    def large(self):
        """Set FPushButton to large size"""
        self.set_fui_size(forza_theme.large)
        return self

    def medium(self):
        """Set FPushButton to  medium"""
        self.set_fui_size(forza_theme.medium)
        return self

    def small(self):
        """Set FPushButton to small size"""
        self.set_fui_size(forza_theme.small)
        return self

    def tiny(self):
        """Set FPushButton to tiny size"""
        self.set_fui_size(forza_theme.tiny)
        return self

    _paint_proxies: dict[int, "FPushButton"] = {}

    @classmethod
    def clear_paint_proxies(cls) -> None:
        cls._paint_proxies.clear()

    @classmethod
    def paint_appearance(
        cls,
        painter,
        rect,
        text: str,
        *,
        fui_size: int | None = None,
        enabled: bool = True,
        fui_type: str = DefaultType,
    ) -> None:
        from forza_ui.input.paint_utils import paint_push_button_appearance

        paint_push_button_appearance(
            cls._paint_proxies,
            painter,
            rect,
            text,
            fui_size=fui_size,
            enabled=enabled,
            fui_type=fui_type,
        )
