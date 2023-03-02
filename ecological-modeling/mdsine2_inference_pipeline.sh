#!/bin/bash

source ~/anaconda3/bin/activate
conda activate mdsine2

for dataset in LF0 HF0; do
	for seed in 0 4 27; do
		python mdsine2_inference_pipeline.py $dataset $seed > $(echo $dataset)_seed$seed.log 2>&1;
	done;
done;