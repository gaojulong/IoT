# import mysql.connectSql as connsql
# import Utils.mydate as mydate
#
# conn = connsql.getConnect()
# cur = connsql.getCursor()
#
# ###创建设备
# def add(user_id,device_passwd,device_name):
#     cur.execute("INSERT INTO device(user_id,device_passwd,device_name,create_date)"
#                 "values('%s','%s','%s','%s')"%(user_id,device_passwd,device_name,mydate.getdate()))
#     conn.commit()
#
# ###用户设备验证信息，查询密码和设备id是否匹配
# ###返回布尔值
#
# def matching(device_id,device_passwd):
#     # 返回受影响的行数
#     row=cur.execute("SELECT * FROM device WHERE device_id='%s'AND device_passwd='%s'" %(device_id,device_passwd))
#     # print(row)
#
#     return row
#
# #根据传入用户id，返回该用户下的所有设备
# def getUserDevice(user_id):
#     # 返回受影响的行数
#     cur.execute("SELECT * FROM device WHERE user_id='%s'" % user_id)  # 返回受影响的行数
#     results = cur.fetchall()  # 返回查询的数据
#     # for row in results:
#     #     print(row[0], row[1], row[2], row[3])
#     print(results)
#
#
# if __name__ == '__main__':
#     #查询某一用户下的所有设备
#     getUserDevice('11')
#
#     # print()
#     #添加设备
#     # add('11','123123','001')
#
#     #验证设备信息
#     # if matching('11','123123'):
#     #     print("验证成功")
#     # else:
#     #     print('验证失败')