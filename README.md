# python-query-edu-system
使用python3.5查询广州航海学院教务系统历年成绩以及最新成绩，并打包成 .exe可执行文件

    **************************************
    *    广州航海学院教务系统成绩查询      *
    *           author:ansion            *
    *            version:1.0             *
    **************************************
    
### 使用模块列表
      
    import requests
    from random import choice
    from lxml import etree
    from pyquery import PyQuery as pq
    import re
    from PIL import Image
    import os
    import webbrowser
    import getpass
 
### 网络编程流程
1. get请求教务系统首页获取cookie
2. 使用变量保存输入的学号以及密码
3. 使用cookie发送get请求到验证码地址，保存验证码并人工识别
4. 根据抓包结果填充post数据域，发送学号、密码以及验证码信息，如果返回302则为成功，返回202则为登录失败，失败后进行原因判断
5. 登陆成功后伪造Host进行首页post跳转
6. 然后伪造referer进行学生成绩查询页get请求
7. 继续伪造referer进行历年成绩post请求
8. 将历年成绩的数据进行加工处理，得出所有成绩，不及格成绩，最新成绩等等信息

### 开发工具
1. PyCharm Community Edition 2016.2.3              IDE
2. Telerik Fiddler Web Debugger v4.6.20171.14978   抓包工具
3. pyinstaller                                     打包exe
4. python 3.5.2                                    python 
 
### 写在最后
欢迎各位小伙伴对源码进行学习研究与扩展，有需要改进的地方可以提交issue或branch。
掌握了网络编程的要领后，就可以举一反三，略加修改后即可用于其他学校的教务系统或者网站

create time 2017-4-15  
项目地址：https://github.com/ansionfor/python-query-edu-system
