#!/bin/bash

#SBATCH --job-name=05_mdsine2_negbin_inference
#SBATCH -p medium
#SBATCH -N 1
#SBATCH -n 4
#SBATCH --cpus-per-task=4
#SBATCH --mem=8000
#SBATCH --time=5-00:00:00
#SBATCH --mail-user=a.castellanoss@uniandes.edu.co
#SBATCH --mail-type=ALL
#SBATCH --array=1-2%2
#SBATCH -o logs/05_mdsine2_negbin_inference.o%j

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/07-mdsine2-negbin

dataset=$(sed -n ${SLURM_ARRAY_TASK_ID}p /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/05_mdsine2_negbin_inference_lookupfile.txt)

source ~/anaconda3/bin/activate
conda activate mdsine2

echo "Negbin inference for" $dataset
mdsine2 infer-negbin -i /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/06-mcnulty-datasets/$dataset/mcnulty_$dataset.pkl \
-s 0 \
-nb 5000 \
-ns 250000 \
-c 250 \
-b . \
-mp

echo "Negbin visualization"
mdsine2 visualize-negbin \
-c mcnulty-$dataset/mcmc.pkl \
-o mcnulty-$dataset

echo "Done"