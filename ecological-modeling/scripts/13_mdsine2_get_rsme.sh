#!/bin/bash

#SBATCH --job-name=13_mdsine2_get_rsme
#SBATCH -p medium
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8000
#SBATCH --time=5-00:00:00
#SBATCH --mail-user=a.castellanoss@uniandes.edu.co
#SBATCH --mail-type=ALL
##SBATCH --array=1-24%10
#SBATCH -o logs/13_mdsine2_get_rsme_.o%j

source ~/anaconda3/bin/activate
conda activate mdsine2

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data

# set $(sed -n ${SLURM_ARRAY_TASK_ID}p /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/13_mdsine2_get_rsme_lookupfile.txt)
# simtype=$1
# dataset=$2
# intra=$3
# inter=$4

# python3 /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/get_rsme.py \
# $simtype \
# $dataset \
# $intra \
# $inter

for simtype in no-module-learning cluster-learning fixed-clusters; do
    for dataset in LF0 HF0; do
        for intra in sum mean; do
            for inter in sum mean; do
                python3 /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/get_rsme.py \
                $simtype \
                $dataset \
                $intra \
                $inter;
            done;
        done;
    done;
done