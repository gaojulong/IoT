import pymysql
conn = pymysql.Connect(host='192.168.43.244',port=3306,user="root",passwd="root",db='IoT')

cur = conn.cursor()

###查询数据
def select():
    cur.execute("SELECT * FROM user")#返回受影响的行数
    results = cur.fetchall() #返回查询的数据
    for row in results:
        print(row[0],row[1],row[2],row[3],row[4],row[5])

###插入数据
def add(user_name,user_passwd):
    cur.execute("INSERT INTO user(user_name,user_passwd,) values('1,'1')")
    cur.commit()


# add('name001','ps001')
select()
cur.close()
