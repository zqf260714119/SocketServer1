"""
tcp服务器流程如下：
1. socket创建⼀个套接字
2. bind绑定ip和port
3. listen设置最大连接数，收到连接请求后，这些请求需要排队，如果队列满，就拒绝请求
4. accept等待客户端的链接、接收连接请求
5. recv/send接收发送数据
"""
from threading import Thread
import time
from multiprocessing import *
from socket import *
import os
# 向客户端展示共享文件夹的顶级目录
def pro1(socket):
    global drive,drive2,WaitDown,Sharedic1,LEN
    print(1,drive)
    # try:
    WaitDown = None
    LEN = None
    # drive2 存放的是当前访问目录
    drive2 = drive
    print(2,drive2)
    hint = "已经连接到服务器\n共享文件夹内容：\n(输入编号操作)"
    socket.send(hint.encode("UTF-8"))
    # 当前访问目录列表
    Sharedic = os.listdir(drive)
    LEN = len(Sharedic)
    # 遍历发送根目录路径
    socket.send(str(LEN).encode("UTF-8"))
    time.sleep(1)
    for id,dic in enumerate(Sharedic,1):
        share = str(id) +"\t"+dic
        socket.send(share.encode("UTF-8"))
        time.sleep(0.01)
    # print("共享根目录："+drive2)
    while True:
        msg = socket.recv(1024)
        inmsg = msg.decode("UTF-8")
        Sharedic1 = os.listdir(drive2)
        print(drive2)
        LEN = len(Sharedic1)
        # print("客户端请求:"+inmsg)
        # 如果发送的是exit 退出循环
        if inmsg.upper()== "EXIT":
            hint1 = ("与服务器断开连接", "Exit")
            socket.send(hint1[0].encode("UTF-8"))
            socket.send(hint1[1].encode("UTF-8"))
            socket.close()
            break
        # 如果发送的是yes发送WaitDown文件数据给客户端
        elif inmsg == "yes":
            # 发送要下载的文件数据
            SendData(drive2,WaitDown,socket)
            continue
        # 如果发送的是No重置WaitDown内容
        elif inmsg.upper()=="NO":
            WaitDown = None
        if (int(inmsg)-len(Sharedic1)) == 1 and drive2 != drive:
            Backdir(socket)
        # 通过发送的数字编号来访问文件
        else:
            # socket.send(str(LEN).encode("UTF-8"))
            # time.sleep(1)
            for id,filename in enumerate(Sharedic1,1):
                # 如果发送的编号和目录下的相同
                if int(inmsg) == id:
                    print(inmsg,id)
    # 判断是否是文件还是文件夹，是文件夹则显示文件夹下文件并设置当前drive2为当前目录路径,文件则发送下载文件提示发送数据
                    ShowMenu(drive2+"/"+filename,filename,socket)
                    break
            else:
                hint2 = "输入有误，重新输入"
                socket.send(hint2.encode("UTF-8"))
    # except:
    #     pass
    # finally:
        # print("当前预下载文件："+ str(WaitDown))
        print("当前目录："+drive2)
        # print("当前目录下文件：",Sharedic1)
# 展示a路径下的文件
def ShowMenu(a,name,socket):
    # print(name)
    global Sharedic1,drive2,WaitDown,drive,LEN
    if os.path.isdir(a):
        Sharedic1 = os.listdir(a)
        hint = str(len(Sharedic1)+1)+"\t" + "返回上级文件夹"
        if a != drive:
            LEN = len(Sharedic1)
            print(LEN)
            socket.send(str(LEN+1).encode("UTF-8"))
            time.sleep(1)
            for id, dic in enumerate(Sharedic1, 1):
                share = str(id) + "\t" + dic
                socket.send(share.encode("UTF-8"))
                time.sleep(0.01)
            else:
                socket.send(hint.encode("UTF-8"))
        else:
            socket.send(str(LEN).encode("UTF-8"))
            time.sleep(1)
            for id, dic in enumerate(Sharedic1, 1):
                share = str(id) + "\t" + dic
                socket.send(share.encode("UTF-8"))
                time.sleep(0.01)
        drive2 = drive2 + "/" + name
        return True
    elif os.path.isfile(a):
        hint = "确定要下载文件？yes/no"
        socket.send(hint.encode("UTF-8"))
        WaitDown = name
        return False
# 返回上级文件夹
def Backdir(socket):
    global drive2,Sharedic1,drive,LEN
    if drive2 == drive:
        drive2 = drive
    else:
        index = drive2.rindex("/")
        # 返回上级文件夹
        drive2 = drive2[:index]
        # print("返回后的文件夹：",drive2)
        Sharedic1 = os.listdir(drive2)
    #     展示给客户端
        time.sleep(1)
    LEN = len(Sharedic1)
    hint = str(len(Sharedic1) + 1) + "\t" + "返回上级文件夹"
    if drive2 != drive:
        socket.send(str(LEN+1).encode("UTF-8"))
        for id, dic in enumerate(Sharedic1, 1):
            share = str(id) + "\t" + dic
            socket.send(share.encode("UTF-8"))
            time.sleep(0.01)
        socket.send(hint.encode("UTF-8"))
    else:
        socket.send(str(LEN).encode("UTF-8"))
        for id, dic in enumerate(Sharedic1, 1):
            share = str(id) + "\t" + dic
            socket.send(share.encode("UTF-8"))
            time.sleep(0.01)
# 发送客户端要下载的文件数据
def SendData(drive,name,socket):
    filename = drive+"/"+name
    f = open(filename,"rb")
    data = f.read()
    LEN1 = len(data)
    hint1 = "ok "+name+" "+str(LEN1)
    socket.send(hint1.encode("UTF-8"))
    # print(filename)
    socket.send(data)
    f.close()
# drive 存放共享文件夹的根目录

global drive
drive = "E:\work"
if __name__ == '__main__':
    socket1 = socket(AF_INET, SOCK_STREAM)
    socket1.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    socket1.bind(("", 8080))
    socket1.listen(5)
    while True:
        socket2,addr = socket1.accept()
        sendmsg = Process(target=pro1,args=(socket2,))
        sendmsg.start()
        socket2.close()


