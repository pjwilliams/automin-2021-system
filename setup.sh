#!/usr/bin/env bash

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cd 3rd-party
./setup.sh
cd ..
