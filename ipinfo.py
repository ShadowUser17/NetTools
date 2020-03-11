#!/usr/bin/env python3
import sys
import argparse
#
from base64 import b64encode
from json import loads as json
from urllib import parse as Parser
from urllib import request as Request
from traceback import print_exc
#
#
def mkuagent():
    python = sys.version.split()
    platform = sys.platform.capitalize()
    return '{} Python v{}'.format(platform, python[0])
#
#
def mkbauth(auth):
    auth = b64encode(auth.encode())
    auth = 'Basic {}'.format(auth.decode())
    return ('Authorization', auth)
#
#
def ip_read_list(fname):
    ips = set()
    #
    with open(fname) as fd:
        for item in fd:
            item = item.lstrip()
            item = item.rstrip()
            ips.add(item)
    #
    return list(filter(None, ips))
#
#
def ip_get_info(ip, auth=None):
    url = Parser.urljoin('https://ipinfo.io', ip)
    req = Request.Request(url)
    #
    if auth: req.add_header(*mkbauth(auth))
    req.add_header('User-Agent', mkuagent())
    req.add_header('Accept', 'application/json')
    #
    data = None
    with Request.urlopen(req) as req: data = req.read()
    return json(data)
#
#
def ip_print(data, fd=sys.stdout):
    data = list(data.items())
    data = list(map(': '.join, data))
    data = '\n'.join(data)
    print(data, '\n', sep='', file=fd)
#
#
def args_parse(args=sys.argv[1:]):
    aparse = argparse.ArgumentParser()
    aparse.add_argument('input', help='Set input file or ip.')
    aparse.add_argument('-m', dest='mode', choices=['s', 'm'], help='Set mode: s/m')
    aparse.add_argument('-t', dest='token', default='', help='Set API key: \'user:pass\'')
    aparse.add_argument('-w', dest='output', default='', help='Set output file.')
    return aparse.parse_args(args)
#
#
if __name__ == '__main__':
    try:
        args = args_parse()
        res = None
        out = sys.stdout
        #
        if args.output:
            out = open(args.output, 'w')
        #
        if args.mode == 's':
            res = ip_get_info(args.input, args.token)
            ip_print(res, out)
        #
        elif args.mode == 'm':
            ips = ip_read_list(args.input)
            #
            ips = [ip_get_info(item, args.token) for item in ips]
            for item in ips: ip_print(item, out)
        #
        else: raise argparse.ArgumentError(args.mode, 'Bad value!')
    #
    except Exception: print_exc()
    else: out.close()
