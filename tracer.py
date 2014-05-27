import numpy as np
from aurespf.tools import AtoKh_old

"""
Algorithm for tracing the vectorised flow of electricity.
"""

def get_links(node_id,admat):
    """
    Create a list of links for each node. Links are given a unique number
    and a +/- 1 to indicate direction.
    Also return a dictionary for in- and outflows containing link number
    and the connected node. This gets very useful later on.
    """
    links=[]
    linkno=-1
    indexi={}
    indexo={}
    for i in range(len(admat[node_id])):
        for j in range(len(admat[node_id])):
            if admat[j][i]>0 and j>i:
                linkno+=1
                if node_id==j:
                    links.append([linkno,-1])
                    indexi[linkno] = j
                if node_id==i:
                    links.append([linkno,1])
                    indexo[linkno] = j
	return links,indexi,indexo

def tracer(N,F,pathadmat=None,lapse=None):
    """
    N and F should be a solved nodes object and corresponding flows,
    respectively.
    """
    colors = 6  # number of contributors in the vectorised color.
                # balancing, wind, solar, curtailment, load, storage

    if N[0].solved != True :
        raise Exeption('The loaded nodes object is not solved!')

    if pathadmat == None :
        pathadmat = N.pathadmat
    
    if lapse == None:
        lapse = N[0].nhours
    
    admat = np.genfromtxt(pathadmat)

    """
    Build incidence matrix and create and index of links.
    listflows = ['from','to',id] e.g. ['AT','CH',0].
    All links are counted only once.
    """
    K,h0,listflows = AtoKh_old(N,pathadmat=pathadmat)

    """
    Make room for the power mixes in the nodes object and add each nodes own
    contribution to the power mix.
    """
    for n in N:
        n.links,n.indict,n.outdict= get_links(n.id,admat)
        n.powermix = np.zeros((len(N),colors,lapse))
        n.total_powermix = np.zeros((len(N),colors))
        n.powermix[n.id,0] = n.get_balancing
        n.powermix[n.id,1] = n.get_wind
        n.powermix[n.id,2] = n.get_solar
        n.powermix[n.id,3] = n.get_curtailment
        n.powermix[n.id,4] = n.load
        n.powermix[n.id,5] = n.get_storage_discharge # charge/discharge: -/+

    """
    Calculate power mix for every time step in lapse.
    """
#    for t in range(lapse):

    # for each node
    # check for imports on links and add to power mix

    # cycle through all nodes until all power mixes are populated


