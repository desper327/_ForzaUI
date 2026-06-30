# Import third-party modules
from Qt import QtCore, QtWidgets


class FProgressBar(QtWidgets.QProgressBar):
    """
    props:
        status: str

    """

    ErrorStatus = "error"
    NormalStatus = "primary"
    SuccessStatus = "success"

    _paint_proxies: dict[tuple, "FProgressBar"] = {}

    def __init__(self, parent=None):
        super(FProgressBar, self).__init__(parent=parent)
        self.setOrientation(QtCore.Qt.Horizontal)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setTextVisible(True)
        self._status = FProgressBar.NormalStatus

    @classmethod
    def clear_paint_proxies(cls) -> None:
        cls._paint_proxies.clear()

    @classmethod
    def paint_appearance(
        cls,
        painter,
        rect: QtCore.QRect,
        *,
        value: int = 0,
        minimum: int = 0,
        maximum: int = 100,
        fui_status: str | None = None,
        enabled: bool = True,
    ) -> None:
        from forza_ui.input.paint_utils import paint_progress_bar_appearance

        paint_progress_bar_appearance(
            cls._paint_proxies,
            painter,
            rect,
            value=value,
            minimum=minimum,
            maximum=maximum,
            fui_status=fui_status or cls.NormalStatus,
            enabled=enabled,
        )

    def auto_color(self):
        self.valueChanged.connect(self._update_color)
        return self

    @QtCore.Slot(int)
    def _update_color(self, value):
        if value >= self.maximum():
            self.set_fui_status(FProgressBar.SuccessStatus)
        else:
            self.set_fui_status(FProgressBar.NormalStatus)

    def get_fui_status(self):
        return self._status

    def set_fui_status(self, value):
        self._status = value
        self.style().polish(self)

    fui_status = QtCore.Property(str, get_fui_status, set_fui_status)

    def normal(self):
        self.set_fui_status(FProgressBar.NormalStatus)
        return self

    def error(self):
        self.set_fui_status(FProgressBar.ErrorStatus)
        return self

    def success(self):
        self.set_fui_status(FProgressBar.SuccessStatus)
        return self
