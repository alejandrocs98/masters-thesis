#!/bin/bash

#SBATCH --job-name=04_mdsine2_studies_creation_noD
#SBATCH -p medium
#SBATCH -N 1
#SBATCH -n 4
#SBATCH --cpus-per-task=4
#SBATCH --mem=8000
#SBATCH --time=5-00:00:00
#SBATCH --mail-user=a.castellanoss@uniandes.edu.co
#SBATCH --mail-type=ALL
#SBATCH -o logs/04_mdsine2_studies_creation_noD.o%j

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/06-mcnulty-datasets

source ~/anaconda3/bin/activate
conda activate mdsine2

for dataset in LF0 HF0; do
	echo $dataset "Study Object creation"
	mdsine2 input \
	-n mcnulty-$dataset \
	-t $dataset/taxonomy.tsv \
	-m $dataset/metadata.tsv \
	-r $dataset/reads.tsv \
	-q $dataset/dna_molecules.tsv \
	-p $dataset/perturbations.tsv \
	-o $dataset/mcnulty_$dataset.pkl
	echo $(pwd)/$dataset/mcnulty_$dataset.pkl
done