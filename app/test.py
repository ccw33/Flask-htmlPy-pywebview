#!/usr/bin/env python
# -*- coding:utf-8 -*-
from scapy.all import srp, Ether, ARP, conf, get_if_hwaddr, get_if_addr
import time

ipscan = '172.16.125.67/24'
import socket
import fcntl
import struct


def ip_conflict():
    start = time.clock()
    print "start time", start
    d = dict()
    ip_me = get_if_addr('enp1s0')
    mac_me = get_if_hwaddr('enp1s0')
    d[ip_me] = mac_me
    while True:
        end = time.clock()
        # print "endtime",end
        # print "??:"
        # print int(end-start)
        if int(end - start) > 2:
            print ('Timeout!!!')
            break
        try:
            ans, unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF") / ARP(pdst=ipscan), timeout=2, verbose=False)
        except Exception, e:
            print str(e)
        else:
            print ("   MAC           --   IP   ")
            for snd, rcv in ans:
                list_mac = rcv.sprintf("%Ether.src% -- %ARP.psrc%")
                mac = rcv.sprintf("%Ether.src%")
                ip = rcv.sprintf("%ARP.psrc%")
                if ip not in d:
                    d[ip] = mac
                else:
                    if mac != d[ip]:
                        print "**************存在ip地址冲突*************"
                        if ip == ip_me:
                            print "IP地址为:", ip
                            print "与本机的ip地址冲突"
                            print "冲突的mac地址", mac_me, d[ip]
                        else:
                            print ""
                            print "IP地址为:", ip
                            print "冲突的mac地址为", mac, d[ip]
                        print "*****************************************"
                print list_mac
    print d


ip_conflict()
# print get_if_hwaddr('wlan0')
# print get_if_addr('wlan0')
print "byebye"