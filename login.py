from flask import render_template,request
from flask import Flask
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
        return 'post request'

#创建设备

@app.route('/createDevice',methods = ['GET','POST'])
def createDevice():
    if request.method=='GET':
        return render_template('createdevice.html')
    else:
        user_id = request.form.get('user_id')
        device_passwd= request.form.get('device_passwd')
        device_name = request.form.get('device_name')

        print('设备ID', user_id, '设备密码：', device_passwd,'设别名称',device_name)
        return 'POST'

#主页
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)