# encoding:utf-8
import sys
import json
import logging
import multiprocessing
import traceback

from flask import Flask, render_template, Response, request
from app import network
from app import windows
from Utils import log_utils
import Conf

logger = log_utils.Log('log/cloud_dashboard_end',level=logging.DEBUG if Conf.mode=='debug' else logging.ERROR).logger

app = Flask(__name__, static_folder='dist/static', template_folder='dist')
app.debug = True if Conf.mode=='debug' else False

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

    try:
        # 跨域和返回数据设置
        # info = [
        #     {
        #         'lan': '111',
        #         'is_auto': True,
        #         'isActive':True,
        #         'ip': '172.10.1.2',
        #         'subnet_mask': '125.214.12.0',
        #         'gateway': '158.158.12.1',
        #         'dns': '15.125.67.25',
        #         'mac': 'EC:D6:8A:1C:B2:D4',
        #         'id': "net1"
        #     },
        #     {
        #         'lan': '222',
        #         'is_auto': False,
        #         'isActive': False,
        #         'ip': '172.10.1.33',
        #         'subnet_mask': '125.214.12.0',
        #         'gateway': '158.158.12.1',
        #         'dns': '114.114.114.114',
        #         'mac': 'EC:D6:8A:1C:HH:D5',
        #         'id': "net2"
        #     },
        # ]
        # resp = Response(json.dumps(info), mimetype='application/json')
        net_info = network.getNetworkInfo()
        for index,info in enumerate(net_info):
            if index==0:
                net_info[index]['isActive']=True
                continue
            net_info[index]['isActive']=False
        resp = Response(json.dumps(net_info), mimetype='application/json')
    except Exception  as e:
        resp = Response(json.dumps({'content': e.message}), mimetype='application/json', status=500)
        logger.error(traceback.format_exc())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/save_lan', methods=['POST'])
def save_lan():
    # 跨域和返回数据设置
    data = request.form.to_dict()
    try:
        if data['is_auto'] == 'true':
            network.setDHCP(data['id'], data['mac'])
        else:
            network.setNetwork(data['id'], data['mac'], data['ip'], data['subnet_mask'], data['gateway'], data['dns'])
        resp = Response(json.dumps({'content': 'success'}), mimetype='application/json', status=200)
    except Exception as e:
        resp = Response(json.dumps({'content': e.message}), mimetype='application/json', status=500)
        logger.error(traceback.format_exc())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/get_wifis')
def get_wifis_data():
    try:
        wifi_list = network.getWifiList()['wifi_list']
        wifi_list = [
            {
                'name': '别连我dsfasefwagewt',
                'is_lock': True,
                'key_type': 'WPA2',
                'strength': 1,
            },
            {
                'name': 'dsfewdsgfew',
                'is_lock': True,
                'key_type': 'WPA2',
                'strength': 4,
            },
            {
                'name': '哈哈哈',
                'is_lock': True,
                'key_type': 'WPA2',
                'strength': 3,
            },
        ]
        resp = Response(json.dumps(wifi_list), mimetype='application/json')
    except Exception  as e:
        resp = Response(json.dumps({'content': e.message}), mimetype='application/json', status=500)
        logger.error(traceback.format_exc())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/connect_wifi', methods=['POST'])
def connect_wifi():
    try:
        data = request.form.to_dict()
        # network.connectWifi()
        wifi_pwd = {}
        with open('file/wifi_pwd', 'r') as fr:
            text = fr.read()
            if text:
                wifi_pwd = json.loads(text)
        with open('file/wifi_pwd', 'w') as fw:
            if data['remember_pwd'] == 'true':
                wifi_pwd[data['name']] = data['password']
            else:
                if data['name'] in wifi_pwd:
                    del wifi_pwd[data['name']]
            json.dump(wifi_pwd, fw)
        resp = Response(json.dumps({'content': 'success'}), mimetype='application/json')
        wifi_link_sender.send(True)
    except Exception  as e:
        resp = Response(json.dumps({'content': e.message}), mimetype='application/json', status=500)
        logger.error(traceback.format_exc())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/open_ip_setting', methods=['POST'])
def open_ip_window():
    try:
        p = multiprocessing.Process(target=windows.ip_window, args=(ip_win_receiver,))
        p.start()
    except Exception  as e:
        logger.error(traceback.format_exc())
    return ''


@app.route('/open_wifi_list', methods=['POST'])
def open_wifi_list():
    try:
        p = multiprocessing.Process(target=windows.wifi_list, args=(wifi_list_receiver,))
        p.start()
    except Exception  as e:
        logger.error(traceback.format_exc())
    return ''


@app.route('/open_wifi_setting', methods=['POST'])
def open_wifi_window():
    try:
        data = request.form.to_dict()
        append_url = '?'
        for k, v in data.items():
            append_url = append_url + k + '=' + v + '&'
        # 查看是否已经记录密码，如果已经记录则把password=dsfew&remember_pwd=true加进去
        wifi_pwd = {}
        with open('file/wifi_pwd', 'r') as fr:
            text = fr.read()
            if text:
                wifi_pwd = json.loads(text)
        if data['name'] in wifi_pwd:
            append_url = "%spassword=%s&remember_pwd=true" % (append_url, wifi_pwd[data['name']])
        wifi_list_sender.send(True)  # 关闭wifi_list
        p = multiprocessing.Process(target=windows.wifi_link, args=(wifi_link_receiver, append_url))
        p.start()
    except Exception  as e:
        logger.error(traceback.format_exc())
    return ''


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'ip':
            open_ip_window()
        elif sys.argv[1] == 'wifi':
            open_wifi_list()
        elif sys.argv[1] == 'wifi_set':
            open_wifi_window()
    else:
        app.run(host='0.0.0.0', port='5082')
