#!/bin/bash

#SBATCH --job-name=03b_genomes_orthologues_orthofinder
#SBATCH -p medium
#SBATCH -N 1
#SBATCH -n 4
#SBATCH --cpus-per-task=4
#SBATCH --mem=40000
#SBATCH --time=5-00:00:00
#SBATCH --mail-user=a.castellanoss@uniandes.edu.co
#SBATCH --mail-type=ALL
#SBATCH -o logs/03b_genomes_orthologues_orthofinder.o%j

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-tesis/data

module load orthofinder/2.5.4

orthofinder -f 04-genomes-proteins/McNulty -a 4 -M msa -A mafft -T iqtree -o 05-genomes-orthologues/msa