''' Plot the dependency graph for a single top level domain (TLD) or IoT Device '''
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

# Retrieve the json data on dependencies
with open(DATA_FILE) as f:
    data = json.load(f)

# Generate edge list
edgelist = []
node_sizes = [DEFAULT_NODE_SIZE]

# This is a web dependency graph
if 'top_domain' in data.keys():
    top_domain = data['top_domain']
    for ext_domain in data['external_domains']:
        if data['external_domains'][ext_domain]['resources']['total'] > 10:
            edgelist.append((top_domain, ext_domain))
            node_sizes.append(data['external_domains'][ext_domain]['resources']['total'] * DEFAULT_NODE_SIZE)
# This is an IoT device dependency graph
elif 'Name' in data.keys() and 'MAC' in data.keys() and 'IPs' in data.keys():
    device_name = data['Name']
    for ext_ip in data['IPs']:
        if data['IPs'][ext_ip]['count'] > 10:
            asorg = data['IPs'][ext_ip]['as_org']
            if not asorg:
                asorg = "UNKNOWN"
            edgelist.append((device_name, ext_ip + '\n' + asorg))
            node_sizes.append(data['IPs'][ext_ip]['count'] * DEFAULT_NODE_SIZE)

# Generate Graph
G = nx.from_edgelist(edgelist)

# Plot it
nx.draw(G, with_labels=True, font_size=12, node_color="skyblue", node_size=node_sizes)
plt.show()
