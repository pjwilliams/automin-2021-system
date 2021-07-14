#!/usr/bin/env python

import argparse
import json
import logging
import sys


def title_case(word):
    if len(word) == 1:
        return word[0].upper()
    return word[0].upper() + word[1:]


def postprocess(summary, participants, args):

    orig_summary = summary
    if args.trim_sentence_starts:
        summary = trim_sentence_starts(summary)
    if args.filter_attributions:
        summary = filter_attributions(summary)
    if args.add_bullets:
        summary = add_bullets(summary)
    assert len(summary.splitlines()) == len(orig_summary.splitlines())

    minutes = ''
    if args.add_participants:
        minutes += format_participant_list(participants) + '\n'
        minutes += '\n'
    minutes += summary
    return minutes


def format_participant_list(participants):

    pairs, others = [], []

    for participant in participants:
        if participant.startswith('PERSON'):
            index = int(participant[len('PERSON'):])
            pairs.append((index, participant))
        else:
            others.append(participant)

    if len(pairs) == 0:
        sorted_participants = participants
    else:
        sorted_participants = [pair[1] for pair in sorted(pairs)]
        for other in others:
            if other != 'UNKNOWN':
                sorted_participants.append(other)

    return 'Attendees: ' + ', '.join(sorted_participants)


def trim_sentence_starts(document):
    empty_words = [
        'again',
        'also',
        'and',
        'because',
        'but',
        'like',
        'ok',
        'okay',
        'or',
        'so',
        'then',
        'well',
        'yeah',
        'yes'
    ]

    def remove_empty_sentence_start(tokens):
        if len(tokens) < 2:
            return tokens
        first_word = tokens[0].lower()
        if first_word[-1] == ',':
            first_word = first_word[:-1]
        if first_word not in empty_words:
            return tokens
        out_tokens = [title_case(tokens[1])]
        if len(tokens) > 2:
            out_tokens += tokens[2:]
        return out_tokens

    out_doc = ''
    for line in document.splitlines():
        tokens = line.split()
        if tokens[0][0] == '[':
            attribution = tokens[0]
            orig_speech = tokens[1:]
        else:
            attribution = None
            orig_speech = tokens
        before_speech = orig_speech
        while True:
            after_speech = remove_empty_sentence_start(before_speech)
            if before_speech == after_speech:
                break
            before_speech = after_speech
        if attribution is not None:
            out_doc += attribution + ' '
        out_doc += ' '.join(after_speech) + '\n'
        #if orig_speech != after_speech:
            #print(' '.join(orig_speech))
            #print(' '.join(after_speech))
            #print()
    return out_doc


def filter_attributions(document):
    first_person_indicators = ["I", "I've", "I'm", "I'll", "you", "you've",
                               "your", "you're", "me", "my"]
    out_doc = ''
    for line in document.splitlines():
        tokens = line.split()
        if tokens[0][0] != '[' or \
           any(x in tokens[1:] for x in first_person_indicators):
            out_doc += line.strip() + '\n'
        else:
            out_doc += ' '.join(tokens[1:]) + '\n'
    return out_doc


def add_bullets(summary):
    out = ''
    for line in summary.splitlines():
        out += f' * {line.strip()}\n'
    return out


if __name__ == '__main__':        
    parser = argparse.ArgumentParser()
    parser.add_argument('--add-bullets', action='store_true', help='')
    parser.add_argument('--add-participants', action='store_true', help='')
    parser.add_argument('--filter-attributions', action='store_true')
    parser.add_argument('--in-section', type=str, default='summary')
    parser.add_argument('--out-section', type=str, default='minutes')
    parser.add_argument('--trim-sentence-starts', action='store_true')
    args = parser.parse_args()

    input_objs, output_objs = json.load(sys.stdin), []
    for obj in input_objs:
        if args.in_section in obj:
            summary = obj[args.in_section]
            participants = obj.get('participants', [])
            obj[args.out_section] = postprocess(summary, participants, args)
        output_objs.append(obj)
    sys.stdout.write(json.dumps(output_objs, indent=2))
