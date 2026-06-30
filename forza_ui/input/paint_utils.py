# -*- coding: utf-8 -*-
"""Shared QStyle paint helpers for F* widget paint_appearance APIs."""

from __future__ import annotations

from collections.abc import Callable

from Qt import QtCore, QtGui, QtWidgets

from forza_ui import forza_theme


def refresh_paint_proxy(widget: QtWidgets.QWidget) -> None:
    """Re-apply QSS to a proxy; call only on create or theme change."""
    forza_theme.apply(widget)
    widget.style().unpolish(widget)
    widget.style().polish(widget)


def _sync_spin_proxy_value(proxy: QtWidgets.QWidget, display_text: str) -> None:
    """Align proxy value with cell text so step button :off/:disabled states are correct."""
    if not display_text:
        return
    try:
        if isinstance(proxy, QtWidgets.QDoubleSpinBox):
            proxy.setValue(float(display_text))
        elif isinstance(proxy, QtWidgets.QSpinBox):
            proxy.setValue(int(display_text))
        elif isinstance(proxy, QtWidgets.QDateEdit):
            date = QtCore.QDate.fromString(display_text, "yyyy-MM-dd")
            if date.isValid():
                proxy.setDate(date)
        elif isinstance(proxy, QtWidgets.QDateTimeEdit):
            dt = QtCore.QDateTime.fromString(display_text, "yyyy-MM-dd HH:mm:ss")
            if dt.isValid():
                proxy.setDateTime(dt)
        elif isinstance(proxy, QtWidgets.QTimeEdit):
            time = QtCore.QTime.fromString(display_text, "HH:mm:ss")
            if time.isValid():
                proxy.setTime(time)
    except (TypeError, ValueError):
        pass


def get_paint_proxy(
    widget_cls: type,
    cache: dict,
    cache_key,
    *,
    setup: Callable[[QtWidgets.QWidget], None] | None = None,
) -> QtWidgets.QWidget:
    """
    Return a cached paint proxy backed by a full F* widget instance.

    P0: refresh_paint_proxy runs only when the proxy is first created.
    """
    proxy = cache.get(cache_key)
    if proxy is None:
        proxy = widget_cls()
        if setup:
            setup(proxy)
        elif hasattr(proxy, "set_fui_size") and isinstance(cache_key, int):
            proxy.set_fui_size(cache_key)
        cache[cache_key] = proxy
        refresh_paint_proxy(proxy)
    return proxy


def paint_line_edit_appearance(
    cache: dict,
    painter: QtGui.QPainter,
    rect: QtCore.QRect,
    text: str,
    *,
    fui_size: int | None = None,
    enabled: bool = True,
) -> None:
    from forza_ui.input.line_edit import FLineEdit

    if not rect.isValid() or rect.width() <= 0 or rect.height() <= 0:
        return

    size = fui_size if fui_size is not None else forza_theme.medium
    proxy = get_paint_proxy(FLineEdit, cache, size)
    proxy.setEnabled(enabled)
    display_text = "" if text is None else str(text)
    proxy.setText(display_text)

    option = QtWidgets.QStyleOptionFrame()
    option.initFrom(proxy)
    option.rect = QtCore.QRect(0, 0, rect.width(), rect.height())
    option.lineWidth = proxy.style().pixelMetric(
        QtWidgets.QStyle.PM_DefaultFrameWidth, option, proxy
    )
    option.midLineWidth = 0
    option.state = QtWidgets.QStyle.State_None
    if enabled:
        option.state |= QtWidgets.QStyle.State_Enabled
    option.frameShape = QtWidgets.QFrame.Panel
    option.frameShadow = QtWidgets.QFrame.Sunken

    style = proxy.style()
    painter.save()
    painter.translate(rect.topLeft())
    style.drawPrimitive(QtWidgets.QStyle.PE_PanelLineEdit, option, painter, proxy)
    text_rect = style.subElementRect(
        QtWidgets.QStyle.SE_LineEditContents, option, proxy
    )
    if text_rect.isValid() and display_text:
        style.drawItemText(
            painter,
            text_rect,
            QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft,
            proxy.palette(),
            enabled,
            display_text,
            QtGui.QPalette.Text,
        )
    painter.restore()


