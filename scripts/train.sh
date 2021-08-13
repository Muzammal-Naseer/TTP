#!/bin/bash

PROJECT_PATH="$HOME/TTP"
cd "$PROJECT_PATH" || exit

python train.py \
  --model_type resnet50 \
  --match_target 3 \
  --gs
