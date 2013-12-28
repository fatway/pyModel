#=============================================================================#
#  Python FAQ
#
#  个人常用代码库，简易维护
#  (基于Python2.5/2.6实现)
#
#  update: 2011-03-28 14:53
#=============================================================================#

# TODO: xml,thread,urllib,httplib...
# TODO: 函数 - 闭包、装饰器

0. 代码头结构
    # -*- coding:utf-8 -*-
    # file: test.py
    # by Lee, 2009-6-25

    """model's description
    """

    __version__ = "0.1"

    if __name__ == "__main__":

1. 生成随机数
    import random
    rnd = random.randint(1, 500) #产生1-500之间的随机整数
    print random.choice(range(1, 30))

    ###一个双色球选号系统，by 'bloodfoxse' @ bbs.crsky.com

    from random import choice

    a=[]
    while True:
        b=choice(range(1, 34))
        if b not in a:
            a.append(b)
        if len(a)==6:
            break
    print '红球号码为：',
    print a
    print '蓝球号码为：',
    print choice(range(1, 17))
    raw_input('按回车退出')

    ## 转载别人记录的备忘
    #随机整数：
    print random.randint(1, 50)

    #随机选取0到100间的偶数：
    print random.randrange(0, 101, 2)

    #随机浮点数：
    print random.random()
    print random.uniform(1, 10)

    #随机字符：
    print random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&*()')

    #多个字符中选取特定数量的字符：
    print random.sample('zyxwvutsrqponmlkjihgfedcba', 5)

    #多个字符中选取特定数量的字符组成新字符串：
    print string.join(random.sample(
        ['z','y','x','w','v','u','t','s',
        'r','q','p','o','n','m','l','k',
        'j','i','h','g','f','e','d','c',
        'b','a'], 5)).replace(' ','')

    #随机选取字符串：
    print random.choice(['剪刀', '石头', '布'])

    #打乱排序
    items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    print random.shuffle(items)

2. 产生GUID
    import uuid  # New in version 2.5
    guid1 = str(uuid.uuid1())  #根据本机和时间生成GUID
    guid2 = str(uuid.uuid4())  #生成随机的GUID
    poiid = str(uuid.uuid4()).upper().replace('-', '')  # 华业龙图ID号
    poiid = str(uuid.uuid4().hex.upper()) #pythonic

    uuid.uuid1().hex[-12:] #根据uuid1的机制，相当于本机的MAC地址.

3. 读写文件
    fp1 = open(r'd:\1.txt', 'r')  #读完以后记得fp1.close()
    fp2 = open('d:\\2.txt', 'w')
    #fp3 = open('d:\\3.txt', 'a')  # 追加读写

    # readline() vs. readlines()
    """.readline() 和 .readlines() 之间的差异是后者一次读取整个文件,
       象 .read() 一样。.readlines() 自动将文件内容分析成一个行的列表，
       该列表可以由 Python 的 for ... in ... 结构进行处理。
       另一方面，.readline() 每次只读取一行，通常比 .readlines() 慢得多。
       仅当没有足够内存可以一次读取整个文件时，才应该使用 .readline()。
    """
    # readlines 只在内存足够大时才使用

    for line in fp1.readlines():  # not pythonic
        fp2.write(line + '\n')

    for line in fp1:  # OK , pythonic
        do with line...
        line = line.rstrip('\n')  # 去除末尾的换行符
        line = line.rstrip()  #去除末尾的空白符（包括换行）

    # 严谨的做法
    file_objet = open('thefile.txt')
    try:
        for line in file_object:
            process(line)
    finally:
        file_object.close()

    ## 替换文本中的内容
    output_file.write(input_file.read().replace(stext, rtext))

    ## 从文件中读取指定的行，适用于小文件
    import linecache
    theline = linecache.getline(filepath, desired_line_number)

    ## 计算文件的行数
    # 小文件
    count = len(open(filepath, 'rU').readlines())
    # 大文件
    count = -1
    for count,line in enumerate(open(filepath, 'rU')):
        pass
    count += 1

    ## 从zip中读取文件
    import zipfile
    z = zipfile.ZipFile("zipfile.zip", "r")
    for filename in z.namelist():
        print 'File:', filename,
        bytes = z.read(filename)
        print 'has', len(bytes), 'bytes'

4. 读写配置文件，存储数据
    import cPickle as p
    #import pickle as p  # pickle理论上是标准模块，而cPickle是用C实现的，效率高很多

    shoplistfile = 'shoplist.data'
    shoplist = ['apple','mango','carrot','egg']

    #write to the file
    f = file(shoplistfile, 'w')
    p.dump(shoplist, f) #dump the object to file
    f.close()

    del shoplist

    #read back from the storage
    f = file(shoplistfile)
    storedlist = p.load(f)
    print storedlist

5. 读取csv文件
    import csv
    sReader = csv.reader(open('data.csv'))  # open('data.csv', 'rb')
    #2 reader = csv.reader(open('passwd', 'rb'), delimiter=';', quoting=csv.QUOTE_NONE)
    for row in sReader:
        print ';'.join(row)
        print row[0].decode('utf-8').encode('gb2312')

6. 使用SQLite等数据库
    import sqlite3
    conn = sqlite3.connect(r'd:\data.db')
    # conn = sqlite3.connect(':memory:')  # 存储于内存中的临时数据库
    cur = conn.cursor()

    cur.execute('select * form table_test')
    t = ('id', 'name',)
    cur.execute('select * from test where id=? and name=?', t)

    cells = cur.fetchall()
    for cell in cells:
        print cell

    conn.commit()  # update needed

    #2 for cell in cur.fetchall(): print cell

    ## 保存二进制文件
    from __future__ import with_statement
    import sqlite3

    db = sqlite3.connect('test.db')
    cur = db.cursor()

    cur.execute("CREATE TABLE if not exists t (b BLOB);")

    with open('0.bin', 'rb') as f:  #with是2.6下的默认模块，2.5调用的话需要加入首行from...
        cur.execute("insert into t values(?)", (sqlite3.Binary(f.read()), ))
        db.commit()

    cur.execute('select b from t limit 1')
    b = cur.fetchone()[0]

    with open('00.bin', 'wb') as f:
        f.write(b)

    db.close()

    ## 使用pyodbc连接SQL Server和Access
    '''连接字符串
       1.使用DSN连接数据库
       "DSN=myserver;PWD=xxx"
       2.不使用DSN连接
         SQL Server 2000-2008：
           DRIVER={SQL Server};SERVER=dbserver;DATABASE=test;UID=user;PWD=password
         Microsoft Access:
           DRIVER={Microsoft Access Driver (*.mdb)};DBQ=d:\\dir\\file.mdb
    '''
    import pyodbc
    connstr = "DRIVER={SQL Server};SERVER=192.168.9.246;DATABASE=GIS;UID=sa;PWD=xiaoping"
    coxn = pyodbc.connect(connstr)
    cur = coxn.cursor()

    # show tables
    cur.tables(tableType='TABLE')
    for table in cur:
        print table

    # select data
    sql = "select * from changsha_bus"
    cur.execute(sql)
    for row in cur:
        print row[0]

7. 数据加密
    ## base64加密
    import base64
    s = '7thSpace'
    s_out = base64.b64encode(s)  #'N3RoU3BhY2U='
    s_origi = base64.b64decode(s_out)  #'7thSpace'

    ## MD5加密
    import hashlib
    a = hashlib.md5('a').hexdigest()
    b = hashlib.sha224("Nobody inspects the spammish repetition").hexdigest()

    import md5   # MD5加密 （旧，不推荐）
    a=123444
    b=str(a)
    c=md5.new(b).hexdigest()

    ## 其他加密
    import hashlib
    h = hashlib.new('md4')
    #2 h = hashlib.new('md5')
    #3 h = hashlib.new('sha1')
    #4 h = hashlib.new('ripemd160')
    h.update('test string')
    outputchr = h.hexdigest()

    ## 比较两个文件是否一致
    import os
    import sys
    import md5
    f1 = open('f:/1.txt','r')
    f2 = open('f:/2.txt','r')
    print md5.new(f1.read()).digest() == md5.new(f2.read()).digest()

    ##--------------------------------------------
    # QQ的登录加密方法
    #from md5 import md5
    def processpwd(self):
        pwd = self.login_data["p"]  #QQ密码
        vc = self.login_data["verifycode"]  #验证码

        vc = vc.upper()

        s = md5(pwd).digest()
        s = md5(s).digest()
        s = md5(s).hexdigest().upper()

        pwd = md5(s+vc).hexdigest()
        self.login_data["p"] = pwd  #最终post给服务器的密码

8. 编码转换
    #不同编码格式之间的转换主要是借助unicode

    #1 unicode -> other
    a = u'中文'
    a_gb2312 = a.encode('gb2312')

    #2 other -> unicode
    a_unicode = a_gb2312.decode('gb2312')
    a_utf8 = a_unicode.encode('utf-8')

    #3 other -> other
    #union #1 & #2 then can trans other -> other, again sample:
    a = u'中文'
    a_gb2312 = a.encode('gb2312')
    a_unicode = a_gb2312.decode('gb2312')
    assert(a_unicode == a)
    a_utf8 = a_unicode.encode('utf-8')

    #4 判断字符串的编码
    isinstance(s, str)  #用来判断是否为一般字符串
    isinstance(s, unicode)  #用来判断是否为unicode

    #将任意字符串转换为unicode
    def u(s, encoding):
        if isinstance(s, unicode):
            return s
        else:
            return unicode(s, encoding)

    # 另有一特例见99其他

