#!/usr/bin/env python

# _*_ coding:utf-8 _*_


import socketserver
import threading
import Utils.strDispose as mystrUtil
import mysql.deviceSql as mydevicesql

conn_deviceID = []      #
conn_obj = {}               #存放连接对象

address = ''    #地址
port=10024      #端口号

class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        global conn
        conn = self.request

        # 返回连接对象的地址和线程
        address, pid = self.client_address
        print("got connection from", address, pid)

        conn.sendall(bytes("你好，请登陆！", encoding="utf-8"))

        # #验证用户设备
        print("正在等待注册......")

        try:
            # 接收客户端发送过来的内容
            ret_bytes = conn.recv(1024)
            ret_str = str(ret_bytes, encoding="utf-8")

            # 输出用户发送过来的注册信息
            print('注册信息为:', ret_str)
            #分割成ID和密码，返回字典【id,passwd】
            id_passwd= mystrUtil.get_Id_Passwd(ret_str)
            if not id_passwd is '':
                device_id=id_passwd[0]
                device_passwd=id_passwd[1]
                print('id',device_id,'密码',device_passwd)
            else:
                conn.sendall(bytes('类型错误', encoding="utf-8"))
                return
        except UnicodeDecodeError:
            print('字符转换错误：非法字符')


            #传入id和密码验证是否存在设备
        if mydevicesql.matching(device_id,device_passwd):
            print('验证成功')
            conn_deviceID.append(device_id)
            conn_obj[device_id]=conn
        else:
            print('设备验证失败')
            conn.sendall(bytes('设备验证失败', encoding="utf-8"))
            return



        print('等待节点上传数据')
        while True :
            try:
                # 接收客户端发送过来的内容

                ret_bytes = conn.recv(1024)
                #如果数据为空退出
                if not ret_bytes :
                    print('没有数据')
                    break
                ret_str = str(ret_bytes, encoding="utf-8")

                # 输出用户发送过来的内容
                print(ret_str)
            except UnicodeDecodeError:
                print('字符转换错误：非法字符')


        #     inp = input("Service请输入要发送的内容>>> ")
        #     conn.sendall(bytes(inp, encoding="utf-8"))


def sendMsg(conn, str):
    conn.sendall(bytes(str, encoding="utf-8"))


def serverStart():
    try:
        server = socketserver.ThreadingTCPServer((address, port), MyServer)
        print('Server is Running...')
        server.serve_forever()

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    t = threading.Thread(target=serverStart)
    # t.setDaemon(True)
    t.start()
    #
    # try:
    #     while t.isAlive():
    #         pass
    # except KeyboardInterrupt:
    #     print('服务线程结束')


