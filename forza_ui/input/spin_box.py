"""
Custom Stylesheet for QSpinBox, QDoubleSpinBox, QDateTimeEdit, QDateEdit, QTimeEdit.
Only add size arg for their __init__.
"""

# Import third-party modules
from Qt import QtCore, QtWidgets

# Import local modules
from forza_ui import forza_theme
from forza_ui.mixin import cursor_mixin


@cursor_mixin
class FSpinBox(QtWidgets.QSpinBox):
    """
    FSpinBox just use stylesheet and add fui_size. No more extend.
    Property:
        fui_size: The height of FSpinBox
    """

    def __init__(self, parent=None):
        self._fui_size = forza_theme.default_size
        super(FSpinBox, self).__init__(parent=parent)

    def get_fui_size(self):
        """
        Get the FSpinBox height
        :return: integer
        """
        return getattr(self, "_fui_size", forza_theme.default_size)

    def set_fui_size(self, value):
        """
        Set the FSpinBox size.
        :param value: integer
        :return: None
        """
        self._fui_size = value
        self.style().polish(self)

    fui_size = QtCore.Property(int, get_fui_size, set_fui_size)

    def huge(self):
        """Set FSpinBox to huge size"""
        self.set_fui_size(forza_theme.huge)
        return self

    def large(self):
        """Set FSpinBox to large size"""
        self.set_fui_size(forza_theme.large)
        return self

    def medium(self):
        """Set FSpinBox to  medium"""
        self.set_fui_size(forza_theme.medium)
        return self

    def small(self):
        """Set FSpinBox to small size"""
        self.set_fui_size(forza_theme.small)
        return self

    def tiny(self):
        """Set FSpinBox to tiny size"""
        self.set_fui_size(forza_theme.tiny)
        return self


@cursor_mixin
class FDoubleSpinBox(QtWidgets.QDoubleSpinBox):
    """
    FDoubleSpinBox just use stylesheet and add fui_size. No more extend.
    Property:
        fui_size: The height of FDoubleSpinBox
    """

    def __init__(self, parent=None):
        self._fui_size = forza_theme.default_size
        super(FDoubleSpinBox, self).__init__(parent=parent)

    def get_fui_size(self):
        """
        Get the FDoubleSpinBox height
        :return: integer
        """
        return getattr(self, "_fui_size", forza_theme.default_size)

    def set_fui_size(self, value):
        """
        Set the FDoubleSpinBox size.
        :param value: integer
        :return: None
        """
        self._fui_size = value
        self.style().polish(self)

    fui_size = QtCore.Property(int, get_fui_size, set_fui_size)

    def huge(self):
        """Set FDoubleSpinBox to huge size"""
        self.set_fui_size(forza_theme.huge)
        return self

    def large(self):
        """Set FDoubleSpinBox to large size"""
        self.set_fui_size(forza_theme.large)
        return self

    def medium(self):
        """Set FDoubleSpinBox to  medium"""
        self.set_fui_size(forza_theme.medium)
        return self

    def small(self):
        """Set FDoubleSpinBox to small size"""
        self.set_fui_size(forza_theme.small)
        return self

    def tiny(self):
        """Set FDoubleSpinBox to tiny size"""
        self.set_fui_size(forza_theme.tiny)
        return self


@cursor_mixin
class FDateTimeEdit(QtWidgets.QDateTimeEdit):
    """
    FDateTimeEdit just use stylesheet and add fui_size. No more extend.
    Property:
        fui_size: The height of FDateTimeEdit
    """

    def __init__(self, datetime=None, parent=None):
        self._fui_size = forza_theme.default_size
        if datetime is None:
            super(FDateTimeEdit, self).__init__(parent=parent)
        else:
            super(FDateTimeEdit, self).__init__(datetime, parent=parent)

    def get_fui_size(self):
        """
        Get the FDateTimeEdit height
        :return: integer
        """
        return getattr(self, "_fui_size", forza_theme.default_size)

    def set_fui_size(self, value):
        """
        Set the FDateTimeEdit size.
        :param value: integer
        :return: None
        """
        self._fui_size = value
        self.style().polish(self)

    fui_size = QtCore.Property(int, get_fui_size, set_fui_size)

    def huge(self):
        """Set FDateTimeEdit to huge size"""
        self.set_fui_size(forza_theme.huge)
        return self

    def large(self):
        """Set FDateTimeEdit to large size"""
        self.set_fui_size(forza_theme.large)
        return self

    def medium(self):
        """Set FDateTimeEdit to  medium"""
        self.set_fui_size(forza_theme.medium)
        return self

    def small(self):
        """Set FDateTimeEdit to small size"""
        self.set_fui_size(forza_theme.small)
        return self

    def tiny(self):
        """Set FDateTimeEdit to tiny size"""
        self.set_fui_size(forza_theme.tiny)
        return self


