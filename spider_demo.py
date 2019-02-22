#!/usr/bin/env python
# coding=utf-8

"""

@author: sml2h3

@license: (C) Copyright 2018-2020

@contact: sml2h3@gmail.com

@software: mmewmd_crack_for_wenshu

@file: spider_demo

@time: 2019-01-21
"""
import requests
import time
import datetime
import execjs
import sys
import json
from lxml import etree
import random
from urllib import parse

with open('encrypt.js', 'r', encoding="utf-8") as f:
    js1 = f.read()
    ctx1 = execjs.compile(js1)
with open('ywtu.js', 'r', encoding="utf-8") as f:
    js2 = f.read()
    ctx2 = execjs.compile(js2)
with open('vl5x.js', 'r', encoding="utf-8") as fp:
    js = fp.read()
    ctx = execjs.compile(js)


class SpiderManager(object):



    def __init__(self, debug=False):
        self.param = ""
        self.court = ""
        self.f80t = ""
        self.f80t_n = ""
        self.meta = ""
        self.f80s = ""
        self.ywtu = ""
        self.vjkl5 = ""
        self.content = ""
        self.debug = debug
        self.conditions = ""
        self.url = "http://wenshu.court.gov.cn/List/List?sorttype=1&conditions={}"
        self.url_for_content = "http://wenshu.court.gov.cn/List/ListContent"
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "wenshu.court.gov.cn",
            "Origin": "http://wenshu.court.gov.cn",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        self.cookies = {
            "ccpassport": "1ff98c661b8f424096c234ce889da9b0",
            "_gscu_2116842793": "47626758817stt18",
            "_gscs_2116842793": "47659453ttzz3o20|pv:14",
            "_gscbrs_2116842793": "1",
            "wzwsconfirm": "0e561c10c60c2f0d44410644eb3c2403",
            "wzwstemplate": "NQ==",
            "wzwschallenge": "-1",
            "wzwsvtime": ""
        }
        self.data = {
            "Param": "法院名称:北京市石景山区人民法院,裁判日期:2017-01-1",
            "Index": "",
            "Page": "20",
            "Order": "法院层级",
            "Direction": "asc",
            "vl5x": "",
            "number": "VUAV4WK7",
            "guid": ""
        }

    def setconditions(self, conditions: str):
        self.conditions = conditions

    def init(self):
        # 要访问的目标页面
        self.targetUrl = "http://test.abuyun.com"
        # targetUrl = "http://proxy.abuyun.com/switch-ip"
        # targetUrl = "http://proxy.abuyun.com/current-ip"

        # 代理服务器
        self.proxyHost = "http-dyn.abuyun.com"
        self.proxyPort = "9020"

        # 代理隧道验证信息
        self.proxyUser = "H2U9VZ41T9AB6W0D"
        self.proxyPass = "9A35A20083D94917"

        self.proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": self.proxyHost,
            "port": self.proxyPort,
            "user": self.proxyUser,
            "pass": self.proxyPass,
        }

        self.proxies = {
            "http": self.proxyMeta,
            "https": self.proxyMeta,
        }
        self.f80t = ""
        self.f80t_n = ""
        self.meta = ""
        self.f80s = ""
        self.ywtu = ""
        self.vjkl5 = ""
        if not self.conditions:
            if self.debug:
                print("条件不能为空")
                return False
        request_url = self.url.format(self.conditions)
        headers = self.headers
        cookies = self.cookies
        cookies['wzwsvtime'] = str(int(time.time()))
        # cookies = "; ".join(cookies)
        try:

            # rsp = requests.get(request_url, headers=headers, cookies=cookies)
            rsp = requests.get("http://wenshu.court.gov.cn", headers=headers)
            rsp.close()
        except Exception as e:
            if self.debug:
                print(e)
                print("网络连接出错，稍等5秒后重新执行")
            time.sleep(5)
            return self.init()

        self.f80s = rsp.cookies['FSSBBIl1UgzbN7N80S']
        self.f80t = rsp.cookies['FSSBBIl1UgzbN7N80T']
        html = etree.HTML(rsp.text)
        self.meta = html.xpath('//*[@id="9DhefwqGPrzGxEp9hPaoag"]/@content')[0]
        self.ywtu = ctx2.call("getc", self.meta)
        return True

    def getvjkl5(self):
        request_url = self.url.format(self.conditions)
        headers = self.headers
        cookies = self.cookies
        cookies['wzwsvtime'] = str(int(time.time()))
        self.ywtu = ctx2.call("getc", self.meta)
        self.f80t_n = ctx1.call("getCookies", self.meta, self.f80t, self.ywtu)

        cookies['FSSBBIl1UgzbN7Nenable'] = "true"
        cookies['FSSBBIl1UgzbN7N80S'] = self.f80s
        cookies['FSSBBIl1UgzbN7N80T'] = self.f80t_n
        cookies['wzwsvtime'] = str(int(time.time()))
        try:
            rsp = requests.get(request_url, headers=headers, cookies=cookies)
            rsp.close()
        except Exception as e:
            if self.debug:
                print(e)
                print("获取vjkl5失败:网络连接出错")
            return False
        if rsp.status_code == 200 and "vjkl5" in rsp.cookies:
            self.vjkl5 = rsp.cookies['vjkl5']
            return True
        else:
            if self.debug:
                print(self.meta)
                print(self.ywtu)
                print(self.f80t)
                print(self.f80t_n)
                print("获取vjkl5失败,code：{}".format(rsp.status_code))
            return False

    def get_vl5x(self):
        """
        根据vjkl5获取参数vl5x
        """
        vl5x = (ctx.call('getKey', self.vjkl5))
        return vl5x

    def createGuid(self):
        return str(hex((int(((1 + random.random()) * 0x10000)) | 0)))[3:]

    def getguid(self):
        return '{}{}-{}-{}{}-{}{}{}' \
            .format(
            self.createGuid(), self.createGuid(),
            self.createGuid(), self.createGuid(),
            self.createGuid(), self.createGuid(),
            self.createGuid(), self.createGuid()
        )

    def getContent(self, page):

        url = self.url_for_content
        self.f80t_n = ctx1.call("getCookies", self.meta, self.f80t, self.ywtu)
        # print(self.f80t_n)
        vl5x = self.get_vl5x()
        data = self.data
        data['Param'] = self.param
        data['Index'] = str(page)
        data['vl5x'] = vl5x
        data['guid'] = self.getguid()
        cookies = self.cookies
        cookies['wzwsvtime'] = str(int(time.time()))
        cookies['FSSBBIl1UgzbN7Nenable'] = "true"
        cookies['FSSBBIl1UgzbN7N80S'] = self.f80s
        cookies['FSSBBIl1UgzbN7N80T'] = self.f80t_n
        cookies['vjkl5'] = self.vjkl5
        headers = self.headers
        headers['Referer'] = self.url.format(parse.quote(self.conditions))
        try:
            rsp = requests.post(url, headers=headers, cookies=cookies, data=data)
            # rsp = requests.post(url, headers=headers, cookies=cookies, data=data, proxies=self.proxies)
        except Exception as e:
            if self.debug:
                print(e)
                print("获取内容时网络请求出错")
            return False
        if rsp.status_code == 200 and "验证码" not in rsp.text:
            self.content = rsp.text
            return True
        else:
            if self.debug:
                print("获取内容出错,code:{},若code为200，可能出现了验证码".format(rsp.status_code))
            return False
    def setParam(self, param:str):
        self.param = param

    def setCourt(self, court:str):
        self.court = court

    def getData(self):
        return self.content



