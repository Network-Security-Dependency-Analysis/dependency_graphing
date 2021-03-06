''' Plot the shared dependencies across multiple top level domains (TLD) or IoT Device '''
import os
import json
import argparse
import networkx as nx
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Generate shared dependency graph for multiple TLDs or IoT Devices')
parser.add_argument('-i', dest='input_dir', type=str, help='Directory for JSON files', required=True)
parser.add_argument('-n', dest='node_size', type=int, help='Integer node size', default=50)
args = parser.parse_args()

DEFAULT_NODE_SIZE = args.node_size
DEFAULT_ROOT_NODE_COLOR = 'pink'
DEFAULT_NODE_COLOR = 'skyblue'
DATA_DIR = args.input_dir

# Types of resources
# 'total', 'a', 'script', 'link', 'iframe', 'video', 'audio', 'img', 'embed', 'object'
RESOURCES = ['total']


################################################################################
# Initial Graph Generation
################################################################################
# Retrieve the json data on dependencies
data_files = []
for fname in os.listdir(DATA_DIR):
    if not fname.endswith('.json'): continue
    with open(DATA_DIR + fname) as f:
        data_files.append(json.load(f))

# Generate list of edges between all nodes
edgelist = []
root_nodes = []
for d in data_files:
    # This is a web dependency graph
    if 'top_domain' in d.keys():
        top_domain = d['top_domain']
        ext_domains = d['external_domains']
        root_nodes.append(top_domain)
        for ext_domain in ext_domains:
            edgelist.append((top_domain, ext_domain))
    # This is an IoT device dependency graph
    elif 'Name' in d.keys() and 'MAC' in d.keys() and 'IPs' in d.keys():
        device_name = d['Name']
        root_nodes.append(device_name)
        for ext_ip in d['IPs']:
            asorg = d['IPs'][ext_ip]['as_org']
            if not asorg:
                asorg = "UNKNOWN"
            edgelist.append((device_name, ext_ip + '\n' + asorg))

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
# All root nodes and external IPs/domains are saved to the dictionary along with
# a tally of how many times they are referenced
num_deps = {}
for d in data_files:
    # This is a web dependency graph
    if 'top_domain' in d.keys():
        num_deps[d['top_domain']] = 1
        for ext_dom in d['external_domains']:
            total = 0
            for r in RESOURCES:
                total += d['external_domains'][ext_dom]['resources'][r]
            if ext_dom in num_deps:
                num_deps[ext_dom] = num_deps[ext_dom] + total
            else:
                num_deps[ext_dom] = total
    # This is an IoT device dependency graph
    elif 'Name' in d.keys() and 'MAC' in d.keys() and 'IPs' in d.keys():
        device_name = d['Name']
        num_deps[device_name] = 1
        for ext_ip in d['IPs']:
            asorg = d['IPs'][ext_ip]['as_org']
            if not asorg:
                asorg = "UNKNOWN"
            ext_name = ext_ip + '\n' + asorg
            if ext_name in num_deps:
                num_deps[ext_name] = num_deps[ext_name] + 1
            else:
                num_deps[ext_name] = 1

# Update node sizes in the graph
node_sizes = [num_deps[node] * DEFAULT_NODE_SIZE for node in G.nodes]

# Change node colors for the TLD
node_colors = []
for node in G.nodes:
    if node in root_nodes:
        node_colors.append(DEFAULT_ROOT_NODE_COLOR)
    else:
        node_colors.append(DEFAULT_NODE_COLOR)

# Change node sizes for the TLD
for i, node in enumerate(G.nodes):
    if node in root_nodes:
        node_sizes[i] = 2000


################################################################################
# Drawing
################################################################################
nx.draw(G, with_labels=True, font_size=5, node_size=node_sizes, node_color=node_colors)
plt.show()
