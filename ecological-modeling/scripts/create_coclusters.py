#!/bin/python3
# -*- coding: utf-8 -*-
# Author: Alejandro Castellanos

# Usage: python3 create_edges_table.py simtype dataset seed output-folder
# simtype: [no-module-learning | cluster-learning | fixed-clusters]
# dataset: [LF0 | HF0]
# seed: [0 | 3 | 4 | 23 | 127]

import mdsine2 as md2
from mdsine2.names import STRNAMES
import matplotlib.pyplot as plt; plt.rc('font', size=16)
import numpy as np
import os
import pandas as pd
from pathlib import Path
import sys

# Define simtype
simtype = sys.argv[1]
# Define dataset
dataset = sys.argv[2]
# Define seed
seed = sys.argv[3]

# Define input folder
input_folder = Path(f'/hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference/{simtype}/mcnulty-{dataset}-seed{seed}/posteriors')
#Define output folder
output_folder = input_folder

taxa = ['B_caccae',
        'B_cellulosilyticus_WH2',
        'B_ovatus',
        'B_thetaiotaomicron',
        'B_uniformis',
        'B_vulgatus',
        'C_aerofaciens',
        'C_scindens',
        'C_spiroforme',
        'D_longicatena',
        'P_distasonis',
        'R_obeum']

coclusters = np.identity(len(taxa))
np.save(f'{output_folder}/coclusters.npy', coclusters)
n_clusters = np.array([12])
np.save(f'{output_folder}/n_clusters.npy', n_clusters)
agglomeration = np.arange(len(taxa))
np.save(f'{output_folder}/agglomeration.npy', agglomeration)