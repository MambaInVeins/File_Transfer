import requests
import re
import urllib.parse
import json
import sqlite3
import time
from lxml import etree
from bs4 import BeautifulSoup

class beike:
    def __init__(self):
        # self.domain = 'https://nj.zu.ke.com/zufang/pg1'
        self.domain = 'http://nj.rent.house365.com'


    def conn_sqlite3(self):
        self.conn = sqlite3.connect('nj_rent_house365.db')
        print("Opened database successfully")
        self.cursor = self.conn.cursor()

    def create_table(self):
        # 名称 价格 位置 大小 朝向 户型 楼层 标签 品牌 维护时间 房源链接 入住 电梯 车位 用水 用电 燃气 采暖 租期 看房 配套设置 联系人 联系方式
        sql = 'CREATE TABLE house(id integer PRIMARY KEY autoincrement, name varchar(30), price integer ,location varchar(30),area varchar(30),orientations varchar(30),layout varchar(30),storey varchar(30),label varchar(30),brand varchar(30),time varchar(30),houseurl varchar(50),check_in varchar(30),elevator varchar(30),parking varchar(30),water varchar(30),electric varchar(30),gas varchar(30),heat varchar(30),rant_term varchar(30),house_watch varchar(30),support varchar(30),contact varchar(30),phone varchar(30))'
        self.cursor.execute(sql)
        self.conn.commit()

    def insert_data(self,data):
        sql = 'INSERT INTO house(name, price,location,area,orientations,layout,storey,label,brand,time,houseurl,check_in,elevator,parking,water,electric,gas,heat,rant_term,house_watch,support,contact,phone) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        self.cursor.execute(sql, data)
    
    def commit_data(self):
        self.conn.commit()

    def close_db(self):
        self.conn.close()

    def crawl(self):
        for page in range(1,2):
            self.crawl_zufang(page)

    def crawl_zufang(self,page):
        response = requests.get(self.domain+'/district_rent/f1-n1-p%d.html'%page).text
        soup = BeautifulSoup(response, "lxml")
        houselist = soup.find_all('div',class_="z-list-item")
        for house in houselist:
            house_info = []
            # 名称
            title = house.find('div',class_="z-list-item-title z-cl").find('a').get_text().strip('\n ')
            house_url = house.find('div',class_="z-list-item-title z-cl").find('a').get('href')
            subway_tips = house.find('span',class_="subway_tips").get('data-tips')
            # 房屋亮点
            try:
                characteristic = []
                characteristic_box = house.find('div',class_="z-list-characteristic-box").find_all('div')
                for item in characteristic_box:
                    characteristic.append(item.get_text())
                characteristic = ' '.join(characteristic)
            except:
                characteristic = ''
            house_info=[title,house_url,subway_tips,characteristic]
            print(house_info)
            try:
                detail = self.crawl_detail(house_url)
            except:
                detail = []
            house_info += detail
            
            # self.insert_data(house_info)
            # self.commit_data()
            time.sleep(1)
        

    def crawl_detail(self,url):
        detail = []
        response = requests.get(url,stream=True).text
        soup = BeautifulSoup(response, "lxml")
        price = soup.find('span',class_="z-price").get_text()
        payment = soup.find('div',class_="z-price-detail").find_all('span')[-1].get_text()    
        house_detail = soup.find('div',class_="z-house--details z-cl").find_all('div',class_="z-fl")
        rent = house_detail[0].find('p').get_text()
        layout = house_detail[1].find('p').get_text()
        area = house_detail[2].find('p').get_text()
        orientations = house_detail[3].find('p').get_text()
        storey = house_detail[4].find('p').get_text().replace(' ','')
        decoration = house_detail[5].find('p').get_text()
        house_area = re.compile('\s').sub('',soup.find('div',class_="z-house-area").get_text().replace('区域',''))
        quarters = soup.find('div',class_="z-quarters").find('a').get_text()
        master_name = soup.find('div',class_="z-house-master-name").get_text().strip('\n\t\r ')
        master_phone = soup.find('div',class_="z-fl z-check-phone").get('data-phone')
        support = re.compile('\s+').sub(' ',soup.find('div',class_="z-cl z-facilities z-specific-info-block").get_text()).strip(' ')
        description = soup.find('div',class_="z-cl z-specific-info-block z-txt-decuration").get_text().strip('\n\t\r ')
        detail = [price,payment,rent,layout,area,orientations,storey,decoration,house_area,quarters,master_name,master_phone,support,description]
        return detail



if __name__ == "__main__":
    beike =beike()
    beike.conn_sqlite3()
    # beike.create_table()
    beike.crawl()