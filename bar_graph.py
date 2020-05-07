import json
import matplotlib.pyplot as plt
import numpy as np

DATA_FILE = "../web_dependencies/data/pittsburgh/0f2ccf8052574eb576b45b1eda666925a5eea9ee.json"

# Retrieve the json data on dependencies
with open(DATA_FILE) as f:
    data = json.load(f)

domains = []
counts = []

for ext_domain in data["external_domains"]:
	if data["external_domains"][ext_domain]["resources"]["total"] > 20:
		domains.append(ext_domain)
		counts.append(data["external_domains"][ext_domain]["resources"]["total"])

plt.rcdefaults()
fig, ax = plt.subplots()
y_pos = np.arange(len(domains))

ax.barh(y_pos, counts, align="center")
ax.set_yticks(y_pos)
ax.set_yticklabels(domains)
ax.set_xlabel("Number of domain references")
ax.set_title("External domain references for " + data["top_domain"])

plt.show()