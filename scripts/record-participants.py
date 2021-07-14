#!/usr/bin/env python

import argparse
import json
import logging
import sys


def is_attribution(token):
    return token[0] == '[' and token[-1] == ':'


def list_participants(document):
    participants = set()
    for line in document.splitlines():
        tokens = line.split()
        assert(is_attribution(tokens[0]))
        participant = tokens[0][1:-2]
        participants.add(participant)
    return list(sorted(participants))


if __name__ == '__main__':        
    parser = argparse.ArgumentParser()
    parser.add_argument('--in-section', type=str, default='document')
    parser.add_argument('--out-section', type=str, default='participants')
    args = parser.parse_args()

    input_objs, output_objs = json.load(sys.stdin), []
    for obj in input_objs:
        if args.in_section in obj:
            obj[args.out_section] = list_participants(obj[args.in_section])
        output_objs.append(obj)
    sys.stdout.write(json.dumps(output_objs, indent=2))
