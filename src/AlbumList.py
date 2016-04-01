# -*- coding: utf-8 -*-

from Album import Album
import config
import Common
from bs4 import BeautifulSoup
import json
import datetime

class AlbumList:
    
    def __init__(self,userID,spider,ownerID):
        self.url = config.ALBUMLISTURL % ownerID
        self.userID = userID
        self.spider = spider
        self.ownerID = ownerID
        self.albumlist = []
        
    def getAllAlbumList(self):
        soup = BeautifulSoup(self.spider.getContent(self.url))
        for item in soup.find_all('script',type='text/javascript'):
            if 'nx.data.photo' in item.getText():
                rawContent = item.getText()
                dictinfo = Common.generateJson(rawContent)
                self.albumCount = dictinfo['albumList']['albumCount']
                for album in dictinfo['albumList']['albumList']:
                    temp = {}
                    temp['albumId'] = album['albumId']
                    temp['albumName'] = album['albumName']
                    temp['photoCount'] = album['photoCount'] 
                    self.albumlist.append(temp)
                break
        print 'get all album list'
        
    def saveAlbum(self,album):
        name = album['albumName'].replace('/','__')
        path = config.PATH + '/' + self.ownerID + '/' + config.ALBUMLISTPATH + '/' + album['albumId'] + ' ' + name
        Common.checkPath(path)
        album = Album(self.userID,self.spider,self.ownerID,album['albumId'],name,album['photoCount'],path)
        album.work()
        
    def work(self):
        self.getAllAlbumList()
        d1 = datetime.datetime.now()
        for album in self.albumlist:
            self.saveAlbum(album)
        d2 = datetime.datetime.now()
        print 'all album save successfully, time:', d2 - d1