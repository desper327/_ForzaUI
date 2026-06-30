"""FSlider"""

# Import third-party modules
from Qt import QtCore, QtWidgets


class FSlider(QtWidgets.QSlider):
    """
    A Slider component for displaying current value and intervals in range.

    FSlider just apply qss for QSlider.
    """

    def __init__(self, orientation=QtCore.Qt.Horizontal, parent=None):
        super(FSlider, self).__init__(orientation, parent=parent)
        self._show_text_when_move = True

    def disable_show_text(self):
        self._show_text_when_move = False

    def mouseMoveEvent(self, event):
        """Override the mouseMoveEvent to show current value as a tooltip."""
        if self._show_text_when_move:
            QtWidgets.QToolTip.showText(event.globalPos(), str(self.value()), self)
        return super(FSlider, self).mouseMoveEvent(event)

    # def mousePressEvent(self, event):
    #     """Override the mousePressEvent to show current value as a tooltip."""
    #     if self._show_text_when_move:
    #         QtWidgets.QToolTip.showText(event.globalPos(), str(self.value()), self)
    #     return super(FSlider, self).mousePressEvent(event)