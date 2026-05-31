# -*- coding: utf-8 -*-
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
    )
    QT_VERSION = 6

except ImportError:
    # ── PySide2 (Nuke 13) ──────────────────────────────────────────
    from PySide2.QtWidgets import (
        QAbstractItemView,
        QAction,
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
