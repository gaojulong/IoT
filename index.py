from flask import render_template,request
from flask import Flask

import mysql.deviceSql as mydevicesql
import mysql.userSql as myusersql
import TCP.Server as tcpservice

app = Flask(__name__)


#登录
@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        userpassword = request.form.get('userpassword')
        print('输入的用户名为：',username,'密码：',userpassword)

        userID=myusersql.matching(username, userpassword)
        if userID is None:
            return '登录失败'

    return ('登录成功,用户ID%s'%userID)



#创建设备
@app.route('/createDevice',methods = ['GET','POST'])
def createDevice():
    if request.method=='GET':
        return render_template('createdevice.html')
    else:
        user_id = request.form.get('user_id')
        device_passwd= request.form.get('device_passwd')
        device_name = request.form.get('device_name')

        mydevicesql.add(user_id,device_passwd,device_name)

        print('设备ID', user_id, '设备密码：', device_passwd,'设别名称',device_name)
        return '添加成功'


#给设备发送消息
@app.route('/sendMsgDevice',methods=['GET','POST'])
def sendMsgDevice():
    if request.method=='GET':
        return render_template('sendMsgDevice.html')
    else:
        device_id = request.form.get('device_id')
        device_name = request.form.get('device_passwd')
        sedMsg = request.form.get('msg')

        str = tcpservice.send_msg(device_id, device_name, sedMsg)

        return ('返回结果:%s'%str)


#主页
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    tcpservice.starTCP()
    app.run(host='0.0.0.0')
