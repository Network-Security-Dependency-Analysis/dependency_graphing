''' Plot the dependency graph for a multiple top level domains (TLD) '''
import os
import json
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

DEFAULT_NODE_SIZE = 1  # library default is 300
DEFAULT_ROOT_NODE_SIZE = 2000
DEFAULT_NODE_COLOR = 'skyblue'
DEFAULT_ROOT_NODE_COLOR = 'pink'
MIN_DEPENDENCIES = 5
DATA_DIR = 'data/pgh2/'

# Types of resources
# 'total', 'a', 'script', 'link', 'iframe', 'video', 'audio', 'img', 'embed', 'object'
# RESOURCES = ['script', 'link', 'iframe']
RESOURCES = ['total']


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
root_nodes = []
for tld in TLDs:
    top_domain = tld['top_domain']
    ext_domains = tld['external_domains']
    root_nodes.append(top_domain)
    for ext_domain in ext_domains:
        edgelist.append((top_domain, ext_domain))

# Generate list of edges between nodes which are dependent on a RESOURCE
# Only keep edges using the resources that we care about
resource_edgelist = []
for tld in TLDs:
    top_domain = tld['top_domain']
    ext_domains = tld['external_domains']
    for ext in ext_domains:
        total = 0
        for r in RESOURCES:
            total += ext_domains[ext]['resources'][r]
        if total != 0:
            resource_edgelist.append((top_domain, ext))

# Generate Graph
G = nx.from_edgelist(resource_edgelist)


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

# Change node colors for the top level domains
node_colors = []
for node in G.nodes:
    if node in root_nodes:
        node_colors.append(DEFAULT_ROOT_NODE_COLOR)
    else:
        node_colors.append(DEFAULT_NODE_COLOR)

# Change node sizes for the top level domains
for i, node in enumerate(G.nodes):
    if node in root_nodes:
        node_sizes[i] = DEFAULT_ROOT_NODE_SIZE


################################################################################
# Drawing
################################################################################
nx.draw(G, with_labels=True, font_size=5, node_color=node_colors, node_size=node_sizes, labels=labels)
# nx.draw(G, with_labels=True, font_size=5, node_color=node_colors, node_size=node_sizes)
plt.show()
