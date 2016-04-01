# -*- coding: utf-8 -*-

import Common
import config
from Comment import Comment
from bs4 import BeautifulSoup
import urllib

class Photos:
    
    def __init__(self,userID,spider,albumName,summary,path):
        self.userID = userID
        self.spider = spider
        self.albumName = albumName
        self.ownerID = summary['ownerId']
        self.albumID = summary['albumId']
        self.pageUrl = config.PHOTOSURL %(self.ownerID,summary['photoId'])
        self.photos = []
        self.path = path
        
    def getPhotoDetailList(self):
        soup = BeautifulSoup(self.spider.getContent(self.pageUrl))
        for item in soup.find_all('script',type='text/javascript'):
            if 'nx.data.photo' in item.getText():
                rawContent = item.getText()
                dictinfo = Common.generateJson(rawContent)
                self.photoCount = dictinfo['photoTerminal']['json']['photoNum']
                for item in dictinfo['photoTerminal']['json']['list']:
                    temp = {}
                    temp['id'] = int(item['id'])
                    temp['title'] = item['originTitle']
                    temp['date'] = item['date']
                    if item['xLargeUrl']:
                        temp['url'] = item['xLargeUrl']
                    else:
                        temp['url'] = item['large480']
                    temp['commentCount'] = item['commentCount']
                    temp['owner'] = item['owner']
                    self.photos.append(temp)
                break
       
    def savePhotos(self):
        for item in self.photos:
            filename = self.path + '/' + str(item['id']) + '.jpg'
            count = 0
            with open(filename,'wb') as f:
                while True:
                    try:
                        urllib.urlretrieve(item['url'], filename)
                    except Exception,e:
                        print item['id'], 'fail +1', e.message
                        count += 1
                    else:
                        count = 0
                        break
#                 f.write(self.spider.getContent(item['url'])) 
    
    def savePhotoComment(self):
        with open(self.path + '/photo details.markdown','w') as f:
            for item in self.photos:
                line = u'**ID: ' + str(item['id']) + '**\n\n'
                line += u'**名称: ' + item['title'].replace('\n',' ') + '**\n\n'
                line += u'**时间: ' + item['date'] + '**\n\n'
                f.write(line.encode('utf-8'))
                filename = str(item['id'])
                f.write(('![' + filename + '](' + filename + '.jpg)\n\n').encode('utf-8'))
                if int(item['commentCount']):
                    comment = Comment(self.userID,self.spider,item['id'],'photo',item['owner'])
                    f.write((u'**评论: **\n\n').encode('utf-8'))
                    f.write(comment.work())
                f.write(config.gap)
                
    def work(self):
        self.getPhotoDetailList()
        self.savePhotos()
        self.savePhotoComment()