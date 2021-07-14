#!/usr/bin/env python

import argparse
import json
import sys

def main():
    objs = json.load(sys.stdin)
    for obj in objs:
        for i, reference in enumerate(obj['references']):
            print('-'*80)
            print(f'{obj["instanceId"]} - reference {i+1}')
            print('-'*80)
            print(reference)
            print()


if __name__ == '__main__':
    main()
