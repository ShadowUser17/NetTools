#!/usr/bin/env python3
from argparse import ArgumentParser
from traceback import print_exc
from urllib import request
#import multiprocessing as mp


def get_args(args=None):
    parser = ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('-w', dest='wlist')
    parser.add_argument('-m', dest='method')
    return parser.parse_args(args)


def reader(fname):
    with open(fname) as fd:
        yield fd.readline()


def writer(fname, fdata):
    with open(fname, 'w') as fd:
        for item in fdata:
            fd.write(item)


def sender(req):
    client = request.urlopen(req)

