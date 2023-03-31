#!/bin/python3
# -*- coding: utf-8 -*-
# Author: Alejandro Castellanos

# Usage: python3 get_rsme.py simtype dataset intra inter
# simtype = [no-module-learning|cluster-learning|fixed-clusters]
# dataset = [LF0 | HF0]
# intra = [sum|mean]
# inter = [sum|mean]

import mdsine2 as md2
from mdsine2.names import STRNAMES
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from pathlib import Path
from sklearn.metrics import mean_squared_error
import sys

md2.visualization.set_perturbation_color('gray')

# Simulation type
simtype = sys.argv[1]
# Define dataset
dataset = sys.argv[2]
# Define intra
intra = sys.argv[3]
# Define inter
inter = sys.argv[4]

# Define study path
study_path = Path(f'/hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/06-mcnulty-datasets')
# Define input paths
fwsim_path = Path(f'/hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference/{simtype}')
filt_path = Path(f'/hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference/{simtype}')
# Define output folder
out_folder = Path(f'/hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/09-mdsine2-rhats_and_rsme/{simtype}/{dataset}')
out_folder.mkdir(parents=True, exist_ok=True)

# Define useful lookup variables
cols = ['#016bff',
        '#b91f1c',
        '#308937',
        '#ff8137',
        '#6f4fc7',
        '#d4b300',
        '#893a2b',
        '#ff6c79',
        '#16c4ff',
        '#766f41',
        '#00c800',
        # '#af3261'
        ]

pretty_names_dir = {'B_caccae': '$B. caccae$',
                'B_cellulosilyticus_WH2': '$B. cellulosilyticus$',
                'B_ovatus': '$B. ovatus$',
                'B_thetaiotaomicron': '$B. thetaiotaomicron$',
                'B_uniformis': '$B. uniformis$',
                'B_vulgatus': '$B. vulgatus$',
                'C_aerofaciens': '$C. aerofaciens$',
                'C_scindens': '$C. scindens$',
                'C_spiroforme': '$C. spiroforme$',
                # 'D_longicatena': '$D. longicatena$',
                'P_distasonis': '$P. distasonis$',
                'R_obeum': '$R. obeum$'
                }

order = ['B_cellulosilyticus_WH2', 
        'B_caccae', 
        'B_vulgatus', 
        'B_thetaiotaomicron', 
        'B_ovatus', 
        'R_obeum', 
        'B_uniformis', 
        'P_distasonis', 
        'C_scindens', 
        'C_aerofaciens', 
        'C_spiroforme', 
        # 'D_longicatena'
        ]

taxa_color = {order: cols[i] for i, order in enumerate(order)}

lf0 = ['1', '2', '3', '4', '5', '6', '7']
hf0 = ['8', '9', '10', '11', '12', '13', '14', '15']

# Define RSME functions
def rsme_fwrsim(study_path, dataset, fwsim_path, seed):
    if dataset == 'LF0':
        subjs = lf0
    elif dataset == 'HF0':
        subjs = hf0
    else:
        raise ValueError(f'Unknown dataset: {dataset}')
    study = md2.Study.load(f'{study_path}/{dataset}/mcnulty_{dataset}.pkl')
    true_abundances = [study[subj].matrix()['abs'] for subj in subjs]
    times = [study[subj].times for subj in subjs]
    taxa = [list(study[subj].taxa.names.keys()) for subj in subjs]
    fwsims = [np.mean(np.load(f'{fwsim_path}/mcnulty-{dataset}-seed{seed}/forward-simulate/Subject_{subj}/fwsim.npy'), axis=0) for subj in subjs]
    start = 0
    step = 0.01
    end = 40
    sim_times = np.arange(start, end+step+step, step)
    if len(true_abundances) != len(fwsims):
        raise ValueError('The number of true abundances and forward simulations are not the same')
    rmse_inds = {}
    for subj in range(len(true_abundances)):
        ext_indx_sim = [np.where(sim_times == obs_times)[0][0] for obs_times in times[subj]]
        rsme_taxa = {}
        for taxon in range(len(taxa[subj])):
            rsme_taxa[taxa[subj][taxon]] = np.sqrt(mean_squared_error(true_abundances[subj][taxon], fwsims[subj][taxon][ext_indx_sim]))
        rmse_inds[subjs[subj]] = rsme_taxa
    return rmse_inds

