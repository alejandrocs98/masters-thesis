#!/bin/bash

#SBATCH --job-name=11_mdsine2_visualize_posteriors_noD
#SBATCH -p short
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32000
#SBATCH --time=12:00:00
#SBATCH --mail-user=a.castellanoss@uniandes.edu.co
#SBATCH --mail-type=ALL
#SBATCH --array=1-6%6
#SBATCH -o logs/11_mdsine2_visualize_posteriors_noD.o%j

source ~/anaconda3/bin/activate
conda activate mdsine2

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference

set $(sed -n ${SLURM_ARRAY_TASK_ID}p /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/11_mdsine2_visualize_posteriors_lookupfile.txt)
simtype=$1
dataset=$2

# Visualize abundances
python3 /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/visualize_posteriors.py \
$simtype \
$dataset

# for simtype in no-module-learning cluster-learning fixed-clusters; do
#     for dataset in LF0 HF0; do
#         python3 /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/plot_forward_sims.py \
#         $simtype \
#         $dataset;
#     done;
# done