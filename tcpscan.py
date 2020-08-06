#!/usr/bin/env python3
import traceback
import argparse
import os
import pathlib
import socket
import ipaddress
import itertools
import multiprocessing as mp
#
#
def _resolve(host):
    try:
        (main, __, ips) = socket.gethostbyaddr(host)
        return (ips[0], main)
    #
    except socket.gaierror: pass
    except socket.herror: pass
#
#
def resolve_targets(targets):
    pool = mp.Pool(mp.cpu_count())
    targets = pool.map(_resolve, targets)
    return list(filter(None, targets))
#
#
def get_ip_type(ip):
    types = {4: socket.AF_INET, 6: socket.AF_INET6}
    ip = ipaddress.ip_address(ip)
    return types[ip.version]
#
#
def _tcpscan(target):
    status = 1
    sock_type = get_ip_type(target[0])
    client = socket.socket(sock_type, socket.SOCK_STREAM)
    #
    try:
        client.settimeout(float(16))
        client.connect(target)
    #
    except socket.timeout: status = 2
    except socket.error: status = 0
    else: client.close()
    #
    return (target[1], status)
#
#
def scan_ports(hosts, ports): pass
#
#
def read_input_list(fname):
    fname = os.path.expanduser(fname)
    fname = pathlib.Path(fname)
    #
    data = fname.read_text()
    data = data.split('\n')
    return list(filter(None, data))
#
#
def get_port_range(ports):
    ports = ports.split(',')
    #
    single = list(filter(str.isdigit, ports))
    single = list(map(int, single))
    #
    ranges = list(itertools.filterfalse(str.isdigit, ports))
    ports = single
    #
    for item in ranges:
        (first, second) = list(map(int, item.split('-')))
        item = [__ for __ in range(first, (second+1))]
        ports.extend(item)
    #
    ports.sort()
    return ports
#
#
def get_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('target', help='Set IPv4/6 or file.')
    parser.add_argument('-p', dest='port', help='Set dest. ports: 21-22,80,443')
    parser.add_argument('-o', dest='output', help='Set output file.')
    #
    return parser.parse_args(args)
#
#
def main(args=None): pass
#
#
if __name__ == '__main__': main()
