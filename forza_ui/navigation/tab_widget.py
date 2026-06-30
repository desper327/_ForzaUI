# Import third-party modules
from Qt import QtCore, QtWidgets

# Import local modules
from forza_ui.mixin import cursor_mixin
from forza_ui.mixin import stacked_animation_mixin
from forza_ui import utils


@cursor_mixin
class FTabBar(QtWidgets.QTabBar):
    def __init__(self, parent=None):
        super(FTabBar, self).__init__(parent=parent)
        self.setDrawBase(False)

    def tabSizeHint(self, index):
        tab_text = self.tabText(index)
        if self.tabsClosable():
            return QtCore.QSize(
                utils.text_width(self.fontMetrics(), tab_text) + 70,
                self.fontMetrics().height() + 20,
            )
        else:
            return QtCore.QSize(
                utils.text_width(self.fontMetrics(), tab_text) + 50,
                self.fontMetrics().height() + 20,
            )


@stacked_animation_mixin
class FTabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super(FTabWidget, self).__init__(parent=parent)
        self.bar = FTabBar()
        self.setTabBar(self.bar)

    def disable_animation(self):
        self.currentChanged.disconnect(self._play_anim)
