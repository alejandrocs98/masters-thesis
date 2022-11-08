#!/bin/python3

# Author: Alejandro Castellanos

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from lmfit import minimize, Parameters, Parameter, report_fit
import matplotlib.pyplot as plt; plt.rc('font', size=16)
import matplotlib.cm as cm

cols = [cm.tab10(i) for i in range(10)]
cols.append(cm.Set2(5))
cols.append(cm.Paired(4))

#------------------------------------------------------------

class Experiment:
    # Attributes
    def __init__(self, data, treatment='LF0'):
        self.treatment = treatment
        self.data = data[data['Treatment'] == treatment].copy()
        self.species = self.data.Strain.unique()
        self.x0 = np.array([self.data[self.data['Day'] == 1].groupby('Strain')['Absolute_abundance'].mean()[i] for i in self.species])
        self.x = np.array([self.data[self.data['Strain'] == i]['Absolute_abundance'].values for i in self.species])
        self.t = np.array([self.data[self.data['Strain'] == i]['Day'].values for i in self.species])
        self.t_span = [self.data.Day.values.min(), self.data.Day.values.max()]
        self.t_eval = self.data.Day.unique()
        self.params = self.define_random_params()

    # Methods
    def define_random_params(self):
        n = len(self.species)
        p = Parameters()
        p.add('species', value=n, vary=False)
        for i in range(n):
            p.add(f'growth_{i+1}', value=np.random.uniform(0, 10), min=0, vary=True)
            p.add(f'susceptibility_{i+1}', value=np.random.uniform(-5, 5), vary=True)
            for j in range(n):
                if i == j:
                    p.add(f'cross_int_{i+1}_{j+1}', value=np.random.uniform(-5, 0), max=0, vary=True)
                else:
                    p.add(f'cross_int_{i+1}_{j+1}', value=np.random.uniform(-5, 5), vary=True)
        return p

    def define_params(self, growth, cross_int, susceptibility):
        n = len(self.species)
        p = Parameters()
        p.add('species', value=n, vary=False)
        for i in range(n):
            p.add(f'growth_{i+1}', value=growth[i], min=0, vary=True)
            p.add(f'susceptibility_{i+1}', value=susceptibility[i], vary=True)
            for j in range(n):
                if i == j:
                    p.add(f'cross_int_{i+1}_{j+1}', value=cross_int[i][j], max=0, vary=True)
                else:
                    p.add(f'cross_int_{i+1}_{j+1}', value=cross_int[i][j], vary=True)
        self.params = p

    def gLV(self, t, x, params):

        growth = np.array([params[f'growth_{i+1}'].value for i in range(params['species'].value)])
        cross_int = np.array([[params[f'cross_int_{i+1}_{j+1}'].value for j in range(params['species'].value)] for i in range(params['species'].value)])
        susceptibility = np.array([params[f'susceptibility_{i+1}'].value for i in range(params['species'].value)])

        inter = np.sum([x[i]*cross_int[i,j] for i in range(len(x)) for j in range(len(x))])

        if self.treatment == 'LF0':
            C = 0 if (t <= 12 or t >= 25) else 1
        if self.treatment == 'HF0':
            C = 1 if (t <= 12 or t >= 25) else 0
        if self.treatment == 'Stein2013':
            C = 1 if t < 1 else 0

        return np.array([x[i]*(growth[i] + inter + C*susceptibility[i]) for i in range(len(x))])

    def solve_gLV(self, params):
        return solve_ivp(lambda t, x: self.gLV(t, x, params=params), self.t_span, self.x0, t_eval=self.t_eval)

    def residuals(self, params, t, x):
        model = self.solve_gLV(params)
        return model.y - x

    def fit_gLV(self):
        self.fitting = minimize(self.residuals, self.params, args=(self.t, self.x))
        self.fitted_x = self.x + self.fitting.residual.reshape(self.x.shape)
        return self.fitting 

    def plot_trajectories(self, x_log=True):
        fig = plt.figure(figsize=(13, 10))
        for i in range(len(self.species)):
            plt.scatter(self.t[i], self.x[i], color=cols[i], s = 15, alpha=0.8)
            plt.plot(self.t_eval, self.fitted_x[i], '-', color=cols[i], label=self.species[i])
        plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.32),
            ncol=3, fancybox=True, shadow=False, title='Especie')
        plt.grid()
        plt.xlabel('Dias')
        if x_log:
            plt.ylabel('Abundancia relativa (log)')
            plt.yscale('log')
        else:
            plt.ylabel('Abundancia absoluta')
        
        return fig

class TestData(Experiment):
    # Attributes
    def __init__(self, species, x0, t_span, t_eval, treatment='LF0'):
        self.treatment = treatment
        self.species = species
        self.x0 = x0
        self.t_span = t_span
        self.t_eval = t_eval
        self.params = self.define_random_params()

    # Methods
    def dynamics_simulation(self):
        system_evolution =  self.solve_gLV(self.params)
        self.t_sim = system_evolution.t
        self.x_sim = system_evolution.y
        return system_evolution

    def plot_dynamics(self, x_log=False):
        fig = plt.figure(figsize=(13, 10))
        for i in range(len(self.species)):
            plt.plot(self.t_sim, self.x_sim[i], '-', color=cols[i], label=self.species[i])
        plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.32),
            ncol=3, fancybox=True, shadow=False, title='Especie')
        plt.grid()
        plt.xlabel('Dias')
        if x_log:
            plt.ylabel('Abundancia relativa (log)')
            plt.yscale('log')
        else:
            plt.ylabel('Abundancia absoluta')
        
        return fig

    def noisy_data(self, noise=0.1):
        self.x = self.x_sim + noise*np.random.normal(0, 1, self.x_sim.shape)
        self.t = np.array([self.t_sim for i in self.species])
