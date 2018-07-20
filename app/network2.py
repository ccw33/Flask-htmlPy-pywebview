#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import platform
import re
import psutil
import netifaces
import time
import pywifi
from pywifi import const


def get_netcard():
    netcard_info = []
    net_info = psutil.net_if_addrs()
    for netcard_name,v in net_info.items():
        if len(v) == 1:
            netcard_info.append({'lan':netcard_name, 'ip':'', 'subnet_mask':'', 'gateway':'', 'dns':''})
        else:
            for item in v:
                if item[0] == 2 and not item[1] == '127.0.0.1':
                    netcard_info.append({'lan':netcard_name, 'ip':item[1], 'subnet_mask':item[2], 'gateway':get_gateway(netcard_name), 'dns':get_dns()})
    return netcard_info

def get_gateway(dev):
    netcard_gateway =[]
    gateways = netifaces.gateways()
    for gateway in gateways.items():
        if not gateway[0] == 'default':
            for item in gateway[1]:
                if item[1] == dev:
                    netcard_gateway = item[0]
    return netcard_gateway

def get_dns():
    path = os.path.join('/etc', 'resolv.conf')
    with open(path, 'r') as fr:
        text = fr.read()
        dns = re.findall(r'\d+\.\d+\.\d+\.\d+', text)[0]
    return dns

def get_os_type():
    name = platform.platform().lower()
    if 'ubuntu' in name:
        print 'ubuntu'
    elif 'debian' in name:
        print 'debian'
    elif 'centos' in name:
        print 'centos'
    elif 'windows' in name:
        print 'windows'
    else:
        print 'other'

def get_wifi_list():
    wifi_list = []
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    #print iface.name()
    scan_results = iface.scan_results()
    for results in scan_results:
        wifi_list.append(results.ssid)
    return wifi_list

def connect_wif(ssid, key):
    wifi = pywifi.PyWiFi()

    iface = wifi.interfaces()[0]
    '''
    print iface.name()
    scan_results = iface.scan_results()
    for results in scan_results:
        print results.ssid
    '''
    iface.disconnect()
    time.sleep(1)
    assert iface.status() in\
        [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = key

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)

    iface.connect(tmp_profile)
    time.sleep(30)
    assert iface.status() == const.IFACE_CONNECTED
'''
    iface.disconnect()
    time.sleep(1)
    assert iface.status() in\
        [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]
'''

if __name__ == "__main__":
    print get_netcard()
    get_os_type()
    print get_wifi_list()
    connect_wif('zwol','12345678')