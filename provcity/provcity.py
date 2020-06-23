import requests
from bs4 import BeautifulSoup
import lxml

f = open('provcity.txt','a+')

url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/"
response_province = requests.get(url)
response_province.encoding='gb2312'
bs_province = BeautifulSoup(response_province.text,'lxml')
provinces = bs_province.find_all("a")[0:-1]
# for province in provinces[0:-1]:
for province in provinces:
    province_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/"+ province["href"]
    province_name = province.get_text()
    response_city = requests.get(province_url)
    response_city.encoding='gb2312'
    bs_city = BeautifulSoup(response_city.text,'lxml')
    citys = bs_city.find_all("a")[0:-1]
    # citys = code_citys[1::2]
    for city in citys:
        if citys.index(city) % 2 ==0:
            pass
        else:
            city_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/"+ city["href"]
            city_name = city.get_text()
            # print(city_name)
            response_district = requests.get(city_url)
            response_district.encoding='gb2312'
            bs_district= BeautifulSoup(response_district.text,'lxml')
            districts = bs_district.find_all("a")[0:-1]
            for district in districts:
                if districts.index(district) % 2 ==0:
                    pass
                else:
                    district_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/"+ district["href"]
                    district_name = district.get_text()
                    if len(citys)==2:
                        print(province_name+district_name)
                        f.write(province_name+district_name+'\n')
                    else:
                        print(city_name+district_name)
                        f.write(city_name+district_name+'\n')