import json
import random
import requests
import urllib.parse
from hashlib import md5

def content_print_byformat(js):
    srcStr = str(js["trans_result"][0]["src"])  # 取得翻译后的文本结果
    dstStr = str(js["trans_result"][0]["dst"])  # 取得翻译后的文本结果
    # 反过滤规则001
    if("\\r\\n" in srcStr):
        srcStr = srcStr.replace("\\r\\n","\n")
    if("\\r\\n" in dstStr):
        dstStr = dstStr.replace("\\r\\n","\n")
    return(dstStr)

def content_filter_word(content):
    """
    过滤内容
    """
    bb= content
    # 过滤规则001
    # 不知道是自己的原因还是百度翻译有点坑
    if("\n" in bb):
        bb = bb.replace("\n", "\\r\\n")
    return bb 

def translate_api(text):
    """英文翻译成中文"""
    appid = '20210617000865323'#你的id
    secretKey = 'B5hJKEsBMF7cYjy6_UUZ'#你的密钥
    myurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    q = text
    fromLang = 'en'
    toLang = 'zh'
    salt = random.randint(32768, 65536)
    sign = appid+q+str(salt)+secretKey
    m1 = md5()
    m1.update(sign.encode("utf-8"))
    sign = m1.hexdigest()

    myurl = myurl+'?appid='+appid+'&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    return myurl

def fanyi(text):
    myurl = translate_api(content_filter_word(text))
    response = requests.get(myurl)
    trans_result = json.loads(response.text)
    result =  content_print_byformat(trans_result)
    print(result)

if __name__=='__main__':
    text = '''The Pentagon is trying to determine how its two newest space entities - Space Command and Space Force - will fit into the Department of Defense’s cyber architecture.

There are no plans - or subsequent authorities - for Space Force to provide personnel to the cyber mission force, which feeds up to U.S. Cyber Command, a Space Force spokesperson told C4ISRNET. The way the cyber force is staffed within the Defense Department is that each of the services are responsible for providing a set number of teams – offensive, defensive and intelligence/support teams – to the joint cyber mission force.'''
    fanyi(text)
