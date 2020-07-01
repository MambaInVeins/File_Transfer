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
        self.conn = sqlite3.connect('beike_nj.db')
        print("Opened database successfully")
        self.cursor = self.conn.cursor()

    def create_table(self):
        # 名称 价格 位置 大小 朝向 户型 楼层 标签 品牌 维护时间 房源链接 入住 电梯 车位 用水 用电 燃气 采暖 租期 看房 配套设置 联系人 联系方式
        sql = 'CREATE TABLE zufang(id integer PRIMARY KEY autoincrement, name varchar(30), price integer ,location varchar(30),area varchar(30),orientations varchar(30),layout varchar(30),storey varchar(30),label varchar(30),brand varchar(30),time varchar(30),houseurl varchar(50),check_in varchar(30),elevator varchar(30),parking varchar(30),water varchar(30),electric varchar(30),gas varchar(30),heat varchar(30),rant_term varchar(30),house_watch varchar(30),support varchar(30),contact varchar(30),phone varchar(30))'
        self.cursor.execute(sql)
        self.conn.commit()

    def insert_data(self,data):
        sql = 'INSERT INTO zufang(name, price,location,area,orientations,layout,storey,label,brand,time,houseurl,check_in,elevator,parking,water,electric,gas,heat,rant_term,house_watch,support,contact,phone) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
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
            print(characteristic)
            house_info=[title,house_url,subway_tips,characteristic]
            detail = self.crawl_detail(house_url)
            house_info += detail
            print(house_info)
            # self.insert_data(house_info)
            # self.commit_data()
            # time.sleep(30)
        

    def crawl_detail(self,url):
        response = requests.get(url).text
        # house_codes=url.split('/')[-1].replace('.html','')
        soup = BeautifulSoup(response, "lxml")
        info_li = soup.find('div',id="info",class_="content__article__info").find_all('li')
        info = []
        # 入住5 电梯8 车位10 用水11 用电13 燃气14 采暖16 租期18 看房21
        for item in info_li:
            item = item.get_text()
            info.append(item)
        detail = [info[5].replace('入住：',''),info[8].replace('电梯：',''),info[10].replace('车位：',''),info[11].replace('用水：',''),info[13].replace('用电：',''),info[14].replace('燃气：',''),info[16].replace('采暖：',''),info[18].replace('租期：',''),info[21].replace('看房：','')]
        
        info2_li = soup.find('ul',class_="content__article__info2").find_all('li',class_="fl oneline")
        info2 = []
        for item in info2_li[1:]:
            item = item.get_text().strip('\n\t\r ')
            info2.append(item)
        fl = ' '.join(info2)
        detail.append(fl)
        contact_name = soup.find('span',class_="contact_name").get_text()
        contact_phone = soup.find('p',id="phone1").get_text()
        if contact_phone=='免费电话咨询':
            contact_url = 'https://nj.zu.ke.com/aj/house/brokers?house_codes='+house_codes
            response = requests.get(contact_url).text
            tp_number = re.findall('"tp_number":"(.*?),(.*?)"',response)[0]
            contact_phone = tp_number[0]+' 转 '+tp_number[1]
        detail.append(contact_name)
        detail.append(contact_phone)
        return detail



if __name__ == "__main__":
    beike =beike()
    beike.conn_sqlite3()
    # beike.create_table()
    beike.crawl()