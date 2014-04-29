from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from aurespf.tools import *

"""
Plots the distribution of each country's balancing capacity.
"""

# Set the desired b-value and quantile.
b = 0.3
q = .99

N = np.load('./results/random-rolando-b-'+str(b)+'.npz')
B = np.load('./results/bc-ensemble-b-'+str(b)+'.npz')

names = N['label']
names = np.append('EU',names)
meanload = N['mean']
meanloadEU = np.mean(meanload)

Bc = B['Bc']
B99 = B['B99']

means = np.mean(B99,1)
meanEU = np.mean(means)

normmeans = means/meanload
normmeanEU = meanEU/meanloadEU

mins = np.min(B99,1)/meanload
maxs = np.max(B99,1)/meanload

x = np.linspace(1,len(means),len(means))
plt.figure()
ax = plt.subplot(1,1,1)
ax.set_ylim(.95*np.min(mins),1.05*np.max(maxs))
ax.set_xlim(-1,len(names)+.1)
ax.set_xticks(np.linspace(0,len(means),len(means)+1))
ax.set_xticklabels(names,rotation = 60, ha="right", va="top")
plt.plot(0,normmeanEU,'ob')
plt.plot(x,normmeans,'ob')
plt.plot([x,x],[mins,maxs],'-r',linewidth=2)
plt.ylabel('Balancing capacities normalised to average load')

means = np.mean(Bc,1)
meanEU = np.mean(means)

normmeans = means/meanload
normmeanEU = meanEU/meanloadEU

mins = np.min(Bc,1)/meanload
maxs = np.max(Bc,1)/meanload

x = np.linspace(1,len(means),len(means))
plt.figure()
ax = plt.subplot(1,1,1)
ax.set_ylim(.95*np.min(mins),1.05*np.max(maxs))
ax.set_xlim(-1,len(names)+.1)
ax.set_xticks(np.linspace(0,len(means),len(means)+1))
ax.set_xticklabels(names,rotation = 60, ha="right", va="top")

plt.plot(0,normmeanEU,'ob')
plt.plot(x,normmeans,'ob')
plt.plot([x,x],[mins,maxs],'-r',linewidth=2)
plt.ylabel('Balancing capacities normalised to average load')
plt.show()