@cursor_mixin
class FDateEdit(QtWidgets.QDateEdit):
    """
    FDateEdit just use stylesheet and add fui_size. No more extend.
    Property:
        fui_size: The height of FDateEdit
    """

    def __init__(self, date=None, parent=None):
        self._fui_size = forza_theme.default_size
        if date is None:
            super(FDateEdit, self).__init__(parent=parent)
        else:
            super(FDateEdit, self).__init__(date, parent=parent)

    def get_fui_size(self):
        """
        Get the FDateEdit height
        :return: integer
        """
        return getattr(self, "_fui_size", forza_theme.default_size)

    def set_fui_size(self, value):
        """
        Set the FDateEdit size.
        :param value: integer
        :return: None
        """
        self._fui_size = value
        self.style().polish(self)

    fui_size = QtCore.Property(int, get_fui_size, set_fui_size)

    def huge(self):
        """Set FDateEdit to huge size"""
        self.set_fui_size(forza_theme.huge)
        return self

    def large(self):
        """Set FDateEdit to large size"""
        self.set_fui_size(forza_theme.large)
        return self

    def medium(self):
        """Set FDateEdit to  medium"""
        self.set_fui_size(forza_theme.medium)
        return self

    def small(self):
        """Set FDateEdit to small size"""
        self.set_fui_size(forza_theme.small)
        return self

    def tiny(self):
        """Set FDateEdit to tiny size"""
        self.set_fui_size(forza_theme.tiny)
        return self


@cursor_mixin
class FTimeEdit(QtWidgets.QTimeEdit):
    """
    FTimeEdit just use stylesheet and add fui_size. No more extend.
    Property:
        fui_size: The height of FTimeEdit
    """

    def __init__(self, time=None, parent=None):
        self._fui_size = forza_theme.default_size
        if time is None:
            super(FTimeEdit, self).__init__(parent=parent)
        else:
            super(FTimeEdit, self).__init__(time, parent=parent)

    def get_fui_size(self):
        """
        Get the FTimeEdit height
        :return: integer
        """
        return getattr(self, "_fui_size", forza_theme.default_size)

    def set_fui_size(self, value):
        """
        Set the FTimeEdit size.
        :param value: integer
        :return: None
        """
        self._fui_size = value
        self.style().polish(self)

    fui_size = QtCore.Property(int, get_fui_size, set_fui_size)

    def huge(self):
        """Set FTimeEdit to huge size"""
        self.set_fui_size(forza_theme.huge)
        return self

    def large(self):
        """Set FTimeEdit to large size"""
        self.set_fui_size(forza_theme.large)
        return self

    def medium(self):
        """Set FTimeEdit to  medium"""
        self.set_fui_size(forza_theme.medium)
        return self

    def small(self):
        """Set FTimeEdit to small size"""
        self.set_fui_size(forza_theme.small)
        return self

    def tiny(self):
        """Set FTimeEdit to tiny size"""
        self.set_fui_size(forza_theme.tiny)
        return self


def _install_spin_paint_api(widget_cls):
    widget_cls._paint_proxies = {}

    @classmethod
    def paint_appearance(
        cls,
        painter,
        rect,
        text: str,
        *,
        fui_size: int | None = None,
        enabled: bool = True,
    ):
        from forza_ui.input.paint_utils import paint_spinbox_appearance

        paint_spinbox_appearance(
            cls,
            cls._paint_proxies,
            painter,
            rect,
            text,
            fui_size=fui_size,
            enabled=enabled,
        )

    @classmethod
    def clear_paint_proxies(cls):
        cls._paint_proxies.clear()

    widget_cls.paint_appearance = paint_appearance
    widget_cls.clear_paint_proxies = clear_paint_proxies


for _spin_cls in (FSpinBox, FDoubleSpinBox, FDateEdit, FDateTimeEdit, FTimeEdit):
    _install_spin_paint_api(_spin_cls)
