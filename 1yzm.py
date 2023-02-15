"""@author RobustBody
设备巡检，自动登录 beta1.0.3
 版本更新：
    提前把输入法切换为en，避免中文输入法下输出的为中文
    添加重新输入密码功能

beta1.0.2 版本更新：
    新增隐私错误自动点击功能

beta1.0.1 版本更新：
    修复了部分bug,账号密码改为了手动输入

 识别验证码步骤：
1.打开浏览器，打开所有安全设备登录页面
2.根据每个页面的title不同，设备设备类型
3.根据设备类型分别调用不同的验证码识别方法，识别输入验证码
4.实现tab页面循环
5.无验证码的根据title，选择不同的登录点击方式
使用方式：
双击py,浏览器启动后，打开巡检的设备，到命令行窗口，输入任意键；
回到浏览器，开始自动登录。
"""



# 导入相关库
import os
import time
import getpass

from ast import Num, Try
from cmath import e
from tkinter import EXCEPTION

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions

import ddddocr
from pymouse import PyMouse
from pykeyboard import PyKeyboard

import win32api
import win32gui
from win32con import WM_INPUTLANGCHANGEREQUEST


#切换输入法为en
hwnd = win32gui.GetForegroundWindow()
win32api.SendMessage(hwnd,WM_INPUTLANGCHANGEREQUEST,0,0x409)


# 启动浏览器
options = EdgeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-headless')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#options.add_argument('user-data-dir=C:\\Users\\lutw\\AppData\\Local\\Microsoft\\Edge\\User Data')
options.add_argument('--user-data-dir=C:\\Users\\lutw\\AppData\\Local\\Microsoft\\Edge\\User Data')  #这行如果导致报错，显示"unknown error: DevToolsActivePort file doesn't exist"  说明edge还有进程在后台运行
driver = webdriver.Edge(options=options)



# 全局实例化对象
m=PyMouse()
k=PyKeyboard()

#脚本测试
#userName="admin"
#passWord="pass"

userName=input("请输入要登录的用户名：")
#passWord=input("请输入用户密码：")
passWord=getpass.getpass("请输入用户密码：")

ifc=0

#天清入侵防御系统
def qm_ips():
    global ifc
    # 获取验证码图片
    yzmimg = driver.find_element(By.ID,"pic")
    # 验证码图片转换为base64
    data = yzmimg.screenshot_as_base64
    ocr = ddddocr.DdddOcr()
    # 进行验证码识别
    yzmtext = ocr.classification(data)
    # 判断识别的验证码是否为4位，通过isdigit()函数，可以判断字符串是否为数字{if yzmtext.isdigit():}
    if len(yzmtext)==4:
        # 定位验证码输入框
        yzminput=driver.find_element(By.ID,"validate")
        yzminput.clear()
        # 输入验证码
        yzminput.send_keys(yzmtext)
        # 输入账号密码
        driver.find_element(By.ID,"userName").clear()
        driver.find_element(By.ID,"password").clear()
        driver.find_element(By.ID,"userName").send_keys(userName)
        driver.find_element(By.ID,"password").send_keys(passWord)
        k.tap_key(k.tab_key)
        driver.find_element(By.ID,"submit").click()
    elif ifc < 10:# 非4位的验证码，需要通过点击刷新重新获取验证码
        driver.find_element(By.ID,"res4").click() # ips
        ifc=ifc+1
        qm_ips() #递归，循环获取验证码，直到识别为4位验证码
    return 0

#天清Web应用安全网关
def qm_waf():
    global ifc
    # 输入账号密码
    driver.find_element(By.NAME,"userName").clear()
    driver.find_element(By.NAME,"passWord").clear()
    driver.find_element(By.NAME,"userName").send_keys(userName)
    driver.find_element(By.NAME,"passWord").send_keys(passWord)
    print('ok')
    # 获取验证码图片
    yzmimg = driver.find_element(By.ID,"imgCheckCode")
    # 验证码图片转换为base64
    data = yzmimg.screenshot_as_base64
    ocr = ddddocr.DdddOcr()
    # 进行验证码识别
    yzmtext = ocr.classification(data)
    # 判断识别的验证码是否为4位，通过isdigit()函数，可以判断字符串是否为数字{if yzmtext.isdigit():}
    if len(yzmtext)==4:
        # 定位验证码输入框
        yzminput=driver.find_element(By.ID,"checkCode")
        yzminput.clear()
        # 输入验证码
        yzminput.send_keys(yzmtext)
        print(yzmtext)
        print("data:image/jpeg;base64,"+data)
        driver.find_element(By.ID,"login_btn").click()
    elif ifc < 20:# 非4位的验证码，需要通过点击刷新重新获取验证码
        yzmimg.click() # waf
        ifc=ifc+1
        qm_waf() #递归，循环获取验证码，直到识别为4位验证码
    return 0

