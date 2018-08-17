##字符串处理工具

# 返回登录信息处理，把传入的设备id和密码进行分割，字符格式要求是(id-passwd),如(123-passwd)
def get_Id_Passwd(loginMsg):
    result = loginMsg.split('-')[:]

    #拆分成两部分
    if len(result) == 2:
        if not result[0] is '' and not result[1] is '':
            return result
    else:
        print('格式错误')
    return ''


if __name__ == '__main__':
    str = get_Id_Passwd('134123')
    if str is '':
        print('返回空')
    else:
        print(str[0], str[1])
