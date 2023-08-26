#!/usr/bin/env python3
import sys
import pathlib
import argparse
import traceback


try:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Set file path.")
    args = parser.parse_args()

    file = pathlib.Path(args.path)
    data = bytearray(file.read_bytes())

    tmp = []
    for (pos, item) in enumerate(data):
        if pos % 30 == 1:
            print("\"{}\"".format("".join(tmp)))
            tmp = []

        else:
            tmp.append("\\x{:02x}".format(item))

except Exception:
    traceback.print_exc()
    sys.exit(1)
