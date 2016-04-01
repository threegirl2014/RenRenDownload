# -*- coding: utf-8 -*-
 
EMAIL = 'email'
PASSWORD = 'password'
ownerID = 'ownerID'

cookieFile = 'cookie.txt'
dbFile = '/tmp/people.txt'
dbName = 'renren'


dbConnectInfo = {
                   'host':'localhost',
                   'user':'root',
                   'passwd':'root',
#                    'db': 'renren',
#                    'charset':'utf8'
                }

PATH = 'data'
BLOGSPATH = 'blogs'
ALBUMLISTPATH = 'albumlist'

LOGINURL = r'http://www.renren.com/PLogin.do'
ICODEURL = r'http://icode.renren.com/getcode.do?t=login&rnd=Math.random()'
# loginUrl = 'http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp=2016202210414'
ALBUMLISTURL = r'http://photo.renren.com/photo/%s/albumlist/v7?showAll=1#'
ALBUMURL = r'http://photo.renren.com/photo/%s/album-%s/v7'
PHOTOSURL = r'http://photo.renren.com/photo/%s/photo-%s/v7'
BLOGLISTURL = r'http://blog.renren.com/blog/%s/blogs?'
BLOGURL = r'http://blog.renren.com/blog/%s/%s'
COMMENTURL = r'http://comment.renren.com/comment/xoa2'
FRIENDLISTURL = r'http://friend.renren.com/groupsdata'
GOSSIPURL = r'http://gossip.renren.com/ajaxgossiplist.do'
CONVERSATIONURL = r'http://gossip.renren.com/getconversation.do'
PERSONALINFOURL = r'http://www.renren.com/%s/profile?v=info_timeline'
STATUSURL = r'http://status.renren.com/GetSomeomeDoingList.do'
VALIDATEURL = r'http://www.renren.com/validateuser.do'

gap = '\n**********************\n'

# FailCode via "login-v6.js"
FAILCODE = {
            '-1': '登录成功',
            '0': '登录系统错误，请稍后尝试',
            '1': '您的用户名和密码不匹配',
            '2': '您的用户名和密码不匹配',
            '4': '您的用户名和密码不匹配',
            '8': '请输入帐号，密码',
            '16': '您的账号已停止使用',
            '32': '帐号未激活，请激活帐号',
            '64': '您的帐号需要解锁才能登录',
            '128': '您的用户名和密码不匹配',
            '512': '请您输入验证码',
            '4096': '登录系统错误，稍后尝试',
}
