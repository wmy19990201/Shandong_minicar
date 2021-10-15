//山东微缩车项目 底层程序
#include <Servo.h>
#include <stdlib.h>
Servo myservo;
int motor_pin1 = 11;
int motor_pin2 = 6;
int dir1 = 5;
int dir2 = 3;
int servo_pin = 9;
int motor = 0; //速度值
float angle = 90;  //角度值
float sup_angle = 180;//角度最大值
float inf_angle = 0;//角度最小值
int num = 0;//临时字符变量，又或者说是缓存用的吧
int sp1 = 0;
int sp2 = 0;
int lev;
int data;
String comdata;
char tmp;

int gear = 0;//默认小车静止
int direction = 16;//默认舵机转角处于中间

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(115200);
  myservo.attach(servo_pin); 
  myservo.write(90);
  pinMode(motor_pin1, OUTPUT);
  pinMode(motor_pin2, OUTPUT);
  pinMode(dir1, OUTPUT);
  pinMode(dir2, OUTPUT);  
}

void loop() {
  Serial.flush();
  while (Serial.available() > 0)  
{   
    comdata = int(Serial.read());

    //comdata为一个字节，高三位控制电机，低5位控制舵机
    gear = comdata / 32;//提取高三位的速度信息
    //000为静止，001为前进，010为后退
    direciton = comdata % 32

    //电机设置
    switch(gear)//静止？前进？后退？
    {
        //静止
        case'0':
            spd1 = 0;
            spd2 = 255;
            motor = 12;
            break;
        //前进
        case'1':
            spd1 = 0;
            spd2 = 255;
            motor = 12;
            break;
        //后退
        case'2':
            spd1 = 255;
            spd2 = 0;
            motor = 12;
            break;
        default:break;
    }
 
    //舵机设置  comdata-- 0到31 映射到 servo-- inf_angle到sup_angle(中心为90)
    //范围映射
    angle = 90 + (comdata - 31) * (sup_angle - 90)/ (31 - 16);
    //对angle限幅
    if(angle > sup_angle)
        angle = sup_angle;
    else if(angle < inf_angle)
        angle = inf_angle;

 
  //数据传输
  myservo.write(angle);  //控制舵机转动相应的角度。
  analogWrite(dir1, sp1);
  analogWrite(dir2, sp2);
  analogWrite(motor_pin1, motor);
  analogWrite(motor_pin2, motor);
  delay(1);
}