def rsme_fwrsim_seed(study_path, dataset, fwsim_path, seeds=[0, 3, 4, 23, 127], intra='sum', inter='sum', save=True):
    rsme_seeds = {}
    for seed in seeds:
        rmse_inds = rsme_fwrsim(study_path, dataset, fwsim_path, seed)
        rsmes_subj_agg = []
        if intra == 'sum':
            for subj in rmse_inds.keys():
                rsmes_subj_agg.append(np.sum(list(rmse_inds[subj].values())))
        elif intra == 'mean':
            for subj in rmse_inds.keys():
                rsmes_subj_agg.append(np.mean(list(rmse_inds[subj].values())))
        else:
            raise ValueError(f'Unknown intra: {intra}')
        if inter == 'sum':
            rmse_inds_agg = np.sum(rsmes_subj_agg)
        elif inter == 'mean':
            rmse_inds_agg = np.mean(rsmes_subj_agg)
        else:
            raise ValueError(f'Unknown inter: {inter}')
        rsme_seeds[seed] = rmse_inds_agg
    rsme_table = pd.DataFrame.from_dict(rsme_seeds, orient='index', columns=['RMSE'])
    rsme_table.index.name = 'Seed'
    if save:
        rsme_table.to_csv(f'{out_folder}/rmse_fwrsim_intra{intra}_inter{inter}.tsv', sep='\t')
    return rsme_table

def rsme_filtering(study_path, dataset, filt_path, seed):
    if dataset == 'LF0':
        subjs = lf0
    elif dataset == 'HF0':
        subjs = hf0
    else:
        raise ValueError(f'Unknown dataset: {dataset}')
    study = md2.Study.load(f'{study_path}/{dataset}/mcnulty_{dataset}.pkl')
    true_abundances = [study[subj].matrix()['abs'] for subj in subjs]
    times = [study[subj].times for subj in subjs]
    taxa = [list(study[subj].taxa.names.keys()) for subj in subjs]
    filt = [pd.read_table(f'{filt_path}/mcnulty-{dataset}-seed{seed}/posteriors/filtering/Subject_{subj}/median.tsv', index_col=0, sep='\t') for subj in subjs]
    filt_times = [filt_subj.T.index.values for filt_subj in filt]
    if len(true_abundances) != len(filt):
        raise ValueError('The number of true abundances and filtering are not the same')
    rmse_inds = {}
    for subj in range(len(true_abundances)):
        if len(times[subj]) != len(filt_times[subj]):
            filt[subj] = filt[subj].loc[:, times[subj].astype(str)]
        rsme_taxa = {}
        for taxon in range(len(taxa[subj])):
            rsme_taxa[taxa[subj][taxon]] = np.sqrt(mean_squared_error(true_abundances[subj][taxon], filt[subj].iloc[taxon,:].values))
        rmse_inds[subjs[subj]] = rsme_taxa
    return rmse_inds

def rsme_filtering_seed(study_path, dataset, filt_path, seeds=[0, 3, 4, 23, 127], intra='sum', inter='sum', save=True):
    rsme_seeds = {}
    for seed in seeds:
        rmse_inds = rsme_filtering(study_path, dataset, filt_path, seed)
        rsmes_subj_agg = []
        if intra == 'sum':
            for subj in rmse_inds.keys():
                rsmes_subj_agg.append(np.sum(list(rmse_inds[subj].values())))
        elif intra == 'mean':
            for subj in rmse_inds.keys():
                rsmes_subj_agg.append(np.mean(list(rmse_inds[subj].values())))
        else:
            raise ValueError(f'Unknown intra: {intra}')
        if inter == 'sum':
            rmse_inds_agg = np.sum(rsmes_subj_agg)
        elif inter == 'mean':
            rmse_inds_agg = np.mean(rsmes_subj_agg)
        else:
            raise ValueError(f'Unknown inter: {inter}')
        rsme_seeds[seed] = rmse_inds_agg
    rsme_table = pd.DataFrame.from_dict(rsme_seeds, orient='index', columns=['RMSE'])
    rsme_table.index.name = 'Seed'
    if save:
        rsme_table.to_csv(f'{out_folder}/rmse_filt_intra{intra}_inter{inter}.tsv', sep='\t')
    return rsme_table

seeds = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 16, 23, 24, 26, 28, 31, 36, 46, 48, 51, 54, 63, 69, 77, 78, 86, 89, 96, 127]

# Calling the functions
rsme_fwrsim_seed(study_path, dataset, fwsim_path, seeds=seeds, intra=intra, inter=inter, save=True)
# rsme_filtering_seed(study_path, dataset, filt_path, seeds=seeds, intra=intra, inter=inter, save=True)