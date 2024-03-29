#! /usr/bin/env python
import aurespf.solvers as au
import numpy as np

# EU grid with all alphas set to .7

alphas = np.ones(30)*.7

files = ['AT.npz', 'FI.npz', 'NL.npz', 'BA.npz', 'FR.npz', 'NO.npz', 'BE.npz', 'GB.npz', 'PL.npz', 'BG.npz', 'GR.npz', 'PT.npz', 'CH.npz', 'HR.npz', 'RO.npz', 'CZ.npz', 'HU.npz', 'RS.npz', 'DE.npz', 'IE.npz', 'SE.npz', 'DK.npz', 'IT.npz', 'SI.npz', 'ES.npz', 'LU.npz', 'SK.npz', 'EE.npz', 'LV.npz', 'LT.npz']

def EU_Nodes(load_filename=None, full_load=False):
    return au.Nodes(admat='./settings/eadmat.txt', path='./data/', prefix = "ISET_country_", files=files, load_filename=load_filename, full_load=full_load, alphas=alphas, gammas=np.ones(30))