def paint_spinbox_appearance(
    widget_cls: type,
    cache: dict,
    painter: QtGui.QPainter,
    rect: QtCore.QRect,
    text: str,
    *,
    fui_size: int | None = None,
    enabled: bool = True,
) -> None:
    if not rect.isValid() or rect.width() <= 0 or rect.height() <= 0:
        return

    size = fui_size if fui_size is not None else forza_theme.medium
    proxy = get_paint_proxy(widget_cls, cache, (widget_cls.__name__, size))
    proxy.setEnabled(enabled)
    display_text = "" if text is None else str(text)
    _sync_spin_proxy_value(proxy, display_text)

    option = QtWidgets.QStyleOptionSpinBox()
    option.initFrom(proxy)
    option.rect = QtCore.QRect(0, 0, rect.width(), rect.height())
    option.frame = True
    option.buttonSymbols = proxy.buttonSymbols()
    option.stepEnabled = proxy.stepEnabled()
    option.state = QtWidgets.QStyle.State_None
    if enabled:
        option.state |= QtWidgets.QStyle.State_Enabled

    style = proxy.style()
    painter.save()
    painter.translate(rect.topLeft())
    style.drawComplexControl(QtWidgets.QStyle.CC_SpinBox, option, painter, proxy)
    text_rect = style.subControlRect(
        QtWidgets.QStyle.CC_SpinBox,
        option,
        QtWidgets.QStyle.SC_SpinBoxEditField,
        proxy,
    )
    if text_rect.isValid() and display_text:
        style.drawItemText(
            painter,
            text_rect.adjusted(4, 0, -4, 0),
            QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft,
            proxy.palette(),
            enabled,
            display_text,
            QtGui.QPalette.Text,
        )
    painter.restore()


def paint_combo_appearance(
    cache: dict,
    painter: QtGui.QPainter,
    rect: QtCore.QRect,
    text: str,
    *,
    fui_size: int | None = None,
    enabled: bool = True,
) -> None:
    from forza_ui.input.combo_box import FComboBox

    if not rect.isValid() or rect.width() <= 0 or rect.height() <= 0:
        return

    size = fui_size if fui_size is not None else forza_theme.medium
    proxy = get_paint_proxy(FComboBox, cache, size)
    proxy.setEnabled(enabled)

    option = QtWidgets.QStyleOptionComboBox()
    option.initFrom(proxy)
    option.rect = QtCore.QRect(0, 0, rect.width(), rect.height())
    option.editable = proxy.isEditable()
    option.frame = True
    display_text = "" if text is None else str(text)
    option.currentText = display_text
    option.iconSize = proxy.iconSize()

    line_edit = proxy.lineEdit()
    if line_edit is not None:
        line_edit.setText(display_text)

    option.state = QtWidgets.QStyle.State_None
    if enabled:
        option.state |= QtWidgets.QStyle.State_Enabled
    else:
        option.state |= QtWidgets.QStyle.State_ReadOnly

    style = proxy.style()
    painter.save()
    painter.translate(rect.topLeft())
    style.drawComplexControl(
        QtWidgets.QStyle.CC_ComboBox, option, painter, proxy
    )
    text_rect = style.subControlRect(
        QtWidgets.QStyle.CC_ComboBox,
        option,
        QtWidgets.QStyle.SC_ComboBoxEditField,
        proxy,
    )
    if text_rect.isValid() and display_text:
        if line_edit is not None:
            margins = line_edit.textMargins()
            text_rect = text_rect.adjusted(margins.left(), 0, -margins.right(), 0)
        style.drawItemText(
            painter,
            text_rect,
            QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft,
            proxy.palette(),
            enabled,
            display_text,
            QtGui.QPalette.Text,
        )
    painter.restore()


def paint_check_indicator_appearance(
    cache: dict,
    painter: QtGui.QPainter,
    rect: QtCore.QRect,
    checked: bool,
    *,
    fui_size: int | None = None,
    enabled: bool = True,
) -> None:
    from forza_ui.input.check_box import FCheckBox

    if not rect.isValid():
        return

    size = fui_size if fui_size is not None else forza_theme.medium
    proxy = get_paint_proxy(FCheckBox, cache, size)
    proxy.setEnabled(enabled)
    proxy.setChecked(checked)

    option = QtWidgets.QStyleOptionButton()
    option.initFrom(proxy)
    indicator_size = proxy.style().pixelMetric(
        QtWidgets.QStyle.PM_IndicatorWidth, option, proxy
    )
    indicator_rect = QtCore.QRect(
        rect.center().x() - indicator_size // 2,
        rect.center().y() - indicator_size // 2,
        indicator_size,
        indicator_size,
    )
    option.rect = indicator_rect
    option.state = QtWidgets.QStyle.State_None
    if enabled:
        option.state |= QtWidgets.QStyle.State_Enabled
    if checked:
        option.state |= QtWidgets.QStyle.State_On
    else:
        option.state |= QtWidgets.QStyle.State_Off

    painter.save()
    proxy.style().drawControl(
        QtWidgets.QStyle.CE_CheckBox, option, painter, proxy
    )
    painter.restore()


