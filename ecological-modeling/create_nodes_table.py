#!/bin/python3
# -*- coding: utf-8 -*-
# Author: Alejandro Castellanos

# Usage: python3 create_nodes_table.py [growth.tsv] [self_interactions.tsv] [cluster_assignment.tsv] [perturbations.tsv] [perturbations_bayes_factors.tsv] [out-folder]
# posteriors/growth/values.tsv
# posteriors/sel_interactions/values.tsv
# posteriors/clustering/clusterassignment.tsv
# posteriors/perturbation/HS/values.tsv
# posteriors/perturbation/HS/bayes_factors.tsv
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

# Load growth rates table
growth = pd.read_csv(sys.argv[1], sep='\t', index_col=0)
# Load self interactions table
self_interactions = pd.read_csv(sys.argv[2], sep='\t', index_col=0)
# Load cluster assignment table
cluster_assignment = pd.read_csv(sys.argv[3], sep='\t', index_col=0)
# Load perturbations effects table
perturbations = pd.read_csv(sys.argv[4], sep='\t', index_col=0)
# Load perturbations bayes factors table
perturbations_bayes_factors = pd.read_csv(sys.argv[5], sep='\t', index_col=0).T

# Define output folder
out_folder = sys.argv[6]

# Tweak growth rates table
print('Growth rates')
growth = growth.loc[:, ['mean', 'median']].copy()
growth.index.name = 'name'
growth.rename(columns={'mean': 'Growth_mean', 'median': 'Growth_median'}, inplace=True)
growth.drop('mean', axis=0, inplace=True)
print(growth)

# Tweak self interactions table
print('Self interactions')
self_interactions = self_interactions.loc[:, ['mean', 'median']].copy()
self_interactions.index.name = 'name'
self_interactions.rename(columns={'mean': 'Self_interaction_mean', 'median': 'Self_interaction_median'}, inplace=True)
self_interactions.drop('mean', axis=0, inplace=True)
print(self_interactions)

# Tweak cluster assignment table
print('Cluster assignment')
cluster_assignment.columns = ['Cluster']
print(cluster_assignment)

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
nodes.to_csv(f'{out_folder}/nodes.tsv', sep='\t')
print(nodes)