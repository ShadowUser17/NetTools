#!/usr/bin/env python3
import argparse
import traceback
import threading

from urllib import parse as urlparse
from urllib import request


def get_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('-w', dest='wordlist', help='Set wordlist')
    parser.add_argument('-m', dest='method', help='Set method')
    parser.add_argument('-d', dest='data', help='Set data')
    parser.add_argument('-p', dest='proxy', help='Set proxy')
    return parser.parse_args(args)


def reader(fname: str):
    with open(fname) as fd:
        line = fd.readline()
        yield line.rstrip()


def writer(fname: str, fdata: list):
    with open(fname, 'w') as fd:
        for item in fdata:
            fd.write(item)


def sender(sem: threading.Semaphore, req: request.Request, res: list):
    try:
        sem.acquire()
        client = request.urlopen(req)
        client.close()

        server = client.getheader('server')
        host = client.geturl()
        code = client.getcode()
        res.append((host, server, code))

    except Exception:
        traceback.print_exc()

    finally:
        sem.release()


def worker(method: str, url: str, data: str, item_iter: list):
    sem = threading.Semaphore(10)
    tlist = list()
    rlist = list()

    for item in item_iter:
        item = urlparse.urljoin(url, item)
        req = request.Request(item, data=data, method=method)

        thr = threading.Thread(
            target=sender,
            args=(sem, req, rlist)
        )

        thr.start()
        tlist.append(thr)

    for item in tlist:
        item.join()

    return rlist
