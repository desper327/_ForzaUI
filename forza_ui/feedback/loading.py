"""
FLoading
"""

# Import third-party modules
from Qt import QtCore, QtGui, QtWidgets

# Import local modules
from forza_ui import forza_theme
from forza_ui.icons import FPixmap


class FLoading(QtWidgets.QWidget):
    """
    Show a loading animation image.
    """

    def __init__(self, size=None, color=None, parent=None):
        super(FLoading, self).__init__(parent)
        size = size or forza_theme.default_size
        self.setFixedSize(QtCore.QSize(size, size))
        self.pix = FPixmap("loading.svg", color or forza_theme.primary_color).scaledToWidth(
            size, QtCore.Qt.SmoothTransformation
        )
        self._rotation = 0
        self._loading_ani = QtCore.QPropertyAnimation()
        self._loading_ani.setTargetObject(self)
        # self.loading_ani.setEasingCurve(QEasingCurve.InOutQuad)
        self._loading_ani.setDuration(1000)
        self._loading_ani.setPropertyName(b"rotation")
        self._loading_ani.setStartValue(0)
        self._loading_ani.setEndValue(360)
        self._loading_ani.setLoopCount(-1)
        self._loading_ani.start()

    def _set_rotation(self, value):
        self._rotation = value
        self.update()

    def _get_rotation(self):
        return self._rotation

    rotation = QtCore.Property(int, _get_rotation, _set_rotation)

    def paintEvent(self, event):
        """override the paint event to paint the 1/4 circle image."""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        painter.translate(self.pix.width() / 2, self.pix.height() / 2)
        painter.rotate(self._rotation)
        painter.drawPixmap(
            -self.pix.width() / 2,
            -self.pix.height() / 2,
            self.pix.width(),
            self.pix.height(),
            self.pix,
        )
        painter.end()
        return super(FLoading, self).paintEvent(event)

    @classmethod
    def huge(cls, color=None):
        """Create a FLoading with huge size"""
        return cls(forza_theme.huge, color)

    @classmethod
    def large(cls, color=None):
        """Create a FLoading with large size"""
        return cls(forza_theme.large, color)

    @classmethod
    def medium(cls, color=None):
        """Create a FLoading with medium size"""
        return cls(forza_theme.medium, color)

    @classmethod
    def small(cls, color=None):
        """Create a FLoading with small size"""
        return cls(forza_theme.small, color)

    @classmethod
    def tiny(cls, color=None):
        """Create a FLoading with tiny size"""
        return cls(forza_theme.tiny, color)


class FLoadingWrapper(QtWidgets.QWidget):
    """
    A wrapper widget to show the loading widget or hide.
    Property:
        fui_loading: bool. current loading state.
    """

    def __init__(self, widget, loading=True, parent=None):
        super(FLoadingWrapper, self).__init__(parent)
        self._widget = widget
        self._mask_widget = QtWidgets.QFrame()
        self._mask_widget.setObjectName("mask")
        policy = QtWidgets.QSizePolicy.Expanding
        self._mask_widget.setSizePolicy(policy, policy)
        self._loading_widget = FLoading()
        self._loading_widget.setSizePolicy(policy, policy)

        self._main_lay = QtWidgets.QGridLayout()
        self._main_lay.setContentsMargins(0, 0, 0, 0)
        self._main_lay.addWidget(widget, 0, 0)
        self._main_lay.addWidget(self._mask_widget, 0, 0)
        self._main_lay.addWidget(self._loading_widget, 0, 0, QtCore.Qt.AlignCenter)
        self.setLayout(self._main_lay)
        self._loading = None
        self.set_fui_loading(loading)

    def _set_loading(self):
        self._loading_widget.setVisible(self._loading)
        self._mask_widget.setVisible(self._loading)

    def set_fui_loading(self, loading):
        """
        Set current state to loading or not
        :param loading: bool
        :return: None
        """
        self._loading = loading
        self._set_loading()

    def get_fui_loading(self):
        """
        Get current loading widget is loading or not.
        :return: bool
        """
        return self._loading

    fui_loading = QtCore.Property(bool, get_fui_loading, set_fui_loading)
