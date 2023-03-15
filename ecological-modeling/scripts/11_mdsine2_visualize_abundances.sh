#!/bin/bash

#SBATCH --job-name=11_mdsine2_visualize_abundances
#SBATCH -p medium
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16000
#SBATCH --time=5-00:00:00
#SBATCH --mail-user=a.castellanoss@uniandes.edu.co
#SBATCH --mail-type=ALL
#SBATCH --array=1-30%10
#SBATCH -o logs/11_mdsine2_visualize_abundances.o%j

source ~/anaconda3/bin/activate
conda activate mdsine2

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference

set $(sed -n ${SLURM_ARRAY_TASK_ID}p /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/11_mdsine2_visualize_abundances_lookupfile.txt)
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