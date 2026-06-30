# Import built-in modules

# Import built-in modules
import functools

# Import third-party modules
from Qt import QtCore, QtGui, QtWidgets

# Import local modules
from forza_ui import forza_theme
from forza_ui.input.check_box import FCheckBox
from forza_ui.navigation.menu import FMenu
from forza_ui.input.push_button import FPushButton
from forza_ui.icons import get_scale_factor
from forza_ui.input.radio_button import FRadioButton
from forza_ui.input.tool_button import FToolButton


class MButtonGroupBase(QtWidgets.QWidget):
    def __init__(self, orientation=QtCore.Qt.Horizontal, parent=None):
        super(MButtonGroupBase, self).__init__(parent=parent)

        self._main_layout = QtWidgets.QBoxLayout(
            QtWidgets.QBoxLayout.LeftToRight
            if orientation == QtCore.Qt.Horizontal
            else QtWidgets.QBoxLayout.TopToBottom
        )

        self._main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self._main_layout)

        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

        self._button_group = QtWidgets.QButtonGroup()

        self._orientation = "horizontal" if orientation == QtCore.Qt.Horizontal else "vertical"

    def set_spacing(self, value):
        self._main_layout.setSpacing(value)

    def get_button_group(self):
        return self._button_group

    def create_button(self, data_dict):
        raise NotImplementedError()

    def add_button(self, data_dict, index=None):
        if isinstance(data_dict, str):
            data_dict = {"text": data_dict}

        elif isinstance(data_dict, QtGui.QIcon):
            data_dict = {"icon": data_dict}

        button = self.create_button(data_dict)

        button.setProperty("combine", self._orientation)

        if data_dict.get("text"):
            button.setProperty("text", data_dict.get("text"))

        if data_dict.get("icon"):
            button.setProperty("icon", data_dict.get("icon"))

        if data_dict.get("data"):
            button.setProperty("data", data_dict.get("data"))

        if data_dict.get("checked"):
            button.setProperty("checked", data_dict.get("checked"))

        if data_dict.get("shortcut"):
            button.setProperty("shortcut", data_dict.get("shortcut"))

        if data_dict.get("tooltip"):
            button.setProperty("toolTip", data_dict.get("tooltip"))

        if data_dict.get("checkable"):
            button.setProperty("checkable", data_dict.get("checkable"))

        if data_dict.get("clicked"):
            button.clicked.connect(data_dict.get("clicked"))

        if data_dict.get("toggled"):
            button.toggled.connect(data_dict.get("toggled"))

        if index is None:
            self._button_group.addButton(button)

        else:
            self._button_group.addButton(button, index)

        self._main_layout.insertWidget(self._main_layout.count(), button)

        return button

    def set_button_list(self, button_list):
        for button in self._button_group.buttons():
            self._button_group.removeButton(button)

            self._main_layout.removeWidget(button)

            button.setVisible(False)

        for index, data_dict in enumerate(button_list):
            button = self.add_button(data_dict, index)

            if index == 0:
                button.setProperty("position", "left")

            elif index == len(button_list) - 1:
                button.setProperty("position", "right")

            else:
                button.setProperty("position", "center")


class FPushButtonGroup(MButtonGroupBase):
    def __init__(self, orientation=QtCore.Qt.Horizontal, parent=None):
        super(FPushButtonGroup, self).__init__(orientation=orientation, parent=parent)

        self.set_spacing(1)

        self._fui_type = FPushButton.PrimaryType

        self._fui_size = forza_theme.default_size

        self._button_group.setExclusive(False)

    def create_button(self, data_dict):
        button = FPushButton()
        button.set_fui_size(data_dict.get("fui_size", self._fui_size))
        button.set_fui_type(data_dict.get("fui_type", self._fui_type))

        return button

    def get_fui_size(self):
        return self._fui_size

    def get_fui_type(self):
        return self._fui_type

    def set_fui_size(self, value):
        self._fui_size = value

    def set_fui_type(self, value):
        self._fui_type = value

    fui_size = QtCore.Property(int, get_fui_size, set_fui_size)
    fui_type = QtCore.Property(str, get_fui_type, set_fui_type)


