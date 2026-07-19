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

def Liuxiaobo_Split(mofa,stext,bsb="_"):
    """
    拆分字符串的功能函数
    以符号 * 隔开的一系列分隔方法：
    符号* 接 奇数的内容 是拆分的符号；偶数内容是 拆分之后的取用范围，逗号分隔拆分几个结果，bsb符号连接拆分的结果。
    当符号 ，隔开的内容里面没有符号 * ，则返回当前内容，不做任何拆分。
    
    举例子 a：
    # 拆分字符串
    stext = "E:/KaiFaTEST/chatGPT/testa/001/Render/chatGPT_testa_001_v002/chatGPT_testa_001_v002.%d.exr"
    # 拆分格式魔法设置：拆分三次，两个逗号分开，第一部分，以符号 / 拆分，取拆分之后第一个，其余取第二个和第三个
    mofa = "*/*1,*/*2,*/*3"   
    # 连接字符设置
    bsb = "  "
    # 返回结果
    return - >>    KaiFaTEST  chatGPT  testa [KaiFaTEST,chatGPT,testa]
    
    举例子 b：
    stext = "E:/KaiFaTEST/chatGPT/testa/001/Render/chatGPT_testa_001_v002/chatGPT_testa_001_v002.%d.exr"
    # 更换 拆分魔法格式，这里符号@ 标识 不以任何符号拆分字符串直接数字符位置截取。 另一种方式可以是直接空位取段 */*-1*@*2:"
    mofa = "*/*1,*/*2,*/*-1*@*2:-7"
    bsb = "  "
    return - >>    KaiFaTEST  chatGPT  atGPT_testa_001_v002 [KaiFaTEST,chatGPT,atGPT_testa_001_v002]
    
    关键字解释：
    mofa ： 拆分格式字符串
    stext ：拆分文字字符串
    bsb ：连接返回的字符串，默认为符号"_"
    
    返回设定：
    返回一个 连接好的字符，以及一个拆分后获取内容的列表
    
    
    """

    if stext is None:
        return "", []

    mfget =  [i for i in mofa.split(",") if i != ""]

    rusl = []
    rtv = None
    for i in mfget:
        ret = stext
        if "*" in i:
            mg2 = [i for i in i.split("*") if i != ""]
            for x in range(0,len(mg2),2):
                fh = mg2[x]
                fw = mg2[x+1]
                if fh == "@":
                    if ":" in fw:
                        fwa = fw.split(":")[0]
                        fwb = fw.split(":")[-1]
                        if fwb == "":
                            ret = ret[int(fwa):]
                        elif fwa == "":
                            ret = ret[:int(fwb)]
                        else:
                            ret = ret[int(fwa):int(fwb)]
                    else:
                        ret = ret[int(fw)]
                else:
                    if ":" in fw:
                        fwa = fw.split(":")[0]
                        fwb = fw.split(":")[-1]
                        if fwb == "":
                            ret = "%s"%fh.join(ret.split(fh)[int(fwa):])
                        elif fwa == "":
                            ret = "%s"%fh.join(ret.split(fh)[:int(fwb)])
                        else:
                            ret = "%s"%fh.join(ret.split(fh)[int(fwa):int(fwb)])
                    else:
                        ret = ret.split(fh)[int(fw)]
                continue
        else:
            ret = i
        rusl.append(ret)
    rtv = "%s"%bsb.join(rusl)
    return rtv,rusl