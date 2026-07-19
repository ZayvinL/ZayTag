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

"""向后兼容包装 — 实际逻辑已拆分到 tree_widgets.py 和 search_panel.py。"""
from ZayWPanel import (
    getfileToolspaceal,
    run_show_funa,
    runshow,
    _nuke_main_window,
    MyDialog,
)
from tree_widgets import TreeView, FolderMarkDelegate, MyTreeWa, FileCopyWorker
