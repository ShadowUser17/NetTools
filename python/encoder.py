#!/usr/bin/env python3
from argparse import ArgumentParser
from traceback import print_exc
from urllib import parse
import base64
import quopri


class Data:
    def __init__(self, data, code):
        self._data = data
        self._code = code

    def encode(self):
        if self._code == 'qp':
            tmp = quopri.encodestring(self._data.encode())
            return tmp.decode()

        elif self._code == 'b64':
            tmp = base64.standard_b64encode(self._data.encode())
            return tmp.decode()

        elif self._code == 'url':
            return parse.quote(self._data)

    def decode(self):
        if self._code == 'qp':
            tmp = quopri.decodestring(self._data.encode())
            return tmp.decode()

        elif self._code == 'b64':
            tmp = base64.standard_b64decode(self._data.encode())
            return tmp.decode()

        elif self._code == 'url':
            return parse.unquote(self._data)


def init_args():
    args = ArgumentParser()
    args.add_argument('data', help='Set data.')

    args.add_argument('-t', '--type', dest='type', default='enc',
                      choices=['enc', 'dec'], help='Task: enc/dec')

    args.add_argument('-c', '--code', dest='code', choices=['qp', 'b64', 'url'],
                      default='url', help='Codec: qp/b64/url')

    return args.parse_args()


def main():
    try:
        args = init_args()
        data = Data(args.data, args.code)

        if args.type == 'enc':
            print(data.encode())

        else:
            print(data.decode())

    except Exception:
        print_exc()


if __name__ == '__main__':
    main()
