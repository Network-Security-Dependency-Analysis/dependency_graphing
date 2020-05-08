''' Plot the DNS dependency graph for a single top level domain (TLD) or IoT Device '''
import json
import argparse
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Get input data
parser = argparse.ArgumentParser(description='Generate dependency graph for a single TLD or IoT Device')
parser.add_argument('-i', dest='input_file', type=str, help='Input JSON file', required=True)
parser.add_argument('-n', dest='node_size', type=int, help='Integer node size', default=50)
args = parser.parse_args()

DATA_FILE = args.input_file
DEFAULT_NODE_SIZE = args.node_size  # library default is 300
DEFAULT_ROOT_NODE_COLOR = 'pink'
DEFAULT_NODE_COLOR = 'skyblue'

# Retrieve the json data on dependencies
with open(DATA_FILE) as f:
    data = json.load(f)

# Generate edge list
edgelist = []
node_sizes = [20000] # Make the center node very big for readability
node_colors = [DEFAULT_ROOT_NODE_COLOR]

# Keep track of sizes for each node based on how many references each DNS name has
nodes = {}

# This is a web dependency graph
if 'top_domain' in data.keys():
    top_domain = data['top_domain']
    for ext_domain in data['external_domains']:
        if data['external_domains'][ext_domain]['authoritative_name_servers']:
            for dns_server in data['external_domains'][ext_domain]['authoritative_name_servers']:
                asorg = data['external_domains'][ext_domain]['authoritative_name_servers'][dns_server]['asn_org']
                if asorg in nodes.keys():
                    nodes[asorg]['refs'] += data['external_domains'][ext_domain]['resources']['total']
                else:
                    nodes[asorg] = {'refs': data['external_domains'][ext_domain]['resources']['total']}
    for node in nodes:
        edgelist.append((top_domain, node))
        size = nodes[node]['refs'] + DEFAULT_NODE_SIZE
        node_sizes.append(size)
        node_colors.append(DEFAULT_NODE_COLOR)
# This is an IoT device dependency graph
elif 'Name' in data.keys() and 'MAC' in data.keys() and 'IPs' in data.keys():
    device_name = data['Name']
    for dns in data['DNS']:
        if dns in nodes.keys():
            nodes[dns]['refs'] += data['DNS'][dns]['count']
        else:
            nodes[dns] = {'refs': data['DNS'][dns]['count']}
    for node in nodes:
        edgelist.append((device_name, node))
        size = nodes[node]['refs'] * DEFAULT_NODE_SIZE
        node_sizes.append(size)
        node_colors.append(DEFAULT_NODE_COLOR)

# Generate Graph
G = nx.from_edgelist(edgelist)

# Plot it
nx.draw(G, with_labels=True, font_size=12, node_color=node_colors, node_size=node_sizes)
plt.show()