9. 遍历文件夹
    import os

    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if name[:-3] == 'exe':
                print name

    top = r'e:\py'
    os.chdir(top)
    for f in os.listdir(top):
        newfile = top + '/' + f
        if os.path.isdir(newfile):
            # 使用是用类和函数的方式来递归遍历
            pass
        if os.path.isfile(newfile):
            print newfile

    #删除文件
    top='mydata/'
    for root,dir,files in os.walk(top,topdown=False):
        for name in files:
            os.remove(os.path.join(root,name))

    os.rmdir('mydata')
    os.mkdir('mydata')

    # simple ####################################################
    # -*- coding: cp936 -*-
    #文件：BASE.py
    #用途：遍历目的文件夹所有文件，并根据过滤标志返回属于过滤条件返回的文件绝对地址
    #作者：刘华飞
    #版本: 0.01
    #时间：2007年5月11日
    #授权：本程序可以免费使用，转载修改必修附上原作者信息

    import os

    #全局变量设置歌曲预定格式
    Const_Song_Format=["mp3","wma","ogg"]

    class BASE:
        #类变量，设置文件列表
        fileList=[""]
        #类变量，设置文件计算
        counter=0

        def __init__(self):
            pass

        def RecusWalkDir(self,dir,filtrate=0):
            """本方法递归遍历目的文件夹中所有文件，获取指定格式的文件绝对地址,利用类变量fileList存储地址"""
            global Const_Song_Format
            for s in os.listdir(dir):
                newDir=dir+"/"+s
                if os.path.isdir(newDir):
                    self.RecusWalkDir(newDir)
                else:
                    if os.path.isfile(newDir):
                        if filtrate:
                            if newDir and (self.GetFileFormat(newDir) in Const_Song_Format):
                                self.__class__.fileList.append(newDir)
                                self.__class__.counter+=1
                            else:
                                self.__class__.fileList.append(newDir)
                                self.__class__.counter+=1

        def CycWalkDir(self,dir,filtrate=0):
            """本方法循环遍历文件夹中所有文件，获取指定格式的文件绝对地址，返回歌曲列表fileList"""
            global Const_Song_Format
            fileList=[""]
            for s in os.listdir(dir):
                newDir=dir+"/"+s
                if os.path.isfile(newDir):
                    if filtrate:
                        if newDir and (self.GetFileFormat(newDir) in Const_Song_Format):
                            fileList.append(newDir)
                    else:
                        fileList.append(newDir)
                else:
                    newDir=dir+"/"+s
                while os.path.isdir(newDir):
                    for s in os.listdir(dir):
                        newDir=dir+"/"+s
                        if os.path.isfile(newDir):
                            if filtrate:
                                if newDir and (self.GetFileFormat(newDir) in Const_Song_Format):
                                        fileList.append(newDir)
                            else:
                                fileList.append(newDir)
                        else:
                            newDir=dir+"/"+s
            return fileList

        def GetFileFormat(self,fileName):
            """返回文件格式"""
            if fileName:
                BaseName=os.path.basename(fileName)
                str=BaseName.split(".")
                return str[-1]
            else:
                return fileName


    if __name__=="__main__":
            b=BASE()
            b.RecusWalkDir(dir="E:/音乐无限")
            print (b.counter)
            for k in  b.fileList:
                            print k

10. lambda,reduce,filter,map,zip
    ## lambda函数是一种快速定义单行的最小函数，从Lisp借用来的。
    #  lambda 变量:单行表达式
    # 使用时的注意事项
    #  lambda 函数可以接收任意多个参数（包括可选参数）并且返回单个表达式的值
    #  lambda 函数不能包含命令，包含的表达式不能超过一个

    def f(x, y):
        return x*y
    f(2,3)
    # <=>
    g = lambda x,y: x*y
    g(2,3)

    ## reduce
    # reduce( function, iterable[, initializer])
    # 将参数列表安装从左到右的顺序依次应用到函数中
    # For example：
    #   reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) #calculates ((((1+2)+3)+4)+5).
    print reduce(lambda x,y:x*y, range(1, 1001)) #求1000的阶乘

    ## filter
    def my_filter(val_in_list):
        if val_in_list < 5:
            return False
        else:
            return True
    print filter(my_filter, [1,2,3,6,7])

    a = [1,2,3,4,5,6,7]
    b = filter(lambda x:x>5, a)
    print b  # [6,7]

    ## map
    # map( function, iterable, ...)
    # 将参数应用到函数上并返回结果列表
    l=[1,3,5,6,5]
    map(str,l)  # 将list的每一个元素转为string

    a = [1,2,3]
    map(lambda x:x+3, a)  # [4,5,6]

    ## zip
    # 将每个参数列表中的第i个元素配对成tuple。不好解释，看示例
    a=[1, 35, 6]
    b=['a', 'b', 'g']
    c=zip(a,b)   # [(1,'a'), (35,'b'), (6,'g')]

    m = ['a', 'b', 'c']
    n = [1, 2, 3, 4]
    zip(m,n)  # [('a', 1), ('b', 2), ('c', 3)]
    l = ['f','d','k']
    zip(m,n,l)  # [('a', 1, 'f'), ('b', 2, 'd'), ('c', 3, 'k')]

11. 正则表达式
    import re
    test = 'http://www.python.org';

    ## 匹配和搜索
    # re.match(pattern, string[, flags])
    # re.search(pattern, string[, flags])
    # re.findall(pattern, string[, flags])
    ##
    # pattern: 匹配模式
    # string: 要进行匹配的字符串
    # flags: 匹配标志
    #     re.I  忽略大小写
    #     re.L  根据本地设置而更改\w \W \b \B \s等的匹配内容
    #     re.M  多行匹配模式
    #     re.S  使“.”元字符匹配换行符
    #     re.U  匹配Unicode字符
    #     re.X  忽略pattern中的空格，并且可以使用“#”注释
    print re.match('python', test)  ## None
    print re.search('python', test)
    print re.findall('\w{3}', test)  # ['htt', 'www', 'pyt', 'hon', 'org']

    ## 替换函数
    # re.sub(pattern, repl, string[, count])
    # re.subn(pattern, repl, string[, count])
    ##
    # pattern: 正则表达式模式
    # repl: 要替换成的内容
    # count: 最大替换次数
    ##
    # subn 和 sub 函数功能相同，不过subn返回的是一个元组
    print re.sub('python', 'ruby', test)  # http://www.ruby.org
    print re.subn('python', 'ruby', test)  # ('http://www.ruby.org', 1)

    ## 分割字符串
    # re.split(pattern, string[, maxsplit = 0])
    print re.split('\.', test)  # ['http://www', 'python', 'org']
    print re.split('\.', test, 1)  # ['http://www', 'python.org']

    ## 编译正则表达式
    # compile(pattern[, flags])
    ##
    # match/search/findall  ->  (string[, pos[, endpos]])
    # sub/subn  ->  (repl, string[, count = 0])
    # split  ->  (string[, maxsplit = 0])
    r = re.compile('\w{4}')
    r.match(test)  # <_sre.SRE_Match object at 0x00F02EC8>
    r.search(test)
    r.findall(test)
    r.sub('*', test, 2)
    r.split(test)

    ## 使用组
    # 使用()表示其中的内容属于一个组
    r = re.compile(r'(\w{3})\.(\w{6})')
    m = r.search(test)
    print m.group(0)  # 'www.python'
    print m.group(1)  # 'www'
    print m.groups()  # ('www', 'python')
    # 使用组名 (?P<组名>)
    m = re.search(r'(?P<Area>\w{3})\.(?P<name>\w{6})', test)
    m.groupdict()  # {'name': 'python', 'Area': 'www'}
    m.group('Area')  # 'www'
    m.group(1)  # 'www'
    m.groups()  # ('www', 'python')

12. py2exe
    # -*- coding:utf-8 -*-
    # file: setup.py(py2exe)

    '''run step:
       1. install py2exe application
       2. build a script 'setup.py'
       3. run 'python setup.py py2exe'
    '''

    from distutils.core import setup
    import py2exe

    includes = ['PyFetion']

    options = {'py2exe':
                 {'compressed': 1,  # create a compressed zip archive
                 'optimize': 2,   #string or int of optimization level (0, 1, or 2)
                                        # 0 = don’t optimize (generate .pyc)
                                        # 1 = normal optimization (like python -O)
                                        # 2 = extra optimization (like python -OO)
                 'includes': includes,  #list of module names to include
                 'bundle_files': 1    #bundle dlls in the zipfile or the exe.
                                        #Valid levels are 1, 2, or 3 (default)
                 }
               }

    setup(
         version = '2.0',
         description = 'Weather to phone by Fetion',
         name = 'Weather2Fetion',
         copyright = 'no copyright',
         options = options,
         zipfile=None,
         # console=['Weather2Fetion.py']
         console=[
            {
             'script' : 'Weather2Fetion.py',
             'icon_resources' : [(1, 'wf.ico')]
            }
            ]
         )

    '''
    ----------------------------------------------------
    # setup.py
    from distutils.core import setup
    import py2exe
    setup(console=['hello.py'])

    运行setup.py，记得要传一个参数给它
    python setup.py py2exe

    py2exe会在当前目录下生成两个目录 build和dist
    build里是一些py2exe运行时产生的中间文件，dist里有最终的可执行文件
    library.zip
    w9xpopen.exe
    python25.dll
    hello.exe
    ----------------------------------------------------
    能不能打包成只有一个文件，hello.exe，这样运行方便些。
    ----------------------------------------------------
    加一个 zipfile = None
    比如：

    from distutils.core import setup
    import py2exe

    setup(
        version = '0.5.0',
        description = 'py2exe sample script',
        name = 'py2exe samples',
        options = {'py2exe': {'optimize': 2, 'bundle_files': 1, 'compressed': 1,}},

        windows = ['test_wx.py'],
        console = ['hello.py'],
        zipfile = None
        )
    ----------------------------------------------------
    呵呵，牛，果然可以，生成三个文件，Hello.exe, MSVCR71.dll, w9xpopen.exe，
    把后面两个文件删除，只保留Hello.exe也可以用.
    那么，后面两个是什么用的，什么情况下会用到。
    ----------------------------------------------------
    w9xpopen.exe是给 windows 98 用的。 MSVCR71.dll 是个vc7.1的动态链接库，
    py2exe生成的exe需要这个动态链接库，不过这个库一般winxp上都是有的。
    ----------------------------------------------------
    '''

