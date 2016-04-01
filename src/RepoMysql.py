# -*- coding:utf-8 -*-

import config
from PersonalInfo import PersonalInfo
from FriendList import FriendList
import MySQLdb
import datetime

createDbSql = 'create database if not exists %s DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci'
useDbSql = 'use %s'
createSql = 'create table people(\
                id char(9) not null,\
                name varchar(15),\
                relation char(6),\
                gender char(1),\
                birth varchar(20),\
                hometown varchar(20),\
                belong varchar(20),\
                circle varchar(20),\
                edu varchar(200),\
                comf varchar(4),\
                primary key (id))'
insertSql = 'insert into people \
            (id,name,relation,gender,birth,hometown,belong,circle,edu,comf) values \
            ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
outputSql = 'select * from people into outfile "%s"' % config.dbFile

class RepoMysql:
    
    def __init__(self,userID,spider):
        self.conn = MySQLdb.connect(**config.dbConnectInfo)
        self.cursor = self.conn.cursor() 
        self.userID = userID
        self.spider = spider
        self.peopleList = []
        
    def __del__(self):
        self.cursor.close()
        self.conn.close()
        
    def createDb(self):
        try:
            self.cursor.execute(createDbSql % config.dbName)
            self.cursor.execute(useDbSql % config.dbName)
            #要么在这里设置，要么在config的dbConnectInfo中添加
            self.conn.set_character_set('utf8')
            self.cursor.execute(createSql)
            self.conn.commit()
        except Exception,e:
            print e
            self.conn.rollback()
        else:
            print 'create db successfully'
            
    def insertDb(self):
        try:
            for item in self.peopleList:
                self.cursor.execute(insertSql % item)
            self.conn.commit()
        except Exception,e:
            print e
            self.conn.rollback()
        else:
            print 'insert db successfully'
                    
    def outputDb(self):
        try:
            self.cursor.execute(outputSql)
            self.conn.commit()
        except Exception,e:
            print e
            self.conn.rollback()
        else:
            print 'output db successfully'
                 
    #输出时间多次出现，是否可用装饰器进行替换？
    def collectInfo(self):
        myself = PersonalInfo(self.userID,self.spider,self.userID)
        self.peopleList.append(myself.work())
        
        friendList = FriendList(self.spider)
        friends = friendList.work()
        d1 = datetime.datetime.now()
        i = 1
        count = len(friends)
        print datetime.datetime.now(), ": begin collect people info"
        for item in friends:
            friend = PersonalInfo(self.userID,self.spider,item['fid'],item)
            self.peopleList.append(friend.work())
            if i % 100 == 0:
                print datetime.datetime.now(), ": already collect %d/%d people info" %(i,count)
            i += 1
        d2 = datetime.datetime.now()
        print 'collect info successfully, time: ', d2 - d1
             
    def work(self):
        self.createDb()
        self.collectInfo()
        self.insertDb()
        self.outputDb()
    