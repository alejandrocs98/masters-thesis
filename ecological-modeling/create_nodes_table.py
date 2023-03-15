#!/bin/python3
# -*- coding: utf-8 -*-
# Author: Alejandro Castellanos

# Usage: python3 create_nodes_table.py simtype dataset seed
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
growth = pd.read_table(f'{input_folder}/growth/values.tsv', sep='\t', index_col=0)
# Tweak growth rates table
print('Growth rates')
growth = growth.loc[:, ['mean', 'median']].copy()
growth.index.name = 'name'
growth.rename(columns={'mean': 'Growth_mean', 'median': 'Growth_median'}, inplace=True)
growth.drop('mean', axis=0, inplace=True)
print(growth)

# Load self interactions table
self_interactions = pd.read_table(f'{input_folder}/self_interactions/values.tsv', sep='\t', index_col=0)
# Tweak self interactions table
print('Self interactions')
self_interactions = self_interactions.loc[:, ['mean', 'median']].copy()
self_interactions.index.name = 'name'
self_interactions.rename(columns={'mean': 'Self_interaction_mean', 'median': 'Self_interaction_median'}, inplace=True)
self_interactions.drop('mean', axis=0, inplace=True)
print(self_interactions)

# Tweak cluster assignment table
print('Cluster assignment')
# Load cluster assignment table
if simtype == 'cluster-learning':
    cluster_assignment = pd.read_table(f'{input_folder}/clustering/clusterassignments.tsv', sep='\t', index_col=0)
    cluster_assignment.columns = ['Cluster']
    print(cluster_assignment)
elif simtype == 'fixed-clusters':
    new_path = Path(f'~/masters-thesis/data/08-mdsine2-inference/cluster-learning/mcnulty-{dataset}-seed{seed}/posteriors')
    cluster_assignment = pd.read_table(f'{new_path}/clustering/clusterassignments.tsv', sep='\t', index_col=0)
    cluster_assignment.columns = ['Cluster']
else:
    cluster_assignment = pd.DataFrame({'name':taxa, 'Cluster':list(range(12))})
    cluster_assignment.set_index('name', inplace=True)

# Load perturbations effects table
if dataset == 'LF0':
    perturbations = pd.read_table(f'{input_folder}/HF/HS/values.tsv', sep='\t', index_col=0)
    perturbations_bayes_factors = pd.read_table(f'{input_folder}/HF/HS/bayes_factors.tsv', sep='\t', index_col=0).T
elif dataset == 'HF0':
    perturbations = pd.read_table(f'{input_folder}/LF/HPP/values.tsv', sep='\t', index_col=0)
    perturbations_bayes_factors = pd.read_table(f'{input_folder}/LF/HPP/bayes_factors.tsv', sep='\t', index_col=0).T

# Tweak perturbations effects table
print('Perturbations')
perturbations = perturbations.loc[:, ['mean', 'median']].copy()
perturbations.index.name = 'name'
perturbations.rename(columns={'mean': 'Perturbation_mean', 'median': 'Perturbation_median'}, inplace=True)
print(perturbations)

# Tweak perturbations bayes factors table
print('Perturbations bayes factors')
perturbations_bayes_factors
perturbations_bayes_factors.index.name = 'name'
perturbations_bayes_factors.columns = ['Perturbation_bayes_factor']
print(perturbations_bayes_factors)

# Merge tables
print('Merging tables -> nodes')
nodes = pd.concat([growth, self_interactions, cluster_assignment, perturbations, perturbations_bayes_factors], axis=1)
nodes.to_csv(f'{output_folder}/nodes.tsv', sep='\t')
print(nodes)