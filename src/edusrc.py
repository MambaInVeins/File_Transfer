import requests
import re
from bs4 import BeautifulSoup
from threading import Thread, Lock
from requests.adapters import HTTPAdapter

requests.packages.urllib3.disable_warnings()
req = requests.Session()
req.mount('http://', HTTPAdapter(max_retries=3))
req.mount('https://', HTTPAdapter(max_retries=3))

class GetInfo(Thread):
    def __init__(self, pages, url):
        super().__init__()
        self.daemon = True
        self.pages = pages
        self.url = url
        self.lock = Lock()
    
    def run(self):
        for i in self.pages:
            url = self.url + "/rank/firm/?page=%d" % i
            res = req.get(url)
            soup = BeautifulSoup(res.text,'html.parser')
            schools = soup.find_all('tr',class_='row')
            for school in schools:
                school_id = school.find('a').get('href').split('/')[-1]
                school_name = school.find('a').get_text()
                school_vuln_number = school.find_all('td')[2].get_text()
                school_vuln_value = school.find_all('td')[3].get_text()
                # self.lock.acquire()
                # try:
                #     school_list.append(school_name)
                # finally:
                #     self.lock.release()
                school_list.append(school_name)
                if len(school_list) % 100 == 0:
                    print(len(school_list))

class Edusrc(object):
    def __init__(self):
        self.baseurl = "https://src.sjtu.edu.cn"
        # 单线程
        # self.dumpsSchoolInfo() 
        # 多线程
        self.dumpsSchoolInfo_multithreading(20)

    def dumpsSchoolInfo(self):
        url = self.baseurl + "/rank/firm/"
        res = req.get(url)
        soup = BeautifulSoup(res.text,'html.parser')
        maxPage = int(soup.find('ul',class_='am-pagination').find_all('li')[-2].get_text())
        pagelist = [_ for _ in range(1,maxPage+1)]
        for i in pagelist:
            url = self.baseurl + "/rank/firm/?page=%d" % i
            res = req.get(url)
            soup = BeautifulSoup(res.text,'html.parser')
            schools = soup.find_all('tr',class_='row')
            school_list = []
            for school in schools:
                school_id = school.find('a').get('href').split('/')[-1]
                school_name = school.find('a').get_text()
                school_vuln_number = school.find_all('td')[2].get_text()
                school_vuln_value = school.find_all('td')[3].get_text()
                # print(school_id,school_name,school_vuln_number,school_vuln_value)
                school_list.append(school_name)
            with open("schools.txt", "a+") as f:
                for school in school_list:
                    f.write(school+'\n')

    def dumpsSchoolInfo_multithreading(self,t=20):
        url = self.baseurl + "/rank/firm/"
        res = req.get(url)
        soup = BeautifulSoup(res.text,'html.parser')
        maxPage = int(soup.find('ul',class_='am-pagination').find_all('li')[-2].get_text())
        pagelist = [_ for _ in range(1,maxPage+1)]
        threads = [GetInfo(pagelist[i:i+t], self.baseurl) for i in range(0,maxPage + 1,t)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        with open("schools.txt", "a+") as f:
            for school in school_list:
                f.write(school+'\n')

    def dumpVulnList(self):
        url = self.baseurl + "/rank/firm/"
        res = req.get(url)
        soup = BeautifulSoup(res.text,'html.parser')
        maxPage = int(soup.find('ul',class_='am-pagination').find_all('li')[-2].get_text())
        pagelist = [_ for _ in range(1,maxPage+1)]
        for i in pagelist:
            url = self.baseurl + "/rank/firm/?page=%d" % i
            res = req.get(url)
            soup = BeautifulSoup(res.text,'html.parser')
            schools = soup.find_all('tr',class_='row')
            school_list = []
            for school in schools:
                school_id = school.find('a').get('href').split('/')[-1]
                school_name = school.find('a').get_text()
                school_vuln_number = school.find_all('td')[2].get_text()
                school_vuln_value = school.find_all('td')[3].get_text()
                # print(school_id,school_name,school_vuln_number,school_vuln_value)
                school_list.append(school_name)
            with open("schools.txt", "a+") as f:
                for school in school_list:
                    f.write(school+'\n')

def baidu_edu_url():
    schools = open('school_list.txt','r').readlines()
    url = 'https://www.baidu.com/s?wd=' 
    headers = {
        'Host': 'www.baidu.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Connection': 'keep-alive',
        'Cookie': 'BAIDUID=12498D68130BECF2FE51970B2321281C:FG=1; __yjs_duid=1_7803913921d802b85e48f1f45ab56ae41621300756608; BIDUPSID=12498D68130BECF2FE51970B2321281C; PSTM=1621304151; H_PS_PSSID=33984_33848_33772_33607_26350_34025; BD_UPN=133352; BDSFRCVID=HN8OJeC62CR6wVoem-_WbQe5Fe0ogz5TH6f3H5K4F36-0DXv0n9uEG0PHf8g0Ku-MvZMogKKL2OTHm_F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=JbkfVI_XJKvbfP0kM-oMMt_HhMQaetJyaR372DnvWJ5TMCoJ06jb3448hecdL-jI5RTl0CJO5-FhShPCb6b1jfn3QG-qe6ORyTFjWDTa3l02VhnIe-t2ynQDXqjzW4RMW23roq7mWn6rsxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJEjj6jK4JKDGDHtjQP; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; ab_sr=1.0.0_ZGM2Njc3M2FiNTc4YmQ2M2RhYWI1OGVkNDNkZTM5NGQwYTM1YmM1MmU3M2JmMjVkZDY0OWI3OTJkMDViODA0ODY0ZDEwNDNmOTUxNGY4YjEzNjU0ZWI2YTU1Zjg0Y2M3; H_PS_645EC=4ba7PAU5V0eAQtRTjJFfSki8LoaEwlhy6T1fq3ajE%2Fik1wCTjF0Sm%2FDyhk4; BA_HECTOR=ah04akal80ak2h0k4r1gas0lo0q; delPer=0; BD_CK_SAM=1; PSINO=7; BDSVRTM=0; ZD_ENTRY=baidu'
    }
    for school in schools:
        school = school.strip('\n')
        school_url = url + school
        res = req.get(school_url,headers=headers)
        soup = BeautifulSoup(res.text,'html.parser')
        try:
            edu_links = soup.find('div',id='content_left').find_all('h3')
            for item in edu_links:
                if '官方' in item.get_text():
                    edu_url = item.find('a').get('href')
                    try:
                        edu_url = req.get(edu_url,verify=False).url.strip('/')
                        print(school,edu_url)
                        with open('school_url.txt','a+') as f:
                            f.write(school + ':' + edu_url + '\n')
                    except Exception as e:
                        print(e)
        except:
            pass

if __name__ == "__main__":
    school_list = []
    # 获取edusrc学校列表 schools.txt
    # edusrc = Edusrc()
    baidu_edu_url()