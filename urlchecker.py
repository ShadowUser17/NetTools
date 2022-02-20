#!/usr/bin/env python3
from urllib import request
from urllib.error import HTTPError

import ssl
import sys

import traceback
import argparse
import typing


def get_args(args: list = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', dest='target_file', default='targets.txt', help='Set target list (targets.txt)')
    parser.add_argument('-t', dest='req_timeout', default=60, help='Set request timeout.', type=float)
    parser.add_argument('-i', dest='ssl_verify', default=True, help='Disable SSL verification.', action='store_false')
    return parser.parse_args(args)


def get_reader(filename: str) -> typing.Generator:
    with open(filename) as fd:
        for line in fd:
            line = line.rstrip()

            if line and (not line.startswith('#')):
                yield line


def res_printer(results: typing.Generator, output=sys.stdout) -> None:
    for item in results:
        print(item, file=output)


def get_context(verify: bool = True) -> ssl.SSLContext:
    if not verify:
        return ssl._create_unverified_context()

    return ssl.create_default_context()


def url_checker(targets: typing.Generator, timeout: float, verify: bool) -> typing.Generator:
    context = get_context(verify)

    for url in targets:
        try:
            with request.urlopen(url=url, timeout=timeout, context=context) as req:
                yield '{} {}: {}'.format(req.code, req.msg, req.url)

        except HTTPError as error:
            yield '{} {}: {}'.format(error.code, error.msg, error.url)

        except OSError:
            print('Timeout:', url, file=sys.stderr)


def main(args=None) -> None:
    try:
        args = get_args(args)
        reader = get_reader(args.target_file)
        res_printer(url_checker(reader, args.req_timeout, args.ssl_verify))

    except KeyboardInterrupt:
        print('Interrupted...', file=sys.stderr)

    except Exception:
        traceback.print_exc()


if __name__ == '__main__':
    main()
