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
#
#----------------------------------------------------------------------------
