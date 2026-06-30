"""FStackedWidget"""

# Import third-party modules
from Qt import QtWidgets

# Import local modules
from forza_ui.mixin import stacked_animation_mixin


@stacked_animation_mixin
class FStackedWidget(QtWidgets.QStackedWidget):
    """Just active animation when current index changed."""

    def __init__(self, parent=None):
        super(FStackedWidget, self).__init__(parent)

    def disable_animation(self):
        self.currentChanged.disconnect(self._play_anim)
