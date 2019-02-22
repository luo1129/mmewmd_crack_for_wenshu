#!/usr/bin/env python
# coding=utf-8
import requests
import re
import time
import datetime
import sys
import json
import warnings

warnings.filterwarnings("ignore")

url_model = "https://app.itslaw.com/app/judgements?count=20&sortType=1&startIndex={0}"
search_word_model = "&conditions=searchWord%2B{0}%2B1%2B{0}"
trial_year = "&conditions=trialYear%2B2017%2B7%2B2017"
court_model = "&conditions={3}%2B{0}%2B{1}%2B{2}"

headers_model = {
    "Accept": "*/*",
    "Accept-Encoding": "br, gzip, deflate",
    "Accept-Language": "zh-cn",
    "Connection": "keep-alive",
    "Host": "app.itslaw.com",
    "User-Agent": "WuSong-iOS/3 CFNetwork/976 Darwin/18.2.0",
    "UA": "iOS_12.1.2-375*667",
    "App-Version": "9.0.1"
}
headers_login_model = {
    "Accept": "*/*",
    "Accept-Encoding": "br, gzip, deflate",
    "Accept-Language": "zh-cn",
    "Connection": "keep-alive",
    "Host": "app.itslaw.com",
    "User-Agent": "WuSong-iOS/3 CFNetwork/976 Darwin/18.2.0",
    "UA": "iOS_12.1.2-375*667",
    "App-Version": "9.0.1",
    # "Hanukkah-UserId": "c1883ba0-509e-4b29-ba19-c4142b134a90",
    # "Victory-UserId": "89d88b68-9210-422d-b119-edd5f2eda685",
    # "WuSong-UserI": "5095721d-5272-4083-8436-f9d91922ab2e"
}

cookies = {'gr_user_id': "001b1fbd-ac64-448d-951a-2a57c632813d"}

date = "二〇一七年一月一日"


def getFirstList():
    index = 0;
    url = url_model.format(index) + search_word_model.format(date) + trial_year;
    print(url)
    headers = headers_model
    # headers['DeviceId'] = "ZRSOCIXHMJD7LNJ3FSR5PSQ26Y"
    while True:
        try:
            rsp = requests.get(url, headers=headers, cookies=cookies, timeout=(3, 7), verify=False)
            result = json.loads(rsp.content)
            for region in result['data']['judgementSearchResultInfo']['filterSearchConditions']:
                if region['label'] in '地域':
                    return region['children']
        except Exception as e:
            print(e)


def getRegionData(id, type, label, count, cr, model, wf):
    download_count = 0;
    print(label + "---" + date)
    while download_count < count:
        try:
            url = url_model.format(download_count) + search_word_model.format(date) + trial_year + model.format(
                id, type, label, cr);
            headers = headers_model
            # headers['DeviceId'] = "ZRSOCIXHMJD7LNJ3FSR5PSQ26Y"
            if download_count > 0:
                headers['token'] = "3cd6397c-6a61-44f2-ad80-39289f8fe812"
            rsp = requests.get(url, headers=headers, cookies=cookies, timeout=(3, 7), verify=False)
            result = json.loads(rsp.content)
            if result['data']['judgementSearchResultInfo']['totalCount'] == 0:
                wf.write("error+++" + url + "\n")
            else:
                download_count += len(result['data']['judgementSearchResultInfo']['judgements'])
                for case in result['data']['judgementSearchResultInfo']['judgements']:
                    wf.write(case["id"] + "+++" + case["title"] + "\n")
            wf.flush()
            print(result['data']['judgementSearchResultInfo']['judgements'])
            time.sleep(5)
        except Exception as e:
            print(e)
            # return False


def toChinese(num):
    num_dict = {'1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '七', '8': '八', '9': '九', '0': '〇', }
    index_dict = {1: '', 2: '十', 3: '百', 4: '千', 5: '万', 6: '十', 7: '百', 8: '千', 9: '亿'}
    nums = list(num)
    nums_index = [x for x in range(1, len(nums) + 1)][-1::-1]

    str = ''
    for index, item in enumerate(nums):
        str = "".join((str, num_dict[item], index_dict[nums_index[index]]))

    str = re.sub("零[十百千零]*", "零", str)
    str = re.sub("零万", "万", str)
    str = re.sub("亿万", "亿零", str)
    str = re.sub("零零", "零", str)
    str = re.sub("零\\b", "", str)
    # if len(str) == 1:
    #     str = '〇'+str
    return str


def getNextDate(str_date, n):
    d = datetime.datetime.strptime(str_date, '%Y-%m-%d')
    delta = datetime.timedelta(days=n)
    n_days = d + delta
    date_str = str(n_days.year).replace("0", "〇").replace("1", "一").replace("2", "二").replace("3", "三").replace("4",
                                                                                                                "四") \
        .replace("5", "五").replace("6", "六").replace("7", "七").replace("8", "八").replace("9", "九")
    return date_str + "年" + toChinese(str(n_days.month)) + "月" + toChinese(str(n_days.day)) + "日"


if __name__ == '__main__':
    startDate = sys.argv[1]
    endDate = getNextDate(sys.argv[2], 0)
    i = 0

    while True:
        date = getNextDate(startDate, i)
        i += 1
        if date in endDate:
            print(date)
            break
        wf = open("case_number-" + date + ".txt", "a+")
        regions = getFirstList()
        for province in regions:
            if province['count'] < 21:
                id = province['id']
                search_type = province['searchType']
                label = province['label']
                type = province['type']
                getRegionData(id, search_type, label, province['count'], type, court_model, wf)
            else:
                cities = province['children']
                for city in cities:
                    if city['count'] < 21:
                        id = city['id']
                        search_type = city['searchType']
                        label = city['label']
                        if '高级人民法院' in label:
                            getRegionData(id, search_type, label, city['count'], 'court', court_model, wf)
                        else:
                            getRegionData(id, search_type, label, city['count'], 'region', court_model, wf)
                    else:
                        courts = city['children']
                        for court in courts:
                            id = court['id']
                            search_type = court['searchType']
                            label = court['label']
                            type = court['type']
                            getRegionData(id, search_type, label, court['count'], type, court_model, wf)
