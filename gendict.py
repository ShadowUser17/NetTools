#!/usr/bin/env python3
import argparse
import traceback
import contextlib
import os


try:
    parser = argparse.ArgumentParser()
    parser.add_argument('scan_dir')
    parser.add_argument('dict_file')
    parser.add_argument('-f', dest='files', help='Include files.', action='store_true')
    args = parser.parse_args()

    with open(args.dict_file, 'w') as fd:
        scan_dir = args.scan_dir.rstrip(os.path.sep)
        (scan_dir, scan_root) = os.path.split(scan_dir)
        os.chdir(scan_dir)

        with contextlib.redirect_stdout(fd):
            for (root, dirs, files) in os.walk(scan_root):
                for dir_item in dirs:
                    tmp = os.path.join(root, dir_item)
                    print(tmp.lstrip(scan_root))

                    if args.files:
                        for file_item in files:
                            tmp = os.path.join(root, dir_item, file_item)
                            print(tmp.lstrip(scan_root))

except Exception:
    traceback.print_exc()
