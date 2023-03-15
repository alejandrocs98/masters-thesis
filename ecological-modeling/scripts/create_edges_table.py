#!/bin/python3
# -*- coding: utf-8 -*-
# Author: Alejandro Castellanos

# Usage: python3 create_edges_table.py simtype dataset seed
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

# Define simulation type
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

# Load growth rates table
mean_matrix = pd.read_table(f'{input_folder}/interactions/mean_matrix.tsv', sep='\t', index_col=0)
# Interactions to table
print('Interaction matrix')
interactions_table = mean_matrix.reset_index()
interactions_table.rename(columns={'index': 'Source'}, inplace=True)
interactions_table = interactions_table.melt(id_vars=['Source'], var_name='Target', value_name='Interaction_coefficient')
def interaction_type(x):
    if x > 0:
        return '+'
    elif x < 0:
        return '-'
    else:
        return np.nan
interactions_table['Interaction_magnitude_log'] = np.log10(np.abs(interactions_table['Interaction_coefficient']))
interactions_table['Interaction'] = interactions_table['Interaction_coefficient'].apply(interaction_type)
interactions_table.dropna(inplace=True)
interactions_table = interactions_table.loc[:, ['Source', 'Target', 'Interaction', 'Interaction_magnitude_log']].copy()
interactions_table.set_index(['Source', 'Target'], inplace=True)
print('Number of edges:', interactions_table.shape)
print(interactions_table)

# Load Bayes factors table
bayes_factors = pd.read_table(f'{input_folder}/interactions/bayes_factors.tsv', sep='\t', index_col=0)
# Bayes factors to table
print('Bayes factors')
bayes_table = bayes_factors.reset_index()
bayes_table.rename(columns={'index': 'Source'}, inplace=True)
bayes_table = bayes_table.melt(id_vars=['Source'], var_name='Target', value_name='Interaction_bayes_factor')
bayes_table = bayes_table[bayes_table['Interaction_bayes_factor'] != 0].copy()
bayes_table = bayes_table.loc[:, ['Source', 'Target', 'Interaction_bayes_factor']].copy()
bayes_table.set_index(['Source', 'Target'], inplace=True)
print('Number of edges:', bayes_table.shape)
print(bayes_table)


# Load coclustr probability
print('Coclusters')
if simtype == 'cluster-learning':
    coclusters = pd.read_csv(f'{input_folder}/clustering/coclusters.tsv', sep=',', index_col=0)
elif simtype == 'fixed-clusters':
    new_path = Path(f'~/masters-thesis/data/08-mdsine2-inference/cluster-learning/mcnulty-{dataset}-seed{seed}/posteriors')
    coclusters = pd.read_csv(f'{new_path}/clustering/coclusters.tsv', sep=',', index_col=0)
else:
    coclusters = pd.DataFrame(np.identity(len(taxa)), index=taxa, columns=taxa)
coclusters_table = coclusters.reset_index()
coclusters_table.rename(columns={'index': 'Source'}, inplace=True)
coclusters_table = coclusters_table.melt(id_vars=['Source'], var_name='Target', value_name='Cocluster_probability')
coclusters_table = coclusters_table.loc[:, ['Source', 'Target', 'Cocluster_probability']].copy()
coclusters_table.set_index(['Source', 'Target'], inplace=True)
print('Number of edges:', coclusters_table.shape)
# Coclusters to table
print(coclusters_table)

# Merge tables
print('Merging tables -> edges')
edges = pd.concat([interactions_table, bayes_table, coclusters_table], axis=1, join='inner')
edges.to_csv(f'{output_folder}/edges.tsv', sep='\t')
print('Number of edges:', edges.shape)
print(edges)