13. 字符与ASCII码
    #char -> ascii
    ord('a')  # 97
    chr(98)  # b

    # 字符检查
    s = 'g fmnc wms bgblr rpylqjyrc gr zw fylb.'
    for i in s:
        if i.isalpha():  # 如果i是字符，isdigit()数字，isalnum()字符或数字
            m = chr(ord(i) + 2)
        else:
            m = i
        print m,
    # 'i  h o p e   y o u   d i d n t   t r { n s l { t e   i t   | y   h { n d .'

    #上面的方法太老土，python有自己的方法
    #string.maketrans()
    import string
    a=string.maketrans('abcdefghijklmnopqrstuvwxyz','cdefghijklmnopqrstuvwxyzab')
    print 'g fmnc wms bgblr rpylqjyrc gr zw fylb.'.translate(a)
    # 'i hope you didnt translate it by hand.'

    s = u'\u5434\u9896'
    print s  # 输出汉字
    s2 = """u'\u5434\u9896'"""
    print eval(s2)   # 输出汉字

14. 常用string操作
    string.capitalize() # 将字符串的第一个字母大写
    string.count()      # 获得字符串中某一子字符串的数目
    string.find()       # 获得字符串中某一子字符串的起始位置
    string.isalnum()    # 检测字符串是否仅包含0-9A-Za-z
    string.isalpha()    # 检测字符串是否仅包含字母A-Za-z
    string.isdigit()    # 检测字符串是否仅包含数字0-9
    string.islower()    # 检测字符串是否均为小写字母
    string.isspace()    # 检测字符串中所有字符是否均为空白字符
    string.istitle()    # 检测字符串中的单词是否为首字母大写
    string.isupper()    # 检测字符串是否均为大写字母
    string.join()       # 连接字符串
    string.lower()      # 将字符串全部转换为小写
    string.split()      # 分割字符串
    string.swapcase()   # 将字符串中大写字母转换为小写，小写字母转换为大写
    string.title()      # 将字符串中的单词首字母大写
    string.upper()      # 将字符串中的全部字母转换为大写
    len(string)         # 获取字符串长度

    # 字符串与数字相互转换, string.atoi(s[, base]) .. str()
    string.atoi(s[, base])
    s: 进行转换的字符串
    base: 可选参数，表示将字符串转换成的进制类型

    string.atoi('104879') + 4  # 104883
    string.atoi('13', 16)  # 19

    ## 字符串逐字反转
    revchars = astring[::-1]
    # 逐词反转
    revwords = satring.split()    # 字符串->单词列表
    revwords.reverse()            # 反转列表
    revwords = " ".join(revwords) # 单词列表->字符串

15. 类型转换
    int: 将字符串或浮点数转换为整数
    float: 将字符串或者整数转换为浮点数
    str: 将数字转换为字符串
    chr: 将ASCII值转换为ASCII字符
    hex: 将整数转换为十六进制的字符串
    long: 将字符串转换为长整型
    oct: 将整数转化为八进制的字符串
    ord: 将ASCII字符转换为ASCII值

    # 2进制到10进制：
    int(str(1011), 2)
    # 10进制到2进制：
    def bin(num):
        if num == 0: return '0'
        return "".join([str((num>>i)&1) for i in xrange(int(math.floor(math.log(num, 2))),-1,-1)])

16. 列表和字典常用方法
    list.append()       # 追加成员
    list.count(x)       # 计算参数x的出现次数
    list.extend(L)      # 向列表追加另一个列表L
    list.index(x)       # 获得参数k在列表中的位置
    list.insert()       # 向列表中插入数据
    list.pop()          # 删除列表的首成员
    list.remove()       # 删除类别的成员
    list.reverse()      # 将列表中成员的顺序颠倒
    list.sort()         # 将列表中成员排序
    
    # 列表推导式
    # TODO
    
    # 排列组合
    a = ['a','b','c']
    b= ['d','e','f']
    for (m,n) in ((m,n) for m in a for n in b):
        print m, n
    '''
    a d
    a e
    a f
    b d
    b e
    b f
    c d
    c e
    c f    
    '''
    
    # 列表再分组
    org = ['a','b','c','d','e','f','g','h','i','g','k']
    rst = [org[i:i+3] for i in range(0,len(org),3)]
    # [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'], ['g', 'k']]
    
    
    dic.clear()         # 清空字典
    dic.copy()          # 复制字典
    dic.get(k)          # 获得键k的值
    dic.has_key(k)      # 是否包含键k
    dic.items()         # 获得由键和值组成的列表
    dic.keys()          # 获得键的列表
    dic.values()        # 获得值的列表
    dic.pop(k)          # 删除键k
    dic.update()        # 更新成员

17. 文件和目录操作
    import os

    os.getcwd()             # 获得当前目录

    os.listdir()            # 获取当前目录中的文件
    os.listdir(path)        # 获取指定目录中的文件

    os.mkdir(path)          # 创建目录
    os.rmdir(path)          # 删除目录

    os.path.isdir(path)     # 判断是否为目录
    os.path.isfile(path)    # 判断是否为文件

    os.chdir()              # 更改工作目录

    os.rename(oldname, newname)  # 重命名

    os.system('notepad')    # 打开记事本程序
    os.system('notepad python.txt')  # 调用记事本打开python.txt文件

    ##调用系统SHELL并获取返回值
    cmd='nslookup %s' % hostname
    handle=os.popen(cmd, 'r')
    result_nslook=handle.read()
    #不获取返回值
    cmd='ls'
    os.system(cmd)


    ## 使用glob模块来获取文件列表
    import glob
    """glob和iglob函数区别在于glob直接返回List,类似range和xrange"""

    list1 = glob.glob(r"e:\*.txt")
    print list1  # eg. ['a.txt', 'b.txt']

    list2 = glob.iglob(r"e:\*.txt")
    print list2  # eg. <generator object at 0x011471C0>
    for i in list2:
        print i

18. ctypes
    '''ctypes模块可以使python调用位于动态链接库中的函数
       New in version 2.5
    '''
    ## sample
    from ctypes import *
    user32 = windll.LoadLibrary('user32.dll')
    user32.MessageBoxA(0, 'Cytpes is cool!', 'ctypes', 0)

    ## 加载DLL，需要符合调用约定
    # stdcall调用约定：
    Objdll = ctypes.windll.LoadLibrary("dllpath")
    Objdll = ctypes.WinDLL("dllpath")
    # cedcl调用约定：
    Objdll = ctypes.cdll.LoadLibrary("dllpath")
    Objdll = ctypes.CDLL("dllpath")
    # 其实windll和cdll分别是WinDLL类和CDLL类的对象

19. time & datetime
    import time

    print time.clock()      # 第一次使用clock()，返回程序运行的实际时间
    time.sleep(1)           # sleep(seconds) 休眠1秒后再执行
    print time.clock()      # 第二次及以后再运行clock()，返回的是自第一次调用后，到本次调用的时间间隔

    print time.ctime()      # 将一个时间戳(默认当前时间)转换为时间字符串 'Thu Jul 23 14:27:55 2009'

    print time.localtime()  # (2009, 7, 23, 14, 38, 55, 3, 204, 0)
                            # 将一个时间（默认当前时间）转换为struct_time
                            # (tm_year,tm_mon,tm_day,tm_hour,tm_min,tm_sec,tm_wday,tm_yday,tm_isdst)
    print time.localtime().tm_mon  # 当前月份
    print time.mktime(time.localtime())  # 1248331202.0
                            # 讲一个struct_time 转换为时间戳(float point number)
    print time.time()       # 返回当前时间戳 float point number

    ## 格式化时间
    # strftime(format[, tuple]) -> string
    # 将指定的struct_time(默认当前时间), 根据指定的格式化字符串输出
    #
    #  %y 两位数的年份表示（00-99）
    #  %Y 四位数的年份表示（000-9999）
    #  %m 月份（01-12）
    #  %d 月内中的一天（0-31）
    #  %H 24小时制小时数（0-23）
    #  %I 12小时制小时数（01-12）
    #  %M 分钟数（00-59）
    #  %S 秒（00-59）
    #
    #  %a 本地简化星期名称
    #  %A 本地完整星期名称
    #  %b 本地简化的月份名称
    #  %B 本地完整的月份名称
    #  %c 本地相应的日期表示和时间表示
    #  %j 年内的一天（001-366）
    #  %p 本地A.M.或P.M.的等价符
    #  %U 一年中的星期数（00-53）星期天为星期的开始
    #  %w 星期（0-6），星期天为星期的开始
    #  %W 一年中的星期数（00-53）星期一为星期的开始
    #  %x 本地相应的日期表示
    #  %X 本地相应的时间表示
    #  %Z 当前时区的名称
    #  %% %号本身
    print time.strftime("%Y-%m-%d %H:%M:%S")  # 2009-07-23 14:50:04

    # strptime(string, format) -> struct_time
    # 将时间字符串根据指定的格式化符转换成数组时间
    print strptime("Sat Mar 28 22:24:24 2009", "%a %b %d %H:%M:%S %Y")
    # (2009, 3, 28, 22, 24, 24, 5, 87, -1)
    # Sat Mar 28 22:24:24 2009 对应的格式化字符串为：%a %b %d %H:%M:%S %Y