#奇安信网神分析平台
def qax_ty():
    global ifc
    # 获取验证码div
    tyYzmDiv=driver.find_element(By.CSS_SELECTOR,".authority-code.clearfix")
    # 获取验证码图片
    yzm=tyYzmDiv.find_element(By.TAG_NAME,"img")
    # 获取验证码输入框
    yzminput=tyYzmDiv.find_element(By.CLASS_NAME,"pull-left")
    # 验证码图片转换为base64
    data = yzm.screenshot_as_base64
    ocr = ddddocr.DdddOcr()
    # 进行验证码识别
    yzmtext = ocr.classification(data)
    # 判断识别的验证码是否为4位，通过isdigit()函数，可以判断字符串是否为数字{if yzmtext.isdigit():}
    if len(yzmtext)==4:
        yzminput.clear()
        # 输入验证码
        yzminput.send_keys(yzmtext)
        print(yzmtext)
        print("data:image/jpeg;base64,"+data)
        # 输入账号密码
        allInput=driver.find_elements(By.TAG_NAME,"input")
        allInput[0].clear()
        allInput[1].clear()
        allInput[0].send_keys(userName)
        allInput[1].send_keys(passWord)
        driver.find_element(By.CSS_SELECTOR,".el-button.login-button.el-button--primary").click()
    elif ifc < 10:# 非4位的验证码，需要通过点击刷新重新获取验证码
        yzm.click()#点击验证码
        ifc=ifc+1
        qax_ty() #递归，循环获取验证码，直到识别为4位验证码
    return 0

#奇安信网神流量传感器
def qax_tyCgq():
    global ifc
    # 获取验证码div
    tyYzmDiv=driver.find_element(By.CSS_SELECTOR,".form-item.form-item-code")
    # 获取验证码图片
    yzm=tyYzmDiv.find_element(By.TAG_NAME,"img")
    # 获取验证码输入框
    yzminput=tyYzmDiv.find_element(By.CLASS_NAME,"q-input__inner")
    # 验证码图片转换为base64
    data = yzm.screenshot_as_base64
    ocr = ddddocr.DdddOcr()
    # 进行验证码识别
    yzmtext = ocr.classification(data)
    # 判断识别的验证码是否为4位，通过isdigit()函数，可以判断字符串是否为数字{if yzmtext.isdigit():}
    if len(yzmtext)==4:
        yzminput.clear()
        # 输入验证码
        yzminput.send_keys(yzmtext)
        # 输入账号密码
        allInput=driver.find_elements(By.TAG_NAME,"input")
        allInput[0].clear()
        allInput[1].clear()
        allInput[0].send_keys(userName)
        allInput[1].send_keys(passWord)
        driver.find_element(By.CSS_SELECTOR,".q-button.q-button--primary.q-button--small").click()
    elif ifc < 10:# 非4位的验证码，需要通过点击刷新重新获取验证码
        yzm.click()#点击验证码
        ifc=ifc+1
        qax_tyCgq() #递归，循环获取验证码，直到识别为4位验证码
    return 0

#奇安信网神文件威胁鉴定器
def qax_tySx():
    global ifc
    # 获取验证码div
    tyYzmDiv=driver.find_element(By.CSS_SELECTOR,".authority-code")
    # 获取验证码图片
    yzm=tyYzmDiv.find_element(By.TAG_NAME,"img")
    # 获取验证码输入框
    yzminput=tyYzmDiv.find_element(By.CLASS_NAME,"q-input__inner")
    # 验证码图片转换为base64
    data = yzm.screenshot_as_base64
    ocr = ddddocr.DdddOcr(beta=True)
    # 进行验证码识别
    yzmtext = ocr.classification(data)
    # 判断识别的验证码是否为4位，通过isdigit()函数，可以判断字符串是否为数字{if yzmtext.isdigit():}
    if len(yzmtext)==4:
        yzminput.clear()
        # 输入验证码
        yzminput.send_keys(yzmtext)
        # 输入账号密码
        allInput=driver.find_elements(By.TAG_NAME,"input")
        allInput[0].clear()
        allInput[1].clear()
        allInput[0].send_keys(userName)
        allInput[1].send_keys(passWord)
        driver.find_element(By.CSS_SELECTOR,".q-button.login-button.q-button--primary").click()
    elif ifc < 10:# 非4位的验证码，需要通过点击刷新重新获取验证码
        yzm.click()#点击验证码
        ifc=ifc+1
        qax_tySx() #递归，循环获取验证码，直到识别为4位验证码
    return 0

