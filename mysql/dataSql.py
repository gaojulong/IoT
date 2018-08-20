import mysql.connectSql as connsql
import Utils.mydate as mydate

conn = connsql.getConnect()
cur =  connsql.getCursor()

#插入数据
#根据传入设备ID进行数据保存
def add(device_id,content):
    cur.execute("INSERT INTO data(device_id,content,date)"
                "values('%s','%s','%s')"%(device_id,content,mydate.getdatetime()))
    conn.commit()

#查询数据device_id
#根据传入的id进行查询数据
###查询数据
def select(device_id):
    cur.execute("SELECT * FROM data WHERE device_id='%s'"%device_id)#返回受影响的行数
    results = cur.fetchall() #返回查询的数据
    for row in results:
        print(row[0],row[1],row[2],row[3])

if __name__ == '__main__':
    # add('12','12')
    # connsql.close()

    select('12')