20. 使用INI配置文件
    import ConfigParser
    import string, os, sys

    '''使用python处理ini文件，官方文档中ConfigParser处理的Linux系统下
       的conf形式的文件。

       ## test.conf或者test.ini
       [db]
       db_host=127.0.0.1
       db_port=3306
       db_user=root
       db_pass=password

       [con]
       thread=10
       processor=20

       该test.conf文件包含两个section，db下有四项、con下有两项
    '''

    cf = ConfigParser.ConfigParser()
    cf.read("test.ini")
    #2 cf.readfp(open('test.conf'))

    # 返回所有的section
    s = cf.sections()
    print 'section:', s  # section: ['db', 'con']

    o = cf.options("db")
    print 'options:', o

    v = cf.items("db")
    print 'db:', v

    print '-'*60
    # 可以按照类型读取出来
    db_host = cf.get("db", "db_host")
    db_port = cf.getint("db", "db_port")
    db_user = cf.get("db", "db_user")
    db_pass = cf.get("db", "db_pass")

    # 返回的是整型的
    threads = cf.getint("con", "thread")
    processors = cf.getint("con", "processor")

    print "db_host:", db_host
    print "db_port:", db_port
    print "db_user:", db_user
    print "db_pass:", db_pass

    print "thread:", threads
    print "processor:", processors

    # 修改一个值，再写回去
    cf.set("db", "db_pass", "password2")
    cf.write(open("test.ini", "w"))

    """另一个config_ini例子
    [portal]
    url = http://%(host)s:%(port)s/Portal
    user = dbserver
    host = localhost
    password = SECRET
    port = 8080

    ##
    from ConfigParser import ConfigParser
    import os

    filename = os.path.join(os.environ['HOME'], '.approachrc')

    config = ConfigParser()
    config.read([filename])

    url = config.get('portal', 'url')
    """

21. 三目运算
    #相信很多写C的人都会经常用到C的三元操作符吧，如下
    var = (condition) ? a: b;

    #在python中，你可以这样写：
    var = condition and a or b   # 也可以是下面的：
    var=x if x>y else y

22. StringIO
    import StringIO
    '''Read and Write string as File

       cStringIO是StringIO的一个更快的实现，但是不支持Unicode
    '''
    output = StringIO.StringIO()
    output.write('First line.\n')
    print >>output, 'Second line.'
        # 头一次见到">>"的使用，不过意思明白
        # 将secondline输出到output(文件)

    output.getvalue()
    # First line.\nSecond line.\n
    output.seek(6)
    output.write('LINE')
    output.getvalue()
    # First LINE.\nSecond line.\n

    output.close()

23. JSON
    import simplejson as json
    '''
       py2.6中内置了json模块

       这里使用simplejson库来实现，django/gae等都内置使用simplejson
       Encoding - dumps() 方法
       Decoding - loads() 方法

       另外可以使用python-json库来实现
    '''

    print json.dumps(['foo',{'bar':('baz',None,1.0,2)}])
    # dumps可以将一个python的数据结构转为json格式
    print json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True)
    # {"a": 0, "b": 0, "c": 0}

    ## 读取天目门址匹配系统返回的json数据
    import urllib

    url = 'http://192.168.9.218:8080/bseigc?GeoCoding&address=平沙二十巷16号&city=广州'
    feedjson = urllib.urlopen(url).read()
    #window._OLR={"c":[{"id":"9070","di":"广东省广州市白云区","na":"","add":"平沙二十巷","dn":"16号","tel":"","lo":11325190,"la":2325228,"mp":100}],"err":""}

    dict = json.loads(feedjson[12:])
    from pprint import pprint
    pprint(dict)
    '''
    {u'c': [{u'add': u'\u5e73\u6c99\u4e8c\u5341\u5df7',
             u'di': u'\u5e7f\u4e1c\u7701\u5e7f\u5dde\u5e02\u767d\u4e91\u533a',
             u'dn': u'16\u53f7',
             u'id': u'9070',
             u'la': 2325228,
             u'lo': 11325190,
             u'mp': 100,
             u'na': u'',
             u'tel': u''}],
     u'err': u''}
    '''

    count_point = len(dict['c']) # 匹配结果数量

    if count_point:
        print '匹配到', count_point, '个点位'
        print '详细信息：'
        for points in dict['c']:
            for point in points:
                print point.items()
    else:
        print dict['err']

24. YAML
    '''Yaml是传说中的堪比xml的数据类型，结构清晰明了，解析也方便快捷，大有取代xml的趋势
    语法：
        Structure通过空格来展示；Sequence里的项用"-"来代表；Map里的键值对用":"分隔
    eg:
        name: John Smith
        age: 37
        spouse:
            name: Jane Smith
            age: 25
        children:
            -   name: Jimmy Smith
                age: 15
            -   name: Jenny Smith
                age: 12

    #John今年37岁，有一个幸福的四口之家。两个孩子Jimmy 和Jenny活泼可爱。妻子Jane年轻美貌。

    ##Python中解析yaml需要使用PyYAML，http://pypi.python.org/pypi/PyYAML
    '''

    ## file:config.yaml
    company: HuayeLongtu
    addr: Dongguan Nancheng
    tel: 0769-22410321

    database:
        - name: SQLServer
          user: sa
          password: test
        - name: Access
        - name: Oracle
          user: sys
          password: huaye

    ## pyfile
    import yaml
    from pprint import pprint

    stream = file('config.yaml', 'r')
    dict = yaml.load(stream)

    pprint(dict)
    '''
    {'addr': 'Dongguan Nancheng',
     'company': 'HuayeLongtu',
     'database': [{'name': 'SQLServer', 'password': 'test', 'user': 'sa'},
                  {'name': 'Access'},
                  {'name': 'Oracle', 'password': 'huaye', 'user': 'sys'}],
     'tel': '0769-22410321'}
    '''

    sqlserveruser = dict['database'][0]['user']
    comtel = dict['tel']

    ## another example
    '''
    ConnString:
      MSSQL:
        driver: SQL Server # under SQLserver 2000 & 2005
        # driver: SQL Native Client # for SQL Server 2005 features
        # driver: SQL Server Native Client 10.0 # for SQLServer 2008 features
        server: 192.168.9.246
        database: Google
        uid: sa
        pwd: xiaoping
        # DRIVER={SQL Server};SERVER=localhost;UID=sa;PWD=psword

      Access:
        driver: Microsoft Access Driver (*.mdb)
        # driver: Microsoft Access Driver (*.mdb, *.accdb) # support for 2007
        DBQ: D:\Tempdata\Data.mdb
        # DRIVER={Microsoft Access Driver (*.mdb)};DBQ=D:\Tempdata\Data.mdb

      Excel:
        driver: Microsoft Excel Driver (*.xls)
        DBQ: D:\Tempdata\Data.xls
        READONLY: TRUE
        # DRIVER={Microsoft Excel Driver (*.xls)};DBQ=D:\Tempdata\Data.xls

    Project:
      name: 东莞
      type: MSSQL
      table: Dongguan2Google

    '''

25. XML
    # TODO:使用lxml模块可以解析xml和html
    pass
