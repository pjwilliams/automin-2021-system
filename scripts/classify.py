#!/usr/bin/env python

import argparse
import json
import sys

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn import metrics

def summarize(doc, ratio):
    lines = doc.splitlines()
    sents = [' '.join(line.split()[1:]) for line in lines]
    df = pd.DataFrame({
            "line": lines,
            "sentence": sents
        }
    )
    pipeline = joblib.load('model.joblib')
    y_prob = pipeline.predict_proba(df.sentence)
    pairs = [(float(prob[0]), i) for (i, prob) in enumerate(y_prob)]
    target_num = int(len(sents) * ratio)
    summary = ''
    indices = []
    for i, pair in enumerate(sorted(pairs)):
        if i == target_num:
            break
        indices.append(pair[1])
    for i in sorted(indices):
        summary += lines[i] + '\n'
    return summary


if __name__ == '__main__':        
    parser = argparse.ArgumentParser()
    parser.add_argument('--in-section', type=str, default='summary')
    parser.add_argument('--out-section', type=str, default='summary')
    parser.add_argument('--ratio', type=float, default=0.2)
    args = parser.parse_args()

    input_objs, output_objs = json.load(sys.stdin), []
    for obj in input_objs:
        if args.in_section in obj:
            obj[args.out_section] = summarize(obj[args.in_section], args.ratio)
        output_objs.append(obj)
    sys.stdout.write(json.dumps(output_objs, indent=2))
