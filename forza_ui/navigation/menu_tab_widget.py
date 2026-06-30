"""A Navigation menu"""

# Import third-party modules
from Qt import QtCore, QtWidgets

# Import local modules
from forza_ui import forza_theme
from forza_ui.input.button_group import MButtonGroupBase
from forza_ui.basic.divider import FDivider
from forza_ui.input.tool_button import FToolButton


class FBlockButton(FToolButton):
    """FBlockButton"""

    def __init__(self, parent=None):
        super(FBlockButton, self).__init__(parent)
        self.setCheckable(True)


class FBlockButtonGroup(MButtonGroupBase):
    """FBlockButtonGroup"""

    sig_checked_changed = QtCore.Signal(int)

    def __init__(self, tab, orientation=QtCore.Qt.Horizontal, parent=None):
        super(FBlockButtonGroup, self).__init__(orientation=orientation, parent=parent)
        self.set_spacing(1)
        self._menu_tab = tab
        self._button_group.setExclusive(True)
        self._button_group.idClicked.connect(self.sig_checked_changed)

    def create_button(self, data_dict):
        button = FBlockButton()
        if data_dict.get("svg"):
            button.svg(data_dict.get("svg"))
        if data_dict.get("text"):
            if data_dict.get("svg") or data_dict.get("icon"):
                button.text_beside_icon()
            else:
                button.text_only()
        else:
            button.icon_only()
        button.set_fui_size(self._menu_tab.get_fui_size())
        return button

    def update_size(self, size):
        for button in self._button_group.buttons():
            button.set_fui_size(size)

    def set_fui_checked(self, value):
        """Set current checked button's id"""
        button = self._button_group.button(value)
        button.setChecked(True)
        self.sig_checked_changed.emit(value)

    def get_fui_checked(self):
        """Get current checked button's id"""
        return self._button_group.checkedId()

    fui_checked = QtCore.Property(int, get_fui_checked, set_fui_checked, notify=sig_checked_changed)


class FMenuTabWidget(QtWidgets.QWidget):
    """FMenuTabWidget"""

    def __init__(self, orientation=QtCore.Qt.Horizontal, parent=None):
        super(FMenuTabWidget, self).__init__(parent=parent)
        self.tool_button_group = FBlockButtonGroup(tab=self, orientation=orientation)

        if orientation == QtCore.Qt.Horizontal:
            self._bar_layout = QtWidgets.QHBoxLayout()
            self._bar_layout.setContentsMargins(10, 0, 10, 0)
        else:
            self._bar_layout = QtWidgets.QVBoxLayout()
            self._bar_layout.setContentsMargins(0, 0, 0, 0)

        self._bar_layout.addWidget(self.tool_button_group)
        self._bar_layout.addStretch()
        bar_widget = QtWidgets.QWidget()
        bar_widget.setObjectName("bar_widget")
        bar_widget.setLayout(self._bar_layout)
        bar_widget.setAttribute(QtCore.Qt.WA_StyledBackground)
        main_lay = QtWidgets.QVBoxLayout()
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.setSpacing(0)
        main_lay.addWidget(bar_widget)

        if orientation == QtCore.Qt.Horizontal:
            main_lay.addWidget(FDivider())

        main_lay.addSpacing(5)
        self.setLayout(main_lay)
        self._fui_size = forza_theme.large

    def tool_bar_append_widget(self, widget):
        """Add the widget too menubar's right position."""
        self._bar_layout.addWidget(widget)

    def tool_bar_insert_widget(self, widget):
        """Insert the widget to menubar's left position."""
        self._bar_layout.insertWidget(0, widget)

    def add_menu(self, data_dict, index=None):
        """Add a menu"""
        self.tool_button_group.add_button(data_dict, index)

    def get_fui_size(self):
        """
        Get the menu tab size.
        :return: integer
        """
        return self._fui_size

    def set_fui_size(self, value):
        """
        Set the menu tab size.
        :param value: integer
        :return: None
        """
        self._fui_size = value
        self.tool_button_group.update_size(self._fui_size)
        self.style().polish(self)

    fui_size = QtCore.Property(int, get_fui_size, set_fui_size)
