#!/usr/bin/env bash

for d in ../3rd-party/automin-2021-confidential-data/task-A-elitr-minuting-corpus-en/test*/*; do
    filename=$(basename $d)
    ./wrap.py $filename $d/transcript_* > test_$filename.json
done
./combine-transcripts.py test_*.json | ../scripts/normalize.py > test.json
