# -*- coding: utf-8 -*-

"""
an example using networkx Graph object as data input
"""

import networkx as nx
import pandas as pd
import GPRas as gpr

## make a nx graph
nodefile = 'test_data/TP_nodes.csv'
linkfile = 'test_data/TP_links.csv'
node_filesetup = {'node_id':'nid', 'xcor':'xcor', 'ycor':'ycor'}
link_filesetup = {'ori':'ori', 'des':'des', 'weight':None}

ndf = pd.read_csv(nodefile)
nii = ndf[node_filesetup['node_id']].tolist()
nxx = ndf[node_filesetup['xcor']].tolist()
nyy = ndf[node_filesetup['ycor']].tolist()
nodes_lis = [ (ii, dict(xxx=xx,yyy=yy)) for ii,xx,yy in zip(nii,nxx,nyy) ]
edf = pd.read_csv(linkfile)
eoo = edf[link_filesetup['ori']].tolist()
edd = edf[link_filesetup['des']].tolist()
edges_lis = [ (oo,dd) for oo,dd in zip(eoo,edd) ]

ag = nx.Graph()
ag.add_nodes_from(nodes_lis)
ag.add_edges_from(edges_lis)

## graph setup info
node_setup = dict(xcor='xxx', ycor='yyy')
link_setup = None

## prepare for calculate
sg = gpr.GPRas()

## set the dataset from nx.Graph object
sg.dataset.from_nx(ag, node_setup, link_setup)

## initialize the algorithm with the basic setup; the dataset must be setup before this line
sg.Initialize(iteration=5000, alpha=1., beta=1., gamma=1.)

## calculate all 6 GPRs
sg.CalculateAll()

## calculate one of them, PR(), WPR(), DDPR(), GPR(), eDDPR(), eGPR() separately
## if need to update the alpha, beta, gamma, can be done here, with update=True arg.
sg.PR()
sg.WPR(alpha=2, update=True)
sg.DDPR(beta=2, update=True)
sg.GPR(alpha=3, beta=2, update=True)
sg.eDDPR(gamma=0.6, update=True)
sg.eGPR(alpha=3, gamma=0.2, update=True)

## output the summary file, the alpha,beta,gamma is the last udpated
sg.output_summary(filename='result/temp2_summary.csv')

## output all (last updated) results into one csv file
sg.All_to_csv(filename='result/temp2_output.csv')

## output DDPR and GPR only, to one csv file
sg.to_csv(filename='result/temp2_output_dd_g.csv', items=['ddpr','gpr'])

## output to node.shp and link.shp for mapping in GIS software
## projection info
crs67 = '+proj=tmerc +lat_0=0 +lon_0=121 +k=0.9999 +x_0=250000 +y_0=0 +ellps=aust_SA +towgs84=-752,-358,-179,-0.0000011698,0.0000018398,0.0000009822,0.00002329 +units=m +no_defs'

## output all results into one node shpfile, and a link shpfile
sg.All_to_shps(filename_prefix='result/temp2_shp', crs=crs67)

## output two of the results
sg.to_shps(filename_prefix='result/temp2_shp_pr_wpr', crs=crs67, items=['pr','wpr'])

## output to nx.Graph object
ag,pos = sg.to_nx()

## demo for drawing the network using matplotlib
ss = []
for n,d in ag.nodes_iter(data=True):
    ss.append(d['DDPR_score']*5000.)
import matplotlib.pyplot as plt
fig,ax = plt.subplots()
nx.draw_networkx_nodes(ag, pos=pos, node_size=ss)
nx.draw_networkx_edges(ag, pos=pos, alpha=0.3)
ax.set_aspect('equal')
plt.show()
