# -*- coding: utf-8 -*-
try:
    from PySide6.QtGui import *
    from PySide6.QtCore import *
    from PySide6.QtWidgets import *
except:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
import sys
import os
import json
import shutil
import glob
import CurrentPath
import nuke
import nukescripts
import Cheese_Pipline_split as cps



# 基础的功能件

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





# 带treeview的基本模块 自定义
class MyTreeWa(QWidget):
    def __init__(self,parent=None):
        super(MyTreeWa,self).__init__(parent)

        ## 控件
        label = QLabel("路径")
        self.line_edit = QLineEdit()
        self.line_edit.editingFinished.connect(self.button_refresh_Run)
        self.button = QPushButton("刷新")
        self.button.clicked.connect(self.button_refresh_Run)

        self.layout01 = QHBoxLayout()
        self.layout01.addWidget(label)
        self.layout01.addWidget(self.line_edit)
        self.layout01.addWidget(self.button)
        self.layout01.setContentsMargins(0, 0, 0, 0)
        self.layout01.setSpacing(0)

        ## 控件
        self.tree_view = TreeView()
        self.tree_view.setGeometry(0, 0, 800, 600)
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.rootPath())
        self.file_model.setFilter(QDir.NoDotAndDotDot | QDir.AllEntries)
        self.tree_view.setModel(self.file_model)
        self.tree_view.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # self.tree_view.setSelectionMode(QTreeView.ExtendedSelection)
        self.tree_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # self.tree_view.setAlternatingRowColors(True)
        # self.tree_view.setSortingEnabled(True)
        # self.tree_view.setEditTriggers(QAbstractItemView.DoubleClicked)
        # self.tree_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        
        # 设置字体大小
        font = self.tree_view.font()  # 获取默认字体
        font.setPointSize(13)  # 设置字体大小为 16 像素
        self.tree_view.setFont(font)  # 设置 QTreeView 的字体


        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.show_context_menu)

        self.layout02 = QVBoxLayout()
        self.layout02.addLayout(self.layout01)
        self.layout02.addWidget(self.tree_view)
        self.layout02.setContentsMargins(0, 0, 0, 0)
        self.layout02.setSpacing(0)

        self.setLayout(self.layout02)
        
        
        

    def show_context_menu(self, pos):
        active_tree_view = self.tree_view
        active_curtreemod = self.file_model
        index = active_tree_view.indexAt(pos)

        if index.isValid():
            menu = QMenu(self)
            action_copy_path = QAction("复制路径", self)
            # shortcut = QKeySequence(Qt.SHIFT + Qt.Key_D)
            # action_copy_path.setShortcut(shortcut)
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

            action_expand_False = QAction("闭合文件夹", self)
            action_expand_False.triggered.connect(
                lambda: self.action_expand_False(active_tree_view, active_curtreemod, index))
            menu.addAction(action_expand_False)

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
        from PySide2 import QtCore,QtGui
        path = file_path
        url = QtCore.QUrl.fromLocalFile(path)
        QtGui.QDesktopServices.openUrl(url)

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

    def button_refresh_Run(self):
        p = self.line_edit.text()
        self.tree_view.setRootIndex(self.file_model.index(p))

    def set_line_edit_text(self, text):
        # 设置 QLineEdit 控件的文本内容
        self.line_edit.setText(text)
        self.button_refresh_Run()


##### 主要工具界面


# 输入框 两个input 信息内容
class MyDialog(QDialog):
    def __init__(self, item, text, parent=None):
        super(MyDialog, self).__init__(parent)

        self.setWindowTitle("对话框")

        # 创建布局
        layout = QVBoxLayout(self)

        # 添加标签和输入框1
        label1 = QLabel("路径 ：", self)
        self.lineedit1 = QLineEdit(self)
        self.lineedit1.setText(item)
        layout.addWidget(label1)
        layout.addWidget(self.lineedit1)

        # 添加标签和输入框2
        label2 = QLabel("备注 ：", self)
        self.lineedit2 = QTextEdit(self)
        self.lineedit2.setPlainText(text)
        layout.addWidget(label2)
        layout.addWidget(self.lineedit2)

        # 添加按钮
        buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        layout.addWidget(buttonbox)

    def get_inputs(self):
        return self.lineedit1.text(), self.lineedit2.toPlainText()

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


