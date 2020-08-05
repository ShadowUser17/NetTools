#!/usr/bin/env python3
import traceback
import argparse
import os
import pathlib
import socket
import multiprocessing
#
#
def _resolve(host):
    try:
        (main, doms, ips) = socket.gethostbyaddr(host)
        return (ips[0], main)
    #
    except socket.gaierror: pass
    except socket.herror: pass
#
#
def resolve_targets(targets):
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    targets = pool.map(_resolve, targets)
    return list(filter(None, targets))
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
if __name__ == '__main__':
    targets = read_input_list('./targets.txt')
    targets = resolve_targets(targets)
    for item in targets: print(item[0], item[1])
    #print(targets)
