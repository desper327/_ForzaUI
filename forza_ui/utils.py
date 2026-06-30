# -*- coding: utf-8 -*-
"""Color helpers and static file resolution for forza_ui."""

from __future__ import annotations

import collections
import os
import contextlib
import signal
import sys

from Qt import QtCore, QtGui, QtWidgets

from forza_ui import CUSTOM_STATIC_FOLDERS, DEFAULT_STATIC_FOLDER
from forza_ui.icons import FIcon, get_scale_factor

ItemViewMenuEvent = collections.namedtuple("ItemViewMenuEvent", ["view", "selection", "extra"])


def text_width(font_metrics, text: str) -> int:
    """Qt5 width() vs Qt6 horizontalAdvance() compatibility."""
    if hasattr(font_metrics, "horizontalAdvance"):
        return font_metrics.horizontalAdvance(text)
    return font_metrics.width(text)


def overflow_format(count, overflow=99) -> str:
    """Format badge count, e.g. 100 -> '99+' when overflow is 99."""
    if count is None:
        return ""
    if count > overflow:
        return f"{overflow}+"
    return str(count)

def get_static_file(path):
    if not isinstance(path, str):
        raise TypeError("Input argument 'path' should be str type, but get {}".format(type(path)))
    full_path = next(
        (
            os.path.join(prefix, path)
            for prefix in ["", DEFAULT_STATIC_FOLDER] + CUSTOM_STATIC_FOLDERS
            if os.path.isfile(os.path.join(prefix, path))
        ),
        path,
    )
    if os.path.isfile(full_path):
        return full_path
    return None


def fade_color(color, alpha):
    q_color = QtGui.QColor(color)
    return "rgba({}, {}, {}, {})".format(q_color.red(), q_color.green(), q_color.blue(), alpha)


def generate_color(primary_color, index):
    hue_step = 2
    saturation_step = 16
    saturation_step2 = 5
    brightness_step1 = 5
    brightness_step2 = 15
    light_color_count = 5
    dark_color_count = 4

    def _get_hue(color, i, is_light):
        h_comp = color.hue()
        if 60 <= h_comp <= 240:
            hue = h_comp - hue_step * i if is_light else h_comp + hue_step * i
        else:
            hue = h_comp + hue_step * i if is_light else h_comp - hue_step * i
        if hue < 0:
            hue += 359
        elif hue >= 359:
            hue -= 359
        return hue / 359.0

    def _get_saturation(color, i, is_light):
        s_comp = color.saturationF() * 100
        if is_light:
            saturation = s_comp - saturation_step * i
        elif i == dark_color_count:
            saturation = s_comp + saturation_step
        else:
            saturation = s_comp + saturation_step2 * i
        saturation = min(100.0, saturation)
        if is_light and i == light_color_count and saturation > 10:
            saturation = 10
        saturation = max(6.0, saturation)
        return round(saturation * 10) / 1000.0

    def _get_value(color, i, is_light):
        v_comp = color.valueF()
        if is_light:
            return min((v_comp * 100 + brightness_step1 * i) / 100, 1.0)
        return max((v_comp * 100 - brightness_step2 * i) / 100, 0.0)

    light = index <= 6
    hsv_color = QtGui.QColor(primary_color) if isinstance(primary_color, str) else primary_color
    index = light_color_count + 1 - index if light else index - light_color_count - 1
    return QtGui.QColor.fromHsvF(
        _get_hue(hsv_color, index, light),
        _get_saturation(hsv_color, index, light),
        _get_value(hsv_color, index, light),
    ).name()


def get_fit_geometry():
    geo = next(
        (screen.availableGeometry() for screen in QtWidgets.QApplication.screens()),
        None,
    )
    return QtCore.QRect(geo.width() / 4, geo.height() / 4, geo.width() / 2, geo.height() / 2)


def convert_to_round_pixmap(orig_pix):
    scale_x, _ = get_scale_factor()
    w = min(orig_pix.width(), orig_pix.height())
    pix_map = QtGui.QPixmap(w, w)
    pix_map.fill(QtCore.Qt.transparent)

    painter = QtGui.QPainter(pix_map)
    painter.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)

    path = QtGui.QPainterPath()
    path.addEllipse(0, 0, w, w)
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, w, w, orig_pix)
    return pix_map


def generate_text_pixmap(width, height, text, alignment=QtCore.Qt.AlignCenter, bg_color=None):
    from forza_ui import forza_theme

    bg_color = bg_color or forza_theme.background_in_color
    pix_map = QtGui.QPixmap(width, height)
    pix_map.fill(QtGui.QColor(bg_color))
    painter = QtGui.QPainter(pix_map)
    painter.setRenderHints(QtGui.QPainter.TextAntialiasing)
    font = painter.font()
    font.setFamily(forza_theme.font_family)
    painter.setFont(font)
    painter.setPen(QtGui.QPen(QtGui.QColor(forza_theme.secondary_text_color)))

    font_metrics = painter.fontMetrics()
    text_width = font_metrics.horizontalAdvance(text)
    text_height = font_metrics.height()
    x = width / 2 - text_width / 2
    y = height / 2 - text_height / 2
    if alignment & QtCore.Qt.AlignLeft:
        x = 0
    elif alignment & QtCore.Qt.AlignRight:
        x = width - text_width
    elif alignment & QtCore.Qt.AlignTop:
        y = 0
    elif alignment & QtCore.Qt.AlignBottom:
        y = height - text_height

    painter.drawText(x, y, text)
    painter.end()
    return pix_map


def get_color_icon(color, size=24):
    scale_x, _ = get_scale_factor()
    pix = QtGui.QPixmap(size * scale_x, size * scale_x)
    q_color = color
    if isinstance(color, str):
        if color.startswith("#"):
            q_color = QtGui.QColor(color)
        elif color.count(",") == 2:
            q_color = QtGui.QColor(*tuple(map(int, color.split(","))))
    pix.fill(q_color)
    return QtGui.QIcon(pix)


def display_formatter(value):
    """Format combo/menu values for display in read-only line edits."""
    if value is None:
        return "--"
    if isinstance(value, dict):
        if "name" in value:
            return display_formatter(value["name"])
        if "code" in value:
            return display_formatter(value["code"])
        return str(value)
    if isinstance(value, list):
        return ",".join(display_formatter(item) for item in value)
    if isinstance(value, float):
        return "{:.2f}".format(round(value, 2))
    return str(value)


def get_percent(value, minimum, maximum):
    """
    Get a given value's percent in the range.
    :param value: value
    :param minimum: the range's minimum value
    :param maximum: the range's maximum value
    :return: percent float
    """
    if minimum == maximum:
        # reference from qprogressbar.cpp
        # If max and min are equal and we get this far, it means that the
        # progress bar has one step and that we are on that step. Return
        # 100% here in order to avoid division by zero further down.
        return 100
    return max(0, min(100, (value - minimum) * 100 / (maximum - minimum)))


@contextlib.contextmanager
def application(*args):
    app = QtWidgets.QApplication.instance()

    if not app:
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        app = QtWidgets.QApplication(sys.argv)
        yield app
        app.exec_()
    else:
        yield app