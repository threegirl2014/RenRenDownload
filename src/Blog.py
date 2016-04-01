# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import json
from bs4.element import NavigableString
import config
from Comment import Comment

class Blog:
    
    def __init__(self,userID,spider,blogID,ownerID,filename,summary):
        self.url = config.BLOGURL % (ownerID,blogID)
        self.userID = userID
        self.spider = spider
        self.blogID = blogID
        self.ownerID = ownerID
        self.filename = filename
        self.summary = summary
    
    def saveBlog(self):
        soup = BeautifulSoup(self.content)
        blogContent = soup.find('div',id='blogContent',class_='blogDetail-content')
        with open(self.filename, 'w+') as f:
            line = u'###日志标题: ' + self.summary['title'] + '\n\n'
            line += u'#####创建时间: ' + self.summary['createTime'] + '\n\n'
            line += u'#####所属分类: ' + self.summary['category'] + '\n\n'
            line += config.gap
            f.write(line.encode('utf-8'))
            f.write(blogContent.encode('utf-8'))
            if int(self.summary['commentCount']):
                f.write(config.gap)
                f.write((u'#####评论:\n\n').encode('utf-8'))
                comments = Comment(self.userID,self.spider,self.blogID,'blog',self.ownerID)
                f.write(comments.work())
        print self.filename + ' save success'
        
    def work(self):
        self.content = self.spider.getContent(self.url)
        self.saveBlog()