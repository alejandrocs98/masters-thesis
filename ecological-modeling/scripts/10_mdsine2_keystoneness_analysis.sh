#!/bin/bash

#SBATCH --job-name=10_mdsine2_keystoneness_analysis
#SBATCH -p gpu
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16000
#SBATCH --time=5-00:00:00
#SBATCH --mail-user=a.castellanoss@uniandes.edu.co
#SBATCH --mail-type=ALL
#SBATCH --array=1-10%10
#SBATCH -o logs/10_mdsine2_keystoneness_analysis.o%j

source ~/anaconda3/bin/activate
conda activate mdsine2

set $(sed -n ${SLURM_ARRAY_TASK_ID}p /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/10_mdsine2_keystoneness_analysis_lookupfile.txt)
dataset=$1
seed=$2
study=mcnulty-$dataset-seed$seed

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference/no-module-learning

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
--simulate-every-n 10 \
-dt 0.01
echo "Done"

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference/cluster-learning

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
-o $study/keystoneness-module \
--n-days 40 \
--simulate-every-n 10 \
-dt 0.01
echo "Done"

mv mcnulty-$dataset-seed$seed/posteriors/coclusters.npy mcnulty-$dataset-seed$seed/posteriors/coclusters_mod.npy
mv mcnulty-$dataset-seed$seed/posteriors/n_clusters.npy mcnulty-$dataset-seed$seed/posteriors/n_clusters_mod.npy
mv mcnulty-$dataset-seed$seed/posteriors/agglomeration.npy mcnulty-$dataset-seed$seed/posteriors/agglomeration_mod.npy

echo "MDSINE2 individual keystoneness analysis for" $dataset "with seed" $seed
python3 /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/create_coclusters.py \
cluster-learning \
$dataset \
$seed

echo "MDSINE2 keystoneness analysis for" $dataset "with seed" $seed
mdsine2 evaluate-keystoneness \
-e $study/posteriors \
-s /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/06-mcnulty-datasets/$dataset/mcnulty_$dataset.pkl \
-if $study/initial_abundances.tsv \
-o $study/keystoneness-individual \
--n-days 40 \
--simulate-every-n 10 \
-dt 0.01
echo "Done"

mv mcnulty-$dataset-seed$seed/posteriors/coclusters_mod.npy mcnulty-$dataset-seed$seed/posteriors/coclusters.npy
mv mcnulty-$dataset-seed$seed/posteriors/n_clusters_mod.npy mcnulty-$dataset-seed$seed/posteriors/n_clusters.npy
mv mcnulty-$dataset-seed$seed/posteriors/agglomeration_mod.npy mcnulty-$dataset-seed$seed/posteriors/agglomeration.npy

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference/fixed-clusters

cp /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference/cluster-learning/mcnulty-$dataset-seed$seed/posteriors/coclusters.npy mcnulty-$dataset-seed$seed/posteriors
cp /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference/cluster-learning/mcnulty-$dataset-seed$seed/posteriors/n_clusters.npy mcnulty-$dataset-seed$seed/posteriors
cp /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference/cluster-learning/mcnulty-$dataset-seed$seed/posteriors/agglomeration.npy mcnulty-$dataset-seed$seed/posteriors

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
-o $study/keystoneness-module \
--n-days 40 \
--simulate-every-n 10 \
-dt 0.01
echo "Done"

mv mcnulty-$dataset-seed$seed/posteriors/coclusters.npy mcnulty-$dataset-seed$seed/posteriors/coclusters_mod.npy
mv mcnulty-$dataset-seed$seed/posteriors/n_clusters.npy mcnulty-$dataset-seed$seed/posteriors/n_clusters_mod.npy
mv mcnulty-$dataset-seed$seed/posteriors/agglomeration.npy mcnulty-$dataset-seed$seed/posteriors/agglomeration_mod.npy

echo "MDSINE2 individual keystoneness analysis for" $dataset "with seed" $seed
python3 /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/scripts/create_coclusters.py \
fixed-clusters \
$dataset \
$seed

echo "MDSINE2 keystoneness analysis for" $dataset "with seed" $seed
mdsine2 evaluate-keystoneness \
-e $study/posteriors \
-s /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/06-mcnulty-datasets/$dataset/mcnulty_$dataset.pkl \
-if $study/initial_abundances.tsv \
-o $study/keystoneness-individual \
--n-days 40 \
--simulate-every-n 10 \
-dt 0.01
echo "Done"

mv mcnulty-$dataset-seed$seed/posteriors/coclusters_mod.npy mcnulty-$dataset-seed$seed/posteriors/coclusters.npy
mv mcnulty-$dataset-seed$seed/posteriors/n_clusters_mod.npy mcnulty-$dataset-seed$seed/posteriors/n_clusters.npy
mv mcnulty-$dataset-seed$seed/posteriors/agglomeration_mod.npy mcnulty-$dataset-seed$seed/posteriors/agglomeration.npy