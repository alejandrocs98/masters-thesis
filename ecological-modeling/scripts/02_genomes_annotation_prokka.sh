#!/bin/bash

#SBATCH --job-name=02_genomes_annotation_prokka
#SBATCH -p medium
#SBATCH -N 1
#SBATCH -n 4
#SBATCH --cpus-per-task=1
#SBATCH --mem=40000
#SBATCH --time=5-00:00:00
#SBATCH --mail-user=a.castellanoss@uniandes.edu.co
#SBATCH --mail-type=ALL
#SBATCH -o logs/02_genomes_annotation_prokka.o%j

cd /hpcfs/home/ciencias_biologicas/a.castellanoss/masters-tesis/data
if='01-genomes/Reyes'
of='03-genomes-annotation'

source ~/anaconda3/bin/activate
conda activate prokka

echo "Starting 'Bacteroides caccae' annotation"
prokka --addgenes --mincontiglen 200 --force --genus Bacteroides --usegenus --outdir $of/B_caccae --locustag Bc --prefix B_caccae $if/B_caccae_nt.fasta
echo "'Bacteroides caccae' annotation completed"

echo "Starting 'Bacteroides ovatus' annotation"
prokka --addgenes --mincontiglen 200 --force --genus Bacteroides --usegenus --outdir $of/B_ovatus --locustag Bo --prefix B_ovatus $if/B_ovatus_nt.fasta
echo "'Bacteroides ovatus' annotation completed"

echo "Starting 'Bacteroides thetaiotaomicron' annotation"
prokka --addgenes --mincontiglen 200 --force --genus Bacteroides --usegenus --outdir $of/B_thetaiotaomicron --locustag Bth --prefix B_thetaiotaomicron $if/B_thetaiotaomicron_nt.fasta
echo "'Bacteroides thetaiotaomicron' annotation completed"

echo "Starting 'Bacteroides uniformis' annotation"
prokka --addgenes --mincontiglen 200 --force --genus Bacteroides --usegenus --outdir $of/B_uniformis --locustag Bu --prefix B_uniformis $if/B_uniformis_nt.fasta
echo "'Bacteroides uniformis' annotation completed"

echo "Starting 'Bacteroides vulgatus' annotation"
prokka --addgenes --mincontiglen 200 --force --genus Bacteroides --usegenus --outdir $of/B_vulgatus --locustag Bv --prefix B_vulgatus $if/B_vulgatus_nt.fasta
echo "'Bacteroides vulgatus' annotation completed"

echo "Starting 'Bacteroides cellulosilyticus' annotation"
prokka --addgenes --mincontiglen 200 --force --genus Bacteroides --usegenus --outdir $of/B_cellulosilyticus --locustag BcWH2 --prefix B_cellulosilyticus $if/B_cellulosilyticus_nt.fasta
echo "'Bacteroides cellulosilyticus' annotation completed"

echo "Starting 'Clostridium scindens' annotation"
prokka --addgenes --mincontiglen 200 --force --genus Clostridium --usegenus --outdir $of/C_scindens --locustag Csc --prefix C_scindens $if/C_scindens_nt.fasta
echo "'Clostridium scindens' annotation completed"

echo "Starting 'Clostridium spiroforme' annotation"
prokka --addgenes --mincontiglen 200 --force --genus Clostridium --usegenus --outdir $of/C_spiroforme --locustag Csp --prefix C_spiroforme $if/C_spiroforme_nt.fasta
echo "'Clostridium spiroforme' annotation completed"

echo "Starting 'Collinsella aerofaciens' annotation"
prokka --addgenes --mincontiglen 200 --force --genus Collinsella --usegenus --outdir $of/C_aerofaciens --locustag Ca --prefix C_aerofaciens $if/C_aerofaciens_nt.fasta
echo "'Collinsella aerofaciens' annotation completed"

echo "Starting 'Dorea longicatena' annotation"
prokka --addgenes --mincontiglen 200 --force --genus Dorea --usegenus --outdir $of/D_longicatena --locustag Dl --prefix D_longicatena $if/D_longicatena_nt.fasta
echo "'Dorea longicatena' annotation completed"

echo "Starting 'Parabacteroides distasonis' annotation"
prokka --addgenes --mincontiglen 200 --force --genus Parabacteroides --usegenus --outdir $of/P_distasonis --locustag Pd --prefix P_distasonis $if/P_distasonis_nt.fasta
echo "'Parabacteroides distasonis' annotation completed"

echo "Starting 'Ruminococcus obeum' annotation"
prokka --addgenes --mincontiglen 200 --force --genus Ruminococcus --usegenus --outdir $of/R_obeum --locustag Ro --prefix R_obeum $if/R_obeum_nt.fasta
echo "'Ruminococcus obeum' annotation completed"

echo "Starting 'Eubacterium rectale' annotation"
prokka --addgenes --mincontiglen 200 --force --genus Eubacterium --usegenus --outdir $of/E_rectale --locustag Er --prefix E_rectale $if/E_rectale_nt.fasta
echo "'Eubacterium rectale' annotation completed"

echo "Starting 'Faecalibacterium prausnitzii M21/2' annotation"
prokka --addgenes --mincontiglen 200 --force --genus Faecalibacterium --usegenus --outdir $of/F_prausnitzii --locustag Fp --prefix F_prausnitzii $if/F_prausnitzii_nt.fasta
echo "'Faecalibacterium prausnitzii M21/2' annotation completed"

echo "Starting 'Ruminococcus torques' annotation"
prokka --addgenes --mincontiglen 200 --force --genus Ruminococcus --usegenus --outdir $of/R_torques --locustag Rt --prefix R_torques $if/R_torques_nt.fasta
echo "'Ruminococcus torques' annotation completed"