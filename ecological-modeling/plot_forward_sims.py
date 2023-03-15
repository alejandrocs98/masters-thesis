#!/bin/python3
# -*- coding: utf-8 -*-
# Author: Alejandro Castellanos

# Usage: python3 plot_forward_sims.py simtype dataset seed
# simtype = [no-module-learning|cluster-learning|fixed-clusters]
# dataset = [LF0 | HF0]
# seed = [0|3|4|23|127]

import mdsine2 as md2
from mdsine2.names import STRNAMES
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from pathlib import Path
import sys

md2.visualization.set_perturbation_color('gray')

# Simulation type
simtype = sys.argv[1]
# Dataset
dataset = sys.argv[2]
# Seed
seed = sys.argv[3]

# Define study path
study_path = Path('/hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/06-mcnulty-datasets')
# Define input paths
fwsim_path = Path(f'/hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference/{simtype}')
filt_path = Path(f'/hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference/{simtype}')
# Define output folder
out_folder = Path(f'/hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference/{simtype}/mcnulty-{dataset}-seed{seed}/abundance-vis')
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
        '#af3261']

pretty_names_dir = {'B_caccae': '$B. caccae$',
                'B_cellulosilyticus_WH2': '$B. cellulosilyticus$',
                'B_ovatus': '$B. ovatus$',
                'B_thetaiotaomicron': '$B. thetaiotaomicron$',
                'B_uniformis': '$B. uniformis$',
                'B_vulgatus': '$B. vulgatus$',
                'C_aerofaciens': '$C. aerofaciens$',
                'C_scindens': '$C. scindens$',
                'C_spiroforme': '$C. spiroforme$',
                'D_longicatena': '$D. longicatena$',
                'P_distasonis': '$P. distasonis$',
                'R_obeum': '$R. obeum$'}

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
        'D_longicatena']

taxa_color = {order: cols[i] for i, order in enumerate(order)}

lf0 = ['1', '2', '3', '4', '5', '6', '7']
hf0 = ['8', '9', '10', '11', '12', '13', '14', '15']

