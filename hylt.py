#!/usr/bin/python
# -*- coding:utf-8 -*-
# 文件: hylt.py
# 作者：李晓平
# 时间：2009-9-4
# 版本：随机记录，不做版本控制
# 用途：记录点点滴滴
# 授权：自用
#
'''
   工作中实际用到的运行于生产的代码模块
   目前包含了公司所有工作用模块和其他好的自用模块
'''


#------------------------------------------------------------------------------
#!/usr/bin/python
# -*- coding:utf-8 -*-
# get_file_info.py

'''
   在cmd界面下获取要处理文件的名称、路径、结果文件等参数
'''


class FileInfo:
    """get the input file's name,path,and ect. Like this:
    e.g. "E:\SpeakOut_Release1.0\HiHoney.pdb" can ruturn the following message
    file:	E:\SpeakOut_Release1.0\HiHoney.pdb
    name:	HiHoney.pdb
    path:	E:\SpeakOut_Release1.0
    type:	pdb
    log:	E:\SpeakOut_Release1.0\HiHoney_log.txt
    """
    name = ""
    path = ""
    type = ""
    log = ""

    def __init__(self, file):
        self.file = file
        list_1 = file.rsplit("\\", 1)
        # ['d:\user\mydoc', 'readme.txt']
        FileInfo.name = list_1[1]
        FileInfo.path = list_1[0]
        list_2 = file.rsplit(".", 1)
        # ['d:\user\mydoc\readme', 'txt']
        FileInfo.type = list_2[1]
        FileInfo.log = list_2[0] + "_log.txt"


def Get_Info():
    fileobject = raw_input("""
          |----------------------------------------------------------|
          |  Please type a file here by use the full path and name   |
          |  or just drag file in,                                   |
          |  press enter and then the process will run.              |
          |        e.g. \"d:\\user\\mydoc\\readme.txt\"                   |
          |----------------------------------------------------------|

>>>""")
    info = FileInfo(fileobject)
    return info


def Pause():
    """just print a message for pause the cmd cosole."""
    print "\n\nDone, you can view log to check the result."
    print "press enter to leave..."
    raw_input()

if __name__ == "__main__":
    Get_Info()


#------------------------------------------------------------------------------
# -*- encoding:utf-8 -*-
# Check_Photo_Name.py
# 2009-5-18
"""
根据Google项目合作问题而制作，检查照片名称中的非法字符，
使用正则表达式的\w进行验证

like “13THIRD111040210442照片 119.JPG” is illegal
作为模块使用时，检查目标为csv照片库文件，直接从生产库中的表poi_photo导出，
8个字段形式为：
PROJECT_ID,PHOTO_ID,PHOTO_NAME,POI_NUM,POI_SUBNUM,CELL_ID_LNG,CELL_ID_LAT,PHOTO_TYPE
结果输出为POICODE \t PHOTO_NAME
usage:
    CheckPhoto(csv_photo_file, output_log_file)
"""

import csv
import re
import get_file_info


def CheckPhoto(file, log):
    log = open(log, 'w')
    reader = csv.reader(open(file))

    for row in reader:
        if re.match(r'^\w+\.((jpg)|(JPG))$', row[2]):
            pass
        else:
            poicode = row[6] + '/' + row[5] + '_' + row[3] + '/' + row[4]
            log.write(poicode + '\t' + row[2] + '\n')

    log.close()

if __name__ == "__main__":
    p = get_file_info.Get_Info()
    CheckPhoto(p.file, p.log)
    get_file_info.Pause()


#------------------------------------------------------------------------------
# coding:utf-8
# file:mapenjoy_json.py
# date:2009-5-19
"""
天目接口测试
BSEI_门址查询接口：
	1 介绍
	BSEIGC门址查询接口是个WEB Server服务，它通过http对外提供服务，用户输入地址和(或)城市名就可以查询该地址的经纬度。
	2 操作
	2.1 请求
	用户通过url请求：例如：
	http://t.mapenjoy.com/bseigc?Geocoding&address=白云路6&city=广州
	Get发送参数：
		查询标志：必须为Geocoding，必须放在最开始处。
		address：查询地址 ，不能为空。
		city: 查询城市，可选，未指明城市则返回所有城市的。
	2.2 正确返回
	返回为JSON格式的数据，例如：
	window._OLR={c:[{id:"208046",di:"广东省广州市越秀区",add:"白云路",dn:"6",lo:113281281,la:23116631,mp:100},{id:"304999",di:"广东省广州市越秀区",add:"白云路",dn:"6号",lo:113275870,la:23119361,mp:100}],err:""}
	各个字段含义如下：
	id：结果编号。
	di：行政区划。
	add：街道。
	dn：门牌号。
	lo，la：经纬度。NTU单位。
	mp：匹配度。
	2.3 错误返回。
		错误原因返回结果中均有说明。例如：window._OLR={c:[],"err":"地址参数为空"}
测试过程：
	由于天目公司WebServer提供的是http服务(非soap)，可以使用Python的httplib和urllib模块进行数据发送和接收。
Bug：
	程序运行一定量后自动退出，添加了time.sleep照旧，不知道是否要用spool技术
"""

import csv,httplib,urllib,time
from get_file_info import Get_Info,Pause