26. xml2dict
    '''http://code.google.com/p/xml2dict/
       这个库不错，将xml解析为dict，更绝的是可以直接用“.”来逐层访问节点
       下面有附源代码
    '''
    from xml2dict import XML2Dict

    s = """<?xml version="1.0" encoding="utf-8" ?>
    <result>
        <count n="1">10</count>
        <data><id>491691</id><name>test</name></data>
        <data><id>491692</id><name>test2</name></data>
        <data><id>503938</id><name>hello, world</name></data>
    </result>"""

    xml = XML2Dict()
    r = xml.fromstring(s)
    from pprint import pprint
    pprint(r)  # 打印机模式的输出，很结构化
    print r.result.count.value
    print r.result.count.n  # 这里就是绝妙之处

    for data in r.result.data:
        print data.id, data.name

    ##同样解析XML文件也很方便
    pprint(xml.parse('a.xml'))

    # {{{
    ## 附：xml2dict.py
    """
    Thunder Chen<nkchenz@gmail.com> 2007.9.1
    """
    try:
        import xml.etree.ElementTree as ET
    except:
        import cElementTree as ET # for 2.4

    from object_dict import object_dict
    import re

    class XML2Dict(object):

        def __init__(self):
            pass

        def _parse_node(self, node):
            node_tree = object_dict()
            # Save attrs and text, hope there will not be a child with same name
            if node.text:
                node_tree.value = node.text
            for (k,v) in node.attrib.items():
                k,v = self._namespace_split(k, object_dict({'value':v}))
                node_tree[k] = v
            #Save childrens
            for child in node.getchildren():
                tag, tree = self._namespace_split(child.tag, self._parse_node(child))
                if  tag not in node_tree: # the first time, so store it in dict
                    node_tree[tag] = tree
                    continue
                old = node_tree[tag]
                if not isinstance(old, list):
                    node_tree.pop(tag)
                    node_tree[tag] = [old] # multi times, so change old dict to a list
                node_tree[tag].append(tree) # add the new one

            return  node_tree

        def _namespace_split(self, tag, value):
            """
               Split the tag  '{http://cs.sfsu.edu/csc867/myscheduler}patients'
                 ns = http://cs.sfsu.edu/csc867/myscheduler
                 name = patients
            """
            result = re.compile("\{(.*)\}(.*)").search(tag)
            if result:
                print tag
                value.namespace, tag = result.groups()
            return (tag, value)

        def parse(self, file):
            """parse a xml file to a dict"""
            f = open(file, 'r')
            return self.fromstring(f.read())

        def fromstring(self, s):
            """parse a string"""
            t = ET.fromstring(s)
            root_tag, root_tree = self._namespace_split(t.tag, self._parse_node(t))
            return object_dict({root_tag: root_tree})

    if __name__ == '__main__':
        s = """<?xml version="1.0" encoding="utf-8" ?>
        <result>
            <count n="1">10</count>
            <data><id>491691</id><name>test</name></data>
            <data><id>491692</id><name>test2</name></data>
            <data><id>503938</id><name>hello, world</name></data>
        </result>"""

        xml = XML2Dict()
        r = xml.fromstring(s)
        from pprint import pprint
        pprint(r)
        print r.result.count.value
        print r.result.count.n

        for data in r.result.data:
            print data.id, data.name
        pprint(xml.parse('a'))

    # }}}

    # {{{ object_dict.py
    """
    object_dict
    nkchenz@gmail.com 2007
    Provided as-is; use at your own risk; no warranty; no promises; enjoy!
    """
    class object_dict(dict):
        """object view of dict, you can
        >>> a = object_dict()
        >>> a.fish = 'fish'
        >>> a['fish']
        'fish'
        >>> a['water'] = 'water'
        >>> a.water
        'water'
        >>> a.test = {'value': 1}
        >>> a.test2 = object_dict({'name': 'test2', 'value': 2})
        >>> a.test, a.test2.name, a.test2.value
        (1, 'test2', 2)
        """
        def __init__(self, initd=None):
            if initd is None:
                initd = {}
            dict.__init__(self, initd)

        def __getattr__(self, item):
            d = self.__getitem__(item)
            # if value is the only key in object, you can omit it
            if isinstance(d, dict) and 'value' in d and len(d) == 1:
                return d['value']
            else:
                return d

        def __setattr__(self, item, value):
            self.__setitem__(item, value)

    def _test():
        import doctest
        doctest.testmod()

    if __name__ == "__main__":
        _test()
    # }}}

27. zipfile打包zip文件
    import os
    import zipfile
    """
    zipfile是python里用来做zip格式编码的压缩和解压缩的module，
    zipfile里有两个非常重要的class：ZipFile和ZipInfo。
        ZipFile是主要的类，用来创建和读取zip文件
        ZipInfo是存储的zip文件的每个文件的信息。

    在这里我需要把一个目录压缩，这就要将目录里的文件一个文件一个文件的加入，
    然后在使用zipfile的ZipFile类的时候，再一个一个写入压缩文件。
    """

    filelist = []
    for root, dirs, files in os.walk("D:\\clean"):
        for name in files:
            filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile("d:\\test.zip", "w", zipfile.zlib.DEFLATED)
    # 压缩模式zipfile.DEFLATED 或者 zipfile.ZIP_STORED
    for tar in filelist:
        zf.write(tar)
    zf.close()

    ## example Two
    import zipfile
    import os.path
    import os

    class ZFile(object):
        def __init__(self, filename, mode='r', basedir=''):
            self.filename = filename
            self.mode = mode
            if self.mode in ('w', 'a'):
                self.zfile = zipfile.ZipFile(filename, self.mode, zipfile.ZIP_DEFLATED)
            else:
                self.zfile = zipfile.ZipFile(filename, self.mode)
            self.basedir = basedir
            if not self.basedir:
                self.basedir = os.path.dirname(filename)

        def addfile(self, path, arcname=None):
            path = path.replace('\\', '/')
            if not arcname:
                if path.startswith(self.basedir):
                    arcname = path[len(self.basedir):]
                else:
                    arcname = ''
            self.zfile.write(path, arcname)

        def addfiles(self, paths):
            for path in paths:
                if isinstance(path, tuple):
                    self.addfile(*path)
                else:
                    self.addfile(path)

        def close(self):
            self.zfile.close()

        def extract_to(self, path):
            for p in self.zfile.namelist():
                self.extract(p, path)

        def extract(self, filename, path):
            if not filename.endswith('/'):
                f = os.path.join(path, filename)
                dir = os.path.dirname(f)
                if not os.path.exists(dir):
                    os.makedirs(dir)
                file(f, 'wb').write(self.zfile.read(filename))


    def create(zfile, files):
        z = ZFile(zfile, 'w')
        z.addfiles(files)
        z.close()

    def extract(zfile, path):
        z = ZFile(zfile)
        z.extract_to(path)
        z.close()

28. profile模块计算函数运行时间
    import profile
    def a():
        for i in range(1000):
            pass
    profile.run('a')

29. 邮件处理示例Send_file_by_GMail
    # GSend.py
    from __future__ import with_statement
    import os
    import sys
    from smtplib import SMTP
    from email.MIMEMultipart import MIMEMultipart
    from email.mime.application import MIMEApplication
    import time

    """
    GMail file sender: Send a file use GMail.

    Usage:
        :: GSeng.bat
        @REM put this file in to windows "Send to" folder
        python c:/gsend.py "%1"
        @pause
    然后就是右键->WinRAR->压缩成一个文件->右键->Send to->gsend.bat
    """

    if len(sys.argv) < 2:
        print 'Usage: python %s <file path>' % os.path.basename(sys.argv[0])
        sys.exit(-1)

    config =  {
        'from': 'XXX@gmail.com'
        'to': 'XXX@hotmail.com',
        'subject': '[gsend]Send file %s' % sys.argv[1],
        'file': sys.argv[1],
        'server': 'smtp.gmail.com',
        'port': 587,
        'username': 'XXX@gmail.com',
        'password': 'xxxxxx',
    }

    print 'Preparing...',

    message = MIMEMultipart()
    message['from'] = config['from']
    message['to'] = config['to']
    message['Reply-To'] = config['from']
    message['Subject'] = config['subject']
    message['Date'] = time.ctime(time.time())

    message['X-Priority'] =  '3'
    message['X-MSMail-Priority'] =  'Normal'
    message['X-Mailer'] =  'Microsoft Outlook Express 6.00.2900.2180'
    message['X-MimeOLE'] =  'Produced By Microsoft MimeOLE V6.00.2900.2180'

    with open(config['file'], 'rb') as f:
        file = MIMEApplication(f.read())
    file.add_header('Content-Disposition', 'attachment', filename=os.path.basename(config['file']))
    message.attach(file)

    print 'OK'
    print 'Logging...',

    smtp = SMTP(config['server'], config['port'])
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(config['username'], config['password'])

    print 'OK'
    print 'Sending...',

    smtp.sendmail(config['from'], [config['from'], config['to']], message.as_string())

    print 'OK'

    smtp.close()
    time.sleep(1)

30. thread & threading
    # TODO
    # 多线程编程，见Python核心编程721页

31. with & yield
    ## with
    # with的功能是执行代码清理
    # 它比使用try..finally要清爽很多
    # 在2.6中是预加载模块，在2.5中需要使用import
    #    from __future__ import with_statement

    with open('/etc/passwd', 'r') as f:
        for line in f:
            print line
            ... more processing code ...
    # 这样即便是for了一半就出现异常，file对象也可以正常关闭


    ## yield
    # yield的代码叠代能力不但能打断函数执行还能记下断点处的数据，
    # 下次next书接上回，这正是递归函数需要的。

    # yield 原理
    # 简单说来就是一个生成器
    # 生成器是这样一个函数，它记住上一次返回时在函数体中的位置。
    # 对生成器函数的第二次（或第 n 次）调用跳转至该函数中间，
    # 而上次调用的所有局部变量都保持不变。

    # yield运行机制
    # 当你问生成器要一个数时，生成器会执行，直至出现 yield 语句
    # 生成器把 yield 的参数给你，之后生成器就不会往下继续运行。
    # 当你问他要下一个数时，他会从上次的状态开始运行，
    # 直至出现yield语句，把参数给你，之后停下。
    # 如此反复直至退出函数。

    #生成全排列
    def perm(items, n=None):
        if n is None:
            n = len(items)
        for i in range(len(items)):
            v = items[i:i+1]
            if n == 1:
                yield v
            else:
                rest = items[:i] + items[i+1:]
                for p in perm(rest, n-1):
                    yield v + p

    #生成组合
    def comb(items, n=None):
        if n is None:
            n = len(items)
        for i in range(len(items)):
            v = items[i:i+1]
            if n == 1:
                yield v
            else:
                rest = items[i+1:]
                for c in comb(rest, n-1):
                    yield v + c

    a = perm('abc')
    for b in a:
        print b
        break
    print '-'*20
    for b in a:
        print b

