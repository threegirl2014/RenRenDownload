# -*- encoding:utf-8 -*-

import sys
import os
import re
import urllib
import urllib2
import cookielib
import webbrowser
import config
import Common

class RenRenSpider:
    '''
    Download your info from RenRen.com, include:
    1. personal information
    2. photos albums
    3. status
    4. blogs
    5. friends information
    6. the gossip
    7. comments
    8. save your own and all your friends personal info into a database(mysql)  
    '''
    def __init__(self):
        self.username,self.password = config.EMAIL,config.PASSWORD
        self.cookie = cookielib.LWPCookieJar()
        self.cookie.load(config.cookieFile, ignore_discard=True, ignore_expires=True)
        self.opener = urllib2.build_opener( urllib2.HTTPCookieProcessor(self.cookie) )
        urllib2.install_opener(self.opener)
    
    def login(self):
        url = urllib2.urlopen('http://www.renren.com').geturl()
        print url
        if re.match('http://www.renren.com/[\d]{9}', url):
            self.userID = url.split('/')[3]
            print 'Login Successfully'
            return True
        else:
            print 'cookie file broke'
            
        data = {
                'email' : self.username,
                'password' : self.password,
                'origURL' : 'http://www.renren.com/home',
                'icode' : ''
                }
        isLogin = False
        failCodePattern = re.compile('&failCode=(\d+)')
        
        print 'Login...'
        while not isLogin:
            validation = self.opener.open(config.ICODEURL).read()
            with open('icode.jpg','wb') as file:
                file.write(validation)
            icode = raw_input('please input validation code：')
            data['icode'] = icode

            request = urllib2.Request(config.LOGINURL, urllib.urlencode(data))
            response = self.opener.open(request,timeout=20)
                
            url = response.geturl()
            print url
            failCode = failCodePattern.search(url)
            if not failCode:
                for item in self.cookie:
                    if item.name == 'id':
                        self.userID = item.value
                        print 'Login Successfully'
                        self.cookie.save(config.cookieFile,ignore_discard=True, ignore_expires=True)
                        isLogin = True
                        break
            else:
                failCode = failCode.group(1)
                if failCode in config.FAILCODE.keys():
                    print 'failCode=',failCode,config.FAILCODE[failCode]
                    if failCode == '512':
                        continue
                else:
                    print "unkown error"
                return False
        return True

    def getRawContent(self,url,data=None):
        try:
            page = self.opener.open(url,data,timeout=20)
        except Exception, e: 
            print 'Fail to login:', e.message
            return
        return page 
    
    def getContent(self,url,data=None):
        return self.getRawContent(url,data).read()   
    
    def getUserID(self):
        return self.userID
        
if __name__ == '__main__':
    lonelyMan = RenRenSpider()
    lonelyMan.login()
