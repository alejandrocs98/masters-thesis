#!/bin/python3

import pandas as pd
from micom.workflows import build
from micom import load_pickle
from micom.qiime_formats import load_qiime_model_db, load_qiime_medium
from micom.workflows import grow
import pickle
from micom.viz import *
from micom.workflows import tradeoff

taxonomy_names = {'B_caccae': 'Bacteroides caccae',
                'B_cellulosilyticus_WH2': 'Bacteroides cellulosilyticus',
                'B_ovatus': 'Bacteroides ovatus',
                'B_thetaiotaomicron': 'Bacteroides thetaiotaomicron',
                'B_uniformis': 'Bacteroides uniformis',
                'B_vulgatus': 'Bacteroides vulgatus',
                'C_aerofaciens': 'Collinsella aerofaciens',
                'C_scindens': 'Clostridium scindens',
                'C_spiroforme': 'Clostridium spiroforme',
                'D_longicatena': 'Dorea longicatena',
                'P_distasonis': 'Parabacteroides distasonis',
                'R_obeum': 'Blautia obeum',
                }

model_ids = {'B_caccae': 'Bacteroides_caccae_ATCC_43185.xml',
                'B_cellulosilyticus_WH2': 'Bacteroides_cellulosilyticus_WH2.xml',
                'B_ovatus': 'Bacteroides_ovatus_ATCC_8483.xml',
                'B_thetaiotaomicron': 'Bacteroides_thetaiotaomicron_VPI_5482.xml',
                'B_uniformis': 'Bacteroides_uniformis_ATCC_8492.xml',
                'B_vulgatus': 'Bacteroides_vulgatus_ATCC_8482.xml',
                'C_aerofaciens': 'Collinsella_aerofaciens_ATCC_25986.xml',
                'C_scindens': 'Clostridium_scindens_ATCC_35704.xml',
                'C_spiroforme': 'Clostridium_spiroforme_DSM_1552.xml',
                # 'D_longicatena': 'Dorea_longicatena',
                'P_distasonis': 'Parabacteroides_distasonis_ATCC_8503.xml',
                'R_obeum': 'Blautia_obeum_ATCC_29174.xml'}

lf0_reads_34 = pd.read_table('lf0_data.tsv', sep='\t')
hf0_reads_12 = pd.read_table('hf0_data.tsv', sep='\t')

manifest_lf0 = build(
    lf0_reads_34,  
    model_db=None,
    out_folder='models/Community/lf0', 
    cutoff=0.000001, 
    threads=4
    )
manifest_lf0

manifest_hf0 = build(
    hf0_reads_12, 
    model_db=None,
    out_folder='models/Community/hf0', 
    cutoff=0.000001, 
    threads=4
    )
manifest_hf0

western_agora = load_qiime_medium('media/western_diet_gut_agora.qza')
western_agora

high_fiber_agora = load_qiime_medium('media/vmh_high_fiber_agora.qza')
high_fiber_agora

tradeoff_results_lf0 = tradeoff(manifest_lf0, "results/lf0", high_fiber_agora, threads=4)
tradeoff_results_hf0 = tradeoff(manifest_hf0, "results/lf0", western_agora, threads=4)

