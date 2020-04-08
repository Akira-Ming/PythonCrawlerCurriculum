import os
import re
import execjs
import requests
import time
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
session = requests.Session()

window_login = tk.Tk()  # 登陆界面为主窗口
window = tk.Toplevel(window_login)  # 原主界面为子窗口
window_login.title('AkiraMing课表查询')  # 解决弹出窗口五标题
window.withdraw()  # 解决运行时同时弹出两个窗口

sw = window.winfo_screenwidth()
# 得到屏幕宽度
sh = window.winfo_screenheight()
# 得到屏幕高度
ww = 1155
wh = 639
# 窗口宽高为100
x = (sw - ww) / 2 - 10
y = (sh - wh) / 2 - 20
window.geometry("%dx%d+%d+%d" % (ww, wh, x, y))  # 居中

window.resizable(0, 0)
window_login.resizable(0, 0)


def loginWindow():
    def print_entry():
        # 记录账号和密码参数
        userinfo = {'Account': '', 'Password': ''}
        userinfo['Account'] = var.get()
        userinfo['Password'] = var2.get()
        # 写入文件
        file_handle = open('UserInfo.ini', mode='w')
        file_handle.write(str(userinfo))
        file_handle.close()
        # window.update()
        pswTureOrFalse()  # 开启密码是否错误
        window.deiconify()
        window.update()
        window_login.destroy()

    def print_exit():
        window.destroy()
        window.quit()
        window_login.destroy()
        window_login.quit()

    # def exitevents(*e):  # 让红叉按钮无效函数
    #     pass
    window_login.title("你还没有登陆过(＾Ｕ＾)ノ~ＹＯ")
    # 得到屏幕宽度
    sw = window.winfo_screenwidth()
    # 得到屏幕高度
    sh = window.winfo_screenheight()
    ww = 710
    wh = 400
    # 窗口宽高为100
    x = (sw - ww) / 2 - 10
    y = (sh - wh) / 2 - 100
    window_login.geometry("%dx%d+%d+%d" % (ww, wh, x, y))  # 居中
    window_login.wm_attributes('-topmost', 1)  # 窗口置顶
    # window_login.protocol("WM_DELETE_WINDOW", exitevents)  # 让红叉按钮无效
    window_login.deiconify()
    window_login.update()
    tk.Label(window_login,
             text='''
检测到您是第一次使用本程序，请输入账户信息，之后使用便可不在需要输入！\n
使用条件：你的账号修改过密码，不是学号做密码!!\n
使用条件：你的账号修改过密码，不是学号做密码!!!!\n
使用条件：你的账号修改过密码，不是学号做密码!!!!!!
        ''',
             font=('楷体', 14)).pack()

    # 框架
    frame_login = tk.Frame(window_login)
    frame_login.pack()
    # 第一行账号输入框
    username = tk.Label(frame_login,
                        text='账户：',
                        font=('微软雅黑', 16),
                        padx=5,
                        pady=15)
    username.grid(row=0)

    var = tk.StringVar()
    # 设置输入框对应的文本变量为var
    tk.Entry(frame_login, textvariable=var, font=16).grid(row=0, column=1)
    # 第二行密码输入框
    pw = tk.Label(frame_login, text='密码：', font=('微软雅黑', 16), padx=5, pady=15)
    pw.grid(row=1)

    var2 = tk.StringVar()
    # 设置输入框对应的文本变量为var
    ps = tk.Entry(frame_login, font=16, textvariable=var2)
    ps.grid(row=1, column=1)  # 设置输入框对应的文本变量为var
    ps['show'] = '*'  # 隐藏显示
    # 第三行按钮事件
    frame_button = tk.Frame(window_login)
    frame_button.pack()

    tk.Button(frame_button, text="登陆", font=('微软雅黑', 16),
              command=print_entry).grid(row=0, column=0, padx=25, pady=15)
    tk.Button(frame_button, text="取消", font=('微软雅黑', 16),
              command=print_exit).grid(row=0, column=1, padx=25, pady=15)
    # quit关闭窗口，destroy摧毁窗口
    window_login.mainloop()


