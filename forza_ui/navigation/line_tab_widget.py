"""FLineTabWidget"""

# Import third-party modules
from Qt import QtCore, QtWidgets

# Import local modules
from forza_ui import forza_theme
from forza_ui.input.button_group import MButtonGroupBase
from forza_ui.basic.divider import FDivider
from forza_ui.layout.stacked_widget import FStackedWidget
from forza_ui.input.tool_button import FToolButton


class FUnderlineButton(FToolButton):
    """
    FUnderlineButton
    """

    def __init__(self, parent=None):
        super(FUnderlineButton, self).__init__(parent)
        self.setCheckable(True)


class FUnderlineButtonGroup(MButtonGroupBase):
    """
    FUnderlineButtonGroup
    """

    sig_checked_changed = QtCore.Signal(int)

    def __init__(self, tab, parent=None):
        super(FUnderlineButtonGroup, self).__init__(parent=parent)
        self._line_tab = tab
        self.set_spacing(1)
        self._button_group.setExclusive(True)
        self._button_group.idClicked.connect(self.sig_checked_changed)

    def create_button(self, data_dict):
        """
        Create a button with data_dict.
        :param data_dict: dict contains text, icon, checkable, checked
        :return: button
        """
        button = FUnderlineButton(parent=self)
        if data_dict.get("svg"):
            button.svg(data_dict.get("svg"))
        if data_dict.get("text"):
            if data_dict.get("svg") or data_dict.get("icon"):
                button.text_beside_icon()
            else:
                button.text_only()
        else:
            button.icon_only()
        button.set_fui_size(self._line_tab.get_fui_size())
        return button

    def update_size(self, size):
        """
        Update all button's size
        :param size: int
        :return: None
        """
        for button in self._button_group.buttons():
            button.set_fui_size(size)

    def set_fui_checked(self, value):
        """Set current checked button's id"""
        button = self._button_group.button(value)
        button.setChecked(True)
        self.sig_checked_changed.emit(value)

    def get_fui_checked(self):
        """
        Get current checked button's id
        """
        return self._button_group.checkedId()

    fui_checked = QtCore.Property(int, get_fui_checked, set_fui_checked, notify=sig_checked_changed)


class FLineTabWidget(QtWidgets.QWidget):
    """
    FLineTabWidget
    """

    def __init__(self, alignment=QtCore.Qt.AlignCenter, parent=None):
        super(FLineTabWidget, self).__init__(parent=parent)
        self.tool_button_group = FUnderlineButtonGroup(tab=self)
        self.bar_layout = QtWidgets.QHBoxLayout()
        self.bar_layout.setContentsMargins(0, 0, 0, 0)
        if alignment == QtCore.Qt.AlignCenter:
            self.bar_layout.addStretch()
            self.bar_layout.addWidget(self.tool_button_group)
            self.bar_layout.addStretch()
        elif alignment == QtCore.Qt.AlignLeft:
            self.bar_layout.addWidget(self.tool_button_group)
            self.bar_layout.addStretch()
        elif alignment == QtCore.Qt.AlignRight:
            self.bar_layout.addStretch()
            self.bar_layout.addWidget(self.tool_button_group)
        self.stack_widget = FStackedWidget()
        self.tool_button_group.sig_checked_changed.connect(
            self.stack_widget.setCurrentIndex
        )
        main_lay = QtWidgets.QVBoxLayout()
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.setSpacing(0)
        main_lay.addLayout(self.bar_layout)
        main_lay.addWidget(FDivider())
        main_lay.addSpacing(5)
        main_lay.addWidget(self.stack_widget)
        self.setLayout(main_lay)
        self._fui_size = forza_theme.default

    def append_widget(self, widget):
        """
        Add the widget to line tab's right position.
        """
        self.bar_layout.addWidget(widget)

    def insert_widget(self, widget):
        """
        Insert the widget to line tab's left position.
        """
        self.bar_layout.insertWidget(0, widget)

    def add_tab(self, widget, data_dict):
        """
        Add a tab.

        :param widget: The widget to be added
        :param data_dict: Dictionary containing tab data like text, icon
        """
        self.stack_widget.addWidget(widget)
        self.tool_button_group.add_button(data_dict, self.stack_widget.count() - 1)

    def get_fui_size(self):
        """
        Get the line tab size.
        :return: integer
        """
        return self._fui_size

    def set_fui_size(self, value):
        """
        Set the line tab size.
        :param value: integer
        :return: None
        """
        self._fui_size = value
        self.tool_button_group.update_size(self._fui_size)
        self.style().polish(self)

    fui_size = QtCore.Property(int, get_fui_size, set_fui_size)
