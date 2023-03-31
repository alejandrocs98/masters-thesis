#!/bin/bash

#SBATCH --job-name=08_mdsine2_forward_simulate_noD
#SBATCH -p gpu
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16000
#SBATCH --time=5-00:00:00
#SBATCH --mail-user=a.castellanoss@uniandes.edu.co
#SBATCH --mail-type=ALL
#SBATCH --array=1-75%10
#SBATCH -o logs/08_mdsine2_forward_simulate_noD.o%j

source ~/anaconda3/bin/activate
conda activate mdsine2

set $(sed -n ${SLURM_ARRAY_TASK_ID}p /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/08_mdsine2_forward_simulate_lookupfile.txt);
dataset=$1
seed=$2
subject=$3
study=mcnulty-$dataset-seed$seed

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference/no-module-learning

echo "MDSINE2 forward-simulation of learned gLV model for individual" $subject "of" $dataset "with seed" $seed
mdsine2 forward-simulate \
-i $study/mcmc.pkl \
--study /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/06-mcnulty-datasets/$dataset/mcnulty_$dataset.pkl \
--subject $subject \
--plot all \
--gibbs-subsample 10 \
-o $study/forward-simulate/Subject_${subject}/fwsim.npy
echo "Done"

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference/cluster-learning

echo "MDSINE2 forward-simulation of learned gLV model for individual" $subject "of" $dataset "with seed" $seed
mdsine2 forward-simulate \
-i $study/mcmc.pkl \
--study /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/06-mcnulty-datasets/$dataset/mcnulty_$dataset.pkl \
--subject $subject \
--plot all \
--gibbs-subsample 10 \
-o $study/forward-simulate/Subject_${subject}/fwsim.npy
echo "Done"

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference/fixed-clusters

echo "MDSINE2 forward-simulation of learned gLV model for individual" $subject "of" $dataset "with seed" $seed
mdsine2 forward-simulate \
-i $study/mcmc.pkl \
--study /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/06-mcnulty-datasets/$dataset/mcnulty_$dataset.pkl \
--subject $subject \
--plot all \
--gibbs-subsample 10 \
-o $study/forward-simulate/Subject_${subject}/fwsim.npy
echo "Done"