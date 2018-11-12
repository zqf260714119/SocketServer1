from threading import *
from socket import *
import time
import re
import os
def pro1():
    # mutex.acquire()
    try:
        time.sleep(1)
        global inmsg,filename,Menu,filesaveaddr,LEN,msg1
        filesaveaddr = None
        while True:
            # print(LEN,Menu)
            time.sleep(1.5)
            # print(msg1)
            if msg1 == None:
                if inmsg == "Exit":
                    break
                if len(Menu) == LEN :
                    # print(Menu)
                    for i in Menu:
                        print(i)
                    time.sleep(0.5)
                    msg = input("输入")
                    socket1.send(msg.encode("UTF-8"))
                    os.system('cls')
                    time.sleep(0.5)
                    if "yes/no" in inmsg:
                    # inmsg =None
                        time.sleep(1)
                        msg = input("输入")
                        if msg == "yes":
                            filesaveaddr = input("输入文件保存路径(盘符+路径)：")
                            if filesaveaddr[-1] != "\\" or filesaveaddr[-1] != "/":
                                filesaveaddr = filesaveaddr + "\\"
                        else:
                            continue
                        socket1.send(msg.encode("UTF-8"))
                        time.sleep(1)
                        continue
                    else:
                        Menu = []
                        # LEN = None
        # mutex.release()
    except:
        print("与服务器链接已经断开")
def pro2():
    global inmsg,filename,Menu,LEN
    Menu = []
    LEN = None
    # mutex.acquire()
    try:
        while True:
            data = socket1.recv(1024)
            inmsg = data.decode("UTF-8")
            # print(inmsg)
            if inmsg.isdigit():
                # print("是")
                LEN = int(inmsg)
                # print(LEN)
                continue
            str = re.match(r"(\d+?.\w+?\.\w+)|(\d+?.\w+)|(\d+?.\.\w+)|(\d+?..\w+)",inmsg)
            if str!= None:
                Menu.append(str.group())
                # print(Menu)
                continue
            if "ok" in inmsg:
                filename = inmsg.split(" ")[1]
                # print(filename)
                filelen = inmsg.split(" ")[2]
                # print(filelen)
                savedata(filelen)
                continue
            if inmsg == "Exit":
                socket1.close()
                break
            print(inmsg)
            # inmsg = None

    except:
        pass
    # mutex.release()
    # print(inmsg)
def savedata(filelen):
    global filename,filesaveaddr,msg1
    print("开始下载")
    file = open(filesaveaddr + filename, "ab")
    while True:
        msg1 = socket1.recv(20480)
        filelen = int(filelen)-len(msg1)
        # print(msg1)
        # print(filelen,len(msg1))
        file.write(msg1)
        # time.sleep(1)
        if int(filelen)==len(msg1) or int(filelen)<500:
            print("%s下载完成" %filename)
            file.close()
            # mutex.release()
            msg1 = None
            break
msg1= None
filename = None
if __name__ == '__main__':
    IP = input("输入服务器IP:")
    # 下载文件保存的路径
    addr = (IP,8080)
    socket1 = socket(AF_INET,SOCK_STREAM)
    try:
        socket1.connect((addr))
        sendmsg = Thread(target=pro1)
        recvmsg = Thread(target=pro2)
        recvmsg.start()
        sendmsg.start()
    except:
        print("服务器未启动")

