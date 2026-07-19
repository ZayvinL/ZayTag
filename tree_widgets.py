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

from ntpath import dirname
from _qt import (
    QAbstractItemView,
    QAction,
    QApplication,
    QCheckBox,
    QColor,
    QComboBox,
    QDir,
    QFileSystemModel,
    QFont,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QMessageBox,
    QMimeData,
    QPushButton,
    QShortcut,
    QStyledItemDelegate,
    Qt,
    QTreeView,
    QVBoxLayout,
    QWidget,
    QCursor,
    QDesktopServices,
    QKeySequence,
    QThread,
    QUrl,
    Signal,
)
import os
import sys
import shutil
import glob
import nuke
import nukescripts
import CurrentPath
import ZaySplit as cps

# Make : Mr.Cheese
# QQ : 971346144

noteword = """
    自定义字符串拆分处理函数
    user： Lenden 
    20250816
    
    根据自定义的魔法格式拆分和处理字符串，支持多种分割和截取模式
    
    参数:
        magic_format: 拆分格式字符串，由逗号分隔的多个处理规则
            魔法解释：
                魔法字符串： "*/*-1,*/*2,*/*3" 
                以符号*间隔的符号和数字，符号代表text字符串从哪个符号开始拆分，数字代表获取哪些拆分之后字符的位置
                特殊情况直接按照数字位数取用字符串，拆分的符号为 @
                
        text: 要处理的原始字符串
        joiner: 结果连接符，默认为 "_"
        ignore_empty: 是否忽略空结果，默认为 False
    
    返回:
        拼接后的字符串和处理结果列表 (joined_str, result_list)
    """

# treeview 自定义
class TreeView(QTreeView):
    def __init__(self, parent=None):
        super(TreeView, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QTreeView.DragDrop)
        self.setDefaultDropAction(Qt.CopyAction)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        # print("c")1
        if event.mimeData().hasUrls():
            # print(event.mimeData().text())
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

# ── A: 文件夹标记委托 — 包含文件的目录用颜色标注 ──
class FolderMarkDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._cache = {}  # path -> has_files

    def _dir_has_files(self, path):
        if path in self._cache:
            return self._cache[path]
        try:
            with os.scandir(path) as it:
                for entry in it:
                    if entry.is_file():
                        self._cache[path] = True
                        return True
                self._cache[path] = False
                return False
        except OSError:
            return False

    def paint(self, painter, option, index):
        if not index.isValid():
            return super().paint(painter, option, index)
        model = index.model()
        if model is None:
            return super().paint(painter, option, index)
        try:
            file_path = model.filePath(index)
            if file_path and os.path.isdir(file_path):
                if self._dir_has_files(file_path):
                    # 绿色圆点标记
                    r = option.rect
                    painter.save()
                    painter.setBrush(QColor(80, 200, 80))
                    painter.setPen(Qt.NoPen)
                    cy = r.center().y()
                    painter.drawEllipse(r.left() + 6, cy - 4, 8, 8)
                    painter.restore()
                    # 加粗字体
                    option.font.setBold(True)
        except Exception:
            pass
        super().paint(painter, option, index)

# ── 拖拽列表控件，支持拖文件到 Nuke ──
class DragListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragOnly)

    def mimeTypes(self):
        return ['text/uri-list']

    def mimeData(self, items):
        mdata = QMimeData()
        urls = []
        for item in items:
            dir_path, _ = self.parent()._parse_flat_item(item)
            if dir_path:
                urls.append(QUrl.fromLocalFile(dir_path).toString())
        mdata.setUrls([QUrl(u) for u in urls])
        return mdata