# Define plotting functions
def plot_data_fit_pred_by_subj(study_path, dataset, fwsim_path, seed=0, subj2plot='all', taxa2plot='all', fwsim=True, filt=True, subplots=True, save=True):
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
    if subj2plot != 'all':
        subjs = subj2plot
    if taxa2plot != 'all':
        taxa = taxa2plot
    if fwsim:
        fwsim = [np.load(f'{fwsim_path}/mcnulty-{dataset}-seed{seed}/forward-simulate/Subject_{subj}/fwsim.npy') for subj in subjs]
        start = 0
        step = 0.01
        end = 40
        sim_times = np.arange(start, end+step+step, step)
    if filt:
        filt = [pd.read_table(f'{fwsim_path}/mcnulty-{dataset}-seed{seed}/posteriors/filtering/Subject_{subj}/median.tsv', sep='\t', index_col=0) for subj in subjs]
        filt_times = [filt_subj.T.index.values.astype(float) for filt_subj in filt]
    if subplots:
        fig, axs = plt.subplots(4, 2, figsize=(20, 20))
        row = 0
        col = 0
        for subj in range(len(subjs)):
            for taxon in range(len(taxa[subj])):
                if fwsim:
                    fwsim_mean = fwsim[subj].mean(axis=0)[taxon]
                    fwsim_std = fwsim[subj].mean(axis=0)[taxon]
                    axs[row, col].plot(sim_times, fwsim_mean, color=taxa_color[taxa[subj][taxon]], linewidth=2)
                    axs[row, col].fill_between(sim_times, fwsim_mean-fwsim_std, fwsim_mean+fwsim_std, color=taxa_color[taxa[subj][taxon]], alpha=0.2)
                if filt:
                    axs[row, col].plot(filt_times[subj], filt[subj].iloc[taxon,:].values, marker='x', linestyle='--', linewidth=0.8, color=taxa_color[taxa[subj][taxon]])
                axs[row, col].plot(times[subj], true_abundances[subj][taxon], label=taxa[subj][taxon], marker='.', linestyle='--', linewidth=0.8, color=taxa_color[taxa[subj][taxon]])
                if dataset == 'LF0':
                    axs[row, col].fill_between(x=[14,26], y1=1, y2=1e12, color='grey', alpha=0.2)
                elif dataset == 'HF0':
                    axs[row, col].fill_between(x=[0,12], y1=1, y2=1e12, color='grey', alpha=0.2)
                    axs[row, col].fill_between(x=[28,40], y1=1, y2=1e12, color='grey', alpha=0.2)
                axs[row, col].set_title(f'Subject {subjs[subj]}')
                axs[row, col].set_ylim(1e4, 1e10)
                axs[row, col].set_yscale('log')
            col += 1
            if col == 2:
                col = 0
                row += 1
        handles, labels = axs[0,0].get_legend_handles_labels()
        fig.legend(handles, labels, loc='lower center', ncol=4)
        fig.supxlabel('Time (Days)', y=0.08)
        fig.supylabel('$Log_{10}$ Abundance', x=0.08)
        fig.suptitle(f'Abundance of all members of the community in dataset {dataset}', y=0.92)
        if save:
            plt.savefig(f'{out_folder}/Abundance_subplots.pdf', bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    else:
        for subj in range(len(subjs)):
            for taxon in range(len(taxa[subj])):
                if fwsim:
                    fwsim_mean = fwsim[subj].mean(axis=0)[taxon]
                    fwsim_std = fwsim[subj].mean(axis=0)[taxon]
                    plt.plot(sim_times, fwsim_mean, color=taxa_color[taxa[subj][taxon]], linewidth=2, label='Predicted')
                    plt.fill_between(sim_times, fwsim_mean-fwsim_std, fwsim_mean+fwsim_std, color=taxa_color[taxa[subj][taxon]], alpha=0.2)
                if filt:
                    plt.plot(filt_times[subj], filt[subj].iloc[taxon,:].values, marker='x', linestyle='--', linewidth=0.8, color=taxa_color[taxa[subj][taxon]], label='Filtered')
                plt.plot(times[subj], true_abundances[subj][taxon], label=taxa[subj][taxon], marker='.', linestyle='--', linewidth=0.8, color=taxa_color[taxa[subj][taxon]])
                if dataset == 'LF0':
                    plt.fill_between(x=[14,26], y1=1, y2=1e12, color='grey', alpha=0.2)
                elif dataset == 'HF0':
                    plt.fill_between(x=[0,12], y1=1, y2=1e12, color='grey', alpha=0.2)
                    plt.fill_between(x=[28,40], y1=1, y2=1e12, color='grey', alpha=0.2)
            plt.title(f'Species abundance in dataset {dataset} for subject {subjs[subj]}')
            plt.yscale('log')
            plt.ylim(1e4, 1e10)
            plt.legend()
            plt.xlabel('Time (Days)')
            plt.ylabel('$Log_{10}$ Abundance')
            if save:
                plt.savefig(f'{out_folder}/Abundance_subject{subjs[subj]}.pdf', bbox_inches='tight')
                plt.close()
            else:
                plt.show()

def plot_data_pred_mean(study_path, dataset, fwsim_path, seed=0, taxa2plot='all', points=True, save=True):
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
    if taxa2plot != 'all':
        taxa = taxa2plot
    fwsim = [np.load(f'{fwsim_path}/mcnulty-{dataset}-seed{seed}/forward-simulate/Subject_{subj}/fwsim.npy') for subj in subjs]
    start = 0
    step = 0.01
    end = 40
    sim_times = np.arange(start, end+step+step, step)
    fwsim_mean = np.mean([fwsim[subj].mean(axis=0) for subj in subjs], axis=0)
    fwsim_std = np.std([fwsim[subj].mean(axis=0) for subj in subjs], axis=0)
    for taxon in range(len(taxa[subjs[0]])):
        fwsim_mean = fwsim[taxon]
        fwsim_std = fwsim[taxon]
        plt.plot(sim_times, fwsim_mean, color=taxa_color[taxa[0][taxon]], linewidth=2, legend_label=taxa[0][taxon])
        plt.fill_between(sim_times, fwsim_mean-fwsim_std, fwsim_mean+fwsim_std, color=taxa_color[taxa[0][taxon]], alpha=0.2)
        if points:
            for subj in range(len(subjs)):
                plt.plot(times[subj], true_abundances[subj][taxon], marker='.', linestyle='none', color=taxa_color[taxa[subj][taxon]])
        if dataset == 'LF0':
            plt.fill_between(x=[14,26], y1=1, y2=1e12, color='grey', alpha=0.2)
        elif dataset == 'HF0':
            plt.fill_between(x=[0,12], y1=1, y2=1e12, color='grey', alpha=0.2)
            plt.fill_between(x=[28,40], y1=1, y2=1e12, color='grey', alpha=0.2)
        plt.title(f'Abundance of all members of the community in dataset {dataset}')
        plt.yscale('log')
        plt.ylim(1e4, 1e10)
        plt.legend()
        plt.xlabel('Time (Days)')
        plt.ylabel('$Log_{10}$ Abundance')
    if save:
        plt.savefig(f'{out_folder}/Abundance_mean.pdf', bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_data_pred_mean_area(study_path, dataset, fwsim_path, seed=0, save=True):
    if dataset == 'LF0':
        subjs = lf0
    elif dataset == 'HF0':
        subjs = hf0
    else:
        raise ValueError(f'Unknown dataset: {dataset}')
    study = md2.Study.load(f'{study_path}/{dataset}/mcnulty_{dataset}.pkl')
    taxa = [list(study[subj].taxa.names.keys()) for subj in subjs]
    fwsim = [np.load(f'{fwsim_path}/mcnulty-{dataset}-seed{seed}/forward-simulate/Subject_{subj}/fwsim.npy') for subj in subjs]
    fwsim_mean = np.mean([fwsim[subj].mean(axis=0) for subj in subjs], axis=0)
    area = pd.DataFrame(fwsim_mean.T, columns=taxa[0], index=np.arange(fwsim_mean.shape[1]))
    area.index = area.index*0.01
    area.plot.area(stacked=True, 
        color=cols, 
        rot=0, 
        linewidth=0.3,
        ylim=(1e5, 5.2e8))
    if dataset == 'LF0':
        plt.fill_between(x=[14,26], y1=1, y2=1e12, color='grey', alpha=0.2)
    elif dataset == 'HF0':
        plt.fill_between(x=[0,12], y1=1, y2=1e12, color='grey', alpha=0.2)
        plt.fill_between(x=[28,40], y1=1, y2=1e12, color='grey', alpha=0.2)
    plt.title(f'Abundance of all members of the community in dataset {dataset}')
    plt.yscale('log')
    plt.ylim(1e4, 1e10)
    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left')
    plt.xlabel('Time (Days)')
    plt.ylabel('$Log_{10}$ Abundance')
    if save:
        plt.savefig(f'{out_folder}/Abundance_area.pdf', bbox_inches='tight')
        plt.close()
    else:
        plt.show()

# Call functions
plot_data_fit_pred_by_subj(study_path, dataset, fwsim_path, seed=seed, subj2plot='all', taxa2plot='all', fwsim=True, filt=True, save=True)
plot_data_fit_pred_by_subj(study_path, dataset, fwsim_path, seed=seed, subj2plot='all', taxa2plot='all', fwsim=True, filt=True, subplots=False, save=True)
plot_data_pred_mean(study_path, dataset, fwsim_path, seed=seed, taxa2plot='all', points=True, save=True)
plot_data_pred_mean_area(study_path, dataset, fwsim_path, seed=seed, save=True)