# 导入pymysql模块
import pymysql
import requests
import cv2
# 连接database
# ihome.qicp.vip 121.237.225.225
conn = pymysql.connect(host='ihome.qicp.vip', user="root",password="yuezhu008",database="yuezhu",charset="utf8",port=33336)
# 得到一个可以执行SQL语句的光标对象
cursor = conn.cursor()
# 定义要执行的SQL语句
sql = """select rental_title,url,videourl from rental_house limit 100;"""
# 执行SQL语句
cursor.execute(sql)
houses = cursor.fetchall()
print(houses)
for house in houses:
    rental_title = house[0]
    url = house[1]
    videourl = house[2]
    if videourl!='':
        video_name = videourl.split('/')[-1]
        video = requests.get(videourl).content
        with open('video/'+video_name,'wb') as video_file:
            video_file.write(video)


# 关闭光标对象
cursor.close()
# 关闭数据库连接
conn.close()