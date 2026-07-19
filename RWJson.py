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
import nuke
import nukescripts


if nuke.NUKE_VERSION_MAJOR < 13:
    stdi,stdo,stde=sys.stdin,sys.stdout,sys.stderr 
    reload(sys)    
    sys.stdin,sys.stdout,sys.stderr=stdi,stdo,stde 
    sys.setdefaultencoding('utf-8')



def WriteJson(path=None, dict_data={}):
    # Json write
    if nuke.NUKE_VERSION_MAJOR < 13:
        data = json.dumps(dict_data, ensure_ascii=False, sort_keys=False, indent=4)
        with open(path, "w") as f:
            f.write(data)
    else:
        Writedata = json.dumps(dict_data, ensure_ascii=False, sort_keys=True, indent=4)
        with open(path, "w", encoding='utf-8') as f:
            f.write(Writedata)
    # 保证所有用户可读写
    try:
        os.chmod(path, 0o666)
    except Exception:
        pass

def ReadJson(path=None):
    # Json Read
    if nuke.NUKE_VERSION_MAJOR < 13:
        if os.path.exists(path):
            with open(path, 'r') as load_f:
                load_dict_lll = json.load(load_f, encoding='utf-8')
        return load_dict_lll
    else:
        with open(path, 'r', encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
        return load_dict    