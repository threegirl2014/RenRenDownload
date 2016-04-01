# -*- coding: utf-8 -*-

import Common
import config
from Comment import Comment
from Photos import Photos
from bs4 import BeautifulSoup
import datetime

class Album:
    
    def __init__(self,userID,spider,ownerID,albumID,albumName,photoCount,path):
        self.url = config.ALBUMURL % (ownerID, albumID)
        self.userID = userID
        self.spider = spider
        self.ownerID = ownerID
        self.albumID = albumID
        self.albumName = albumName
        self.path = path
        self.photoCount = photoCount
        self.photoList = []
        
    def getPhotoList(self):
        soup = BeautifulSoup(self.spider.getContent(self.url))
        for item in soup.find_all('script',type='text/javascript'):
            if 'nx.data.photo' in item.getText():
                rawContent = item.getText()
                dictinfo = Common.generateJson(rawContent)
                for photo in dictinfo['photoList']['photoList']:
                    temp = {}
                    temp['albumId'] = photo['albumId']
                    temp['photoId'] = photo['photoId']
                    temp['ownerId'] = photo['ownerId']
                    self.photoList.append(temp)
                break
    
    def getAlbumComments(self):
        comment = Comment(self.userID,self.spider,self.albumID,'album',self.ownerID)
        content = comment.work()
        if content == '':
            with open(self.path + '/comments.markdown','w') as f:
                f.write((u'**评论: **\n\n').encode('utf-8'))
                f.write(content)
        
    def savePhotos(self):
        for item in self.photoList:
            photos = Photos(self.userID,self.spider,self.albumName,item,self.path)
            photos.work()
            break
    
    def work(self):
        self.getPhotoList()
        self.getAlbumComments()
        print datetime.datetime.now(), self.albumName, 'downloading...'
        self.savePhotos()
        print datetime.datetime.now(), self.albumName, 'save successfully'