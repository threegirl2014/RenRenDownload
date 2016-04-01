# -*- coding:utf-8 -*-

import urllib
import json
import config

class Gossip:

    def __init__(self,userID,spider,ownerID):
        self.url = config.GOSSIPURL
        self.conversationUrl = config.CONVERSATIONURL
        self.userID = userID
        self.ownerID = ownerID
        self.spider = spider
        self.gossipCount = 0
        self.gossipContent = []
    
    def setGossipCount(self,content):
        dictinfo = json.loads(content)
        self.gossipCount = dictinfo['gossipCount']
    
    def getGossipData(self,pageNo=0):
        data = {
                'guest': self.userID,
                'curpage': -1,
                'destpage': 0,
                'page': pageNo,
                'id': self.ownerID,
                'resource': 'undefined',
                'search': 0,
                'boundary': 0,
                'gossipCount': self.gossipCount
                }
        return urllib.urlencode(data)
        
    def setContent(self,content):
        dictinfo = json.loads(content)
        for item in dictinfo['array']:
            temp = {}
            temp['time'] = item['time']
            temp['guestId'] = item['guestId']
            temp['guestName'] = item['guestName']
            temp['filterdBody'] = item['filterdBody']
            temp['id'] = item['id']
            if item['gift'] == 'true':
                temp['isGift'] = True
            else:
                temp['isGift'] = False
            self.gossipContent.append(temp)
    
    def saveContent(self):
        with open(config.PATH + '/' + self.ownerID  + '/gossip.markdown','w') as f:
            f.write('quantity of gossips: ' + str(self.gossipCount) + '\n')
            f.write(config.gap)
            for item in self.gossipContent:
                line = 'id: ' + item['id'] + '\n\n'
                line += 'time: ' + item['time'] + '\n\n'
                line += 'guestId: ' + item['guestId'] + '\n\n'
                line += 'guestName: ' + item['guestName'] + '\n\n'
                line += 'isGift: ' + str(item['isGift']) + '\n\n'
#                 line += 'filterOriginalBody: ' + item['filterOriginalBody'] + '\n'
                line += 'filterdBody: ' + item['filterdBody'] + '\n'
                line += config.gap
                f.write(line.encode('utf-8'))
        print 'save gossip complete' 
                    
    def work(self):
        self.setGossipCount(self.spider.getContent(self.url, self.getGossipData(0)))
        i = 0
        for i in range(0, self.gossipCount/20 + 1):
            self.setContent(self.spider.getContent(self.url, self.getGossipData(i)))
        self.saveContent()       
            
            