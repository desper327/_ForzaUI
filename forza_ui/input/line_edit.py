"""FLineEdit
Get the user input is a text field
"""

# Import built-in modules
import functools

# Import third-party modules
from Qt import QtCore, QtWidgets

# Import local modules
from forza_ui import forza_theme
from forza_ui.mixin import focus_shadow_mixin
from forza_ui.input.push_button import FPushButton
from forza_ui.input.tool_button import FToolButton


@focus_shadow_mixin
class FLineEdit(QtWidgets.QLineEdit):
    """FLineEdit"""

    sig_delay_text_changed = QtCore.Signal(str)

    def __init__(self, text="", parent=None):
        self._fui_size = forza_theme.default_size
        super(FLineEdit, self).__init__(text, parent)
        self._main_layout = QtWidgets.QHBoxLayout()
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.addStretch()

        self._prefix_widget = None
        self._suffix_widget = None

        self.setLayout(self._main_layout)
        self.setProperty("history", self.property("text"))
        self.setTextMargins(2, 0, 2, 0)

        self._delay_timer = QtCore.QTimer()
        self._delay_timer.setInterval(500)
        self._delay_timer.setSingleShot(True)
        self._delay_timer.timeout.connect(self._slot_delay_text_changed)
        self.textChanged.connect(self._slot_begin_to_start_delay)

    def get_fui_size(self):
        """
        Get the push button height
        :return: integer
        """
        return getattr(self, "_fui_size", forza_theme.default_size)

    def set_fui_size(self, value):
        """
        Set the avatar size.
        :param value: integer
        :return: None
        """
        self._fui_size = value
        if hasattr(self._prefix_widget, "set_fui_size"):
            self._prefix_widget.set_fui_size(self._fui_size)
        if hasattr(self._suffix_widget, "set_fui_size"):
            self._suffix_widget.set_fui_size(self._fui_size)
        self.style().polish(self)

    fui_size = QtCore.Property(int, get_fui_size, set_fui_size)

    def set_delay_duration(self, millisecond):
        """Set delay timer's timeout duration."""
        self._delay_timer.setInterval(millisecond)

    @QtCore.Slot()
    def _slot_delay_text_changed(self):
        self.sig_delay_text_changed.emit(self.text())

    @QtCore.Slot(str)
    def _slot_begin_to_start_delay(self, _):
        if self._delay_timer.isActive():
            self._delay_timer.stop()
        self._delay_timer.start()

    def get_prefix_widget(self):
        """Get the prefix widget for user to edit"""
        return self._prefix_widget

    def set_prefix_widget(self, widget):
        """Set the line edit left start widget"""
        if self._prefix_widget:
            index = self._main_layout.indexOf(self._prefix_widget)
            self._main_layout.takeAt(index)
            self._prefix_widget.setVisible(False)
        # if isinstance(widget, FPushButton):
        widget.setProperty("combine", "horizontal")
        widget.setProperty("position", "left")
        if hasattr(widget, "set_fui_size"):
            widget.set_fui_size(self._fui_size)

        margin = self.textMargins()
        margin.setLeft(margin.left() + widget.width())
        self.setTextMargins(margin)

        self._main_layout.insertWidget(0, widget)
        self._prefix_widget = widget
        return widget

    def get_suffix_widget(self):
        """Get the suffix widget for user to edit"""
        return self._suffix_widget

    def set_suffix_widget(self, widget):
        """Set the line edit right end widget"""
        if self._suffix_widget:
            index = self._main_layout.indexOf(self._suffix_widget)
            self._main_layout.takeAt(index)
            self._suffix_widget.setVisible(False)
        # if isinstance(widget, FPushButton):
        widget.setProperty("combine", "horizontal")
        widget.setProperty("position", "right")
        if hasattr(widget, "set_fui_size"):
            widget.set_fui_size(self._fui_size)

        margin = self.textMargins()
        margin.setRight(margin.right() + widget.width())
        self.setTextMargins(margin)
        self._main_layout.addWidget(widget)
        self._suffix_widget = widget
        return widget

    def setText(self, text):
        """Override setText save text to history"""
        self.setProperty("history", "{}\n{}".format(self.property("history"), text))
        return super(FLineEdit, self).setText(text)

    def clear(self):
        """Override clear to clear history"""
        self.setProperty("history", "")
        return super(FLineEdit, self).clear()

    def search(self):
        """Add a search icon button for FLineEdit."""
        suffix_button = FToolButton().icon_only().svg("close_line.svg")
        suffix_button.clicked.connect(self.clear)
        self.set_suffix_widget(suffix_button)
        self.setPlaceholderText(self.tr("Enter key word to search..."))
        return self

    def error(self):
        """A a toolset to FLineEdit to store error info with red style"""

        @QtCore.Slot()
        def _slot_show_detail(self):
            dialog = QtWidgets.QTextEdit(self)
            dialog.setReadOnly(True)
            geo = QtWidgets.QApplication.primaryScreen().geometry()
            dialog.setGeometry(geo.width() / 2, geo.height() / 2, geo.width() / 4, geo.height() / 4)
            dialog.setWindowTitle(self.tr("Error Detail Information"))
            dialog.setText(self.property("history"))
            dialog.setWindowFlags(QtCore.Qt.Dialog)
            dialog.show()

        self.setProperty("fui_type", "error")
        self.setReadOnly(True)
        _suffix_button = FToolButton().icon_only().svg("detail_line.svg")
        _suffix_button.clicked.connect(functools.partial(_slot_show_detail, self))
        self.set_suffix_widget(_suffix_button)
        self.setPlaceholderText(self.tr("Error information will be here..."))
        return self

    def search_engine(self, text="Search"):
        """Add a FPushButton to suffix for FLineEdit"""
        _suffix_button = FPushButton(text=text).primary()
        _suffix_button.clicked.connect(self.returnPressed)
        _suffix_button.setFixedWidth(100)
        self.set_suffix_widget(_suffix_button)
        self.setPlaceholderText(self.tr("Enter key word to search..."))
        return self

    def file(self, filters=None):
        """Add a tool button that opens a file dialog."""
        suffix_button = FToolButton().icon_only().svg("folder_fill.svg")

        @QtCore.Slot()
        def _pick_file():
            path, _ = QtWidgets.QFileDialog.getOpenFileName(self, self.tr("Select File"), self.text(), filters or "")
            if path:
                self.setText(path)

        suffix_button.clicked.connect(_pick_file)
        self.set_suffix_widget(suffix_button)
        self.setPlaceholderText(self.tr("Click button to browse files"))
        return self

    def save_file(self, filters=None):
        """Add a tool button that opens a save file dialog."""
        suffix_button = FToolButton().icon_only().svg("save_line.svg")

        @QtCore.Slot()
        def _pick_save_file():
            path, _ = QtWidgets.QFileDialog.getSaveFileName(self, self.tr("Save File"), self.text(), filters or "")
            if path:
                self.setText(path)

        suffix_button.clicked.connect(_pick_save_file)
        self.set_suffix_widget(suffix_button)
        self.setPlaceholderText(self.tr("Click button to set save file"))
        return self

    def folder(self):
        """Add a tool button that opens a folder dialog."""
        suffix_button = FToolButton().icon_only().svg("folder_fill.svg")

        @QtCore.Slot()
        def _pick_folder():
            path = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr("Select Folder"), self.text())
            if path:
                self.setText(path)

        suffix_button.clicked.connect(_pick_folder)
        self.set_suffix_widget(suffix_button)
        self.setPlaceholderText(self.tr("Click button to browse folder"))
        return self

    def huge(self):
        """Set FLineEdit to huge size"""
        self.set_fui_size(forza_theme.huge)
        return self

    def large(self):
        """Set FLineEdit to large size"""
        self.set_fui_size(forza_theme.large)
        return self

    def medium(self):
        """Set FLineEdit to  medium"""
        self.set_fui_size(forza_theme.medium)
        return self

    def small(self):
        """Set FLineEdit to small size"""
        self.set_fui_size(forza_theme.small)
        return self

    def tiny(self):
        """Set FLineEdit to tiny size"""
        self.set_fui_size(forza_theme.tiny)
        return self

    def password(self):
        """Set FLineEdit to password echo mode"""
        self.setEchoMode(QtWidgets.QLineEdit.Password)
        return self

    _paint_proxies: dict[int, "FLineEdit"] = {}

    @classmethod
    def clear_paint_proxies(cls) -> None:
        cls._paint_proxies.clear()

    @classmethod
    def paint_appearance(
        cls,
        painter,
        rect,
        text: str,
        *,
        fui_size: int | None = None,
        enabled: bool = True,
    ) -> None:
        from forza_ui.input.paint_utils import paint_line_edit_appearance

        paint_line_edit_appearance(
            cls._paint_proxies,
            painter,
            rect,
            text,
            fui_size=fui_size,
            enabled=enabled,
        )
