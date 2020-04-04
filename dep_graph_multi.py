''' Plot the dependency graph for a multiple top level domains (TLD) '''
import os
import json
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

DATA_DIR = 'data/'
DEFAULT_NODE_SIZE = 15  # library default is 300

# Retrieve the json data on dependencies
json_data = []
for fname in os.listdir(DATA_DIR):
    if not fname.endswith('.json'): continue
    with open(DATA_DIR + fname) as f:
        json_data.append(json.load(f))

# Generate list of edges between all nodes
edgelist = []
for data in json_data:
    top_domain = data['top_domain']
    ext_domain = data['external_domains']
    for ed in ext_domain:
        edgelist.append((top_domain, ed))

# Generate Graph
G = nx.from_edgelist(edgelist)

# Count the total number of dependencies
num_deps = {}
for data in json_data:
    for ed in data['external_domains']:
        total = data['external_domains'][ed]['resources']['total']
        if ed in num_deps: num_deps[ed] = num_deps[ed] + total
        else: num_deps[ed] = total
    td = data['top_domain']
    if td in num_deps: num_deps[td] = num_deps[td] + 1
    else: num_deps[td] = 1

# Update node sizes in the graph
node_sizes = []
for node in G.nodes:
    node_sizes.append(num_deps[node] * DEFAULT_NODE_SIZE)

# Plot it
nx.draw(G, with_labels=True, font_size=5, node_color="skyblue", node_size=node_sizes)
plt.show()
