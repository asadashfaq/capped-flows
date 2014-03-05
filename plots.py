from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

# Plots of different implementations of the capped flow.

# Structure of F is a matrix with a row for each link with flow for every time
# step.

# Access elements of N by typing N['load']. There are 30 nodes. Structure of N:
"""
N = 
['load',
 'storage_default_output',
 'storage_level',
 'storage_discharge',
 'mismatch',
 'normwind',
 'label',
 'solved',
 'curtailment',
 'balancing',
 'nhours',
 'alpha',
 'normsolar',
 'id',
 'gamma',
 'mean']
"""

# The Martin flow
Nm = np.load("./results/martin.npz")
Fm = np.load("./results/martin_flows.npy")

Bc = np.max(Nm['balancing'])
aLn = np.mean(Nm['load'],1)
x = np.linspace(1,30,30)
plt.plot(x,Bc/aLn,'*')
plt.xlabel('Node')
plt.ylabel(r'$B_c/\langle L_n\rangle$')
plt.title('Capped Martin flow')
plt.savefig('bcm.eps')
