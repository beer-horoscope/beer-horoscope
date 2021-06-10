#!/bin/bash

export FLASK_APP=/home/temp/beer-horoscope/src/rest_api/main.py
export TRAINED_MODELS_DIR=/mnt/storage/out/
export HOST=mysql
export PORT=3306
export DATABASE=beer_horoscope
export USER=user
export PASSWORD=password
mkdir -p /mnt/storage/out
source /home/temp/venv/bin/activate
pip install -r /home/temp/beer-horoscope/src/rest_api/requirements.txt
flask run --host=0.0.0.0