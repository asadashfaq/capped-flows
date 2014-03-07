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

def Bc0(file):
# Calculation of initial balancing constraints for normalisation
    N = EU_Nodes(load_filename=file+'.npz')
    mean_n = [node.mean for node in N]
    Global_B = np.max(-sum(n.mismatch for n in N))
    Bc0 = mean_n*Global_B/sum(mean_n)
    print 'Bc0 = ',Bc0
    print len(Bc0)
    return Bc0

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

    # Rolando flow
    if 'rolando' in mode:
        print 'Solving capped Rolando flow'
        for b in np.linspace(.1,2,39):
            N,F = au.solve(N,mode='capped rolando verbose',h0=caps,b=b)
            N.save_nodes('rolando-b-'+str(b))
            np.save('./results/rolandoflows-b-'+str(b),F)

if 'plot' in task:
    if 'martin' in mode:
# Put all of this in a function
        print 'Plotting capped Martin flow'
        mBc = []
        qBc = []
        Tc = []
        Bc0 = Bc0('martin-b-0.1')
        for b in np.linspace(.1,2,39):
            N = EU_Nodes('martin-b-'+str(b)+'.npz')
            F = np.load('./results/martinflows-b-'+str(b)+'.npy')
            mBc.append(np.sum(np.max(n.balancing)) for n in N) # remember normalisation
            q=[]
            for i in range(0,30): # This should be done in another way
                q.append(get_q(N['load'][i]))
            qBc.append(sum(q))
            Tc.append(sum(biggestpair(np.max(abs(F),1))))
        plt.figure()
        plt.plot(Tc,mBc/Bc0,'-b')
        plt.plot(Tc,qBc/Bc0,'-k')
        plt.xlabel('Tc')
        plt.ylabel('Bc')
        plt.title('Martin flow')
        plt.savefig('bctc_martin.eps')

    if 'rolando' in mode:
        print 'Plotting capped Rolando flow'
        mBc = []
        qBc = []
        Tc = []
        for b in np.linspace(.1,2,39):
            N = np.load('./results/rolando-b-'+str(b)+'.npz')
            F = np.load('./results/rolandoflows-b-'+str(b)+'.npy')
            mBc.append(np.sum(np.max(N['load'],1)))
            q=[]
            for i in range(0,30):
                q.append(get_q(N['load'][i]))
            qBc.append(sum(q))
            Tc.append(sum(biggestpair(np.max(abs(F),1))))
        plt.figure()
        plt.plot(Tc,mBc,'-b')
        plt.plot(Tc,qBc,'-k')
        plt.xlabel('Tc')
        plt.ylabel('Bc')
        plt.title('Rolando flow')
        plt.savefig('bctc_rolando.eps')
