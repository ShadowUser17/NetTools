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
        #return (ips[0], main)
        return ips[0]
    #
    except socket.gaierror: pass
    except socket.herror: pass
#
#
def resolve_targets(targets):
    'Return: [(ip, fqdn), ...]'
    pool = mp.Pool(mp.cpu_count())
    targets = pool.map(_resolve, targets)
    return list(filter(None, targets))
#
#
def get_ip_type(ip):
    'Return: AF_INET/AF_INET6'
    types = {4: socket.AF_INET, 6: socket.AF_INET6}
    ip = ipaddress.ip_address(ip)
    return types[ip.version]
#
#
def _tcpscan(target):
    'target=(ip, port)'
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
def scan_ports(hosts, ports):
    'Return: [(host, [(port, stat), ...]), ...]'
    pool = mp.Pool(mp.cpu_count())
    items = []
    #
    for host in hosts:
        target = itertools.repeat(host, len(ports))
        res = pool.map(_tcpscan, zip(target, ports))
        items.append((host, res))
    #
    return items
#
#
def read_input_list(fname):
    'Return: [item, ...]'
    fname = os.path.expanduser(fname)
    fname = pathlib.Path(fname)
    #
    data = fname.read_text()
    data = data.split('\n')
    return list(filter(None, data))
#
#
def get_port_range(ports):
    'Return: [port, ...]'
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
def format_output(output): pass
#
#
def save_output(fname, output): pass
#
#
def get_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('target', help='Set IPv4/6 or file.')
    parser.add_argument('-p', dest='port', default='1-1023', help='Set dest. ports: 21-22,80,443')
    parser.add_argument('-w', dest='output', help='Set output file.')
    parser.add_argument('-O', dest='open', action='store_true', default=True, help='Show open ports only.')
    #
    return parser.parse_args(args)
#
#
def main(args=None):
    try:
        args = get_args(args)
        hosts = None
        #
        if os.path.isfile(args.target): hosts = read_input_list(args.target)
        else: hosts = args.target
        #
        ports = get_port_range(args.port)
        hosts = resolve_targets(hosts)
        #
        res = scan_ports(hosts, ports)
        for item in res: print(item)
    #
    except Exception: traceback.print_exc()
#
#
if __name__ == '__main__': main(['./targets.txt', '-p', '1122,80,443,8080'])
