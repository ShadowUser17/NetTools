#!/usr/bin/env python3
from argparse import ArgumentParser
from traceback import print_exc
from urllib import request
from sys import version
#
#
try:
    args = ArgumentParser()
    args.add_argument('url', help='Set short url.')
    args.add_argument('-r', dest='redirect', default=10, type=int, help='Set max redirects.')
    args.add_argument('-p', dest='proxy', help='Set http proxy.')
    args = args.parse_args()
    #
    handle_redirect = request.HTTPRedirectHandler()
    handle_redirect.max_redirections = args.redirect
    #
    handle_cookie = request.HTTPCookieProcessor()
    request.install_opener(request.build_opener(handle_redirect, handle_cookie))
    #
    req = request.Request(args.url, method='HEAD')
    version = version.split()
    req.add_header('User-Agent', 'Python v{}'.format(version))
    #
    if args.proxy:
        proxy = request.urlparse(args.proxy)
        req.set_proxy('{}:{}'.format(proxy.hostname, proxy.port), proxy.scheme)
    #
    with request.urlopen(req) as req:
        print('Location: {}'.format(req.url))
        print('Code: {}'.format(req.code))
        print('Server: {}'.format(req.headers.get('Server')))
        print('Content-Type: {}'.format(req.headers.get('Content-Type')))
        print('Set-Cookie: {}'.format(req.headers.get('Set-Cookie')))
    #
except Exception: print_exc()

