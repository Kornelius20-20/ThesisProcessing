import networkx as nx
import pandas as pd
from collections import Counter

graphfile = "drought_module2.gexf"
dframe = "txt/processed_uniprot.csv"

graph = nx.read_gexf(graphfile)
frame = pd.read_csv(dframe)

import re

for node in graph.nodes:
    row = frame[frame['Entry'] == node]

    if not row.empty:
        biogo = row["Gene ontology (biological process)"].to_string() + row["Gene ontology (GO)"].to_string()
        biogo += row["Gene ontology (molecular function)"].to_string() + row["Gene ontology IDs"].to_string()
        res = re.findall("GO:\d\d\d\d\d\d\d", biogo)
        goset = set(res)

        toadddict = {node:{'GO': goset}}
        nx.set_node_attributes(graph, toadddict)
        graph.nodes[node]['GO'] = goset

# Get all the associated GO terms for each node and add them as a list

for node,attrs in graph.nodes(True):
    if 'GO' in attrs:

        nodego = attrs['GO']
        combinedgos = []
        for neighbor in graph.neighbors(node):
            try:
                neighborgo = graph.nodes[neighbor]['GO']
            except KeyError:
                continue

            intersected = nodego.intersection(neighborgo)
            combinedgos += list(intersected)

        golabels = Counter(combinedgos)
        mostcomlabel = golabels.most_common(1)
        if len(mostcomlabel) > 0:
            graph.nodes[node]['GO'] = mostcomlabel[0][0]

        else:
            graph.nodes[node]['GO'] = list(graph.nodes[node]['GO'])[0]

# for node,attrs in graph.nodes(True):
#     if 'GO' in attrs:
#         print(node,attrs['GO'])


nx.write_gexf(graph,"testgraph.gexf")