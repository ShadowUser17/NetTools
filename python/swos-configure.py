#!/usr/bin/env python3
#import argparse
import traceback
import requests
import binascii
import socket
import time

def ip_to_net(address):
    tmp = socket.inet_aton(address)
    tmp = bytearray(tmp)
    tmp.reverse()
    return '0x' + tmp.hex()


url = 'http://192.168.88.1/'
login = 'admin'
passwd = ''

auth = requests.auth.HTTPDigestAuth(login, passwd)

snmp_community = binascii.hexlify(b'public')
snmp_contact = binascii.hexlify(b'')
snmp_location = binascii.hexlify(b'')

sys_address = ip_to_net('172.17.1.100')
sys_name = binascii.hexlify(b'MTK')
sys_vlan = hex(200)


try:
    params = {
        'rstp.b': "ena:0x00",
        'snmp.b': "en:0x01,com:'{com}',ci:'{ci}',loc:'{loc}'".format(
            com=snmp_community.decode(), ci=snmp_contact.decode(), loc=snmp_location.decode()
        ),
        'sys.b': "iptp:0x01,sip:{ip},id:'{id}',alla:0x00,allm:0x00,allp:0x3f,avln:{vlan},wdt:0x00,ivl:0x00,igmp:0x00,dsc:0x00".format(
            ip=sys_address, id=sys_name.decode(), vlan=sys_vlan
        )
    }

    for (key,val) in params.items():
        val = '{' + val + '}'
        print(key, val, requests.post(url + key, data=val, auth=auth))
        time.sleep(1)

except Exception:
    traceback.print_exc()
