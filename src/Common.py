# -*- coding:utf-8 -*-
import os
import json

def checkPath(path):
    if not os.path.exists(path):
        os.mkdir(path)
        
def generateJson(rawContent):
    content = rawContent[rawContent.find('{') : rawContent.find('};')+1]
    #由于从人人网解析出来的content中并不是严格使用双引号，所以需要将出现的单引号替换为双引号
    #但是用replace替换的话有一个地方会对结果造成干扰（见下，单引号全部替换后，由于http后面有“:”，会使得json报错）
    #所以用单引号之前有没有“=”来判断是否需要转换，具体步骤见如下循环
    #"title":"<img src='http://a.xnimg.cn/imgpro/icons/statusface/zongzi.gif' alt='粽子'  />高铁上拣韭菜。。。\n"
#     content = content.replace("'",'"')
    newContent = ''
    i= -1
    for k in range(0,len(content)):
        if i == -1:
            if content[k] != "'":
                newContent += content[k]
            else:
                i = k
        else:
            if content[k] == "'":
                if i - 1 >= 0 and content[i-1] == '=':
                    newContent += content[i:k+1]
                else:
                    newContent += '"' + content[i+1:k] + '"'
                i = -1
#     print newContent
    return json.loads(newContent)