# AutoMin 2021 System

UEDIN's minuting system for the AutoMin 2021 shared task.

The minuter is a pipeline that applies the following steps to each transcript:

 1. **Normalization** of speaker attributions. This ensures that each utterance begins with a speaker attribution and that the same format is used throughout, e.g. `[PERSON5]` and not `(PERSON5)`.
 1. **Preprocessing**. This rule-based step cleans up the input text by removing speech and transcription artefacts, such as filler words (`er`, `um`, etc), restarts (`we sh-, we should`), and tags (such as `<laughing>`).
 1. **Extractive summarization** using a [modified version](https://github.com/pjwilliams/bert-extractive-summarizer) of the [bert-extractive-summarizer](https://github.com/dmmiller612/bert-extractive-summarizer) lecture summarizer that is altered to recognise utterance boundaries and to over-generate by producing five utterances (instead of one) for every cluster.
 1. **Filtering** by using a binary logistic regression model to assign a probability to each utterance and then taking the top fifth of utterances. The model was learned from a manually labelled subset of the training data where the label of an utterance indicates (a subjective human judgement on) whether or not it is suitable to appear in the minutes.
 1. **Postprocessing**. This final rule-based step produces the minutes by adding a list of partcipants and cleaning up the summary by, for example, trimming conjunctions from the starts of utterances.

## Setup

1. Ensure that you have Python 3.8 or later. If your version of Python is older then a local (i.e. directory-level) installation using pyenv is recommended. For example:

   ```
   $ pyenv install 3.9.6
   $ pyenv local 3.9.6
   ```

1. Run the top-level `./setup.sh` script. This will:
  * Create a Python virtual environment and install the required packages.
  * Clone the required third-party Git repositories (`automin-2021-confidential-data` and `bert-extractive-summarizer`).

## Instructions

1. Activate the Python virtual environment:

   ```
   $ source venv/bin/activate
   ```

1. Normalize the test transcripts and wrap them in the JSON format expected by the minuter:

   ```
   $ cd data
   $ ./wrap-test.sh
   ```

   The transcripts will be added to the `document` sections of the `data/test.json`.

1. Run the minuting script. This reads `data/test.json` as input and writes output files to the `minuter/outputs` directory. By default, it uses GPU 0 for the extractive summarization step. You can change this by editing the ```CUDA_VISIBLE_DEVICES=0``` statement (delete the device number to use CPU instead).

   ```
   $ cd minuter
   $ ./minute.sh
   ```
   The length of the minutes can be controlled with the ratio variable.
