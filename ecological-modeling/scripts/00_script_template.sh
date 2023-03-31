#!/bin/bash

#SBATCH --job-name=
#SBATCH -p medium
#SBATCH -N 1
#SBATCH -n 4
#SBATCH --cpus-per-task=1
#SBATCH --mem=40000
#SBATCH --time=5-00:00:00
#SBATCH --mail-user=a.castellanoss@uniandes.edu.co
#SBATCH --mail-type=ALL
#SBATCH -o logs/.o%j

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-tesis/data

# module load quast/5.0.2
# source ~/anaconda3/bin/activate
# conda activate