def Run_JSON(file, log):
	log = open(log, "w")
	sourcedata = csv.reader(open(file))
	strURLHead = "http://t.mapenjoy.com/bseigc?Geocoding&address="

	for row in sourcedata:
		strURL = strURLHead + row[4] + row[5]
		feeddata = urllib.urlopen(strURL).read()
		log.write(",".join(row))
		log.write(',"' + feeddata + '"')
		log.write("\n")

	log.close()

def main():
	p = Get_Info()
	Run_JSON(p.file, p.log)
	Pause()

if __name__ == "__main__":
	main()

#### 读取结果
import urllib
import simplejson as json

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


#------------------------------------------------------------------------------
#!/usr/bin/python
# -*- coding:utf-8 -*-
# file:Union_BusLine.py
# date:2009-6-2
# author:Lee

"""
从南京项目开始，公司的生产规范中关于公交线路的录入方法发送了改变，将原来的一条公交线
按途径线路进行拆分录入。这样做一是便于线路的应用，二是避免单条数据造成的照片过多
名称超过字段限制的情况。

由于提交Google数据的需求，公交线路仍需要按之前的标准进行处理。
处理思想：将形同5/2_233/1、5/2_233/2、5/2_233/3合并到5/2_233/0中
由于频繁检索归类数据，需要采用SQLite进行处理，

原始表结构是从csv文件导入(UTF-8编码)
CSV文件格式：POICode,BusLine,Photo
原始提供数据中不包含标题且公交和照片多个信息之间应以分号分隔
"""

import sqlite3,csv
from get_file_info import Get_Info,Pause

class UnionBuslines():
    """
       The class of process huaye's busline data
       Attribute:file, path, log, __tempDatabase
       Funcation:InitialDB, SplitCode, UnionData
    """
    #__tempDatabase = ":memory:" # private attribute, define the database file
    conn = sqlite3.connect(":memory:")

    def __init__(self, file, log):
        self.file = file
        self.log = log
        #self.__tempDatabase = self.path + "\\Bus_Temp.db"
        #__tempDatabase: temp db, now change to :memory:

    def InitialDB(self):
        """
           In this part of code, process will inital a sqlite database,
           then create table and import data.
           by the way, split poicode can not use a indepand operate to deal
           so append it in this region.
        """
        print "\nBegin initial database..."
        #conn = sqlite3.connect(self.__tempDatabase)

        cur_init = self.conn.cursor()

        try:
            # create the temp table, need to delete it at first?
            # by use :memory:, drop table is not useable.
            #cur_init.execute("DROP TABLE citybus")
            cur_init.execute(
                """
CREATE TABLE citybus(
    poicode TEXT PRIMARY KEY,
    busline TEXT,
    photo TEXT,
    code_gc TEXT,
    code_dh TEXT
);
                """)

            # import data from csv file
            reader = csv.reader(open(self.file))

            for row in reader:
                li_code = row[0].rsplit('/', 1)
                t = (row[0],row[1],row[2],li_code[0],li_code[1])
                cur_init.execute("INSERT INTO citybus VALUES (?,?,?,?,?)", t)

            self.conn.commit() # don't forget this

            print "Initial Database Successful."

        except:
            print "Sorry, but there is something wrong with it."
            #print e.value or str(e)
        finally:
            cur_init.close()

    def SplitCode(self):
        """
           there is something wrong with it.
           The table is locked when it readed by a process,
           and surely it can not be update...
           so, throw this destrict of code...
        """
        print "\nBegin split poicode..."
        #conn = sqlite3.connect(self.__tempDatabase)

        cur_split = self.conn.cursor() # used to process main
        cur_split_temp = self.conn.cursor() # used to update split

        #try:
        cur_split.execute("ALTER TABLE citybus ADD COLUMN code_gc TEXT")
        cur_split.execute("ALTER TABLE citybus ADD COLUMN code_dh TEXT")

        self.conn.commit()

        cur_split.execute("select * from citybus")

        for row in cur_split:
            li_code = row[0].rsplit('/', 1)
            t = (li_code[0], li_code[1], row[0])
            cur_split_temp.execute("""
update citybus set project_id=?, point_id=? where poicode=?
                """, t)

        self.conn.commit()
        #except:
        #    print "Sorry, but there is something wrong with it."
        #finally:
        cur_split.close()
        cur_split_temp.close()

    def UnionData(self):
        """
           Union the same busline into one item,
           bus will be union derectly
           photo should check unique and illegal ones.
           output the result to log text file and err to errlog.
        """
        print "\nBegin union busline data..."
        #conn = sqlite3.connect(self.__tempDatabase)

        cur_unique = self.conn.cursor() # used to select unique data
        cur_union = self.conn.cursor() # used to select the to-be-union group

        #try:
        union_log = open(self.log, 'w') # create log file
        union_log_err = open(self.log + "_err.txt", 'w') # create err log file

        cur_unique.execute("select * from citybus where code_dh='0'")

        for row in cur_unique:
            li_bus = [] # initial a list to record busline
            li_photo = [] # initial a list to recode photo name

            t = (row[3],)
            cur_union.execute("select * from citybus where code_gc=?", t)

            for data in cur_union:
                if data[1] != "": li_bus.append(data[1])
                if data[2] != "": li_photo.append(data[2])

            li_bus.sort()
            bus_new = ";".join(li_bus)
            # busline data done.

            photo = ";".join(li_photo) # all photo name union together
            li_photo_temp = photo.split(";") # split all photo to singal

            if len(li_photo_temp) <= 1:
                li_photo_new = li_photo_temp # new list of photo without repeat
            else:
                table = {li_photo_temp[0][-12:]:li_photo_temp[0]}
                for pic in li_photo_temp:
                    #
                    # Check the photo name not start with 'I' or 'S'
                    # anyone not like 'IMG_0001.JPG','SDC00001.JPG'
                    #
                    if pic[-12:][0] == "I" or pic[-12:][0] == "S":
                        pass
                    else:
                        union_log_err.write(row[0].encode('gbk')
                                            + ','
                                            + pic.encode('gbk')
                                            + '\n')
                    table.update({pic[-12:]:pic})
                    # same key will be update, others append

                li_photo_new = table.values()

            photo_new = ";".join(li_photo_new)
            # photo name data done.

            # write output result to log file.
            union_log.write(row[0].encode('gbk')
                            + ','
                            + bus_new.encode('gbk')
                            + ','
                            + photo_new.encode('gbk')
                            + '\n')

        print "Union Busline Data Successful."
        #except:
        #    print "Sorry, but there is something wrong with it."
        #finally:
        cur_union.close()
        cur_unique.close()
        union_log.close()
        union_log_err.close()

