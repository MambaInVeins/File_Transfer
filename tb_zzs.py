import requests

def tz_zzs():
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
        'Cookie':'miid=757578951477544117; cna=JOAhF+sDrhsCATFNnDs+IFdN; isg=BMPDML1xmdsLRlX8kIJSzb1fUYdtOFd6veyRjfWiiyLVtOnWfQr-yApmKsT6D69y; l=eBP5FpuPQ-lqDXXSBO5CPurza779uQRVlkPzaNbMiInca6O5shuN1NQDlP0k-dtfgt5YJetzhriIydEy5WaT5xaEMIZDqeAm1Lv6Se1..; tfstk=ci9FB_G_JvHELhWAK96PViCg6kKdZHJkLR7FtIgIs65r__5GimzRjyPPbNP-e6f..; sgcookie=E21OAFnNMjiJkP1s9bom6; uc3=vt3=F8dBxGGVruoVZ10oBsA%3D&id2=UUjYHtv0jVqsNg%3D%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D&nk2=1z9KmIGtKmgjCTYNcC8R%2FQ%3D%3D; lgc=%5Cu5927%5Cu9EC4%5Cu5C0F%5Cu9EC4%5Cu963F%5Cu9EC4%5Cu9EC4%5Cu9EC4; uc4=nk4=0%401fCxqUDFQVXKwO4oXPsPc9WOjdEjQ%2FxUA%2F0a&id4=0%40U2o67ZkIzhh5FZbNsTW0cwhgRkbS; tracknick=%5Cu5927%5Cu9EC4%5Cu5C0F%5Cu9EC4%5Cu963F%5Cu9EC4%5Cu9EC4%5Cu9EC4; _cc_=VT5L2FSpdA%3D%3D; enc=CFzonbTaDrt%2BGqujrXfzgRNO952GD6wl4bhLCJxnGnGZzsu4Aw9m416EYMs7BI%2FZJB2UTowf1ARZVoQjvwv6wg%3D%3D; mt=ci=19_1; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; _m_h5_tk=f0ee6498b97ba48f13b8b58ec8b102b3_1592712316068; _m_h5_tk_enc=3907684e22649b129052d5964ef0cf22; JSESSIONID=207C2BB951297CFC3D1062D446993FE0; cookie2=168e64f8772562c28299598736fcde4b; t=b83ea353988afb1b1c48e6551a18a46d; _tb_token_=e6b4300be717e'
    }

    response = requests.get('https://shopsearch.taobao.com/search?q=%E9%92%88%E7%BB%87%E8%A1%AB&js=1&initiative_id=staobaoz_20200623&ie=utf8',headers=headers)
    # print(response.text)
    with open('1.txt','w',encoding='utf-8') as f:
        f.write(response.text)

tz_zzs()