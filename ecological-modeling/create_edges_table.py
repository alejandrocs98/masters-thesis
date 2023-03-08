#!/bin/python3
# -*- coding: utf-8 -*-
# Author: Alejandro Castellanos

# Usage: python3 create_edges_table.py [mean_matrix.tsv] [bayes_factors.tsv] [coclusters.tsv] [out-folder]
# posteriors/interactions/mean_matrix.tsv
# posteriors/interactions/bayes_factors.tsv
# posteriors/clustering/coclusters.tsv
# posteriors/network-vis

import mdsine2 as md2
from mdsine2.names import STRNAMES
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import os
import pandas as pd
from pathlib import Path
import matplotlib.cm as cm
import seaborn as sns
import sys

# Load interaction mean matrix
mean_matrix = pd.read_table(sys.argv[1], sep='\t', index_col=0)
# Load intercation bayes factors matrix
bayes_factors = pd.read_table(sys.argv[2], sep='\t', index_col=0)
# Load coclusters probabilitis matrix
coclusters = pd.read_table(sys.argv[3], sep=',', index_col=0)

# Define output folder
out_folder = sys.argv[4]

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

# Bayes factors to table
print('Bayes factors')
bayes_table = bayes_factors.reset_index()
bayes_table.rename(columns={'index': 'Source'}, inplace=True)
bayes_table = bayes_table.melt(id_vars=['Source'], var_name='Target', value_name='Interaction_bayes_factor')
bayes_table = bayes_table[bayes_table['Bayes_factor'] != 0].copy()
bayes_table = bayes_table.loc[:, ['Source', 'Target', 'Bayes_factor']].copy()
bayes_table.set_index(['Source', 'Target'], inplace=True)
print('Number of edges:', bayes_table.shape)
print(bayes_table)

# Coclusters to table
print('Coclusters')
coclusters_table = coclusters.reset_index()
coclusters_table.rename(columns={'index': 'Source'}, inplace=True)
coclusters_table = coclusters_table.melt(id_vars=['Source'], var_name='Target', value_name='Cocluster_probability')
coclusters_table = coclusters_table.loc[:, ['Source', 'Target', 'Cocluster_probability']].copy()
coclusters_table.set_index(['Source', 'Target'], inplace=True)
print('Number of edges:', coclusters_table.shape)
print(coclusters_table)

# Merge tables
print('Merging tables -> edges')
edges = pd.concat([interactions_table, bayes_table, coclusters_table], axis=1, join='inner')
edges.to_csv(f'{out_folder}/edges.tsv', sep='\t')
print('Number of edges:', edges.shape)
print(edges)