#!/usr/bin/env python3
import ctypes
import socket
import fcntl
import binascii
import random
import argparse
import traceback


IFF_UP = 0x0001
SIOCGIFFLAGS = 0x8913
SIOCSIFFLAGS = 0x8914

IFF_LOOPBACK = 0x0008
IFF_POINTTOPOINT = 0x0010

SIOCGIFHWADDR = 0x8927
SIOCSIFHWADDR = 0x8924

digits = '0123456789ABCDEF'


class _sockaddr(ctypes.Structure):
    _fields_ = [
        ('sa_family', ctypes.c_ushort),
        ('sa_data', ctypes.c_char * 14)
    ]


class _ifunion(ctypes.Union):
    _anonymous_ = ('_sa',)
    _fields_ = [
        ('ifr_flags', ctypes.c_short),
        ('_sa', _sockaddr)
    ]


class ifreq(ctypes.Structure):
    _anonymous_ = ('_un',)
    _fields_ = [
        ('ifr_name', ctypes.c_char * 16),
        ('_un', _ifunion)
    ]


class MAC:
    def __init__(self, ifname):
        self._ifname = ifname
        self._socket = None

        ifname = ifname.encode()
        self._if_flags = ifreq()
        self._if_flags.ifr_name = ifname

        self._if_hwaddr = ifreq()
        self._if_hwaddr.ifr_name = ifname

        self._socket = socket.socket(
            socket.AF_PACKET,
            socket.SOCK_RAW,
            socket.ntohs(0x3)
        )

        self._socket.bind((self._ifname, 0))
        fcntl.ioctl(self._socket.fileno(), SIOCGIFFLAGS, self._if_flags)


    def __del__(self):
        if self._socket:
            self._socket.close()


    def if_isup(self):
        if bool(self._if_flags.ifr_flags & IFF_UP):
            return 'Up'

        else:
            return 'Down'


    def if_up(self):
        self._if_flags.ifr_flags |= IFF_UP
        fcntl.ioctl(self._socket.fileno(), SIOCSIFFLAGS, self._if_flags)


    def if_down(self):
        self._if_flags.ifr_flags ^= IFF_UP
        fcntl.ioctl(self._socket.fileno(), SIOCSIFFLAGS, self._if_flags)


    def if_check(self):
        if (self._if_flags.ifr_flags & IFF_LOOPBACK):
            return False

        if (self._if_flags.ifr_flags & IFF_POINTTOPOINT):
            return False

        return True


    def hwaddr_get(self):
        fcntl.ioctl(self._socket.fileno(), SIOCGIFHWADDR, self._if_hwaddr)

        MAC = self._if_hwaddr.sa_data
        MAC = binascii.hexlify(MAC)
        MAC = MAC.decode()
        MAC = MAC.upper()

        return '{}:{}:{}:{}:{}:{}'.format(
            MAC[:2], MAC[2:4],
            MAC[4:6], MAC[6:8],
            MAC[8:10], MAC[10:12]
        )


    def hwaddr_rnd(self):
        MAC = '02{}{}{}{}{}{}{}{}{}{}'.format(
            random.choice(digits),
            random.choice(digits),
            random.choice(digits),
            random.choice(digits),
            random.choice(digits),
            random.choice(digits),
            random.choice(digits),
            random.choice(digits),
            random.choice(digits),
            random.choice(digits)
        )

        self._if_hwaddr.sa_data = binascii.unhexlify(MAC)
        self.if_down()
        fcntl.ioctl(self._socket.fileno(), SIOCSIFHWADDR, self._if_hwaddr)
        self.if_up()

        return '{}:{}:{}:{}:{}:{}'.format(
            MAC[:2], MAC[2:4],
            MAC[4:6], MAC[6:8],
            MAC[8:10], MAC[10:12]
        )


try:
    args = argparse.ArgumentParser()
    args.add_argument('iface')
    args = args.parse_args()

    mac = MAC(args.iface)
    print('Interface {} is {}'.format(args.iface, mac.if_isup()))

    if mac.if_check():
        print('OLD: {}'.format(mac.hwaddr_get()))
        print('NEW: {}'.format(mac.hwaddr_rnd()))

    else:
        raise TypeError('Interface loop or p-to-p')

except Exception:
    traceback.print_exc()
