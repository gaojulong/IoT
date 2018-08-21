from flask import render_template, request
from flask import Flask

import datetime

import mysql.deviceSql as mydevicesql
import mysql.userSql as myusersql
import TCP.Server as tcpservice
import mysql.mysql as mysql
import json

app = Flask(__name__)


# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        userpassword = request.form.get('userpassword')
        print('输入的用户名为：', username, '密码：', userpassword)

        userID = myusersql.matching(username, userpassword)
        if userID is None:
            return '登录失败'

    return ('登录成功,用户ID%s' % userID)

# 插看所有的设备
@app.route('/getdevices/<userid>')
def getdevices(userid):
    print(userid)
    devices= mysql.MySQL().getUserDevice(userid)
    return render_template('devicelist.html',devices= devices)


# 创建设备
@app.route('/createdevice', methods=['GET', 'POST'])
def createdevice():
    if request.method == 'GET':
        return render_template('createdevice.html')
    else:
        user_id = request.form.get('user_id')
        device_passwd = request.form.get('device_passwd')
        device_name = request.form.get('device_name')

        #弃用
        # mydevicesql.add(user_id, device_passwd, device_name)

        flag = mysql.MySQL().insertDevice(user_id, device_passwd, device_name)
        print(flag)
        if flag :
            print('用户的ID', user_id, '设备密码：', device_passwd, '设别名称', device_name)
            return '添加成功'
        else:
            return '请查看设备名是否唯一'


# 给设备发送消息
@app.route('/sendMsgDevice', methods=['GET', 'POST'])
def sendMsgDevice():
    if request.method == 'GET':
        return render_template('sendMsgDevice.html')
    else:
        device_id = request.form.get('device_id')


        device_name = request.form.get('device_passwd')
        sedMsg = request.form.get('msg')

        str = tcpservice.send_msg(device_id, device_name, sedMsg)

        return ('返回结果:%s' % str)

        # 给设备发送消息

#查询设备的数据
@app.route('/api/devices/<flag>', methods=['GET'])
def selectData(flag):
    print(flag)
    dic= mysql.MySQL().selectLastData(flag)
    jsons = json.dumps(dic,cls=DateEncoder)
    return ('%s'%jsons)




# 主页
@app.route('/')
def index():
    return render_template('index.html')


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        # elif isinstance(obj, date):
        #     return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':
    tcpservice.starTCP()
    app.run(host='0.0.0.0')
