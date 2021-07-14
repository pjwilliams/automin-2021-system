#!/usr/bin/env python

import argparse
import json
import sys

def main():
    objs = json.load(sys.stdin)
    for obj in objs:
        print('-'*80)
        print(obj['instanceId'])
        print('-'*80)
        print(obj['document'])
        print()


if __name__ == '__main__':
    main()
