#encoding:utf-8
import sys
import requests
import Conf

base_url = 'http://%s:%s/' % (Conf.host,Conf.port)

if __name__=="__main__":
    if sys.argv[1] == 'ip':
        requests.post(base_url + 'open_ip_setting')
    elif sys.argv[1] == 'wifi':
        requests.post(base_url + 'open_wifi_list')
    elif sys.argv[1] == 'wifi_set':
        requests.post(base_url + 'open_wifi_setting')