def getLogon_encoded():
    # 读取加密方法js文件
    with open(r'./Lib/conwork.js') as f:
        ctx = execjs.compile(f.read())

    # 读取account,pwd
    file_handle = open('UserInfo.ini', mode='r')  # 打开
    user_xx = eval(file_handle.read())  # str转dic读取
    file_handle.close()  # 关闭
    # 账户密码加密
    encoded = ctx.call('encodeInp', user_xx['Account']) + '%%%' + ctx.call(
        'encodeInp', user_xx['Password'])
    return encoded


def logonWeb():
    logon_data = {"encoded": getLogon_encoded()}
    logon_url = "http://54.222.196.251:81/gllgdxbwglxy_jsxsd/xk/LoginToXk"
    session.post(logon_url, data=logon_data)


def getName():
    logonWeb()
    myName_html = session.get(
        "http://54.222.196.251:81/gllgdxbwglxy_jsxsd/xskb/xskb_list.do")
    myName = re.findall('nc" style="color: #000000;">(.*?)</div>',
                        myName_html.text)
    return myName[0]


def pswTureOrFalse():  # 密码是否错误
    logonWeb()
    login_html = session.get(
        "http://54.222.196.251:81/gllgdxbwglxy_jsxsd/xskb/xskb_list.do")
    login = re.findall('color="red">(.*?)</font>', login_html.text)
    lg = ['请先登录系统']
    mmcw = 'no'
    if login == lg:
        window_login.withdraw()
        # window_login.destroy()
        mmcw = tkinter.messagebox.showerror('错误', '用户名或密码错误，请重新出入！！')
    if mmcw == 'ok':
        loginWindow()


def getWeek():
    weeks_html = session.get(
        "http://54.222.196.251:81/gllgdxbwglxy_jsxsd/xskb/xskb_list.do")
    weeks = re.findall('<option value="(.*?)"  >第.*?</option>',
                       weeks_html.text)
    return weeks


def getSemester():
    semester_html = session.get(
        "http://54.222.196.251:81/gllgdxbwglxy_jsxsd/xskb/xskb_list.do")
    semesters = re.findall('<option value="(.*?)" .*?>2.*?</option>',
                           semester_html.text)
    return semesters


def getHtml():
    data = {"zc": combobox_week.get(), "xnxq01id": combobox_semester.get()}
    curriculum_url = 'http://54.222.196.251:81/gllgdxbwglxy_jsxsd/xskb/xskb_list.do'  # 课表链接
    bwjwc = session.post(curriculum_url, data=data).text
    return bwjwc


def cl_class(jsxx):  # 获取教室
    zi = []
    for i in jsxx:
        i = re.findall("title='教室'>(.*?)<", i)
        zi.append(i)
    return zi


