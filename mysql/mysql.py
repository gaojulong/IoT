import pymysql
import Utils.mydate as mydate

class MySQL:
    conn = None
    cur = None
    def __init__(self):

        print('新的数据库连接')

        self.conn = pymysql.Connect(host='127.0.0.1', port=3306, user="root", passwd="root", db='IoT')
        self.cur = self.conn.cursor()

    #插入新的数据
    def insertData(self,device_id, content):
        self.cur.execute("INSERT INTO data(device_id,content,date)"
                    "values('%s','%s','%s')" % (device_id, content, mydate.getdatetime()))
        self.conn.commit()

        self.cur.close()
        self.conn.close()

    #创建设备,必须知道是哪一个用户，参数二:设置设备密码 ，参数三：设备别名
    def insertDevice(self,user_id, device_passwd, device_name):

        row = MySQL().matching_Device_name(user_id,device_name)
        if  row== 0:
            self.cur.execute("INSERT INTO device(user_id,device_passwd,device_name,create_date)"
                        "values('%s','%s','%s','%s')" % (user_id, device_passwd, device_name, mydate.getdate()))
            self.conn.commit()

            return True
        else:
            return False

    #插入设备之前，先判断该用户下设备名是否已存在,返回查询到条数
    def matching_Device_name(self,user_id,device_name):
        #手影响的函数
        row = self.cur.execute("SELECT * FROM  device WHERE user_id='%s' AND device_name='%s'"%(user_id,device_name))
        return row

    '''
     用户登录
     '''

    def userlogin(self, user_name, duser_passwd):

        self.cur.execute("SELECT * FROM user WHERE user_name='%s'AND user_passwd='%s'" % (user_name, duser_passwd))

        results = self.cur.fetchall()  # 返回查询的数据二维数组
        if len(results) > 0:
            user_id = results[0][0]  # 返回用户的ID
            return user_id
        else:
            print('NO USER DATA')

        return None

    # 查询数据device_id
    # 根据传入的id进行查询数据
    #查询最新数据
    def selectLastData(self,device_id):
        #查询最新数据消息
        self.cur.execute("SELECT * FROM data WHERE device_id='%s' order by date desc  LIMIT 1" % device_id)
        results = self.cur.fetchall()  # 返回查询的数据
        if len(results) == 0:
            return None
        return results

    #查询所有数据
    def get_all_Data(self,device_id):
        #查询最新数据消息
        self.cur.execute("SELECT * FROM data WHERE device_id='%s'" % device_id)
        results = self.cur.fetchall()  # 返回查询的数据
        if len(results) == 0:
            return None
        return results

    # 根据传入用户id，返回该用户下的所有设备
    def getUserDevice(self, user_id):
        # 返回受影响的行数
        self.cur.execute("SELECT * FROM device WHERE user_id='%s'" % user_id)  # 返回受影响的行数
        devices = self.cur.fetchall()  # 返回查询的数据
        return  devices

    #根据传入的id删除设备,并自动删除该设备下的所有数据
    def delectDevice(self,user_id,device_id):
        row = self.cur.execute("DELETE FROM device WHERE user_id='%s' AND device_id='%s'" %(user_id,device_id))
        self.conn.commit()
        self.closesql()
        return row

    # ###用户设备验证信息，查询密码和设备id是否匹配
    # ###返回布尔值
    def matching(self, device_id,device_passwd):
        # 返回受影响的行数
        row=self.cur.execute("SELECT * FROM device WHERE device_id='%s'AND device_passwd='%s'" %(device_id,device_passwd))
        # print(row)
        return row

    def closesql(self):
        self.cur.close()
        self.conn.close()

if __name__ == '__main__':
#
    mysql=MySQL()
    # row = mysql.matching_Device_name(11,'小车')

    #测试删除设备
    mysql.delectDevice('12')

    #测试 查询某一用户下的所有设备
    # devices = mysql.getUserDevice(11)
    # print(devices)



#     #测试查询数据
#     mysql.selectLastData(12)

    # mysql.selectAllData(12)

    # mysql.insertData('13','13')


