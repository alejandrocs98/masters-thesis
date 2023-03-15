#!/bin/bash

#SBATCH --job-name=08_mdsine2_visualize_nodes_coeffs
#SBATCH -p medium
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH --mem=4000
#SBATCH --time=5-00:00:00
#SBATCH --mail-user=a.castellanoss@uniandes.edu.co
#SBATCH --mail-type=ALL
##SBATCH --array=1-30%10
#SBATCH -o logs/08_mdsine2_visualize_nodes_coeffs_.o%j

source ~/anaconda3/bin/activate
conda activate mdsine2

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference

# set $(sed -n ${SLURM_ARRAY_TASK_ID}p /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/08_mdsine2_visualize_nodes_coeffs_lookupfile.txt)
# simtype=$1
# dataset=$2
# seed=$3

# # Visualize the coefficients of the nodes
# python3 /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/visualize_nodes_coeffs.py \
# $simtype \
# $dataset \
# $seed

for simtype in no-module-learning cluster-learning fixed-clusters; do
    for dataset in LF0 HF0; do
        for seed in 0 3 4 23 127; do
            python3 /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/visualize_nodes_coeffs.py \
            $simtype \
            $dataset \
            $seed
        done;
    done;
done