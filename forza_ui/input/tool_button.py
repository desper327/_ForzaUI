"""FToolButton"""

# Import third-party modules
from Qt import QtCore, QtWidgets

# Import local modules
from forza_ui import forza_theme
from forza_ui.mixin import cursor_mixin
from forza_ui.icons import FIcon


@cursor_mixin
class FToolButton(QtWidgets.QToolButton):
    """FToolButton"""

    def __init__(self, parent=None):
        super(FToolButton, self).__init__(parent=parent)
        self._fui_svg = None
        self.setAutoExclusive(False)
        self.setAutoRaise(True)

        self._polish_icon()
        self.toggled.connect(self._polish_icon)
        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

        self._fui_size = forza_theme.default_size

    @QtCore.Slot(bool)
    def _polish_icon(self, checked=None):
        if self._fui_svg:
            if self.isCheckable() and self.isChecked():
                self.setIcon(FIcon(self._fui_svg, forza_theme.primary_color))
            else:
                self.setIcon(FIcon(self._fui_svg))

    def enterEvent(self, event):
        """Override enter event to highlight the icon"""
        if self._fui_svg:
            self.setIcon(FIcon(self._fui_svg, forza_theme.primary_color))
        return super(FToolButton, self).enterEvent(event)

    def leaveEvent(self, event):
        """Override leave event to recover the icon"""
        self._polish_icon()
        return super(FToolButton, self).leaveEvent(event)

    def get_fui_size(self):
        """
        Get the tool button height
        :return: integer
        """
        return self._fui_size

    def set_fui_size(self, value):
        """
        Set the tool button size.
        :param value: integer
        :return: None
        """
        self._fui_size = value
        self.style().polish(self)
        if self.toolButtonStyle() == QtCore.Qt.ToolButtonIconOnly:
            self.setFixedSize(QtCore.QSize(self._fui_size, self._fui_size))
            self.setIconSize(QtCore.QSize(self._fui_size, self._fui_size))

    def get_fui_svg(self):
        """Get current svg path"""
        return self._fui_svg

    def set_fui_svg(self, path):
        """Set current svg path"""
        self._fui_svg = path
        self._polish_icon()

    fui_size = QtCore.Property(int, get_fui_size, set_fui_size)

    def huge(self):
        """Set FToolButton to huge size"""
        self.set_fui_size(forza_theme.huge)
        return self

    def large(self):
        """Set FToolButton to large size"""
        self.set_fui_size(forza_theme.large)
        return self

    def medium(self):
        """Set FToolButton to  medium size"""
        self.set_fui_size(forza_theme.medium)
        return self

    def small(self):
        """Set FToolButton to small size"""
        self.set_fui_size(forza_theme.small)
        return self

    def tiny(self):
        """Set FToolButton to tiny size"""
        self.set_fui_size(forza_theme.tiny)
        return self

    def svg(self, path):
        """Set current svg path"""
        self.set_fui_svg(path)
        return self

    def icon_only(self):
        """Set tool button style to icon only"""
        self.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.setFixedSize(QtCore.QSize(self._fui_size, self._fui_size))
        return self

    def text_only(self):
        """Set tool button style to text only"""
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        return self

    def text_beside_icon(self):
        """Set tool button style to text beside icon"""
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        return self

    def text_under_icon(self):
        """Set tool button style to text under icon"""
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        return self
