#!/bin/bash

source ~/anaconda3/bin/activate
conda activate carveme

# for i in $(ls genomes-proteins); do
# 	name=$(basename $i _aa.fasta);
# 	echo $name "GSMM reconsctruction"
# 	carve $i -g LB[-O2] --fbc2 -o gsmms/$name.xml;
# done

carve genomes-proteins/B_caccae_aa.fasta -g LB[-O2] --fbc2 -o gsmms/B_caccae.xml >> gsmms_recons.log 2>&1
carve genomes-proteins/B_cellulosilyticus_aa.fasta -g LB[-O2] --fbc2 -o gsmms/B_cellulosilyticus.xml >> gsmms_recons.log 2>&1
carve genomes-proteins/B_ovatus_aa.fasta -g LB[-O2] --fbc2 -o gsmms/B_ovatus.xml >> gsmms_recons.log 2>&1
carve genomes-proteins/B_thetaiotaomicron_aa.fasta -g LB[-O2] --fbc2 -o gsmms/B_thetaiotaomicron.xml >> gsmms_recons.log 2>&1
carve genomes-proteins/B_uniformis_aa.fasta -g LB[-O2] --fbc2 -o gsmms/B_uniformis.xml >> gsmms_recons.log 2>&1
carve genomes-proteins/B_vulgatus_aa.fasta -g LB[-O2] --fbc2 -o gsmms/B_vulgatus.xml >> gsmms_recons.log 2>&1
carve genomes-proteins/C_aerofaciens_aa.fasta -g LB[-O2] --fbc2 -o gsmms/C_aerofaciens.xml >> gsmms_recons.log 2>&1
carve genomes-proteins/C_scindens_aa.fasta -g LB[-O2] --fbc2 -o gsmms/C_scindens.xml >> gsmms_recons.log 2>&1
carve genomes-proteins/C_spiroforme_aa.fasta -g LB[-O2] --fbc2 -o gsmms/C_spiroforme.xml >> gsmms_recons.log 2>&1
carve genomes-proteins/D_longicatena_aa.fasta -g LB[-O2] --fbc2 -o gsmms/D_longicatena.xml >> gsmms_recons.log 2>&1
carve genomes-proteins/P_distasonis_aa.fasta -g LB[-O2] --fbc2 -o gsmms/P_distasonis.xml >> gsmms_recons.log 2>&1
carve genomes-proteins/R_obeum_aa.fasta -g LB[-O2] --fbc2 -o gsmms/R_obeum.xml >> gsmms_recons.log 2>&1