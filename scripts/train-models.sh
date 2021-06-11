#!/bin/bash

# environment directories
export TRAINED_MODELS_DIR=/mnt/storage/out/
export VIRTENV_DIR=/home/temp/venv
export REPOSITORY_DIR=/home/temp/beer-horoscope

# database connection info
export HOST=mysql
export PORT=3306
export DATABASE=beer_horoscope
export USER=user
export PASSWORD=password

mkdir -p $TRAINED_MODELS_DIR
virtualenv $VIRTENV_DIR
source $VIRTENV_DIR/bin/activate
pip install -r $REPOSITORY_DIR/src/training/requirements.txt
python $REPOSITORY_DIR/src/training/main.py