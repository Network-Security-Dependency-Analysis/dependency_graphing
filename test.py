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
edgelist = []
top_url = data['top_url']
for ext_url in data['external_urls']:
    edgelist.append((top_url, ext_url))

# Generate Graph
G = nx.from_edgelist(edgelist)

# Plot it
nx.draw(G, with_labels=True)
plt.show()
