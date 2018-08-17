import mysql.connectSql as connsql
import Utils.mydate as mydate

conn = connsql.getConnect()
cur = connsql.getCursor()

###插入数据
def add(user_id,device_passwd,device_name,create_date):
    cur.execute("INSERT INTO device(user_id,device_passwd,device_name,create_date)"
                "values('%s','%s','%s','%s')"%(user_id,device_passwd,device_name,create_date))
    conn.commit()

if __name__ == '__main__':
    add('11','123123','001',mydate.getdate())