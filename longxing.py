#-*- coding=utf-8 -*-#
# 文件: longxing.py
# 作者：李晓平
# 时间：2013-11-11
# 用途：记录点点滴滴
# 授权：自用
#
'''工作中实际用到的运行于生产的代码模块
'''


#----------------------------------------------------------------------------
#  不太适应这个作息时间，做个休息提醒 2013-11-12
#  配合系统定时任务进行提醒
#----------------------------------------------------------------------------
__version__ = "0.1"
if __name__ == "__main__":
    print
    print "            EEEEEEEEEEEEEEEEEEEEE"
    print "          EEMMMMMMMMMMMMMMMMMMMMM"
    print "          MMMMMMMMMMMMMMMMMBBBBBBBB"
    print "        ::BBBBMMMMMMMMMMMMMMMMMMMMM"
    print "        BBBBBBBBBBBBBBBBBBBBBBBBBBBLL"
    print "        MMMMMMBBBBBBBBBBBBBBBBBBBBBMM"
    print "       FMMMMBBBBBBBBBBBBBBBBBBBBBBBMM"
    print "        MMMMBBBBBBBBBBBBBBBBBBBMMBBEE"
    print "          MMBBBBBBBBBBBBBBBMMMMBBBB"
    print "            BBBBBBBBBBBBBBBBBMMEE"
    print "              EEMMMMBBMMMMMMMI"
    print "                  EEMMBMMI"
    print "                     MB"
    print "                     MM"
    print "                     BM"
    print "                     MB"
    print "                     BB"
    print "             ..LLEEBBMMBBEEI ."
    print "         EEBBMBBBBBBBBBMBBMMMMMBBBMMLL"
    print "          ::I I  I I I  I I I I I .."
    print
    print "It's time to have a rest! Let tings to what it can be..."
    raw_input()


#----------------------------------------------------------------------------
#  使用lxml进行页面内容的抓取  2013-11-20
#----------------------------------------------------------------------------
import lxml.html.soupparser as soupparser
import lxml.etree as etree
from lxml.cssselect import CSSSelector

html = '''<table class="racebox" id="aaa354_8" name="loc_race" style="display:none">
<tbody><tr>
<td>
<div class="raceno" id="354_8">
<div class="bar_result" id="HK_bar"/><span>Race 8</span>
</div>
<div class="result_tote">
<ul>
<li id="mc_tote">MC Tote </li>
</ul>
<div class="clear"/>
</div>

<!--table thead--><table class="result_table" id="resultThead">
<tbody><tr>
<th>&#160;</th>
<td>Horse<span>|</span></td>
<td>Win / Plc</td>
</tr>
</tbody></table>

<!-- Win/plc--><table class="result_table winplc">
<tbody><tr>
<th style="border-bottom:1px solid #fff;" valign="top">1<sup>st</sup></th>
<td style="font-weight:bold;border-left:none;">8</td>
<td class="mctote" style="border-right:none;">63</td>
<td class="mctote slash">/</td>
<td class="mctote" style="border-left:none;">20.50</td>
</tr>
<tr>
<th style="border-bottom:1px solid #fff;" valign="top">2<sup>nd</sup></th>
<td style="font-weight:bold;border-left:none;">1</td>
<td class="mctote" style="border-right:none;">-</td>
<td class="mctote slash">/</td>
<td class="mctote" style="border-left:none;">19.50</td>
</tr>
<tr>
<th valign="top">3<sup>rd</sup></th>
<td style="font-weight:bold;border-left:none;">4</td>
<td class="mctote" style="border-right:none;">-</td>
<td class="mctote slash">/</td>
<td class="mctote" style="border-left:none;">29.50</td>
</tr>
</tbody></table>

<!-- FC--><table class="result_table">
<tbody><tr>
<th rowspan="1" valign="top">FC</th>
<td style="font-weight:bold;border-left:none;">1-8</td>
<td class="mctote">144.50</td>
</tr>
</tbody></table>

<!-- PFT--><table class="result_table">
<tbody><tr>
<th rowspan="3" valign="top">PFT</th>
<td style="font-weight:bold;border-left:none;">1-4</td>
<td class="mctote">83</td>
</tr>
<tr>
<td style="font-weight:bold;border-left:none;">1-8</td>
<td class="mctote">83</td>
</tr>
<tr>
<td style="font-weight:bold;border-left:none;">4-8</td>
<td class="mctote">85</td>
</tr>
</tbody></table>
</td>
</tr>
</tbody></table>
'''

