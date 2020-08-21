import cv2
import numpy as np
import os
import re
from PIL import Image

# 从本地读取一段视频，并获取帧数，帧率以及时长 
def get_video_frame(video_path):
    cap=cv2.VideoCapture(video_path)
    nbFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    wait = int(1/fps * 1000/1) 
    duration = (nbFrames * fps) / 1000 
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
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
    print(frame)
    i = 0
    image_path = video_path.split('.')[0]+'/'
    if os.path.exists(image_path):
        pass
    else:
        os.mkdir(image_path) 
    print(image_path)
    
    while success :
        i = i + 1
        save_image(frame,image_path,i)
        if success:
            print('save image:',i)
        success, frame = videoCapture.read()


# 识别水印位置
def identify_watermark_location(image):
    src = cv2.imread(image)
    cv2.namedWindow("input", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("input", src)
    """
    提取图中的红色部分
    """
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    low_hsv = np.array([0,43,46])
    high_hsv = np.array([10,255,255])
    mask = cv2.inRange(hsv,lowerb=low_hsv,upperb=high_hsv)
    cv2.imshow("test",mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 通过点击获取这个点的像素色彩信息，也就是RGB值
def pic_bgr(image):
    img = cv2.imread(image)

    def click_info(event, x, y, flags, param):
        # 只处理双击事件
        if event == cv2.EVENT_LBUTTONDBLCLK:
            print('坐标', x, y)
            b, g, r = img[y, x]     # 获取b, g, r
            print("像素点的bgr值", b, g, r)

    cv2.namedWindow('image')
    cv2.setMouseCallback('image',  click_info)

    while True:
        cv2.imshow("image", img)
        # 点击 esc键
        if cv2.waitKey(20) & 0xFF ==27:
            break

    cv2.destroyAllWindows()

# 图片连成视频
def pic_to_video(image_path,fps):
    file_dir=image_path
    img_list=[]
    for root,dirs,files in os.walk(file_dir):
        for file in files:
            img_list.append(file)  #获取目录下文件名列表
    img_list.sort(key=lambda i: int(re.match(r'(\d+)', i).group()))

    video=cv2.VideoWriter('video/test.avi',cv2.VideoWriter_fourcc(*'MJPG'),fps,(1280,720))  #定义保存视频目录名称及压缩格式，fps=10,像素为1280*720
    for i in range(1,len(img_list)+1):
        img = Image.open(image_path+img_list[i-1]) # 打开当前路径图像
        # box1 = (0, 70, 1280, 720) # 设置图像裁剪区域 (x左上，y左上，x右下,y右下)
        box1 = (0, 10, 1280, 720) # 设置图像裁剪区域 (x左上，y左上，x右下,y右下)
        image1 = img.crop(box1) # 图像裁剪
        image1.save(image_path+img_list[i-1]) # 存储裁剪得到的图像
        img=cv2.imread(image_path+img_list[i-1])  #读取图片
        img=cv2.resize(img,(1280,720)) #将图片转换为1280*720
        video.write(img)   #写入视频

    video.release()

video_list= []
dirs = os.listdir('video')                    # 获取指定路径下的文件
for i in dirs:                             # 循环读取路径下的文件并筛选输出
    if os.path.splitext(i)[1] == ".mp4":   # 筛选csv文件
        video_list.append(i)
        nbFrames,fps,duration,frame_height,frame_width = get_video_frame('video/'+i)
        print('video/'+i,frame_height,frame_width)
        if os.path.exists(('video/'+i).replace('.mp4','')):
            pass
        else:
            extract_frame('video/'+i)
# pic_to_video('video/mda-kf7iq8rr08w8fzdr/')
# pic_bgr('video/mda-kf7iq8rr08w8fzdr/1.jpg')
# identify_watermark_location('video/mda-kf7iq8rr08w8fzdr/1.jpg')