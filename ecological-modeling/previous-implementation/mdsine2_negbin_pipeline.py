#!/bin/python3
# -*- coding: utf-8 -*-
# Author: Alejandro Castellanos

# Usage: python3 mdsine2_negbin_pipeline.py [dataset] [seed]

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

md2.visualization.set_perturbation_color('gray')
cols = [cm.tab10(i) for i in range(10)]
cols.append(cm.Set2(5))
cols.append(cm.Paired(4))

if len(sys.argv) == 1:
    dataset = 'LF0'
    seed = 0
    print(f'Using {dataset} dataset and seed {seed}')
elif len(sys.argv) == 2:
    dataset = 'LF0'
    seed = int(sys.argv[1])
    print(f'Using {dataset} dataset and seed {seed}')
elif len(sys.argv) == 3:
    dataset = str(sys.argv[1])
    if dataset not in ['LF0', 'HF0']:
        raise ValueError(f'Invalid dataset {dataset}')
    seed = int(sys.argv[2])
    print(f'Using {dataset} dataset and seed {seed}')
else:
    raise ValueError('Too many arguments')

burnin = 5000
n_samples = 100000
checkpoint = 500

# Define the input directory
input_dir = Path(f'mcnulty-datasets/{dataset}')
# Define the output directory
output_dir = Path(f'mcnulty-results/{dataset}')
output_dir.mkdir(parents=True, exist_ok=True)
# Define negbin directory
negbin_dir = Path(f'{output_dir}/negbin')
negbin_dir.mkdir(parents=True, exist_ok=True)

# Save the output to a log file
sys.stdout = open(f"{negbin_dir}/{dataset}_seed{seed}_negbin.log", "wt")

### Create MDSINE2 Study object from input datasets ###
print('Create MDSINE2 Study object from input datasets')
# Parse tables of samples and cast in Subject sets. Automatically creates the subject classes with the respective names
print('Parse datasets into MDSINE2 Study object')
mcnulty = md2.dataset.parse(                                    # Parse a dataset. Acts as a wrapper for mdsine2.Study.parse
    name=f'{dataset}_s{seed}',                                  # Name of the dataset
    metadata=str(input_dir / 'metadata.tsv'),                   # Metadata file
    taxonomy=str(input_dir / 'taxonomy.tsv'),                   # Taxonomy file
    reads=str(input_dir / 'reads.tsv'),                         # Reads file
    qpcr=str(input_dir / 'dna_yields.tsv'),                     # qPCR (DNA yields) file
    perturbations=str(input_dir / 'perturbations.tsv'),         # Perturbations file 
    sep='\t'                                                    # Separator used in the input files
)

### Learn the Negative Binomial dispersion parameters ###
print('Learn the Negative Binomial dispersion parameters')
# Set negative binomial model inference parameters
# Configuration class for learning the negative binomial dispersion parameters. Note that these parameters are learned offline 
print('Set negative binomial model inference parameters')
params_negbin = md2.config.NegBinConfig(    # Initialize the MCMC chain (NegBinConfig class)
    seed=0,                                 # Seed to start the inference
    burnin=burnin,                          # Number of initial Gibbs steps to throw away (burn-in iterations)
    n_samples=n_samples,                    # Number of total Gibbs steps (total iterations)
    checkpoint=checkpoint,                  # How often to write the trace in RAM to disk. Note that this must be a multiple of both burnin and n_samples
    basepath=str(negbin_dir)                # Basepath to save the trace to disk
)

# Build the compute graph for learning the model that is used to learn negative binomial parameters
print('Building the graph used for posterior inference of the negative binomial dispersion parameters')
mcmc_negbin = md2.negbin.build_graph(   # Builds the graph used for posterior inference of the negative binomial dispersion parameters (mdsin2.BaseMCMC)
    params=params_negbin,               # Parameters to run the model
    graph_name=mcnulty.name,            # Name (label) of the graph
    subjset=mcnulty                     # Subject (MDSINE2.Study object)
)

# Run inference to learn the negative binomial parameters
print('Running the MCMC chain to learn the negative binomial parameters')
mcmc_negbin = md2.negbin.run_graph(         # Run the MCMC chain mcmc (mdsin2.BaseMCMC)
    mcmc_negbin,                            # Inference object that is already built and initialized (mdsine2.BaseMCMC)
    crash_if_error=True                     # If True, throws an error if there is an exception during inference.
)

# Visualize the negative binomial dispersion model
print('Visualize the negative binomial dispersion model')
fig_negbin = md2.negbin.visualize_learned_negative_binomial_model(
    mcmc_negbin                         # Inference object with the negative binomial posteriors and the data it was learned on (mdsine2.BaseMCMC) 
)
fig_negbin.tight_layout()
plt.savefig(str(negbin_dir /'negbin.png'), dpi=300)

# Get a0 and a1 from negbin (get the mean of the posterior) and fixes them for inference
a0 = md2.summary(mcmc_negbin.graph[STRNAMES.NEGBIN_A0])['mean']
a1 = md2.summary(mcmc_negbin.graph[STRNAMES.NEGBIN_A1])['mean']

print('negbin d0:', a0)
print('negbin d1:', a1)