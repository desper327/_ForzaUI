"""
FAlert class.
"""

# Import built-in modules
import functools

# Import third-party modules
from Qt import QtCore, QtWidgets

# Import local modules
from forza_ui import forza_theme
from forza_ui.basic.avatar import FAvatar
from forza_ui.basic.label import FLabel
from forza_ui.mixin import property_mixin
from forza_ui.icons import FPixmap
from forza_ui.icons import get_scale_factor
from forza_ui.input.tool_button import FToolButton


@property_mixin
class FAlert(QtWidgets.QWidget):
    """
    Alert component for feedback.

    Property:
        fui_type: The feedback type with different color container.
        fui_text: The feedback string showed in container.
    """

    InfoType = "info"
    SuccessType = "success"
    WarningType = "warning"
    ErrorType = "error"

    def __init__(self, text="", parent=None, flags=QtCore.Qt.Widget):
        super(FAlert, self).__init__(parent, flags)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self._icon_label = FAvatar()
        self._icon_label.set_fui_size(forza_theme.tiny)
        self._content_label = FLabel().secondary()
        self._close_button = FToolButton().svg("close_line.svg").tiny().icon_only()
        self._close_button.clicked.connect(functools.partial(self.setVisible, False))

        scale_x, _ = get_scale_factor()
        margin = 8 * scale_x

        self._main_lay = QtWidgets.QHBoxLayout()
        self._main_lay.setContentsMargins(margin, margin, margin, margin)
        self._main_lay.addWidget(self._icon_label)
        self._main_lay.addWidget(self._content_label)
        self._main_lay.addStretch()
        self._main_lay.addWidget(self._close_button)

        self.setLayout(self._main_lay)
        self.set_show_icon(True)
        self.set_closable(False)

        self._fui_type = None
        self._fui_text = None
        self.set_fui_type(FAlert.InfoType)
        self.set_fui_text(text)

    def set_closable(self, closable):
        """Display the close icon button or not."""
        self._close_button.setVisible(closable)

    def set_show_icon(self, show_icon):
        """Display the information type icon or not."""
        self._icon_label.setVisible(show_icon)

    def _set_fui_text(self):
        self._content_label.setText(self._fui_text)
        self.setVisible(bool(self._fui_text))

    def set_fui_text(self, value):
        """Set the feedback content."""

        if isinstance(value, str):
            self._fui_text = value
        else:
            msg = "Input argument 'value' should be string type, but get {}"
            raise TypeError(msg.format(type(value)))
        self._set_fui_text()

    def _set_fui_type(self):
        self._icon_label.set_fui_image(
            FPixmap(
                "{}_fill.svg".format(self._fui_type),
                vars(forza_theme).get(self._fui_type + "_color"),
            )
        )
        self.style().polish(self)

    def set_fui_type(self, value):
        """Set feedback type."""
        valid_types = [
            FAlert.InfoType,
            FAlert.SuccessType,
            FAlert.WarningType,
            FAlert.ErrorType,
        ]
        if value in valid_types:
            self._fui_type = value
        else:
            msg = "Input argument 'value' should be one of info/success/warning/error string."
            raise ValueError(msg)
        self._set_fui_type()

    def get_fui_type(self):
        """
        Get FAlert feedback type.
        :return: str
        """
        return self._fui_type

    def get_fui_text(self):
        """
        Get FAlert feedback message.
        :return: str
        """
        return self._fui_text

    fui_text = QtCore.Property(str, get_fui_text, set_fui_text)
    fui_type = QtCore.Property(str, get_fui_type, set_fui_type)

    def info(self):
        """Set FAlert to InfoType"""
        self.set_fui_type(FAlert.InfoType)
        return self

    def success(self):
        """Set FAlert to SuccessType"""
        self.set_fui_type(FAlert.SuccessType)
        return self

    def warning(self):
        """Set FAlert to  WarningType"""
        self.set_fui_type(FAlert.WarningType)
        return self

    def error(self):
        """Set FAlert to ErrorType"""
        self.set_fui_type(FAlert.ErrorType)
        return self

    def closable(self):
        """Set FAlert closebale is True"""
        self.set_closable(True)
        return self
