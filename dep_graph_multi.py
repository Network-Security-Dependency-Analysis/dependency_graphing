''' Plot the dependency graph for a multiple top level domains (TLD) '''
import os
import json
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

DEFAULT_NODE_SIZE = 1  # library default is 300
MIN_DEPENDENCIES = 5
DATA_DIR = 'data/pgh/'
# RESOURCES = ['script', 'iframe', 'video', 'audio', 'img', 'embed']
RESOURCES = ['script']


################################################################################
# Initial Graph Generation
################################################################################
# Retrieve the json data on dependencies
TLDs = []
for fname in os.listdir(DATA_DIR):
    if not fname.endswith('.json'): continue
    with open(DATA_DIR + fname) as f:
        TLDs.append(json.load(f))

# Generate list of edges between all nodes
edgelist = []
for tld in TLDs:
    top_domain = tld['top_domain']
    ext_domains = tld['external_domains']
    for ext_domain in ext_domains:
        edgelist.append((top_domain, ext_domain))

# Generate Graph
G = nx.from_edgelist(edgelist)


################################################################################
# Parameter adjusting (labels, node sizes, etc.)
################################################################################
# Count the total number of dependent resources for each TLD
num_deps = {}
for tld in TLDs:
    # Add the top domain into the dictionary
    td = tld['top_domain']
    num_deps[td] = num_deps[td] + 1 if td in num_deps else 1

    # Add the external domains into the dictionary
    ext_domains = tld['external_domains']
    for ext in ext_domains:
        total = 0
        for r in RESOURCES:
            total += ext_domains[ext]['resources'][r]
        num_deps[ext] = num_deps[ext] + total if ext in num_deps else total

# Update node sizes in the graph
node_sizes = []
for node in G.nodes:
    node_sizes.append(num_deps[node] * DEFAULT_NODE_SIZE)

# Update node labels in the graph
labels = {}
for node, size in zip(G.nodes, node_sizes):
    if size >= MIN_DEPENDENCIES:
        labels[node] = node
    elif node in [tld['top_domain'] for tld in TLDs]:
        labels[node] = node
    else:
        labels[node] = ''


################################################################################
# Drawing
################################################################################
nx.draw(G, with_labels=True, font_color='r', font_size=5, node_color="skyblue", node_size=node_sizes, labels=labels)
plt.show()
