import requests
from queue import Queue
import json, random, os, pickle
import threading
import hashlib
from bs4 import BeautifulSoup

m = hashlib.md5()
import re


def get_md5(aa):
    m.update(aa.encode(encoding='UTF-8'))
    return m.hexdigest()


try:
    with open('配置.txt', 'r')as filed:
        line_list = filed.readlines()
        peizhi = {}
        for line_ in line_list:
            line_ = line_.replace('\n', '')
            li_list = line_.split('==')
            peizhi[li_list[0]] = li_list[1]
except:
    with open('配置.txt', 'r', encoding='utf-8')as filed:
        line_list = filed.readlines()
        peizhi = {}
        for line_ in line_list:
            line_ = line_.replace('\n', '')
            li_list = line_.split('==')
            peizhi[li_list[0]] = li_list[1]


def wanzheng_douhao(word):
    word = re.sub(r'[\t\n\r ]', '', word)
    
    if len(word) < 200:
        return word
    
    word = word[:200]

    #判断句号在最后还是感叹号在最后
    period = '。'
    plaint = '！'
    periodRIndex = word.rfind(period)
    plaintRIndex = word.rfind(plaint)
    if periodRIndex == plaintRIndex == -1 or periodRIndex == plaintRIndex == 0:
        return word
    if periodRIndex > plaintRIndex:
        return word[:periodRIndex + 1]
    else:
        return word[:plaintRIndex + 1]


def get_one(ans_id):
    url = 'https://www.wukong.com/question/{}/'.format(ans_id)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
    res = requests.get(url, headers=headers)
    html = res.text
    html = html.encode("ISO-8859-1")
    html = html.decode("utf-8")

    retContent = []

    try:
        targetText = html.split('<script>window.__INITIAL_STATE__=')[1]
        targetText = targetText.split('</script>', 1)[0]

        targetJson = json.loads(targetText)
        # contentRaw = targetJson['qData']['data']['ans_list'][0]['content']
        ansLists = targetJson['qData']['data']['ans_list']
        for ansItem in ansLists:
            contentRaw = ansItem['content']
            content = re.sub('<[^<]+?>', '', contentRaw).replace('\n', '').strip()
            if 'PGC_VIDEO' in content or not len(content) > 10:
                continue
            content = wanzheng_douhao(content)
            # if content[-1] not in '。！？’”':
            #     content += '。'

            with open('qucong.txt', 'rb')as filed:
                qucong = pickle.load(filed)

            m1 = get_md5(content)
            if m1 in qucong:
                continue

            qucong.add(m1)
            with open('qucong.txt', 'wb')as filed:
                pickle.dump(qucong, filed)

            retContent.append(content)
            break
    except Exception as e:
        retContent = []

    return retContent


# if os.path.exists('qucong.txt'): os.remove('qucong.txt')
if not os.path.exists('qucong.txt'):
    with open('qucong.txt', 'wb')as filed:
        qucong = set()
        qucong.add(1)
        pickle.dump(qucong, filed)


def read_zh():
    gjc_list = []
    try:
        with open('搜索关键词.txt', 'r') as f1:
            for zh in f1.readlines():
                zh2 = zh.strip('\n')
                gjc_list.append(zh2)
    except:
        with open('搜索关键词.txt', 'r', encoding='utf-8') as f1:
            for zh in f1.readlines():
                zh2 = zh.strip('\n')
                gjc_list.append(zh2)
    print(gjc_list)
    return gjc_list


def get_baidu(keyword):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'PSTM=1586959446; BAIDUID=280A1327FC40A228BC7CE2CBF6FD363AFG=1; delPer=0; BD_CK_SAM=1; PSINO=3; BIDUPSID=D01D28EC40F7C74190C61538FCB5224C; H_PS_PSSID=30975_1455_31124_21091_31187_31229_30823_31164_22157; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BD_UPN=12314753; COOKIE_SESSION=334_0_3_1_0_2_0_1_3_1_0_0_0_0_0_0_0_0_1586959781%7C3%230_0_1586959781%7C1; H_PS_645EC=a5f2rIm2aa%2F4Z2gjNro4BI706mlj3noDt4yskK2xn5Q3MlXyWxUAAOIM%2F5k',
        'Host': 'www.baidu.com', 'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    url = 'https://www.baidu.com/s?wd={}'.format(keyword)
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "lxml")
        ele = soup.find_all('div', id='rs')
        div = ele[0].find_all('a')
        ress = []
        for i in div:
            ress.append(i.text)
        return ress
    except Exception as e:
        print(e)


