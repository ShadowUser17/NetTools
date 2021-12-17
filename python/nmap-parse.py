#!/usr/bin/env python3
import argparse
import traceback
import types
import os
import re
import sys
import collections


class NmapParser:
    def __init__(self):
        self.regex_begin = re.compile(r'Nmap scan*')
        self.regex_port = re.compile(r'\d+\/*')
        self.regex_end = re.compile(r'\n')
        self.items = collections.OrderedDict()

    def _parse(self, file: types.GeneratorType):
        for line in file:
            line = line.rstrip()

            if self.regex_begin.match(line):
                line = line.split()

                ip = line[-1]
                ip = ip.lstrip('(')
                ip = ip.rstrip(')')
                ports = list()

                for line in file:
                    if self.regex_port.match(line):
                        line = line.rstrip()
                        line = line.split()
                        line = line[0]
                        line = line.split('/')
                        ports.append(line[0])
                        continue

                    if self.regex_end.match(line):
                        break

                if ports:
                    ports = ','.join(ports)
                    self.items[ip] = ports

    def load_from_file(self, file_name: str):
        with open(file_name) as file:
            self._parse(file)

    def load_from_stdin(self):
        self._parse(sys.stdin)

    def save_to_file(self, file_name: str):
        template = '-p {plist} {host}\n'

        with open(file_name, 'w') as file:
            for key in self.items:
                line = template.format(host=key, plist=self.items[key])
                file.write(line)

    def show_to_stdout(self):
        template = '-p {plist} {host}\n'

        for key in self.items:
            print(template.format(host=key, plist=self.items[key]), end='')


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', dest='sfile', default='', help='Set Nmap output file (-oN)')
    parser.add_argument('-d', dest='dfile', default='', help='Set output file')
    return parser.parse_args(args)

if __name__ == "__main__":
    try:
        args = parse_args()
        nmap = NmapParser()

        if os.path.exists(args.sfile):
            nmap.load_from_file(args.sfile)

        else:
            nmap.load_from_stdin()

        if args.dfile == '':
            nmap.show_to_stdout()

        else:
            nmap.save_to_file(args.dfile)

    except Exception:
        traceback.print_exc()
