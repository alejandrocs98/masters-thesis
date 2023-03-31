#!/bin/bash

#SBATCH --job-name=06_mdsine2_inference_noD_3
#SBATCH -p short
#SBATCH -N 1
#SBATCH -n 4
#SBATCH --cpus-per-task=4
#SBATCH --mem=8000
#SBATCH --time=2-00:00:00
#SBATCH --mail-user=a.castellanoss@uniandes.edu.co
#SBATCH --mail-type=ALL
#SBATCH --array=1-3%3
#SBATCH -o logs/06_mdsine2_inference_noD_3.o%j

source ~/anaconda3/bin/activate
conda activate mdsine2

set $(sed -n ${SLURM_ARRAY_TASK_ID}p /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/06_mdsine2_inference_lookupfile_3.txt)
dataset=$1
seed=$2
study=mcnulty-$dataset-seed$seed

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference/no-module-learning

echo "MDSINE2 inference for" $dataset "with seed" $seed
mdsine2 infer \
-i /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/06-mcnulty-datasets/$dataset/mcnulty_$dataset.pkl \
--nomodules \
--negbin /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/07-mdsine2-negbin/mcnulty-$dataset/mcmc.pkl \
-s $seed \
-nb 1000 \
-ns 25000 \
-c 100 \
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

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference/cluster-learning

echo "MDSINE2 inference for" $dataset "with seed" $seed
mdsine2 infer \
-i /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/06-mcnulty-datasets/$dataset/mcnulty_$dataset.pkl \
--negbin /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/07-mdsine2-negbin/mcnulty-$dataset/mcmc.pkl \
-s $seed \
-nb 1000 \
-ns 25000 \
-c 100 \
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

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference/fixed-clusters

echo "MDSINE2 inference for" $dataset "with seed" $seed
mdsine2 infer \
-i /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/06-mcnulty-datasets/$dataset/mcnulty_$dataset.pkl \
--fixed-clustering /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-infer/cluster-learning/$dataset/seed$seed/mcnulty-$dataset/mcmc.pkl \
--negbin /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/07-mdsine2-negbin/mcnulty-$dataset/mcmc.pkl \
-s $seed \
-nb 1000 \
-ns 25000 \
-c 100 \
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