def get_5ans_list(keyword):
    headers = {
        'Host': 'www.wukong.com',
        'Connection': 'keep-alive',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'tt_webid=6814473667024569863; wendacsrftoken=3369c7ab7c433a99e0f5c29f46b27774; tt_webid=6814473667024569863'
    }
    # ye翻页参数，默认0开始10、20、30、.........
    url = 'https://www.wukong.com/wenda/wapshare/search/brow/?search_text={0}&offset=0'.format(keyword)
    # try:
    response = requests.get(url, headers=headers)
    res_json = json.loads(response.text)
    feed_question = res_json['data']['feed_question']
    res_list = []
    try:
        for i in feed_question:
            if len(i['ans_list']) > 0:
                abstract_text = i['ans_list'][0]['abstract_text']
                abstract_text = wanzheng_douhao(abstract_text)
                # print('abstract_text', abstract_text)
                with open('qucong.txt', 'rb')as filed:
                    qucong = pickle.load(filed)
                if get_md5(abstract_text) in qucong:
                    continue

                ans_id = i['question']['qid']
                print('进入详情')
                print(ans_id)
                contentBigs = get_one(ans_id)# 返回问答列表
                for contentBig in contentBigs:
                    print(ans_id, contentBig)
                    if not contentBig: continue

                    # print([i['question']['title'], contentBig])
                    res_list.append([i['question']['title'], contentBig])
                if len(res_list) == 5:
                    return res_list
        else:
            return False
    except Exception as e:
        print(e)
        return False


def start(q):
    while True:
        if q.empty():
            print('队列为空')
            break
        keyword = q.get()
        print(keyword)
        with open('keyqucong.txt', 'r')as filed:
            keyqucong = pickle.load(filed)
        if keyword in keyqucong:
            continue
        else:
            keyqucong.add(keyword)
            with open('keyqucong.txt', 'w')as filed:
                pickle.dump(keyqucong, filed)
        ress = get_baidu(keyword)
        if ress != None:
            keyword2 = ress[0]
            keyqucong.add(keyword2)
            with open('keyqucong.txt', 'w')as filed:
                pickle.dump(keyqucong, filed)
            print(keyword2)
            if keyword2:
                print('开始采集：' + keyword)
                res_list = get_5ans_list(keyword)
                res_list2 = get_5ans_list(keyword2)
                if res_list and res_list2:
                    res_list = res_list + res_list2

                    random.shuffle(res_list)
                    if not os.path.exists('data'):
                        os.makedirs('data')
                    path_name = 'data/' + keyword + '({})'.format(keyword2) + '.txt'
                    if os.path.exists(path_name):
                        for i in range(1000):
                            path_name = 'data{0}/'.format(i) + keyword + '({})'.format(keyword2) + '.txt'
                            if not os.path.exists(path_name):
                                if not os.path.exists('data{0}/'.format(i)):
                                    os.makedirs('data{0}/'.format(i))
                                else:
                                    pass
                                break
                    with open(path_name.replace("?","？"), 'w', encoding='utf-8')as filed:
                        for wd in res_list:
                            try:
                                print('<p style="text-indent:2em">' + wd[1] + '</p>')
                                filed.writelines('<p style="text-indent:2em">' + wd[1] + '</p>')
                            except:
                                pass
                    print('-' * 30)
        else:
            print('跳过')


if __name__ == '__main__':
    # if os.path.exists('keyqucong.txt'): os.remove('keyqucong.txt')
    word_task = Queue()
    word_list = read_zh()
    if not os.path.exists('keyqucong.txt'):
        with open('keyqucong.txt', 'wb')as filed:
            qucong = set()
            pickle.dump(qucong, filed)

    for x in word_list:
        word_task.put(x)
    print('线程数：' + peizhi['线程数'])
    for i in range(int(peizhi['线程数'])):
        t1 = threading.Thread(target=start, args=[word_task])
        t1.start()