#D01网络资产测绘分析系统
def ga_D01():
    #先输入密码，再输入账号，在识别验证码
    global ifc
    allInput=driver.find_elements(By.TAG_NAME,"input")
    allInput[1].clear()
    allInput[2].clear()
    allInput[1].send_keys(userName)
    allInput[2].send_keys(passWord)
    # 获取验证码div
    YzmDiv=driver.find_element(By.CSS_SELECTOR,".input-main.yzm")
    # 获取验证码图片
    yzm=YzmDiv.find_element(By.TAG_NAME,"img")
    # 获取验证码输入框
    yzminput=YzmDiv.find_element(By.TAG_NAME,"input")
    # 验证码图片转换为base64
    data = yzm.screenshot_as_base64
    ocr = ddddocr.DdddOcr()
    # 进行验证码识别
    yzmtext = ocr.classification(data)
    # 判断识别的验证码是否为4位，通过isdigit()函数，可以判断字符串是否为数字{if yzmtext.isdigit():}
    if len(yzmtext)==4:
        yzminput.clear()
        # 输入验证码
        yzminput.send_keys(yzmtext)
        print(yzmtext)
        # 输入账号密码
        #allInput=driver.find_elements(By.TAG_NAME,"input")
        #allInput[1].clear()
        #allInput[2].clear()
        #allInput[1].send_keys(userName)
        #allInput[2].send_keys(passWord)
        driver.find_element(By.CSS_SELECTOR,".submit.lg-container-footer").click()
    elif ifc < 10:# 非4位的验证码，需要通过点击刷新重新获取验证码
        yzm.click()#点击验证码
        ifc=ifc+1
        ga_D01() #递归，循环获取验证码，直到识别为4位验证码
    return 0

#专网非法外联监测系统 网联E01
def ga_E01():
    global ifc
    # 获取验证码div
    #YzmDiv=driver.find_element(By.CSS_SELECTOR,".ant-col.ant-form-item-control-wrapper")
    # 获取验证码图片
    #yzm=YzmDiv.find_element(By.TAG_NAME,"img")
    yzm=driver.find_element(By.CLASS_NAME,"verificationCodeImg___3hf-y")
    # 获取验证码输入框
    #yzminput=YzmDiv.find_element(By.TAG_NAME,"input")
    yzminput=driver.find_element(By.CSS_SELECTOR,".ant-input.ant-input-lg.verificationCodeInputStyle___1glDS")
    # 验证码图片转换为base64
    data = yzm.screenshot_as_base64
    ocr = ddddocr.DdddOcr(beta=True)
    # 进行验证码识别
    yzmtext = ocr.classification(data)
    # 判断识别的验证码是否为4位，通过isdigit()函数，可以判断字符串是否为数字{if yzmtext.isdigit():}
    if len(yzmtext)==4:
        yzminput.clear()
        # 输入验证码
        yzminput.send_keys(yzmtext)
        # 输入账号密码
        allInput=driver.find_elements(By.TAG_NAME,"input")
        allInput[0].clear()
        allInput[1].clear()
        allInput[0].send_keys(userName)
        allInput[1].send_keys(passWord)
        driver.find_element(By.CSS_SELECTOR,".ant-btn.submitBtn___1dntF.ant-btn-primary.ant-btn-lg").click()
    elif ifc < 10:# 非4位的验证码，需要通过点击刷新重新获取验证码
        yzm.click()#点击验证码
        ifc=ifc+1
        ga_E01() #递归，循环获取验证码，直到识别为4位验证码
    return 0

