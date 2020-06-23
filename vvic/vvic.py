# https://www.vvic.com/gz/markets.html

# 地址  电话 微信 QQ 产地 旺旺 主营

import requests
import re
import urllib.parse
import json
import sqlite3
import time

class vvic:
    def __init__(self):
        self.domain = 'https://www.vvic.com'

    def conn_sqlite3(self):
        self.conn = sqlite3.connect('vvic.db')
        print("Opened database successfully")
        self.cursor = self.conn.cursor()

    def create_table(self):
        sql = 'CREATE TABLE shop(id integer PRIMARY KEY autoincrement, name varchar(30), shopurl varchar(30) UNIQUE, category varchar(30), wangwang varchar(30),market varchar(30),tel varchar(30),qq varchar(30),address varchar(30) , wechat varchar(30) ,years integer,source varchar(30))'
        self.cursor.execute(sql)
        self.conn.commit()

    def insert_data(self,data):
        sql = 'INSERT INTO shop(name,shopurl,category,wangwang,market,tel,qq,address,wechat,years,source) values (?,?,?,?,?,?,?,?,?,?,?)'
        self.cursor.execute(sql, data)
    
    def commit_data(self):
        self.conn.commit()

    def close_db(self):
        self.conn.close()

    def crawl_market(self):
        market_url = 'https://www.vvic.com/gz/markets.html'
        response = requests.get(market_url)
        html = response.text
        markets = re.findall('<li class="item"><a target="_blank" href="(.*?)" vda="link\|content">(.*?)</a></li>',html)
        for market in markets:
            market_url = market[0]
            market_name = market[1]
            print(market_url,market_name)
            self.crawl_shops(self.domain+market_url,market_name)
            self.commit_data()
        self.close_db()

    def crawl_shops(self,market_url,market_name):
        response = requests.get(market_url)
        html = response.text
        all_shops = re.findall('<div class="mk-shops mt10">(.*?)<input id="GOLDSHOPLIST"',html,re.S)[0]
        shops = re.findall('<a class="items.*?>',all_shops)
        for shop in shops:
            data_title = re.search('data-title="(.*?)"',shop).group(1)
            href = self.domain + re.search('href="(.*?)"',shop).group(1)
            data_cate = re.search('data-cate1="(.*?)"',shop).group(1)
            data_ww = re.search('data-ww="(.*?)"',shop).group(1)
            data_market = re.search('data-market="(.*?)"',shop).group(1)
            data_tel = re.search('data-tel="(.*?)"',shop).group(1)
            data_qq = re.search('data-qq="(.*?)"',shop).group(1)
            data_address = re.search('data-address="(.*?)"',shop).group(1)
            data_wechat = re.search('data-wechat="(.*?)"',shop).group(1)
            data_years = re.search('data-years="(.*?)"',shop).group(1)
            data_source = re.search('data-source="(.*?)"',shop).group(1)
            shop_info = [data_title,href,data_cate,data_ww,data_market,data_tel,data_qq,data_address,data_wechat,data_years,data_source]
            print(data_title,data_market)
            try:
                self.insert_data(shop_info)
            except Exception as e:
                print(e)



  
            

if __name__ == "__main__":
    vvic = vvic()
    vvic.conn_sqlite3()
    # vvic.create_table()
    vvic.crawl_market()