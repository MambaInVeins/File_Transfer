import cv2
import numpy as np
import os
import re
from PIL import Image
import shutil
import pymysql
import requests

from qiniu import Auth, put_file, etag
from qiniu import BucketManager
import qiniu.config
import json
import jsonpath
import time


frame_list = [[960, 544], [1280, 720], [404, 720], [600, 450], [408, 720], [640, 480], [1268, 720],[720,544]]

# 从本地读取一段视频，并获取帧数，帧率以及时长 
def get_video_frame(video_path):
    cap=cv2.VideoCapture(video_path)
    nbFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    wait = int(1/fps * 1000/1) 
    duration = (nbFrames * fps) / 1000 
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # print('Num. Frames = ',nbFrames)
    # print('Frame Rate = ', fps, 'fps')
    # print('Duration = ', duration, 'sec') 
    # print('Height = ', frame_height) 
    # print('Width = ', frame_width) 
    return(nbFrames,fps,duration,frame_height,frame_width)

# 视频提取每一帧
def extract_frame(video_path):
    def save_image(image,addr,num):
        address = addr + str(num)+ '.jpg'
        cv2.imwrite(address,image)
    
    # 读取视频文件
    videoCapture = cv2.VideoCapture(video_path)
    #读帧
    success, frame = videoCapture.read()
    # print(frame)
    i = 0
    image_path = video_path.split('.')[0]+'/'
    if os.path.exists(image_path):
        pass
    else:
        os.mkdir(image_path) 
    
    while success :
        i = i + 1
        save_image(frame,image_path,i)
        if success:
            # print('save image:',i)
            pass
        success, frame = videoCapture.read()

# 根据视频大小裁剪
def classify_video_size(frame_width,frame_height):
    # print(frame_width,frame_height)
    if [frame_width,frame_height]==[960,544]:
        # 205,50
        x1,y1,x2,y2 = 0,50,frame_width,frame_height
    elif [frame_width,frame_height]==[1280, 720]:
        # 575,85
        x1,y1,x2,y2 = 0,85,frame_width,frame_height
    elif [frame_width,frame_height]==[404, 720]:
        # 85,25
        x1,y1,x2,y2 = 0,25,frame_width,frame_height
    elif [frame_width,frame_height]==[600, 450]:
        # 138,40
        x1,y1,x2,y2 = 0,40,frame_width,frame_height
    elif [frame_width,frame_height]==[408, 720]:
        # 85,25
        x1,y1,x2,y2 = 0,25,frame_width,frame_height
    elif [frame_width,frame_height]==[640, 480]:
        # 135,40
        x1,y1,x2,y2 = 0,40,frame_width,frame_height
    elif [frame_width,frame_height]==[1268, 720]:
        # 270,85
        x1,y1,x2,y2 = 0,85,frame_width,frame_height
    elif [frame_width,frame_height]==[720, 544]:
        # 147,45
        x1,y1,x2,y2 = 0,45,frame_width,frame_height
    else:
        pass
    return x1,y1,x2,y2

# 图片裁剪并连成视频
def pic_to_video(image_path,video_name,fps,frame_width,frame_height):
    file_dir=image_path
    img_list=[]
    for root,dirs,files in os.walk(file_dir):
        for file in files:
            img_list.append(file)  #获取目录下文件名列表
    img_list.sort(key=lambda i: int(re.match(r'(\d+)', i).group()))

    # video=cv2.VideoWriter('video/{}.avi'.format(video_name),cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'),fps,(frame_width,frame_height))  #定义保存视频目录名称及压缩格式，fps=10,像素为1280*720
    video=cv2.VideoWriter('video/{}-yz.mp4'.format(video_name),cv2.VideoWriter_fourcc(*'mp4v'),fps,(frame_width,frame_height))  #定义保存视频目录名称及压缩格式，fps=10,像素为1280*720
    # video=cv2.VideoWriter('video/{}-yz.mp4'.format(video_name),-1,fps,(frame_width,frame_height))  #定义保存视频目录名称及压缩格式，fps=10,像素为1280*720
    x1,y1,x2,y2 = classify_video_size(frame_width,frame_height)
    for i in range(1,len(img_list)+1):
        img = Image.open(image_path+img_list[i-1]) # 打开当前路径图像
        box1 = (x1,y1,x2,y2) # 设置图像裁剪区域 (x左上，y左上，x右下,y右下)
        image1 = img.crop(box1) # 图像裁剪
        image1.save(image_path+img_list[i-1]) # 存储裁剪得到的图像
        img=cv2.imread(image_path+img_list[i-1])  #读取图片
        img=cv2.resize(img,(frame_width,frame_height)) #将图片转换为1280*720
        video.write(img)   #写入视频

    video.release()