class TreeView(QTreeView):
    def __init__(self, parent=None):
        super(TreeView, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QTreeView.DragDrop)
        self.setDefaultDropAction(Qt.CopyAction)

    def dragEnterEvent(self, event):
        # print("b")
        if event.mimeData().hasUrls():
            # print(event.mimeData().text())
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        # print("a")
        if event.mimeData().hasUrls():
            # print(event.mimeData().text())
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

            # file_paths = [url.toLocalFile() for url in event.mimeData().urls()]
            # print(file_paths)

            # copy_worker = FileCopyWorker(file_paths, target_path)
            # copy_worker.finished.connect(self.file_copy_finished)
            # copy_worker.start()
        else:
            event.ignore()


#####



class getfileToolspaceal(QMainWindow):  # QDialog # QWidget # QMainWindow
    def __init__(self, parent=None):
        super(getfileToolspaceal, self).__init__(parent)

        self.setUpUIGN()

    def setUpUIGN(self):
        # 设置整体透明度
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(0.95)
        
        # combox 2 个  信息采样列表，路径列表
        # button 3 个 添加，删除，编辑
        # lineedit 3 个项目名，场次号，镜头号，
        ###-------关键字----------------
        self.pathsset = "ALLPATHS"
        # self.sampleset = "SAMPLERULER"
        ###-----------------------
        
        self.qed_pro = QLineEdit()
        self.qed_pro.setPlaceholderText("项目名{P}")
        self.qed_seq = QLineEdit()
        self.qed_seq.setPlaceholderText("场次号{E}")
        self.qed_sht = QLineEdit()
        self.qed_sht.setPlaceholderText("镜头号{S}")
        
        label_sampleinfo = QLabel("采样规则 ：")
        label_sampleinfo.setToolTip(noteword)
        
        self.sampleinfo = QComboBox() # 信息采样的设定规则，
        self.sampleinfo.setEditable(True)
        self.sampleinfo.setToolTip(noteword)
        self.btrefresh2 = QPushButton("从Read获取")
        self.btrefresh2.clicked.connect(self.getPES_Read)

        self.btrefresh3 = QPushButton("从工程获取")
        self.btrefresh3.clicked.connect(self.getPES_Read)
        
        self.btrefresh4 = QPushButton("保存规则")
        self.btrefresh4.clicked.connect(self.savesampleruler)
        
        self.btrefresh5 = QPushButton("删除规则")
        self.btrefresh5.clicked.connect(self.delsampleruler)
        
        self.layout_a1 = QHBoxLayout()
        self.layout_a2 = QHBoxLayout()
        
        # self.layout_a1.setMargin(0)
        
        self.layout_a1.addWidget(self.qed_pro,1)
        self.layout_a1.addWidget(self.qed_seq,1)
        self.layout_a1.addWidget(self.qed_sht,1)
        
        self.layout_a2.addWidget(label_sampleinfo,0.1)
        self.layout_a2.addWidget(self.sampleinfo,1)
        self.layout_a2.addWidget(self.btrefresh2,0.6)
        self.layout_a2.addWidget(self.btrefresh3,0.6)
        self.layout_a2.addWidget(self.btrefresh4,0.6)
        self.layout_a2.addWidget(self.btrefresh5,0.6)
        
        
        self.layout_b1 = QHBoxLayout()
        # self.layout_b1.setMargin(0)
        self.layout_b2 = QHBoxLayout()
        # self.layout_b2.setMargin(0)
        # self.layout_b3 = QHBoxLayout()
        # self.layout_b3.setMargin(0)
        label_pathsset = QLabel("路径设定包 ：")
        # 每个项目自定义一套路径包，叫项目路径设定包也行
        self.prosetfile = QComboBox()  # 预设的路径包，每个项目可以不一样，包含不同的路径预设，
        self.prosetfile.currentIndexChanged.connect(self.reload_pathsset) # 刷新路径集合
        self.prosetfile.currentIndexChanged.connect(self.reload_pathtypeset) # 刷新 路径预设组
        self.prosetfile.currentIndexChanged.connect(self.reload_curpathset) # 刷新路径预设组选项
        self.but_add_prosetfile = QPushButton("添加新包")
        self.but_add_prosetfile.clicked.connect(self.but_add_prosetfile_Run)
        self.but_res_prosetfile = QPushButton("刷新包")
        self.but_res_prosetfile.clicked.connect(self.but_res_prosetfile_Run)
        self.but_res_prosetfile.clicked.connect(self.load_sampleruler)
        self.but_del_prosetfile = QPushButton("删除包")
        self.but_del_prosetfile.clicked.connect(self.but_del_prosetfile_Run)
        self.but_del_prosetfile.clicked.connect(self.load_sampleruler)
        self.but_sav_prosetfile = QPushButton("保存路径")
        self.but_sav_prosetfile.clicked.connect(self.but_sav_prosetfile_Run)
        
        self.layout_b1.addWidget(label_pathsset,0.1)
        self.layout_b1.addWidget(self.prosetfile,1)
        self.layout_b1.addWidget(self.but_add_prosetfile,0.3)
        self.layout_b1.addWidget(self.but_res_prosetfile,0.3)
        self.layout_b1.addWidget(self.but_del_prosetfile,0.3)
        self.layout_b1.addWidget(self.but_sav_prosetfile,0.3)
        
        label_pathstool = QLabel("路径预设组 ：")
        self.pathtype = QComboBox() # 不同的路径组合，完成特别的需求，比如灯光路径，查大样的路径dailies路径这些，可以制作一个预设 
        self.pathtype.currentIndexChanged.connect(self.reload_curpathset)
        self.but_add_pathtype = QPushButton("保存设定")
        self.but_add_pathtype.clicked.connect(self.but_add_pathtype_Run)
        # self.but_add_pathtype.clicked.connect(self.reload_pathtypeset)
        self.but_del_pathtype = QPushButton("删除设定")
        self.but_del_pathtype.clicked.connect(self.but_del_pathtype_Run)
        self.but_opn_pathtype = QPushButton("打开")
        self.but_opn_pathtype.clicked.connect(self.refresh_searchPath)
        
        self.layout_b2.addWidget(label_pathstool,0.1)
        self.layout_b2.addWidget(self.pathtype,1)
        
        self.layout_b2.addWidget(self.but_opn_pathtype,1)
        self.layout_b2.addWidget(self.but_add_pathtype,0.3)
        self.layout_b2.addWidget(self.but_del_pathtype,0.3)
        

        

        
        
        
        ############################///////////////////////////////////////////////////////////////////////////////
        
        self.tab01 = QTabWidget()
        self.tab02 = QTabWidget()
        self.tab01.setTabsClosable(True)

        tab_bar = self.tab01.tabBar()
        tab_bar.tabCloseRequested.connect(self.close_tab)

        self.wida = QWidget()
        self.widb = QWidget()
        self.wida.setContentsMargins(0, 0, 0, 0)
        self.widb.setContentsMargins(0, 0, 0, 0)
        self.tab02.addTab(self.widb, "文件管理")
        self.tab02.addTab(self.wida, "路径集合")
        
        
        
        # 路径集合
        self.searchFile = QListWidget()  # 搜索预设路径
        self.searchFile.setResizeMode(QListView.Fixed)
        self.searchFile.itemDoubleClicked.connect(self.myeditItem)
        self.searchFile.setContextMenuPolicy(Qt.CustomContextMenu)  # 打开右键菜单共鞥你
        self.searchFile.customContextMenuRequested.connect(self.menu_scr)
        
        
        self.layout_a = QVBoxLayout()
        self.layout_c = QVBoxLayout()
        # self.layout_c.setMargin(0)
        # self.layout_a.setMargin(0)
        self.layout_a.setSpacing(0)
        
        self.layout_a.addWidget(self.searchFile)
        self.wida.setLayout(self.layout_a)
        
        self.layout_c.addWidget(self.tab01)
        self.widb.setLayout(self.layout_c)
        
        
        ############################///////////////////////////////////////////////////////////////////////////////
        
        
        
        
        
        
        
        
        
        
        self.master = QVBoxLayout()
        # self.master.setMargin(0)
        
        self.master.addLayout(self.layout_b1)
        self.master.addLayout(self.layout_a2)
        self.master.addLayout(self.layout_b2)
        self.master.addLayout(self.layout_a1)
        # self.master.addLayout(self.layout_b3)
        self.master.addWidget(self.tab02)
        
        
        central_widget = QWidget()
        central_widget.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(self.master)
        self.setCentralWidget(central_widget)
        self.setMinimumSize(200, 100)
        # self.resize(700, 500)
        self.setWindowTitle("文件查找工具 Made: Mr.Cheese QQ: 971346144")
        
        curnum = True
        if curnum:
            self.but_res_prosetfile_Run() # 刷新路径设定包列表
            self.load_sampleruler() # 刷新采样规则列表
            curnum = False
            
            
        # 应用样式表
        self.setStyleSheet("""
            QPushButton {
                background-color: #0e639c;
                color: white;
                padding: 8px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
            QLineEdit {
                font-size: 14px;
                padding: 6px;
                color: #d4d4d4;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                background-color: #252526;
            }
            QListWidget {
                color: #d4d4d4;
                font-size: 14px;
                background-color: #252526;
                border: 1px solid #3c3c3c;
            }
            QListWidget::item:selected {
                background-color: #094771;
            }
            QCheckBox {
                color: #d4d4d4;
                font-size: 14px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QComboBox {
                padding: 5px;
                color: #d4d4d4;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                background-color: #252526;
            }
            QComboBox:hover {
                border: 1px solid #0e639c;
            }
            QTabWidget::pane {
                font-size: 14px;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 5px;
                background-color: #1e1e1e;
            }
        """)
            

    
    
    ###----------------------------------------------------------------------------------------------------------------------------
    
    def CreatedFileExpo(self, pathsList):
        # 创建 tab页面
        num = 0
        for p in pathsList:
            if os.path.exists(p):
                if p.split("/")[-1] == "":
                    try:
                        qname = p.split("/")[-2]
                    except:
                        qname = str(p)
                else:
                    qname = p.split("/")[-1]

                self.Crtreeview = MyTreeWa()

                self.tab01.addTab(self.Crtreeview, qname)
                self.tab01.setTabToolTip(num, p)

                self.Crtreeview.set_line_edit_text("%s"%p)
                num += 1
                print("打开路径 ： %s " % p)
            else:
                print("路径不存在 ： %s " %p)
    
    
    def refresh_searchPath(self):
        # 生成路径的文件资源管理器
        # 获取p e s
        pnameget = self.qed_pro.text()
        enameget = self.qed_seq.text()
        snameget = self.qed_sht.text()

        searchPathGot = self.getChoose(self.searchFile)
        PathGot = []
        for i in searchPathGot:
            if i[0] == True:
                gv = i[1]
                PathGot.append(gv)
        SePathGot = []
        if PathGot != []:
            for i in PathGot:
                pgot = i.replace("{P}", "%s" % pnameget).replace("{E}", "%s" % enameget).replace("{S}", "%s" % snameget)
                if not pgot.endswith("/"):
                    pgot = pgot + "/"
                if pgot not in SePathGot:
                    SePathGot.append(pgot)
        sorted(SePathGot)
        
        # 设置不同系统的路径转换
        SePathGot = self.xitongchange(SePathGot)


        self.delAllShowpage(self.tab01)
        self.CreatedFileExpo(SePathGot)
        self.tab02.setCurrentIndex(0)
    
    # 路径转换设定
    def xitongchange(self,getlist=[]):
        if getlist != []:
            if sys.platform.startswith('win'):
                # Windows 系统
                return getlist

            elif sys.platform.startswith('darwin'):
                # macOS 系统
                print("macOS")
                return getlist
                    
            elif sys.platform.startswith('linux'):
                # Linux 系统
                newlist = []
                for i in getlist:
                    pass
                    
            else:
                # 其他系统
                print("other??")
                return getlist
    
    
    def delAllShowpage(self, kb=None):
        for i in range(kb.count() - 1, -1, -1):
            kb.removeTab(i)
    
    ###----------------------------------------------------------------------------------------------------------------------------
    def getPES_Read(self):
        thiskb = self.sender()
        if thiskb == self.btrefresh3:
            thb = "SCRIPT"
        else:
            thb = "READ"

        if thb == "READ":
            try:
                nds = nuke.selectedNodes("Read")
                getf = nds[0]["file"].value()#getEvaluatedValue()

            except:
                getf = None
        else:
            try:
                getf = nuke.scriptName()
            except:
                getf = None
        

        typef = self.sampleinfo.currentText()

        
        self.qed_pro.setText("")
        self.qed_seq.setText("")
        self.qed_sht.setText("")
        # if "*" in typef and getf != None:
        rtv,rtvlist = cps.Liuxiaobo_Split(typef,getf)

        lasb = [self.qed_pro, self.qed_seq, self.qed_sht]
        
        curinx = len(lasb)
        
        result_list = rtvlist[:curinx] if len(rtvlist) >= curinx else rtvlist + [''] * (curinx - len(rtvlist))
        
        for k, v in zip(result_list, lasb):
            v.setText(k)
                
            

        # else:
            
    
    ###----------------------------------------------------------------------------------------------------------------------------
    # 保存预设组
    def but_add_pathtype_Run(self):
        kb = self.searchFile
        gets = [i for i in self.getChoose(kb) if i[0]]
        # print(gets)
        
        curse = self.prosetfile.currentText()
        if os.path.exists(curse):
            curtext = self.pathtype.currentText()
            changedtype, messagetext = self.input_dialog_fun(gtin=curtext)
            if changedtype:
                curkey = messagetext
                ptsdictgv = self.ReadJson(curse) 
                ptsdictgv[curkey] = gets
                self.WriteJson(curse,ptsdictgv)
                print("预设保存成功\n%s"%curkey)
                self.reload_pathtypeset(curkey)
                
        else:
            print("无效的路径设定路径地址\n%s"%curse)
    
    # 删除预设组
    def but_del_pathtype_Run(self):
        curse = self.prosetfile.currentText()
        if os.path.exists(curse):
            curtext = self.pathtype.currentText()
            message_box = QMessageBox.question(self, '提示：', '删除预设？ ：\n%s'%curtext, QMessageBox.Ok | QMessageBox.Cancel)
            if message_box == QMessageBox.Ok:
                ptsdictgv = self.ReadJson(curse) 
                keysgv = [k for k in ptsdictgv.keys()]
                if curtext in keysgv:
                    ptsdictgv.pop(curtext)
                    self.WriteJson(curse, ptsdictgv)
                    
                    self.reload_pathtypeset()
                    self.reload_curpathset()
                    
                    print("预设删除成功\n%s"%curtext)
                
        else:
            print("无效的路径设定路径地址\n%s"%curse)
    
    def savesampleruler(self):
        rrget = self.sampleptset()
        kb = self.sampleinfo
        curr = kb.currentText()
        dt = self.ReadJson(rrget)
        getlist = dt["RR"]
        if curr not in getlist:
            getlist.append(curr)
        dt["RR"] = getlist
        self.WriteJson(rrget,dt)
        self.load_sampleruler(curr)
    
    def delsampleruler(self):
        rrget = self.sampleptset()
        kb = self.sampleinfo
        curr = kb.currentText()
        dt = self.ReadJson(rrget)
        getlist = dt["RR"]
        if curr in getlist:
            message_box = QMessageBox.question(self, '提示:', '删除规则？\n%s'%curr, QMessageBox.Ok | QMessageBox.Cancel)
            if message_box == QMessageBox.Ok:
                getlist.remove(curr)
                dt["RR"] = getlist
                self.WriteJson(rrget,dt)
                self.load_sampleruler()
        
    
    def load_sampleruler(self,curtext=None):
        rrget = self.sampleptset()
        kb = self.sampleinfo
        dt = self.ReadJson(rrget)
        glist = dt["RR"]
        kb.clear()
        kb.addItems(glist)
        if curtext:
            kb.setCurrentText(curtext)
        
        
        
        
    
    ###----------------------------------------------------------------------------------------------------------------------------
    
    def but_add_prosetfile_Run(self):
        curpt = self.CurrentFilePath()
        fgetv = [i.replace("\\","/") for i in glob.glob("%s*.json"%curpt)]
        
        # 第三个参数表示显示类型，可选，有正常（QLineEdit.Normal）、密碼（ QLineEdit. Password）、不显示（ QLineEdit. NoEcho）三种情况
        value, ok = QInputDialog.getText(self, "添加新的路径包", "输入路径包名:", QLineEdit.Normal, "")
        if ok:
            newjs = curpt + value + ".json"
            if newjs not in fgetv:
                self.WriteJson(newjs,dict_data={})
                print("创建成功\n%s"%newjs)
        else:
            print("取消创建")
    
    def but_res_prosetfile_Run(self):
        curpt = self.CurrentFilePath()
        fgetv = [i.replace("\\","/") for i in glob.glob("%s*.json"%curpt)]
        self.prosetfile.clear()
        self.prosetfile.addItems(fgetv)
    
    def but_del_prosetfile_Run(self):
        curse = self.prosetfile.currentText()
        if os.path.exists(curse):
            message_box = QMessageBox.question(self, '提示:', '删除设定包\n%s'%curse, QMessageBox.Ok | QMessageBox.Cancel)
            if message_box == QMessageBox.Ok:
                os.remove(curse)
                print("删除 \n%s\n成功"%curse)

    
    def but_sav_prosetfile_Run(self,delcu=None):     
        curse = self.prosetfile.currentText()
        if os.path.exists(curse):
            ptsdictgv = self.ReadJson(curse) 
            if self.pathsset in list(ptsdictgv.keys()):
                curpts = ptsdictgv[self.pathsset]
            else:
                curpts = []
            ptlist = [[False,"%s"%(i[-1])] for i in self.getChoose(self.searchFile)]
            for i in ptlist:
                if i not in curpts:
                   curpts.append(i)
            ptsdictgv[self.pathsset] = curpts
            # print(ptsdictgv)
            
            if delcu:
                curdel = delcu[-1]
                for k,v in ptsdictgv.items():
                    for i in v:
                        if curdel in i:
                            v.remove(i)
                    ptsdictgv[k] = v
                
                for k in list(ptsdictgv.keys()):
                    v = ptsdictgv[k]
                    if v == []:
                        del ptsdictgv[k]

                    
            
            self.WriteJson(curse,ptsdictgv)
            print("保存路径到包\n%s"%curse)
        else:
            print("无效的路径设定包地址\n%s"%curse)
            
    
    
    
    def reload_curpathset(self):
        curse = self.prosetfile.currentText()
        curtp = self.pathtype.currentText()
        curpts = []
        if os.path.exists(curse):
            try:
                ptsdictgv = self.ReadJson(curse) 
                if curtp in list(ptsdictgv.keys()):
                    curpts = [i[-1] for i in ptsdictgv[curtp]]
                else:
                    curpts = []
            except:
                curpts = []
        if curpts != []:
            # 假设 kb 是 QListWidget 对象
            # 遍历 kb 中的所有项
            kb = self.searchFile
            for i in range(kb.count()):
                # 获取当前项
                item = kb.item(i)
                # 获取当前项关联的部件（QCheckBox）
                checkbox_widget = kb.itemWidget(item)
                # 确保 checkbox_widget 是 QCheckBox 对象
                if isinstance(checkbox_widget, QCheckBox):
                    # 获取复选框的文本内容
                    checkbox_text = checkbox_widget.text()
                    # 如果找到合适的文本，设置复选框的状态为 True
                    if checkbox_text in curpts:
                        checkbox_widget.setChecked(True)
                    else:
                        checkbox_widget.setChecked(False)

    
    def reload_pathsset(self):
        # 更新路径集合的内容
        # self.searchFile.clear()
        curse = self.prosetfile.currentText()
        if os.path.exists(curse):
            try:
                ptsdictgv = self.ReadJson(curse) 
                if self.pathsset in list(ptsdictgv.keys()):
                    curpts = ptsdictgv[self.pathsset]
                else:
                    curpts = []
            except:
                curpts = []
        
            self.insert(curpts, self.searchFile)
    
    def reload_pathtypeset(self,curkey=None):
        # 更新路径预设组
        curse = self.prosetfile.currentText()
        if os.path.exists(curse):
            try:
                ptsdictgv = self.ReadJson(curse) 
                curpathtypes = []
                for i in list(ptsdictgv.keys()):
                    if i != self.pathsset and i not in curpathtypes:
                        curpathtypes.append(i)
                self.pathtype.clear()
                self.pathtype.addItems(curpathtypes)
                if curkey:
                    self.pathtype.setCurrentText(curkey)
                
            except:
                print("Error:0000001")
        
        
        
            
        
            
    #-------------------------------------------------------------------------------------------------------
    #### 采样数据的路径
    def sampleptset(self):
        cc = CurrentPath.local_path_get()
        cc = cc.replace(os.sep, "/")
        if not os.path.exists(cc):
            os.mkdir(cc)        
        jsfile = cc + "SearchPanelB_Ruler.json"
        # jsfile = "C:/Users/liuxb/.nuke/CheeseTools_7.0/Cheese_PanelTools/SearchPanelB_JSONPathSETING/SearchPanelB_SampleRuler.json"
        if not os.path.exists(jsfile):
            dvset = ["*/*-1*_*0,*/*-1*_*1,*/*-1*_*2","*/*-1*@*:3"]
            dt = {}
            dt["RR"] = dvset
            self.WriteJson(jsfile, dt)

        return jsfile

    #### 获取程序所在路径位置
    def CurrentFilePath(self):
        # return 一个当前程序所在路径的位置
        cc = CurrentPath.local_path_get() + "SearchPanelB_jsonfile/"
        # cc = "C:/Users/liuxb/.nuke/CheeseTools_7.0/Cheese_PanelTools/SearchPanelB_JSONPathSETING/"
        cc = cc.replace(os.sep, "/")
        if not os.path.exists(cc):
            os.mkdir(cc)
        cfp = cc
        return cfp

    #### 读取和写入json文件的方法
    def WriteJson(self, path=None, dict_data={}):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        Writedata = json.dumps(dict_data, ensure_ascii=False, sort_keys=True, indent=4)
        with open(path, "w", encoding='utf-8') as f:
            f.write(Writedata)

    def ReadJson(self, path=None):
        with open(path, 'r', encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
        return load_dict
    
    #-------------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------
    
    
    
    def myeditItem(self):
        kb = None
        if self.sender() == self.searchFile:
            kb = self.searchFile
        if kb != None:
            selected_items = kb.selectedItems()
            for item in selected_items:
                cb = kb.itemWidget(item)
                if cb.isChecked():
                    adp = [True, cb.text()]
                else:
                    adp = [False, cb.text()]
                kbte = adp[-1]
                self.editkb(kb, kbte, adp)
    
    def menu_scr(self):
        self.a_prepMenu = QMenu()
        if self.sender() == self.searchFile:
            self.a_prepMenu.addAction(QAction(u'添加查找路径', self.searchFile))
            self.a_prepMenu.addAction(QAction(u'删除查找路径', self.searchFile))
        self.a_prepMenu.triggered[QAction].connect(self.scr_fun)  # 右键点击 运行
        self.a_prepMenu.exec_(QCursor.pos())
    
    def scr_fun(self, p):
        cmmd = p.text()  # 单击按钮的功能
        if cmmd == u'添加查找路径':
            self.addkb(self.searchFile)

        if cmmd == u'删除查找路径':
            self.delselitem(self.searchFile)
    
    def addkb(self, kb):
        changedtype, messagetext = self.input_dialog_fun()
        messagetext = messagetext.replace(os.sep, "/")
        if changedtype:
            chooses = self.getChoose(kb)
            gt = [i[-1] for i in chooses]
            if messagetext not in gt:
                adp = [False, "%s" % messagetext]
                chooses.append(adp)
                self.insert(chooses, kb)
                self.but_sav_prosetfile_Run()

    def delselitem(self, kb=None):
        if kb != None:
            selected_items = kb.selectedItems()
            for item in selected_items:
                cb = kb.itemWidget(item)
                if cb.isChecked():
                    adp = [True, cb.text()]
                else:
                    adp = [False, cb.text()]
                chooses = self.getChoose(kb)
                if adp in chooses:
                    message_box = QMessageBox.question(self, '提示:', '删除路径？\n%s'%adp, QMessageBox.Ok | QMessageBox.Cancel)
                    if message_box == QMessageBox.Ok:
                        chooses.remove(adp)
                        # print("RRRRRRRRRRR %s"%chooses)
                        self.but_sav_prosetfile_Run(delcu=adp)
                self.insert(chooses, kb)
    
    def editkb(self, kb, kbte, oldt):
        changedtype, messagetext = self.input_dialog_fun(kbte)
        if changedtype:
            chooses = self.getChoose(kb)
            gt = [i[-1] for i in chooses]
            if messagetext == "":
                chooses.remove(oldt)
                self.insert(chooses, kb)

            elif messagetext not in gt:
                idx = chooses.index(oldt)
                chooses.remove(oldt)
                oldt[-1] = messagetext
                neld = oldt
                chooses.insert(idx, neld)
                self.insert(chooses, kb)
    
    def getChoose(self, kb="") -> [str]:
        chooses = []
        if kb != "":
            count = kb.count()  # 得到QListWidget的总个数
            cb_list = [kb.itemWidget(kb.item(i)) for i in range(count)]  # 得到QListWidget里面所有QListWidgetItem中的QCheckBox
            for cb in cb_list:  # type:QCheckBox
                if cb.isChecked():
                    adp = [True, cb.text()]
                else:
                    adp = [False, cb.text()]
                chooses.append(adp)
        return chooses

    def insert(self, data_list=[], kb=""):
        if data_list != [] and kb != "":
            kb.clear()
            for i in range(0, len(data_list)):
                box = QCheckBox(data_list[i][-1])  # 实例化一个QCheckBox，吧文字传进去
                box.setChecked(data_list[i][0])
                item = QListWidgetItem()  # 实例化一个Item，QListWidget，不能直接加入QCheckBox
                kb.addItem(item)  # 把QListWidgetItem加入QListWidget
                kb.setItemWidget(item, box)  # 再把QCheckBox加入QListWidgetItem
        elif data_list == []:
            kb.clear()
                
    
    def close_tab(self,index):
        widget = self.tab01.widget(index)
        self.tab01.removeTab(index)
        widget.deleteLater()
    
    # 一个通用的编辑输入框
    def input_dialog_fun(self, gtin=""):
        input_dialog = QInputDialog(self)
        input_dialog.setInputMode(QInputDialog.TextInput)
        input_dialog.setWindowTitle("编辑内容")
        input_dialog.setLabelText("输入：")
        messagetext = "%s" % gtin
        changedtype = False
        input_dialog.setTextValue(messagetext)
        # input_dialog.textValueChanged.connect('输入框 发生变化时 响应')
        input_dialog.setFixedSize(500, 300)
        input_dialog.show()
        if input_dialog.exec_() == input_dialog.Accepted:
            messagetext = input_dialog.textValue()
            # if "%s" % gtin != "%s" % messagetext:
            # changedtype = True
            changedtype = True
        return changedtype, messagetext
        
        

nukepgetsear = nukescripts.panels.registerWidgetAsPanel("SearchPanelB.getfileToolspaceal","查找文件工具","QZDFlixuaiobo.SearchPanelB.getfileToolspaceal_ver30",True)

def run_show_funa():
    pane = nuke.getPaneFor("Properties.1")
    nukepgetsear.addToPane(pane)




def _nuke_main_window():  # 找到nuke的主面板，把当前面板设置成它的子面板，这会让这个子面板置顶
    """Returns Nuke's main window"""
    for obj in QApplication.topLevelWidgets():
        if (obj.inherits('QMainWindow') and
                obj.metaObject().className() == 'Foundry::UI::DockMainWindow'):
                return obj
    else:
        raise RuntimeError('Could not find DockMainWindow instance')

def runshow():
    global wgetb
    # wgetb = getfileToolspaceal(parent=None)
    wgetb = getfileToolspaceal(parent=_nuke_main_window())
    wgetb.show()
