''' Plot the shared dependencies across multiple top level domains (TLD) '''
import os
import json
import networkx as nx
import matplotlib.pyplot as plt

DEFAULT_NODE_SIZE = 150
DATA_DIR = 'data/pgh/'
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

# Generate list of shared dependences
# A dependency is shared when "external_domain" exists for many "top_domains"
shared_deps_edgelist = []
for edge in edgelist:
    all_other_ext_domains = [e[1] for e in edgelist if e != edge]
    if edge[1] in all_other_ext_domains:
        shared_deps_edgelist.append(edge)

# Generate Graph
G = nx.from_edgelist(shared_deps_edgelist)


################################################################################
# Parameter adjusting (labels, node sizes, etc.)
################################################################################
# Count the number of dependencies (used to determine node size)
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
node_sizes = [num_deps[node] * DEFAULT_NODE_SIZE for node in G.nodes]
print(node_sizes)
print(len(G.nodes))
print(len(node_sizes))


################################################################################
# Drawing
################################################################################
nx.draw(G, with_labels=True, font_color='k', font_size=5, node_sizes=node_sizes)
plt.show()
