#!/bin/bash

#SBATCH --job-name=08c_mdsine2_forward_simulate_fiexd_clusters
#SBATCH -p medium
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16000
#SBATCH --time=5-00:00:00
#SBATCH --mail-user=a.castellanoss@uniandes.edu.co
#SBATCH --mail-type=ALL
#SBATCH --array=1-75%10
#SBATCH -o logs/08c_mdsine2_forward_simulate_fiexd_clusters.o%j

source ~/anaconda3/bin/activate
conda activate mdsine2

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference/fixed-clusters

set $(sed -n ${SLURM_ARRAY_TASK_ID}p /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/08_mdsine2_forward_simulate_lookupfile.txt);
dataset=$1
seed=$2
subject=$3
study=mcnulty-$dataset-seed$seed

echo "MDSINE2 forward-simulation of learned gLV model for individual" $subject "of" $dataset "with seed" $seed
mdsine2 forward-simulate \
-i $study/mcmc.pkl \
--study /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/06-mcnulty-datasets/$dataset/mcnulty_$dataset.pkl \
--subject $subject \
--plot all \
--gibbs-subsample 100 \
-o $study/forward-simulate/Subject_${subject}/fwsim.npy
echo "Done"