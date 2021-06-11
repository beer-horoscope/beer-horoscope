#!/bin/bash

# environment directories
export TRAINED_MODELS_DIR=<trained_models_directory> # i.e. /mnt/storage/out/
export VIRTENV_DIR=<virtual_python_environment_directory> # i.e. /home/temp/venv
export REPOSITORY_DIR=<path_this_source_repository> # i.e. /home/temp/beer-horoscope

# database connection info
export HOST=localhost
export PORT=3306
export DATABASE=beer_horoscope
export USER=root
export PASSWORD=<root_password> # i.e. password

mkdir -p $TRAINED_MODELS_DIR
virtualenv $VIRTENV_DIR
source $VIRTENV_DIR/bin/activate
pip install -r $REPOSITORY_DIR/src/training/requirements.txt
python $REPOSITORY_DIR/src/training/main.py