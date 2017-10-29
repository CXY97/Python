'''
selenium模拟登陆教务系统
'''

from selenium import webdriver
import time


def sel_login(url):

    driver = webdriver.Firefox()
    driver.get(url)

    # 填写信息
    driver.find_element_by_id('txtUserName').send_keys('账号')
    driver.find_element_by_id('TextBox2').send_keys('密码')
    time.sleep(0.5)

    # 找到验证码并输入
    certify_code = driver.find_element_by_id('txtSecretCode')
    time.sleep(0.5)
    code = input('自行输入验证码：')
    certify_code.send_keys(code)
    driver.find_element_by_id('Button1').click()
    time.sleep(0.5)

    # 不明觉厉的验证码第一次时常会爆出输入报错，但是若登进去会跳转网页链接(重定向), 检查一下
    if driver.current_url == url:
        driver.switch_to_alert().accept()
        driver.find_element_by_id('TextBox2').send_keys('cxy.971229')
        time.sleep(0.5)
        # 再次找到验证码并输入
        certify_code = driver.find_element_by_id('txtSecretCode')
        time.sleep(0.5)
        code = input('再次 自行输入验证码：')
        certify_code.send_keys(code)
        driver.find_element_by_id('Button1').click()

    print('标题: ', driver.title)  # 未登录进去显示为：欢迎使用正方教务管理系统！请登录


if __name__ == '__main__':

    login_url = 'http://jw.学校教务.edu.cn/'
    sel_login(login_url) # 至此会登录进去, 若需要做别的操作, 自行添加
    
