#!/usr/bin/env python

import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('instance_id', type=str)
    parser.add_argument('transcript_file', type=str)
    parser.add_argument('reference_files', type=str, nargs='*')
    args = parser.parse_args()

    with open(args.transcript_file) as f:
        transcript = f.read()
    references = []
    for ref_file in args.reference_files:
        with open(ref_file) as f:
            references.append(f.read())

    d = {
        "instanceId": args.instance_id,
        "document":  transcript,
        "references": references
    }
    print(json.dumps([d], indent=2))


if __name__ == '__main__':
    main()
