#!/usr/bin/env bash

project_root_dir=..

export PYTHONPATH=$(realpath $project_root_dir)/3rd-party/bert-extractive-summarizer/:$PYTHONPATH

rm -rf tmp outputs
mkdir tmp outputs

for split in test; do

    $project_root_dir/scripts/record-participants.py \
        < $project_root_dir/data/$split.json \
        > tmp/$split-participants.json

    $project_root_dir/scripts/preprocess.py \
        --in-section document \
        --out-section document \
        --fix-restarts \
        --preserve-lines \
        --remove-filler-words \
        --remove-incomplete-sentences \
        --remove-incomplete-words \
        --remove-tags \
        --remove-unintelligible \
        < tmp/$split-participants.json \
        > tmp/$split-preprocessed.json

    for ratio in 0.035; do

        CUDA_VISIBLE_DEVICES=0 $project_root_dir/scripts/summarize-e-bert.py \
            --in-section document \
            --out-indices-section summaryIndices \
            --out-section summary \
            --ratio $ratio \
            --sents-per-cluster 5 \
            --write-indices \
            < tmp/$split-preprocessed.json \
            > tmp/$split-contrastive-b-raw-$ratio.json

        $project_root_dir/scripts/classify.py \
            --ratio 0.2 \
            < tmp/$split-contrastive-b-raw-$ratio.json \
            > tmp/$split-contrastive-b-filtered-$ratio.json \

        $project_root_dir/scripts/postprocess.py \
            --add-bullets \
            --add-participants \
            --filter-attributions \
            --trim-sentence-starts \
            < tmp/$split-contrastive-b-filtered-$ratio.json \
            > outputs/$split-contrastive-b-$ratio.json

        mkdir -p outputs/$ratio
        $project_root_dir/scripts/dump-minutes.py \
            --write-files \
            --output-dir outputs/$ratio \
            < outputs/$split-contrastive-b-$ratio.json
    done
done
