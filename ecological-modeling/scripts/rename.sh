#!/bin/bash

#SBATCH --job-name=10_mdsine2_keystoneness_analysis
#SBATCH -p medium
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16000
#SBATCH --time=5-00:00:00
#SBATCH --mail-user=a.castellanoss@uniandes.edu.co
#SBATCH --mail-type=ALL
#SBATCH -o logs/10_mdsine2_keystoneness_analysis.o%j


cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference
for simtype in cluster-learning fixed-clusters; do
    for dataset in LF0 HF0; do
        for seed in 0 3 4 23 127; do
        mv ~/masters-thesis/data/08-mdsine2-inference/$simtype/mcnulty-$dataset-seed$seed/posteriors/coclusters_mod.npy ~/masters-thesis/data/08-mdsine2-inference/$simtype/mcnulty-$dataset-seed$seed/posteriors/coclusters.npy
        mv ~/masters-thesis/data/08-mdsine2-inference/$simtype/mcnulty-$dataset-seed$seed/posteriors/n_clusters_mod.npy ~/masters-thesis/data/08-mdsine2-inference/$simtype/mcnulty-$dataset-seed$seed/posteriors/n_clusters.npy
        mv ~/masters-thesis/data/08-mdsine2-inference/$simtype/mcnulty-$dataset-seed$seed/posteriors/agglomeration_mod.npy ~/masters-thesis/data/08-mdsine2-inference/$simtype/mcnulty-$dataset-seed$seed/posteriors/agglomeration.npy
        done;
    done;
done;