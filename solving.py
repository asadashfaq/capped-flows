#! /usr/bin/env python
import os
import sys
import aurespf.solvers as au
import numpy as np
from pylab import plt
import multiprocessing as mp
from aurespf.tools import *
from grid import *

"""
Solving different implementations of capped flow to produce Bc vs Tc figures

Examples to run the script from terminal:
1) python solving.py solve martin rolando
2) python solving.py plot martin
"""

def plotter(mode):
    mBc = []
    qBc = []
    Tc = []
    for b in np.linspace(.1,2,39):
        N = EU_Nodes(str(mode)+'-b-'+str(b)+'.npz')
        F = np.load('./results/'+str(mode)+'flows-b-'+str(b)+'.npy')
        Tload = np.sum(np.sum(n.mean for n in N))
        mBc.append(np.sum(np.max(n.balancing) for n in N)/Tload)
        qBc.append(np.sum(get_q(n.balancing,.99) for n in N)/Tload)
        Tc.append(sum(biggestpair(np.max(abs(F),1))))
    plt.figure()
    plt.plot(Tc,mBc,'-b')
    plt.plot(Tc,qBc,'-k')
    plt.xlabel('Tc')
    plt.ylabel('Bc')
    plt.title(str(mode)+' flow')
    plt.savefig('bctc_'+str(mode)+'.eps')

# Which implementation to solve
if len(sys.argv)<3:
    raise Exception('Not enough inputs!')
else:
    task = str(sys.argv[1])
    mode = str(sys.argv[2:])
    if (('solve' not in task ) and ('plot' not in task)):
        raise Exception('Wrong task selected!')
    if (('martin' not in mode) and ('rolando' not in mode)):
        raise Exception('No implementation selected!')

if 'solve' in task:
    # Load data and get flow quantiles
    N = EU_Nodes()
    caps = get_quant_caps(quant=.99)

    # Martin flow
    if 'martin' in mode:
        print 'Solving capped Martin flow'
        for b in np.linspace(.1,2,39):
            N,F = au.solve(N,mode='capped martin verbose',h0=caps,b=b)
            N.save_nodes('martin-b-'+str(b))
            np.save('./results/martinflows-b-'+str(b),F)

    # Rolando flow
    if 'rolando' in mode:
        print 'Solving capped Rolando flow'
        for b in np.linspace(.1,2,39):
            N,F = au.solve(N,mode='capped rolando verbose',h0=caps,b=b)
            N.save_nodes('rolando-b-'+str(b))
            np.save('./results/rolandoflows-b-'+str(b),F)

if 'plot' in task:
    if 'martin' in mode:
        print 'Plotting capped Martin flow'
        plotter('martin')

    if 'rolando' in mode:
        plotter('rolando')
