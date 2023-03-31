#!/bin/bash

#SBATCH --job-name=12_mdsine2_diagnostics.sh
#SBATCH -p short
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16000
#SBATCH --time=12:00:00
#SBATCH --mail-user=a.castellanoss@uniandes.edu.co
#SBATCH --mail-type=ALL
#SBATCH --array=1-6%6
#SBATCH -o logs/12_mdsine2_diagnostics.sh.o%j

source ~/anaconda3/bin/activate
conda activate bayesian-diagnostics

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference

set $(sed -n ${SLURM_ARRAY_TASK_ID}p /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/12_mdsine2_diagnostics_lookupfile.txt)
# simtype=$1
dataset=$1

simtype=no-module-learning

echo $simtype $dataset;
python3 /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/get_convergence_diagnostics.py \
$simtype \
$dataset


# for simtype in no-module-learning cluster-learning fixed-clusters; do
#     for dataset in LF0 HF0; do
#         echo $simtype $dataset;
#         python3 /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/get_convergence_diagnostics.py \
#         $simtype \
#         $dataset;
#     done;
# done