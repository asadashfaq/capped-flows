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
"""

# Scaling factor for transmission capacities
a = np.linspace(0,2,41)
# Scaling factor for transmission capacities used in the ensembles
ae = [0.0, 0.05, 0.1, 0.25, 0.35, 0.5, 0.7, 1.0]
# Quantiles to be plotted
q = [100, 99.9, 99.5, 99, 98, 95]

def loader(mode,a,ae,q):
    BcT = []
    TcT = []
    for q in q:
        Bc = []
        Tc = []
        for b in a:
            N = EU_Nodes(str(mode)+'-b-'+str(b)+'.npz')
            F = np.load('./results/'+str(mode)+'flows-b-'+str(b)+'.npy')
            Tload = np.sum(np.sum(n.mean for n in N))
            Bc.append(np.sum(get_q(n.balancing,q) for n in N)/Tload)
            Tc.append(sum(biggestpair(np.max(abs(F),1)))/1e6)
        BcT.append(Bc)
        TcT.append(Tc)
    return BcT,TcT

def plotter(mode,Bc,Tc):
    col = ['#191970','#0000FF','#6495ED','#B0E0E6','#B0C4De']
    plt.figure()
    for p in len(Bc):
        plt.plot(Tc[p],Bc[p],'-'+str(col[p]))
    plt.xlabel('Tc [TW]')
    plt.ylabel('Bc normalised to total EU load')
    plt.title(str(mode)+' flow on EU grid')
    plt.legend(('100','99.9','99.5','99','98','95'),\
    # insert as loop in stead: [str(Q[i]) for i in range(len(Q))]
            loc='center left', bbox_to_anchor=(1, 0.5))

    # Shrink current axis by 25% to make room for legend
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.savefig('figures/bctc_'+str(mode)+'.eps')

# Load and plot figures
# Bc,Tc = loader('martin',a,ae,q)
# plotter('martin',Bc,Tc)

# need support for plotting one figure with 99.9% for all schemes

# need support for a bar plot of the distribution of Bc for each country.
