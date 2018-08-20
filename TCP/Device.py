import socket

class Device:
    def __init__(self, skt, deviceid='none'):
        self.skt=skt
        self.deviceid=deviceid
    def send_msg(self,msg):
        self.skt.send(msg)
    def logout(self):
        self.skt.close()