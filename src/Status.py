# -*- coding:utf-8 -*-

import urllib
import json
import config
from Comment import Comment
from bs4 import BeautifulSoup
import datetime

class Status:

    def __init__(self,userID,spider,ownerID):
        self.url = config.STATUSURL
        self.userID = userID
        self.spider = spider
        self.ownerID = ownerID
        self.status = []
    
    def getStatusUrl(self, pageNo=0):
        data = {
                'userId' : self.ownerID,
                'curpage' : pageNo
                }
        return self.url + '?' + urllib.urlencode(data)
    
    def setContent(self,content):
        dictinfo = json.loads(content)
        if dictinfo['doingArray'] == []:
            return False
        for item in dictinfo['doingArray']:
            temp = {}
            temp['id'] = int(item['id'])
            temp['dtime'] = item['dtime']
            temp['comment_count'] = item['comment_count']
            temp['content'] = item['content']
            if item.has_key('rootDoingUserName'):
                temp['rootDoingUserName'] = item['rootDoingUserName']
                temp['rootContent'] = item['rootContent']
            else:
                temp['rootDoingUserName'] = ''
                temp['rootContent'] = ''
            self.status.append(temp)
        return True
    
    def getStatusList(self):
        return self.status
    
    def saveContent(self):
        self.statusCount = len(self.status)
        with open(config.PATH + '/' + self.ownerID + '/status.markdown','w') as f:
            f.write('quantity of status:' + str(self.statusCount) + '\n')
            f.write(config.gap)
            for item in self.status:
                line = u'**ID号:** ' + str(item['id']) + '\n'
                line += u'**发表时间:** ' + item['dtime'] + '\n'
                line += u'**评论数:** ' + str(item['comment_count']) + '\n\n'
#                 line += 'content: ' + BeautifulSoup(item['content']).getText() + '\t\t'
                line += u'**内容:** ' + item['content'] + '\n\n'
                line += u'**原作者:** ' + item['rootDoingUserName'] + '\n\n'
                line += u'**原内容:** ' + item['rootContent'] + '\n\n'
                f.write(line.encode('utf-8'))
                if int(item['comment_count']):
                    f.write((u'**评论:**\n\n').encode('utf-8'))
                    comments = Comment(self.userID,self.spider,item['id'],'status',self.ownerID)
                    f.write(comments.work())
                f.write(config.gap)
        print datetime.datetime.now(), ': status save successfully'
        
    def work(self):
        pageNo = 0
        while True:
            result = self.setContent(self.spider.getContent(self.getStatusUrl(pageNo)))
            pageNo += 1
            if result == False:
                break
        self.saveContent()    
        
        