#!/usr/bin/env python

import argparse
import json
import sys

def main():
    d_list = []
    for transcript_file in sys.argv[1:]:
        with open(transcript_file) as f:
            d = json.load(f)
            d_list.extend(d)
    print(json.dumps(d_list, indent=2))


if __name__ == '__main__':
    main()
