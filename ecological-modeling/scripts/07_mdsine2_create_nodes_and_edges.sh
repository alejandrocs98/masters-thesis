#!/bin/bash

#SBATCH --job-name=07_mdsine2_create_nodes_and_edges
#SBATCH -p medium
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH --mem=4000
#SBATCH --time=5-00:00:00
#SBATCH --mail-user=a.castellanoss@uniandes.edu.co
#SBATCH --mail-type=ALL
##SBATCH --array=1-30%10
#SBATCH -o logs/07_mdsine2_create_nodes_and_edges_.o%j

source ~/anaconda3/bin/activate
conda activate mdsine2

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference

# set $(sed -n ${SLURM_ARRAY_TASK_ID}p /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/07_mdsine2_create_nodes_and_edges_lookupfile.txt)
# simtype=$1
# dataset=$2
# seed=$3

# # Create nodes
# python3 /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/create_nodes_table.py \
# $simtype \
# $dataset \
# $seed
# # Create edges
# python3 /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/create_edges_table.py \
# $simtype \
# $dataset \
# $seed

for simtype in no-module-learning cluster-learning fixed-clusters; do
    for dataset in LF0 HF0; do
        for seed in 0 3 4 23 127; do
            python3 /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/create_nodes_table.py \
            $simtype \
            $dataset \
            $seed;
            python3 /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/create_edges_table.py \
            $simtype \
            $dataset \
            $seed;
        done;
    done;
done