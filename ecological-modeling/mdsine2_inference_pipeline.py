#!/bin/python3
# -*- coding: utf-8 -*-
# Author: Alejandro Castellanos

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
checkpoint = 250

# Define the input directory
input_dir = Path(f'mcnulty-datasets/{dataset}')
# Define the output directory
output_dir = Path(f'mcnulty-results/{dataset}')
output_dir.mkdir(parents=True, exist_ok=True)

### Create MDSINE2 Study object from input datasets ###
print('Create MDSINE2 Study object from input datasets')
# Parse tables of samples and cast in Subject sets. Automatically creates the subject classes with the respective names
print('Parse datasets into MDSINE2 Study object')
mcnulty = md2.dataset.parse(                                    # Parse a dataset. Acts as a wrapper for mdsine2.Study.parse
    name=f'{dataset}_s{seed}',                                          # Name of the dataset
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
params_negbin = md2.config.NegBinConfig(        # Initialize the MCMC chain (NegBinConfig class)
    seed=seed,                                  # Seed to start the inference
    burnin=burnin,                              # Number of initial Gibbs steps to throw away (burn-in iterations)
    n_samples=n_samples,                        # Number of total Gibbs steps (total iterations)
    checkpoint=checkpoint,                      # How often to write the trace in RAM to disk. Note that this must be a multiple of both burnin and n_samples
    basepath=str(output_dir / "negbin")         # Basepath to save the trace to disk
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
mcmc_negbin = md2.negbin.run_graph(     # Run the MCMC chain mcmc (mdsin2.BaseMCMC)
    mcmc_negbin,                            # Inference object that is already built and initialized (mdsine2.BaseMCMC)
    crash_if_error=True                     # If True, throws an error if there is an exception during inference.
)

# Visualize the negative binomial dispersion model
print('Visualize the negative binomial dispersion model')
fig_negbin = md2.negbin.visualize_learned_negative_binomial_model(
    mcmc_negbin                         # Inference object with the negative binomial posteriors and the data it was learned on (mdsine2.BaseMCMC) 
)
fig_negbin.tight_layout()
plt.savefig(str(output_dir / 'negbin' /'negbin.png'), dpi=300)

# Get a0 and a1 from negbin (get the mean of the posterior) and fixes them for inference
a0 = md2.summary(mcmc_negbin.graph[STRNAMES.NEGBIN_A0])['mean']
a1 = md2.summary(mcmc_negbin.graph[STRNAMES.NEGBIN_A1])['mean']

print('negbin d0:', a0)
print('negbin d1:', a1)

### Run MDSINE2 inference ###
print('Run MDSINE2 inference')

# Set directory
basepath = output_dir / "mdsine2" / f"seed{seed}"
basepath.mkdir(exist_ok=True, parents=True)

print(f'Run MDSINE2 inference with seed {seed} with 1000 burn-in steps and 10000 total steps')
# Initialize parameters of the model
print('Initialize parameters of the model')
params = md2.config.MDSINE2ModelConfig(
    basepath=basepath,                          # Basepath to save the inference trace to disk
    seed=seed,                                  # Seed to start the inference
    burnin=burnin,                              # Number of initial Gibbs steps to throw away (burn-in iterations)
    n_samples=n_samples,                        # Number of total Gibbs steps (total iterations)
    negbin_a0=a0, negbin_a1=a1,                 # Negative binomial dispersion parameters   
    checkpoint=checkpoint                       # How often to write the trace in RAM to disk. Note that this must be a multiple of both burnin and n_samples
)

# Initialize the clustering choice {config.py, pylab/variables.py}
params.INITIALIZATION_KWARGS[STRNAMES.CLUSTERING]['value_option'] = 'no-clusters'

# Builds the graph with the posterior classes and creates an mdsine2.BaseMCMC inference chain object that you ran run inference with
print('Builds the graph for the MCMC chain')
mcmc = md2.initialize_graph(             # Return pylab.inference.BaseMCMC
    params=params,                       # Parameters to run the model (MDSINE2ModelConfig class)
    graph_name=mcnulty.name,            # Name (label) of the graph
    subjset=mcnulty                     # Subject (MDSINE2.Study object)
)

# Perform inference
print('Perform inference')
mcmc = md2.run_graph(    # Run the MCMC chain mcmc (mdsin2.BaseMCMC)
    mcmc,                # Inference object that is already built and initialized (mdsine2.BaseMCMC)
    crash_if_error=True     # If True, throws an error if there is an exception during inference.
)

# Get the taxa from the graph
taxa = mcmc.graph.data.taxa
taxa_list = [taxa[i].name for i in range(len(taxa))]

### Get and visualize posteriors ###
print('Get and visualize posteriors')
# Set directories
growth_rate_dir = basepath / "growth-rate"
self_interactions_dir = basepath / "self-interactions"
interactions_dir = basepath / "interactions"
perturbation_dir = basepath / "perturbation"
coclusters_dir = basepath / "coclusters"
growth_rate_dir.mkdir(exist_ok=True, parents=True)
self_interactions_dir.mkdir(exist_ok=True, parents=True)
interactions_dir.mkdir(exist_ok=True, parents=True)
perturbation_dir.mkdir(exist_ok=True, parents=True)
coclusters_dir.mkdir(exist_ok=True, parents=True)

## Growth rates ##
print('Growth rates')
# Get the trace of the growth rates
growth_rates = mcmc.graph[STRNAMES.GROWTH_VALUE]

# Get the mean of the growth rates for each taxa
growth_rates_mean = md2.summary(growth_rates)['mean']
for i in range(growth_rates_mean.shape[0]):
    print(f'{taxa_list[i]}: {growth_rates_mean[i]}')

# Render the traces in the folder basepath. Makes a pandas.DataFrame table where the index is the Taxa name in taxa_formatter
print('# Plot the growth rates posteriors and create a table summarizing its values')
growth_rates_table = growth_rates.visualize(        # Return pandas.DataFrame
    growth_rate_dir                                 # Loction to write the files to
)
growth_rates_table.to_csv(growth_rate_dir / 'growth_rates_table.tsv', sep='\t')

## Self-interactions ##
print('Self-interactions')

# Get the trace of the self interactions 
self_interactions = mcmc.graph[STRNAMES.SELF_INTERACTION_VALUE]

# Get the mean of the self interaction for each taxa
self_interactions_mean = md2.summary(self_interactions)['mean']
for i in range(self_interactions_mean.shape[0]):
    print(f'{taxa_list}: {self_interactions_mean[i]}')

# Render the self interaction traces in the folder basepath. Makes a pandas.DataFrame table where the index is the Taxa name in taxa_formatter
self_interactions_table = self_interactions.visualize(
    self_interactions_dir          # Loction to write the files to
)
self_interactions_table.to_csv(self_interactions_dir / 'self_interactions_table.tsv', sep='\t')

## Taxa module assignments ##
print('Taxa module assignments')

# Get the clustering assignments and probabilities
clustering = mcmc.graph[STRNAMES.CLUSTERING_OBJ]
# Once the inference is complete, compute the clusters posthoc using sklearn's AgglomerativeClustering function with distance matrix being 1 - cocluster matrix {util.py}
print('Once the inference is complete, compute the clusters posthoc using sklearn\'s AgglomerativeClustering function with distance matrix being 1 - cocluster matrix')
md2.generate_cluster_assignments_posthoc(       # Returns np.ndarray(size=(len(items), ), dtype=int)
    clustering,                                 # Clustering object (mdsine2.posterior.Clustering)
    # n_clusters=12,                            # This specifies the number of clusters that are used during Agglomerative clustering.
    set_as_value=True                           # If True then set the result as the value of the clustering object
)
coclusters_assignment = md2.generate_cluster_assignments_posthoc(clustering)
coclusters_assignment_table = pd.DataFrame(coclusters_assignment, index=taxa_list, columns=['cluster_assignment'])
coclusters_assignment_table.to_csv(coclusters_dir / 'cluster_assignments_vector.tsv', sep='\t')

coclustering = clustering.generate_coclusters()
coclustering_table = pd.DataFrame(coclustering, index=taxa_list, columns=taxa_list)
coclustering_table.to_csv(coclusters_dir / 'cluster_assignments_matrix.tsv', sep='\t')

# Visualize co-cluster posterior probability
print('Visualize co-cluster posterior probability')
coclusters = md2.summary(mcmc.graph[STRNAMES.CLUSTERING_OBJ].coclusters)['mean']  # Get the mean of the cocluster posterior
coclusters_table = pd.DataFrame(coclusters, index=taxa_list, columns=taxa_list)
coclusters_table.to_csv(coclusters_dir / 'coclusters_probabilities.tsv', sep='\t')
md2.visualization.render_cocluster_probabilities(      # Render the cocluster proportions. Values in coclusters should be [0,1]
    coclusters, taxa=mcnulty.taxa,                                      # Square matrix indicating the cocluster proportions (2-dim np.ndarray)
    yticklabels='%(name)s | %(index)s')                                 # Label for the y-axis (str)
plt.savefig(coclusters_dir / 'coclustering_probabilities.png', bbox_inches='tight', dpi=300)

# Visualize trace for number of modules
md2.visualization.render_trace(  # Visualizes the Trace of a random variable
    clustering.n_clusters                               # Trace of the co-clustering probabilities
)
plt.savefig(coclusters_dir / 'clusters_trace.png', bbox_inches='tight', dpi=300)

## Interactions ##
print('Interactions')

# Get Lotka-Volterra interactions
interactions = mcmc.graph[STRNAMES.CLUSTER_INTERACTION_VALUE]
interactions.visualize(interactions_dir)
interactions_matrix = pd.read_table(f'{interactions_dir}/mean_matrix.tsv', index_col=0)

# Create format for cytoscape
interactions_table = interactions_matrix.reset_index()
interactions_table.rename(columns={'index': 'Source'}, inplace=True)
interactions_table = interactions_table.melt(id_vars=['Source'], var_name='Target', value_name='Interaction_coefficient')
def interaction_type(x):
    if x > 0:
        return '+'
    elif x < 0:
        return '-'
    else:
        return np.nan
interactions_table['Interaction_magnitude_log'] = np.log10(np.abs(interactions_table['Interaction_coefficient']))
interactions_table['Interaction'] = interactions_table['Interaction_coefficient'].apply(interaction_type)
interactions_table.dropna(inplace=True)
interactions_table = interactions_table.loc[:, ['Source', 'Target', 'Interaction', 'Interaction_magnitude_log']].copy()
interactions_table.set_index(['Source', 'Target'], inplace=True)
interactions_table.to_csv(f'{interactions_dir}/interaction_network.tsv', sep='\t')
interactions_table

interaction_bayes_factors_table = pd.DataFrame(md2.generate_interation_bayes_factors_posthoc(mcmc), index=taxa_list, columns=taxa_list)
interaction_bayes_factors_table.to_csv(f'{interactions_dir}/interaction_bayes_factors.tsv', sep='\t')

## Perturbation effects ##
print('Perturbation effects')
glv_params_pert_mag = mcmc.graph[STRNAMES.GLV_PARAMETERS].pert_mag
np.savetxt(f'{perturbation_dir}/perturbation_magnitude.tsv', glv_params_pert_mag.asarray(), delimiter='\t')

print('Visualize perturbation coefficients')
glv_params_pert_mag.visualize(perturbation_dir, 0)