def getDajie():
    bwjwc = getHtml()
    xq1 = re.findall('<div id=".*?-1-1".*?kbcontent1">(.*?)<', bwjwc)
    xq1 = ['' if i == '&nbsp;' else i for i in xq1]
    xq1_cs = re.findall('<div id=".*?-1-1".*?kbcontent1.*?>(.*?)</div>', bwjwc)
    xq1_class = cl_class(xq1_cs)
    xq1_class = ['' if a == [] else a for a in xq1_class]

    xq2 = re.findall('<div id=".*?-2-1".*?kbcontent1">(.*?)<', bwjwc)
    xq2 = ['' if i == '&nbsp;' else i for i in xq2]
    xq2_cs = re.findall('<div id=".*?-2-1".*?kbcontent1.*?>(.*?)</div>', bwjwc)
    xq2_class = cl_class(xq2_cs)
    xq2_class = ['' if i == [] else i for i in xq2_class]

    xq3 = re.findall('<div id=".*?-3-1".*?kbcontent1">(.*?)<', bwjwc)
    xq3 = ['' if i == '&nbsp;' else i for i in xq3]
    xq3_cs = re.findall('<div id=".*?-3-1".*?kbcontent1.*?>(.*?)</div>', bwjwc)
    xq3_class = cl_class(xq3_cs)
    xq3_class = ['' if i == [] else i for i in xq3_class]

    xq4 = re.findall('<div id=".*?-4-1".*?kbcontent1">(.*?)<', bwjwc)
    xq4 = ['' if i == '&nbsp;' else i for i in xq4]
    xq4_cs = re.findall('<div id=".*?-4-1".*?kbcontent1.*?>(.*?)</div>', bwjwc)
    xq4_class = cl_class(xq4_cs)
    xq4_class = ['' if i == [] else i for i in xq4_class]

    xq5 = re.findall('<div id=".*?-5-1".*?kbcontent1" >(.*?)<', bwjwc)
    xq5 = ['' if i == '&nbsp;' else i for i in xq5]
    xq5_cs = re.findall('<div id=".*?-5-1".*?kbcontent1.*?>(.*?)</div>', bwjwc)
    xq5_class = cl_class(xq5_cs)
    xq5_class = ['' if i == [] else i for i in xq5_class]

    xq6 = re.findall('<div id=".*?-6-1".*?kbcontent1">(.*?)<', bwjwc)
    xq6 = ['' if i == '&nbsp;' else i for i in xq6]
    xq6_cs = re.findall('<div id=".*?-6-1".*?kbcontent1.*?>(.*?)</div>', bwjwc)
    xq6_class = cl_class(xq6_cs)
    xq6_class = ['' if i == [] else i for i in xq6_class]

    xq7 = re.findall('<div id=".*?-7-1".*?kbcontent1" >(.*?)<', bwjwc)
    xq7 = ['' if i == '&nbsp;' else i for i in xq7]
    xq7_cs = re.findall('<div id=".*?-7-1".*?kbcontent1.*?>(.*?)</div>', bwjwc)
    xq7_class = cl_class(xq7_cs)
    xq7_class = ['' if i == [] else i for i in xq7_class]
    # kec 课程
    kec1 = ['', '', '', '', '', '']
    for i in range(6):
        kec1[i] = str(xq1[i]) + '\n' + str(xq1_class[i])

    kec2 = ['', '', '', '', '', '']
    for i in range(6):
        kec2[i] = str(xq2[i]) + '\n' + str(xq2_class[i])

    kec3 = ['', '', '', '', '', '']
    for i in range(6):
        kec3[i] = str(xq3[i]) + '\n' + str(xq3_class[i])

    kec4 = ['', '', '', '', '', '']
    for i in range(6):
        kec4[i] = str(xq4[i]) + '\n' + str(xq4_class[i])

    kec5 = ['', '', '', '', '', '']
    for i in range(6):
        kec5[i] = str(xq5[i]) + '\n' + str(xq5_class[i])

    kec6 = ['', '', '', '', '', '']
    for i in range(6):
        kec6[i] = str(xq6[i]) + '\n' + str(xq6_class[i])

    kec7 = ['', '', '', '', '', '']
    for i in range(6):
        kec7[i] = str(xq7[i]) + '\n' + str(xq7_class[i])

    return kec1, kec2, kec3, kec4, kec5, kec6, kec7


def getTodayWeek():
    todayWeek = int(time.strftime('%W'))
    if todayWeek >= 10 and todayWeek <= 26:
        todaySchoolWeek = todayWeek - 9
    elif todayWeek >= 36:
        todaySchoolWeek = todayWeek - 35
    elif todayWeek <= 9 or (todayWeek > 26 and todayWeek <= 35):
        todaySchoolWeek = 0
    else:
        pass
    return todaySchoolWeek


if __name__ == "__main__":
    userwj = os.path.exists("UserInfo.ini")  # ture or false
    if not userwj:
        window.withdraw()
        loginWindow()
    pswTureOrFalse() #开启密码检测是否错误

# ######################### MAKE GUI ################################# #
frame_header = tk.Frame(bd=5, relief="groove")
frame_header.pack(fill="both", padx=5, pady=5)

lable_youName = tk.Label(frame_header,
                         text='欢迎您：' + getName(),
                         font=('微软雅黑', 10))
