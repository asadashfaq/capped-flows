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
    mode = str(sys.argv[1:])

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