# 带treeview的基本模块 自定义
class MyTreeWa(QWidget):
    def __init__(self,parent=None):
        super(MyTreeWa,self).__init__(parent)

        label = QLabel("路径")
        self.line_edit = QLineEdit()
        self.line_edit.editingFinished.connect(self.button_refresh_Run)
        self.button = QPushButton("刷新")
        self.button.setToolTip("CN: 刷新文件浏览器\nEN: Refresh file browser")
        self.button.clicked.connect(self.button_refresh_Run)
        self.flat_mode = QComboBox()
        self.flat_mode.setToolTip("CN: 文件浏览模式\nEN: View mode - Tree / All Files / Sequences")
        self.flat_mode.addItems(["树", "所有文件", "序列整理"])
        self.flat_mode.currentIndexChanged.connect(self._on_flat_mode_changed)

        self.layout01 = QHBoxLayout()
        self.layout01.addWidget(label)
        self.layout01.addWidget(self.line_edit)
        self.layout01.addWidget(self.button)
        self.layout01.addWidget(self.flat_mode)
        self.layout01.setContentsMargins(0, 0, 0, 0)
        self.layout01.setSpacing(0)

        ## 控件
        self.tree_view = TreeView()
        # self.tree_view.setItemDelegate(FolderMarkDelegate(self.tree_view))
        self.tree_view.setGeometry(0, 0, 800, 600)
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.rootPath())
        self.file_model.setFilter(QDir.NoDotAndDotDot | QDir.AllEntries)
        self.tree_view.setModel(self.file_model)
        self.tree_view.header().setSectionResizeMode(0, QHeaderView.Interactive)
        self.tree_view.header().resizeSection(0, 340)
        self.tree_view.setSelectionMode(QAbstractItemView.ExtendedSelection)

        font = self.tree_view.font()
        font.setPointSize(13)
        self.tree_view.setFont(font)

        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.show_context_menu)

        act_copy_shortcut = QAction("复制路径 (C)", self.tree_view)
        act_copy_shortcut.setShortcut("C")
        act_copy_shortcut.setShortcutContext(Qt.WidgetShortcut)
        act_copy_shortcut.triggered.connect(self._shortcut_copy_path)
        self.tree_view.addAction(act_copy_shortcut)

        act_expand_shortcut = QAction("展开到文件 (F)", self.tree_view)
        act_expand_shortcut.setShortcut("F")
        act_expand_shortcut.setShortcutContext(Qt.WidgetShortcut)
        act_expand_shortcut.triggered.connect(self._shortcut_expand_to_files)
        self.tree_view.addAction(act_expand_shortcut)

        act_collapse_shortcut = QAction("闭合文件夹 (W)", self.tree_view)
        act_collapse_shortcut.setShortcut("W")
        act_collapse_shortcut.setShortcutContext(Qt.WidgetShortcut)
        act_collapse_shortcut.triggered.connect(self._shortcut_collapse)
        self.tree_view.addAction(act_collapse_shortcut)

        # 扁平文件列表
        self.flat_list = DragListWidget()

        act_flat_copy = QAction("复制路径 (C)", self.flat_list)
        act_flat_copy.setShortcut("C")
        act_flat_copy.setShortcutContext(Qt.WidgetShortcut)
        act_flat_copy.triggered.connect(self._flat_shortcut_copy)
        self.flat_list.addAction(act_flat_copy)

        act_flat_open = QAction("打开文件夹 (F)", self.flat_list)
        act_flat_open.setShortcut("F")
        act_flat_open.setShortcutContext(Qt.WidgetShortcut)
        act_flat_open.triggered.connect(self._flat_shortcut_open)
        self.flat_list.addAction(act_flat_open)

        self.flat_list.setFont(font)
        self.flat_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.flat_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.flat_list.customContextMenuRequested.connect(self._show_flat_context_menu)
        self.flat_list.itemDoubleClicked.connect(self._on_flat_item_double_clicked)
        self.flat_list.hide()

        self.layout02 = QVBoxLayout()
        self.layout02.addLayout(self.layout01)
        self.layout02.addWidget(self.tree_view)
        self.layout02.addWidget(self.flat_list)
        self.layout02.setContentsMargins(0, 0, 0, 0)
        self.layout02.setSpacing(0)

        self.setLayout(self.layout02)

    def _shortcut_copy_path(self):
        for idx in self.tree_view.selectionModel().selectedIndexes():
            if idx.isValid() and idx.column() == 0:
                self.copy_path(self.tree_view, self.file_model, idx)
                return

    def _shortcut_expand_to_files(self):
        for idx in self.tree_view.selectionModel().selectedIndexes():
            if idx.isValid() and idx.column() == 0:
                self._expand_to_files(self.tree_view, idx)
                return

    def _shortcut_collapse(self):
        for idx in self.tree_view.selectionModel().selectedIndexes():
            if idx.isValid() and idx.column() == 0:
                self.tree_view.setExpanded(idx, False)
                return

    def show_context_menu(self, pos):
        active_tree_view = self.tree_view
        active_curtreemod = self.file_model
        index = active_tree_view.indexAt(pos)

        if index.isValid():
            menu = QMenu(self)
            action_copy_path = QAction("复制路径 (C)", self)
            action_copy_path.triggered.connect(lambda: self.copy_path(active_tree_view, active_curtreemod, index))
            menu.addAction(action_copy_path)

            action_open_path = QAction("打开文件", self)
            # shortcut = QKeySequence(Qt.ALT + Qt.)
            # action_open_path.setShortcut(shortcut)
            action_open_path.triggered.connect(lambda: self.open_path(active_curtreemod,index))
            menu.addAction(action_open_path)

            action_expand_all = QAction("展开文件夹", self)
            action_expand_all.triggered.connect(
                lambda: self.expand_all_folders(active_tree_view, active_curtreemod, index))
            menu.addAction(action_expand_all)

            action_expand_False = QAction("闭合文件夹 (W)", self)
            action_expand_False.triggered.connect(
                lambda: self.action_expand_False(active_tree_view, active_curtreemod, index))
            menu.addAction(action_expand_False)

            action_expand_to_files = QAction("展开到文件 (F)", self)
            action_expand_to_files.triggered.connect(
                lambda: self._expand_to_files(active_tree_view, index))
            menu.addAction(action_expand_to_files)

            # new_folder_action = QAction("新建文件夹", self)
            # new_folder_action.triggered.connect(
                # lambda: self.createFolder(active_tree_view, active_curtreemod, index))
            # menu.addAction(new_folder_action)

            # del_folder_action = QAction("删除文件夹", self)
            # del_folder_action.triggered.connect(
                # lambda: self.deleteFolder(active_tree_view, active_curtreemod, index))
            # menu.addAction(del_folder_action)

            importAsRead = QAction("选中文件夹下的所有文件作为Read导入", self)
            importAsRead.triggered.connect(
                lambda: self.importAsRead_fun(active_curtreemod, index))
            menu.addAction(importAsRead)

            menu.exec_(active_tree_view.viewport().mapToGlobal(pos))
    #     else:
    #         menu = QMenu(self)
    #         action_created01 = QAction("新建测试", self)
    #         action_created01.triggered.connect(lambda: self.created01())
    #         menu.addAction(action_created01)
    #         menu.exec_(active_tree_view.viewport().mapToGlobal(pos))
    #
    # def created01(self):
    #     # 创建测试
    #     p = self.line_edit.text()
    #     print("TEST")
    #     print(p)

    def importAsRead_fun(self,active_curtreemod, index):
        file_model = active_curtreemod
        file_path = file_model.filePath(index)
        gvf = nuke.getFileNameList(file_path)
        if gvf:
            gvf = [file_path + "/" + i for i in gvf]
        else:
            gvf = nuke.getFileNameList(os.path.dirname(file_path))
            gvf = [os.path.dirname(file_path) + "/" + i for i in gvf]

        for i in range(0, len(gvf)):
            gv = gvf[i]
            r = nuke.createNode('Read', inpanel=False)
            r['file'].fromUserText(gv)
            r['raw'].setValue(True)
            if i == 0:
                xps = r.xpos()
                yps = r.ypos()
            else:
                xps += 200
                yps = yps
                r.setXYpos(xps, yps)

    def deleteFolder(self, tree_view, file_model, index):
        folder_path = file_model.filePath(index)  # 获取文件夹路径
        response = QMessageBox.question(self, "确认删除", "确定要删除此文件夹及其内容吗？", QMessageBox.Yes | QMessageBox.No)
        if response == QMessageBox.Yes:
            try:
                shutil.rmtree(folder_path)  # 递归删除文件夹及其内容
                # 更新文件模型
                file_model.remove(index)
                # file_model.refresh(index.parent())
            except Exception as e:
                QMessageBox.critical(self, "删除失败", "删除文件夹时出现错误：" + str(e))

    def createFolder(self, tree_view, file_model, index):
        #parent_index = index.parent()  # 获取父级索引
        parent_index = index#.parent()  # 获取父级索引
        if parent_index.isValid():  # 确保父级索引有效
            parent_path = file_model.filePath(parent_index)  # 获取父级文件夹路径
            new_folder_name, ok = QInputDialog.getText(self, "新建文件夹", "请输入文件夹名称:")
            if ok and new_folder_name:
                new_folder_path = os.path.join(parent_path, new_folder_name)  # 构造新文件夹路径
                if not os.path.exists(new_folder_path):  # 确保文件夹不存在
                    os.mkdir(new_folder_path)  # 创建新文件夹
                    #file_model.refresh(parent_index)  # 刷新父级索引以显示新文件夹
                else:
                    QMessageBox.warning(self, "错误", "文件夹已存在！")
            else:
                QMessageBox.warning(self, "错误", "无效的文件夹名称！")
        else:
            QMessageBox.warning(self, "错误", "无效的父级文件夹！")

    def action_expand_False(self, cindex, cview, myindex):
        # 获取TreeView的选择模型
        selection_model = cindex.selectionModel()
        # 获取选定项的索引列表
        selected_indexes = selection_model.selectedIndexes()
        if selected_indexes != []:
            for i in selected_indexes:
                # cindex.expand(i)
                cindex.setExpanded(i, False)
                paths = self.get_subdirectories(i)
                if paths == []:
                    return
                # 遍历路径列表
                for path in paths:
                    # 查找路径对应的节点
                    nindex = cview.index(path)

                    # 检查节点是否有效并可展开
                    if nindex.isValid() and cview.hasChildren(nindex):
                        # 设置节点展开
                        cindex.setExpanded(nindex, False)
        else:
            cindex.setExpanded(myindex, False)
            paths = self.get_subdirectories(myindex)
            if paths == []:
                return
            # 遍历路径列表
            for path in paths:
                # 查找路径对应的节点
                nindex = cview.index(path)

                # 检查节点是否有效并可展开
                if nindex.isValid() and cview.hasChildren(nindex):
                    # 设置节点展开
                    cindex.setExpanded(nindex, False)

    def expand_all_folders(self, cindex, cview, myindex):
        # 展开前20个子文件夹
        # 获取TreeView的选择模型
        selection_model = cindex.selectionModel()
        # 获取选定项的索引列表
        selected_indexes = selection_model.selectedIndexes()
        if selected_indexes != []:
            for i in selected_indexes:
                cindex.expand(i)
                paths = self.get_subdirectories(i)
                if paths == []:
                    return
                # 遍历路径列表
                for path in paths:
                    # 查找路径对应的节点
                    nindex = cview.index(path)

                    # 检查节点是否有效并可展开
                    if nindex.isValid() and cview.hasChildren(nindex):
                        # 设置节点展开
                        cindex.setExpanded(nindex, True)
        else:
            cindex.expand(myindex)
            paths = self.get_subdirectories(myindex)
            if paths == []:
                return
            # 遍历路径列表
            for path in paths:
                # 查找路径对应的节点
                nindex = cview.index(path)

                # 检查节点是否有效并可展开
                if nindex.isValid() and cview.hasChildren(nindex):
                    # 设置节点展开
                    cindex.setExpanded(nindex, True)

    def get_subdirectories(self, index):
        # 获取单选路径的 前20 子文件夹 方便展开
        file_model = self.file_model
        file_path = file_model.filePath(index)

        if not os.path.isdir(file_path):
            QMessageBox.warning(self, "提示", "选中项不是文件夹！")
            return []

        subdirectories = []
        for root, dirs, files in os.walk(file_path):
            for dir in dirs:
                if len(subdirectories) > 20:
                    return subdirectories
                else:
                    subdirectories.append(os.path.join(root, dir))

        return subdirectories

    def open_path(self, ctrmodget,index):
        # 复制路径的功能
        file_model = ctrmodget
        file_path = file_model.filePath(index)
        # QApplication.clipboard().setText(file_path)
        # os.startfile(file_path)
        path = file_path
        url = QUrl.fromLocalFile(path)
        QDesktopServices.openUrl(url)

    def copy_path(self, ctreeget, ctrmodget, index):
        paths = []
        selection_model = ctreeget.selectionModel()
        # 获取选中的索引列表
        selected_indexes = selection_model.selectedIndexes()
        # 提取每个索引对应的路径信息并复制
        for ide in selected_indexes:
            gg = ctrmodget.filePath(ide)
            if gg not in paths and os.path.exists(gg):
                paths.append(gg)

        if paths:
            QApplication.clipboard().setText("\n".join(paths))

    # ── B: 展开到文件 ──
    def _expand_to_files(self, tree_view, index):
        """递归展开目录，跳过只有子文件夹的层级，直到找到含有文件的目录。"""
        model = tree_view.model()
        path = model.filePath(index)
        if not os.path.isdir(path):
            return
        try:
            entries = list(os.scandir(path))
        except OSError:
            return
        has_files = any(e.is_file() for e in entries)
        subdirs = [e.path for e in entries if e.is_dir()]
        if has_files or not subdirs:
            tree_view.expand(index)
            return
        # 只有子目录没有文件 → 展开，继续深入每个子目录
        tree_view.expand(index)
        for sub in subdirs:
            child_idx = model.index(sub)
            if child_idx.isValid():
                self._expand_to_files(tree_view, child_idx)

    # ── C: 扁平文件列表 ──
    def _on_flat_mode_changed(self, idx):
        if idx == 0:  # 树
            self.flat_list.hide()
            self.tree_view.show()
        else:
            self.tree_view.hide()
            self._populate_flat_list()
            self.flat_list.show()

    @staticmethod
    def _parse_frame_range(files):
        """从一组同前缀同扩展名的文件中提取帧范围和缺失帧。

        返回 (prefix, ext, first, last, missing, frame_padding)
        例如 file.0001.exr, file.0003.exr, file.0005.exr
          → ('file.', '.exr', 1, 5, [2, 4], 4)
        """
        import re
        frames = []
        base_prefix = None
        base_ext = None
        padding = 0
        for fp in files:
            name = os.path.basename(fp)
            m = re.match(r'^(.+?)(\d+)(\.[^.]+)$', name)
            if not m:
                # try v001 pattern
                m = re.match(r'^(.+?)[._]v(\d+)(\.[^.]+)$', name)
                if not m:
                    return None, None, None, None, None, None
            prefix = m.group(1)
            pad = len(m.group(2))
            ext = m.group(3)
            if base_prefix is None:
                base_prefix = prefix
                base_ext = ext
                padding = pad
            if prefix != base_prefix or ext != base_ext:
                return None, None, None, None, None, None
            frames.append(int(m.group(2)))
        if not frames:
            return None, None, None, None, None, None
        frames.sort()
        first, last = frames[0], frames[-1]
        missing = [f for f in range(first, last + 1) if f not in frames]
        return base_prefix, base_ext, first, last, missing, padding

    def _populate_flat_list(self):
        self.flat_list.clear()
        root_path = self.line_edit.text()
        if not os.path.isdir(root_path):
            root_path = self.file_model.rootPath()
        all_files = list(dict.fromkeys(
            os.path.join(dirpath, f)
            for dirpath, dirnames, filenames in os.walk(root_path)
            for f in filenames
        ))
        all_files.sort()

        if self.flat_mode.currentIndex() == 1:  # 所有文件
            for fp in all_files:
                name = os.path.basename(fp)
                item = QListWidgetItem(name)
                item.setToolTip(fp)
                self.flat_list.addItem(item)
                
            return

        # 序列整理模式
        import re
        by_dir = {}
        for fp in all_files:
            d = os.path.dirname(fp)
            by_dir.setdefault(d, []).append(fp)

        for d, files in sorted(by_dir.items()):
            grouped = set()
            for i, fp in enumerate(files):
                if i in grouped:
                    continue
                name = os.path.basename(fp)
                full = d + "/" + name
                m = re.match(r'^(.+?)(\d+)(\.[^.]+)$', name)
                if not m:
                    m = re.match(r'^(.+?)[._]v(\d+)(\.[^.]+)$', name)
                if not m:
                    item = QListWidgetItem(name)
                    item.setToolTip(full)
                    self.flat_list.addItem(item)
                    grouped.add(i)
                    continue
                prefix = m.group(1)
                ext = m.group(3)
                pad = len(m.group(2))
                pattern = re.compile(
                    r'^' + re.escape(prefix) + r'(\d{' + str(pad) + r'})'
                    + re.escape(ext) + r'$'
                )
                seq_files = [fp2 for j, fp2 in enumerate(files)
                             if j not in grouped and pattern.match(os.path.basename(fp2))]
                if len(seq_files) <= 1:
                    item = QListWidgetItem(name)
                    item.setToolTip(full)
                    self.flat_list.addItem(item)
                    grouped.add(i)
                else:
                    grouped.update(files.index(f) for f in seq_files)
                    seq_files.sort()
                    first_name = os.path.basename(seq_files[0])
                    last_name = os.path.basename(seq_files[-1])
                    mf = pattern.match(first_name)
                    ml = pattern.match(last_name)
                    first_frame = int(mf.group(1)) if mf else 0
                    last_frame = int(ml.group(1)) if ml else 0
                    all_frames = [int(pattern.match(os.path.basename(f)).group(1))
                                  for f in seq_files
                                  if pattern.match(os.path.basename(f))]
                    all_frames.sort()
                    missing = [f for f in range(first_frame, last_frame + 1) if f not in all_frames]
                    label = "%s%s[%s-%s]%s" % (prefix, "%0" + str(pad) + "d", str(first_frame).zfill(pad), str(last_frame).zfill(pad), ext)
                    tooltip = "目录: %s\n帧范围: %d-%d (共 %d 帧)" % (d, first_frame, last_frame, len(seq_files))
                    if missing:
                        tooltip += "\n缺失帧: %s" % str(missing)[:200]
                    item = QListWidgetItem(label)
                    item.setToolTip(tooltip)
                    self.flat_list.addItem(item)
                    
            for i, fp in enumerate(files):
                if i not in grouped:
                    name = os.path.basename(fp)
                    full = d + "/" + name
                    item = QListWidgetItem(name)
                    item.setToolTip(full)
                    self.flat_list.addItem(item)

    def _parse_flat_item(self, item):
        tip = item.toolTip()
        if tip.startswith("目录: "):
            dir_path = tip.split("\n")[0]
            dir_path = dir_path[4:].strip()
            dir_path = dir_path.replace("\\", "/")
            copy_path = os.path.dirname(dir_path) + "/"
            # print(dir_path)
            return copy_path,dir_path
        else:
            dir_path = tip.strip()
            dir_path = dir_path.replace("\\", "/")
            copy_path = os.path.dirname(dir_path) + "/"
            # print(dir_path)
            return copy_path,dir_path

    def _flat_shortcut_copy(self):
        item = self.flat_list.currentItem()
        if item:
            copy_path, _ = self._parse_flat_item(item)
            if copy_path:
                QApplication.clipboard().setText(copy_path)

    def _flat_shortcut_open(self):
        item = self.flat_list.currentItem()
        if item:
            _, dir_path = self._parse_flat_item(item)
            if dir_path:
                QDesktopServices.openUrl(QUrl.fromLocalFile(dir_path))

    def _show_flat_context_menu(self, pos):
        item = self.flat_list.itemAt(pos)
        menu = QMenu(self)
        if item:
            copy_path, dir_path = self._parse_flat_item(item)

            def _do_copy():
                QApplication.clipboard().setText(dir_path)
            def _do_open():
                QDesktopServices.openUrl(QUrl.fromLocalFile(copy_path))
            def _do_read():
                self._flat_import_as_read(dir_path)

            act_copy = QAction("复制路径", self)
            act_copy.triggered.connect(_do_copy)
            menu.addAction(act_copy)
            act_open = QAction("在资源管理器打开", self)
            act_open.triggered.connect(_do_open)
            menu.addAction(act_open)
            act_read = QAction("作为Read导入", self)
            act_read.triggered.connect(_do_read)
            menu.addAction(act_read)
        menu.exec_(self.flat_list.viewport().mapToGlobal(pos))

    def _flat_import_as_read(self, dir_path):
        if not dir_path:
            return
        gvf = nuke.getFileNameList(dir_path)
        if gvf:
            gvf = [dir_path + "/" + i for i in gvf]
        else:
            gvf = nuke.getFileNameList(os.path.dirname(dir_path))
            gvf = [os.path.dirname(dir_path) + "/" + i for i in gvf]
        for i, gv in enumerate(gvf):
            r = nuke.createNode('Read', inpanel=False)
            r['file'].fromUserText(gv)
            r['raw'].setValue(True)
            if i == 0:
                xps = r.xpos()
                yps = r.ypos()
            else:
                xps += 200
                r.setXYpos(xps, yps)

    def _on_flat_item_double_clicked(self, item):
        dir_path, is_seq = self._parse_flat_item(item)
        target = dir_path if is_seq else os.path.join(dir_path, item.text()) if dir_path else item.text()
        if os.path.exists(target):
            QDesktopServices.openUrl(QUrl.fromLocalFile(target))

    def button_refresh_Run(self):
        p = self.line_edit.text()
        self.tree_view.setRootIndex(self.file_model.index(p))
        if self.flat_mode.currentIndex() != 0:
            self._populate_flat_list()

    def set_line_edit_text(self, text):
        # 设置 QLineEdit 控件的文本内容
        self.line_edit.setText(text)
        self.button_refresh_Run()

##### 主要工具界面

### treeview 拖拽

class FileCopyWorker(QThread):
    finished = Signal()

    def __init__(self, file_paths, target_path, parent=None):
        super(FileCopyWorker, self).__init__(parent)
        self.file_paths = file_paths
        self.target_path = target_path

    def run(self):
        for file_path in self.file_paths:
            try:
                shutil.copy2(file_path, self.target_path)
                print("复制文件:", file_path, "到目标路径:", self.target_path)
            except Exception as e:
                print("复制文件失败:", str(e))
        self.finished.emit()

#####

