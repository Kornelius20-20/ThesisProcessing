import os
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
import approx_go
import pandas as pd

def descendingdictkeys(dic,desc=True):
       """
       Method that takes in a dictionary with keys and values that are integers and returns the keys in descending order
       of the values

       Parameters
       ----------
       dic: input dictionary

       Returns
       -------
       list of keys sorted based on order specified

       """

       keys, values = zip(*dic.items())
       keys = list(keys)
       values = list(values)

       output = []
       while len(values) > 0:
              bestind = values.index(max(values))
              output.append(keys[bestind])
              keys.pop(bestind)
              values.pop(bestind)

       if desc:
              return output
       else: return output.reverse()

def greedyclustergraph(graph, frame, aliasfile,id='BLAST_UniProt_ID',asterm=False):

       graph = approx_go.assign_metadata(graph, frame, asterm=asterm)

       results = greedy_modularity_communities(graph)

       for i in range(len(results)):
              # add cluster label
              for node in results[i]:
                     graph.nodes[node]['cluster'] = i + 1


       from stringInteractions2namedInteractions import stringidconvert,create_aliasdict

       aliasdict = create_aliasdict(aliasfile)

       proteins = [stringidconvert(results[i],aliasdict,id) for i in range(len(results))]

       return proteins


dframe2 = "txt/uniprot_original.csv"
# graph = nx.read_gexf('outputs/graphs/p-w=10-a=0.1-i=50-c=50.0.gexf')
aliasfile = "gz/39947.protein.aliases.v11.5.txt.gz"
frame = pd.read_csv(dframe2,delimiter=',')

for _,_,files in os.walk('outputs/graphs'):
       for file in files:
              if "seedsAndGO" not in file:
                     graph = nx.read_gexf(os.path.join('outputs/graphs',file))

                     proteins = greedyclustergraph(graph,frame,aliasfile)

                     with open(f"outputs/results/clusterfile{file}.txt",'w') as file:
                            for clust in proteins:
                                   for item in clust:
                                          file.write(item+'\n')
                                   file.write('\n')