def main():
    p = Get_Info()  # get the file's info
    data = UnionBuslines(p.file, p.log) # use the class to deal with it
    data.InitialDB()
    #data.SplitCode() # view its __doc__
    data.UnionData()
    Pause()  # pause >> nul

if __name__ == "__main__":
    main()


#------------------------------------------------------------------------------
#!/usr/bin/python
# -*- coding:utf-8 -*-
# file:weather2fetion.py
# by Lee, date 2009-6-25 9:05:14
# original author: tingsking
# quote on: http://blog.csdn.net/tingsking18/archive/2009/04/03/4037584.aspx

"""
   python正则表达式分析新浪网天气预报，通过pyfetion发送短信的代码
   汗一下，这个不是给公司搞生产用，完全自用，哈哈
"""

import sys,os
import re
import urllib
import mimetypes
import PyFetion


def GetWeather(s="东莞"):
    try:
        #get original weather html code from sina.com
        city = urllib.urlencode({"city":s.decode('utf-8').encode('gb2312')})
        sock = urllib.urlopen("http://php.weather.sina.com.cn/search.php?f=1&"+city+"&dpc=1")
        strhtml = sock.read()
        strhtml = unicode(strhtml, 'gb2312','ignore').encode('utf-8','ignore')

        #get all degreed number by ℃ and del the today's feel number.
        theGrades = re.findall('''(\d+)℃''', strhtml)
        for i in range(2): del theGrades[2]

        #get all date
        theDates = re.findall('''(\d+月\d+日)''',strhtml)

        #fetch the descirbe of weather
        weathersin = re.findall('''<h2>(.*)</h2>''',strhtml)
        weather_today = weathersin[1]  # today's report
        weathersout = re.findall('''<p>天气：(.*)</p>''',strhtml)  #next two days

        #get all the winds
        winds = re.findall('''风力：(.*)级''', strhtml)

        #sms = ["%s天气大米报" % s]
        sms = []
        sms.append("%s,%s,%s-%s℃,风力%s级" % (theDates[0], weather_today, theGrades[0], theGrades[1], winds[0]))
        sms.append("%s,%s,%s-%s℃,风力%s级" % (theDates[1], weathersout[0], theGrades[2], theGrades[3], winds[1]))
        sms.append("%s,%s,%s-%s℃,风力%s级" % (theDates[2], weathersout[1], theGrades[4], theGrades[5], winds[2]))
        #sms.append("天气有冷暖，真情永不变!")

        # smscontent = '\n'.join(sms)
        # return smscontent
        # print len(smscontent)  #temp, check length of sms fetion
        return sms

    except:
        print "shit..."


def SendSMS(sms):
    myphone = '15899676367'
    mypwd = '**************'
    destphone = ('15899676367', '13620034802')
    # destphone = ('15899676367',) # test me...

    try:
        me = PyFetion.PyFetion(myphone, mypwd, 'TCP')
    except:
        print "Pls check your mobile NO. and password."
        return -1
    me.login()

    for phone in destphone:
        me.send_sms(sms, phone, long=False)  #long.发送长短信.会出现收不到短信的情况

    return


def main():
    ##msg = GetWeather()
    ##SendSMS(msg)

    msg_dg = GetWeather('东莞')
    msg_ay = GetWeather('安阳')

    msg = ['天气预报']
    msg.append('东莞:' + msg_dg[0] + ';' + msg_dg[1])
    msg.append('安阳:' + msg_ay[0])
    msg.append('=猪头猪头,下雨不愁.人家有伞,我有猪头=')

    content = '\n'.join(msg)
    # print content.decode('utf-8').encode('gbk')
    SendSMS(content)


if __name__ == "__main__":
    sys.exit(main())


#------------------------------------------------------------------------------
#!/usr/bin/python
# -*- coding:utf-8 -*-
# file: UpdatePhone.py
# by Lee, 2009-6-29 14:27:05

"""
长沙市电话号码升级为八位，但已入库数据基本都是七位数的电话号码，使用正则表达式进行替换
替换的原理是见连续的七位数字（其左右均非数字），替换为"8+七位电话"

原始csv数据：
1/1_1/0,0731-5533455;15973153408
1/1_5/0,13975884699
1/1_12/0,0731-4250680
1/1_13/0,13107110233;13217310057
1/1_14/0,0731-4832125;13187219156

处理结果：
1/1_1/0,0731-5533455;15973153408,0731-85533455;15973153408
1/1_5/0,13975884699,13975884699
1/1_12/0,0731-4250680,0731-84250680
1/1_13/0,13107110233;13217310057,13107110233;13217310057
1/1_14/0,0731-4832125;13187219156,0731-84832125;13187219156
"""

