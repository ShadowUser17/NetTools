#!/usr/bin/env python3
from argparse import ArgumentParser
from re import compile as mkregex
from traceback import print_exc
from collections import OrderedDict
#from json import dumps as js_dump
from pathlib import Path
#
#
class NmapParser:
    def __init__(self):
        self.regex_ip = mkregex('\s(\d+\.\d+\.\d+\.\d+)\n')
        self.regex_port = mkregex('\n(\d+)/(\w+)\s')
        #
        self._raw = None
        self.items = OrderedDict()
    #
    def _parse(self):
        self._raw = self._raw.split('\n\n')
        #
        for item in iter(self._raw):
            ip = self.regex_ip.findall(item)
            #
            if ip:
                ports = self.regex_port.findall(item)
                self.items[ip[0]] = ports
        #
        self._raw = None
    #
    @classmethod
    def port_to_string(self, ports):
        tmp = map(lambda item: item[0], ports)
        return ','.join(tmp)
    #
    def load_from_file(self, fname):
        file = Path(fname)
        self._raw = file.read_text()
        self._parse()
    #
    def load_from_string(self, data):
        self._raw = data
        self._parse()
#
#
def init_args(args=None):
    parser = ArgumentParser()
    parser.add_argument('file', help='Set Nmap output file (Normal).')
    #parser.add_argument('-j', dest='json', action='store_true', help='Set Json output.')
    return parser.parse_args(args)
#
#
def main(args):
    nmap = NmapParser()
    nmap.load_from_file(args.file)
    #
    for key in nmap.items.keys():
        print('{}:{}'.format(key, nmap.port_to_string(nmap.items[key])))
#
#
if __name__ == '__main__':
    try: main(init_args())
    except Exception: print_exc()
