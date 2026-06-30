# -*- coding: utf-8 -*-
"""Styled item views without built-in data models."""

from __future__ import annotations

from Qt import QtCore, QtGui, QtWidgets

from forza_ui import forza_theme
from forza_ui import utils
from forza_ui.display.header_view import FHeaderView
from forza_ui.icons import FPixmap, get_scale_factor


def _source_model(model):
    while isinstance(model, QtCore.QSortFilterProxyModel):
        model = model.sourceModel()
    return model


def _model_is_empty(model) -> bool:
    if model is None:
        return True
    source = _source_model(model)
    if hasattr(source, "rowCount"):
        return source.rowCount() == 0
    return False


def draw_empty_content(view, text=None, pix_map=None):
    pix_map = pix_map or FPixmap("empty.svg")
    text = text or view.tr("No Data")
    painter = QtGui.QPainter(view)
    font_metrics = painter.fontMetrics()
    painter.setPen(QtGui.QPen(QtGui.QColor(forza_theme.secondary_text_color)))
    content_height = pix_map.height() + font_metrics.height()
    padding = 10
    proper_min_size = min(
        view.height() - padding * 2,
        view.width() - padding * 2,
        content_height,
    )
    if proper_min_size < content_height:
        height = proper_min_size - font_metrics.height()
        pix_map = pix_map.scaledToHeight(height, QtCore.Qt.SmoothTransformation)
        content_height = proper_min_size
    painter.drawText(
        view.width() / 2 - utils.text_width(font_metrics, text) / 2,
        view.height() / 2 + content_height / 2 - font_metrics.height() / 2,
        text,
    )
    painter.drawPixmap(
        view.width() / 2 - pix_map.width() / 2,
        view.height() / 2 - content_height / 2,
        pix_map,
    )
    painter.end()


def enable_context_menu(self, enable):
    if enable:
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.slot_context_menu)
    else:
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)


@QtCore.Slot(QtCore.QPoint)
def slot_context_menu(self, point):
    proxy_index = self.indexAt(point)
    if proxy_index.isValid():
        need_map = isinstance(self.model(), QtCore.QSortFilterProxyModel)
        selection = []
        selected = self.selectionModel().selectedRows() or self.selectionModel().selectedIndexes()
        for index in selected:
            if need_map:
                source_index = self.model().mapToSource(index)
                data_obj = source_index.internalPointer()
            else:
                data_obj = index.internalPointer()
            selection.append(data_obj)
        event = utils.ItemViewMenuEvent(view=self, selection=selection, extra={})
        self.sig_context_menu.emit(event)
    else:
        event = utils.ItemViewMenuEvent(view=self, selection=[], extra={})
        self.sig_context_menu.emit(event)


class FTableView(QtWidgets.QTableView):
    enable_context_menu = enable_context_menu
    slot_context_menu = slot_context_menu
    sig_context_menu = QtCore.Signal(object)

    def __init__(self, size=None, show_row_count=False, parent=None):
        super().__init__(parent)
        self._no_data_image = None
        self._no_data_text = self.tr("No Data")
        size = size or forza_theme.default_size
        ver_header_view = FHeaderView(QtCore.Qt.Vertical, parent=self, show_sort_indicator=False)
        ver_header_view.setDefaultSectionSize(size)
        ver_header_view.setSortIndicatorShown(False)
        self.setVerticalHeader(ver_header_view)
        self.header_view = FHeaderView(QtCore.Qt.Horizontal, parent=self)
        self.header_view.setFixedHeight(size)
        if not show_row_count:
            ver_header_view.hide()
        self.setHorizontalHeader(self.header_view)
        self.setSortingEnabled(True)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)

    def set_no_data_text(self, text):
        self._no_data_text = text

    def set_no_data_image(self, image):
        self._no_data_image = image

    def setShowGrid(self, flag):
        self.header_view.setProperty("grid", flag)
        self.verticalHeader().setProperty("grid", flag)
        self.header_view.style().polish(self.header_view)
        return super().setShowGrid(flag)

    def paintEvent(self, event):
        if _model_is_empty(self.model()):
            draw_empty_content(self.viewport(), self._no_data_text, self._no_data_image)
        return super().paintEvent(event)

    def save_state(self, name):
        settings = QtCore.QSettings(
            QtCore.QSettings.IniFormat,
            QtCore.QSettings.UserScope,
            "Forza",
            "forza_ui",
        )
        settings.setValue(f"{name}/headerState", self.header_view.saveState())

    def load_state(self, name):
        settings = QtCore.QSettings(
            QtCore.QSettings.IniFormat,
            QtCore.QSettings.UserScope,
            "Forza",
            "forza_ui",
        )
        if settings.value(f"{name}/headerState"):
            self.header_view.restoreState(settings.value(f"{name}/headerState"))


class FTreeView(QtWidgets.QTreeView):
    enable_context_menu = enable_context_menu
    slot_context_menu = slot_context_menu
    sig_context_menu = QtCore.Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._no_data_image = None
        self._no_data_text = self.tr("No Data")
        self.header_view = FHeaderView(QtCore.Qt.Horizontal)
        self.setHeader(self.header_view)
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)

    def paintEvent(self, event):
        if _model_is_empty(self.model()):
            draw_empty_content(self.viewport(), self._no_data_text, self._no_data_image)
        return super().paintEvent(event)

    def set_no_data_text(self, text):
        self._no_data_text = text


class FBigView(QtWidgets.QListView):
    enable_context_menu = enable_context_menu
    slot_context_menu = slot_context_menu
    sig_context_menu = QtCore.Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._no_data_image = None
        self._no_data_text = self.tr("No Data")
        self.header_view = None
        self.setViewMode(QtWidgets.QListView.IconMode)
        self.setResizeMode(QtWidgets.QListView.Adjust)
        self.setMovement(QtWidgets.QListView.Static)
        self.setSpacing(10)
        default_size = forza_theme.big_view_default_size
        self.setIconSize(QtCore.QSize(default_size, default_size))

    def scale_size(self, factor):
        new_size = self.iconSize() * factor
        max_size = forza_theme.big_view_max_size
        min_size = forza_theme.big_view_min_size
        if new_size.width() > max_size:
            new_size = QtCore.QSize(max_size, max_size)
        elif new_size.width() < min_size:
            new_size = QtCore.QSize(min_size, min_size)
        self.setIconSize(new_size)

    def wheelEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier:
            num_degrees = event.delta() / 8.0
            num_steps = num_degrees / 15.0
            factor = pow(1.125, num_steps)
            self.scale_size(factor)
        else:
            super().wheelEvent(event)

    def paintEvent(self, event):
        if _model_is_empty(self.model()):
            draw_empty_content(self.viewport(), self._no_data_text, self._no_data_image)
        return super().paintEvent(event)

    def set_no_data_text(self, text):
        self._no_data_text = text


class FListView(QtWidgets.QListView):
    enable_context_menu = enable_context_menu
    slot_context_menu = slot_context_menu
    sig_context_menu = QtCore.Signal(object)

    def __init__(self, size=None, parent=None):
        super().__init__(parent)
        self._no_data_image = None
        self._no_data_text = self.tr("No Data")
        self.setProperty("fui_size", size or forza_theme.default_size)
        self.header_view = None
        self.setModelColumn(0)
        self.setAlternatingRowColors(True)

    def set_model_column(self, column: int) -> None:
        self.setModelColumn(column)

    def paintEvent(self, event):
        if _model_is_empty(self.model()):
            draw_empty_content(self.viewport(), self._no_data_text, self._no_data_image)
        return super().paintEvent(event)

    def set_no_data_text(self, text):
        self._no_data_text = text
