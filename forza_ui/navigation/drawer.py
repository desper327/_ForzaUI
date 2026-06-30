"""FDrawer"""

# Import third-party modules
from Qt import QtCore, QtWidgets

# Import local modules
from forza_ui.basic.divider import FDivider
from forza_ui.basic.label import FLabel
from forza_ui.icons import get_scale_factor
from forza_ui.input.tool_button import FToolButton


class FDrawer(QtWidgets.QWidget):
    """
    A panel which slides in from the edge of the screen.
    """

    LeftPos = "left"
    RightPos = "right"
    TopPos = "top"
    BottomPos = "bottom"

    sig_closed = QtCore.Signal()

    def __init__(self, title, position="right", closable=True, parent=None):
        super(FDrawer, self).__init__(parent)
        self.setObjectName("message")
        self.setWindowFlags(QtCore.Qt.Popup)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)

        self._title_label = FLabel(parent=self).h4()
        self._title_label.setText(title)

        self._close_button = FToolButton(parent=self).icon_only().svg("close_line.svg").small()
        self._close_button.clicked.connect(self._request_close)
        self._close_button.setVisible(closable or False)

        self._title_extra_lay = QtWidgets.QHBoxLayout()
        _title_lay = QtWidgets.QHBoxLayout()
        _title_lay.addWidget(self._title_label)
        _title_lay.addStretch()
        _title_lay.addLayout(self._title_extra_lay)
        _title_lay.addWidget(self._close_button)
        self._bottom_lay = QtWidgets.QHBoxLayout()
        self._bottom_lay.addStretch()

        self._scroll_area = QtWidgets.QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._main_lay = QtWidgets.QVBoxLayout()
        self._main_lay.addLayout(_title_lay)
        self._main_lay.addWidget(FDivider())
        self._main_lay.addWidget(self._scroll_area)
        self._main_lay.addWidget(FDivider())
        self._main_lay.addLayout(self._bottom_lay)
        self.setLayout(self._main_lay)

        self._position = position
        self._closing = False

        self._close_timer = QtCore.QTimer(self)
        self._close_timer.setSingleShot(True)
        self._close_timer.timeout.connect(self._finish_close)
        self._close_timer.setInterval(300)

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

    def set_widget(self, widget):
        self._scroll_area.setWidget(widget)

    def add_widget_to_bottom(self, button):
        self._bottom_lay.addWidget(button)

    def add_widget_to_top(self, button):
        self._title_extra_lay.addWidget(button)

    def _reset_open_state(self) -> None:
        self._close_timer.stop()
        self._closing = False
        self._pos_ani.setDirection(QtCore.QAbstractAnimation.Forward)
        self._opacity_ani.setDirection(QtCore.QAbstractAnimation.Forward)
        self.setWindowOpacity(1.0)

    def _fade_out(self):
        self._pos_ani.setDirection(QtCore.QAbstractAnimation.Backward)
        self._pos_ani.start()
        self._opacity_ani.setDirection(QtCore.QAbstractAnimation.Backward)
        self._opacity_ani.start()

    def _fade_in(self):
        self._pos_ani.setDirection(QtCore.QAbstractAnimation.Forward)
        self._opacity_ani.setDirection(QtCore.QAbstractAnimation.Forward)
        self._pos_ani.start()
        self._opacity_ani.start()

    def _set_proper_position(self):
        parent = self.parent()
        if parent is None:
            return
        parent_geo = parent.geometry()
        if self._position == FDrawer.LeftPos:
            pos = (
                parent_geo.topLeft()
                if parent.parent() is None
                else parent.mapToGlobal(parent_geo.topLeft())
            )
            target_x = pos.x()
            target_y = pos.y()
            self.setFixedHeight(parent_geo.height())
            self._pos_ani.setStartValue(QtCore.QPoint(target_x - self.width(), target_y))
            self._pos_ani.setEndValue(QtCore.QPoint(target_x, target_y))
        if self._position == FDrawer.RightPos:
            pos = (
                parent_geo.topRight()
                if parent.parent() is None
                else parent.mapToGlobal(parent_geo.topRight())
            )
            self.setFixedHeight(parent_geo.height())
            target_x = pos.x() - self.width()
            target_y = pos.y()
            self._pos_ani.setStartValue(QtCore.QPoint(target_x + self.width(), target_y))
            self._pos_ani.setEndValue(QtCore.QPoint(target_x, target_y))
        if self._position == FDrawer.TopPos:
            pos = (
                parent_geo.topLeft()
                if parent.parent() is None
                else parent.mapToGlobal(parent_geo.topLeft())
            )
            self.setFixedWidth(parent_geo.width())
            target_x = pos.x()
            target_y = pos.y()
            self._pos_ani.setStartValue(QtCore.QPoint(target_x, target_y - self.height()))
            self._pos_ani.setEndValue(QtCore.QPoint(target_x, target_y))
        if self._position == FDrawer.BottomPos:
            pos = (
                parent_geo.bottomLeft()
                if parent.parent() is None
                else parent.mapToGlobal(parent_geo.bottomLeft())
            )
            self.setFixedWidth(parent_geo.width())
            target_x = pos.x()
            target_y = pos.y() - self.height()
            self._pos_ani.setStartValue(QtCore.QPoint(target_x, target_y + self.height()))
            self._pos_ani.setEndValue(QtCore.QPoint(target_x, target_y))

    def set_fui_position(self, value):
        """
        Set the placement of the FDrawer.
        top/right/bottom/left, default is right
        :param value: str
        :return: None
        """
        self._position = value
        scale_x, _ = get_scale_factor()
        if value in [FDrawer.BottomPos, FDrawer.TopPos]:
            self.setFixedHeight(200 * scale_x)
        else:
            self.setFixedWidth(200 * scale_x)

    def get_fui_position(self):
        """
        Get the placement of the FDrawer
        :return: str
        """
        return self._position

    fui_position = QtCore.Property(str, get_fui_position, set_fui_position)

    def left(self):
        """Set drawer's placement to left"""
        self.set_fui_position(FDrawer.LeftPos)
        return self

    def right(self):
        """Set drawer's placement to right"""
        self.set_fui_position(FDrawer.RightPos)
        return self

    def top(self):
        """Set drawer's placement to top"""
        self.set_fui_position(FDrawer.TopPos)
        return self

    def bottom(self):
        """Set drawer's placement to bottom"""
        self.set_fui_position(FDrawer.BottomPos)
        return self

    def open(self):
        """Show drawer with slide-in animation; refresh position if already visible."""
        self._reset_open_state()
        self._set_proper_position()
        self._fade_in()
        super(FDrawer, self).show()
        self.activateWindow()
        self.raise_()

    def toggle(self):
        """Open if hidden; otherwise start animated close."""
        if self.isVisible() and not self._closing:
            self._request_close()
        else:
            self.open()

    def show(self):
        """Alias for open() to keep backward compatibility."""
        self.open()

    def _request_close(self):
        if self._closing:
            return
        self._closing = True
        self._close_timer.stop()
        self._close_timer.start()
        self._fade_out()

    def _finish_close(self):
        self.hide()
        self._closing = False
        self.sig_closed.emit()

    def closeEvent(self, event):
        if self._closing:
            event.accept()
            return
        event.ignore()
        self._request_close()
