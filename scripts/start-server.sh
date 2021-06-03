#!/bin/bash

export FLASK_APP=/home/payday/projects/chicago-red-hat-summit-ai-ml/src/rest_api/main.py
export TRAINED_MODELS_DIR=/mnt/sdb1/out/
export HOST=localhost
export PORT=3306
export DATABASE=beer_horoscope
export USER=user
export PASSWORD=password
source /home/payday/pyenv/001/bin/activate
flask run --host=0.0.0.0