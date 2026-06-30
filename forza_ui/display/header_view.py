# -*- coding: utf-8 -*-
"""Styled table/tree header view."""

from __future__ import annotations

import functools

from Qt import QtCore, QtGui, QtWidgets

from forza_ui.navigation.menu import FMenu


def _source_model(model):
    while isinstance(model, QtCore.QSortFilterProxyModel):
        model = model.sourceModel()
    return model


class FHeaderView(QtWidgets.QHeaderView):
    def __init__(self, orientation, parent=None, show_sort_indicator=True):
        super().__init__(orientation, parent)
        self.setMovable(True)
        self.setClickable(True)
        self.setSortIndicatorShown(show_sort_indicator)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._slot_context_menu)
        self.setDefaultAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.setProperty(
            "orientation",
            "horizontal" if orientation == QtCore.Qt.Horizontal else "vertical",
        )

    @QtCore.Slot(QtCore.QPoint)
    def _slot_context_menu(self, point):
        model = _source_model(self.model())
        if model is None:
            return

        context_menu = FMenu(parent=self)
        fit_action = context_menu.addAction(self.tr("Fit Size"))
        fit_action.triggered.connect(functools.partial(self._slot_set_resize_mode, True))
        context_menu.addSeparator()
        for column in range(self.count()):
            header_text = model.headerData(column, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole)
            action = context_menu.addAction(header_text or str(column))
            action.setCheckable(True)
            action.setChecked(not self.isSectionHidden(column))
            action.toggled.connect(functools.partial(self._slot_set_section_visible, column))
        context_menu.exec_(QtGui.QCursor.pos() + QtCore.QPoint(10, 10))

    @QtCore.Slot(QtCore.QModelIndex, int)
    def _slot_set_section_visible(self, index, flag):
        self.setSectionHidden(index, not flag)

    @QtCore.Slot(bool)
    def _slot_set_resize_mode(self, flag):
        if flag:
            self.resizeSections(QtWidgets.QHeaderView.ResizeToContents)
        else:
            self.resizeSections(QtWidgets.QHeaderView.Interactive)

    def setClickable(self, flag):
        try:
            QtWidgets.QHeaderView.setSectionsClickable(self, flag)
        except AttributeError:
            QtWidgets.QHeaderView.setClickable(self, flag)

    def setMovable(self, flag):
        try:
            QtWidgets.QHeaderView.setSectionsMovable(self, flag)
        except AttributeError:
            QtWidgets.QHeaderView.setMovable(self, flag)

    def resizeMode(self, index):
        try:
            QtWidgets.QHeaderView.sectionResizeMode(self, index)
        except AttributeError:
            QtWidgets.QHeaderView.resizeMode(self, index)

    def setResizeMode(self, mode):
        try:
            QtWidgets.QHeaderView.setResizeMode(self, mode)
        except AttributeError:
            QtWidgets.QHeaderView.setSectionResizeMode(self, mode)
