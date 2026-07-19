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

from _qt import (
    QAbstractItemView,
    QAction,
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
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
    QTabWidget,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
    QDir,
    Qt,
    QUrl,
    QCursor,
    QFont,
    QKeySequence,
    QT_VERSION,
)
import os
import sys
import json
import shutil
import glob
import nuke
import nukescripts
import CurrentPath
import RWJson
import ZaySplit as cps
from tree_widgets import TreeView, FolderMarkDelegate, MyTreeWa, FileCopyWorker, noteword

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
        
        self.qed_values = QLineEdit()
        self.qed_values.setPlaceholderText("采样值, 以逗号间隔, 路径中用 {0}{1}{2}... 引用")
        
        label_sampleinfo = QLabel("采样规则 ：")
        label_sampleinfo.setToolTip(noteword)
        
        self.sampleinfo = QComboBox() # 信息采样的设定规则，
        self.sampleinfo.setEditable(True)
        self.sampleinfo.setObjectName("sampleRuleCombo")
        self.sampleinfo.setPlaceholderText("输入或选择采样规则...")
        self.sampleinfo.setToolTip(noteword)
        self.sampleinfo.currentIndexChanged.connect(self._save_session)
        self.btrefresh2 = QPushButton("从Read获取 (Alt+1)")
        self.btrefresh2.setShortcut("Alt+1")
        self.btrefresh2.setToolTip("从选中 Read 节点提取路径层级信息\nExtract path tokens from selected Read node")
        self.btrefresh2.clicked.connect(self.getPES_Read)

        self.btrefresh3 = QPushButton("从工程获取 (Alt+2)")
        self.btrefresh3.setShortcut("Alt+2")
        self.btrefresh3.setToolTip("从当前 Nuke 工程路径提取层级信息\nExtract path tokens from current script path")
        self.btrefresh3.clicked.connect(self.getPES_Read)
        
        self.btrefresh4 = QPushButton("保存采样规则")
        self.btrefresh4.setToolTip("CN: 保存当前采样规则到预设列表\nEN: Save current sample rule to presets")
        self.btrefresh4.clicked.connect(self.savesampleruler)

        self.btrefresh5 = QPushButton("删除采样规则")
        self.btrefresh5.setToolTip("CN: 从预设列表删除当前采样规则\nEN: Delete current sample rule from presets")
        self.btrefresh5.clicked.connect(self.delsampleruler)
        
        self.layout_a1 = QHBoxLayout()
        self.layout_a2 = QHBoxLayout()
        
        # self.layout_a1.setMargin(0)
        
        self.layout_a1.addWidget(self.qed_values, 1)
        
        self.layout_a2.addWidget(label_sampleinfo, 0.1)
        self.layout_a2.addWidget(self.sampleinfo, 1)
        self.layout_a2.addWidget(self.btrefresh2, 0.6)
        self.layout_a2.addWidget(self.btrefresh3, 0.6)
        
        
        self.layout_b1 = QHBoxLayout()
        # self.layout_b1.setMargin(0)
        # self.layout_b3 = QHBoxLayout()
        # self.layout_b3.setMargin(0)
        label_pathsset = QLabel("路径设定包 ：")
        # 每个项目自定义一套路径包，叫项目路径设定包也行
        self.prosetfile = QComboBox()  # 预设的路径包，每个项目可以不一样，包含不同的路径预设，
        self.prosetfile.currentIndexChanged.connect(self.reload_pathsset) # 刷新路径集合
        self.prosetfile.currentIndexChanged.connect(self.reload_pathtypeset) # 刷新 路径预设组
        self.prosetfile.currentIndexChanged.connect(self.reload_curpathset) # 刷新路径预设组选项
        self.prosetfile.currentIndexChanged.connect(self._save_session)
        self.but_add_prosetfile = QPushButton("添加新包")
        self.but_add_prosetfile.setToolTip("CN: 添加新的路径设定包\nEN: Add new path pack")
        self.but_add_prosetfile.clicked.connect(self.but_add_prosetfile_Run)
        self.but_del_prosetfile = QPushButton("删除包")
        self.but_del_prosetfile.setToolTip("CN: 删除当前路径设定包\nEN: Delete current path pack")
        self.but_del_prosetfile.clicked.connect(self.but_del_prosetfile_Run)

        self.layout_b1.addWidget(label_pathsset, 0.1)
        self.layout_b1.addWidget(self.prosetfile, 1)
        self.layout_b1.addWidget(self.but_add_prosetfile, 0.3)
        self.layout_b1.addWidget(self.but_del_prosetfile, 0.3)
        self.layout_b1.addWidget(self.btrefresh4, 0.3)
        self.layout_b1.addWidget(self.btrefresh5, 0.3)
        
        label_pathstool = QLabel("路径预设组 ：")
        self.pathtype = QListWidget()
        self.pathtype.itemClicked.connect(self._on_preset_clicked)
        self.pathtype.itemClicked.connect(self._save_session)
        self.but_add_pathtype = QPushButton("保存设定")
        self.but_add_pathtype.setToolTip("CN: 保存当前勾选路径为预设组\nEN: Save checked paths as preset")
        self.but_add_pathtype.clicked.connect(self.but_add_pathtype_Run)
        self.but_del_pathtype = QPushButton("删除设定")
        self.but_del_pathtype.setToolTip("CN: 删除当前路径预设组\nEN: Delete current preset")
        self.but_del_pathtype.clicked.connect(self.but_del_pathtype_Run)

        self.layout_preset = QVBoxLayout()
        self.layout_preset.addWidget(label_pathstool)
        self.layout_preset.addWidget(self.pathtype)

        ############################///////////////////////////////////////////////////////////////////////////////

        self.tab01 = QTabWidget()
        self.tab02 = QTabWidget()
        self.tab01.setTabsClosable(True)

        tab_bar = self.tab01.tabBar()
        tab_bar.tabCloseRequested.connect(self.close_tab)

        self.wida = QWidget()
        self.widb = QWidget()
        self.widc = QWidget()
        self.wida.setContentsMargins(0, 0, 0, 0)
        self.widb.setContentsMargins(0, 0, 0, 0)
        self.widc.setContentsMargins(0, 0, 0, 0)
        self.tab02.addTab(self.widb, "文件管理")
        self.tab02.addTab(self.wida, "路径集合")

        help_text = QTextBrowser()
        help_text.setOpenExternalLinks(True)

        # 直接读取 README.md 作为帮助内容
        script_dir = CurrentPath.local_path_get()
        readme_path = os.path.join(script_dir, "README.md")
        if os.path.exists(readme_path):
            with open(readme_path, "r", encoding="utf-8") as f:
                md_content = f.read()
            # 尝试多种方式渲染 Markdown
            try:
                # 优先使用 Python markdown 库
                import markdown
                html_content = markdown.markdown(md_content, extensions=["tables", "fenced_code"])
                help_text.setHtml(html_content)
            except ImportError:
                try:
                    # PySide6 / Qt 5.14+ 内置 Markdown 支持
                    help_text.setMarkdown(md_content)
                except AttributeError:
                    # 兜底：纯文本显示
                    help_text.setPlainText(md_content)
        else:
            help_text.setPlainText("README.md 未找到，请确认文件存在。")
        help_layout = QVBoxLayout(self.widc)
        help_layout.addWidget(help_text)
        self.tab02.addTab(self.widc, "帮助")

        # 左侧预设面板容器
        preset_widget = QWidget()
        preset_widget.setLayout(self.layout_preset)

        self.splitter = QSplitter()
        self.splitter.addWidget(preset_widget)
        self.splitter.addWidget(self.tab02)
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setSizes([220, 600])
        
        
        
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

        self.layout_pathtype_btns = QHBoxLayout()
        self.layout_pathtype_btns.addWidget(self.but_add_pathtype)
        self.layout_pathtype_btns.addWidget(self.but_del_pathtype)
        self.layout_a.addLayout(self.layout_pathtype_btns)

        self.wida.setLayout(self.layout_a)
        
        self.layout_c.addWidget(self.tab01)
        self.widb.setLayout(self.layout_c)
        
        
        ############################///////////////////////////////////////////////////////////////////////////////
        
        
        
        
        
        
        
        
        
        
        self.master = QVBoxLayout()
        # self.master.setMargin(0)
        
        self.master.addLayout(self.layout_b1)
        self.master.addLayout(self.layout_a2)
        self.master.addLayout(self.layout_a1)
        self.master.addWidget(self.splitter, 1)
        
        
        central_widget = QWidget()
        central_widget.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(self.master)
        self.setCentralWidget(central_widget)
        self.setMinimumSize(200, 100)
        # self.resize(700, 500)
        self.setWindowTitle("ZayTag 路径标签系统")
        
        self.prosetfile.blockSignals(True)
        self.but_res_prosetfile_Run()
        self.prosetfile.blockSignals(False)

        self.sampleinfo.blockSignals(True)
        self.load_sampleruler()
        self.sampleinfo.blockSignals(False)

        self._load_session()
            
            
        # 应用样式表
        self.setStyleSheet("""
            QPushButton {
                background-color: #a0682a;
                color: #f0e0d0;
                padding: 4px 10px;
                border: 1px solid #6b4520;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #c08038;
            }
            QPushButton:pressed {
                background-color: #7a4e1e;
            }
            QLineEdit {
                font-size: 14px;
                padding: 4px 6px;
                color: #d4d4d4;
                border: 1px solid #3c3c3c;
                border-radius: 3px;
                background-color: #252526;
            }
            QListWidget {
                color: #d4d4d4;
                font-size: 14px;
                background-color: #252526;
                border: 1px solid #3c3c3c;
                outline: none;
            }
            QListWidget::item:selected {
                background-color: #8b5e28;
                color: #f0ddb0;
            }
            QListWidget::item:hover {
                background-color: #3d3420;
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
                padding: 3px 6px;
                color: #d4d4d4;
                border: 1px solid #3c3c3c;
                border-radius: 3px;
                background-color: #252526;
            }
            QComboBox:hover {
                border: 1px solid #a0682a;
            }
            QComboBox::drop-down {
                border: none;
                background: transparent;
            }
            QComboBox::down-arrow {
                width: 14px;
                height: 14px;
            }
            QComboBox#sampleRuleCombo {
                padding: 3px 28px 3px 6px;
            }
            QComboBox#sampleRuleCombo QLineEdit {
                background-color: #252526;
                color: #d4d4d4;
                border: none;
                padding: 0px;
            }
            QComboBox#sampleRuleCombo::drop-down {
                background-color: #a0682a;
                border-left: 1px solid #6b4520;
                border-top-right-radius: 2px;
                border-bottom-right-radius: 2px;
                width: 24px;
            }
            QComboBox#sampleRuleCombo:focus::drop-down {
                background-color: #c08038;
            }
            QComboBox#sampleRuleCombo::drop-down:hover {
                background-color: #c08038;
            }
            QComboBox#sampleRuleCombo::down-arrow {
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #8b5e28;
                color: #f0ddb0;
            }
            QTabWidget::pane {
                font-size: 14px;
                border: none;
                padding: 0px;
                background-color: #1e1e1e;
            }
            QTabBar::tab {
                padding: 4px 12px;
                color: #b0b0b0;
                background: #2d2d2d;
                border: 1px solid #3c3c3c;
                border-bottom: none;
                border-top-left-radius: 3px;
                border-top-right-radius: 3px;
            }
            QTabBar::tab:selected {
                color: #f0d890;
                background: #1e1e1e;
            }
            QSplitter::handle {
                background-color: #3c3c3c;
                width: 1px;
            }
            QTreeView {
                color: #d4d4d4;
                font-size: 13px;
                background-color: #1e1e1e;
                border: none;
                outline: none;
            }
            QTreeView::item:selected {
                background-color: #8b5e28;
                color: #f0ddb0;
            }
            QTreeView::item:hover {
                background-color: #3d3420;
            }
            QHeaderView::section {
                background-color: #2d2d2d;
                color: #b0b0b0;
                padding: 2px 6px;
                border: 1px solid #3c3c3c;
                font-size: 13px;
            }
            QTextBrowser {
                color: #d4d4d4;
                font-size: 14px;
                background-color: #1e1e1e;
                border: none;
                padding: 10px;
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
    
    
    def _on_preset_clicked(self, item):
        self.reload_curpathset()
        self.refresh_searchPath()

    def refresh_searchPath(self):
        vals = self.qed_values.text().split(",")

        searchPathGot = self.getChoose(self.searchFile)
        PathGot = []
        for i in searchPathGot:
            if i[0]:
                PathGot.append(i[1])
        SePathGot = []
        if PathGot:
            for i in PathGot:
                pgot = i
                for idx, v in enumerate(vals):
                    pgot = pgot.replace("{%d}" % idx, v.strip())
                if not pgot.endswith("/"):
                    pgot = pgot + "/"
                if pgot not in SePathGot:
                    SePathGot.append(pgot)
        sorted(SePathGot)
        
        # 设置不同系统的路径转换
        SePathGot = self.xitongchange(SePathGot)


        self.delAllShowpage(self.tab01)
        self.CreatedFileExpo(SePathGot)
    
    # 路径转换设定
    def xitongchange(self, getlist=None):
        if getlist is None:
            getlist = []
        if not getlist:
            return getlist

        curse = self._cur_prosetfile_path()
        if not curse or not os.path.exists(curse):
            return getlist

        try:
            data = RWJson.ReadJson(curse)
            sysmap = data.get("_systemMap", {})
        except Exception:
            return getlist

        if not sysmap:
            return getlist

        # 确定当前平台对应的转换规则 key
        if sys.platform.startswith('win'):
            rule_key = "linux_to_win"
        elif sys.platform.startswith('linux'):
            rule_key = "win_to_linux"
        elif sys.platform.startswith('darwin'):
            rule_key = "win_to_mac"
        else:
            return getlist

        rules = sysmap.get(rule_key, [])
        if not rules:
            return getlist

        newlist = []
        for path in getlist:
            converted = path
            for src, dst in rules:
                if path.startswith(src):
                    converted = dst + path[len(src):]
                    break
            newlist.append(converted)

        return newlist
    
    
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
        

        if not getf:
            if thb == "READ":
                QMessageBox.warning(self, "提示", "请先选中一个 Read 节点")
            else:
                QMessageBox.warning(self, "提示", "请先保存工程文件")
            return

        typef = self.sampleinfo.currentText()


        self.qed_values.setText("")
        rtv, rtvlist = cps.Liuxiaobo_Split(typef, getf)
        if rtvlist:
            self.qed_values.setText(",".join(rtvlist))
                
            

        # else:
            
    
    ###----------------------------------------------------------------------------------------------------------------------------
    # 保存预设组
    def but_add_pathtype_Run(self):
        kb = self.searchFile
        gets = [i for i in self.getChoose(kb) if i[0]]

        curse = self._cur_prosetfile_path()
        if os.path.exists(curse):
            item = self.pathtype.currentItem()
            curtext = item.text() if item else ""
            changedtype, messagetext = self.input_dialog_fun(gtin=curtext)
            if changedtype:
                curkey = messagetext
                ptsdictgv = RWJson.ReadJson(curse) 
                ptsdictgv[curkey] = gets
                RWJson.WriteJson(curse,ptsdictgv)
                print("预设保存成功\n%s"%curkey)
                self.reload_pathtypeset(curkey)
                
        else:
            print("无效的路径设定路径地址\n%s"%curse)
    
    # 删除预设组
    def but_del_pathtype_Run(self):
        curse = self._cur_prosetfile_path()
        item = self.pathtype.currentItem()
        if not item:
            return
        curtext = item.text()
        if os.path.exists(curse):
            message_box = QMessageBox.question(self, '提示：', '删除预设？ ：\n%s' % curtext, QMessageBox.Ok | QMessageBox.Cancel)
            if message_box == QMessageBox.Ok:
                ptsdictgv = RWJson.ReadJson(curse) 
                keysgv = [k for k in ptsdictgv.keys()]
                if curtext in keysgv:
                    ptsdictgv.pop(curtext)
                    RWJson.WriteJson(curse, ptsdictgv)
                    
                    self.reload_pathtypeset()
                    self.reload_curpathset()
                    
                    print("预设删除成功\n%s"%curtext)
                
        else:
            print("无效的路径设定路径地址\n%s"%curse)
    
    def savesampleruler(self):
        rrget = self.sampleptset()
        kb = self.sampleinfo
        curr = kb.currentText()
        dt = RWJson.ReadJson(rrget)
        getlist = dt["RR"]
        if curr not in getlist:
            getlist.append(curr)
        dt["RR"] = getlist
        RWJson.WriteJson(rrget,dt)
        self.load_sampleruler(curr)
    
    def delsampleruler(self):
        rrget = self.sampleptset()
        kb = self.sampleinfo
        curr = kb.currentText()
        dt = RWJson.ReadJson(rrget)
        getlist = dt["RR"]
        if curr in getlist:
            message_box = QMessageBox.question(self, '提示:', '删除规则？\n%s'%curr, QMessageBox.Ok | QMessageBox.Cancel)
            if message_box == QMessageBox.Ok:
                getlist.remove(curr)
                dt["RR"] = getlist
                RWJson.WriteJson(rrget,dt)
                self.load_sampleruler()
        
    
    def load_sampleruler(self,curtext=None):
        rrget = self.sampleptset()
        kb = self.sampleinfo
        dt = RWJson.ReadJson(rrget)
        glist = dt["RR"]
        kb.clear()
        kb.addItems(glist)
        if curtext:
            kb.setCurrentText(curtext)
        
        
        
        
    
    def _cur_prosetfile_path(self):
        """返回当前选中路径包 JSON 文件的完整路径。"""
        return self.prosetfile.currentData()

    ###----------------------------------------------------------------------------------------------------------------------------

    def but_add_prosetfile_Run(self):
        curpt = self.CurrentFilePath()
        fgetv = [i.replace("\\","/") for i in glob.glob("%s*.json"%curpt)]
        
        # 第三个参数表示显示类型，可选，有正常（QLineEdit.Normal）、密碼（ QLineEdit. Password）、不显示（ QLineEdit. NoEcho）三种情况
        value, ok = QInputDialog.getText(self, "添加新的路径包", "输入路径包名:", QLineEdit.Normal, "")
        if ok:
            newjs = curpt + value + ".json"
            if newjs not in fgetv:
                RWJson.WriteJson(newjs, dict_data={})
                self.but_res_prosetfile_Run()
                self.prosetfile.setCurrentText(value)
                print("创建成功 %s" % value)
        else:
            print("取消创建")
    
    def but_res_prosetfile_Run(self):
        curpt = self.CurrentFilePath()
        fgetv = [i.replace("\\", "/") for i in glob.glob("%s*.json" % curpt)]
        self.prosetfile.clear()
        for f in fgetv:
            name = os.path.splitext(os.path.basename(f))[0]
            self.prosetfile.addItem(name, f)
    
    def but_del_prosetfile_Run(self):
        curse = self._cur_prosetfile_path()
        if os.path.exists(curse):
            name = self.prosetfile.currentText()
            message_box = QMessageBox.question(self, '提示:', '删除设定包\n%s' % name, QMessageBox.Ok | QMessageBox.Cancel)
            if message_box == QMessageBox.Ok:
                os.remove(curse)
                self.but_res_prosetfile_Run()
                print("删除 %s 成功" % name)

    
    def _auto_save_paths(self,delcu=None):     
        curse = self._cur_prosetfile_path()
        if os.path.exists(curse):
            ptsdictgv = RWJson.ReadJson(curse) 
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

                    
            
            RWJson.WriteJson(curse,ptsdictgv)
            print("保存路径到包\n%s"%curse)
        else:
            print("无效的路径设定包地址\n%s"%curse)
            
    
    
    
    def reload_curpathset(self):
        curse = self._cur_prosetfile_path()
        if not curse:
            return
        item = self.pathtype.currentItem()
        if not item:
            return
        curtp = item.text()
        curpts = []
        if os.path.exists(curse):
            try:
                ptsdictgv = RWJson.ReadJson(curse) 
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
                    checkbox_text = checkbox_widget.text()
                    checkbox_widget.blockSignals(True)
                    checkbox_widget.setChecked(checkbox_text in curpts)
                    checkbox_widget.blockSignals(False)

    
    def reload_pathsset(self):
        curse = self._cur_prosetfile_path()
        if not curse:
            return
        if os.path.exists(curse):
            try:
                ptsdictgv = RWJson.ReadJson(curse) 
                if self.pathsset in list(ptsdictgv.keys()):
                    curpts = ptsdictgv[self.pathsset]
                else:
                    curpts = []
            except:
                curpts = []
        
            self.insert(curpts, self.searchFile)
    
    def reload_pathtypeset(self, curkey=None):
        curse = self._cur_prosetfile_path()
        if not curse:
            return
        if os.path.exists(curse):
            try:
                ptsdictgv = RWJson.ReadJson(curse) 
                curpathtypes = []
                for i in list(ptsdictgv.keys()):
                    if i != self.pathsset and i not in curpathtypes:
                        curpathtypes.append(i)
                self.pathtype.clear()
                for name in curpathtypes:
                    self.pathtype.addItem(name)
                if curkey:
                    items = self.pathtype.findItems(curkey, Qt.MatchExactly)
                    if items:
                        self.pathtype.setCurrentItem(items[0])
                
            except:
                print("Error:0000001")
        
        
        
            
        
            
    #-------------------------------------------------------------------------------------------------------
    #### 采样数据的路径
    def sampleptset(self):
        cc = CurrentPath.local_path_get()
        cc = cc.replace(os.sep, "/")
        if not os.path.exists(cc):
            os.mkdir(cc)
            try:
                os.chmod(cc, 0o777)
            except Exception:
                pass
        jsfile = cc + "SampleRuler.json"
        # jsfile = "C:/Users/liuxb/.nuke/CheeseTools_7.0/Cheese_PanelTools/SearchPanelB_JSONPathSETING/SearchPanelB_SampleRuler.json"
        if not os.path.exists(jsfile):
            dvset = ["*/*-1*_*0,*/*-1*_*1,*/*-1*_*2","*/*-1*@*:3"]
            dt = {}
            dt["RR"] = dvset
            RWJson.WriteJson(jsfile, dt)

        return jsfile

    #### 获取程序所在路径位置
    def CurrentFilePath(self):
        # return 一个当前程序所在路径的位置
        cc = CurrentPath.local_path_get() + "PathPackSet/"
        # cc = "C:/Users/liuxb/.nuke/CheeseTools_7.0/Cheese_PanelTools/SearchPanelB_JSONPathSETING/"
        cc = cc.replace(os.sep, "/")
        if not os.path.exists(cc):
            os.mkdir(cc)
            try:
                os.chmod(cc, 0o777)
            except Exception:
                pass
        cfp = cc
        return cfp

    #### 读写 json 委托给 RWJson 模块
    
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

    def myeditItem_menu(self):
        kb = self.searchFile
        selected_items = kb.selectedItems()
        if not selected_items:
            return
        item = selected_items[0]
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
            self.a_prepMenu.addAction(QAction(u'编辑选中路径', self.searchFile))
        self.a_prepMenu.triggered[QAction].connect(self.scr_fun)  # 右键点击 运行
        self.a_prepMenu.exec_(QCursor.pos())
    
    def scr_fun(self, p):
        cmmd = p.text()  # 单击按钮的功能
        if cmmd == u'添加查找路径':
            self.addkb(self.searchFile)

        if cmmd == u'删除查找路径':
            self.delselitem(self.searchFile)

        if cmmd == u'编辑选中路径':
            self.myeditItem_menu()
    
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
                self._auto_save_paths()

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
                        self._auto_save_paths(delcu=adp)
                self.insert(chooses, kb)
    
    def editkb(self, kb, kbte, oldt):
        changedtype, messagetext = self.input_dialog_fun(kbte)
        if changedtype:
            chooses = self.getChoose(kb)
            gt = [i[-1] for i in chooses]
            if messagetext == "":
                chooses.remove(oldt)
                self.insert(chooses, kb)
                self._auto_save_paths()

            elif messagetext not in gt:
                idx = chooses.index(oldt)
                chooses.remove(oldt)
                oldt[-1] = messagetext
                neld = oldt
                chooses.insert(idx, neld)
                self.insert(chooses, kb)
                self._auto_save_paths()
    
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
                box = QCheckBox(data_list[i][-1])
                box.setChecked(data_list[i][0])
                box.stateChanged.connect(lambda state, kb=kb: self._auto_save_paths())
                item = QListWidgetItem()
                kb.addItem(item)
                kb.setItemWidget(item, box)
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
        if input_dialog.exec_():
            messagetext = input_dialog.textValue()
            # if "%s" % gtin != "%s" % messagetext:
            # changedtype = True
            changedtype = True
        return changedtype, messagetext

    def _session_file(self):
        user_dir = os.path.expanduser("~/.nuke/ZayTag/")
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        return user_dir + "UserSession.json"

    def _save_session(self):
        try:
            cur_preset = self.pathtype.currentItem()
            session = {
                "last_path_pack": self.prosetfile.currentText(),
                "last_sample_rule": self.sampleinfo.currentText(),
                "last_preset_group": cur_preset.text() if cur_preset else "",
            }
            RWJson.WriteJson(self._session_file(), session)
        except Exception:
            pass

    def _load_session(self):
        try:
            sf = self._session_file()
            if not os.path.exists(sf):
                return
            session = RWJson.ReadJson(sf)
            pack_name = session.get("last_path_pack", "")
            if pack_name:
                idx = self.prosetfile.findText(pack_name)
                if idx >= 0:
                    # 先切到 -1 确保后续 setCurrentIndex 一定会触发 currentIndexChanged
                    self.prosetfile.blockSignals(True)
                    self.prosetfile.setCurrentIndex(-1)
                    self.prosetfile.blockSignals(False)
                    self.prosetfile.setCurrentIndex(idx)
            # 恢复路径预设组选择（必须在 prosetfile 设置之后，reload_pathtypeset 已在信号链中重填列表）
            preset_name = session.get("last_preset_group", "")
            if preset_name:
                items = self.pathtype.findItems(preset_name, Qt.MatchExactly)
                if items:
                    self.pathtype.setCurrentItem(items[0])
                    self.reload_curpathset()
            rule_text = session.get("last_sample_rule", "")
            if rule_text:
                idx = self.sampleinfo.findText(rule_text)
                if idx >= 0:
                    self.sampleinfo.setCurrentIndex(idx)
        except Exception:
            pass




nukepgetsear = nukescripts.panels.registerWidgetAsPanel("ZayTagPath.getfileToolspaceal","ZayTag 路径标签系统","QZDFlixuaiobo.ZayTagPath.getfileToolspaceal_ver30",True)

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
