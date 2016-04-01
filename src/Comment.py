# -*- coding:utf-8 -*-

import urllib
import json
import config

class Comment:

    def __init__(self,userID,spider,entryId,sourceType,ownerID):
        self.url = config.COMMENTURL
        self.userID = userID
        self.spider = spider
        self.entryId = entryId
        self.sourceType = sourceType
        self.ownerID = ownerID
        self.comments = []
        
    def getCommentUrl(self, offset=0):
        data = {
                'limit' : 20,
                'desc' : 'false',
                'offset' : offset,
                'replaceUBBLarge' : 'true',
                'type' : self.sourceType,
                'entryId' : self.entryId,
                'entryOwnerId' : self.ownerID
                }
        return self.url + '?' + urllib.urlencode(data)
        
    def setContent(self,content):
#         print content
        dictinfo = json.loads(content)
        for item in dictinfo['comments']:
            temp = {}
            temp['type'] = item['type']
            temp['id'] = item['id']
            temp['time'] = item['time']
            temp['authorName'] = item['authorName']
            temp['authorId'] = item['authorId']
            temp['content'] = item['content']
            self.comments.append(temp)
#         print dictinfo['hasMore'], len(self.comments)
        return (dictinfo['hasMore'], dictinfo['nextOffset'])
            
        
    def saveContent(self):
        lines = '\n'
        for item in self.comments:
            lines += item['authorName'] + '    ' + item['time'] + '\n\n'
#             for line in item['content'].split('\n'):
#                 if line == '':
#                     continue
            line = item['content'].replace('\n','')
            line = line.replace('\r','')
            lines += '*' + line + '*\n\n'
        return lines.encode('utf-8')
    
    def work(self):
        offset = 0
        while True:
            result = self.setContent(self.spider.getContent(self.getCommentUrl(offset)))
            hasMore,nextOffset = result
            if hasMore:
                offset = nextOffset
            else:
                break
        return self.saveContent()