#微步在线 TDP 威胁感知平台
def wb_TDP():
    global ifc
    # 获取验证码div
    #YzmDiv=driver.find_element(By.CSS_SELECTOR,".index-cssmodule__auth-code-2dCrH")
    # 获取验证码图片
    #yzm=YzmDiv.find_element(By.TAG_NAME,"img")
    yzm=driver.find_elements(By.TAG_NAME,"img")[1]
    # 获取验证码输入框
    #yzminput=YzmDiv.find_element(By.TAG_NAME,"input")
    yzminput=driver.find_elements(By.TAG_NAME,"input")[2]
    # 验证码图片转换为base64
    #data1 = yzm.screenshot_as_base64
    data = yzm.get_attribute("src").split('base64,')[1].replace('%0A','')
    ocr = ddddocr.DdddOcr()
    # 进行验证码识别
    yzmtext = ocr.classification(data)
    print(yzmtext)
    # 判断识别的验证码是否为4位，通过isdigit()函数，可以判断字符串是否为数字{if yzmtext.isdigit():};isalpha()判断字符串是否为字母
    if len(yzmtext)==4 and yzmtext.isalpha():
        yzminput.clear()
        # 输入验证码
        yzminput.send_keys(yzmtext)
        print(yzmtext)
        print("data:image/jpeg;base64,"+data)
        # 输入账号密码
        allInput=driver.find_elements(By.TAG_NAME,"input")
        allInput[0].clear()
        allInput[1].clear()
        allInput[0].send_keys(userName)
        allInput[1].send_keys(passWord)
        driver.find_element(By.CSS_SELECTOR,".btn.btn-primary.mini.radius").click()
    elif ifc < 20:# 非4位的验证码，需要通过点击刷新重新获取验证码
        yzm.click()#点击验证码
        ifc=ifc+1
        wb_TDP() #递归，循环获取验证码，直到识别为4位验证码
    return 0


#微步在线 TIP 本地威胁情报管理平台
def wb_TIP():
    global ifc
    # 获取验证码div
    YzmDiv=driver.find_element(By.CSS_SELECTOR,"._3wo1js4jQLoOnM1gX58JqU")
    # 获取验证码图片
    yzm=YzmDiv.find_element(By.TAG_NAME,"img")
    # 获取验证码输入框
    yzminput=YzmDiv.find_element(By.TAG_NAME,"input")
    # 验证码图片转换为base64
    data = yzm.screenshot_as_base64
    ocr = ddddocr.DdddOcr()
    # 进行验证码识别
    yzmtext = ocr.classification(data)
    # 判断识别的验证码是否为4位，通过isdigit()函数，可以判断字符串是否为数字{if yzmtext.isdigit():}
    if len(yzmtext)==4:
        yzminput.clear()
        # 输入验证码
        yzminput.send_keys(yzmtext)
        # 输入账号密码
        allInput=driver.find_elements(By.TAG_NAME,"input")
        allInput[0].clear()
        allInput[1].clear()
        allInput[0].send_keys(userName)
        allInput[1].send_keys(passWord)
        driver.find_element(By.CSS_SELECTOR,"._2_6ftFZWAQy6yNxjlzlyT8._1UPXyXMlD_ARtFoyw5l7cM._1MOc1Ri8kL8jdFa0tC38qa").click()
    elif ifc < 10:# 非4位的验证码，需要通过点击刷新重新获取验证码
        yzm.click()#点击验证码
        ifc=ifc+1
        wb_TIP() #递归，循环获取验证码，直到识别为4位验证码
    return 0

#明御APT攻击预警平台
def ah_myAPT():
    global ifc
    # 获取验证码div
    YzmDiv=driver.find_element(By.CSS_SELECTOR,".cut-form-item.login-form-captcha.is-required.cut-form-item--medium")
    # 获取验证码图片
    yzm=YzmDiv.find_element(By.TAG_NAME,"img")
    # 获取验证码输入框
    #yzminput=YzmDiv.find_element(By.NAME,"captcha")
    yzminput=YzmDiv.find_element(By.TAG_NAME,"input")
    # 验证码图片转换为base64
    data = yzm.screenshot_as_base64
    ocr = ddddocr.DdddOcr()
    # 进行验证码识别
    yzmtext = ocr.classification(data)
    # 判断识别的验证码是否为4位，通过isdigit()函数，可以判断字符串是否为数字{if yzmtext.isdigit():}
    if len(yzmtext)==4:
        #yzminput.clear()
        driver.execute_script("arguments[0].value='';",yzminput)
        # 输入验证码
        yzminput.send_keys(yzmtext)
        # 输入账号密码
        #allInput=driver.find_elements(By.TAG_NAME,"input")
        #allInput[0].clear()
        #allInput[1].clear()
        #allInput[0].send_keys(userName)
        #allInput[1].send_keys(passWord)
        #driver.find_element(By.ID,"login-user-input").clear()
        #driver.find_element(By.ID,"password").clear()
        driver.execute_script("document.getElementById('login-user-input').value='';")
        driver.execute_script("document.getElementById('password').value='';")
        driver.find_element(By.ID,"login-user-input").send_keys(userName)
        driver.find_element(By.ID,"password").send_keys(passWord)
        driver.find_element(By.CSS_SELECTOR,".cut-button.login-submit.cut-button--primary.cut-button--medium").click()
    elif ifc < 10:# 非4位的验证码，需要通过点击刷新重新获取验证码
        yzm.click()#点击验证码
        ifc=ifc+1
        ah_myAPT() #递归，循环获取验证码，直到识别为4位验证码
    return 0

