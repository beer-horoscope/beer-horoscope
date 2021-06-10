#!/bin/bash

export TRAINED_MODELS_DIR=/mnt/storage/out/
export HOST=mysql
export PORT=3306
export DATABASE=beer_horoscope
export USER=user
export PASSWORD=password
mkdir -p /mnt/storage/out
virtualenv /home/temp/venv
source /home/temp/venv/bin/activate
pip install -r /home/temp/beer-horoscope/src/training/requirements.txt
python /home/temp/beer-horoscope/src/training/main.py