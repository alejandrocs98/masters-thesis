#!/bin/python3
# -*- coding: utf-8 -*-
# Author: Alejandro Castellanos

# Usage: python3 r_hat.py simtype dataset
# simtype = [no-module-learning|cluster-learning|fixed-clusters]
# dataset = [LF0 | HF0]

import mdsine2 as md2
from mdsine2.names import STRNAMES
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import sys

# Define simtype
simtype = sys.argv[1]
# Define dataset
dataset = sys.argv[2]

print(simtype, dataset)

# Define input folder
input_folder = Path(f'/hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference/{simtype}')
# Define output folder
output_folder = Path(f'/hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/09-mdsine2-rhats_and_rsme/{simtype}/{dataset}')
output_folder.mkdir(exist_ok=True, parents=True)

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
seeds = [0, 3, 4, 23, 127]

# Load the chains for each dataset
chains = [pd.read_pickle(f'{input_folder}/mcnulty-{dataset}-seed{seed}/mcmc.pkl') for seed in seeds]

# Calculate the shrink factor for a set of chains for a given variable through a series of windows
def shrink_factor(chains, vname, window=500, save=False):
    r_hat_window = []
    j = 0
    while j < chains[0].n_samples:
        r_hat_window.append(md2.pylab.inference.r_hat(chains, start=j, end=j+window, vname=vname))
        j += window
    if save:
        np.save(f'{output_folder}/{vname}_rhat.npy', np.array(r_hat_window))
    return np.array(r_hat_window)

# Plot the shrink factor for a set of chains for a given variable through a series of windows
def plot_shrink_factor(shrink_factor_vector, chains, vname, layout='overlaped', save=False):
    dataset = chains[0].graph.name.split('_')[0]
    shrink_factors = shrink_factor_vector
    taxa = [chains[0].graph.data.taxa[i].name for i in range(len(chains[0].graph.data.taxa))]
    shape_len = len(shrink_factors.shape)
    shape = shape = shrink_factors.shape[1]
    if shape_len <= 2:
        if layout == 'overlaped':
            fig = plt.figure(figsize=(12, 8))
            for i in range(shrink_factors.shape[1]):
                species = f'{taxa[i].split("_")[0]}. {taxa[i].split("_")[1]}'
                plt.plot(shrink_factors[:,i], alpha=0.8, color=cols[i], label=species)
            plt.xlabel('Window')
            plt.ylabel('Rhat')
            plt.title(f'{dataset} Rhat {chains[0].graph[vname].name}')
            plt.legend()
            plt.grid()
            if save:
                fig.savefig(f'{output_folder}/{vname}_rhat_{layout}.png', dpi=300)
        elif layout == 'mean':
            fig = plt.figure(figsize=(12, 8))
            plt.plot(np.mean(shrink_factors, axis=1))
            plt.xlabel('Window')
            plt.ylabel('Rhat')
            plt.title(f'{dataset} Rhat {chains[0].graph[vname].name}')
            plt.grid()
            if save:
                fig.savefig(f'{output_folder}/{vname}_rhat_{layout}.png', dpi=300)
        elif layout == 'subplots':
            fig, ax = plt.subplots(4,3, figsize=(12, 16), sharex=True, sharey=True)
            row=0
            col=0
            for i in range(shape):
                species = f'{taxa[i].split("_")[0]}. {taxa[i].split("_")[1]}'
                ax[row,col].plot(shrink_factors[:, i])
                ax[row,col].set_title(f'${species}$')
                ax[row,col].grid()
                col += 1
                if col == 3:
                    col = 0
                    row += 1
            fig.supxlabel('Window', y=0.08)
            fig.supylabel('Rhat', x=0.08)
            fig.suptitle(f'{dataset} Rhat {chains[0].graph[vname].name}', y=0.92)
            if save:
                fig.savefig(f'{output_folder}/{vname}_rhat_{layout}.png', dpi=300)
    else:
        if layout == 'overlaped':
            fig = plt.figure(figsize=(12, 8))
            for i in range(shape):
                species = f'{taxa[i].split("_")[0]}. {taxa[i].split("_")[1]}'
                for j in range(shape):
                    if j == 0:
                        plt.plot(shrink_factors[:,i,j], alpha=0.8, color=cols[i], label=species)
                    else:
                        plt.plot(shrink_factors[:,i,j], alpha=0.8, color=cols[i])
            plt.xlabel('Window')
            plt.ylabel('Rhat')
            plt.title(f'{dataset} Rhat {chains[0].graph[vname].name}')
            plt.legend()
            plt.grid()
            if save:
                fig.savefig(f'{output_folder}/{vname}_rhat_{layout}.png', dpi=300)
        elif layout == 'mean':
            fig = plt.figure(figsize=(12, 8))
            for i in range(shape):
                species = f'{taxa[i].split("_")[0]}. {taxa[i].split("_")[1]}'
                plt.plot(np.nanmean(shrink_factors, axis=1)[:,i], alpha=0.8, color=cols[i], label=species)
            plt.legend()
            plt.xlabel('Window')
            plt.ylabel('Rhat')
            plt.title(f'{dataset} Rhat {chains[0].graph[vname].name}')
            plt.grid()
            if save:
                plt.savefig(f'{output_folder}/{vname}_rhat_{layout}.png', dpi=300)
        elif layout == 'subplots':
            fig, ax = plt.subplots(4,3, figsize=(12, 16), sharex=True, sharey=True)
            row=0
            col=0
            for i in range(shape):
                species_tit = f'{taxa[i].split("_")[0]}. {taxa[i].split("_")[1]}'
                for j in range(shape):
                    species = f'{taxa[j].split("_")[0]}. {taxa[j].split("_")[1]}'
                    ax[row,col].plot(shrink_factors[:, i, j], color=cols[j], alpha=0.8, label=species)
                ax[row,col].set_title(f'${species_tit}$')
                ax[row,col].grid()
                col += 1
                if col == 3:
                    col = 0
                    row += 1
            handles, labels = ax[0,0].get_legend_handles_labels()
            fig.legend(handles, labels, loc='lower center', ncol=4)
            fig.supxlabel('Window', y=0.08)
            fig.supylabel('Rhat', x=0.08)
            fig.suptitle(f'{dataset} Rhat {chains[0].graph[vname].name}', y=0.92)
            if save:
                fig.savefig(f'{output_folder}/{vname}_rhat_{layout}.png', dpi=300)
    return fig


# Get the shrink factor for all the variables
for vname in [STRNAMES.GROWTH_VALUE, STRNAMES.SELF_INTERACTION_VALUE, STRNAMES.INTERACTIONS_OBJ]:
    print(f'Start shrink factor calculation for {vname}')
    shrink_factor_vector = shrink_factor(chains=chains, vname=vname, window=100, save=True)
    for layout in ['overlaped', 'mean', 'subplots']:
        print(f'Plot shrink factor with layout {layout}')
        plot_shrink_factor(shrink_factor_vector=shrink_factor_vector, chains=chains, vname=vname, layout=layout, save=True)
    print('Finish')
