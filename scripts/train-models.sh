#!/bin/bash

export TRAINED_MODELS_DIR=/mnt/sdb1/out/
export HOST=localhost
export PORT=3306
export DATABASE=beer_horoscope
export USER=user
export PASSWORD=password
source /home/payday/pyenv/001/bin/activate
python /home/payday/projects/chicago-red-hat-summit-ai-ml/src/training/main.py