def paint_switch_indicator_appearance(
    cache: dict,
    painter: QtGui.QPainter,
    rect: QtCore.QRect,
    checked: bool,
    *,
    fui_size: int | None = None,
    enabled: bool = True,
) -> None:
    from forza_ui.input.switch import FSwitch

    if not rect.isValid():
        return

    size = fui_size if fui_size is not None else forza_theme.medium
    proxy = get_paint_proxy(FSwitch, cache, size)
    proxy.setEnabled(enabled)
    proxy.setChecked(checked)

    hint = proxy.minimumSizeHint()
    indicator_rect = QtCore.QRect(
        rect.center().x() - hint.width() // 2,
        rect.center().y() - hint.height() // 2,
        hint.width(),
        hint.height(),
    )

    option = QtWidgets.QStyleOptionButton()
    option.initFrom(proxy)
    option.rect = indicator_rect
    option.state = QtWidgets.QStyle.State_None
    if enabled:
        option.state |= QtWidgets.QStyle.State_Enabled
    if checked:
        option.state |= QtWidgets.QStyle.State_On
    else:
        option.state |= QtWidgets.QStyle.State_Off

    painter.save()
    proxy.style().drawControl(
        QtWidgets.QStyle.CE_RadioButton, option, painter, proxy
    )
    painter.restore()


def paint_push_button_appearance(
    cache: dict,
    painter: QtGui.QPainter,
    rect: QtCore.QRect,
    text: str,
    *,
    fui_size: int | None = None,
    enabled: bool = True,
    fui_type: str = "default",
) -> None:
    from forza_ui.input.push_button import FPushButton

    if not rect.isValid() or rect.width() <= 0 or rect.height() <= 0:
        return

    size = fui_size if fui_size is not None else forza_theme.medium
    cache_key = (size, fui_type)

    def _setup(proxy: QtWidgets.QWidget) -> None:
        proxy.set_fui_size(size)
        proxy.set_fui_type(fui_type)

    proxy = get_paint_proxy(FPushButton, cache, cache_key, setup=_setup)
    proxy.setEnabled(enabled)
    display_text = "" if text is None else str(text)

    option = QtWidgets.QStyleOptionButton()
    option.initFrom(proxy)
    option.rect = QtCore.QRect(0, 0, rect.width(), rect.height())
    option.text = display_text
    option.features = QtWidgets.QStyleOptionButton.Flat
    option.state = QtWidgets.QStyle.State_None
    if enabled:
        option.state |= QtWidgets.QStyle.State_Enabled

    painter.save()
    painter.translate(rect.topLeft())
    proxy.style().drawControl(
        QtWidgets.QStyle.CE_PushButton, option, painter, proxy
    )
    painter.restore()


def paint_progress_bar_appearance(
    cache: dict,
    painter: QtGui.QPainter,
    rect: QtCore.QRect,
    *,
    value: int = 0,
    minimum: int = 0,
    maximum: int = 100,
    fui_status: str = "primary",
    enabled: bool = True,
) -> None:
    """Paint a horizontal progress bar left-to-right (delegate-safe, no QStyle)."""
    from forza_ui import forza_theme, utils
    from forza_ui.feedback.progress_bar import FProgressBar

    _ = cache  # kept for API compatibility with other paint_appearance helpers

    if not rect.isValid() or rect.width() <= 0 or rect.height() <= 0:
        return

    clamped = max(minimum, min(maximum, value))
    percent = utils.get_percent(clamped, minimum, maximum)

    if fui_status == FProgressBar.ErrorStatus:
        chunk_color = QtGui.QColor(forza_theme.error_6)
    elif fui_status == FProgressBar.SuccessStatus:
        chunk_color = QtGui.QColor(forza_theme.success_6)
    else:
        chunk_color = QtGui.QColor(forza_theme.primary_color)

    track_color = QtGui.QColor(forza_theme.border_color)
    text_color = QtGui.QColor(forza_theme.primary_text_color)
    if not enabled:
        chunk_color = QtGui.QColor(chunk_color)
        chunk_color.setAlpha(128)
        text_color = QtGui.QColor(text_color)
        text_color.setAlpha(128)

    radius = min(forza_theme.progress_bar_radius, rect.height() // 2, rect.width() // 2)
    radius = max(1, radius)
    bar_rect = QtCore.QRectF(rect)

    painter.save()
    painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
    painter.setPen(QtCore.Qt.NoPen)
    painter.setBrush(track_color)
    painter.drawRoundedRect(bar_rect, radius, radius)

    fill_width = int(bar_rect.width() * percent / 100.0)
    if fill_width > 0:
        fill_rect = QtCore.QRectF(
            bar_rect.left(),
            bar_rect.top(),
            fill_width,
            bar_rect.height(),
        )
        painter.save()
        painter.setClipRect(fill_rect)
        painter.setBrush(chunk_color)
        painter.drawRoundedRect(bar_rect, radius, radius)
        painter.restore()

    label = f"{int(round(percent))}%"
    font = painter.font()
    font.setPixelSize(max(8, rect.height() - 2))
    painter.setFont(font)
    painter.setPen(text_color)
    painter.drawText(rect, QtCore.Qt.AlignCenter, label)
    painter.restore()
