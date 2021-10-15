# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 13:10:31 2021

@author: wang_returns
"""
#山东微缩车项目中可能调用的函数
import numpy as np

l = 45.641#20cm = 45.641 像素

#-----------------------------------------------------------------
#用纯追踪算法控制小车的舵机转角实现巡线
#输入量：摄像头坐标系下小车位置坐标（单位：像素）、预瞄点坐标（单位：像素）、小车朝向角（单位：弧度）
#输出量：小车舵机转角（单位：弧度）
def line_follower(msr, setpoint, theta_msr):
    Kp = 1 #P控制器参数（带调节）
    ##计算预瞄点相对于小车后轮的坐标
    #输入量：相对于原坐标系的坐标值（二维向量）、输出坐标系相对于原坐标系坐标（二维向量）、输出坐标系相对于原坐标系的旋转角（单位：弧度）
    #输出量：相对于输出坐标系的坐标值（二维向量）
    def frame_trans(input_coordinate, relative_coordinate, theta):
        #计算齐次坐标变换矩阵
        T = np.array([[np.cos(theta), -np.sin(theta), relative_coordinate[0]],
                     [np.sin(theta), np.cos(theta), relative_coordinate[1]],
                     [0 ,              0   ,                  1            ]])
        
        
        input_vector = np.array([[input_coordinate[0]],[input_coordinate[1]], 1])#点在原来坐标系的坐标[x,y,1]^T
        input_vector = np.array([input_coordinate[0],input_coordinate[1], 1])#点在原来坐标系的坐标[x,y,1]^T
        output_vector = np.dot(T, input_vector)#求出相对于新坐标系的坐标[x',y',1]^T
        
        return [output_vector[0], output_vector[1]]
        
        
    sp_vehicle = frame_trans(msr, setpoint, theta_msr)#得到预瞄点相对于小车后轮的坐标
    dis2sp = np.sqrt((msr[0]-setpoint[0])**2 + (msr[1]-setpoint[1])**2) #小车中心点到预瞄点的距离
    err_theta = np.arctan2(sp_vehicle[1],sp_vehicle[0]) #预瞄点与小车中心的连线与小车中轴线之间的夹角
   
    #纯追踪算法进行横向控制
    u = Kp * np.arctan2(2*l*np.sin(err_theta)/dis2sp, 1.0)
    return u

print(line_follower([1,2],[3,4], 1))

#----------------------------------------------
#编码底层控制程序，设置电机转速和舵机转角 gear:静止--0 前进--1 后退--2 direction:舵机转角
inf_direction = -45#单位：角度，待测量
sup_direction = 45
middle_direction = (inf_direction + sup_direction)/2
def send_data(gear, direction):
    #将direction转换为低8位
    direction_5_bit = int(15 + (direction - middle_direction) * 32 / (sup_direction - inf_direction))
    #给direction_5_bit限幅
    if direction_5_bit > 31:
        direction_5_bit = 31
    elif direction_5_bit < 0:
        direction_5_bit = 0

    #将电机舵机信息整合成一字节    
    comdata = gear*32 + dirction_5_bit

    #编码
    send_data = chr(int(comdata))
    return send_data


    