import csv
import re
from get_file_info import Get_Info,Pause


p = Get_Info()
# E:\Py\HYLT\UpdatePhone_Changsha\Phone_Changsha.csv

reader = csv.reader(open(p.file))
out = open(p.log, 'w')

for row in reader:
    id = row[0]
    phone = row[1]

    m = re.compile(r'(?P<tel>\b\d{7}\b)')
    new_phone = m.sub(r'8\g<tel>', phone)

    out.write(row[0] + ',' + row[1] + ',' + new_phone + '\n')

out.close()
Pause()


#------------------------------------------------------------------------------
#!/usr/bin/python
# -*- coding:utf-8 -*-
# file: generateguid.py
# by Lee, 2009-7-14
#
'''
       脱离图层环境，对文本POICode记录文件生成随机的POIID(guid机制)

       使用方法：
           1. 将生产工程号保存到csv文件，如果多列的话确保首列为POICode
               2/28_304/0
               2/35_2494/0
               3/32_2813/0
           2. 将csv文件路径输入到程序中
           3. 生成的成品记录示例如下：
               2/28_304/0,1BD04F3B2A404DAF82FFD5D916904345
               2/35_2494/0,1E5E59876D404DE1B397A7AE430B92C3
               3/32_2813/0,A7C2A114801141CC8E9355631E6D4169
'''

import sys,os
import uuid
import csv
from get_file_info import Get_Info,Pause

class GenerateGUID:
    '''生成符合Google提交数据要求格式的GUID形式的ID号'''
    def __init__(self, file, log):
        self.file = file
        self.log = log

    def generate(self):
        reader = csv.reader(open(self.file))
        outlog = open(self.log, 'w')

        for row in reader:
            poicode = row[0]
            poiid = str(uuid.uuid4()).upper().replace('-', '')

            outlog.write(poicode + ',' + poiid + '\n')

def main():
    p = Get_Info()
    guid = GenerateGUID(p.file, p.log)
    guid.generate()
    Pause()

if __name__ == '__main__':
    os.system('title Generate POIID  v1.0')
    print __doc__.decode('utf-8').encode('cp936')
    sys.exit(main())


#------------------------------------------------------------------------------
# -*- coding:utf-8 -*-
# file: DoorEngineTest.py
# by Lee, 2009-7-27

'''测试内部配置的门址查询系统
   地址：http://192.168.9.218:8080/bseigc?Geocoding&address=天河路
   使用SQLite数据库记录并随机提供地址
'''

import time
import sys
import urllib
#import random
import sqlite3

CONNECTCOUNT = 500  # 循环次数

conn = sqlite3.connect('door.db')
cur_door = conn.cursor()  # 检索数据的游标
cur_time = conn.cursor()  # 记录时间的游标
cur_time.execute('DROP TABLE IF EXISTS conntime')
cur_time.execute('CREATE TABLE conntime (sj FLOAT)')

logfile = open('door_log.txt', 'w')
logfile.write('执行时间(毫秒),查询地址,反馈结果'.decode('utf-8').encode('gbk') + '\n')
logfile.write('-' * 80 + '\n')

time.clock()  # 抛弃该次初始化时间记录
for i in xrange(CONNECTCOUNT):
    sql = 'SELECT address FROM gz ORDER BY random() LIMIT 1'
    address = cur_door.execute(sql).fetchone()[0]  # 随机查询一个地址

    content = address
    print content  # 使用中间变量记录查询条件

    ##address = random.choice(['天河路1584号', '机场路 1号', '广园路98号'])
    ##address = urllib.urlencode({'address':address.decode('utf-8').encode('gbk')})
    address = urllib.urlencode({'address':address.encode('gbk')})

    url = 'http://192.168.9.218:8080/bseigc?Geocoding&%s' % address

    time1 = float(str(time.clock()))

    reader = urllib.urlopen(url).read()  # 执行查询并获取反馈结果

    time2 = float(str(time.clock()))
    timecmp = (time2 - time1) * 1000
    cur_time.execute('INSERT INTO conntime VALUES (%s)' % timecmp)

    logfile.write(str(timecmp) + ','  \
                        + content.encode('gbk') + ','  \
                        + reader + '\n')
    # 记录间隔时间和返回结果记录

cur_time.execute('delete from conntime where sj > 100')  # 删除第一条时间记录
conn.commit()
mintime = cur_time.execute('select min(sj) from conntime').fetchone()[0]
avgtime = cur_time.execute('select avg(sj) from conntime').fetchone()[0]
maxtime = cur_time.execute('select max(sj) from conntime').fetchone()[0]

logfile.write('-' * 80 + '\n')
logfile.write('Mininum Connect Time (ms):' + str(mintime) + '\n' \
            + 'Maxinum Connect Time (ms):' + str(maxtime) + '\n' \
            + 'Average Connect Time (ms):' + str(avgtime) + '\n')

conn.close()
logfile.close()


