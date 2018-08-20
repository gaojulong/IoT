import sys
import socket
import threading, time
import TCP.Device as mydevice
import Utils.myStringUtil as mystrUtil
import mysql.deviceSql as mydevicesql
import mysql.dataSql as mydatasql

devicelist = []


def hand_user_con(device):
    device.skt.sendall(bytes("你好，请登陆！", encoding="utf-8"))
    # #验证用户设备
    print("正在等待注册......")

    try:
        # 接收客户端发送过来的内容
        ret_bytes = device.skt.recv(1024)
        ret_str = str(ret_bytes, encoding="utf-8")

        # 输出用户发送过来的注册信息
        print('注册信息为:', ret_str)
        # 分割成ID和密码，返回字典【id,passwd】
        id_passwd = mystrUtil.get_Id_Passwd(ret_str)
        if not id_passwd is '':
            device_id = id_passwd[0]
            device_passwd = id_passwd[1]
            print('id', device_id, '密码', device_passwd)
        else:
            device.skt.sendall(bytes('类型错误', encoding="utf-8"))
            return
    except UnicodeDecodeError:
        print('字符转换错误：非法字符')

    if mydevicesql.matching(device_id, device_passwd):
        print('验证成功')

        # 给设备绑定ID号
        device.deviceid = device_id
        device.skt.sendall(bytes('设备验证成功', encoding="utf-8"))
    else:
        print('设备验证失败')
        device.skt.sendall(bytes('设备验证失败', encoding="utf-8"))
        return

    print('等待节点上传数据')

    # 循环接收数据并处理保存到数据库
    receiveMsg(device)


    # -----------------验证设备成功后循环接收发送来的数据-----------------------#


def receiveMsg(device):
    try:

        isNormar = True
        while isNormar:
            data = device.skt.recv(1024)
            if not data:
                print('没有数据，从列表中移除对象')
                devicelist.remove(device)#在列表中移除这个对象
                break
            else:
                # 接收客户端发送过来的内容
                ret_str = str(data, encoding="utf-8")
                # 输出用户发送过来的注册信息
                print(device.deviceid, '号上传数据:', ret_str)

                #讲数据保存到数据库
                mydatasql.add(device.deviceid,ret_str)
                device.skt.send('OK'.encode())#接收数据后返回ok给客户端




    except:
        isNormar = False

#发送消息给设备
def send_msg(deviceid, devicepassed, msg):
    if mydevicesql.matching(deviceid, devicepassed):

        if (len(devicelist) >= 1):
            for device in devicelist:
                # if not device.deviceid is None
                if (device.deviceid == deviceid):
                    print('设备在线')

                    try:
                        device.skt.send(msg.encode())
                    except BrokenPipeError:
                        devicelist.remove(device)
                        print('发送异常，可能设备没有正常下线，设备列表中没有清除')
                        return '发送异常'
                    return '发送成功'
            print('目标设备不在线')
            return '目标设备不在线'
        else:
            print('目前没有一个连接')
            return '设备没有连接'

    else:
        print('目标设备密码错误')
        return '目标设备密码错误'


# 程序入口
def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', 10024))
        s.listen(5)
        print(u'waiting for connection...')

        while True:
            sock, addr = s.accept()  # 等待用户连接
            user = mydevice.Device(sock)
            devicelist.append(user)
            t = threading.Thread(target=hand_user_con, args=(user,));
            t.start()
        s.close()
    except OSError:
        print('TCP创建异常')


# # 因为main里为死循环，导致线程主线程卡主
def starTCP():
    try:
        print('TCP服务已启动')
        thr = threading.Thread(target=main)
        thr.start()
    except ( KeyboardInterrupt ):
        print('TCP服务启动失败')


# if (__name__ == "__main__"):
#     starTCP()
