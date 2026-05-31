# -*- coding: UTF-8 -*-
import os
import json
import sys


# 本地路径
def local_path_get():
    # 默认地址放插件路径 - 示意图地址需要特定指定
    currentPath = os.path.dirname(os.path.abspath(__file__)) + "/"
    currentPath = currentPath.replace(os.sep,"/")
    
    # 集中管理地址 ---------------------------------------------------------------------------

    # if sys.platform.startswith('win'):
         ###Windows 系统
        # currentPath = "C:/Users/liuxb/.nuke/CheeseTools_7.0/Cheese_PanelTools/TESTFiles/"

    # elif sys.platform.startswith('darwin'):
         ###macOS 系统
        # print("macOS")
        # currentPath = "C:/Users/liuxb/.nuke/CheeseTools_7.0/Cheese_PanelTools/TESTFiles/"
            
    # elif sys.platform.startswith('linux'):
         ###Linux 系统
        # currentPath = "C:/Users/liuxb/.nuke/CheeseTools_7.0/Cheese_PanelTools/TESTFiles/"
            
    # else:
        ###其他系统
        # print("other??")
        # currentPath = "C:/Users/liuxb/.nuke/CheeseTools_7.0/Cheese_PanelTools/TESTFiles/"
    
    # print("aaaaaaaaaaaaaaaaaaaaaaaaaaa")
    # print(currentPath)
    #  ---------------------------------------------------------------------------
    
    return currentPath

def icon_get():
    currentPath = local_path_get()
    icon = currentPath + 'icons/AltWicon.png'
    return icon