dom = soupparser.fromstring(html)

race_type = '3'
race_num = None
tote_code = "HK_HK"

# xpath /绝对定位  //搜索定位
partten = '//table[@id="aaa%s_%s"]'
if race_num:
    partten = partten %(race_type, race_num)
else:
    partten = '//table[contains(@id, "aaa%s_")]' %race_type

print partten

tdClass = tote_code[-2:].lower()+'tote'

print tdClass

raceResult = []
for item in dom.xpath(partten):
    # 依次分析所有场次
    print etree.tostring(item)
    itemDom = soupparser.fromstring(etree.tostring(item))
    race_num_inner = itemDom.xpath('//div[@class="raceno"]/div/span')[0].text.replace('Race ','')

    result = []
    i = 1
    for sn in itemDom.xpath('//table[@class="result_table winplc"]/tr'):
        #print etree.tostring(sn)
        snDom = soupparser.fromstring(etree.tostring(sn))

        horseNum = snDom.xpath('/html/tr/td[1]')[0].text
        snTote = snDom.xpath('//td[@class="%s"]' %tdClass)
        horseWin = snTote[0].text
        horsePlc = snTote[1].text
        horseWin = 0 if horseWin=='-' else horseWin
        result.append((i, horseNum, horseWin, horsePlc),)
        i += 1
    raceResult.append({"raceNumber": int(race_num_inner), "result": result})
print raceResult



#----------------------------------------------------------------------------
# 使用SimpleXMLRpc来进行服务器程序的远程控制 2014-02-28
#----------------------------------------------------------------------------

### server
from SimpleXMLRPCServer import SimpleXMLRPCServer

svr = SimpleXMLRPCServer(("0.0.0.0", 808))

def my_func(txt):
    print txt

svr.register_function(my_func, "fun")
svr.serve_forever()


### client
import xmlrpclib
s = xmlrpclib.ServerProxy("http://127.0.0.1:8202")
#s.fun()
print s.system.listMethods()



#----------------------------------------------------------------------------
# 微线程工作流生成器 2014-03-31
#----------------------------------------------------------------------------

# coding:utf-8


class MicroThread():
    def __init__(self, flow, kw):
        self.flow = flow
        self.path = kw.get("path", "")
        self.name = kw.get("name", "test.py")
        self.thread_class = kw.get("class", "Test")

    def write_header(self, py):
        header = """\
# coding: utf-8

import time

"""
        py.write(header)

    def write_class(self, py, class_name, first_status):
        cls = """
class {0}(object):
    def __init__(self):
        self.status = "{1}"
"""
        py.write(cls.format(class_name, first_status))

    def write_body(self, py, currect_status, doc, next_status):
        body = """
    def {0}(self):
        '''{1}'''
        while True:
            if self.status == '{0}':
                print 'currect status : {0} \t {1}'

                time.sleep(1)

                self.status = '{2}'
            yield
"""
        py.write(body.format(currect_status, doc, next_status))

    def write_footer(self, py):
        footer = """
    def main(self):
        while True:
            getattr(self, self.status)().next()

if __name__ == '__main__':
    {0}().main()
"""
        py.write(footer.format(self.thread_class))

    def main(self):
        if self.flow:
            py = file(self.path+self.name, 'w')
            self.write_header(py)
            first_status = self.flow[0][0]
            self.write_class(py, self.thread_class, first_status)
            for i in range(len(self.flow)):
                curr = self.flow[i][0]
                doc = self.flow[i][1]
                next = first_status if i == len(self.flow)-1 else self.flow[i+1][0]
                self.write_body(py, curr, doc, next)
            self.write_footer(py)
            py.close()
        else:
            print "empty flow work.."


if __name__ == "__main__":
    flowwork = [
        ("login","登陆"),
        ("get_job","获取任务"),
        ("check_ending","检查结束时间状态"),
        ("check_pedding","查询"),
        ("do_job", "执行任务"),
        ("free_job","结束任务,报告机器空闲"),
    ]
    params = {
        'name': 'sSlave.py',
        'class': 'ServerSlave',
    }
    MicroThread(flowwork, params).main()



#----------------------------------------------------------------------------
#
#----------------------------------------------------------------------------