# 递归删除目录下文件和文件夹
def del_file(rootdir):
    filelist=os.listdir(rootdir)                #列出该目录下的所有文件名
    for f in filelist:
        filepath = os.path.join( rootdir, f )   #将文件名映射成绝对路劲
        if os.path.isfile(filepath):            #判断该文件是否为文件或者文件夹
            os.remove(filepath)                 #若为文件，则直接删除
            print(str(filepath)+" removed!")
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath,True)        #若为文件夹，则删除该文件夹及文件夹内所有文件
            print("dir "+str(filepath)+" removed!")

def qiniu_is_exist(data):
    # 七牛的配置信息
    access_key = 'qeg4bbEkVHLA5eAttv7L5HBeTQ5MtMBzaiU-LcI1'
    secret_key = 'Nvcak_xnLn2S1Z4UuXnwkZiAgqPSUUW5PucbYte9'
    # 空间名
    bucket_name = 'huka'

    q = Auth(access_key, secret_key)

    # 定义文件的key
    pwd = os.getcwd()
    key = data

    # 判断七牛key是否已经存在
    buc = BucketManager(q)
    res, info1 = buc.stat(bucket_name, key)
    if(res != None):
        # exit(res.text)
        return True
    else:
        return False

def qiniu_upload_file(data):
    """
    上传文件
    :param data: 要上传的bytes类型数据
    :return:
    """
    # 七牛的配置信息
    access_key = 'qeg4bbEkVHLA5eAttv7L5HBeTQ5MtMBzaiU-LcI1'
    secret_key = 'Nvcak_xnLn2S1Z4UuXnwkZiAgqPSUUW5PucbYte9'
    # 空间名
    bucket_name = 'huka'

    q = Auth(access_key, secret_key)

    # 定义文件的key
    pwd = os.getcwd()
    key = data


    # 上传文件的地址
    localfile  = pwd+'/'+data
    if(os.path.exists(localfile) == False):
        print('文件不存在')
        return False
    # 获取上传的token
    token = q.upload_token(bucket_name, key, 36000000)

    # 上传文件
    ret, info = put_file(token, key, localfile)
    if(ret == None):
        # 上传失败
        print(res.text)
        return False
    print('{} 上传成功'.format(data))
    return True

def video_watermark_remove(video):
    video = video.split('/')[-1]
    video_name = video.replace('.mp4','')
    data ='video/{}-yz.mp4'.format(video_name)
    nbFrames,fps,duration,frame_height,frame_width = get_video_frame('video/'+video)
    if [frame_width,frame_height] not in frame_list:
        frame_list.append([frame_width,frame_height])
        print('video/'+video,frame_width,frame_height)
    else:
        img_path = 'video/'+video_name+'/'
        if os.path.exists(img_path):
            pass
        else:
            extract_frame('video/'+video)
        pic_to_video(img_path,video_name,fps,frame_width,frame_height)
    return data


def main():
    conn = pymysql.connect(host='ihome.qicp.vip', user="root",password="yuezhu008",database="yuezhu",charset="utf8",port=33336)
    cursor = conn.cursor()
    sql = "select rental_title,url,videourl from rental_house where videourl != '';"
    cursor.execute(sql)
    houses = cursor.fetchall()
    for house in houses:
        print(house)
        try:
            rental_title = house[0]
            url = house[1]
            videourl = house[2]
            if videourl.startswith('https://cdn.zhu6.com'):
                pass
            else:
                video_name = videourl.split('/')[-1]
                video = requests.get(videourl).content
                with open('video/'+video_name,'wb') as video_file:
                    video_file.write(video)
                data ='video/{}-yz.mp4'.format(video_name.replace('.mp4',''))
                is_exist = qiniu_is_exist(data)
                if is_exist==True:
                    print('已在云端')
                else:
                    data = video_watermark_remove('video/'+video_name)
                    qiniu_upload_file(data)
                    videourl_update = 'https://cdn.zhu6.com'+'/'+data
                    sql = """update rental_house set videourl ='{}' where url='{}';""".format(videourl_update,url)
                    print(videourl_update,sql)
                    cursor.execute(sql)
                    conn.commit()
        except Exception as e:
            print(e)
        del_file('video')
    cursor.close()
    conn.close()
                

if __name__=='__main__':
    # download_video()

    # qiniu_upload_file('/video/mda-kgqqviqpcwigp50p.avi')
    # a = qiniu_is_exist('video/mda-kgqqviqpcwi1213gp50p.flv')
    # print(a)
    del_file('video')
    main()