#科来网络回溯分析系统
def kl_wlhs():
    global ifc
    # 获取验证码图片
    yzmimg = driver.find_element(By.ID,"captcha-img")
    # 验证码图片转换为base64
    data = yzmimg.screenshot_as_base64
    ocr = ddddocr.DdddOcr(beta=True)
    # 进行验证码识别
    yzmtext = ocr.classification(data)
    # 判断识别的验证码是否为4位，通过isdigit()函数，可以判断字符串是否为数字{if yzmtext.isdigit():}
    if len(yzmtext)==4 and yzmtext.isdigit():
        # 定位验证码输入框
        yzminput=driver.find_element(By.ID,"captcha")
        yzminput.clear()
        # 输入验证码
        yzminput.send_keys(yzmtext)
        print(yzmtext)
        print("data:image/jpeg;base64,"+data)
        # 输入账号密码
        driver.find_element(By.ID,"username").clear()
        driver.find_element(By.ID,"password").clear()
        driver.find_element(By.ID,"username").send_keys(userName)
        driver.find_element(By.ID,"password").send_keys(passWord)
        driver.find_element(By.NAME,"do-login").click()
    elif ifc < 20:# 非4位的验证码，非数字，需要通过点击刷新重新获取验证码
        yzmimg.click()#点击验证码
        ifc=ifc+1
        kl_wlhs() #递归，循环获取验证码，直到识别为4位验证码
    return 0
def my_dbSjFk():
    # 输入账号密码
    driver.find_element(By.ID,"username").clear()
    driver.find_element(By.ID,"password").clear()
    driver.find_element(By.ID,"username").send_keys(userName)
    driver.find_element(By.ID,"password").send_keys(passWord)
    #点击登录
    driver.find_element(By.CSS_SELECTOR,".ant-btn.ant-btn-primary.ant-btn-lg.ant-btn-block").click()
def my_AiLPHA():
    global ifc
    # 获取验证码图片
    try:
        yzmimg = driver.find_element(By.CLASS_NAME,"codeImg")
    except:
        null_yzm()
        return 0
    # 验证码图片转换为base64
    data = yzmimg.screenshot_as_base64
    ocr = ddddocr.DdddOcr()
    # 进行验证码识别
    yzmtext = ocr.classification(data)
    # 判断识别的验证码是否为4位，通过isdigit()函数，可以判断字符串是否为数字{if yzmtext.isdigit():}
    if len(yzmtext)==4:
        # 定位验证码输入框
        inputs=driver.find_elements(By.TAG_NAME,"input")
        inputs[2].clear()
        # 输入验证码
        inputs[2].send_keys(yzmtext)
        # 输入账号密码
        inputs[0].clear()
        inputs[1].clear()
        inputs[0].send_keys(userName)
        inputs[1].send_keys(passWord)
        k.tap_key(k.tab_key)
        driver.find_element(By.CSS_SELECTOR,".ivu-btn.ivu-btn-primary").click()
    elif ifc < 10:# 非4位的验证码，需要通过点击刷新重新获取验证码
        yzmimg.click()
        ifc=ifc+1
        my_AiLPHA() #递归，循环获取验证码，直到识别为4位验证码
    return 0

def ahjh_DBSec():
    # 输入账号密码
    m.move(1710,255)
    m.click(1710,255)
    k.tap_key(k.tab_key)
    k.tap_key(k.tab_key)
    k.tap_key(k.tab_key)
    k.type_string(userName)
    time.sleep(0.1) #间隔100ms
    k.tap_key(k.tab_key)
    k.type_string(passWord)
    time.sleep(0.1) #间隔100ms
    k.press_key(k.enter_key)