lable_youName.grid(row=0, column=0)
lable_week = tk.Label(frame_header, text='周次：', font=('微软雅黑', 10))
lable_week.grid(row=0, column=1)

combobox_week = ttk.Combobox(frame_header,
                             font=('微软雅黑', 10),
                             width=2,
                             state='readonly')
combobox_week.grid(row=0, column=2)
combobox_week['values'] = getWeek()
combobox_week.current(getTodayWeek())  # 做个标记，以后根据系统时间算第几周

lable_semester = tk.Label(frame_header, text='学年学期：', font=('微软雅黑', 10))
lable_semester.grid(row=0, column=3)
combobox_semester = ttk.Combobox(frame_header,
                                 font=('微软雅黑', 10),
                                 width=11,
                                 state='readonly')
combobox_semester.grid(row=0, column=4)
combobox_semester['values'] = getSemester()
combobox_semester.current(0)


# #####--------课程内容---------###### #
# 容器
frame_timetable = tk.Frame(bd=5, relief="groove")
# sticky='w'指定了组件在单元格中靠左对齐
frame_timetable.pack(fill="both", padx=5, pady=5)

# 内容
lable_week0 = tk.Label(frame_timetable,
                       text='',
                       font=('微软雅黑', 10),
                       bd=2,
                       relief="groove",
                       width=17,
                       height=4,
                       wraplength=130)
lable_week0.grid(row=0, column=0)
lable_week1 = tk.Label(frame_timetable,
                       text='星期一',
                       font=('微软雅黑', 10),
                       bd=2,
                       relief="groove",
                       width=17,
                       height=4,
                       wraplength=130)
lable_week1.grid(row=0, column=1)
lable_week2 = tk.Label(frame_timetable,
                       text='星期二',
                       font=('微软雅黑', 10),
                       bd=2,
                       relief="groove",
                       width=17,
                       height=4,
                       wraplength=130)
lable_week2.grid(row=0, column=2)
lable_week3 = tk.Label(frame_timetable,
                       text='星期三',
                       font=('微软雅黑', 10),
                       bd=2,
                       relief="groove",
                       width=17,
                       height=4,
                       wraplength=130)
lable_week3.grid(row=0, column=3)
lable_week4 = tk.Label(frame_timetable,
                       text='星期四',
                       font=('微软雅黑', 10),
                       bd=2,
                       relief="groove",
                       width=17,
                       height=4,
                       wraplength=130)
lable_week4.grid(row=0, column=4)
lable_week5 = tk.Label(frame_timetable,
                       text='星期五',
                       font=('微软雅黑', 10),
                       bd=2,
                       relief="groove",
                       width=17,
                       height=4,
                       wraplength=130)
lable_week5.grid(row=0, column=5)
lable_week6 = tk.Label(frame_timetable,
                       text='星期六',
                       font=('微软雅黑', 10),
                       bd=2,
                       relief="groove",
                       width=17,
                       height=4,
                       wraplength=130)
lable_week6.grid(row=0, column=6)
lable_week7 = tk.Label(frame_timetable,
                       text='星期日',
                       font=('微软雅黑', 10),
                       bd=2,
                       relief="groove",
                       width=17,
                       height=4,
                       wraplength=130)
lable_week7.grid(row=0, column=7)

tk.Label(frame_timetable,
         text='第一大节',
         font=('微软雅黑', 10),
         bd=2,
         relief="groove",
         width=17,
         height=4,
         wraplength=130).grid(row=1, column=0)
tk.Label(frame_timetable,
         text='第二大节',
         font=('微软雅黑', 10),
         bd=2,
         relief="groove",
         width=17,
         height=4,
         wraplength=130).grid(row=2, column=0)
tk.Label(frame_timetable,
         text='第三大节',
         font=('微软雅黑', 10),
         bd=2,
         relief="groove",
         width=17,
         height=4,
         wraplength=130).grid(row=3, column=0)
tk.Label(frame_timetable,
         text='第四大节',
         font=('微软雅黑', 10),
         bd=2,
         relief="groove",
         width=17,
         height=4,
         wraplength=130).grid(row=4, column=0)