#------------------------------------------------------------------------------
#!/usr/bin/python
# -*- coding:utf-8 -*-
# file: OralEng.py
# by Lee, 2009-8-25
#
'''
   自用
   从网上Down了一篇口语短句，共有四百多条。用这个脚本处理成ics日历格式
   导入GoogleCalendar后可以每天收条短信学习啦。
'''

import time
import sqlite3

outICS = open('oralenglish.ics','w')

outICS.writelines('''BEGIN:VCALENDAR
PRODID:-//Google Inc//Google Calendar 70.9054//EN
VERSION:2.0
''')  # 文件头

conn = sqlite3.connect('OralEnglish.db')
cells = conn.cursor().execute('select en,cn from oe order by random(en)').fetchall() #随机排序先

now = int(time.time())
sec = 24*60*60
i = 0
for cell in cells:
    theDate = time.strftime('%Y%m%d', time.localtime(now+i*sec)) #日子一天一天过，我们会慢慢长大

    en = cell[0].encode('utf-8')  # 口语短句
    cn = cell[1].encode('utf-8')  # 汉语翻译

    outICS.write('BEGIN:VEVENT\n')
    outICS.write('DTSTART:' + theDate + 'T153000Z\n')
    outICS.write('DTEND:' + theDate + 'T153000Z\n')
    outICS.write('DESCRIPTION:\n')
    outICS.write('LOCATION:@' + cn + '\n')
    outICS.write('SEQUENCE:0\n')
    outICS.write('STATUS:CONFIRMED\n')
    outICS.write('SUMMARY:' + en + '\n')
    outICS.write('TRANSP:OPAQUE\n')
    outICS.write('END:VEVENT\n')

    i += 1

outICS.write('END:VCALENDAR\n')
conn.close()
outICS.close()


#------------------------------------------------------------------------------
#!/usr/bin/python
# -*- coding:utf-8 -*-
# file: spss.py
# by Lee, 2009-9-2
#
'''
长沙提交Google数据的营业时间信息包含在xml打包字段中,要统计营业时间的占有率是个问题
用正则统计下数据量先吧.

>>>config.yaml
#"DRIVER={SQL Server};SERVER=192.168.9.246;DATABASE=Google;UID=sa;PWD=test"
driver: {SQL Server}
host: dbserver2
server: 192.168.9.246
database: Google
uid: sa
pwd: test
table: Guangzhou2Google

'''

import pyodbc
import yaml
import re

conf = yaml.load(file('config.yaml','r'))
connstr = '''DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s''' % (
    conf['server'],
    conf['database'],
    conf['uid'],
    conf['pwd'])

conn = pyodbc.connect(connstr)
cur = conn.cursor()

for cate in ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','99']:
    sum = 0
    c_tel = 0
    c_hour = 0

    rows = cur.execute("select tel,described from Changsha WHERE SUBSTRING(CateCode,1,2)=?", cate).fetchall()
    for row in rows:
        sum += 1  # total count
        # tel count
        if row.tel:
            c_tel += 1

        # businesshour count
        reg = re.search(r'<BusinessHour>(?P<bh>.*)</BusinessHour>', row.described)
        target = reg.group('bh')
        if target:
            c_hour += 1

    print cate, sum, c_tel, c_hour

print 'SPSS Done.'


#------------------------------------------------------------------------------
#!/usr/bin/python
# -*- coding:utf-8 -*-
# file: Exp2Csv.py
# by Lee, 2009-9-2

'''
读取MSSql中的数据，导出到csv文件
'''

import yaml
import pyodbc
#import csv
import datetime

##outfile = csv.writer(open('data.csv', 'w')) #error output of code
outfile = open('data.csv','w')

conf = yaml.load(file('config.yaml','r'))
connstr = '''DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s''' % (
    conf['server'],
    conf['database'],
    conf['uid'],
    conf['pwd'])

conn = pyodbc.connect(connstr)
cur = conn.cursor()

#rows = cur.execute('SELECT Top 3 * FROM ?', (conf['table'],)).fetchall()
rows = cur.execute('SELECT Top 3000 * FROM Guangzhou2Google').fetchall()
for row in rows:
    li = []
    for i in xrange(len(row)):
        if row[i] == None:
            li.append('')
        elif isinstance(row[i], float):
            li.append(row[i])
        elif isinstance(row[i], datetime.datetime):
            li.append(str(row[i]))
        else:
            li.append('"' + row[i] + '"')

    outrow = ','.join(li)
    outfile.write(outrow.encode('utf-8'))
    outfile.write('\n')

outfile.close()
conn.close()


#------------------------------------------------------------------------------
#!/usr/bin/python
# -*- coding:utf-8 -*-
# file: countnum.py
# by Lee, 2009-9-3
#
'''
   计算周工空间数据库管理系统的总代码行数
   系统分团队和总库两个大模块
'''

import os

#团队模块代码行数统计
top = r'D:\code\team'
os.chdir(top)
sum = 0
for root,dir,files in os.walk(top,topdown=False):
    for name in files:
        print name + '\t',
        codes = open(name, 'r')
        i = 0
        while codes.readline():
            i += 1
        sum += i
        print i

print sum
print '\n'

#总库模块代码行数统计
top2 = r'D:\code\company'
os.chdir(top2)
sum = 0
for root,dir,files in os.walk(top2,topdown=False):
    for name in files:
        print name + '\t',
        codes = open(name, 'r')
        i = 0
        while codes.readline():
            i += 1
        sum += i
        print i

print sum


