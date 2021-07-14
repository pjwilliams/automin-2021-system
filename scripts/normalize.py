#!/usr/bin/env python

import argparse
import json
import re
import sys

def normalize(summary, args):
    if args.utterance_policy == 'merge-sentences':
        summary = merge_sentences(summary)
    else:
        assert args.utterance_policy == 'copy-attribution'
        summary = copy_attribution(summary)
    return summary


PERSON_REGEX = re.compile('^[\[\(]PERSON(\d+)[\]\)](.*)')

def copy_attribution(document):
    out_doc = ''
    current_person = None
    for i, line in enumerate(document.splitlines()):
        in_line = line.strip()
        if in_line == '':
            continue
        pobj = PERSON_REGEX.match(in_line)
        if pobj is not None:
            current_person = f'[PERSON{pobj.group(1)}]'
            in_line = pobj.group(2).strip()
        if current_person is None:
            out_doc += '[UNKNOWN]: ' + in_line + '\n'
        else:
            out_doc += current_person + ': ' + in_line + '\n'

    return out_doc


def merge_sentences(document):
    out_doc = ''
    out_line = ''
    for i, line in enumerate(document.splitlines()):
        in_line = line.strip()
        if in_line.startswith('[PERSON') or in_line.startswith('(PERSON'):
            if out_line != '':
                out_doc += out_line + '\n'
            out_line = in_line
        else:
            out_line += ' ' + in_line
    if out_line != '':
        out_doc += out_line + '\n'

    return out_doc


if __name__ == '__main__':        
    parser = argparse.ArgumentParser()
    parser.add_argument('--in-section', type=str, default='document')
    parser.add_argument('--out-section', type=str, default='document')
    parser.add_argument('--utterance-policy', type=str,
                        choices=['merge-sentences', 'copy-attribution'],
                        default='copy-attribution')
    args = parser.parse_args()

    input_objs, output_objs = json.load(sys.stdin), []
    for obj in input_objs:
        if args.in_section in obj:
            obj[args.out_section] = normalize(obj[args.in_section], args)
        output_objs.append(obj)
    sys.stdout.write(json.dumps(output_objs, indent=2))
