"""
FAvatar.
"""

# Import third-party modules
from Qt import QtCore, QtGui, QtWidgets

# Import local modules
from forza_ui import forza_theme
from forza_ui.icons import FPixmap


class FAvatar(QtWidgets.QLabel):
    """
    Avatar component. It can be used to represent people or object.
    Property:
        image: avatar image, should be QPixmap.
        fui_size: the size of image.
    """

    def __init__(self, parent=None, flags=QtCore.Qt.Widget):
        super(FAvatar, self).__init__(parent, flags)
        self._default_pix = FPixmap("user_fill.svg")
        self._pixmap = self._default_pix
        self._original_pixmap = self._default_pix
        self._fui_size = 0
        self.set_fui_size(forza_theme.default_size)

    def set_fui_size(self, value):
        """
        Set the avatar size.
        :param value: integer
        :return: None
        """
        self._fui_size = value
        self._set_fui_size()

    def _set_fui_size(self):
        self.setFixedSize(QtCore.QSize(self._fui_size, self._fui_size))
        self._set_fui_image()

    def _set_fui_image(self):
        # Check if pixmap is null or has zero size
        if self._pixmap.isNull() or self._pixmap.size().isEmpty():
            # Reset to default pixmap
            self._pixmap = self._default_pix.copy()
            # Also update original pixmap reference to ensure consistency
            self._original_pixmap = self._default_pix

        # Scale the pixmap to the current size
        if self.height() > 0:
            scaled_pixmap = self._pixmap.scaledToWidth(self.height(), QtCore.Qt.SmoothTransformation)
            self.setPixmap(scaled_pixmap)

    def set_fui_image(self, value):
        """
        Set avatar image.
        :param value: QPixmap or None.
        :return: None
        """

        if value is None:
            self._pixmap = self._default_pix
            self._original_pixmap = self._default_pix
        elif isinstance(value, QtGui.QPixmap):
            if value.isNull():
                self._pixmap = self._default_pix
                self._original_pixmap = self._default_pix
            else:
                self._pixmap = value
                self._original_pixmap = value
        else:
            msg = "Input argument 'value' should be QPixmap or None, but get {}"
            raise TypeError(msg.format(type(value)))
        self._set_fui_image()

    def get_fui_image(self):
        """
        Get the avatar image.
        :return: QPixmap
        """
        return self._original_pixmap

    def get_fui_size(self):
        """
        Get the avatar size
        :return: integer
        """
        return self._fui_size

    fui_image = QtCore.Property(QtGui.QPixmap, get_fui_image, set_fui_image)
    fui_size = QtCore.Property(int, get_fui_size, set_fui_size)

    @classmethod
    def huge(cls, image=None):
        """Create a FAvatar with huge size"""
        inst = cls()
        inst.set_fui_size(forza_theme.huge)
        inst.set_fui_image(image)
        return inst

    @classmethod
    def large(cls, image=None):
        """Create a FAvatar with large size"""
        inst = cls()
        inst.set_fui_size(forza_theme.large)
        inst.set_fui_image(image)
        return inst

    @classmethod
    def medium(cls, image=None):
        """Create a FAvatar with medium size"""
        inst = cls()
        inst.set_fui_size(forza_theme.medium)
        inst.set_fui_image(image)
        return inst

    @classmethod
    def small(cls, image=None):
        """Create a FAvatar with small size"""
        inst = cls()
        inst.set_fui_size(forza_theme.small)
        inst.set_fui_image(image)
        return inst

    @classmethod
    def tiny(cls, image=None):
        """Create a FAvatar with tiny size"""
        inst = cls()
        inst.set_fui_size(forza_theme.tiny)
        inst.set_fui_image(image)
        return inst
