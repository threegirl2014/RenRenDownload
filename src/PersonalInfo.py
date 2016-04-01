# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import config

class PersonalInfo:
    
    def __init__(self,userID,spider,ownerID,summary=None):
        self.personalInfoUrl =  config.PERSONALINFOURL % ownerID
        self.userID = userID
        self.spider = spider
        self.ownerID = ownerID
        self.summary = summary

    def getContent(self,info):
        return self.soup.find('div',class_='info-section clearfix',id=info)
    
    def getEduInfo(self,info):
        edu = ''
        if self.getContent(info) == None:
            return edu
        for item in self.getContent(info).find_all('dl',class_='info'):
            edu += item.find('dt').string + ':(' + item.find('dd').get_text().strip().replace('\n','') +') ' 
        return edu
        
    def getBasicInfo(self,info):    
        gender, birth, hometown = '','',''
        if self.getContent(info) == None:
            return (gender, birth, hometown)
        for item in self.getContent(info).find_all('dl',class_='info'):
            if item.find('dt').string == u'性别':
                if item.find('dd').get_text().strip() == u'男':
                    gender = 'm'
                elif item.find('dd').get_text().strip() == u'女':
                    gender = 'f'
                else:
                    gender = 'u'
            elif item.find('dt').string == u'生日':
                birth = item.find('dd').get_text().strip().replace('\n','')
            elif item.find('dt').string == u'家乡':
                hometown = item.find('dd').get_text().strip().replace('\n','')       
        return (gender, birth, hometown)
            
    def getInfo(self,content):
        self.soup = BeautifulSoup(content)
        edu = self.getEduInfo('educationInfo')
        gender, birth, hometown = self.getBasicInfo('basicInfo')
        id = self.ownerID
        if self.userID == self.ownerID:
            relation = 'myself'
            name,belong,group,comf = '','','',''
        else:
            relation = 'friend'
            name = self.summary['fname']
            belong = self.summary['belong']
            group = self.summary['group']
            comf = self.summary['comf']
        return (id,name,relation,gender,birth,hometown,belong,group,edu,comf)

    def optionalValidate(self,content):
        soup = BeautifulSoup(content)
        for item in soup.find_all('div',class_='optional'):
            src = item.img['src']
            validateCode = self.spider.getContent(src)
            with open('icode.jpg','wb') as f:
                f.write(validateCode)
            icode = raw_input('please input validation code：')
            data = {
                    'id' : self.ownerID,
                    #人人网使用utf-8
                    'submit' : u'继续浏览'.encode('utf-8'),
                    'icode' : icode
                    }
            self.spider.getContent(config.VALIDATEURL,urllib.urlencode(data))
            break
    
    def work(self):
        while True:
            page = self.spider.getRawContent(self.personalInfoUrl)
            url = page.geturl()
            content = page.read()
            if url != self.personalInfoUrl:
                if 'validateuser.do' in url:
                    self.optionalValidate(content)
                    continue
                else:
                    print "unknown error"
                    return
            else:
                break
        return self.getInfo(content)
