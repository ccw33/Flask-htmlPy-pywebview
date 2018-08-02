# encoding:utf-8
import threading
import re
import sys
import platform

is_windows = platform.system()=='Windows'

if is_windows:
    import webview

    def close_message_listener(receiver):
        close = receiver.recv()
        if close:
            webview.destroy_window()
            print('窗口  close')

    def open_window(receiver, title, url):
        t = threading.Thread(target=close_message_listener, args=(receiver,))  # 接收关闭信号并关闭窗口的线程
        t.start()
        uid = webview.create_window(title=title, url=url)
        return uid
    
else:
    import htmlPy
    from PySide import QtCore, QtGui

    def close_message_listener_htmlpy(receiver,web_app):
        close = receiver.recv()
        if close:
            web_app.stop()
            print('窗口  close')



def ip_window(receiver):
    '''
    打开ip窗口并返回该对象
    :return: web_app
    '''
    
    if not is_windows :
        web_app = htmlPy.WebAppGUI(title=u"Python Website",
                                   width=700, height=600,
                                   developer_mode=True)
        # 获取中心点坐标
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        x, y = re.findall(r'\d+', str(cp))
        # 修改窗口坐标
        web_app.x_pos = int(x) - web_app.width / 2
        web_app.y_pos = int(y) - web_app.height / 2
    
        # 隐藏菜单栏
        # web_app.window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    
        web_app.url = u"http://127.0.0.1:5000/#/"
        t = threading.Thread(target=close_message_listener_htmlpy,args=(receiver,web_app))#接收关闭信号并关闭窗口的线程
        t.start()
        web_app.start()
    else:
        t = threading.Thread(target=close_message_listener,args=(receiver,))#接收关闭信号并关闭窗口的线程
        t.start()
        uid = webview.create_window("网络设置", "http://localhost:5000/#/",width=700, height=600)
        return uid


def wifi_list(receiver):
    '''
    打开wifi窗口并返回该对象
    :return: web_app
    '''
    if not is_windows:
        web_app = htmlPy.WebAppGUI(title=u"Python Website",
                                   width=224, height=500,
                                   developer_mode=True)
        # 获取中心点坐标
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        x, y = re.findall(r'\d+', str(cp))
        # 修改窗口坐标
        web_app.x_pos = int(x) - web_app.width / 2
        web_app.y_pos = int(y) - web_app.height / 2

        # # 隐藏菜单栏
        # web_app.window.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        web_app.url = u"http://localhost:5000/#/wifi"

        t = threading.Thread(target=close_message_listener_htmlpy,args=(receiver,web_app))#接收关闭信号并关闭窗口的线程
        t.start()
        web_app.start()
    else:
        t = threading.Thread(target=close_message_listener,args=(receiver,))#接收关闭信号并关闭窗口的线程
        t.start()
        uid = webview.create_window("wifi列表", "http://localhost:5000/#/wifi",width=224, height=500,)
        return uid


def wifi_link(receiver):
    '''
    打开wifi窗口并返回该对象
    :return: web_app
    '''
    if not is_windows:
        web_app = htmlPy.WebAppGUI(title=u"Python Website",
                                   width=450, height=250,
                                   developer_mode=True)
        # 获取中心点坐标
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        x, y = re.findall(r'\d+', str(cp))
        # 修改窗口坐标
        web_app.x_pos = int(x) - web_app.width / 2
        web_app.y_pos = int(y) - web_app.height / 2

        # 隐藏菜单栏
        # web_app.window.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        web_app.url = u"http://127.0.0.1:5000/#/wifi_connect_win"

        t = threading.Thread(target=close_message_listener_htmlpy,args=(receiver,web_app))#接收关闭信号并关闭窗口的线程
        t.start()
        web_app.start()
    else:
        t = threading.Thread(target=close_message_listener,args=(receiver,))#接收关闭信号并关闭窗口的线程
        t.start()
        uid = webview.create_window("连接wifi", "http://localhost:5000/#/wifi_connect_win",width=450, height=250)
        return uid



if __name__ == "__main__":
    if sys.argv[1] == 'ip':
        ip_window()
    elif sys.argv[1] == 'wifi':
        wifi_link()
    elif sys.argv[1] == 'wifi_set':
        wifi_link()
