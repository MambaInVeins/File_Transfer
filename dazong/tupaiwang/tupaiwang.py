import requests
from lxml import etree
from bs4 import BeautifulSoup
import os
import csv

class tupaiwang_spider:
    def __init__(self):
        self.path = os.path.abspath('.')
        self.domain = 'http://www.chinatupai.com'
        self.prefix = 'http://www.chinatupai.com/Mother/index.php/news,lists,cid,'
        self.url = {
            "土拍头条":self.prefix+"1",
            "国土要闻":self.prefix+"9",
            "市场快讯":self.prefix+"10",
            "城市动态":self.prefix+"12",
        }

    # 采集多页
    def crawl_pages(self,category,page_start,page_end):
        for page in range(page_start,page_end+1):
            self.crawl_page(category,page)

    # 采集单页
    def crawl_page(self,category,page):
        url = self.url[category]+',page,{}'.format(page)
        response = requests.get(url).text
        soup = BeautifulSoup(response, "lxml")
        infolist = soup.find('div',class_="list-cont").find_all('ul',class_="list")
        for info in infolist:
            url = info.find('div',class_="youbian").find('a').get('href')
            # 如果是直播，跳过
            if url.startswith('http://zhibo.chinatupai.com'):
                continue
            url = self.domain + url
            self.crawl_info(category,url)


    def crawl_info(self,category,url):
        item = {}
        response = requests.get(url).text
        soup = BeautifulSoup(response, "lxml")
        item['title'] = soup.find('div',class_="artTitle").get_text()
        item['category'] = category
        item['url'] = url
        form = soup.find('div',class_="artFrom").find_all('span')
        item['source'] = form[0].get_text()
        item['anthor'] = form[1].get_text()
        item['post_date'] = soup.find('a',class_="showtime").get_text()
        abstract  = soup.find('div',class_="artIntroduce")
        item['abstract'] = abstract.get_text().replace('摘要','').strip(' \n\r\t') if abstract!=[] else ''
        content = []
        content_box = soup.find('div',class_="artCon").find_all('p')
        for p in content_box:
            if p.find('img'):
                img_src = p.find('img').get('src')
                img_name = p.find('img').get('title')
                self.download_img(img_src,img_name)
                img_tab = "\n<img src='{}'></img>\n".format(img_name)
                content.append(img_tab)
            else:
                content.append(p.get_text())
        item['content'] = ' '.join(content)
        print(itme['title'])
        self.write_csv(item)

    def download_img(self,src,name):
        path = self.path+'/img/'
        isExists=os.path.exists(path)
        if not isExists:
            os.makedirs(path) 
        try:
            pic = requests.get(src, timeout=10)
            if os.path.exists(path+name):
                pass
            else:
                print(path+name)    
                fp = open(path+name, 'wb')
                fp.write(pic.content)
                fp.close()
        except requests.exceptions.ConnectionError:
            print('图片无法下载')
        except:
            pass

    def write_csv(self,data):
        path = self.path+'/'+'tupaiwang.csv'
        with open(path, 'a+',encoding='utf-8',errors='ignore') as f:  # Just use 'w' mode in 3.x
            w = csv.DictWriter(f, data.keys())
            # w.writeheader()
            w.writerow(data)

if __name__ == "__main__":
    spider = tupaiwang_spider()
    spider.crawl_pages("土拍头条",1,2)
    # spider.crawl_page("土拍头条",1)