# -*- coding: UTF-8 -*-
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