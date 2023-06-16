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
input_folder = Path(f'/hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference')
#Define output folder
output_folder = input_folder

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

lf0 = ['1', '2', '3', '4', '5', '6', '7']
hf0 = ['8', '9', '10', '11', '12', '13', '14', '15']

taxa_color = {order: cols[i] for i, order in enumerate(order)}
taxa_color

def filter_sims(x):
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            if (x[i,j].max() > 1e10) | (x[i,j].min() < 1e3):
                x[i,j] = np.nan
    return x

def plot_forward_sims_by_ind(simtype, dataset, seed, taxa2plot='all', true_data=True, filt_data=False, save=False):
    if dataset == 'LF0':
        subjs = lf0
    elif dataset == 'HF0':
        subjs = hf0
    else:
        raise ValueError(f'Unknown dataset: {dataset}')
    study = md2.Study.load(f'/hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/06-mcnulty-datasets/{dataset}/mcnulty_{dataset}.pkl')
    true_abundances = [study[subj].matrix()['abs'] for subj in subjs]
    times = [study[subj].times for subj in subjs]
    taxa = [list(study[subj].taxa.names.keys()) for subj in subjs]
    fwsim = [np.load(f'{input_folder}/{simtype}/mcnulty-{dataset}-seed{seed}/forward-simulate/Subject_{subj}/fwsim.npy') for subj in subjs]
    fwsim_filt = [filter_sims(fwsim[subj]) for subj in range(len(subjs))]
    start = 0
    step = 0.01
    end = 40
    sim_times = np.arange(start, end+step+step, step)
    if filt_data:
        filt = [pd.read_table(f'{input_folder}/{simtype}/mcnulty-{dataset}-seed{seed}/posteriors/filtering/Subject_{subj}/median.tsv', index_col=0) for subj in subjs]
        filt_times = [filt[subj].T.index.values.astype(float) for subj in range(len(subjs))]
    fig, axs = plt.subplots(4, 2, figsize=(20, 20))
    row = 0
    col = 0
    for subj in range(len(subjs)):
        if taxa2plot == 'all':
            taxa2plot = taxa[subj]
            out_name = 'all'
        else:
            out_name = '_'.join(taxa2plot)
        for i, j in enumerate(taxa[subj]):
            if j in taxa2plot:
                taxon = i
            else:
                continue
            if true_data:
                axs[row,col].plot(times[subj], true_abundances[subj][taxon,:], color=taxa_color[taxa[subj][taxon]], marker='x', linestyle=':')
            if filt_data:
                axs[row,col].plot(filt_times[subj], filt[subj].T[taxa[subj][taxon]], color=taxa_color[taxa[subj][taxon]], marker='.', linestyle='--')
            fwsim_mean = np.nanmean(fwsim_filt[subj], axis=0)[taxon]
            fwsim_std = np.nanstd(fwsim_filt[subj], axis=0)[taxon]
            axs[row,col].plot(sim_times, fwsim_mean, color=taxa_color[taxa[subj][taxon]], linewidth=2, label=f'{taxa[subj][taxon]}')
            axs[row,col].fill_between(sim_times, fwsim_mean-fwsim_std, fwsim_mean+fwsim_std, color=taxa_color[taxa[subj][taxon]], alpha=0.2)
        if dataset == 'LF0':
            axs[row,col].fill_between(x=[13,27], y1=1, y2=1e12, color='grey', alpha=0.2)
        elif dataset == 'HF0':
            axs[row,col].fill_between(x=[0,13], y1=1, y2=1e12, color='grey', alpha=0.2)
            axs[row,col].fill_between(x=[27,40], y1=1, y2=1e12, color='grey', alpha=0.2)
        axs[row,col].set_title(f'Subject {subjs[subj]}')
        axs[row,col].set_yscale('log')
        axs[row,col].set_ylim([1e4, 1e9])
        fig.suptitle(f'Forward Simulation of species trajectories for subjects in {dataset} dataset', y=0.92)
        fig.supxlabel('Time (days)', y=0.075)
        fig.supylabel('$\log_{10}$ Abundance', x=0.075)
        handles, labels = axs[0,0].get_legend_handles_labels()
        pretty_labels = [x if x not in pretty_names_dir else pretty_names_dir[x] for x in labels]
        fig.legend(handles, pretty_labels, loc='lower center', ncol=4)
        col += 1
        if col == 2:
            col = 0
            row += 1
    if save:
        fig.savefig(f'{output_folder}/{simtype}/mcnulty-{dataset}-seed{seed}/forward-simulate/forward_simulation_byind_{out_name}.pdf', bbox_inches='tight')
        plt.close()
    else:
        return fig, axs
    