tk.Label(frame_timetable,
         text='第五大节',
         font=('微软雅黑', 10),
         bd=2,
         relief="groove",
         width=17,
         height=4,
         wraplength=130).grid(row=5, column=0)
tk.Label(frame_timetable,
         text='第六大节',
         font=('微软雅黑', 10),
         bd=2,
         relief="groove",
         width=17,
         height=4,
         wraplength=130).grid(row=6, column=0)


def abc123(abc):
    # 星期一
    laji = getDajie()

    class1_1 = tk.StringVar()
    class1_1.set(laji[0][0])

    class1_2 = tk.StringVar()
    class1_2.set(laji[0][1])

    class1_3 = tk.StringVar()
    class1_3.set(laji[0][2])

    class1_4 = tk.StringVar()
    class1_4.set(laji[0][3])

    class1_5 = tk.StringVar()
    class1_5.set(laji[0][4])

    class1_6 = tk.StringVar()
    class1_6.set(laji[0][5])

    # 星期二
    class2_1 = tk.StringVar()
    class2_1.set(laji[1][0])

    class2_2 = tk.StringVar()
    class2_2.set(laji[1][1])

    class2_3 = tk.StringVar()
    class2_3.set(laji[1][2])

    class2_4 = tk.StringVar()
    class2_4.set(laji[1][3])

    class2_5 = tk.StringVar()
    class2_5.set(laji[1][4])

    class2_6 = tk.StringVar()
    class2_6.set(laji[1][5])

    # 星期三
    class3_1 = tk.StringVar()
    class3_1.set(laji[2][0])

    class3_2 = tk.StringVar()
    class3_2.set(laji[2][1])

    class3_3 = tk.StringVar()
    class3_3.set(laji[2][2])

    class3_4 = tk.StringVar()
    class3_4.set(laji[2][3])

    class3_5 = tk.StringVar()
    class3_5.set(laji[2][4])

    class3_6 = tk.StringVar()
    class3_6.set(laji[2][5])

    # 星期四
    class4_1 = tk.StringVar()
    class4_1.set(laji[3][0])

    class4_2 = tk.StringVar()
    class4_2.set(laji[3][1])

    class4_3 = tk.StringVar()
    class4_3.set(laji[3][2])

    class4_4 = tk.StringVar()
    class4_4.set(laji[3][3])

    class4_5 = tk.StringVar()
    class4_5.set(laji[3][4])

    class4_6 = tk.StringVar()
    class4_6.set(laji[3][5])

    # 星期五
    class5_1 = tk.StringVar()
    class5_1.set(laji[4][0])

    class5_2 = tk.StringVar()
    class5_2.set(laji[4][1])

    class5_3 = tk.StringVar()
    class5_3.set(laji[4][2])

    class5_4 = tk.StringVar()
    class5_4.set(laji[4][3])

    class5_5 = tk.StringVar()
    class5_5.set(laji[4][4])

    class5_6 = tk.StringVar()
    class5_6.set(laji[4][5])

    # 星期六
    class6_1 = tk.StringVar()
    class6_1.set(laji[5][0])

    class6_2 = tk.StringVar()
    class6_2.set(laji[5][1])

    class6_3 = tk.StringVar()
    class6_3.set(laji[5][2])

    class6_4 = tk.StringVar()
    class6_4.set(laji[5][3])

    class6_5 = tk.StringVar()
    class6_5.set(laji[5][4])

    class6_6 = tk.StringVar()
    class6_6.set(laji[5][5])

    # 星期日
    class7_1 = tk.StringVar()
    class7_1.set(laji[6][0])

    class7_2 = tk.StringVar()
    class7_2.set(laji[6][1])

    class7_3 = tk.StringVar()
    class7_3.set(laji[6][2])

    class7_4 = tk.StringVar()
    class7_4.set(laji[6][3])

    class7_5 = tk.StringVar()
    class7_5.set(laji[6][4])

    class7_6 = tk.StringVar()
    class7_6.set(laji[6][5])

    # 星期一
    tk.Label(frame_timetable,
             textvariable=class1_1,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=1, column=1)
    tk.Label(frame_timetable,
             textvariable=class1_2,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=2, column=1)
    tk.Label(frame_timetable,
             textvariable=class1_3,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=3, column=1)
    tk.Label(frame_timetable,
             textvariable=class1_4,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=4, column=1)
    tk.Label(frame_timetable,
             textvariable=class1_5,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=5, column=1)
    tk.Label(frame_timetable,
             textvariable=class1_6,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=6, column=1)

    # 星期二
    tk.Label(frame_timetable,
             textvariable=class2_1,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=1, column=2)
    tk.Label(frame_timetable,
             textvariable=class2_2,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=2, column=2)
    tk.Label(frame_timetable,
             textvariable=class2_3,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=3, column=2)
    tk.Label(frame_timetable,
             textvariable=class2_4,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=4, column=2)
    tk.Label(frame_timetable,
             textvariable=class2_5,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=5, column=2)
    tk.Label(frame_timetable,
             textvariable=class2_6,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=6, column=2)

    # 星期三
    tk.Label(frame_timetable,
             textvariable=class3_1,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=1, column=3)
    tk.Label(frame_timetable,
             textvariable=class3_2,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=2, column=3)
    tk.Label(frame_timetable,
             textvariable=class3_3,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=3, column=3)
    tk.Label(frame_timetable,
             textvariable=class3_4,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=4, column=3)
    tk.Label(frame_timetable,
             textvariable=class3_5,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=5, column=3)
    tk.Label(frame_timetable,
             textvariable=class3_6,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=6, column=3)

    # 星期四
    tk.Label(frame_timetable,
             textvariable=class4_1,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=1, column=4)
    tk.Label(frame_timetable,
             textvariable=class4_2,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=2, column=4)
    tk.Label(frame_timetable,
             textvariable=class4_3,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=3, column=4)
    tk.Label(frame_timetable,
             textvariable=class4_4,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=4, column=4)
    tk.Label(frame_timetable,
             textvariable=class4_5,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=5, column=4)
    tk.Label(frame_timetable,
             textvariable=class4_6,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=6, column=4)

    # 星期五
    tk.Label(frame_timetable,
             textvariable=class5_1,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=1, column=5)
    tk.Label(frame_timetable,
             textvariable=class5_2,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=2, column=5)
    tk.Label(frame_timetable,
             textvariable=class5_3,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=3, column=5)
    tk.Label(frame_timetable,
             textvariable=class5_4,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=4, column=5)
    tk.Label(frame_timetable,
             textvariable=class5_5,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=5, column=5)
    tk.Label(frame_timetable,
             textvariable=class5_6,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=6, column=5)

    # 星期六
    tk.Label(frame_timetable,
             textvariable=class6_1,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=1, column=6)
    tk.Label(frame_timetable,
             textvariable=class6_2,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=2, column=6)
    tk.Label(frame_timetable,
             textvariable=class6_3,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=3, column=6)
    tk.Label(frame_timetable,
             textvariable=class6_4,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=4, column=6)
    tk.Label(frame_timetable,
             textvariable=class6_5,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=5, column=6)
    tk.Label(frame_timetable,
             textvariable=class6_6,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=6, column=6)

    # 星期日
    tk.Label(frame_timetable,
             textvariable=class7_1,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=1, column=7)
    tk.Label(frame_timetable,
             textvariable=class7_2,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=2, column=7)
    tk.Label(frame_timetable,
             textvariable=class7_3,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=3, column=7)
    tk.Label(frame_timetable,
             textvariable=class7_4,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=4, column=7)
    tk.Label(frame_timetable,
             textvariable=class7_5,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=5, column=7)
    tk.Label(frame_timetable,
             textvariable=class7_6,
             font=('微软雅黑', 10),
             bd=2,
             relief="groove",
             width=17,
             height=4,
             wraplength=130).grid(row=6, column=7)


abc123(123)

combobox_week.bind("<<ComboboxSelected>>", abc123)
combobox_semester.bind("<<ComboboxSelected>>", abc123)

window.mainloop()