32. SQLAlchemy对象-关系管理器ORMs
    """
    ORM   =   Object   Relational   Mapping
    Object  是指面向对象的
    Relational  是指面向关系数据库
    ORM   就是将关系数据库的数据模型变换映射到面向对象的模型的工具。以方便程序员编程使用.
    """

    # 摘自一个好教程 http://www.javaeye.com/topic/319020
    # 在PythonWin进行的测试

    >>> from sqlalchemy import create_engine
    >>> from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
    >>> engine = create_engine('sqlite:///e://sqlalchemy.db', echo=True)
    # echo表示是否打开sqlalchemy的日志输出，使用的是py的标准日志组件

    >>> metadata = MetaData()  # 这个还不太明白!?
    >>> users_table = Table('user', metadata,
    ... 	Column('id', Integer, primary_key=True),
    ... 	Column('name', String),
    ... 	Column('fullname', String),
    ... 	Column('password', String)
    ... )
    >>> metadata.create_all(engine)  # 发布创建表的声明

    2010-01-13 15:25:22,342 INFO sqlalchemy.engine.base.Engine.0x...8230 PRAGMA table_info("user")
    2010-01-13 15:25:22,358 INFO sqlalchemy.engine.base.Engine.0x...8230 ()
    2010-01-13 15:25:22,358 INFO sqlalchemy.engine.base.Engine.0x...8230
    CREATE TABLE user (
        id INTEGER NOT NULL,
        name VARCHAR,
        fullname VARCHAR,
        password VARCHAR,
        PRIMARY KEY (id)
    )

    2010-01-13 15:25:22,375 INFO sqlalchemy.engine.base.Engine.0x...8230 ()
    2010-01-13 15:25:22,437 INFO sqlalchemy.engine.base.Engine.0x...8230 COMMIT

    # 定义一个用户类
    >>> class User(object):
    ... 	def __init__(self,name,fullname,password):
    ... 		self.name = name
    ... 		self.fullname = fullname
    ... 		self.password = password
    ... 	def __repr__(self):
    ... 		return "<User('%s','%s','%s')>" % (self.name,self.fullname,self.password)
    ...

    # 设置映射
    >>> from sqlalchemy.orm import mapper
    >>> mapper(User, users_table)
    <Mapper at 0x1378810; User>

    # 映射好以后就可以创建和检查用户对象
    >>> ed_user = User('ed','Ed Jones', 'edpwd')
    >>> ed_user.name
    'ed'
    >>> ed_user.password
    'edpwd'
    >>> str(ed_user.id)
    'None'

    ## 一次性创建表、对象和映射
    >>> from sqlalchemy.ext.declarative import declarative_base
    >>> Base = declarative_base()
    >>> class User2(Base):
    ... 	__tablename__ = 'user'
    ... 	id = Column(Integer, primary_key=True)
    ... 	name = Column(String)
    ... 	fullname = Column(String)
    ... 	password = Column(String)
    ... 	def __init__(self,name,fullname,password):
    ... 		self.name = name
    ... 		self.fullname = fullname
    ... 		self.password = password
    ... 	def __repr__(self):
    ... 		return "<User('%s','%s','%s')>" % (self.name, self.fullname, self.password)
    ...
    # 上面的declarative_base()功能实现了一个新的类Base， User继承Base

    # 创建Session，orm操作数据库采用的是session
    >>> from sqlalchemy.orm import sessionmaker
    >>> Session = sessionmaker(bind=engine)  # 绑定session到engine数据库

    >>> lee = User2('lee','Bruce Lee', 'xiaoping')  # 创建一条记录

    >>> session = Session()  # 实例
    >>> session.add(lee)  # 添加记录到engine中
    >>> session.commit()  # 记住要commit
    2010-01-13 16:07:56,030 INFO sqlalchemy.engine.base.Engine.0x...8230 BEGIN
    2010-01-13 16:07:56,030 INFO sqlalchemy.engine.base.Engine.0x...8230 INSERT INTO user (name, fullname, password) VALUES (?, ?, ?)
    2010-01-13 16:07:56,046 INFO sqlalchemy.engine.base.Engine.0x...8230 ['lee', 'Bruce Lee', 'xiaoping']
    2010-01-13 16:07:56,046 INFO sqlalchemy.engine.base.Engine.0x...8230 COMMIT

    # 查询
    >>> u = session.query(User2).filter_by(name='lee').first()
    2010-01-13 16:11:45,405 INFO sqlalchemy.engine.base.Engine.0x...8230 BEGIN
    2010-01-13 16:11:45,405 INFO sqlalchemy.engine.base.Engine.0x...8230 SELECT user.id AS user_id, user.name AS user_name, user.fullname AS user_fullname, user.password AS user_password
    FROM user
    WHERE user.name = ?
     LIMIT 1 OFFSET 0
    2010-01-13 16:11:45,421 INFO sqlalchemy.engine.base.Engine.0x...8230 ['lee']
    >>> u
    <__main__.User3 object at 0x01B255D0>
    >>> u.fullname
    u'Bruce Lee'
    >>> u.password
    u'xiaoping'

    # 更新
    >>> u.password = 'calin'
    >>> session.commit()
    2010-01-13 16:13:39,171 INFO sqlalchemy.engine.base.Engine.0x...8230 UPDATE user SET password=? WHERE user.id = ?
    2010-01-13 16:13:39,171 INFO sqlalchemy.engine.base.Engine.0x...8230 ['calin', 1]
    2010-01-13 16:13:39,187 INFO sqlalchemy.engine.base.Engine.0x...8230 COMMIT

    # 删除
    >>> u = session.query(User3).filter_by(name='lee').first()
    2010-01-13 16:16:10,953 INFO sqlalchemy.engine.base.Engine.0x...8230 BEGIN
    2010-01-13 16:16:10,953 INFO sqlalchemy.engine.base.Engine.0x...8230 SELECT user.id AS user_id, user.name AS user_name, user.fullname AS user_fullname, user.password AS user_password
    FROM user
    WHERE user.name = ?
     LIMIT 1 OFFSET 0
    2010-01-13 16:16:10,953 INFO sqlalchemy.engine.base.Engine.0x...8230 ['lee']

    >>> session.delete(u)

    >>> session.commit()
    2010-01-13 16:16:39,967 INFO sqlalchemy.engine.base.Engine.0x...8230 DELETE FROM user WHERE user.id = ?
    2010-01-13 16:16:39,967 INFO sqlalchemy.engine.base.Engine.0x...8230 [1]
    2010-01-13 16:16:39,967 INFO sqlalchemy.engine.base.Engine.0x...8230 COMMIT

33. 使用get setattr getattr
    当需要取值时最好使用这些方法，可以在没有对应属性时取默认值

    # get 用于字典取值
    >>> dt = {'a': 'apple', 'b': 'blackberry', 'n': 'nokia'}
    >>> dt['c']
    Traceback (most recent call last):
      File "<interactive input>", line 1, in <module>
    KeyError: 'c'
    >>> dt.get('c', 'none...')
    'none...'
    >>> dt.get('a', 'none...')
    'apple'

    # getattr 取对象的属性值
    # getattr(object, name[, default])  <=> object.name
    >>> class c:
    ... 	a = 'apple'
    ... 	b = 'blackberry'
    ...
    >>> getattr(c, 'a', 'none...')
    'apple'
    >>> getattr(c, 'c', 'none...')
    'none...'

    # hasattr(object, name)  -> boolen

    # setattr 设置对象属性值
    # setattr(object, name, value)
    >>> setattr(c, 'a', 'app')
    >>> c.a
    'app'
    >>> setattr(c, 'n', 'nokia')
    >>> c.n
    'nokia'

34. exec & eval_r & execfile & compile
    #2012/5/16
    #via: http://blog.sina.com.cn/s/blog_76e94d210100w1bl.html

    exec语句用来执行储存在字符串或文件中的Python语句。
        例如，我们可以在运行时生成一个包含Python代码的字符串，然后使用exec语句执行这些语句。
        >>> exec 'print "Hello World"'
        Hello World

    eval_r语句用来计算存储在字符串中的有效Python表达式。下面是一个简单的例子。
        >>> eval_r('2*3')
        6

    eval_r(str [ globals [ locals ]])函数将字符串str当成有效python表达式来求值，并返回计算结果。

    同样地, exec语句将字符串str当成有效Python代码来执行.提供给exec的代码的名称空间和exec语句的名称空间相同.


    execfile(filename [,globals [,locals ]])函数可以用来执行一个文件,看下面的例子:
        >>> eval_r('3+4')
        7
        >>> exec 'a=100' 
        >>> a 
        100 
        >>> execfile(r'd:\code\ex\test.py')
        hello world!
        >>>

    默认的，eval_r(),exec,execfile()所运行的代码都位于当前的名字空间中. 
    eval_r(), exec 和 execfile()函数也可以接受一个或两个可选字典参数作为代码执行的全局名字空间和局部名字空间. 例如:
        1  globals = {'x': 7,
        2             'y': 10,
        3             'birds': ['Parrot', 'Swallow', 'Albatross']
        4            }
        5  locals = { }
        6  
        7  # 将上边的字典作为全局和局部名称空间 
        8  a = eval("3*x + 4*y", globals, locals) 
        9  exec "for b in birds: print b" in globals, locals # 注意这里的语法 
        10 execfile("foo.py", globals, locals)
    如果你省略了一个或者两个名称空间参数,那么当前的全局和局部名称空间就被使用.
    如果一个函数体内嵌嵌套函数或lambda匿名函数时,同时又在函数主体中使用exec或execfile()函数时，
    由于牵到嵌套作用域，会引发一个SyntaxError异常.

    注意例子中exec语句的用法和eval_r(), execfile()是不一样的. 
    exec是一个语句(就象print或while), 而eval_r()和execfile()则是内建函数.
    exec(str) 这种形式也被接受，但是它没有返回值。

    当一个字符串被exec,eval_r(),或execfile()执行时,解释器会先将它们编译为字节代码，然后再执行.
    这个过程比较耗时,所以如果需要对某段代码执行很多次时,最好还是对该代码先进行预编译,
    这样就不需要每次都编译一遍代码，可以有效提高程序的执行效率。

    compile(str ,filename ,kind )函数将一个字符串编译为字节代码, 
    str是将要被编译的字符串, 
    filename是定义该字符串变量的文件，
    kind参数指定了代码被编译的类型-- 'single'指单个语句, 'exec'指多个语句, 'eval'指一个表达式. 

    compile()函数返回一个代码对象，该对象当然也可以被传递给eval_r()函数和exec语句来执行,例如:
        >>> str = 'for i in range(0, 10): print i'
        >>> c = compile(str,'','exec')      # 编译为字节代码对象 
        >>> exec c        # 执行
        0
        1
        2
        3
        4
        5
        6
        7
        8
        9
        >>> str2 = '3*6 + 4*8'
        >>> c2 = compile(str2,'','eval')        # 编译为表达式 
        >>> result = eval_r(c2)                 # 执行
        >>> result
        50
        >>>

