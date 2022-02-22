#!/usr/bin/env python3
from urllib import request
from datetime import datetime
from urllib.error import HTTPError

import ssl
import sys
import re

import traceback
import argparse
import typing


def get_args(args: list = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', dest='target_file', default='targets.txt', help='Set target list (targets.txt)')
    parser.add_argument('-i', dest='ssl_verify', default=True, help='Disable SSL verification.', action='store_false')
    parser.add_argument('-t', dest='req_timeout', default=60, help='Set request timeout.', type=float)
    parser.add_argument('-o', dest='log_file', default='results.txt', help='Redirect output to file.')
    parser.add_argument('-r', dest='body_regex', default='.*', help='Set body regex.')
    return parser.parse_args(args)


def get_reader(filename: str) -> typing.Generator:
    with open(filename) as fd:
        for line in fd:
            line = line.rstrip()

            if line and (not line.startswith('#')):
                yield line


def res_printer(results: typing.Generator, logfile: str) -> None:
    with open(logfile, 'w') as logfile:
        for item in results:
            print(item, file=logfile, flush=True)


def get_context(verify: bool = True) -> ssl.SSLContext:
    if not verify:
        return ssl._create_unverified_context()

    return ssl.create_default_context()


def get_regex_status(regex: re.Pattern, body: bytes) -> str:
    if bool(regex.match(body.decode())):
        return 'Match'

    return 'Mismatch'


def url_checker(targets: typing.Generator, regex: re.Pattern, timeout: float, verify: bool) -> typing.Generator:
    context = get_context(verify)

    for url in targets:
        dt_start = datetime.now()

        try:
            with request.urlopen(url=url, timeout=timeout, context=context) as req:
                body = get_regex_status(regex, req.read())

                dt_stop = datetime.now() - dt_start
                yield '{} {} {}: {}'.format(dt_stop, req.code, body, req.url)

        except HTTPError as error:
            dt_stop = datetime.now() - dt_start
            yield '{} {} {}: {}'.format(dt_stop, error.code, error.msg, error.url)

        except OSError:
            dt_stop = datetime.now() - dt_start
            print('Timeout after {}: {}'.format(dt_stop, url), file=sys.stderr)


def main(args=None) -> None:
    try:
        args = get_args(args)
        regex = re.compile(args.body_regex)

        reader = get_reader(args.target_file)
        output = url_checker(reader, regex, args.req_timeout, args.ssl_verify)
        res_printer(output, args.log_file)

    except KeyboardInterrupt:
        print('Interrupted...', file=sys.stderr)

    except Exception:
        traceback.print_exc()


if __name__ == '__main__':
    main()
