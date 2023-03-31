#!/bin/python3
# -*- coding: utf-8 -*-
# Author: Alejandro Castellanos

# Usage: python3 get_rsme.py simtype dataset intra inter
# simtype = [no-module-learning|cluster-learning|fixed-clusters]
# dataset = [LF0 | HF0]
# intra = [sum|mean]
# inter = [sum|mean]

import numpy as np
import pandas as pd
from pathlib import Path
import sys

# Simulation type
simtype = sys.argv[1]
# Define dataset
dataset = sys.argv[2]

taxa = ['B_caccae',
        'B_cellulosilyticus_WH2',
        'B_ovatus',
        'B_thetaiotaomicron',
        'B_uniformis',
        'B_vulgatus',
        'C_aerofaciens',
        'C_scindens',
        'C_spiroforme',
        # 'D_longicatena',
        'P_distasonis',
        'R_obeum']

input_path = Path('/hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference')
output_path = Path('/hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/09-mdsine2-rhats_and_rsme')
seeds = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 16, 23, 24, 26, 28, 31, 36, 46, 48, 51, 54, 63, 69, 77, 78, 86, 89, 96, 127]

def bayes_factors_scores(simtype, dataset, seeds=seeds):
    if dataset == 'LF0':
        perturbation = 'HF/HS'
    elif dataset == 'HF0':
        perturbation = 'LF/HPP'
    inter_bayes_fact_scores = []
    pertur_bayes_fact_scores = []
    for seed in seeds:
        inter_bayes_fact = pd.read_table(f'{input_path}/{simtype}/mcnulty-{dataset}-seed{seed}/posteriors/interactions/bayes_factors.tsv', sep='\t', index_col=0)
        inter_bayes_fact = inter_bayes_fact.values
        for i in range(len(taxa)):
            for j in range(len(taxa)):
                if (inter_bayes_fact[i,j] > 3) & (inter_bayes_fact[i,j] < 10):
                    inter_bayes_fact[i,j] = 1**2
                elif (inter_bayes_fact[i,j] > 10) & (inter_bayes_fact[i,j] < 100):
                    inter_bayes_fact[i,j] = 2**2
                elif (inter_bayes_fact[i,j] > 100):
                    inter_bayes_fact[i,j] = 3**2
                elif (inter_bayes_fact[i,j] < 1/3) & (inter_bayes_fact[i,j] > 0.1):
                    inter_bayes_fact[i,j] = 1**2
                elif (inter_bayes_fact[i,j] < 0.1) & (inter_bayes_fact[i,j] > 0.01):
                    inter_bayes_fact[i,j] = 2**2
                elif (inter_bayes_fact[i,j] < 0.01):
                    inter_bayes_fact[i,j] = 3**2
                else:
                    inter_bayes_fact[i,j] = 0
        inter_bayes_fact_scores.append(inter_bayes_fact.sum())
        pertur_bayes_fact = pd.read_table(f'{input_path}/{simtype}/mcnulty-{dataset}-seed{seed}/posteriors/{perturbation}/bayes_factors.tsv', sep='\t', index_col=0)
        pertur_bayes_fact = pertur_bayes_fact.values[0]
        for i in range(len(taxa)):
            if (pertur_bayes_fact[i] > 3) & (pertur_bayes_fact[i] < 10):
                pertur_bayes_fact[i] = 1**2
            elif (pertur_bayes_fact[i] > 10) & (pertur_bayes_fact[i] < 100):
                pertur_bayes_fact[i] = 2**2
            elif (pertur_bayes_fact[i] > 100):
                pertur_bayes_fact[i] = 3**2
            elif (pertur_bayes_fact[i] < 1/3) & (pertur_bayes_fact[i] > 0.1):
                pertur_bayes_fact[i] = 1**2
            elif (pertur_bayes_fact[i] < 0.1) & (pertur_bayes_fact[i] > 0.01):
                pertur_bayes_fact[i] = 2**2
            elif (pertur_bayes_fact[i] < 0.01):
                pertur_bayes_fact[i] = 3**2
            else:
                pertur_bayes_fact[i] = 0
        pertur_bayes_fact_scores.append(pertur_bayes_fact.sum())
    table = pd.DataFrame({'seed':seeds, 'inter_bayes_fact_score': inter_bayes_fact_scores, 'pertur_bayes_fact_score': pertur_bayes_fact_scores})
    table.to_csv(f'{output_path}/{simtype}/{dataset}/bayes_factors_scores.tsv', sep='\t', index=False)

bayes_factors_scores(simtype, dataset, seeds=seeds)