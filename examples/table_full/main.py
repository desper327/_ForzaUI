# -*- coding: utf-8 -*-
"""
forza_ui Table 全面能力演示

运行:
    python examples/table_full/main.py
"""

from __future__ import annotations

import os
import sys


_EXAMPLE_ROOT = os.path.dirname(os.path.abspath(__file__))
if _EXAMPLE_ROOT not in sys.path:
    sys.path.insert(0, _EXAMPLE_ROOT)


def ensure_example_paths() -> None:
    if _EXAMPLE_ROOT not in sys.path:
        sys.path.insert(0, _EXAMPLE_ROOT)


_EXAMPLE_ROOT = os.path.dirname(os.path.abspath(__file__))
_EXAMPLES_ROOT = os.path.abspath(os.path.join(_EXAMPLE_ROOT, ".."))
_FORZA_UI_ROOT = os.path.abspath(os.path.join(_EXAMPLE_ROOT, "..", ".."))
if _FORZA_UI_ROOT not in sys.path:
    sys.path.insert(0, _FORZA_UI_ROOT)
if _EXAMPLES_ROOT not in sys.path:
    sys.path.insert(0, _EXAMPLES_ROOT)

import _bootstrap  # noqa: F401

from Qt import QtWidgets

from forza_ui import forza_theme
from forza_ui.utils import application

from controllers.asset_table_controller import AssetTableController
from models.asset_model import GlobalModel


def main() -> None:
    with application() as app:
        model = GlobalModel()
        controller = AssetTableController(model)
        app.aboutToQuit.connect(controller.shutdown)
        forza_theme.apply(controller.window)
        controller.window.show()
        if QtWidgets.QApplication.instance() is app:
            app.exec()


if __name__ == "__main__":
    main()
