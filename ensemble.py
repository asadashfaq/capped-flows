#! /usr/bin/env python
from __future__ import division
import os
import sys
import aurespf.solvers as au
import numpy as np
from pylab import plt
import multiprocessing as mp
from aurespf.tools import *
from grid import *

"""
Solving an ensemble of Rolando flows with randomized hours in order to get rid
of the time dependence.
"""

def plotter(mode):
    if mode == 'martin':
        col = ['ob','og']
    if mode == 'rolando':
        col = ['oc','oy']
    if mode == 'linear':
        col = ['*b','*y']
    if mode == 'square':
        col = ['*c','*y']
    mBc = []
    qBc = []
    Tc = []
    for b in a:
        N = EU_Nodes(str(mode)+'-b-'+str(b)+'.npz')
        F = np.load('./results/'+str(mode)+'flows-b-'+str(b)+'.npy')
        Tload = np.sum(np.sum(n.mean for n in N))
        mBc.append(np.sum(np.max(n.balancing) for n in N)/Tload)
        qBc.append(np.sum(get_q(n.balancing,.99) for n in N)/Tload)
        Tc.append(sum(biggestpair(np.max(abs(F),1)))/1e6)
    plt.plot(Tc,mBc,str(col[0]))
    plt.plot(Tc,qBc,str(col[1]))

# Load data and get flow quantiles
N = EU_Nodes()
caps = get_quant_caps(quant=.99)

# Scaling factor for transmission capacities
a = np.linspace(0,2,41)
b = 0.25

# Rolando flow
runs = 2
Bc = np.zeros((len(N),runs))
B99 = np.zeros((len(N),runs))
for i in range(runs):
    lapse = np.arange(0,70128)
    lapse = np.random.shuffle(lapse)
    N,F = au.solve(N,mode='capped rolando verbose',h0=caps,b=b,lapse=lapse)
    N.save_nodes('random-rolando1-'+str(i))
    for n in N:
        Bc[n.id,i] = np.max(n.balancing)
        B99[n.id,i] = get_q(n.balancing,.99)

# Calculate mean of Bc, B99
Bcm = np.mean(Bc,1)
B99m = np.mean(B99,1)

# Check for consistency
BEU = np.sum(Bcm,0)
print 'Total EU balancing capacity',BEU

# put mean Bc as initial condition for a second run
#for b in a:
#    N,F = au.solve(N,mode='capped rolando verbose',h0=caps,b=b)
#    N.save_nodes('rolando-b-'+str(b))
#    np.save('./results/rolandoflows-b-'+str(b),F)

#if 'plot' in task:
#    print 'Plotting flows'
#    plotter('martin')
#    plotter('rolando')
#    plt.xlabel('Tc [TW]')
#    plt.ylabel('Bc normalised to total EU load')
#    plt.title('Capped flows on EU grid')
#    plt.legend(('Max Martin','99 Q Martin','Max Rolando','99 Q Rolando'),loc=1)
#    plt.savefig('bctc_martin_rolando.eps')