class FCheckBoxGroup(MButtonGroupBase):
    sig_checked_changed = QtCore.Signal(list)

    def __init__(self, orientation=QtCore.Qt.Horizontal, parent=None):
        super(FCheckBoxGroup, self).__init__(orientation=orientation, parent=parent)
        scale_x, _ = get_scale_factor()
        self.set_spacing(15 * scale_x)
        self._button_group.setExclusive(False)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._slot_context_menu)
        self._button_group.idClicked.connect(self._slot_map_signal)
        self._fui_checked = []

    def create_button(self, data_dict):
        return FCheckBox()

    @QtCore.Slot(QtCore.QPoint)
    def _slot_context_menu(self, point):
        context_menu = FMenu(parent=self)
        action_select_all = context_menu.addAction("Select All")
        action_select_none = context_menu.addAction("Select None")
        action_select_invert = context_menu.addAction("Select Invert")
        action_select_all.triggered.connect(functools.partial(self._slot_set_select, True))
        action_select_none.triggered.connect(functools.partial(self._slot_set_select, False))
        action_select_invert.triggered.connect(functools.partial(self._slot_set_select, None))
        context_menu.exec_(QtGui.QCursor.pos() + QtCore.QPoint(10, 10))

    @QtCore.Slot(bool)
    def _slot_set_select(self, state):
        for check_box in self._button_group.buttons():
            if state is None:
                old_state = check_box.isChecked()
                check_box.setChecked(not old_state)
            else:
                check_box.setChecked(state)
        self._slot_map_signal()

    @QtCore.Slot(int)
    def _slot_map_signal(self, state=None):
        checked_buttons = [
            check_box.text()
            for check_box in self._button_group.buttons()
            if check_box.isChecked()
        ]
        self.sig_checked_changed.emit(checked_buttons)

    def set_fui_checked(self, value):
        if not isinstance(value, list):
            value = [value]

        if value == self.get_fui_checked():
            return

        self._fui_checked = value
        for check_box in self._button_group.buttons():
            flag = QtCore.Qt.Checked if check_box.text() in value else QtCore.Qt.Unchecked

            if flag != check_box.checkState():
                check_box.setCheckState(flag)

        self.sig_checked_changed.emit(value)

    def get_fui_checked(self):
        checked_buttons = [
            check_box.text()
            for check_box in self._button_group.buttons()
            if check_box.isChecked()
        ]
        return checked_buttons

    fui_checked = QtCore.Property(
        "QVariantList",
        get_fui_checked,
        set_fui_checked,
        notify=sig_checked_changed
    )


class FRadioButtonGroup(MButtonGroupBase):
    """
    Property:
        fui_checked
    """

    sig_checked_changed = QtCore.Signal(int)

    def __init__(self, orientation=QtCore.Qt.Horizontal, parent=None):
        super(FRadioButtonGroup, self).__init__(orientation=orientation, parent=parent)
        scale_x, _ = get_scale_factor()
        self.set_spacing(15 * scale_x)
        self._button_group.setExclusive(True)
        self._button_group.idClicked.connect(self.sig_checked_changed)

    def create_button(self, data_dict):
        return FRadioButton()

    def set_fui_checked(self, value):
        if value == self.get_fui_checked():
            return

        button = self._button_group.button(value)
        if button:
            button.setChecked(True)
            self.sig_checked_changed.emit(value)
        else:
            print("error")

    def get_fui_checked(self):
        return self._button_group.checkedId()

    fui_checked = QtCore.Property(
        int,
        get_fui_checked,
        set_fui_checked,
        notify=sig_checked_changed
    )


class FToolButtonGroup(MButtonGroupBase):
    sig_checked_changed = QtCore.Signal(int)

    def __init__(
        self,
        size=None,
        type=None,
        exclusive=False,
        orientation=QtCore.Qt.Horizontal,
        parent=None,
    ):
        super(FToolButtonGroup, self).__init__(orientation=orientation, parent=parent)
        self.set_spacing(1)
        self._button_group.setExclusive(exclusive)
        self._size = size
        self._type = type
        self._button_group.idClicked.connect(self.sig_checked_changed)

    def create_button(self, data_dict):
        button = FToolButton()
        if data_dict.get("svg"):
            button.svg(data_dict.get("svg"))
        if data_dict.get("text"):
            if data_dict.get("svg") or data_dict.get("icon"):
                button.text_beside_icon()
            else:
                button.text_only()
        else:
            button.icon_only()
        return button

    def set_fui_checked(self, value):
        if value == self.get_fui_checked():
            return
        button = self._button_group.button(value)
        if button:
            button.setChecked(True)
            self.sig_checked_changed.emit(value)
        else:
            print("error")

    def get_fui_checked(self):
        return self._button_group.checkedId()

    fui_checked = QtCore.Property(
        int,
        get_fui_checked,
        set_fui_checked,
        notify=sig_checked_changed
    )