def readCourtFile():
    fo = open("courts.txt", "r")
    courtlist = fo.read().splitlines()
    print(courtlist)

def string_toDatetime(st):
    now = datetime.datetime.strptime(st, "%Y-%m-%d")
    now = now + datetime.timedelta(days=1)
    if now.year > 2017:
        return ""
    print(now)
    return now.strftime('%Y-%m-%d')

if __name__ == '__main__':
    model1 = "法院名称:{},裁判日期:{}"
    model2 = "searchWord+{0}+SLFY++法院名称:{0}&conditions=searchWord++CPRQ++裁判日期:{1}"
    # startDate = sys.argv[2]
    startDate = "2017-03-11"
    # court = sys.argv[1]
    court = "北京市石景山区人民法院"

    wf = open("case_number.txt", "a+")

    while True:
        i = 1;
        while True:
            # 实例化并开启调试模式，会返回报错信息
            spider = SpiderManager(debug=True)
            # 设置采集条件
            spider.setconditions(model2.format(court, startDate))
            spider.setParam(model1.format(court, startDate))
            # spider.setconditions("searchWord+1+AJLX++案件类型:刑事案件")
            try:
                # 初始化
                init_status = spider.init()
                print("初始化成功")
                status = spider.getvjkl5()
                if status:
                    print("获取vjkl5成功")
                    status = spider.getContent(page=i)
                    if status:
                        print(spider.getData())
                        print(len(spider.getData()))
                        if len(spider.getData()) < 100:
                            continue
                        result = json.loads(spider.getData())
                        print(result)
                        count = 0
                        if "\"Count\":\"0\"" in result:
                            count = 0
                        else:
                            result = json.loads(result)
                            try :
                                count = int(result[0]['Count'])
                                for j in range(1, len(result)):
                                    print(result[j]["案号"])
                                    wf.write(result[j]["案号"]+"---"+startDate+"---"+court+"---"+str(i)+"\n")
                                wf.flush()
                            except KeyError:
                                print("解析数据时出错误了:")
                                wf.write("error---" + startDate + "---" + court + "---" + str(i) + "\n")
                                wf.flush()

                        i+=1
                        if count < i * 20:
                            break
                    else:
                        print("获取列表页内容失败")
                else:
                    # 自己写，重新获得getvjkl5
                    pass
            except IOError:
                print("IOError")
            except KeyError:
                print("KeyError")
            except AttributeError:
                print("AttributeError")
            # except BaseException as e:
            #     print("BaseException")
            time.sleep(5)
        startDate = string_toDatetime(startDate)
        if startDate == "":
            break






