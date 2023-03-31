#!/bin/bash

#SBATCH --job-name=14_mdsine2_get_bayes_factors_scores
#SBATCH -p short
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8000
#SBATCH --time=12:00:00
#SBATCH --mail-user=a.castellanoss@uniandes.edu.co
#SBATCH --mail-type=ALL
##SBATCH --array=1-6%6
#SBATCH -o logs/14_mdsine2_get_bayes_factors_scores.o%j

source ~/anaconda3/bin/activate
conda activate mdsine2

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data

# set $(sed -n ${SLURM_ARRAY_TASK_ID}p /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/14_mdsine2_get_bayes_factors_scores_lookupfile.txt)
# simtype=$1
# dataset=$2

# python3 /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/get_bayes_factors_scores.py \
# $simtype \
# $dataset 

simtype=no-module-learning

# for simtype in no-module-learning cluster-learning fixed-clusters; do
for dataset in LF0 HF0; do
    python3 /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/get_bayes_factors_scores.py \
    $simtype \
    $dataset
done;
# done