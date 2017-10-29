'''
requests库模拟登录方正教务系统
'''

import requests
import os
from PIL import Image
from bs4 import BeautifulSoup


def get_post_data(headers, base_url, ver_code_url):
   
    # 保持会话，正方系统cookie退出就没了(浏览器中查看到寿命为None)
    s = requests.session() 
    
    # 先请求一下，得到未登录时候的cookie
    html = s.get(base_url)
    
    # 保留cookies, 待会儿请求时候带上~
    cookies = s.cookies         
    
    # 找到form的验证参数
    soup = BeautifulSoup(html.text, 'lxml')
    __VIEWSTATE = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']    
    # print(__VIEWSTATE)

    # 下载验证码图片
    pic = s.get(ver_code_url, headers=headers, cookies=cookies).content
    with open('ver_pic.png', 'wb') as f:
        f.write(pic)

    # 打开验证码图片(可省略, 在当前路径找到即可)
    image = Image.open('{}/ver_pic.png'.format(os.getcwd()))
    image.show()

    # 构造需要post的参数表
    data = {
        'txtUserName': '',
        'Textbox1': '',
        'TextBox2': '',
        'txtSecretCode': "",
        '__VIEWSTATE': '',
        
        # import urllib : 使用rullib.request.quote('某汉字')
        'RadioButtonList1': '学生', # %D1%A7%C9%FA;  或许库自动转换了编码,写成'学生'也可哦
        'Button1': '',
        'lbLanguage': '',
        'hidPdrs': '',
        'hidsc': '',
    }

    # 构造登录的post参数
    data['__VIEWSTATE'] = __VIEWSTATE
    data['txtUserName'] = input("请输入学号: ")
    data['TextBox2'] = input("请输入密码: ")
    data['txtSecretCode'] = input('请输入验证码: ')
    # print(data)
    return data, cookies


# 登录教务系统
def login(url, data, cookies, headers):
    # cookies很重要
    s = requests.session()
    s.post(url, data=data, cookies=cookies, headers=headers)
    return s


if __name__ == '__main__':

    # 基本信息
    headers = {
        "Referer":"http://jw.学校教务系统.edu.cn/default2.aspx",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
                     Chrome/49.0.2623.110 Safari/537.36",
    }

    # 原始url
    base_url = 'http://jw.学校教务系统.edu.cn/default2.aspx'
    # 验证码的获取url
    ver_code_url = 'http://jw.学校教务系统.edu.cn/CheckCode.aspx'

    # 返回需要的数据
    data, cookies = get_post_data(headers, base_url, ver_code_url)
    # print(data, cookies)
    
    # 传送数据
    s = login(base_url, data, cookies, headers)

    # 模拟登录教务系统, 给出后期url
    url = 'http://jw.学校教务系统.edu.cn/xs_main.aspx?xh=你的账号'
    # 带上登录网站后的cookies值
    test = s.get(url, headers=headers, cookies=cookies).text


    # 检查是否登陆进去
    soup = BeautifulSoup(test, 'lxml')
    print(soup.title.get_text())

    # 执行登录后的一些操作, 此处只是简单验证
    if soup.title.get_text() == '正方教务管理系统':
        name = soup.find(id='xhxm').get_text()
        print('欢迎你啊~ ', name)
        
