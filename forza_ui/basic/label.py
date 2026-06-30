# Import third-party modules
from Qt import QtCore, QtWidgets

# Import local modules
from forza_ui import forza_theme


class FLabel(QtWidgets.QLabel):
    """
    Display title in different level.
    Property:
        fui_level: integer
        fui_type: str
    """

    SecondaryType = "secondary"
    WarningType = "warning"
    DangerType = "danger"
    H1Level = 1
    H2Level = 2
    H3Level = 3
    H4Level = 4

    def __init__(self, text="", parent=None, flags=QtCore.Qt.Widget):
        super(FLabel, self).__init__(text, parent, flags)
        flags = QtCore.Qt.TextBrowserInteraction | QtCore.Qt.LinksAccessibleByMouse
        self.setTextInteractionFlags(flags)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self._fui_type = ""
        self._fui_underline = False
        self._fui_mark = False
        self._fui_delete = False
        self._fui_strong = False
        self._fui_code = False
        self._fui_level = 0
        self._elide_mode = QtCore.Qt.ElideNone
        self.setProperty("fui_text", text)

    def get_fui_level(self):
        """Get FLabel level."""
        return self._fui_level

    def set_fui_level(self, value):
        """Set FLabel level"""
        self._fui_level = value
        self.style().polish(self)

    def set_fui_underline(self, value):
        """Set FLabel underline style."""
        self._fui_underline = value
        self.style().polish(self)

    def get_fui_underline(self):
        return self._fui_underline

    def set_fui_delete(self, value):
        """Set FLabel a delete line style."""
        self._fui_delete = value
        self.style().polish(self)

    def get_fui_delete(self):
        return self._fui_delete

    def set_fui_strong(self, value):
        """Set FLabel bold style."""
        self._fui_strong = value
        self.style().polish(self)

    def get_fui_strong(self):
        return self._fui_strong

    def set_fui_mark(self, value):
        """Set FLabel mark style."""
        self._fui_mark = value
        self.style().polish(self)

    def get_fui_mark(self):
        return self._fui_mark

    def set_fui_code(self, value):
        """Set FLabel code style."""
        self._fui_code = value
        self.style().polish(self)

    def get_fui_code(self):
        return self._fui_code

    def get_elide_mode(self):
        return self._elide_mode

    def set_elide_mode(self, value):
        """Set FLabel elide mode.
        Only accepted Qt.ElideLeft/Qt.ElideMiddle/Qt.ElideRight/Qt.ElideNone"""
        self._elide_mode = value
        self._update_elided_text()

    def get_fui_type(self):
        return self._fui_type

    def set_fui_type(self, value):
        self._fui_type = value
        self.style().polish(self)

    fui_level = QtCore.Property(int, get_fui_level, set_fui_level)
    fui_type = QtCore.Property(str, get_fui_type, set_fui_type)
    fui_underline = QtCore.Property(bool, get_fui_underline, set_fui_underline)
    fui_delete = QtCore.Property(bool, get_fui_delete, set_fui_delete)
    fui_strong = QtCore.Property(bool, get_fui_strong, set_fui_strong)
    fui_mark = QtCore.Property(bool, get_fui_mark, set_fui_mark)
    fui_code = QtCore.Property(bool, get_fui_code, set_fui_code)
    fui_elide_mod = QtCore.Property(QtCore.Qt.TextElideMode, get_fui_code, set_fui_code)

    def minimumSizeHint(self):
        return QtCore.QSize(1, self.fontMetrics().height())

    def text(self):
        """
        Overridden base method to return the original unmodified text

        :returns:   The original unmodified text
        """
        return self.property("text")

    def setText(self, text):
        """
        Overridden base method to set the text on the label

        :param text:    The text to set on the label
        """
        self.setProperty("text", text)
        self._update_elided_text()
        self.setToolTip(text)

    def set_link(self, href, text=None):
        """

        :param href: The href attr of a tag
        :param text: The a tag text content
        """
        # 这里富文本的超链接必须使用 html 的样式，使用 qss 不起作用
        link_style = forza_theme.hyperlink_style
        text_content = text or href
        self.setText(
            f'{link_style}<a href="{href}">{text_content}</a>'
        )
        self.setOpenExternalLinks(True)

    def _update_elided_text(self):
        """
        Update the elided text on the label
        """
        _font_metrics = self.fontMetrics()
        text = self.property("text")
        text = text if text else ""
        _elided_text = _font_metrics.elidedText(text, self._elide_mode, self.width() - 2 * 2)
        super(FLabel, self).setText(_elided_text)

    def resizeEvent(self, event):
        """
        Overridden base method called when the widget is resized.

        :param event:    The resize event
        """
        self._update_elided_text()

    def h1(self):
        """Set QLabel with h1 type."""
        self.set_fui_level(FLabel.H1Level)
        return self

    def h2(self):
        """Set QLabel with h2 type."""
        self.set_fui_level(FLabel.H2Level)
        return self

    def h3(self):
        """Set QLabel with h3 type."""
        self.set_fui_level(FLabel.H3Level)
        return self

    def h4(self):
        """Set QLabel with h4 type."""
        self.set_fui_level(FLabel.H4Level)
        return self

    def secondary(self):
        """Set QLabel with secondary type."""
        self.set_fui_type(FLabel.SecondaryType)
        return self

    def warning(self):
        """Set QLabel with warning type."""
        self.set_fui_type(FLabel.WarningType)
        return self

    def danger(self):
        """Set QLabel with danger type."""
        self.set_fui_type(FLabel.DangerType)
        return self

    def strong(self):
        """Set QLabel with strong style."""
        self.set_fui_strong(True)
        return self

    def mark(self):
        """Set QLabel with mark style."""
        self.set_fui_mark(True)
        return self

    def code(self):
        """Set QLabel with code style."""
        self.set_fui_code(True)
        return self

    def delete(self):
        """Set QLabel with delete style."""
        self.set_fui_delete(True)
        return self

    def underline(self):
        """Set QLabel with underline style."""
        self.set_fui_underline(True)
        return self

    def event(self, event):
        is_text_change = (
            event.type() == QtCore.QEvent.DynamicPropertyChange
            and event.propertyName() == "fui_text"
        )
        if is_text_change:
            self.setText(self.property("fui_text"))
        return super(FLabel, self).event(event)
