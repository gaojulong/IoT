from flask import render_template, request, redirect, url_for
from flask import Flask,session
import os
import datetime
import TCP.Server as tcpservice
import mysql.mysql as mysql
import json

app = Flask(__name__)

app.config ['SECRET_KEY'] = '#=ii\xba\x08|;LK\x01\xad-\xe6V\xfb\x7ft9\xbbAf\xb4s'
# print(os.urandom(24))


# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        userpassword = request.form.get('userpassword')
        print('输入的用户名为：', username, '密码：', userpassword)

        userid = mysql.MySQL().userlogin(username, userpassword)
        if userid is None:
            return '登录失败'
        else:
            session['user_id']= userid   #登录成功后返回用户id，保存到session中
            # session有效期31天
            #登录成功后跳转到设备列表界面
            return redirect(url_for('get_all_devices'))


# 插看所有的设备
@app.route('/getalldevices')
def get_all_devices():
    userid= session.get('user_id')
    print(userid)
    devices= mysql.MySQL().getUserDevice(userid)
    return render_template('devicelist.html',devices= devices)

#删除设备
'''
删除之前需要判断是否设备是改用户下的
'''
@app.route('/devices/<device_id>',methods=['GET','POST'])
def devices(device_id):

    #从session中获取id
    userid = session.get('user_id')

    if request.method == 'POST':
        row = mysql.MySQL().delectDevice(userid,device_id)
        print(row)
        if row==0:
            return '删除失败'
        else:
            return redirect(url_for('get_all_devices'))
            # return '删除成功'
    if request.method == 'GET':
        return '不支持GET请求'



# 创建设备
@app.route('/createdevice', methods=['GET', 'POST'])
@app.route('/createdevice/', methods=['GET', 'POST'])
def createdevice():
    if request.method == 'GET':
        return render_template('createdevice.html')
    else:
        user_id = session.get('user_id')
        device_passwd = request.form.get('device_passwd')
        device_name = request.form.get('device_name')


        flag = mysql.MySQL().insertDevice(user_id, device_passwd, device_name)
        print(flag)
        if flag :
            print('用户的ID', user_id, '设备密码：', device_passwd, '设别名称', device_name)
            return redirect(url_for('get_all_devices'))
        else:
            return '设备可能已存在'

#发送消息页面
@app.route('/sendpage/<device_id>',methods=['GET'])
def sendpage(device_id):

    #把设备id放到session中，在发送页面中从session获取到设备的id
    session['device_id'] = device_id
    return render_template('sendMsgDevice.html')



@app.route('/sendmsg', methods=['POST'])
def sendmsg():

    device_id = session.get('device_id')
    print(device_id)
    device_passwd = request.form.get('device_passwd')
    sedMsg = request.form.get('msg')

    str = tcpservice.send_msg(device_id, device_passwd, sedMsg)

    return ('返回结果:%s' % str)



#查询设备最后一条的数据
@app.route('/api/devices/<flag>', methods=['GET'])
def selectData(flag):
    print(flag)
    dic= mysql.MySQL().selectLastData(flag)
    jsons = json.dumps(dic,cls=DateEncoder)
    return ('%s'%jsons)

#查询设备的所有数据
@app.route('/device/<device_id>', methods=['GET'])
def getdata(device_id):
    print(device_id)
    dic= mysql.MySQL().get_all_Data(device_id)
    if dic is None:
        return '没有数据记录'
    return render_template('datelist.html',dates = dic)

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
