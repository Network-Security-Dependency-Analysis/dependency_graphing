''' Testing the networkx graphing library '''
import json
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

DATA_FILE = 'data/test.json'

# Retrieve the json data on dependencies
with open(DATA_FILE) as f:
    data = json.load(f)

# Generate edge list
top_url = data['top_url']
edgelist = [ (top_url, ext_url) for ext_url in data['external_urls'] ]
nodesize = [ data['external_urls'][ext_url]['count']*300 for ext_url in data['external_urls'] ]
nodesize.insert(0, 300)  # top_url
print(nodesize)

# Generate Graph
G = nx.from_edgelist(edgelist)

# Plot it
nx.draw(G, with_labels=True, node_color="skyblue", node_size=nodesize)
plt.show()
