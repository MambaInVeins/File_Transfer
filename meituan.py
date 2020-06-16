import json
import csv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import re
import requests

def meituan_spider():
    browser = webdriver.Firefox()
    browser.get("http://qd.meituan.com")
    browser.get("http://qd.meituan.com")
    browser.get("https://qd.meituan.com/s/%E7%BE%8E%E9%A3%9F/")
    # browser.find_element_by_class_name('header-search-input').send_keys('美食')
    # browser.find_element_by_class_name('header-search-btn').click()

    page_source = browser.page_source
    pat_content = '<script>window.AppData = (.*?);</script>'
    json = re.findall(pat_content,page_source)[0]
    print(json)
    f = open('json/meishi_1.json','w')
    f.write(json)

    for i in range(2,64):
        print(i)
        browser.find_element_by_class_name('icon-btn_right').click()
        page_source = browser.page_source
        pat_content = '<script>window.AppData = (.*?);</script>'
        json = re.findall(pat_content,page_source)[0]
        f = open('json/meishi_%d.json'%i,'w') 
        f.write(json)

def get_json():
    for i in range(32,1000,32):
        url = "https://apimobile.meituan.com/group/v4/poi/pcsearch/60?uuid=fb6cbb4f5bfe45d5a285.1592300162.1.0.0&userid=-1&limit={}&offset={}&cateId=-1&q=%E7%BE%8E%E9%A3%9F".format(i,i+32)
       
        cookies = {
            "_hc.v":"db60fb74-4c2c-09db-f8c0-4e531ff63ec5.1592300531",
            "_lxsdk_cuid":"172bc7c51570-0849c5081104b4-71226753-180dda-172bc7c5158c8",
            # "_lxsdk_s":"172bc7c5159-a0-6d3-f73||178",
            "ci":"60",
            "rvct":"60",
            "uuid":"fb6cbb4f5bfe45d5a285.1592300162.1.0.0"}
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
            'Cookie' :'uuid=fb6cbb4f5bfe45d5a285.1592300162.1.0.0; _lxsdk_cuid=172bc7c51570-0849c5081104b4-71226753-180dda-172bc7c5158c8;ci=60; rvct=60; _hc.v=db60fb74-4c2c-09db-f8c0-4e531ff63ec5.1592300531'
        }

        print(url)
        response = requests.get(url, headers = headers )
        print(response.text)

def load_json():
    for i in range(2,3):
        dicts = open('json/meishi_%d.json'%i,'r').read()
        json_dicts=json.loads(dicts)
        shops = json_dicts["data"]["searchResult"]
        for shop in shops:
            # id,title，address,avgprice,avgscore,comments,backCateName
            print(shop["id"],shop["title"],shop["address"],shop["avgprice"])

def json1():
    for i in range(5,52):
            dicts = open('json/meishi_%d.json'%i,'r').read()
            a = dicts[:-1]
            f = open('json/%d.json'%i,'w')
            f.write(a)
            # json_dicts=json.loads(dicts)
            # shops = json_dicts["data"]["searchResult"]
            # for shop in shops:
            #     # id,title，address,avgprice,avgscore,comments,backCateName
            #     print(shop["id"],shop["title"],shop["address"],shop["avgprice"])



if __name__=='__main__':
    # meituan_spider()
    get_json()
    # load_json()
    # json1()

