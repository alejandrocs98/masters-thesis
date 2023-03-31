#!/bin/python3
# -*- coding: utf-8 -*-
# Author: Alejandro Castellanos

# Usage: python3 create_edges_table.py simtype dataset seed output-folder
# simtype: [no-module-learning | cluster-learning | fixed-clusters]
# dataset: [LF0 | HF0]
# seed: [0 | 3 | 4 | 23 | 127]

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import os
import pandas as pd
from pathlib import Path
import h5py
import arviz as az
import rpy2.robjects as robjects
import sys

cols = [col for i, col in enumerate(cm.tab20b.colors) if i % 4 == 0]
cols = cols + [col for i, col in enumerate(cm.tab20c.colors) if i % 4 == 0]
cols = cols + [col for i, col in enumerate(cm.tab20b.colors) if i % 4 == 1]
cols = cols + [col for i, col in enumerate(cm.tab20c.colors) if i % 4 == 1]
cols = cols + [col for i, col in enumerate(cm.tab20b.colors) if i % 4 == 2]
cols = cols + [col for i, col in enumerate(cm.tab20c.colors) if i % 4 == 2]
cols = cols + [col for i, col in enumerate(cm.tab20b.colors) if i % 4 == 3]
cols = cols + [col for i, col in enumerate(cm.tab20c.colors) if i % 4 == 3]
cols = cols[0:30]

# Define simtype
simtype = sys.argv[1]
# Define dataset
dataset = sys.argv[2]

input_folder = Path(f'/hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference')
output_path = Path(f'/hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/09-mdsine2-rhats_and_rsme')

# Define useful lookup variables
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
                'R_obeum': '$R. obeum$'}

burn_in = 1000
seeds = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 16, 23, 24, 26, 28, 31, 36, 46, 48, 51, 54, 63, 69, 77, 78, 86, 89, 96, 127]

def load_traces(key, simtype, dataset, seeds=seeds, burn_in=burn_in):
    traces = []
    for seed in seeds:
        filename = Path(f'{input_folder}/{simtype}/mcnulty-{dataset}-seed{seed}/traces.hdf5')
        with h5py.File(filename, 'r') as f:
            trace = f[key][()][burn_in:]
            traces.append(trace)
    traces = np.array(traces)
    traces = np.nan_to_num(traces)
    return traces

def save_trace_as_rds(key, simtype, dataset, seeds=seeds, burn_in=burn_in):
    output_folder = Path(f'{output_path}/{simtype}/{dataset}/r-objects')
    output_folder.mkdir(parents=True, exist_ok=True)
    traces = load_traces(key=key, simtype=simtype, dataset=dataset, seeds=seeds, burn_in=burn_in)
    traces_flatten = traces.flatten('F')
    traces2r = robjects.r['array'](robjects.FloatVector(traces_flatten), dim=robjects.IntVector(traces.shape))
    robjects.r['saveRDS'](traces2r, file = f'{output_folder}/{key.replace(" ", "_").replace("/", "_")}.rds')

def plot_forest(key, simtype, dataset, seeds=seeds, burn_in=burn_in):
    traces = load_traces(key=key, simtype=simtype, dataset=dataset, seeds=seeds, burn_in=burn_in)
    plot_path = Path(f'{output_path}/{simtype}/{dataset}/diagnostics')
    plot_path.mkdir(parents=True, exist_ok=True)
    if key in ['Growth parameter', 'Self interaction parameter', 'HF/HS', 'LF/HPP']:
        traces_az = az.convert_to_inference_data(traces)
        axes = az.plot_forest(traces_az, ess=True, r_hat=True, figsize=(14, 8), combined=True, colors='black')
        axes[0].set_title(f'{key} 94% HDI')
        axes[1].set_title(f'{key} ess')
        axes[2].set_title(f'{key} ' '$\hat{r}$')
        plt.savefig(f'{plot_path}/{key.replace(" ", "_").replace("/", "_")}_forest.png', dpi=300)
        plt.close()
    elif key == 'Interactions object':
        for i in range(len(taxa)):
            species1 = taxa[i]
            species2 = taxa.copy()
            species2.pop(i)
            inter = np.ma.array(traces[:,:,i,:], mask=False)
            inter.mask[:,:,i] = True
            inter = inter[~inter.mask].reshape(inter.shape[0], inter.shape[1], -1)
            interactions_az = az.convert_to_inference_data(inter)
            axes = az.plot_forest(interactions_az, ess=True, r_hat=True, figsize=(14, 8), combined=True, colors='black')
            axes[0].set_title(f'{key} 94% HDI')
            axes[1].set_title(f'{key} ess')
            axes[2].set_title(f'{key} ' '$\hat{r}$')
            plt.savefig(f'{plot_path}/{key.replace(" ", "_").replace("/", "_")}_forest_for_{species1}.png', dpi=300)
            plt.close()
    else:
        traces_az = az.convert_to_inference_data(traces)
        axes = az.plot_forest(traces_az, ess=True, r_hat=True, combined=True, colors='black')
        axes[0].set_title(f'{key} 94% HDI')
        axes[1].set_title(f'{key} ess')
        axes[2].set_title(f'{key} ' '$\hat{r}$')
        plt.savefig(f'{plot_path}/{key.replace(" ", "_").replace("/", "_")}_forest.png', dpi=300)
        plt.close()

