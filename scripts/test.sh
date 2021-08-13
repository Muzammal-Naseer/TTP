#!/bin/bash

PROJECT_PATH="$HOME/TTP"
cd "$PROJECT_PATH" || exit

python eval_sub.py \
  --source_model resnet50 \
  --target_model resnet50 \
  --NRP \
  --batch_size 1