#------------------------------------------------------------------------------
#!/usr/bin/python
# -*- coding:utf-8 -*-
# file: GenID.py
# by Lee, 2009-9-15

'''\
基于MSSQL进行编制ID的处理

前面写的编制GUID的脚本需要根据csv文件来批量生产，需要导入到数据库后再执行更新操作
本脚本使用pyodbc直接对mssql数据库进行操作（PS:以前还写了对Access进行操作的，由于
执行效率问题没有提上日程），执行时间和效率有待考验。
'''

import pyodbc
import uuid

connstr = 'DRIVER={SQL Server};SERVER=192.168.9.246;DATABASE=Google;UID=sa;PWD=test'
conn = pyodbc.connect(connstr, autocommit=True)
cur = conn.cursor()
cur2 = conn.cursor()

rows = cur.execute('select poicode from bbtemp_gz').fetchall()
for row in rows:
    poicode = row.poicode
    poiid = str(uuid.uuid4().hex.upper())
    print poicode,poiid,len(poiid)
    cur2.execute("update bbtemp_gz set poiid=? where poicode=?", (poiid, poicode))

conn.close()


#------------------------------------------------------------------------------
#!/usr/bin/python
# -*- coding:utf-8 -*-
# file: SpssCateCode.py
# by Lee, 2009-11-05

'''统计每个城市的三级分类的数据量，依照提交给Google的数据进行查询。'''

import pyodbc
import csv

connstr = "DRIVER={SQL Server};SERVER=192.168.9.246;DATABASE=GIS;UID=sa;PWD=xiaoping"
conn = pyodbc.connect(connstr)
cur = conn.cursor()

result = file('catecode_number.txt', 'w') #定义输出记录文件

citylist = ['zhuhai','foshan','zhongshan'] #城市列表可以自定义

for city in citylist:
    print city
    result.write(city + '\n')

    sReader = csv.reader(open('catecode.csv'))
    for row in sReader:
        codenum = str(row[0])
        sql = "select count(*) from %s where catecode='%s'" % (city,codenum)
        sum = cur.execute(sql).fetchone()[0] #这里加上0号索引才能识别出数值来

        print sum
        #result.write(codenum + '\t' + str(sum) + '\n')
        result.write(str(sum) + '\n')
    #sReader.close() #csv的reader不需要手动关闭

result.close()
conn.close()


#------------------------------------------------------------------------------
#!/usr/bin/python
# -*- coding:utf-8 -*-
# file: Coord4Grid.py
# by Lee, 2009-11-13

'''配准图幅自动生成坐标模板
根据输入的图幅计算该图四个角的坐标值，从而生成模板文件。

先根据国家标准分幅的图幅号计算坐标，即考虑在1:5000形式下的比例尺算法。
计算公式：
    经度=(数字码-31)*6度+(列号-1)*1.875分
    纬度=(字符码-1)*4+(4度/1.25分-行号)*1.25分

再根据ABCD的分法取四个小图幅的坐标并格式化成需要的模板形式。

2.0改进：
通过研究ArcMap配准后生成都jgw格式内容：
    1、X-Scale(一个像元的大小)
    2、旋转项
    3、旋转项
    4、负的Y-Scale(一个像元的大小)
    5、转换项，即左上角X坐标
    6、转换项，即左上角Y坐标
发现只要计算出一个像元代表的度数大小，再算出左上角的经纬度即可
难点是我们的ABCD分幅还玩外扩充了一部分，通过大量测量和分析得出扩充大小
1、3368×2381像素的图幅：
    X轴  左边扩充226px，右边219.25px
    Y轴  上边扩充229.5px，下边204.5px
2、2246×1588像素的格式：X轴左边扩充150px
    X轴  左边扩充150.5px，右边146px
    Y轴  上边扩充153px，下边137px
'''

import os
import string

dis_lng = 0.03125  # 经差1.875分，统一转换为度数
dis_lat = 0.0208333333333333  # 维差1.25分

def coordinate(graphnum):
    '''计算国家标准分幅西南角坐标值，graphnum为国家标准1:5000分幅号(e.g. F49H045179)'''
    a = ord(graphnum[0])-64  # 字符码6(F)
    b = int(graphnum[1:3])  # 数字码49
    c = int(graphnum[4:7])  # 行号45
    d = int(graphnum[7:10])  # 列号179

    # 西南角坐标
    lng = (b-31)*6 + (d-1)*dis_lng
    lat = (a-1)*4 + (4/dis_lat - c)*dis_lat

    return lng,lat

def get_coord(gis):
    '''根据华业龙图分幅标准，计算1:2500比例下左下角和右上角（红线交叉处）坐标'''
    if len(gis) != 11:
        return 0,0,0,0

    coord = coordinate(gis[0:-1]) #获取1:5000分幅坐标
    # 西南角（左下角）坐标
    lng_left = coord[0]
    lat_bottom = coord[1]
    # 东北角（右上角）坐标
    lng_right = lng_left + dis_lng
    lat_upper = lat_bottom + dis_lat
    # 中心坐标（方便再分幅使用）
    lng_mid = (lng_left+lng_right)/2
    lat_mid = (lat_bottom+lat_upper)/2

    # 根据分幅返回西南和东北（左下和右上角）坐标
    if gis[-1] == 'A': return lng_left,lat_mid,lng_mid,lat_upper
    if gis[-1] == 'B': return lng_mid,lat_mid,lng_right,lat_upper
    if gis[-1] == 'C': return lng_left,lat_bottom,lng_mid,lat_mid
    if gis[-1] == 'D': return lng_mid,lat_bottom,lng_right,lat_mid

    return 0,0,0,0

