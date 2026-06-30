"""FDockWidget"""

# Import third-party modules
from Qt import QtCore, QtWidgets


class FDockWidget(QtWidgets.QDockWidget):
    """
    Just apply the qss. No more extend.
    """

    def __init__(self, title="", parent=None, flags=QtCore.Qt.Widget):
        super(FDockWidget, self).__init__(title, parent=parent, flags=flags)
