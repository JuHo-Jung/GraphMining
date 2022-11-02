# -*- coding: utf-8 -*-

import GPRas as gpr

## file_setup
nodefile = 'test_data/TP_nodes.csv'
linkfile = 'test_data/TP_links.csv'
node_filesetup = {'node_id':'nid', 'xcor':'xcor', 'ycor':'ycor'}
link_filesetup = {'ori':'ori', 'des':'des', 'weight':'time'}

## prepare for calculate
sg = gpr.GPRas()

## set the dataset from csv files
sg.dataset.from_csv(nodefile, linkfile, node_filesetup, link_filesetup)
### networkx graph object can be also imported using from_nx(anxgraph, node_setup, link_setup=None)
### see another example file

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


## get the summary of the calculation
summary_df = sg.get_summary()
print(summary_df)

## get result dataframe(pandas)
result_df = sg.get_results()
print(result_df.head())

## output the summary file, the alpha,beta,gamma is the last udpated
sg.output_summary(filename='result/temp_summary.csv')

## output (last udpated) DDPR and GPR only, to one csv file; default to all
sg.to_csv(filename='result/temp_output_dd_g.csv', items=['ddpr','gpr'])
## output all (last updated) results into one csv file
sg.All_to_csv(filename='result/temp_output.csv')


## output to node.shp and link.shp for mapping in GIS software
## projection info
crs67 = '+proj=tmerc +lat_0=0 +lon_0=121 +k=0.9999 +x_0=250000 +y_0=0 +ellps=aust_SA +towgs84=-752,-358,-179,-0.0000011698,0.0000018398,0.0000009822,0.00002329 +units=m +no_defs'

## output all results into one node shpfile, and a link shpfile
sg.All_to_shps(filename_prefix='result/temp_shp', crs=crs67)

## output two of the results
sg.to_shps(filename_prefix='result/temp_shp_pr_wpr', crs=crs67, items=['pr','wpr'])
