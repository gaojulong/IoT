import pymysql
conn = pymysql.Connect(host='192.168.43.244',port=3306,user="root",passwd="root",db='IoT')

# 创建游标
cur = conn.cursor()
print('连接')
#返回游标
def getCursor():
    return cur
#返回连接
def getConnect():
    return conn

def close():
    cur.close()
    conn.close()

