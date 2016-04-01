# RenRenDownload
***
####相关博客
[一个人人网python爬虫](http://www.jianshu.com/p/b7e596ba3b77)

####功能说明：
下载人人网上和自己相关的信息：

    Download your info from RenRen.com, include:
    1. personal information
    2. photos albums
    3. status
    4. blogs
    5. friends information
    6. the gossip
    7. comments
    8. save your own and all your friends personal info into a database(mysql) 
    
其中相册中的图片是保存到本地。

而其他项目中的图片则未下载，由于使用了markdown来保存信息，看到的图片其实是存储在本地的该图片的url。

由于目标是下载自己在人人网上留下的信息，所以并没有考虑如何下载别人的相册、日志等信息。如果下载目标非本人，则可尝试将调用函数中的ownerID更改为目标人的ID。我已尝试下载朋友的相册，结果是成功的。

本代码不能下载分享和收藏两项，留言下载功能只能下载最初的留言板功能上的留言，不能下载后续的对话留言。
***

####使用方法：

在config.py中更改EMAIL/PASSWORD/ownerID，以及其后所需的文件名和路径，若需要使用MySQL，则需要将dbConnectInfo也进行更改。

设置好后，运行Main.py即可。

需要注意的是，有时候登录需要进行验证码识别，另外在爬去别人的个人主页时，人人网会对浏览数目进行累计，如果超过100，则同样会需要用户进行验证码识别。程序中已经考虑了验证码环节，当命令台输出“please input validation code：”时，在代码保存的目录会生成icode.jpg，输入该图片中的验证码至命令台即可。
