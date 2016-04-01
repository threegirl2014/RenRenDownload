# -*- coding:utf-8 -*-

import json
from PersonalInfo import PersonalInfo
import config

class FriendList:
    
    def __init__(self,spider):
        self.url = config.FRIENDLISTURL
        self.spider = spider
        self.friendList = []
        
    def getFriendListUrl(self):
        return self.url
    
    def setContent(self,content):
        content = content[content.find('"data"'):-3]
        dictinfo = json.loads('{' + content + '}')
        self.friendsNum = dictinfo['data']['hostFriendCount']
        for item in dictinfo['data']['friends']:
            temp = {}
            if len(item['fgroups']) == 0:
                group = u'无圈'
            else:
                group = item['fgroups'][0]
            temp['group'] = group
            temp['fid'] = item['fid']
            temp['comf'] = item['comf']
            temp['fname'] = item['fname']
            temp['belong'] = item['info']
            self.friendList.append(temp)
    
#     def saveContent(self): 
#         for item in self.friendList:
#             print item['group'], item['fid'], item['comf'], item['fname'], item['belong']

    def work(self):
        self.setContent(self.spider.getContent(self.url))
        return self.friendList
