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


# Define input folder
input_folder = Path(f'/hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference')
#Define output folder
output_folder = input_folder

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

input_folder = Path(f'/hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/08-mdsine2-inference')
output_path = Path(f'/hpcfs/home/ciencias_biologicas/a.castellanoss/masters-thesis/data/09-mdsine2-rhats_and_rsme')

def plot_species_posteriors(parameter, simtype, dataset, seeds=[0, 3, 4, 23, 127], step=1, start=0, end=25000, burn_in=1000):
    param = []
    pretty_taxa = [x if x not in pretty_names_dir else pretty_names_dir[x] for x in taxa]
    for seed in seeds:
        filename = input_folder / f'{simtype}/mcnulty-{dataset}-seed{seed}/traces.hdf5'
        with h5py.File(filename, "r") as f:
            print(parameter)
            param.append(f[parameter][()][burn_in:])
    param = np.array(param)

    name = parameter.replace(' ', '_')
    if (parameter == 'HF/HS') | (parameter == 'LF/HPP'):
        name='Perturbation_parameter'

    steps = np.arange(start+burn_in, end, step)

    for species in range(param[0].shape[1]):
        fig, axs = plt.subplots(1, 2, figsize=(12, 5))
        col = 0
        for seed in range(param.shape[0]):
            axs[0].hist(param[seed][:, species], bins=100, alpha=0.6, label=f'Seed {seeds[seed]}', color=cols[col])
            axs[1].scatter(steps, param[seed][:, species], s=0.4, alpha=0.6, label=f'Seed {seeds[seed]}', color=cols[col])
            col += 1
        axs[0].set_xlabel(f'{parameter} parameter value')
        axs[0].set_ylabel(f'Frequency')
        axs[1].set_xlabel(f'Step')
        axs[1].set_ylabel(f'{parameter} parameter value')
        fig.suptitle(f'{pretty_taxa[species]} {parameter} posteriors', y=0.94)
        handles, labels = axs[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc='lower center', ncol=9, bbox_to_anchor=(0.5, -0.2))

        output_folder = Path(f'{output_path}/{simtype}/{dataset}/posteriors/{name}')
        output_folder.mkdir(exist_ok=True, parents=True)
        fig.savefig(f'{output_folder}/{name}_{taxa[species]}.png', bbox_inches='tight')
        plt.close()

def plot_species_mean_posteriors(parameter, simtype, dataset, seeds=[0, 3, 4, 23, 127], step=1, start=0, end=25000, burn_in=1000):
    param = []
    for seed in seeds:
        filename = input_folder / f'{simtype}/mcnulty-{dataset}-seed{seed}/traces.hdf5'
        with h5py.File(filename, "r") as f:
            print(parameter)
            param.append(f[parameter][()][burn_in:])
    param = np.array(param)
    param = np.nanmean(param, axis=2)

    name = parameter.replace(' ', '_')
    if (parameter == 'HF/HS') | (parameter == 'LF/HPP'):
        name='Perturbation_parameter'

    steps = np.arange(start+burn_in, end, step)

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    col = 0
    for seed in range(param.shape[0]):
        axs[0].hist(param[seed], bins=100, alpha=0.6, label=f'Seed {seeds[seed]}', color=cols[col])
        axs[1].scatter(steps, param[seed], s=0.4, alpha=0.6, label=f'Seed {seeds[seed]}', color=cols[col])
        col += 1
    axs[0].set_xlabel(f'{parameter} parameter value')
    axs[0].set_ylabel(f'Frequency')
    axs[1].set_xlabel(f'Step')
    axs[1].set_ylabel(f'{parameter} parameter value')
    fig.suptitle(f'Mean {parameter} posteriors', y=0.94)
    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=9, bbox_to_anchor=(0.5, -0.2))
    
    output_folder = Path(f'{output_path}/{simtype}/{dataset}/posteriors/{name}')
    output_folder.mkdir(exist_ok=True, parents=True)
    fig.savefig(f'{output_folder}/{name}_mean.png', bbox_inches='tight')
    plt.close()

def plot_interaction_posteriors(simtype, dataset, seeds=[0, 3, 4, 23, 127], step=1, start=0, end=25000, burn_in=1000):
    parameter = 'Interactions object'
    param = []
    pretty_taxa = [x if x not in pretty_names_dir else pretty_names_dir[x] for x in taxa]
    for seed in seeds:
        filename = input_folder / f'{simtype}/mcnulty-{dataset}-seed{seed}/traces.hdf5'
        with h5py.File(filename, "r") as f:
            print(parameter)
            param.append(f[parameter][()][burn_in:])
    param = np.array(param)
    param = np.nan_to_num(param)

    steps = np.arange(start+burn_in, end, step)

    for species1 in range(param[0].shape[1]):
        for species2 in range(param[0].shape[1]):
            fig, axs = plt.subplots(1, 2, figsize=(12, 5))
            col = 0
            for seed in range(param.shape[0]):
                axs[0].hist(param[seed][:, species1, species2], bins=100, alpha=0.6, label=f'Seed {seeds[seed]}', color=cols[col])
                axs[1].scatter(steps, param[seed][:, species1, species2], s=0.4, alpha=0.6, label=f'Seed {seeds[seed]}', color=cols[col])
                col += 1
            axs[0].set_xlabel(f'{parameter} parameter value')
            axs[0].set_ylabel(f'Frequency')
            axs[1].set_xlabel(f'Step')
            axs[1].set_ylabel(f'{parameter} parameter value')
            fig.suptitle(f'{pretty_taxa[species1]}-{pretty_taxa[species2]} {parameter} posteriors', y=0.94)
            handles, labels = axs[0].get_legend_handles_labels()
            fig.legend(handles, labels, loc='lower center', ncol=9, bbox_to_anchor=(0.5, -0.2))

            output_folder = Path(f'{output_path}/{simtype}/{dataset}/posteriors/{parameter.replace(" ", "_")}')
            output_folder.mkdir(exist_ok=True, parents=True)
            fig.savefig(f'{output_folder}/{parameter.replace(" ", "_")}_{taxa[species1]}_{taxa[species2]}.png', bbox_inches='tight')
            plt.close()

