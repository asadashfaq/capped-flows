#! /usr/bin/env python
from __future__ import division
import os
import sys
import aurespf.solvers as au
import numpy as np
from pylab import plt
from aurespf.tools import *
from grid import *

"""
Plotting a lot of Bc vs. Tc figures of different export schemes.

To load and plot figures:
Bc,Tc = loader(mode,a,ae,q)
plotter(mode,Bc,Tc,q)
"""

# Scaling factor for transmission capacities
a = np.linspace(0,.1,3) # np.linspace(0,2,41)

# Scaling factor for transmission capacities used in the ensembles
ae = [0.0, 0.05, 0.1]#, 0.25, 0.35, 0.5, 0.7, 1.0]

# Quantiles to be plotted
q = [1, .999, .995, .99, .98, .95]

# Modes to be plotted:
modes = ['martin','linear','square','random-rolando']

def loader(mode,a,ae,Q):
    if mode == 'random-rolando':
        Bc = np.zeros((len(ae),len(Q)))
        Tc = np.zeros((len(ae),len(Q)))
    else:
        Bc = np.zeros((len(a),len(Q)))
        Tc = np.zeros((len(a),len(Q)))
    for i,b in enumerate(a):
        N = EU_Nodes(str(mode)+'-b-'+str(b)+'.npz')
        F = np.load('./results/'+str(mode)+'flows-b-'+str(b)+'.npy')
        Tload = np.sum(np.sum(n.mean for n in N))
        for j,qq in enumerate(Q):
            Bc[i,j] = np.sum(get_q(n.balancing,qq) for n in N)/Tload
            Tc[i,j] = sum(biggestpair(np.max(abs(F),1)))/1e6
    return Bc,Tc

def plotter(mode,Bc,Tc,Q):
    col = ['#000080','#0000FF','#4169E1','#6495ED','#00BFFF','#B0E0E6']
    plt.figure()
    ax = plt.subplot(111)
    for p in range(Bc.shape[1]):
        plt.plot(Tc[:,p],Bc[:,p],'-',color=str(col[p]))
    plt.xlabel('Tc [TW]')
    plt.ylabel('Bc normalised to total EU load')
    plt.title(str(mode)+' flow')
    
    # Shrink current axis by 25% to make room for legend
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])

    plt.legend(\
        ([str(Q[i]*100) for i in range(len(Q))]),\
        loc='center left', bbox_to_anchor=(1, 0.5),title='Quantiles')
    
    plt.savefig('figures/bctc_'+str(mode)+'.eps')

def plot_all(Bc,Tc,Q):
#    col = ['#000080','#0000FF','#4169E1','#6495ED','#00BFFF','#B0E0E6']
    col = ['-*r','-g','-b','-m']
    plt.figure()
    ax = plt.subplot(111)
    for p in range(Bc.shape[1]):
        plt.plot(Tc[:,p],Bc[:,p],str(col[p]))
    plt.xlabel('Tc [TW]')
    plt.ylabel('Bc normalised to total EU load')
    plt.title('Comparison')
    
    # Shrink current axis by 25% to make room for legend
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])

    plt.legend(\
        ([str(modes[i]) for i in range(len(modes))]),\
        loc='center left', bbox_to_anchor=(1, 0.5),title='99.9% quantiles')
    
    plt.savefig('figures/bctc_all.eps')

# Actual plotting and saving of figures
BcT = np.zeros((len(a),len(modes)))
TcT = np.zeros((len(a),len(modes)))
for k,m in enumerate(modes):
    B,T = loader(m,a,ae,q)
    plotter(m,B,T,q)

# need support for plotting one figure with 99.9% for all schemes
    BcT[:,k] = B[:,1]
    TcT[:,k] = T[:,1]

plot_all(BcT,TcT,q)

# need support for a bar plot of the distribution of Bc for each country.
