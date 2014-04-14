#! /usr/bin/env python
from __future__ import division
import os
import sys
import aurespf.solvers as au
import numpy as np
from pylab import plt
from multiprocessing import Pool
from aurespf.tools import *
from grid import *

"""
Solving an ensemble of Rolando flows with randomized hours in order to get rid
of the time dependence.
"""

# Scaling factor for transmission capacities
a = [0.0, 0.25, 0.35, 0.5, 0.7, 1.0]

def run(b):
    # Load data and get flow quantiles
    N = EU_Nodes()
    caps = get_quant_caps(quant=.99)
    
    # Multiple Rolando flows to be averaged
    runs = 2
    Bc = np.zeros((len(N),runs))
    B99 = np.zeros((len(N),runs))
    for i in range(runs):
        lapse = np.arange(0,70128)
        np.random.shuffle(lapse)
        N,F = au.solve(N,mode='capped random rolando',h0=caps,b=b,lapse=lapse)
        for n in N:
            Bc[n.id,i] = np.max(n.balancing)
            B99[n.id,i] = get_q(n.balancing,.99)

    # Calculate mean of Bc, B99
    Bcm = np.mean(Bc,1)
    B99m = np.mean(B99,1)

    # Saving results for second run
    np.savez('./results/bc-ensemble-mean-b-'+str(b)+'.npz',Bc=Bcm,B99=B99m,)

    # Second run with ensemble means as initial balancing capacities
    N,F = au.solve(N,mode='capped random mean rolando',h0=caps,b=b,lapse=lapse)
    N.save_nodes('random-rolando-b-'+str(b))
    np.save('./results/random-rolandoflows-b-'+str(b),F)

# Solve on multiple cores
p = Pool(6)
p.map(run,a)
