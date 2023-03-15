#!/bin/bash

#SBATCH --job-name=12_mdsine2_rhat_calculation
#SBATCH -p medium
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16000
#SBATCH --time=5-00:00:00
#SBATCH --mail-user=a.castellanoss@uniandes.edu.co
#SBATCH --mail-type=ALL
#SBATCH --array=1-6%6
#SBATCH -o logs/12_mdsine2_rhat_calculation_.o%j

source ~/anaconda3/bin/activate
conda activate mdsine2

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data

set $(sed -n ${SLURM_ARRAY_TASK_ID}p /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/12_mdsine2_rhat_calculation_lookupfile.txt)
simtype=$1
dataset=$2

echo $simtype $dataset;
python3 /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/rhat_calculation.py \
$simtype \
$dataset


# for simtype in no-module-learning cluster-learning fixed-clusters; do
#     for dataset in LF0 HF0; do
#         echo $simtype $dataset;
#         python3 /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/rhat_calculation.py \
#         $simtype \
#         $dataset;
#     done;
# done