# -- coding: utf-8 --

	# theme:广州航海学院教务系统成绩查询
	# created by ansion
	# qq 77931774
	# creating time 2017年4月11日
  	# python3.5

import requests
from random import choice
from lxml import etree
from pyquery import PyQuery as pq
import re
from PIL import Image
import os
import webbrowser
import getpass

print(
    """
    **************************************
    *    广州航海学院教务系统成绩查询    *
    *           author:ansion            *
    *            version:1.0             *
    **************************************
    """
)

def user_agents():
    user_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'
    ]
    return choice(user_agents)

# username = input('请输入学号:')     #学号
# pwd = getpass.getpass('请输入密码:')           #密码
username = ''
pwd = ''

index_url = 'http://jw.gzhmt.edu.cn/'
verifyCode_url = 'http://jw.gzhmt.edu.cn/CheckCode.aspx'
redirect_url = index_url+'/xs_main.aspx?xh='
login_url = 'http://jw.gzhmt.edu.cn/default2.aspx'

session = requests.Session()

#可选伪装参数
session.headers['User-Agent'] = user_agents()
session.headers['Upgrade-Insecure-Requests'] = '1'
session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
session.headers['Accept-Language'] = 'zh-CN,zh;q=0.8'

#递归验证登录，保存验证码图片，人工识别输入
def postLogin(name='',password=''):
    #请求首页，获取cookie,便于发送验证码验证
    session.get(index_url)
    verifyCode_img = session.get(verifyCode_url).content
    files = open('code.jpg', 'wb')
    files.write(verifyCode_img)
    files.close()

    global username
    global pwd

    if name == '':
        username = input('请输入学号:')
    if password == '':
        pwd = input('请输入密码:')
    #自动打开灰度处理的验证码
    im = Image.open('code.jpg')
    im = im.resize((150,60))
    RGB = im.convert('L')
    RGB.show()
    code = input('请输入验证码:')

    data = {
        '__VIEWSTATE':'dDwyODE2NTM0OTg7Oz7+DvlAiI3NmiHC6YJdsiHmUYfo+w==',
        'txtUserName':username,
        'TextBox2':pwd,
        'txtSecretCode':code,
        'RadioButtonList1':'学生',
        'Button1':'',
        'lbLanguage':'',
        'hidPdrs':'',
        'hidsc':''
    }

    # 发送登录请求
    result = session.post(login_url, data=data, allow_redirects=False)
    if result.status_code == 200:
        if re.search("验证码不正确",result.text):
            print('验证码错误')
            postLogin(username,pwd)
        elif re.search("密码错误",result.text):
            print('密码错误')
            postLogin(username)
        else:
            print('学号错误')
            postLogin('',pwd)
    elif result.status_code == 302:
        return

postLogin()

session.headers['Host'] = 'jw.gzhmt.edu.cn'
result = session.post(redirect_url+username)

selector = etree.HTML(result.text)
checkGrade = selector.xpath('//*[@id="headDiv"]/ul/li[6]/ul/li[5]/a')
checkGrade = index_url+checkGrade[0].get('href')

#必须伪装参数
session.headers['Referer'] = index_url+'/xs_main.aspx?xh='+username

#发送成绩查询页面请求
grede = session.get(checkGrade,allow_redirects=False)
xs_main = grede.text
selector = etree.HTML(xs_main)
form_action = index_url+selector.xpath('//*[@id="Form1"]')[0].get('action')
viewstate = selector.xpath('//*[@id="Form1"]/input[3]')[0].get('value')

data = {
    '__EVENTTARGET':'',
    '__EVENTARGUMENT':'',
    '__VIEWSTATE':viewstate,
    'hidLanguage':'',
    'ddlXN': '',
    'ddlXQ': '',
    'ddl_kcxz': '',
    'btn_zcj': '历年成绩',

}

#发送历年成绩查询
session.headers['Referer'] = form_action
r = session.post(form_action, data=data)
html = pq(r.text)
info = html('table#Datagrid1 tr')

#学科总数
length = info.length-1
#总绩点
sum_gpa = 0
fail_sum_gpa = 0
#课程总学分
sum_credit = 0
fail_sum_credit = 0

#学分绩点计算公式：(课程学分1*绩点+..+课程学分n*绩点)/(课程学分1+...+课程学分n)
#设x = (课程学分1*绩点+..+课程学分n*绩点)
x = 0

#所有科目集合
all = []
#不及格的科目集合
fail = []
#缺考/无绩点科目集合
absent = []
#最新的科目集合
recent = []

#判断字符串是否为数字
def is_num_by_except(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

#获取所有科目
for i in info[1:]:
    tr = pq(i)
    gpa = tr('td').eq(7).text()
    time = tr('td').eq(0).text()
    term = tr('td').eq(1).text()
    name = tr('td').eq(3).text()
    type = tr('td').eq(4).text()
    type2 = tr('td').eq(5).text()
    credit = tr('td').eq(6).text()
    score = tr('td').eq(8).text()
    if str(gpa) == '': #绩点为空则为缺考科目
        gpa = 0
        absent.append([time,term,name,type,type2,credit,gpa,score])
    if isinstance(score,str) and score == '不及格' or is_num_by_except(score) and int(score) < 60:
        second_score = tr('td').eq(10).text()
        fail.append([time,term,name,type,type2,credit,float(gpa),score,second_score])
    all.append([time,term,name,type,type2,credit,float(gpa),score])

print('\n所有课程：年份 学期 科目 类型 绩点 成绩')
for i in all:
    gpa = i[6]
    credit = float(i[5])
    sum_gpa += gpa
    sum_credit += credit
    x += credit*gpa
    print(i[0],i[1],i[2],i[3],i[4],i[6],i[7])
    
#平均学分绩点
avg_credit_gpa = round(x/sum_credit, 2)

print('总共有%d门课程'%length)
print('总绩点为:',sum_gpa)
print('总学分为:',sum_credit)
print('平均绩点为%.2f'%avg_credit_gpa)

print('\n不及格课程：年份 学期 科目 类型 绩点 成绩 补考成绩')
for i in fail:
    fail_gpa = i[6]
    fail_credit = float(i[5])
    fail_sum_gpa += fail_gpa
    fail_sum_credit += fail_credit
    print(i[0], i[1], i[2], i[3], i[4], i[6], i[7],i[8])

print('总共有%d门不及格课程'%len(fail))
print('总绩点为:',fail_sum_gpa)
print('总不及格学分为%.2f'%fail_sum_credit)

#最新的年月与学期
recent_time = str(all[-1][0])
recent_term = int(all[-1][1])

print('\n最新学期的课程成绩：年份 学期 科目 类型 绩点 成绩')
for i in all[::-1]:
    if str(i[0]) == recent_time and int(i[1]) == recent_term:
        print(i[0],i[1],i[2],i[3],i[6],i[7])

print('\n如果你觉得这个程序很有趣的话，请访问源码地址给作者1个star哦\n1：退出\n2：重新查询\n3：访问源码地址')
status = int(input('\n输入:'))
if status == 1:
    exit()
elif status == 2:
    os.system(os.path.realpath(os.sys.argv[0]))
else:
    webbrowser.open('https://github.com/ansionfor/python-query-edu-system')
