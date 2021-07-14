#!/usr/bin/env python

import argparse
import json
import os
import sys


def write_files(objs, output_dir):
    for obj in objs:
        instance_id = obj['instanceId']
        path = os.path.join(output_dir, instance_id + '.txt')
        with open(path, 'w') as f:
            f.write(obj['minutes'])


def write_digest(objs):
    for obj in objs:
        print('-'*80)
        print(obj['instanceId'])
        print('-'*80)
        #print(obj['minutes'])
        minutes = obj['minutes']
        for line in minutes.splitlines():
            line = line.strip()
            print(len(line), line)
        print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-files', action='store_true')
    parser.add_argument('--output-dir', type=str)
    args = parser.parse_args()

    objs = json.load(sys.stdin)

    if args.write_files:
        output_dir = '.' if args.output_dir is None else args.output_dir
        write_files(objs, output_dir)
    else:
        write_digest(objs)


if __name__ == '__main__':
    main()