def null_yzm():
    #ActionChains(driver).move_by_offset(200,200).click().perform()
    #a=m.position()
    #print(a)
    #time.sleep(0.5)
    m.move(1710,255)
    m.click(1710,255)
    k.tap_key(k.tab_key)
    k.type_string(userName)
    time.sleep(0.1) #间隔100ms
    k.tap_key(k.tab_key)
    k.type_string(passWord)
    time.sleep(0.1) #间隔100ms
    #k.tap_key(k.tab_key)
    if "NSFOCUS NIPS" in driver.title:
        driver.find_element(By.ID,"login_btn").click() #点击登录
    elif "AiNTA" in driver.title:
        driver.find_element(By.CSS_SELECTOR,".ivu-btn.ivu-btn-primary.ivu-btn-long").click()
    elif "欢迎登录" in driver.title: #深信服
        driver.find_element(By.CSS_SELECTOR,".uedc-ppkg-login_product-submit").click()
    elif "明御WEB应用防火墙" in driver.title:
        driver.find_element(By.ID,"user_login").click()
    #elif "系统登录" in driver.title: #安和金华
        #driver.find_element(By.ID,"btnLogin").click()
        #driver.find_element(By.CLASS_NAME,"loginBtn").click()
    else:
        k.tap_key(k.enter_key)

# 通过网页title，判断设备类型，调用设备对应的类方法;或通过Copyright的内容判断设备厂商，辅助判断设备类型
def ifTitle():
    if "新建标签页" in driver.title:
        print("跳过")
    elif "天清入侵防御系统" in driver.title or driver.title == "":
        qm_ips()
    elif "天清Web应用安全网关" in driver.title:
        qm_waf()
    elif "网神分析平台" in driver.title or "天眼分析平台" in driver.title:
        qax_ty()
    elif "网神流量传感器" in driver.title or "天眼流量传感器" in driver.title:
        qax_tyCgq()
    elif "网神文件威胁鉴定器" in driver.title or "天眼文件威胁鉴定器" in driver.title:
        qax_tySx()
    elif "D01" in driver.title:
        ga_D01()
    elif "E01" in driver.title:
        ga_E01()
    elif "威胁感知平台" in driver.title:
        wb_TDP()
    elif "TIP" in driver.title:
        wb_TIP()
    elif "明御APT攻击预警平台" in driver.title:
        ah_myAPT()
    elif "科来网络回溯分析系统" in driver.title:
        kl_wlhs()
    elif "明御数据库审计与风险控制系统" in driver.title:
        my_dbSjFk()
    elif "AiLPHA安全分析与管理平台" in driver.title:
        my_AiLPHA()
    elif "系统登录" in driver.title: #安和金华
        ahjh_DBSec()
    else:
        print("无当前设备类型")
        null_yzm()

def err_Cert():
    driver.find_element(By.ID,"details-button").click()
    driver.find_element(By.ID,"proceed-link").click()

def ifTitle2():
    if "隐私错误" in driver.title:
        err_Cert()

#循环标签页识别验证码
def bianLiTab(key_123):
    all_handles = driver.window_handles #获取到当前所有的句柄,所有的句柄存放在列表当中
    print(all_handles) #打印句柄
    #num=len(driver.window_handles)
    for handles in all_handles:
    #for i in range(1,num):
        #print(i)
        # 切换到对应下标的tab页面
        #driver.switch_to.window(driver.window_handles[i])
        driver.switch_to.window(handles)
        print(driver.current_window_handle) #获取当前窗口的句柄 
        print(driver.title)
        try:
            # 循环判断每个标签页，通过页面title区分设备类型，执行不同设备的验证码识别方法
            #time.sleep(1)
            global ifc
            ifc=0
            if key_123==1:
                ifTitle()
            elif key_123==2:
                ifTitle2()
        except Exception as e:
            print(e)
        #time.sleep(2)

def main():
    #打开浏览器后，等待下一步操作
    #测试站点
    #driver.get('https:// /sensor/login')
    #driver.switch_to.window(driver.window_handles[1]) #切换到第二个标签页，跳过第一个空白tab
    #循环tab，识别验证码
    while True:#循环执行识别，任意键后等待2s
        #os.system("pause")
        key_123=input("请输入序号执行相关功能（回车默认为1）：\n 1.自动登录(enter default);\n 2.隐私错误自动点击;\n 3.重新输入账号密码;\n 序号：")
        #print(key_123)
        if key_123=="2":
            time.sleep(2)
            bianLiTab(2)
        elif key_123=="1" or key_123=="":
            time.sleep(2)
            bianLiTab(1)
        elif key_123=="exit":
            break
        elif key_123=="3":
            global userName,passWord
            userName=input("请输入要登录的用户名：")
            passWord=getpass.getpass("请输入用户密码：")
        else:
            continue
    #os.system("pause")
    driver.quit()


if __name__=="__main__":
    main()
