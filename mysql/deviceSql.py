import mysql.connectSql as connsql
import Utils.mydate as mydate

conn = connsql.getConnect()
cur = connsql.getCursor()

###插入数据
def add(user_id,device_passwd,device_name):
    cur.execute("INSERT INTO device(user_id,device_passwd,device_name,create_date)"
                "values('%s','%s','%s','%s')"%(user_id,device_passwd,device_name,mydate.getdate()))
    conn.commit()

###用户设备验证信息，查询密码和设备id是否匹配
###返回布尔值

def matching(device_id,device_passwd):
    # 返回受影响的行数
    row=cur.execute("SELECT * FROM device WHERE device_id='%s'AND device_passwd='%s'" %(device_id,device_passwd))
    # print(row)

    return row


# if __name__ == '__main__':

    # print()
    #添加设备
    # add('11','123123','001')

    #验证设备信息
    # if matching('11','123123'):
    #     print("验证成功")
    # else:
    #     print('验证失败')