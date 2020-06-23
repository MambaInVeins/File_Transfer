import requests
import re
import urllib.parse
import json
import sqlite3

class tbzzs:
    def conn_sqlite3(self):
        self.conn = sqlite3.connect('data.db')
        print("Opened database successfully")
        self.cursor = self.conn.cursor()

    def create_table(self):
        sql = 'CREATE TABLE shop(id integer PRIMARY KEY autoincrement, name varchar(30), shopurl varchar(30) UNIQUE, nick varchar(30), provcity varchar(30), totalsold integer)'
        self.cursor.execute(sql)
        self.conn.commit()

    def insert_data(self,data):
        sql = 'INSERT INTO shop(name,shopurl,nick,provcity,totalsold) values (?,?,?,?,?)'
        self.cursor.execute(sql, data)
    
    def commit_data(self):
        self.conn.commit()

    def close_db(self):
        self.conn.close()

    def crawl(self):
        f = open('provcity.txt','r')
        keywordlist = f.readlines()
        keywordlist = ''.join(keywordlist).strip('\n').splitlines()
        for keyword in keywordlist:
            keyword = '针织衫 ' + keyword
            for page_offset in range(0,200,20):
                flag = self.crawl_page(keyword,page_offset)
                if flag == False:
                    break
                print(keyword,(page_offset/20+1))
            self.commit_data()
        self.close_db()

    def crawl_page(self,search_keyword,page_offset):
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
            'Cookie':'miid=757578951477544117; cna=JOAhF+sDrhsCATFNnDs+IFdN; isg=BMPDML1xmdsLRlX8kIJSzb1fUYdtOFd6veyRjfWiiyLVtOnWfQr-yApmKsT6D69y; l=eBP5FpuPQ-lqDXXSBO5CPurza779uQRVlkPzaNbMiInca6O5shuN1NQDlP0k-dtfgt5YJetzhriIydEy5WaT5xaEMIZDqeAm1Lv6Se1..; tfstk=ci9FB_G_JvHELhWAK96PViCg6kKdZHJkLR7FtIgIs65r__5GimzRjyPPbNP-e6f..; sgcookie=E21OAFnNMjiJkP1s9bom6; uc3=vt3=F8dBxGGVruoVZ10oBsA%3D&id2=UUjYHtv0jVqsNg%3D%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D&nk2=1z9KmIGtKmgjCTYNcC8R%2FQ%3D%3D; lgc=%5Cu5927%5Cu9EC4%5Cu5C0F%5Cu9EC4%5Cu963F%5Cu9EC4%5Cu9EC4%5Cu9EC4; uc4=nk4=0%401fCxqUDFQVXKwO4oXPsPc9WOjdEjQ%2FxUA%2F0a&id4=0%40U2o67ZkIzhh5FZbNsTW0cwhgRkbS; tracknick=%5Cu5927%5Cu9EC4%5Cu5C0F%5Cu9EC4%5Cu963F%5Cu9EC4%5Cu9EC4%5Cu9EC4; _cc_=VT5L2FSpdA%3D%3D; enc=CFzonbTaDrt%2BGqujrXfzgRNO952GD6wl4bhLCJxnGnGZzsu4Aw9m416EYMs7BI%2FZJB2UTowf1ARZVoQjvwv6wg%3D%3D; mt=ci=19_1; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; _m_h5_tk=f0ee6498b97ba48f13b8b58ec8b102b3_1592712316068; _m_h5_tk_enc=3907684e22649b129052d5964ef0cf22; JSESSIONID=207C2BB951297CFC3D1062D446993FE0; cookie2=168e64f8772562c28299598736fcde4b; t=b83ea353988afb1b1c48e6551a18a46d; _tb_token_=e6b4300be717e'
        }
        search_keyword = urllib.parse.quote(search_keyword)
        response = requests.get('https://shopsearch.taobao.com/search?q={}&js=1&initiative_id=staobaoz_20200623&ie=utf8&s={}'.format(search_keyword,page_offset),headers=headers)
        print(response.text)
        query_result = re.findall('g_page_config = (.*?);\s+g_srp_loadCss\(\)',response.text)[0]
        if '"shoplist":{"status":"hide"}' in query_result:
            print('上限')
            return False
        else:
            data = json.loads(query_result)
            shops = data["mods"]["shoplist"]["data"]["shopItems"]
            for shop in shops:
                data = (shop["title"],shop["shopUrl"][2:],shop["nick"],shop["provcity"],shop["totalsold"])
                print(data)
                try:
                    self.insert_data(data)
                except Exception as e:
                    print(e)
            return True
            
            


if __name__ == "__main__":
    tbzzs = tbzzs()
    tbzzs.conn_sqlite3()
    # tbzzs.create_table()
    # tbzzs.crawl()
    tbzzs.crawl_page('针织衫',0)