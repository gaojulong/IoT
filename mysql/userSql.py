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

###根据传入

# if __name__ == '__main__':
#     # add('001' ,'123123')
#     select('user')
#
#     connsql.close()
