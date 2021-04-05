#!/usr/bin/env python3
import argparse
import traceback
import contextlib
import os


try:
    parser = argparse.ArgumentParser()
    parser.add_argument('scan_dir')
    parser.add_argument('dict_file')
    args = parser.parse_args()

    with open(args.dict_file, 'w') as fd:
        scan_dir = args.scan_dir.rstrip(os.path.sep)
        (scan_dir, scan_root) = os.path.split(scan_dir)
        os.chdir(scan_dir)

        with contextlib.redirect_stdout(fd):
            for (root, dirs, _) in os.walk(scan_root):
                for item in dirs:
                    tmp = os.path.join(root, item)
                    print(tmp.lstrip(scan_root))

except Exception:
    traceback.print_exc()
