#!/usr/bin/env python
# -*- coding: utf-8 -*-

import NetworkManager
import uuid
import os

def getNetworkInfo():
    c = NetworkManager.const
    networkInfos = []

    for conn in NetworkManager.NetworkManager.ActiveConnections:
        settings = conn.Connection.GetSettings()

        for s in list(settings.keys()):
            if 'data' in settings[s]:
                settings[s + '-data'] = settings[s].pop('data')

        secrets = conn.Connection.GetSecrets()
        for key in secrets:
            settings[key].update(secrets[key])

        devices = ""
        if conn.Devices:
            networkInfo = {}
            devices = "%s" % ", ".join([x.Interface for x in conn.Devices])
            size = max([max([len(y) for y in list(x.keys()) + ['']]) for x in settings.values()])
            lan = "%s" % ", ".join([x.Interface for x in conn.Devices])
            networkInfo.update(lan=lan)
            for key, val in sorted(settings.items()):
                for name, value in val.items():
                    #print name, value
                    if name == 'id':
                        networkInfo.update(id=value)
                    if name == 'mac-address':
                        networkInfo.update(mac=value)
                    if key == 'ipv4' and name == 'method':
                        #networkInfo.update(method=value)
                        if value == 'auto':
                            networkInfo.update(is_auto=True)
                        else:
                            networkInfo.update(is_auto=False)
                    if key == 'ipv4' and value and name == 'addresses':
                        networkInfo.update(ip=value[0][0])
                        networkInfo.update(subnet_mask=str(intToMask(value[0][1])))
                        #networkInfo.update(gateway=value[0][2])
                    if key == 'ipv4' and value and name == 'gateway':
                        networkInfo.update(gateway=value)
                    if key == 'ipv4' and value and name == 'dns':
                        networkInfo.update(dns=value[0])
        networkInfos.append(networkInfo)
    return networkInfos

def setNetwork(id, mac, address, netmask, gateway, dns):
    conn_info = {
        'connection':{'id':id,
                      'type':'802-3-ethernet',
                      'uuid':str(uuid.uuid4())},
        '802-3-ethernet':{'mac-address':mac},
        'ipv4':{'method':'manual',
                'addresses':[(address, maskToInt(netmask), gateway)],
                'gateway':gateway,
                'dns':[dns]},
        'ipv6':{'method':'auto'}
    }
    file = '/etc/NetworkManager/system-connections/%s' % (id)
    if os.path.exists(file):
        os.remove(file)
    NetworkManager.Settings.AddConnection(conn_info)
    NetworkManager.Settings.ReloadConnections()

def setDHCP(id, mac):
    conn_info = {
        'connection':{'id':id,
                      'type':'802-3-ethernet',
                      'uuid':str(uuid.uuid4())},
        '802-3-ethernet':{'mac-address':mac},
        'ipv4':{'method':'auto'},
        'ipv6':{'method':'auto'}
    }
    file = '/etc/NetworkManager/system-connections/%s' % (id)
    if os.path.exists(file):
        os.remove(file)
    NetworkManager.Settings.AddConnection(conn_info)
    NetworkManager.Settings.ReloadConnections()

def getWifiList():
    wifi_lists = {}
    wifi_list =[]
    for dev in NetworkManager.NetworkManager.GetDevices():
        if dev.DeviceType != NetworkManager.NM_DEVICE_TYPE_WIFI:
            continue
        for ap in dev.GetAccessPoints():
            wifi_dict = {}
            print('%-30s %dMHz %d%%' % (ap.Ssid, ap.Frequency, ap.Strength))
            wifi_dict.update(name=ap.Ssid)
            wifi_dict.update(strength=ap.Strength)
            wifi_list.append(wifi_dict)
    wifi_lists.update(wifi_list=wifi_list)
    return wifi_lists

def connectWifi(id, mac, name, password):
    conn_info = {
        'connection':{'id':id,
                      'type':'802-11-wireless',
                      'uuid':str(uuid.uuid4())},
        '802-3-ethernet':{'mac-address':mac},
        'ipv4':{'method':'auto'},
        'ipv6':{'method':'auto'}
    }
    file = '/etc/NetworkManager/system-connections/%s' % (id)
    if os.path.exists(file):
        os.remove(file)
    NetworkManager.Settings.AddConnection(conn_info)
    NetworkManager.Settings.ReloadConnections()

def maskToInt(mask):
    count_bit = lambda bin_str: len([i for i in bin_str if i == '1'])
    mask_splited = mask.split('.')
    mask_count = [count_bit(bin(int(i))) for i in mask_splited]
    return sum(mask_count)

def intToMask(n):
    bin_arr = ['0' for i in range(32)]
    for i in range(n):
        bin_arr[i] = '1'
    tmpmask = [''.join(bin_arr[i * 8: i * 8 + 8]) for i in range(4)]
    tmpmask = [str(int(tmpstr, 2)) for tmpstr in tmpmask]
    return '.'.join(tmpmask)

if __name__ == '__main__':
    # print maskToInt('255.255.255.0')
    # print intToMask(16)
    #networkInfos = getNetworkInfo()
    #print(networkInfos)
    # for networkInfo in networkInfos:
    #     print networkInfo
    #setDHCP('Wired connection 1', '00:0c:29:35:c1:f9')
    #setDHCP('Wired connection 2', '00:0c:29:35:c1:03')
     setNetwork('net1', 'ec:d6:8a:1c:b2:d4', '172.16.110.108', '255.255.255.0', '172.16.110.254', '114.114.114.114')
    #setNetwork('Wired connection 2', '00:0c:29:35:c1:03', '192.168.1.250', '255.255.255.0', '192.168.1.254', '8.8.8.8')
    # getWifiList()