35. 



#
781页
# TODO: httplib,urllib和urllib2

'''
    python模块之---- urllib2模块详解
    http://blog.alexa-pro.cn/?p=195

    简介：
    urllib2是python的一个获取url（Uniform Resource Locators，统一资源定址器）的模块。它用urlopen函数的形式提供了一个非常简洁的接口。这使得用各种各样的协议获取url成为可能。它同时也提供了一个稍微复杂的接口来处理常见的状况-如基本的认证，cookies，代理，等等。这些都是由叫做opener和handler的对象来处理的。

    以下是获取url最简单的方式：

    import urllib2
    response = urllib2.urlopen('http://python.org/')
    html = response.read()

    许多urlib2的使用都是如此简单（注意我们本来也可以用一个以”ftp:”"file：”等开头的url取代”HTTP”开头的url）.然而，这篇教程的目的是解释关于HTTP更复杂的情形。HTTP建基于请求和回应（requests &responses ）-客户端制造请求服务器返回回应。urlib2用代 表了你正在请求的HTTP request的Request对象反映了这些。用它最简单的形式，你建立了一个Request对象来明确指明你想要获取的url。调用urlopen函数对请求的url返回一个respons对象。这个respons是一个像file的对象，这意味着你能用.read()函数操作这个respon对象：

    import urllib2

    req = urllib2.Request('http://www.voidspace.org.uk')
    response = urllib2.urlopen(req)
    the_page = response.read()

    注意urlib2利用了同样的Request接口来处理所有的url协议。例如，你可以像这样请求一个ftpRequest：

    req = urllib2.Request('ftp://example.com/')

    对于HTTP，Request对象允许你做两件额外的事：第一，你可以向服务器发送数据。第二，你可以向服务器发送额外的信息（metadata），这些信息可以是关于数据本身的，或者是关于这个请求本身的–这些信息被当作HTTP头发送。让我们依次看一下这些。

    数据：
    有时你想向一个URL发送数据（通常这些数据是代表一些CGI脚本或者其他的web应用）。对于HTTP，这通常叫做一个Post。当你发送一个你在网上填的form（表单）时，这通常是你的浏览器所做的。并不是所有的Post请求都来自HTML表单，这些数据需要被以标准的方式encode，然后作为一个数据参数传送给Request对象。Encoding是在urlib中完成的，而不是在urlib2中完成的。

    import urllib
    import urllib2

    url = 'http://www.someserver.com/cgi-bin/register.cgi'
    values = {'name' : 'Michael Foord',
    'location' : 'Northampton',
    'language' : 'Python' }

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()

    如果你不传送数据参数，urlib2使用了一个GET请求。一个GET请求和POST请求的不同之处在于POST请求通常具有边界效应：它们以某种方式改变系统的状态。（例如，通过网页设置一条指令运送一英担罐装牛肉到你家。）虽然HTTP标准清楚的说明Post经常产生边界效应，而get从不产生边界效应，但没有什么能阻止一个get请求产生边界效应，或一个Post请求没有任何边界效应。数据也能被url自己加密（Encoding）然后通过一个get请求发送出去。

    这通过以下实现：
    >>> import urllib2
    >>> import urllib
    >>> data = {}
    >>> data['name'] = 'Somebody Here'
    >>> data['location'] = 'Northampton'
    >>> data['language'] = 'Python'
    >>> url_values = urllib.urlencode(data)
    >>> print url_values
    name=Somebody+Here&language=Python&location=Northampton
    >>> url = 'http://www.example.com/example.cgi'
    >>> full_url = url + '?' + url_values
    >>> data = urllib2.open(full_url)

    头：
    我们将会在这里讨论一个特殊的HTTP头，来阐释怎么向你的HTTP请求中加入头。
    有一些网站不希望被某些程序浏览或者针对不同的浏览器返回不同的版本。默认情况下，urlib2把自己识别为Python-urllib/x.y（这里的 xy是python发行版的主要或次要的版本号，如， Python-urllib/2.5），这些也许会混淆站点，或者完全不工作。浏览器区别自身的方式是通过User-Agent头。当你建立一个 Request对象时，你可以加入一个头字典。接下来的这个例子和上面的请求一样，不过它把自己定义为IE的一个版本。

    import urllib
    import urllib2

    url = 'http://www.someserver.com/cgi-bin/register.cgi'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    values = {'name' : 'Michael Foord',
    'location' : 'Northampton',
    'language' : 'Python' }
    headers = { 'User-Agent' : user_agent }

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    the_page = response.read()

    Respons同样有两种有用的方法。当我们出差错之后，看一下关于info and geturl的部分。

    异常处理：

    不能处理一个respons时，urlopen抛出一个urlerror（虽然像平常一样对于python APIs，内建异常如，ValueError, TypeError 等也会被抛出。）
    HTTPerror是HTTP URL在特别的情况下被抛出的URLError的一个子类。
    urlerror：
    通常，urlerror被抛出是因为没有网络连接（没有至特定服务器的连接）或者特定的服务器不存在。在这种情况下，含有reason属性的异常将被抛出，以一种包含错误代码和文本错误信息的tuple形式。

    e.g.
    >>> req = urllib2.Request('http://www.pretend_server.org')
    >>> try: urllib2.urlopen(req)
    >>> except URLError, e:
    >>> print e.reason
    >>>
    (4, 'getaddrinfo failed')

    当一个错误被抛出的时候，服务器返回一个HTTP错误代码和一个错误页。你可以使用返回的HTTP错误示例。这意味着它不但具有code属性，而且同时具有read，geturl，和info，methods属性。
    >>> req = urllib2.Request('http://www.python.org/fish.html')
    >>> try:
    >>> urllib2.urlopen(req)
    >>> except URLError, e:
    >>>     print e.code
    >>> print e.read()
    >>>
    404...... etc

    容错：
    如果你准备处理HTTP错误和URL错误这里有两种基本的方法，我更倾向于后一种：

    1.
    from urllib2 import Request, urlopen, URLError, HTTPError
    req = Request(someurl)
    try:
    response = urlopen(req)
    except HTTPError, e:
    print 'The server couldn\'t fulfill the request.'
    print 'Error code: ', e.code
    except URLError, e:
    print 'We failed to reach a server.'
    print 'Reason: ', e.reason
    else:
    # everything is fine

    注意:HTTP错误异常必须在前面，否则URL错误也会捕获一个HTTP错误。
    2
    from urllib2 import Request, urlopen, URLError
    req = Request(someurl)
    try:
    response = urlopen(req)
    except URLError, e:
    if hasattr(e, 'reason'):
    print 'We failed to reach a server.'
    print 'Reason: ', e.reason
    elif hasattr(e, 'code'):
    print 'The server couldn\'t fulfill the request.'
    print 'Error code: ', e.code
    else:
    # everything is fine

    注意:URL错误是IO错误异常的一个子类。这意味着你能避免引入（import）URL错误而使用：

    from urllib2 import Request, urlopen
    req = Request(someurl)
    try:
    response = urlopen(req)
    except IOError, e:
    if hasattr(e, 'reason'):
    print 'We failed to reach a server.'
    print 'Reason: ', e.reason
    elif hasattr(e, 'code'):
    print 'The server couldn\'t fulfill the request.'
    print 'Error code: ', e.code
    else:
    # everything is fine

    极少数环境下，urllib2能够抛出socket.error.

    INFO and GETURL
    urlopen返回的response（或者HTTP错误实例）有两个有用的方法：info和geturl。

    geturl–它返回被获取网页的真正的url。这是很有用的，因为urlopen（或使用的opener对象）也许会伴随一个重定向。
    获取的网页url也许和要求的网页url不一样。

    info–它返回一个像字典的对象来描述获取的网页，尤其是服务器发送的头。它现在一般是httplib.HTTPMessage的一个实例。
    典型的头包含'Content-length', 'Content-type', 等等。看一下Quick Reference to HTTP Headers中，HTTP头列表，还有
    关于他们简单的解释和使用方法。
    Openers 和Handlers
    当你获取一个URL时，你使用一个opener（一个可能以一个比较迷糊名字命名的实例–urllib2.OpenerDirector）。正常情况下
    我们一直使用默认的opener，通过urlopen，但你也可以创建自定义的openers。opener使用操作器（handlers）。所有的重活都交给这些handlers来做。每一个handler知道
    怎么打开url以一种独特的url协议（http，ftp等等），或者怎么处理打开url的某些方面，如，HTTP重定向，或者HTTP cookie。

    你将会创建openers如果你想要用安装特别的handlers获取url，例如，获取一个处理cookie的opener，或者一个不处理重定向的opener。

    枚举一个OpenerDirector，然后多次调用.add_handler(some_handler_instance)来创建一个opener。
    或者，你可以用build_opener，这是一个很方便的创建opener对象的函数，它只有一个函数调用。build_opener默认会加入许多
    handlers，但是提供了一个快速的方法添加更多东西和/或使默认的handler失效。
    其他你想要的handlers能够处理代理，authentication和其他平常但是又有些特殊的情况。
    install_opener能被用于创建一个opener对象，（全局）默认的opener。这意味着调用urlopen将会用到你刚安装的opener。
    opener对象有一个open方法，它可以被直接调用来获取url以一种和urlopen函数同样的方式：没有必要调用install_opener，除非是为了方便。

    Basic Authentication：（基本验证）

    为了解释创建和安装一个handler，我们将会使用 HTTPBasicAuthHandler。更多关于这个东西的内容和详细讨论—包括一个 Basic Authentication如何工作的解说–参见 Basic Authentication Tutorial.

    当需要Authentication的时候，服务器发送一个头（同时还有401代码）请求Authentication。它详细指明了一个Authentication和一个域。这个头看起来像：

    Www-authenticate: SCHEME realm=”REALM”.
    e.g.
    Www-authenticate: Basic realm=”cPanel Users”

    客户端然后就会用包含在头中的正确的帐户和密码重新请求这个域。这是”基本验证”。为了简化这个过程，我们可以创建一个
    HTTPBasicAuthHandler和opener的实例来使用这个handler。
    HTTPBasicAuthHandler用一个叫做密码管理的对象来处理url和用户名和密码的域的映射。如果你知道域是什么（从服务器发送的authentication
    头中），那你就可以使用一个HTTPPasswordMgr。多数情况下人们不在乎域是什么。那样使用HTTPPasswordMgrWithDefaultRealm就很方便。它
    允许你为一个url具体指定用户名和密码。这将会在你没有为一个特殊的域提供一个可供选择的密码锁时提供给你。我们通过提供None作为add_password方法域的参数指出
    这一点。
    最高级别的url是需要authentication的第一个url。比你传递给.add_password()的url更深的url同样也会匹配。

    # create a password manager
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    # Add the username and password.
    # If we knew the realm, we could use it instead of “None“.
    top_level_url = “http://example.com/foo/”
    password_mgr.add_password(None, top_level_url, username, password)

    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    # create “opener” (OpenerDirector instance)
    opener = urllib2.build_opener(handler)
    # use the opener to fetch a URL
    opener.open(a_url)
    # Install the opener.
    # Now all calls to urllib2.urlopen use our opener.
    urllib2.install_opener(opener)

    注意:在以上的示例中我们只给build_opener提供了HTTPBasicAuthHandler。默认opener有对普通情况的操作器（handlers）- ProxyHandler, UnknownHandler, HTTPHandler, HTTPDefaultErrorHandler, HTTPRedirectHandler, FTPHandler, FileHandler, HTTPErrorProcessor.
    高级别url实际上是一个完整的url（包括http:协议组件和主机名可选的端口号），如”http://example.com”或者是一个授权（同样，主机名，可选的端口号）
    如”"example.com” 或 “example.com:8080″（后一个示例包含了一个端口号）。授权，如果被呈现，一定不能包含用户信息-如”oe@password:example.com”
    是不正确的、
    代理：
    urllib2将会自动检测你的代理设置并使用它们。这是通过 ProxyHandler实现的，它是操作器链的一部分。正常情况下，这是个好东西，但是也有它不那么有用的偶然情况。
    一个做这些的方法是安装我们自己的ProxyHandler，不用任何定义任何代理。使用一个和建立Basic Authentication操作器相似的步骤可以实现：

    >>> proxy_support = urllib2.ProxyHandler({})
    >>> opener = urllib2.build_opener(proxy_support)
    >>> urllib2.install_opener(opener)
    注意：
    目前urllib2不支持通过代理获取HTTPs位置。这是一个问题。
    sockets和layers
    python支持获取层叠的网页的源码。urllib2使用httplib library，而httplib library反过来使用socket library。
    对于python2.3你可以指明一个socket应该在超时之前等待response多久。这在这些不得不获取网页的应用中很有用。默认socket模块没有超时而且能够挂起。
    目前，socket超时在urllib2或者httplib水平中不可见。然而，你可以全局地为所有socket设置默认的超时。

    import socket
    import urllib2
    # timeout in seconds
    timeout = 10
    socket.setdefaulttimeout(timeout)
    # this call to urllib2.urlopen now uses the default timeout
    # we have set in the socket module
    req = urllib2.Request('http://www.voidspace.org.uk')
    response = urllib2.urlopen(req)
'''


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


