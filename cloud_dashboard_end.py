#encoding:utf-8
import sys
from flask import Flask,render_template,Response,request
# from app.network import get_netcard
from app import network
import json
from app import windows
import webview
import multiprocessing


app = Flask(__name__,static_folder='dist/static',template_folder='dist')

# 解决jinja和vue的冲突
app.jinja_env.variable_start_string = '#{ '
app.jinja_env.variable_end_string = ' }#'

ip_win_receiver, ip_win_sender = multiprocessing.Pipe()
wifi_list_receiver, wifi_list_sender = multiprocessing.Pipe()
wifi_link_receiver, wifi_link_sender = multiprocessing.Pipe()


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/get_lans')
def get_lans_data():
    # 跨域和返回数据设置
    # info=[
    #       {
    #         'lan': '111',
    #         'is_auto': False,
    #         'ip': '172.10.1.2',
    #         'subnet_mask': '125.214.12.0',
    #         'gateway': '158.158.12.1',
    #         'dns': '15.125.67.25'
    #       },
    #     ]
    # resp = Response(json.dumps(info), mimetype='application/json')
    try:
        resp = Response(json.dumps(network.getNetworkInfo()), mimetype='application/json')
    except Exception  as e:
        resp = Response(json.dumps({'content':e.message}), mimetype='application/json',status=500)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/save_lan',methods=['POST'])
def save_lan():
    # 跨域和返回数据设置
    data = request.form.to_dict()
    try:
        # network.setNetwork(data['id'], data['mac'], data['ip'], data['subnet_mask'], data['gateway'], data['dns'])
        resp = Response(json.dumps({'content': 'success'}), mimetype='application/json',status=200)
    except Exception as e:
        resp = Response(json.dumps({'content': e.message}), mimetype='application/json',status=500)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/get_wifis')
def get_wifis_data():
    try:
        wifi_list = network.getWifiList().wifi_list
        resp = Response(json.dumps(wifi_list), mimetype='application/json')
    except Exception  as e:
        resp = Response(json.dumps({'content':e.message}), mimetype='application/json',status=500)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/open_ip_setting',methods=['POST'])
def open_ip_window():
    p = multiprocessing.Process(target=windows.ip_window,args=(ip_win_receiver,))
    p.start()
    return ''

@app.route('/open_wifi_list',methods=['POST'])
def open_wifi_list():
    p = multiprocessing.Process(target=windows.wifi_list,args=(wifi_list_receiver,))
    p.start()
    return ''

@app.route('/open_wifi_setting',methods=['POST'])
def open_wifi_window():
    wifi_list_sender.send(True)#关闭wifi_list
    p = multiprocessing.Process(target=windows.wifi_link,args=(wifi_link_receiver,))
    p.start()
    return ''


@app.route('/close_window',methods=['POST'])
def close_window():
    a = request.form

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'ip':
            open_ip_window()
        elif sys.argv[1] == 'wifi':
            open_wifi_list()
        elif sys.argv[1] == 'wifi_set':
            open_wifi_window()
    else:
        app.debug=True
        app.run(host='0.0.0.0',port='5000')