def plot_rank(key, simtype, dataset, seeds=seeds, burn_in=burn_in):
    traces = load_traces(key=key, simtype=simtype, dataset=dataset, seeds=seeds, burn_in=burn_in)
    plot_path = Path(f'{output_path}/{simtype}/{dataset}/diagnostics')
    plot_path.mkdir(parents=True, exist_ok=True)
    if key in ['Growth parameter', 'Self interaction parameter', 'HF/HS', 'LF/HPP', 'Process Variance parameter']:
        traces_az = az.convert_to_inference_data(traces)
        az.plot_rank(traces_az, colors=cols, figsize=(12, 24), ref_line_kwargs={'lw':0.5})
        plt.savefig(f'{plot_path}/{key.replace(" ", "_").replace("/", "_")}_rank.png', dpi=300)
        plt.close()
    elif key == 'Interactions object':
        for i in range(len(taxa)):
            species1 = taxa[i]
            species2 = taxa.copy()
            species2.pop(i)
            inter = np.ma.array(traces[:,:,i,:], mask=False)
            inter.mask[:,:,i] = True
            inter = inter[~inter.mask].reshape(inter.shape[0], inter.shape[1], -1)
            interactions_az = az.convert_to_inference_data(inter)
            az.plot_rank(interactions_az, colors=cols)
            plt.savefig(f'{plot_path}/{key.replace(" ", "_").replace("/", "_")}_rank_for_{species1}.png', dpi=300)
            plt.close()

def plot_rank_vlines(key, simtype, dataset, seeds=seeds, burn_in=burn_in):
    traces = load_traces(key=key, simtype=simtype, dataset=dataset, seeds=seeds, burn_in=burn_in)
    plot_path = Path(f'{output_path}/{simtype}/{dataset}/diagnostics')
    plot_path.mkdir(parents=True, exist_ok=True)
    if key in ['Growth parameter', 'Self interaction parameter', 'HF/HS', 'LF/HPP', 'Process Variance parameter']:
        traces_az = az.convert_to_inference_data(traces)
        az.plot_rank(traces_az, kind="vlines",
             vlines_kwargs={'lw':0}, marker_vlines_kwargs={'lw':3}, colors=cols)
        plt.savefig(f'{plot_path}/{key.replace(" ", "_").replace("/", "_")}_rank_vlines.png', dpi=300)
        plt.close()
    elif key == 'Interactions object':
        for i in range(len(taxa)):
            species1 = taxa[i]
            species2 = taxa.copy()
            species2.pop(i)
            inter = np.ma.array(traces[:,:,i,:], mask=False)
            inter.mask[:,:,i] = True
            inter = inter[~inter.mask].reshape(inter.shape[0], inter.shape[1], -1)
            interactions_az = az.convert_to_inference_data(inter)
            az.plot_rank(interactions_az, kind="vlines",
             vlines_kwargs={'lw':0}, marker_vlines_kwargs={'lw':3}, colors=cols)
            plt.savefig(f'{plot_path}/{key.replace(" ", "_").replace("/", "_")}_rank_vlines_for_{species1}.png', dpi=300)
            plt.close()

def get_bayesian_summary(key, simtype, dataset, seeds=seeds, burn_in=burn_in):
    traces = load_traces(key=key, simtype=simtype, dataset=dataset, seeds=seeds, burn_in=burn_in)
    out_path = Path(f'{output_path}/{simtype}/{dataset}/diagnostics')
    out_path.mkdir(parents=True, exist_ok=True)
    if key in ['Growth parameter', 'Self interaction parameter', 'HF/HS', 'LF/HPP', 'Process Variance parameter']:
        traces_az = az.convert_to_inference_data(traces)
        summary = az.summary(traces_az)
        if key == 'Process Variance parameter':
            summary.index = ['Process Variance']
        else:
            summary.index = taxa
        summary.to_csv(f'{out_path}/{key.replace(" ", "_").replace("/", "_")}_diag_summary.tsv', sep='\t', index=True)
    elif key == 'Interactions object':
        diagn = []
        for i in range(len(taxa)):
            species2 = taxa.copy()
            species2.pop(i)
            inter = np.ma.array(traces[:,:,i,:], mask=False)
            inter.mask[:,:,i] = True
            inter = inter[~inter.mask].reshape(inter.shape[0], inter.shape[1], -1)
            interactions_az = az.convert_to_inference_data(inter)
            interactions_summary = az.summary(interactions_az)
            interactions_summary.index = species2
            interactions_summary.index.name = 'species2'
            interactions_summary['species1'] = taxa[i]
            interactions_summary.reset_index(inplace=True)
            interactions_summary.set_index(['species1', 'species2'], inplace=True)
            diagn.append(interactions_summary)
        diagn = pd.concat(diagn)
        diagn.to_csv(f'{out_path}/{key.replace(" ", "_").replace("/", "_")}_diag_summary.tsv', sep='\t', index=True)


for key in ['Growth parameter', 'Self interaction parameter', 'Perturbation object', 'Process Variance parameter', 'Interactions object']:
    if (key == 'Perturbation object') & (dataset == 'LF0'):
        key = 'HF/HS'
    elif (key == 'Perturbation object') & (dataset == 'HF0'):
        key = 'LF/HPP'
    save_trace_as_rds(key, simtype, dataset, seeds=seeds, burn_in=burn_in)
    plot_forest(key, simtype, dataset, seeds=seeds, burn_in=burn_in)
    plot_rank(key, simtype, dataset, seeds=seeds, burn_in=burn_in)
    plot_rank_vlines(key, simtype, dataset, seeds=seeds, burn_in=burn_in)
    get_bayesian_summary(key, simtype, dataset, seeds=seeds, burn_in=burn_in)