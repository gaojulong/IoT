import mysql.connectSql as connsql

#获取数据库连接
conn = connsql.getConnect()
cur = connsql.getCursor()


###查询数据
def select(tables):
    cur.execute("SELECT * FROM %s"%tables)#返回受影响的行数
    results = cur.fetchall() #返回查询的数据
    for row in results:
        print(row[0],row[1],row[2],row[3],row[4],row[5])


###插入数据
def add(user_name,user_passwd):
    cur.execute("INSERT INTO user(user_name,user_passwd)values('%s','%s')"%(user_name,user_passwd))
    conn.commit()

###用户登录验证，查询数据库信息是否匹配
###返回查询到的用户id，否则返回None

def matching(user_name,duser_passwd):
    # 返回受影响的行数
    row=cur.execute("SELECT * FROM user WHERE user_name='%s'AND user_passwd='%s'" %(user_name,duser_passwd))

    results = cur.fetchall()  # 返回查询的数据二维数组
    if len(results) > 0:
        user_id = results[0][0] #返回用户的ID
        return user_id
    else:
        print('NO USER DATA')

    return None

###根据传入

if __name__ == '__main__':
    print(matching('001','123123'))
#     # add('001' ,'123123')
#     select('user')
#
#     connsql.close()