def get_corner_coord(grid, type):
    '''计算整个图幅左上角坐标'''
    center_grid = get_coord(grid)  # 获取图幅中心红线区域两角坐标
    left_up_x = center_grid[0]  # 红线左上角经度
    left_up_y = center_grid[3]  # 红线左上角纬度

    # 获取整个图幅左上角坐标
    if type == '1':
        corner_x = left_up_x - dis_lng/2/(3368-226-219.25)*226
        corner_y = left_up_y + dis_lat/2/(2381-229.5-204.5)*229.5
        dis_x = dis_lng/2/(3368-226-219.25)
        dis_y = dis_lat/2/(2381-229.5-204.5)
        return dis_x,dis_y,corner_x,corner_y
    if type == '2':
        corner_x = left_up_x - dis_lng/2/(2246-150.5-146)*150.5
        corner_y = left_up_y + dis_lat/2/(1588-153-137)*153
        dis_x = dis_lng/2/(2246-150.5-146)
        dis_y = dis_lat/2/(1588-153-137)
        return dis_x,dis_y,corner_x,corner_y

def final_format(grid, type):
    '''格式化输出内容'''
    grid_coordinate = get_corner_coord(grid, type)

    return '''\
%s
0.0000000000
0.0000000000
-%s
%s
%s
''' % (grid_coordinate[0], grid_coordinate[1],
       grid_coordinate[2],grid_coordinate[3])


if __name__ == '__main__':
    path = raw_input("""\
坐标配准模板生成器

请输入图幅所在的文件夹（或者将文件夹拖拽进来即可）
>>>""".decode('utf8').encode('cp936'))

    grid_type = raw_input("""
选择影像图像素模式
    1: 3368×2381像素
    2: 2246×1588像素
>>>""".decode('utf8').encode('cp936'))

    graphs_original = os.listdir(path) # 原始目录文件信息
    graphs = []
    for name in graphs_original:
        if string.lower(name[-4:]) == '.jpg':
            graphs.append(name[:-4])  # 过滤剩下jpg文件

    for code in graphs:
        print '............',
        print code,
        print '............'
        out = file(path + "\\" + code + '.jgw', 'w')
        out.write(final_format(code, grid_type)) # 输出配准文件
        out.close()

    print
    print '完成!饭也OK啦，可以米西了！'.decode('utf8').encode('cp936')
    raw_input()


#------------------------------------------------------------------------------
#!/usr/bin/python
# -*- coding:utf-8 -*-
# file: Coord4Grid.pyw
# Version: 2.0
# by Lee, 2009-11-16

'''配准图幅自动生成坐标模板
根据输入的图幅计算该图四个角的坐标值，从而生成模板文件。

先根据国家标准分幅的图幅号计算坐标，即考虑在1:5000形式下的比例尺算法。
计算公式：
    经度=(数字码-31)*6度+(列号-1)*1.875分
    纬度=(字符码-1)*4+(4度/1.25分-行号)*1.25分
再根据ABCD的分法取四个小图幅的坐标并格式化成需要的模板形式。

0.2改进：
由配准模板改为影像校准文件机制。通过研究ArcMap配准后生成都jgw格式内容：
    1)、X-Scale(一个像元的大小)
    2)、旋转项
    3)、旋转项
    4)、负的Y-Scale(一个像元的大小)
    5)、转换项，即左上角X坐标
    6)、转换项，即左上角Y坐标
发现只要计算出一个像元代表的度数大小，再算出左上角的经纬度即可
难点是我们的ABCD分幅还往外扩充了一部分，通过大量测量和分析得出扩充大小
1、3368×2381像素的图幅：
    X轴  左边扩充226px，右边219.25px
    Y轴  上边扩充229.5px，下边204.5px
2、2246×1588像素的格式：X轴左边扩充150px
    X轴  左边扩充150.5px，右边146px
    Y轴  上边扩充153px，下边137px

0.3改进：
使用OO机制并且GUI化(基于Tk)
'''

import os
import string
from Tkinter import *

