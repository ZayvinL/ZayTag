# -*- coding: utf-8 -*-
# Copyright 2026 LIUXIAOBO (刘晓波)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""PySide2 / PySide6 统一导入兼容层。

用法:
    from _qt import QApplication, Qt, QMainWindow, QT_VERSION, ...
"""

# ── PySide6 (Nuke 14+) ──────────────────────────────────────────────
try:
    from PySide6.QtWidgets import (
        QAbstractItemView,
        QApplication,
        QCheckBox,
        QComboBox,
        QDialog,
        QDialogButtonBox,
        QFileDialog,
        QFileSystemModel,
        QHBoxLayout,
        QHeaderView,
        QInputDialog,
        QLabel,
        QLineEdit,
        QListView,
        QListWidget,
        QListWidgetItem,
        QMainWindow,
        QMenu,
        QMessageBox,
        QPushButton,
        QSplitter,
        QStyledItemDelegate,
        QTabWidget,
        QTextBrowser,
        QTreeView,
        QVBoxLayout,
        QWidget,
    )
    from PySide6.QtCore import (
        QDir,
        QMimeData,
        QThread,
        Qt,
        QUrl,
        Signal,
    )
    from PySide6.QtGui import (
        QAction,
        QColor,
        QCursor,
        QDesktopServices,
        QFont,
        QKeySequence,
        QShortcut,
    )
    QT_VERSION = 6

except ImportError:
    # ── PySide2 (Nuke 13) ──────────────────────────────────────────
    from PySide2.QtWidgets import (
        QAbstractItemView,
        QAction,
        QApplication,
        QShortcut,
        QCheckBox,
        QComboBox,
        QDialog,
        QDialogButtonBox,
        QFileDialog,
        QFileSystemModel,
        QHBoxLayout,
        QHeaderView,
        QInputDialog,
        QLabel,
        QLineEdit,
        QListView,
        QListWidget,
        QListWidgetItem,
        QMainWindow,
        QMenu,
        QMessageBox,
        QPushButton,
        QSplitter,
        QStyledItemDelegate,
        QTabWidget,
        QTextBrowser,
        QTreeView,
        QVBoxLayout,
        QWidget,
    )
    from PySide2.QtCore import (
        QDir,
        QMimeData,
        QThread,
        Qt,
        QUrl,
        Signal,
    )
    from PySide2.QtGui import (
        QColor,
        QCursor,
        QDesktopServices,
        QFont,
        QKeySequence,
    )
    QT_VERSION = 5

__all__ = [
    # Widgets
    "QAbstractItemView",
    "QAction",
    "QApplication",
    "QCheckBox",
    "QComboBox",
    "QDialog",
    "QDialogButtonBox",
    "QFileDialog",
    "QFileSystemModel",
    "QHBoxLayout",
    "QHeaderView",
    "QInputDialog",
    "QLabel",
    "QLineEdit",
    "QListView",
    "QListWidget",
    "QListWidgetItem",
    "QMainWindow",
    "QMenu",
    "QMessageBox",
    "QPushButton",
    "QSplitter",
    "QStyledItemDelegate",
    "QTabWidget",
    "QTreeView",
    "QVBoxLayout",
    "QWidget",
    # Core
    "QDir",
    "QThread",
    "Qt",
    "QUrl",
    "Signal",
    # Gui
    "QColor",
    "QCursor",
    "QDesktopServices",
    "QFont",
    "QKeySequence",
    # Version
    "QT_VERSION",
]