def plot_interaction_mean_posteriors(simtype, dataset, seeds=[0, 3, 4, 23, 127], step=1, start=0, end=25000, burn_in=1000):
    parameter = 'Interactions object'
    param = []
    for seed in seeds:
        filename = input_folder / f'{simtype}/mcnulty-{dataset}-seed{seed}/traces.hdf5'
        with h5py.File(filename, "r") as f:
            print(parameter)
            param.append(f[parameter][()][burn_in:])
    param = np.array(param)
    param = np.nanmean(np.nanmean(param, axis=2), axis=2)

    steps = np.arange(start+burn_in, end, step)

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    col = 0
    for seed in range(param.shape[0]):
        axs[0].hist(param[seed], bins=100, alpha=0.6, label=f'Seed {seeds[seed]}', color=cols[col])
        axs[1].scatter(steps, param[seed], s=0.4, alpha=0.6, label=f'Seed {seeds[seed]}', color=cols[col])
        col += 1
    axs[0].set_xlabel(f'{parameter} parameter value')
    axs[0].set_ylabel(f'Frequency')
    axs[1].set_xlabel(f'Step')
    axs[1].set_ylabel(f'{parameter} parameter value')
    fig.suptitle(f'Mean {parameter} posteriors', y=0.94)
    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=9, bbox_to_anchor=(0.5, -0.2))
    
    output_folder = Path(f'{output_path}/{simtype}/{dataset}/posteriors/{parameter.replace(" ", "_")}')
    output_folder.mkdir(exist_ok=True, parents=True)
    fig.savefig(f'{output_folder}/{parameter.replace(" ", "_")}_mean.png', bbox_inches='tight')
    plt.close()

def plot_process_variance_posteriors(simtype, dataset, seeds=[0, 3, 4, 23, 127], step=1, start=0, end=25000, burn_in=1000):
    parameter = 'Process Variance parameter'
    param = []
    for seed in seeds:
        filename = input_folder / f'{simtype}/mcnulty-{dataset}-seed{seed}/traces.hdf5'
        with h5py.File(filename, "r") as f:
            print(parameter)
            param.append(f[parameter][()][burn_in:])
    param = np.array(param)

    steps = np.arange(start+burn_in, end, step)

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    col = 0
    for seed in range(param.shape[0]):
        axs[0].hist(param[seed], bins=100, alpha=0.6, label=f'Seed {seeds[seed]}', color=cols[col])
        axs[1].scatter(steps, param[seed], s=0.4, alpha=0.6, label=f'Seed {seeds[seed]}', color=cols[col])
        col += 1
    axs[0].set_xlabel(f'{parameter} parameter value')
    axs[0].set_ylabel(f'Frequency')
    axs[1].set_xlabel(f'Step')
    axs[1].set_ylabel(f'{parameter} parameter value')
    fig.suptitle(f'{parameter} posteriors', y=0.94)
    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=9, bbox_to_anchor=(0.5, -0.2))

    output_folder = Path(f'{output_path}/{simtype}/{dataset}/posteriors/{parameter.replace(" ", "_")}')
    output_folder.mkdir(exist_ok=True, parents=True)
    fig.savefig(f'{output_folder}/{parameter.replace(" ", "_")}.png', bbox_inches='tight')
    plt.close()

seeds = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 16, 23, 24, 26, 28, 31, 36, 46, 48, 51, 54, 63, 69, 77, 78, 86, 89, 96, 127]

for parameter in ['Growth parameter', 'Self interaction parameter', 'Perturbation object']:
    if (parameter == 'Perturbation object') & (dataset == 'LF0'):
        parameter = 'HF/HS'
    elif (parameter == 'Perturbation object') & (dataset == 'HF0'):
        parameter = 'LF/HPP'
    plot_species_posteriors(parameter, simtype, dataset, seeds=seeds, step=1, start=0, end=25000, burn_in=1000)
    plt.close()
    plot_species_mean_posteriors(parameter, simtype, dataset, seeds=seeds, step=1, start=0, end=25000, burn_in=1000)
    plt.close()

plot_interaction_posteriors(simtype, dataset, seeds=seeds, step=1, start=0, end=25000, burn_in=1000)
plt.close()
plot_interaction_mean_posteriors(simtype, dataset, seeds=seeds, step=1, start=0, end=25000, burn_in=1000)
plt.close()

plot_process_variance_posteriors(simtype, dataset, seeds=seeds, step=1, start=0, end=25000, burn_in=1000)
plt.close()