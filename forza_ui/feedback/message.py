"""FMessage"""

# Import third-party modules
from Qt import QtCore, QtWidgets

# Import local modules
from forza_ui import forza_theme
from forza_ui.basic.avatar import FAvatar
from forza_ui.basic.label import FLabel
from forza_ui.feedback.loading import FLoading
from forza_ui.icons import FPixmap
from forza_ui.input.tool_button import FToolButton


class FMessage(QtWidgets.QWidget):
    """
    Display global messages as feedback in response to user operations.
    """

    InfoType = "info"
    SuccessType = "success"
    WarningType = "warning"
    ErrorType = "error"
    LoadingType = "loading"

    default_config = {"duration": 2, "top": 24}

    sig_closed = QtCore.Signal()

    def __init__(self, text, duration=None, fui_type=None, closable=False, parent=None):
        super(FMessage, self).__init__(parent)
        self.setObjectName("message")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Dialog)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)

        if fui_type == FMessage.LoadingType:
            _icon_label = FLoading.tiny()
        else:
            _icon_label = FAvatar.tiny()
            current_type = fui_type or FMessage.InfoType
            _icon_label.set_fui_image(
                FPixmap(
                    "{}_fill.svg".format(current_type),
                    vars(forza_theme).get(current_type + "_color"),
                )
            )

        self._content_label = FLabel(parent=self)
        # self._content_label.set_elide_mode(Qt.ElideMiddle)
        self._content_label.setText(text)

        self._close_button = FToolButton(parent=self).icon_only().svg("close_line.svg").tiny()
        self._close_button.clicked.connect(self.close)
        self._close_button.setVisible(closable or False)

        self._main_lay = QtWidgets.QHBoxLayout()
        self._main_lay.addWidget(_icon_label)
        self._main_lay.addWidget(self._content_label)
        self._main_lay.addStretch()
        self._main_lay.addWidget(self._close_button)
        self.setLayout(self._main_lay)

        _close_timer = QtCore.QTimer(self)
        _close_timer.setSingleShot(True)
        _close_timer.timeout.connect(self.close)
        _close_timer.timeout.connect(self.sig_closed)
        _close_timer.setInterval((duration or self.default_config.get("duration")) * 1000)

        _ani_timer = QtCore.QTimer(self)
        _ani_timer.timeout.connect(self._fade_out)
        _ani_timer.setInterval((duration or self.default_config.get("duration")) * 1000 - 300)

        _close_timer.start()
        _ani_timer.start()

        self._pos_ani = QtCore.QPropertyAnimation(self)
        self._pos_ani.setTargetObject(self)
        self._pos_ani.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self._pos_ani.setDuration(300)
        self._pos_ani.setPropertyName(b"pos")

        self._opacity_ani = QtCore.QPropertyAnimation()
        self._opacity_ani.setTargetObject(self)
        self._opacity_ani.setDuration(300)
        self._opacity_ani.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self._opacity_ani.setPropertyName(b"windowOpacity")
        self._opacity_ani.setStartValue(0.0)
        self._opacity_ani.setEndValue(1.0)

        self._set_proper_position(parent)
        self._fade_in()

    def _fade_out(self):
        self._pos_ani.setDirection(QtCore.QAbstractAnimation.Backward)
        self._pos_ani.start()
        self._opacity_ani.setDirection(QtCore.QAbstractAnimation.Backward)
        self._opacity_ani.start()

    def _fade_in(self):
        self._pos_ani.start()
        self._opacity_ani.start()

    def _set_proper_position(self, parent):
        parent_geo = parent.geometry()
        pos = parent_geo.topLeft() if parent.parent() is None else parent.mapToGlobal(parent_geo.topLeft())
        offset = 0
        for child in parent.children():
            if isinstance(child, FMessage) and child.isVisible():
                offset = max(offset, child.y())
        base = pos.y() + FMessage.default_config.get("top")
        target_x = pos.x() + parent_geo.width() / 2 - 100
        target_y = (offset + 50) if offset else base
        self._pos_ani.setStartValue(QtCore.QPoint(target_x, target_y - 40))
        self._pos_ani.setEndValue(QtCore.QPoint(target_x, target_y))

    @classmethod
    def info(cls, text, parent, duration=None, closable=None):
        """Show a normal message"""
        inst = cls(
            text,
            fui_type=FMessage.InfoType,
            duration=duration,
            closable=closable,
            parent=parent,
        )
        inst.show()
        return inst

    @classmethod
    def success(cls, text, parent, duration=None, closable=None):
        """Show a success message"""
        inst = cls(
            text,
            fui_type=FMessage.SuccessType,
            duration=duration,
            closable=closable,
            parent=parent,
        )

        inst.show()
        return inst

    @classmethod
    def warning(cls, text, parent, duration=None, closable=None):
        """Show a warning message"""
        inst = cls(
            text,
            fui_type=FMessage.WarningType,
            duration=duration,
            closable=closable,
            parent=parent,
        )
        inst.show()
        return inst

    @classmethod
    def error(cls, text, parent, duration=None, closable=None):
        """Show an error message"""
        inst = cls(
            text,
            fui_type=FMessage.ErrorType,
            duration=duration,
            closable=closable,
            parent=parent,
        )
        inst.show()
        return inst

    @classmethod
    def loading(cls, text, parent):
        """Show a message with loading animation"""
        inst = cls(text, fui_type=FMessage.LoadingType, parent=parent)
        inst.show()
        return inst

    @classmethod
    def config(cls, duration=None, top=None):
        """
        Config the global FMessage duration and top setting.
        :param duration: int (unit is second)
        :param top: int (unit is px)
        :return: None
        """
        if duration is not None:
            cls.default_config["duration"] = duration
        if top is not None:
            cls.default_config["top"] = top