class Coord4Grid:
    '''定义实现获取坐标和偏移量等参数值的类'''
    def __init__(self, grid, type):
        self.grid = grid
        self.type = type
        self.dis_lng = 0.03125  # 经差1.875分，统一转换为度数
        self.dis_lat = 0.0208333333333333  # 纬差1.25分

    def coordinate(self, graphnum):
        '''计算国家标准分幅西南角坐标值，graphnum为国家标准1:5000分幅号(e.g. F49H045179)'''
        a = ord(graphnum[0])-64  # 字符码6(F)
        b = int(graphnum[1:3])  # 数字码49
        c = int(graphnum[4:7])  # 行号45
        d = int(graphnum[7:10])  # 列号179

        # 西南角坐标
        lng = (b-31)*6 + (d-1)*self.dis_lng
        lat = (a-1)*4 + (4/self.dis_lat - c)*self.dis_lat

        return lng,lat

    def get_coord(self, gis):
        '''根据华业龙图分幅标准，计算1:2500比例下左下角和右上角（红线交叉处）坐标'''
        if len(gis) != 11:
            return 0,0,0,0

        coord = self.coordinate(gis[0:-1]) #获取1:5000分幅坐标
        # 西南角（左下角）坐标
        lng_left = coord[0]
        lat_bottom = coord[1]
        # 东北角（右上角）坐标
        lng_right = lng_left + self.dis_lng
        lat_upper = lat_bottom + self.dis_lat
        # 中心坐标（方便再分幅使用）
        lng_mid = (lng_left+lng_right)/2
        lat_mid = (lat_bottom+lat_upper)/2

        # 根据分幅返回西南和东北（左下和右上角）坐标
        if gis[-1] == 'A': return lng_left,lat_mid,lng_mid,lat_upper
        if gis[-1] == 'B': return lng_mid,lat_mid,lng_right,lat_upper
        if gis[-1] == 'C': return lng_left,lat_bottom,lng_mid,lat_mid
        if gis[-1] == 'D': return lng_mid,lat_bottom,lng_right,lat_mid

        return 0,0,0,0

    def get_corner_coord(self, grid, type):
        '''计算整个图幅左上角坐标'''
        center_grid = self.get_coord(grid)  # 获取图幅中心红线区域两角坐标
        left_up_x = center_grid[0]  # 红线左上角经度
        left_up_y = center_grid[3]  # 红线左上角纬度

        # 获取整个图幅左上角坐标
        if type == '1':
            corner_x = left_up_x - self.dis_lng/2/(3368-226-219.25)*226
            corner_y = left_up_y + self.dis_lat/2/(2381-229.5-204.5)*229.5
            dis_x = self.dis_lng/2/(3368-226-219.25)
            dis_y = self.dis_lat/2/(2381-229.5-204.5)
            return dis_x,dis_y,corner_x,corner_y
        if type == '2':
            corner_x = left_up_x - self.dis_lng/2/(2246-150.5-146)*150.5
            corner_y = left_up_y + self.dis_lat/2/(1588-153-137)*153
            dis_x = self.dis_lng/2/(2246-150.5-146)
            dis_y = self.dis_lat/2/(1588-153-137)
            return dis_x,dis_y,corner_x,corner_y

    def final_format(self):
        '''格式化输出内容(唯一的出口函数)'''
        grid_out = self.get_corner_coord(self.grid, self.type)

        return '''\
%s
0.0000000000
0.0000000000
-%s
%s
%s
''' % (grid_out[0], grid_out[1], grid_out[2],grid_out[3])


# 创建Tkinter实例，用于实现界面效果
root = Tk()
root.geometry("400x300")  # 定义窗体大小
root.title("影像自动配准")  # Caption

def Enter():
    '''执行配准功能函数'''
    path = text_path.get()  # 获取路径
    if path:
        type = str(v.get())  # 获取分辨率模式
        if type in ['1','2']:
            Run(path, type)  # 执行
        else:
            listbox.insert(END, '请选择影像分辨率模式!!')
    else:
        listbox.insert(END, '请给出影像所在地址!! (提示：复制影像所在文件夹过来即可)')

def ReturnInsert(event):
    '''路径文本框的回车事件'''
    Enter()

def Run(path, grid_type):
    '''执行主函数,根据路径和类型进行校准文件的生成'''
    graphs_original = os.listdir(path) # 原始目录文件信息
    graphs = []
    for name in graphs_original:
        if string.upper(name[-4:]) == '.JPG':
            graphs.append(string.upper(name[:-4]))  # 过滤剩下jpg文件

    for code in graphs:
        listbox.insert(END, '........... '+code+' ...........')
        out = file(path + "\\" + code + '.jgw', 'w')
        photo = Coord4Grid(code, grid_type)
        out.write(photo.final_format()) # 输出配准文件
        out.close()

    listbox.insert(END, '')
    listbox.insert(END, '完成!饭也OK啦，可以米西啦!')
    listbox.insert(END, '')

# 窗体框架
labelframe = Frame(root)  # 文件夹路径
textframe = Frame(root)  # 影像分辨率模式
listframe = Frame(root)  # 日志提示输出

# 窗体部件
label_path = Label(labelframe, text='输入影像文件夹的路径：')
text_path = Entry(labelframe)
label_type = Label(textframe, text='选择影像的分辨率模式：')

v=IntVar()  # 定义单选按钮使用的变量
v.set('1')  # 默认选择第一个
radio_big = Radiobutton(textframe, text='3368×2381', variable = v, value=1)
radio_small = Radiobutton(textframe, text='2246×1588', variable = v, value=2)

enter_button = Button(textframe, text="  执行  ", command=Enter)  #执行按钮

scrollbar = Scrollbar(listframe, orient=VERTICAL)
listbox = Listbox(listframe, yscrollcommand=scrollbar.set, selectmode=EXTENDED)
scrollbar.configure(command=listbox.yview)  # 定义list并将scroll绑定上去

# 绑定路径文本框的回车事件到执行函数
text_path.bind("<Return>", ReturnInsert)

# 绑定控件到窗体
label_path.pack(side=LEFT)
text_path.pack(side=LEFT, fill=X, expand=1)
label_type.pack(side=LEFT)
radio_big.pack(side=LEFT)
radio_small.pack(side=LEFT)
listbox.pack(side=LEFT,fill=BOTH, expand=1)
scrollbar.pack(side=RIGHT, fill=Y)
labelframe.pack(fill=X)
textframe.pack(fill=X)
listframe.pack(fill=BOTH, expand=1)
enter_button.pack(side=RIGHT)

# 循环监视
root.mainloop()
