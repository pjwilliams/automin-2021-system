#!/usr/bin/env python

import argparse
import json
import sys

from summarizer import Summarizer

MODEL = Summarizer()

def summarize(doc, ratio, sents_per_cluster=1, return_indices=False):
    if return_indices or sents_per_cluster > 1:

        optimal_k = MODEL.calculate_optimal_k(doc, k_max=20)
        sys.stderr.write(f'Optimal num clusters = {optimal_k}\n')

        sentences, indices = \
            MODEL(doc, ratio=ratio, max_length=250, use_first=False, return_as_list=True,
                  sents_per_cluster=sents_per_cluster)
        summary = '\n'.join(sentences)
        return summary, indices
    else:
        sentences = \
            MODEL(doc, ratio=ratio, max_length=250, use_first=False, return_as_list=True)
        summary = '\n'.join(sentences)
        return summary


if __name__ == '__main__':        
    parser = argparse.ArgumentParser()
    parser.add_argument('--in-section', type=str, default='document')
    parser.add_argument('--out-indices-section', type=str,
                        default='summaryIndices')
    parser.add_argument('--out-section', type=str, default='summary')
    parser.add_argument('--sents-per-cluster', default=1, type=int)
    parser.add_argument('--write-indices', action='store_true')
    parser.add_argument('--ratio', dest='ratio',
                    default=0.5, type=float, help='Ratio (default: 0.5)')
    args = parser.parse_args()

    input_objs, output_objs = json.load(sys.stdin), []
    for obj in input_objs:
        if args.in_section in obj:
            if args.write_indices:
                summary, indices = summarize(obj[args.in_section], args.ratio,
                                             args.sents_per_cluster,
                                             return_indices=True)
                obj[args.out_indices_section] = indices
            else:
                summary = summarize(obj[args.in_section], args.ratio)
            obj[args.out_section] = summary
        output_objs.append(obj)
    sys.stdout.write(json.dumps(output_objs, indent=2))