98. Django杂项
    98.1 django怎么来执行数据库的in操作呢？
        有2个方法可以很好的实现：
            1直接用filter语句里的方法来实现
            2用到extra方法

        比如我们要执行：select * from table where id in (3, 4, 5, 20)用上面2个方法分别怎么操作呢
        django filter:
        Blog.objects.filter(pk__in=[3,4,5,20])
        django extra:
        Blog.objects.extra(where=['id IN (3, 4, 5, 20)'])

        这2个方法实现的django in效果都差不多，就看你喜欢用什么方法了

99. 其他杂项代码

    ## 主板响一下
    print chr(7)
    print '\a'
    print '\007'


    ## Windows下查看本地IP地址
    import socket
    print socket.gethostbyname(socket.gethostname())

    uuid.uuid1().hex[-12:] # 根据uuid1的机制，相当于查看本机的MAC地址.


    ## 一个条件判断语句
    "X if C else Y"


    ## 九九乘法表
    print "".join([('%s*%s=%s%s' % (y,x,x*y,'\n' if x==y else '\t')) for x in range(1,10) for y in range(1,10) if x >= y])
    '''输出：
    1*1=1
    1*2=2   2*2=4
    1*3=3   2*3=6   3*3=9
    1*4=4   2*4=8   3*4=12  4*4=16
    1*5=5   2*5=10  3*5=15  4*5=20  5*5=25
    1*6=6   2*6=12  3*6=18  4*6=24  5*6=30  6*6=36
    1*7=7   2*7=14  3*7=21  4*7=28  5*7=35  6*7=42  7*7=49
    1*8=8   2*8=16  3*8=24  4*8=32  5*8=40  6*8=48  7*8=56  8*8=64
    1*9=9   2*9=18  3*9=27  4*9=36  5*9=45  6*9=54  7*9=63  8*9=72  9*9=81
    '''


    ## 打开外部网页
    import webbrowser
    webbrowser.open('http://www.google.com')
    import os
    os.system('start http://www.google.com')


    ## urllib超时问题解决
    import socket
    socket.setdefaulttimeout(30)


    ## shutil模块
    shutil.copyfile(src, dst)  # 拷贝文件
    shutil.copytree(srcDir, dstDir)  # 拷贝目录


    ## 编码问题
    # by jhuangjiahua@gmail.com in python-cn
    给妳一招，但凡看到类似
    'ascii' codec can't decode byte OOXX JJYY
    就在程序头部加上
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')


    ##web.py设置404和500
    # 404
    def notfound():
        return web.notfound("Sorry, the page you were looking for was not found.")
        # You can use template result like below, either is ok:
        #return web.notfound(render.notfound())
        #return web.notfound(str(render.notfound()))
    app.notfound = notfound

    # 500
    def internalerror():
        return web.internalerror("Bad, bad server. No donut for you.")
    app.internalerror = internalerror


    ## unicode输出汉字
    s = u'\u5434\u9896'
    print s  # 输出汉字
    s2 = """u'\u5434\u9896'"""
    print eval(s2)   # 输出汉字


    ## try..except
    try:
        print 'Synchronizing with Google Code'
        from syncr.app.googlecode import GoogleCodeSyncr
        f = GoogleCodeSyncr()
        f.syncSvnChanges()
        f.syncProjectDownloads()
        print 'Done.'
    except Exception, e:
        print 'Sync Error: %s' % (e)

100. 古典算法
    100.1 生死兔子
        问题：
            有一对兔子，从出生后第3个月起每个月都生一对兔子，小兔子长到第三个月
            后每个月又生一对兔子，假如兔子都不死，问每个月的兔子总数为多少？
        分析：
            典型的斐波那契函数问题
            为了符合函数式，这里把一对兔子看作1来分析，最后得出结果为兔子的对数
            第一个月：f1 = 1
            第二个月：f2 = 1
            第三个月：f3 = f1 + f2 = 1 + 1 = 2
            第四个月：f4 = f2 + f3 = 1 + 2 = 3
            第五个月：f5 = f3 + f4 = 2 + 3 = 5
            。。。。
            第N个月：fn = f(n-1) + f(n-2)

        伪码：
            f1 = 1, f2 = 2
            if n <3:
                fn = 1
            else:
                fn = f(n-1)+f(n-2)

        算法1：
            def rabbit(n):
                if n>=3:
                    return rabbit(n-1) + rabbit(n-2)
                else:
                    return 1

            def main():
                n = raw_input("which mouth do you want see? ->")
                print rabbit(int(n)) * 2

        算法2：
            n = raw_input("which mouth do you want see? ->")
            f1 = f2 = 1
            for i in range(1,n+1):
                if i%2 == 0:
                    print f1, f2
                else:
                    print f1
                f1 = f1 + f2
                f2 = f1 + f2











