"""FProgressCircle"""

# Import third-party modules
from Qt import QtCore, QtGui, QtWidgets

# Import local modules
from forza_ui import forza_theme
from forza_ui import utils
from forza_ui.basic.label import FLabel


class FProgressCircle(QtWidgets.QProgressBar):
    """
    FProgressCircle: Display the current progress of an operation flow.
    When you need to display the completion percentage of an operation.

    Property:
        fui_width: int
        fui_color: str
    """

    def __init__(self, dashboard=False, parent=None):
        super(FProgressCircle, self).__init__(parent)
        self._main_lay = QtWidgets.QHBoxLayout()
        self._default_label = FLabel().h3()
        self._default_label.setAlignment(QtCore.Qt.AlignCenter)
        self._main_lay.addWidget(self._default_label)
        self.setLayout(self._main_lay)
        self._color = None
        self._width = None

        self._start_angle = 90 * 16
        self._max_delta_angle = 360 * 16
        self._height_factor = 1.0
        self._width_factor = 1.0
        if dashboard:
            self._start_angle = 225 * 16
            self._max_delta_angle = 270 * 16
            self._height_factor = (2 + pow(2, 0.5)) / 4 + 0.03

        self.set_fui_width(forza_theme.progress_circle_default_radius)
        self.set_fui_color(forza_theme.primary_color)

    def set_widget(self, widget):
        """
        Set a custom widget to show on the circle's inner center
         and replace the default percent label
        :param widget: QWidget
        :return: None
        """
        self.setTextVisible(False)
        if not widget.styleSheet():
            widget.setStyleSheet("background:transparent")
        self._main_lay.addWidget(widget)

    def get_fui_width(self):
        """
        Get current circle fixed width
        :return: int
        """
        return self._width

    def set_fui_width(self, value):
        """
        Set current circle fixed width
        :param value: int
        :return: None
        """
        self._width = value
        self.setFixedSize(QtCore.QSize(self._width * self._width_factor, self._width * self._height_factor))

    def get_fui_color(self):
        """
        Get current circle foreground color
        :return: str
        """
        return self._color

    def set_fui_color(self, value):
        """
        Set current circle's foreground color
        :param value: str
        :return:
        """
        self._color = value
        self.update()

    fui_color = QtCore.Property(str, get_fui_color, set_fui_color)
    fui_width = QtCore.Property(int, get_fui_width, set_fui_width)

    def paintEvent(self, event):
        """Override QProgressBar's paintEvent."""
        if self.text() != self._default_label.text():
            self._default_label.setText(self.text())
        if self.isTextVisible() != self._default_label.isVisible():
            self._default_label.setVisible(self.isTextVisible())

        percent = utils.get_percent(self.value(), self.minimum(), self.maximum())
        total_width = self.get_fui_width()
        pen_width = int(3 * total_width / 50.0)
        radius = total_width - pen_width - 1

        painter = QtGui.QPainter(self)
        painter.setRenderHints(QtGui.QPainter.Antialiasing)

        # draw background circle
        pen_background = QtGui.QPen()
        pen_background.setWidth(pen_width)
        pen_background.setColor(QtGui.QColor(forza_theme.background_selected_color))
        pen_background.setCapStyle(QtCore.Qt.RoundCap)
        painter.setPen(pen_background)
        painter.drawArc(
            pen_width / 2.0 + 1,
            pen_width / 2.0 + 1,
            radius,
            radius,
            self._start_angle,
            -self._max_delta_angle,
        )

        # draw foreground circle
        pen_foreground = QtGui.QPen()
        pen_foreground.setWidth(pen_width)
        pen_foreground.setColor(QtGui.QColor(self._color))
        pen_foreground.setCapStyle(QtCore.Qt.RoundCap)
        painter.setPen(pen_foreground)
        painter.drawArc(
            pen_width / 2.0 + 1,
            pen_width / 2.0 + 1,
            radius,
            radius,
            self._start_angle,
            -percent * 0.01 * self._max_delta_angle,
        )
        painter.end()

    @classmethod
    def dashboard(cls, parent=None):
        """Create a dashboard style MCircle"""
        return FProgressCircle(dashboard=True, parent=parent)
