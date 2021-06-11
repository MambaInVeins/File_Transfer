import requests
import urllib3
from lxml import etree

urllib3.disable_warnings() #忽略https证书告警
headers = {
    'Cookie': '登录后获取自己cookie',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://fofa.so/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
}

# fofa搜索结果url，qbase是搜索内容的base64加密结果，page_size是每页多少个，page是页数
base_url = "https://fofa.so/result?qbase64=Ii9zZWxsZXIucGhwP3M9L1B1YmxpYy9sb2dpbiIgJiYgaXNfZG9tYWluPXRydWU%3D&page_size=50&page="

def get_domainList(url):
    response = requests.get(url=url, verify=False, headers=headers)
    selector = etree.HTML(response.text)
    domainList = selector.xpath('//span[@class="aSpan"]/a/text()')
    # print("domainlist:", domainList)
    return domainList

def get_IPLIst(url):
    response = requests.get(url=url, verify=False, headers=headers)
    selector = etree.HTML(response.text)
    IPList = selector.xpath('//div[@class="contentMain"]/div[@class="contentLeft"]/p[2]/a[@class="jumpA"]/text()')
    # print("iplist:", IPList)
    return IPList

def write_list(listName, filename):
    f = open(filename, 'a', encoding='utf-8')
    print("writeing in : ", filename)
    for list1 in listName:
        print(list1)
        f.write(list1 +('\n'))
    f.close()

def main():
    for i in range(1, 6):
        url = base_url+str(i)
        domainList = get_domainList(url)
        IPList = get_IPLIst(url)
        write_list(domainList, "./save_file/shiziyuSQL-domainList.txt")
        write_list(IPList, "./save_file/shiziyuSQL-IPList.txt")
    print("save success!")

if __name__ == '__main__':
    main()