#!/bin/bash

cd vmh

source ~/miniconda3/bin/activate
conda activate memote

for model in ../../vmh/*.xml; do
memote report snapshot --solver gurobi $model;
done