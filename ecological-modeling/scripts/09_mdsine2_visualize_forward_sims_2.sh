#!/bin/bash

#SBATCH --job-name=09_mdsine2_visualize_forward_sims_noD_2
#SBATCH -p short
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32000
#SBATCH --time=12:00:00
#SBATCH --mail-user=a.castellanoss@uniandes.edu.co
#SBATCH --mail-type=ALL
#SBATCH --array=1-6%6
#SBATCH -o logs/09_mdsine2_visualize_forward_sims_noD_2.o%j

source ~/anaconda3/bin/activate
conda activate mdsine2

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference

set $(sed -n ${SLURM_ARRAY_TASK_ID}p /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/09_mdsine2_visualize_forward_sims_lookupfile_2.txt)
simtype=$1
dataset=$2
seed=$3

# Visualize abundances
python3 /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/plot_forward_sims.py \
$simtype \
$dataset \
$seed

# for simtype in no-module-learning cluster-learning fixed-clusters; do
#     for dataset in LF0 HF0; do
#         for seed in 0 3 4 23 127; do
#             python3 /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/plot_forward_sims.py \
#             $simtype \
#             $dataset \
#             $seed;
#         done;
#     done;
# done