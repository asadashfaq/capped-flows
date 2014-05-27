import numpy as np
from aurespf.tools import AtoKh_old

"""
Algorithm for tracing the vectorised flow of electricity.
"""

def get_links(node_id,matr):
    """
    Create a list of links for each node. Links are given a unique number
    and an integer to indicate direction.
    """
	links=[]
	linkno=-1
	for j in range(len(matr[node_id])):
		for i in range(len(matr[node_id])):
			if matr[i][j]>0 and i>j:
				linkno+=1
				if node_id==i: links.append([linkno,-1])
				if node_id==j: links.append([linkno,1])
	return links

def tracer(N,F,admat=None,lapse=None):
    """
    N and F should be a solved nodes object and corresponding flows,
    respectively.
    """
    colors = 6  # number of contributors in the vectorised color.
                # balancing, wind, solar, curtailment, load, storage

    if N[0].solved != True :
        raise Exeption('The loaded nodes object should be solved.')

    if admat == None :
        admat = N.pathadmat
    
    if lapse == None:
        lapse = N[0].nhours

    """
    Build incidence matrix and create and index of links.
    listflows = ['from','to',id] e.g. ['AT','CH',0].
    All links are counted only once.
    """
    K,h0,listflows = AtoKh_old(N,pathadmat=admat)

    """
    Make room for the power mixes in the nodes object and add each nodes own
    contribution to the powermix.
    """
    for n in N:
        n.links = get_links(n.id,matr)
        n.powermix = np.zeros((len(N),colors,lapse))
        n.total_powermix = np.zeros((len(N),colors))
        n.powermix[n.id,0] = n.get_balancing
        n.powermix[n.id,1] = n.get_wind
        n.powermix[n.id,2] = n.get_solar
        n.powermix[n.id,3] = n.get_curtailment
        n.powermix[n.id,4] = n.load
        n.powermix[n.id,5] = n.get_storage_discharge # charge/discharge: -/+

    """
    Calculate powermix for every time step in lapse.
    """
    for t in range(lapse):


