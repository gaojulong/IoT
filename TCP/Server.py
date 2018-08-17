#!/usr/bin/env python

# _*_ coding:utf-8 _*_


import socketserver
import threading



conn_listpid = []
conn_listRegister = []
conn_obj = {}


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
            print('注册信息为:',ret_str)
        except UnicodeDecodeError:
            print('字符转换错误：非法字符')

        # 追加到list里
        if ret_str not in conn_listRegister:
            #保存设备序列号和对应的连接对象
            conn_listRegister.append(ret_str)
            conn_obj[ret_str] = conn
        else:
            print('信息已被注册')
            conn.sendall(bytes('信息已被注册', encoding="utf-8"))
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
        server = socketserver.ThreadingTCPServer(('127.0.0.1', 10024,), MyServer)
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


