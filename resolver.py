#!/usr/bin/env python3
import traceback
import argparse
import ipaddress
import socket
import multiprocessing as mp


def resolve_host(host):
    try:
        host = socket.gethostbyname_ex(host)
        return (host[0], host[-1])

    except (socket.gaierror, socket.herror):
        return (host, [])


def resolve_ip(ip):
    try:
        ip = socket.gethostbyaddr(ip)
        return (ip[0], ip[-1])

    except (socket.gaierror, socket.herror):
        return (ip, [])


def file_reader(fname):
    with open(fname) as fd:
        for line in fd:
            yield line.rstrip('\n')


def cidr_iter(cidr):
    for netitem in cidr:
        network = ipaddress.ip_network(netitem)

        for item in network.hosts():
            yield str(item)


def pool_exec(func, data):
    pool = mp.Pool(mp.cpu_count())
    yield from iter(pool.map(func, data))


def print_result(result):
    for (host, ips) in result:
        ips = ', '.join(ips)
        print('[{} -> {}]'.format(host, ips))


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input', help='Set input list.')
    parser.add_argument('-H', dest='to_host', help='Resolve hosts or ips.', action='store_true')
    return parser.parse_args(args)


def main(args=None):
    try:
        args = parse_args(args)
        data = file_reader(args.input)

        if args.to_host:
            result = pool_exec(resolve_host, data)
            print_result(result)

        else:
            data = cidr_iter(data)
            result = pool_exec(resolve_ip, data)
            print_result(result)

    except Exception:
        traceback.print_exc()


if __name__ == '__main__':
    main()
