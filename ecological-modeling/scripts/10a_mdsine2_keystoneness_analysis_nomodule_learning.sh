#!/bin/bash

#SBATCH --job-name=010a_mdsine2_keystoneness_analysis_nomodule_learning
#SBATCH -p medium
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16000
#SBATCH --time=5-00:00:00
#SBATCH --mail-user=a.castellanoss@uniandes.edu.co
#SBATCH --mail-type=ALL
#SBATCH --array=1-10%10
#SBATCH -o logs/010a_mdsine2_keystoneness_analysis_nomodule_learning.o%j

source ~/anaconda3/bin/activate
conda activate mdsine2

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference/no-module-learning

set $(sed -n ${SLURM_ARRAY_TASK_ID}p /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/10_mdsine2_keystoneness_analysis_lookupfile.txt)
dataset=$1
seed=$2
study=mcnulty-$dataset-seed$seed

python3 /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/create_coclusters.py \
no-module-learning \
$dataset \
$seed

echo "Extraction of initial conditions for" $dataset "with seed" $seed
mdsine2 extract-abundances \
-s /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/06-mcnulty-datasets/$dataset/mcnulty_$dataset.pkl \
-t 0 \
-o $study/initial_abundances.tsv
echo "Done"
echo "MDSINE2 keystoneness analysis for" $dataset "with seed" $seed
mdsine2 evaluate-keystoneness \
-e $study/posteriors \
-s /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/06-mcnulty-datasets/$dataset/mcnulty_$dataset.pkl \
-if $study/initial_abundances.tsv \
-o $study/keystoneness-individual \
--n-days 40 \
--simulate-every-n 100 \
-dt 0.01
echo "Done"