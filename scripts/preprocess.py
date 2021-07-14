#!/usr/bin/env python

import argparse
import json
import logging
import sys


def title_case(word):
    if len(word) == 1:
        return word[0].upper()
    return word[0].upper() + word[1:]


def is_attribution(token):
    return token[0] == '[' and token[-1] == ':'


def preprocess(summary, args):
    orig_summary = summary

    if args.remove_unintelligible:
        summary = remove_unintelligible(summary, args.preserve_lines)

    if args.remove_tags:
        summary = remove_tags(summary)

    if args.remove_filler_words:
        summary = remove_filler_words(summary)

    if args.remove_incomplete_words:
        summary = remove_incomplete_words(summary)

    if args.remove_incomplete_sentences:
        summary = remove_incomplete_sentences(summary, args.preserve_lines)

    if args.fix_restarts:
        summary = fix_restarts(summary)

    if args.preserve_lines:
        assert len(summary.splitlines()) == len(orig_summary.splitlines())

    return summary


def remove_unintelligible(document, preserve_lines):
    out_doc = ''
    for line in document.splitlines():
        if 'unintelligible' not in line:
            out_doc += line.strip() + '\n'
        elif preserve_lines:
            out_doc += '\n'
    return out_doc


def fix_restarts(document):

    def normalize_tokens(tokens):

        def remove_trailing_punc(token):
            while True:
                if len(token) < 2:
                    break
                if token[-1] in [',', '.', '?', '-']:
                    token = token[:-1]
                else:
                    break
            return token

        out_tokens = []
        for token in tokens:
            out_tokens.append(remove_trailing_punc(token.lower()))
        return out_tokens

    def find_repetitions(line, n):
        tokens = line.split()
        if len(tokens) == 0:
            return []
        if is_attribution(tokens[0]):
            tokens = [tokens[0]] + normalize_tokens(tokens[1:])
        else:
            tokens = normalize_tokens(tokens)
        i = 0
        starts = []
        while i < (len(tokens) - 2*n):
            match = True
            for j in range(n):
                if tokens[i+j] != tokens[i+j+n]:
                    match = False
                    break
            if match:
                starts.append(i)
                i += 2*n
            else:
                i += 1
        return starts

    def remove_repetitions(line, n, starts):
        in_tokens, out_tokens = line.split(), []
        i = 0
        while i < len(in_tokens):
            if i in starts:
                for j in range(n):
                    out_tokens.append(in_tokens[i+j+n])
                if i == 0 or i == 1:
                    out_tokens[i] = title_case(out_tokens[i])
                i += 2*n
            else:
                out_tokens.append(in_tokens[i])
                i += 1
        return ' '.join(out_tokens)

    out_doc = ''
    for line in document.splitlines():
        line = line.strip()
        for n in [3, 2, 1]:
            while True:
                before_line = line
                starts = find_repetitions(line, n)
                line = remove_repetitions(line, n, starts)
                if before_line == line:
                    break
        out_doc += line + '\n'
    return out_doc


def remove_tags(document):
    out_doc = ''
    for line in document.splitlines():
        out_tokens = []
        for token in line.split():
            if len(token) > 2 and token[0] == '<' and token[-1] == '>':
                continue
            out_tokens.append(token)
        out_line = ' '.join(out_tokens)
        out_doc += out_line + '\n'
    return out_doc


def remove_filler_words(document):
    def make_pass(document):
        out_doc = ''
        for line in document.splitlines():
            for filler in ['um', 'uhm', 'uh', 'eh', 'ehm', 'er']:
                line = line.replace(f'{title_case(filler)}, ', '')
                line = line.replace(f'{title_case(filler)} ', '')
                line = line.replace(f' {filler} ', ' ')
                line = line.replace(f', {filler} ', ' ')
                line = line.replace(f', {filler}, ', ' ')
                line = line.replace(f' {filler}, ', ' ')
            out_doc += line.strip() + '\n'
        return out_doc
    old_doc = document
    new_doc = make_pass(old_doc)
    while new_doc != old_doc:
        old_doc = new_doc
        new_doc = make_pass(old_doc)
    return new_doc


def remove_incomplete_words(document):
    out_doc = ''
    for line in document.splitlines():
        out_tokens = []
        for token in line.split():
            if len(token) < 2 or token[-1] != '-':
                out_tokens.append(token)
        out_line = ' '.join(out_tokens)
        out_doc += out_line + '\n'
    return out_doc


def remove_incomplete_sentences(document, preserve_lines):
    out_doc = ''
    for line in document.splitlines():
        line = line.strip()
        is_complete = len(line) > 0 and (line[-1] == '.' or line[-1] == '?')
        if is_complete:
            out_doc += line + '\n'
        elif preserve_lines:
            out_doc += '\n'
    return out_doc


if __name__ == '__main__':        
    parser = argparse.ArgumentParser()
    parser.add_argument('--fix-restarts', action='store_true')
    parser.add_argument('--in-section', type=str, default='document')
    parser.add_argument('--out-section', type=str, default='document')
    parser.add_argument('--preserve-lines', action='store_true')
    parser.add_argument('--remove-filler-words', action='store_true')
    parser.add_argument('--remove-incomplete-sentences', action='store_true')
    parser.add_argument('--remove-incomplete-words', action='store_true')
    parser.add_argument('--remove-tags', action='store_true')
    parser.add_argument('--remove-unintelligible', action='store_true')
    args = parser.parse_args()

    input_objs, output_objs = json.load(sys.stdin), []
    for obj in input_objs:
        if args.in_section in obj:
            obj[args.out_section] = preprocess(obj[args.in_section], args)
        output_objs.append(obj)
    sys.stdout.write(json.dumps(output_objs, indent=2))
