"""
FToast
"""

# Import third-party modules
from Qt import QtCore, QtWidgets

# Import local modules
from forza_ui import forza_theme
from forza_ui.basic.avatar import FAvatar
from forza_ui.basic.label import FLabel
from forza_ui.feedback.loading import FLoading
from forza_ui.icons import FPixmap


class FToast(QtWidgets.QWidget):
    """
    FToast
    A Phone style message.
    """

    InfoType = "info"
    SuccessType = "success"
    WarningType = "warning"
    ErrorType = "error"
    LoadingType = "loading"

    default_config = {
        "duration": 2,
    }

    sig_closed = QtCore.Signal()

    def __init__(self, text, duration=None, fui_type=None, parent=None):
        super(FToast, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Dialog)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)

        _icon_lay = QtWidgets.QHBoxLayout()
        _icon_lay.addStretch()

        if fui_type == FToast.LoadingType:
            _icon_lay.addWidget(FLoading(size=forza_theme.huge, color=forza_theme.text_color_inverse))
        else:
            _icon_label = FAvatar()
            _icon_label.set_fui_size(forza_theme.toast_icon_size)
            _icon_label.set_fui_image(
                FPixmap(
                    "{}_line.svg".format(fui_type or FToast.InfoType),
                    forza_theme.text_color_inverse,
                )
            )
            _icon_lay.addWidget(_icon_label)
        _icon_lay.addStretch()

        _content_label = FLabel()
        _content_label.setText(text)
        _content_label.setAlignment(QtCore.Qt.AlignCenter)

        _main_lay = QtWidgets.QVBoxLayout()
        _main_lay.setContentsMargins(0, 0, 0, 0)
        _main_lay.addStretch()
        _main_lay.addLayout(_icon_lay)
        _main_lay.addSpacing(10)
        _main_lay.addWidget(_content_label)
        _main_lay.addStretch()
        self.setLayout(_main_lay)
        self.setFixedSize(QtCore.QSize(forza_theme.toast_size, forza_theme.toast_size))

        _close_timer = QtCore.QTimer(self)
        _close_timer.setSingleShot(True)
        _close_timer.timeout.connect(self.close)
        _close_timer.timeout.connect(self.sig_closed)
        _close_timer.setInterval((duration or self.default_config.get("duration")) * 1000)
        self.has_played = False

        if fui_type != FToast.LoadingType:
            _close_timer.start()

        self._opacity_ani = QtCore.QPropertyAnimation()
        self._opacity_ani.setTargetObject(self)
        self._opacity_ani.setDuration(300)
        self._opacity_ani.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self._opacity_ani.setPropertyName(b"windowOpacity")
        self._opacity_ani.setStartValue(0.0)
        self._opacity_ani.setEndValue(0.9)

        self._get_center_position(parent)
        self._fade_int()

    def closeEvent(self, event):
        if self.has_played:
            event.accept()
        else:
            self._fade_out()
            event.ignore()

    def _fade_out(self):
        self.has_played = True
        self._opacity_ani.setDirection(QtCore.QAbstractAnimation.Backward)
        self._opacity_ani.finished.connect(self.close)
        self._opacity_ani.start()

    def _fade_int(self):
        self._opacity_ani.start()

    def _get_center_position(self, parent):
        parent_geo = parent.geometry()
        pos = parent_geo.topLeft() if parent.parent() is None else parent.mapToGlobal(parent_geo.topLeft())
        offset = 0
        for child in parent.children():
            if isinstance(child, FToast) and child.isVisible():
                offset = max(offset, child.y())
        target_x = pos.x() + parent_geo.width() / 2 - self.width() / 2
        target_y = pos.y() + parent_geo.height() / 2 - self.height() / 2
        self.setProperty("pos", QtCore.QPoint(target_x, target_y))

    @classmethod
    def info(cls, text, parent, duration=None):
        """Show a normal toast message"""
        inst = cls(text, duration=duration, fui_type=FToast.InfoType, parent=parent)
        inst.show()
        return inst

    @classmethod
    def success(cls, text, parent, duration=None):
        """Show a success toast message"""
        inst = cls(text, duration=duration, fui_type=FToast.SuccessType, parent=parent)
        inst.show()
        return inst

    @classmethod
    def warning(cls, text, parent, duration=None):
        """Show a warning toast message"""
        inst = cls(text, duration=duration, fui_type=FToast.WarningType, parent=parent)
        inst.show()
        return inst

    @classmethod
    def error(cls, text, parent, duration=None):
        """Show an error toast message"""
        inst = cls(text, duration=duration, fui_type=FToast.ErrorType, parent=parent)
        inst.show()
        return inst

    @classmethod
    def loading(cls, text, parent):
        """Show a toast message with loading animation.
        You should close this widget by yourself."""
        inst = cls(text, fui_type=FToast.LoadingType, parent=parent)
        inst.show()
        return inst

    @classmethod
    def config(cls, duration):
        """
        Config the global FToast duration setting.
        :param duration: int (unit is second)
        :return: None
        """
        if duration is not None:
            cls.default_config["duration"] = duration
