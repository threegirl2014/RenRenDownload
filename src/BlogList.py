# -*- coding:utf-8 -*-

import urllib
import json
import config
from Comment import Comment
from Blog import Blog
import datetime

class BlogList:
    
    def __init__(self,userID,spider,ownerID):
        self.url = config.BLOGLISTURL % ownerID
        self.userID = userID
        self.spider = spider
        self.ownerID = ownerID
        self.blogsCount = 0
        self.bloglist = []
        
    def getBlogListUrl(self, categoryId=0, pageNo=0):
        data = {
                'categoryId': categoryId,
                'curpage': pageNo,
                }
        return self.url + urllib.urlencode(data)
    
    def setContent(self,content):
#         print content
        dictinfo = json.loads(content)
        self.blogsCount = dictinfo['count']
        for item in dictinfo['data']:
            temp = {}
            #都是20xx年创建的
            temp['createTime'] = '20' + item['createTime']
            temp['commentCount'] = item['commentCount']
            temp['id'] = int(item['id'])
            temp['title'] = item['title']
            temp['category'] = item['category']
            temp['containAudio'] = item['containAudio']
            temp['containImage'] = item['containImage']
            temp['containVideo'] = item['containVideo']
            self.bloglist.append(temp)
        if self.blogsCount - len(self.bloglist) > 0:
            return True
        else:
            return False
        
    def saveContent(self):
        with open(config.PATH + '/' + self.ownerID + '/bloglist.markdown','w') as f:
            f.write(str(self.blogsCount) + '\n')
            f.write(config.gap)
            for item in self.bloglist:
                line = 'id: ' + str(item['id']) + '\n\n'
                line += 'createTime: ' + item['createTime'] + '\n\n'
                line += 'category: ' + item['category'] + '\n\n'
                line += 'title: ' + item['title'] + '\n\n'
                line += 'commentCount: ' + str(item['commentCount']) + '\n\n'
                line += 'containImage: ' + str(item['containImage']) + '\n\n'
                line += 'containAudio: ' + str(item['containAudio']) + '\n\n'
                line += 'containVideo: ' + str(item['containVideo']) + '\n\n'
                line += config.gap
                f.write(line.encode('utf-8'))
        print datetime.datetime.now(), ': bloglist save successfully'
    
    def saveEveryBlog(self):
        d1 = datetime.datetime.now()
        for item in self.bloglist:
            blogID = str(item['id'])
            filename = config.PATH + '/' + self.ownerID + '/' + config.BLOGSPATH + '/' + item['createTime'] + '  ' + item['category'] + '  ' + item['title'] + '.markdown' 
            blog = Blog(self.userID,self.spider,blogID,self.ownerID,filename,item)
            blog.work()
        d2 = datetime.datetime.now()
        print 'all blogs have been downloaded successfully, time: ', d2 - d1
        
    def work(self):
        i = 0
        while True:
            result = self.setContent(self.spider.getContent(self.getBlogListUrl(pageNo=i)))
            i += 1
            if result == False:
                break
        self.saveContent()
        self.saveEveryBlog()
        