def plot_forward_sims_for_inds(simtype, dataset, seed, taxa2plot='all', true_data=True, filt_data=False, save=False):
    if dataset == 'LF0':
        subjs = lf0
    elif dataset == 'HF0':
        subjs = hf0
    else:
        raise ValueError(f'Unknown dataset: {dataset}')
    study = md2.Study.load(f'/hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/06-mcnulty-datasets/{dataset}/mcnulty_{dataset}.pkl')
    true_abundances = [study[subj].matrix()['abs'] for subj in subjs]
    times = [study[subj].times for subj in subjs]
    taxa = [list(study[subj].taxa.names.keys()) for subj in subjs]
    fwsim = [np.load(f'{input_folder}/{simtype}/mcnulty-{dataset}-seed{seed}/forward-simulate/Subject_{subj}/fwsim.npy') for subj in subjs]
    fwsim_filt = [filter_sims(fwsim[subj]) for subj in range(len(subjs))]
    start = 0
    step = 0.01
    end = 40
    sim_times = np.arange(start, end+step+step, step)
    # Aggregate
    taxa = taxa[0]
    fwsim_filt_agg = np.concatenate(fwsim_filt)
    if filt_data:
        filt = [pd.read_table(f'{input_folder}/{simtype}/mcnulty-{dataset}-seed{seed}/posteriors/filtering/Subject_{subj}/median.tsv', index_col=0) for subj in subjs]
        filt_times = [filt[subj].T.index.values.astype(float) for subj in range(len(subjs))]
    fig, ax = plt.subplots(figsize=(10, 6))
    if taxa2plot == 'all':
        taxa2plot = taxa
        out_name = 'all'
    else:
        out_name = '_'.join(taxa2plot)
    for i, j in enumerate(taxa):
        if j in taxa2plot:
            taxon = i
        else:
            continue
        if true_data:
            for subj in range(len(subjs)):
                ax.plot(times[subj], true_abundances[subj][taxon,:], color=taxa_color[taxa[taxon]], marker='x', linestyle='')
        if filt_data:
            for subj in range(len(subjs)):
                ax.plot(filt_times[subj], filt[subj].T[taxa[subj][taxon]], color=taxa_color[taxa[taxon]], marker='.', linestyle='')
        fwsim_mean = np.nanmean(fwsim_filt_agg, axis=0)[taxon]
        fwsim_std = np.nanstd(fwsim_filt_agg, axis=0)[taxon]
        ax.plot(sim_times, fwsim_mean, color=taxa_color[taxa[taxon]], linewidth=2, label=f'{taxa[taxon]}')
        ax.fill_between(sim_times, fwsim_mean-fwsim_std, fwsim_mean+fwsim_std, color=taxa_color[taxa[taxon]], alpha=0.2)
    if dataset == 'LF0':
        ax.fill_between(x=[14,26], y1=1, y2=1e12, color='grey', alpha=0.2)
    elif dataset == 'HF0':
        ax.fill_between(x=[0,14], y1=1, y2=1e12, color='grey', alpha=0.2)
        ax.fill_between(x=[26,40], y1=1, y2=1e12, color='grey', alpha=0.2)
    ax.set_yscale('log')
    ax.set_ylim([1e4, 1e9])
    ax.set_xlabel('Time (days)')
    ax.set_ylabel('$\log_{10}$ Abundance')
    handles, labels = ax.get_legend_handles_labels()
    ax.set_title(f'Forward Simulation of species trajectories for subjects in {dataset} dataset')
    handles, labels = ax.get_legend_handles_labels()
    pretty_labels = [x if x not in pretty_names_dir else pretty_names_dir[x] for x in labels]
    ax.legend(handles, pretty_labels, bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0., fontsize=12)
    if save:
        fig.savefig(f'{output_folder}/{simtype}/mcnulty-{dataset}-seed{seed}/forward-simulate/forward_simulation_{out_name}.pdf', bbox_inches='tight')
        plt.close()
    else:
        return fig, ax
    

# Function calling
plot_forward_sims_by_ind(simtype, dataset, seed, taxa2plot='all', true_data=False, filt_data=False, save=True)
plt.close()
plot_forward_sims_by_ind(simtype, dataset, seed, taxa2plot=['B_caccae', 'B_cellulosilyticus_WH2', 'B_ovatus', 'P_distasonis'], true_data=True, filt_data=False, save=True)
plt.close()
plot_forward_sims_by_ind(simtype, dataset, seed, taxa2plot=['R_obeum', 'C_aerofaciens', 'C_scindens', 'C_spiroforme'], true_data=True, filt_data=False, save=True)
plt.close()
plot_forward_sims_by_ind(simtype, dataset, seed, taxa2plot=['B_uniformis', 'B_thetaiotaomicron', 'B_vulgatus'], true_data=True, filt_data=False, save=True)
plt.close()
plot_forward_sims_for_inds(simtype, dataset, seed, taxa2plot='all', true_data=False, filt_data=False, save=True)
plt.close()
plot_forward_sims_for_inds(simtype, dataset, seed, taxa2plot=['B_caccae', 'B_cellulosilyticus_WH2', 'B_ovatus', 'P_distasonis'], true_data=True, filt_data=False, save=True)
plt.close()
plot_forward_sims_for_inds(simtype, dataset, seed, taxa2plot=['R_obeum', 'C_aerofaciens', 'C_scindens', 'C_spiroforme'], true_data=True, filt_data=False, save=True)
plt.close()
plot_forward_sims_for_inds(simtype, dataset, seed, taxa2plot=['B_uniformis', 'B_thetaiotaomicron', 'B_vulgatus'], true_data=True, filt_data=False, save=True)
plt.close()