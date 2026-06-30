# -*- coding: utf-8 -*-
"""Add forza_ui and Qt shim to sys.path for standalone examples."""

from __future__ import annotations

import os
import sys

_FORZA_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
_FORZA_UI_ROOT = os.path.join(_FORZA_ROOT, "Forza_Lib", "forza_ui")
_QT_VENDOR = os.path.join(_FORZA_ROOT, "Forza_Lib", "vendor")

for path in (_QT_VENDOR, _FORZA_UI_ROOT):
    if path not in sys.path:
        sys.path.insert(0, path)
