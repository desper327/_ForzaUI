# Import third-party modules
from Qt import QtCore, QtGui, QtWidgets

# Import local modules
from forza_ui import forza_theme
from forza_ui.input.completer import FCompleter
from forza_ui.mixin import cursor_mixin
from forza_ui.mixin import focus_shadow_mixin
from forza_ui.mixin import property_mixin
import forza_ui.utils as utils


@property_mixin
class FComboBoxSearchMixin(object):
    def __init__(self, *args, **kwargs):
        super(FComboBoxSearchMixin, self).__init__(*args, **kwargs)
        self.filter_model = QtCore.QSortFilterProxyModel(self)
        self.filter_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.filter_model.setSourceModel(self.model())
        self.completer = FCompleter(self)
        self.completer.setCompletionMode(QtWidgets.QCompleter.UnfilteredPopupCompletion)
        self.completer.setModel(self.filter_model)

    def search(self):
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setEditable(True)

        self.setCompleter(self.completer)

        edit = self.lineEdit()
        edit.setReadOnly(False)
        edit.returnPressed.disconnect()
        edit.textEdited.connect(self.filter_model.setFilterFixedString)
        self.completer.activated.connect(lambda t: t and self.setCurrentIndex(self.findText(t)))

    def _set_searchable(self, value):
        """search property to True then trigger search"""
        value and self.search()

    def setModel(self, model):
        super(FComboBoxSearchMixin, self).setModel(model)
        self.filter_model.setSourceModel(model)
        self.completer.setModel(self.filter_model)

    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.filter_model.setFilterKeyColumn(column)
        super(FComboBoxSearchMixin, self).setModelColumn(column)


@cursor_mixin
@focus_shadow_mixin
class FComboBox(FComboBoxSearchMixin, QtWidgets.QComboBox):
    Separator = "/"
    sig_value_changed = QtCore.Signal(object)
    _paint_proxies: dict[int, "FComboBox"] = {}

    def __init__(self, parent=None):
        self._fui_size = forza_theme.default_size
        super(FComboBox, self).__init__(parent)

        self._root_menu = None
        self._display_formatter = utils.display_formatter
        self.setEditable(True)
        line_edit = self.lineEdit()
        line_edit.setReadOnly(True)
        line_edit.setTextMargins(4, 0, 4, 0)
        line_edit.setStyleSheet("background-color:transparent")
        line_edit.setCursor(QtCore.Qt.PointingHandCursor)
        line_edit.installEventFilter(self)
        self._has_custom_view = False
        self.set_value("")
        self.set_placeholder(self.tr("Please Select"))
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        forza_theme.apply(self)

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
        self.lineEdit().setProperty("fui_size", value)
        self.style().polish(self)

    fui_size = QtCore.Property(int, get_fui_size, set_fui_size)

    def set_formatter(self, func):
        self._display_formatter = func

    def set_placeholder(self, text):
        """Display the text when no item selected."""
        self.lineEdit().setPlaceholderText(text)

    def set_value(self, value):
        self.setProperty("value", value)

    def _set_value(self, value):
        self.lineEdit().setProperty("text", self._display_formatter(value))
        if self._root_menu:
            self._root_menu.set_value(value)

    def set_menu(self, menu):
        self._root_menu = menu
        self._root_menu.sig_value_changed.connect(self.sig_value_changed)
        self._root_menu.sig_value_changed.connect(self.set_value)

    def setView(self, *args, **kwargs):
        """Override setView to flag _has_custom_view variable."""
        self._has_custom_view = True
        super(FComboBox, self).setView(*args, **kwargs)

    def showPopup(self):
        """Override default showPopup. When set custom menu, show the menu instead."""
        if self._has_custom_view or self._root_menu is None:
            super(FComboBox, self).showPopup()
        else:
            super(FComboBox, self).hidePopup()
            self._root_menu.popup(self.mapToGlobal(QtCore.QPoint(0, self.height())))

    # def setCurrentIndex(self, index):
    #     raise NotImplementedError

    def eventFilter(self, widget, event):
        if widget is self.lineEdit() and widget.isReadOnly() and self.isEnabled():
            if event.type() == QtCore.QEvent.MouseButtonPress:
                self.showPopup()
        return super(FComboBox, self).eventFilter(widget, event)

    def huge(self):
        """Set FComboBox to huge size"""
        self.set_fui_size(forza_theme.huge)
        return self

    def large(self):
        """Set FComboBox to large size"""
        self.set_fui_size(forza_theme.large)
        return self

    def medium(self):
        """Set FComboBox to  medium"""
        self.set_fui_size(forza_theme.medium)
        return self

    def small(self):
        """Set FComboBox to small size"""
        self.set_fui_size(forza_theme.small)
        return self

    def tiny(self):
        """Set FComboBox to tiny size"""
        self.set_fui_size(forza_theme.tiny)
        return self

    # 以下的代码用于 Delegate 非编辑态绘制，实现见 paint_utils.paint_combo_appearance

    @classmethod
    def clear_paint_proxies(cls) -> None:
        """Drop cached paint proxies after theme changes."""
        cls._paint_proxies.clear()

    @classmethod
    def paint_appearance(
        cls,
        painter: QtGui.QPainter,
        rect: QtCore.QRect,
        text: str,
        *,
        fui_size: int | None = None,
        enabled: bool = True,
    ) -> None:
        """Draw a non-interactive FComboBox look using Qt Style + QSS."""
        from forza_ui.input.paint_utils import paint_combo_appearance

        paint_combo_appearance(
            cls._paint_proxies,
            painter,
            rect,
            text,
            fui_size=fui_size,
            enabled=enabled,
        )
