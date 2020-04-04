''' Plot the dependency graph for a single top level domain (TLD) '''
import json
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

DATA_FILE = 'data/47b3bb0e99cef4dbf43d6ce37cbf87f700334d77.json'
DEFAULT_NODE_SIZE = 300  # library default is 300

# Retrieve the json data on dependencies
with open(DATA_FILE) as f:
    data = json.load(f)

# Generate edge list
edgelist = []
node_sizes = [DEFAULT_NODE_SIZE]
top_domain = data['top_domain']
for ext_domain in data['external_domains']:
    edgelist.append((top_domain, ext_domain))
    node_sizes.append(data['external_domains'][ext_domain]['resources']['total'] * DEFAULT_NODE_SIZE)

# Generate Graph
G = nx.from_edgelist(edgelist)

# Plot it
nx.draw(G, with_labels=True, font_size=5, node_color="skyblue", node_size=node_sizes)
plt.show()
