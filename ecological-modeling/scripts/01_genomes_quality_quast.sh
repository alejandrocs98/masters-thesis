#!/bin/bash

#SBATCH --job-name=01_genomes_quality_quast
#SBATCH -p medium
#SBATCH -N 1
#SBATCH -n 4
#SBATCH --cpus-per-task=1
#SBATCH --mem=40000
#SBATCH --time=5-00:00:00
#SBATCH --mail-user=a.castellanoss@uniandes.edu.co
#SBATCH --mail-type=ALL
#SBATCH -o logs/01_genomes_quality_quast.o%j

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-tesis/data

module load quast/5.0.2

echo "McNulty's community"
python /hpcfs/apps/anaconda/3.9/envs/quast-5.0.2/bin/quast -o 02-genomes-stats/McNulty 01-genomes/McNulty/*

echo "Reyes' community"
python /hpcfs/apps/anaconda/3.9/envs/quast-5.0.2/bin/quast -o 02-genomes-stats/Reyes 01-genomes/Reyes/*