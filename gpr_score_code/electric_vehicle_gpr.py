from fcntl import DN_DELETE
import networkx as nx
import pandas as pd ## just for the reading of file before creating nx.Graph
import GPRas as gpr
import random

nodefile = './221026/TP_nodes_tmp.csv'
linkfile = './221026/TP_links.csv'
node_filesetup = {'node_id':'nid', 'xcor':'xcor', 'ycor':'ycor'}
link_filesetup = {'ori':'ori', 'des':'des', 'weight':'time'}

ndf = pd.read_csv(nodefile)
nii = ndf[node_filesetup['node_id']].tolist()
nxx = ndf[node_filesetup['xcor']].tolist()
nyy = ndf[node_filesetup['ycor']].tolist()
nodes_lis = [ (ii, dict(xxx=xx,yyy=yy)) for ii,xx,yy in zip(nii,nxx,nyy) ]
edf = pd.read_csv(linkfile)
eoo = edf[link_filesetup['ori']].tolist()
edd = edf[link_filesetup['des']].tolist()
edges_lis = [ (oo,dd) for oo,dd in zip(eoo,edd) ]

sources = []
targets = []
weights = []

for i in range(1, 24):
    for j in range(1, 24):
        if i == j:
            continue
        if random.randrange(1,4) > 2:
            sources.append(i)
            targets.append(j)
            weights.append(random.randrange(1,11))

df = pd.DataFrame(
    {
        'source' : sources,
        'target' : targets,
        'weight' : weights
    }
)


G = nx.DiGraph()
# G.add_nodes_from(nodes_lis)

G.add_nodes_from([(item, {
        "name": item,
        "type": "source",
        "xxx": nodes_lis[index][1]["xxx"],
        "yyy": nodes_lis[index][1]["yyy"]
    }) for index, item in enumerate(list(set(df.loc[:, ('source')].values.tolist())))
])
G.add_nodes_from([(item, {
        "name": item,
        "type": "target",
        "xxx": nodes_lis[index][1]["xxx"],
        "yyy": nodes_lis[index][1]["yyy"]
    }) for index, item in enumerate(list(set(df.loc[:, ('target')].values.tolist())))
])

# G.add_edges_from(edges_lis)
edges_weight = df.loc[:, ('source', 'target', 'weight')].values.tolist()
G.add_weighted_edges_from(edges_weight)



sg = gpr.GPRas()

## graph setup info
node_setup = dict(xcor='xxx', ycor='yyy') ## x,y columns from the nodes attr.
link_setup = None

# sg = sgc()
sg.dataset.from_nx(G, node_setup, link_setup)


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
print(result_df)


G = nx.DiGraph()
# G.add_nodes_from(nodes_lis)


G.add_nodes_from([(item, {
        "name": item,
        "type": "source",
        "xxx": nodes_lis[index][1]["xxx"],
        "yyy": nodes_lis[index][1]["yyy"],
        "score": item["GPR_score"]
    }) for index, item in enumerate(zip(list(set(df.loc[:, ('source')].values.tolist())), sg.gpr_dic.values()))
])
G.add_nodes_from([(item, {
        "name": item,
        "type": "target",
        "xxx": nodes_lis[index][1]["xxx"],
        "yyy": nodes_lis[index][1]["yyy"]
    }) for index, item in enumerate(list(set(df.loc[:, ('target')].values.tolist())))
])

# G.add_edges_from(edges_lis)
edges_weight = df.loc[:, ('source', 'target')].values.tolist()
G.add_edges_from(edges_weight)

nx.write_graphml(G, "test.graphml") 