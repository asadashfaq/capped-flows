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
"""

# Which implementation to solve
if len(sys.argv)<2:
    raise Exception('No mode selected!')
else:
    task = str(sys.argv[1])
    if len(sys.argv)>2:
        mode = str(sys.argv[2:])

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

    #Rolando flow
    if 'rolando' in mode:
        print 'Solving capped Rolando flow'
        for b in np.linspace(.1,2,39):
            N,F = au.solve(N,mode='capped rolando verbose',h0=caps,b=b)
            N.save_nodes('rolando-b-'+str(b))
            np.save('./results/rolandoflows-b-'+str(b),F)

if 'plot' in task:
    if 'martin' in mode:
        mBc = []
        qBc = []
        Tc = []
        for b in np.linspace(.1,2,39):
            N = np.load('./results/martin-b-'+str(b)+'.npz')
            F = np.load('./results/martinflows-b-'+str(b)+'.npy')
            mBc.append(np.sum(np.max(N['load'],1)))
            q=[]
            for i in range(0,30):
                q.append(get_q(N['load'][i]))
            qBc.append(sum(q))
            Tc.append(sum(biggestpair(np.max(abs(F),1))))
    plt.figure()
    plt.plot(Tc,mBc,'-b')
    plt.plot(Tc,qBc,'-k')
    plt.savefig('bctc.eps')
