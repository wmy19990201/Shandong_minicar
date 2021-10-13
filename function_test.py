#摄像头识别二维码并得到二维码位姿
import numpy as np
import time
import cv2
import cv2.aruco as aruco
from functions import *

font = cv2.FONT_HERSHEY_SIMPLEX #font for displaying text (below)

from digi.xbee.devices import XBeeDevice
# pygame用于获取键盘按键信息，控制发射指令
import time
# 发送信息途中会出现错误，可能子板不存在（小车没开电）
from digi.xbee.exception import TransmitException

# xbee主板的com口
PORT = "COM7"
# 波特率，主板子板要一致，如果控制多辆小车，建议115200， 9600太小
BAUD_RATE = 115200
# xbee的ni，子板要配置，主板不用配置。使用的是186固件，升级过的。
REMOTE_NODE_ID = ["8"]
# 创建一个主板对象
device = XBeeDevice(PORT, BAUD_RATE)
# 用于存储已经连接上的子板
end_device = []

device.open()
xbee_network = device.get_network()
# remote_device1 = xbee_network.discover_device("2")
for i in range(1):
    try:
        # 用于链接子板
        tmp = xbee_network.discover_device(REMOTE_NODE_ID[i])
    except ValueError:
        tmp = 0
    end_device.append(tmp)
    print(end_device)



# 选择摄像头的编号
cap = cv2.VideoCapture(0)
# 设置960*540,帧率60
cap.set(3,960)
cap.set(4,540)
cap.set(5,60)
# 添加这句是可以用鼠标拖动弹出的窗体
cv2.namedWindow('real_img', cv2.WINDOW_NORMAL)
while(cap.isOpened()):
    # 读取摄像头的画面
    ret, frame = cap.read()
    #图像高度hght与宽度wght
    hght= frame.shape[0]
    wght= frame.shape[1]
    #灰度化
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #设置预定义的字典
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
    #使用默认值初始化检测器参数
    parameters =  aruco.DetectorParameters_create()
    M = calM_3()
    #透视变换
    #gray = cv2.warpPerspective(gray,M,(hght, wght))
    
    #使用aruco.detectMarkers()函数可以检测到二维码，返回ID和标志板的4个角点坐标
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame,aruco_dict,parameters=parameters)

    #若找得到id
    if ids is not None:
        for i in range(len(corners)):
            markerCenter,pose,theta,delta_x,delta_y=location(i,corners,ids)           
            X = pose[0]
            Y = pose[1]
            #画出二维码位置与朝向
            cv2.arrowedLine(frame, (int(markerCenter[0]), int(markerCenter[1])), (int(markerCenter[0]+delta_x/2), int(markerCenter[1]+delta_y/2)), (255,0,255),5,8,0,0.2)

        #屏幕显示id
        cv2.putText(frame, "Id: " + str(ids), (0,64), font, 1, (0,255,0),2,cv2.LINE_AA) 
    
    #若找不到id
    else:
        #屏幕显示没有id
        cv2.putText(frame, "No Ids", (0,64), font, 1, (0,255,0),2,cv2.LINE_AA)
    
    cv2.imshow('real_img', frame)

    #按q退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

v = 1
ii=0
while ii < len(x1):
    if X<x1[ii] and Y<y1[ii] :
        if ii+5 < len(x1):
            input_delta = np.arctan2(y2[ii+5]-Y,x2[ii+5]-X) - theta
            print("aaaa")
        else:
            input_delta = np.arctan2(y1[-1]-Y,x1[-1]-X) - theta
    ii += 1
    input_data = v*100 + input_delta + 90
    DATA_TO_SEND = str(input_data)
    if end_device[0]:
        # 如果连接上就发送信息
        device.send_data(end_device[0], DATA_TO_SEND)
        print("bbbbb")
    else:
        print("0数据发送失败")
    time.sleep(0.01)
    print("第0段完成")
time.sleep(1)

ii=0
while ii < len(x2):
    if X<x2[ii] and Y<y2[ii] :
        v = 0
        if ii+5 < len(x2):
            input_delta = np.arctan2(y2[ii+5]-Y,x2[ii+5]-X) - theta
        else:
            input_delta = np.arctan2(y2[-1]-Y,x2[-1]-X) - theta
    ii += 1
    input_data = v*100 - input_delta + 90
    DATA_TO_SEND = str(input_data)
    if end_device[0]:
        # 如果连接上就发送信息
        device.send_data(end_device[0], DATA_TO_SEND)
    else:
        print("0数据发送失败")
    time.sleep(0.01)
    print("第0段完成")

cap.release()
cv2.destroyAllWindows()