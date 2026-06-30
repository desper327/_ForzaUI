"""
FRadioButton
"""

# Import third-party modules
from Qt import QtWidgets

# Import local modules
from forza_ui.mixin import cursor_mixin


@cursor_mixin
class FRadioButton(QtWidgets.QRadioButton):
    """
    FRadioButton just use stylesheet and set cursor shape when hover. No more extend.
    """

    def __init__(self, text="", parent=None):
        super(FRadioButton, self).__init__(text=text, parent=parent)
