import time

def getdate():
    #2018-08-17
    return time.strftime('%Y-%m-%d',time.localtime(time.time()))


def getdatetime():
    #2018-08-17 15:21:37
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))