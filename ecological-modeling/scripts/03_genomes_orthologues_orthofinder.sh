#!/bin/bash

#SBATCH --job-name=03_genomes_orthologues_orthofinder
#SBATCH -p medium
#SBATCH -N 1
#SBATCH -n 4
#SBATCH --cpus-per-task=4
#SBATCH --mem=40000
#SBATCH --time=5-00:00:00
#SBATCH --mail-user=a.castellanoss@uniandes.edu.co
#SBATCH --mail-type=ALL
#SBATCH -o logs/03_genomes_orthologues_orthofinder.o%j

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-tesis/data

module load orthofinder/2.5.4

echo "McNulty's community"
orthofinder -f 04-genomes-proteins/McNulty -a 4 -o 05-genomes-orthologues/McNulty

echo "Reyes' community"
orthofinder -f 04-genomes-proteins/Reyes -a 4 -o 05-genomes-orthologues/Reyes