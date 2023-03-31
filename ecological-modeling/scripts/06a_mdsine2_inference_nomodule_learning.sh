#!/bin/bash

#SBATCH --job-name=06a_mdsine2_inference_nomodule_learning
#SBATCH -p medium
#SBATCH -N 1
#SBATCH -n 4
#SBATCH --cpus-per-task=4
#SBATCH --mem=8000
#SBATCH --time=5-00:00:00
#SBATCH --mail-user=a.castellanoss@uniandes.edu.co
#SBATCH --mail-type=ALL
#SBATCH --array=1-10%10
#SBATCH -o logs/06a_mdsine2_inference_nomodule_learning.o%j

source ~/anaconda3/bin/activate
conda activate mdsine2

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference/no-module-learning

set $(sed -n ${SLURM_ARRAY_TASK_ID}p /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/06_mdsine2_inference_lookupfile.txt)
dataset=$1
seed=$2
study=mcnulty-$dataset-seed$seed

echo "MDSINE2 inference for" $dataset "with seed" $seed
mdsine2 infer \
-i /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/06-mcnulty-datasets/$dataset/mcnulty_$dataset.pkl \
--nomodules \
--negbin /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/07-mdsine2-negbin/mcnulty-$dataset/mcmc.pkl \
-s $seed \
-nb 5000 \
-ns 250000 \
-c 250 \
-ip strong-sparse \
-pp weak-agnostic \
--rename-study $study \
-b  . \
-mp 1

echo "Extraction of posterior parameters"
mdsine2 extract-posterior \
-i $study/mcmc.pkl \
-o $study/posteriors

echo "Posterior visualization"
mdsine2 visualize-posterior \
-c $study/mcmc.pkl \
-o $study/posteriors \
-s posterior

echo "MDSINE2 visualize learned interactions for" $dataset "with seed" $seed
mdsine2 interaction-to-cytoscape \
-i $study/mcmc.pkl \
-o $study/posteriors/mdsine2_interactions_network.json

echo "Done"